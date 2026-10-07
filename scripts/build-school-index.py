#!/usr/bin/env python3
"""
逐校情报索引生成器 (build-school-index.py)
==========================================
把 school-registry-*.md 与 school-updates-*.md 解析成结构化索引，供
`school-info.py` 按校名取单条——从此「某校情报」不再需要整读 markdown。

产物（默认写到 {SKILL_DIR}/data/）：
    schools.json        逐校情报：校名 / 别名 / 地区 / 来源文件 / 行号区间 / 正文
    updates-index.json  月度案例日志索引：日期 / 学生 / 主题 / 涉及学校 / 来源 / 行号
    manifest.json       源文件指纹，供 school-info.py 判断索引是否过期

用法：
    python3 scripts/build-school-index.py            # 生成/刷新
    python3 scripts/build-school-index.py --check    # 只校验索引是否与源文件同步（供闸门用）

⚠️ 本脚本只读 markdown、只写 data/ 下的 json，不改动源文件。
"""

import argparse
import hashlib
import json
import os
import re
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF_DIR = os.path.join(SKILL_DIR, "references")
DATA_DIR = os.path.join(SKILL_DIR, "data")

REGISTRY_GLOB = "school-registry-"
UPDATES_GLOB = "school-updates-"
# 月度分册索引用，不作为案例来源
UPDATES_SKIP = {"school-updates-log.md"}

REGION_RE = re.compile(r"^##\s+(.*?)\s*$")
SCHOOL_RE = re.compile(r"^####\s+(.*?)\s*$")
UPDATE_SEC_RE = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})[^\n（(]*[（(]([^）)]*)[）)]\s*$")

# 校名里要去掉的装饰与附注
EMOJI_RE = re.compile("[\U0001F1E6-\U0001F1FF\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]")
TRAIL_NOTE_RE = re.compile(r"\s*[（(]\s*(?:\d{4}-\d{2}-\d{2}|update|NEW|新)[^）)]*[）)]\s*$", re.I)
ABBR_RE = re.compile(r"\b([A-Z][A-Za-z&]*(?:[-(][A-Za-z0-9]+[)])?)\b")


def clean_name(raw):
    """把 `#### 🇦🇺 University of Melbourne（2026-09-20）` 洗成规范校名。"""
    s = EMOJI_RE.sub("", raw).strip()
    s = TRAIL_NOTE_RE.sub("", s).strip()
    s = re.sub(r"\s*⚠️\s*$", "", s).strip()
    return s


# `####` 在这些文件里兼作小标题，必须把「不是学校」的挑出来剔掉，
# 否则索引里会混进「1. 写完必须跑…」「抓取作业注意」这类条目。
NOT_SCHOOL_NUM = re.compile(r"^\d+\s*[.、)）]")
NOT_SCHOOL_PUNCT = re.compile(r"[：，。；]")
CHINESE_SCHOOL_WORD = re.compile(r"大学|學院|学院|理工|科技大|都会大|浸會|浸会|师范|科大")
LATIN_TOKEN = re.compile(r"[A-Za-z]{3,}")


def is_school_heading(name):
    if not name or len(name) > 60:
        return False
    if NOT_SCHOOL_NUM.match(name) or NOT_SCHOOL_PUNCT.search(name):
        return False
    return bool(LATIN_TOKEN.search(name) or CHINESE_SCHOOL_WORD.search(name))


ALIAS_STOP = {"EXCLUDED", "REVIEWED", "AVAILABILITY", "NEW", "SPA", "OK", "NA",
              "URL", "GRE", "PDF", "API", "HTML", "CSS", "JS", "TBD", "TODO",
              "UK", "US", "USA", "HK", "MO", "CN", "NZ", "AU", "EU", "SG"}


def aliases_for(name, body):
    """只取原文出现过的缩写，不臆造。"""
    out = set()
    for m in re.finditer(r"[（(]([A-Z][A-Za-z0-9&.\- ]{1,14})[）)]", name):
        out.add(m.group(1).strip())
    for m in re.finditer(r"`([^`\n]{1,16})`", body):
        tok = m.group(1).strip()
        if not tok:
            continue
        # 拉丁缩写：全大写或含数字（HKU / HKUST(GZ) / BNBU）；中文简称：含学校词且 ≤8 字
        if re.fullmatch(r"[A-Z][A-Z0-9&.()\-]{1,14}", tok) or \
           (len(tok) <= 8 and CHINESE_SCHOOL_WORD.search(tok)):
            if tok.upper() in ALIAS_STOP:
                continue
            out.add(tok)
    out.discard(name)
    return sorted(out)


def region_code(filename):
    m = re.match(REGISTRY_GLOB + r"(.+)\.md$", filename)
    return m.group(1) if m else ""


def parse_registry(path, section_state):
    """解析一个地区分册。section 取最近的 ## 标题（仅作定位提示）。"""
    recs = []
    text = open(path, encoding="utf-8-sig").read()
    lines = text.split("\n")
    src = os.path.basename(path)
    rcode = region_code(src)
    cur = None
    for i, line in enumerate(lines):
        if line.startswith("#### "):
            pass
        elif REGION_RE.match(line):
            title = clean_name(REGION_RE.match(line).group(1))
            if title:
                section_state[0] = title
            if cur:
                recs.append(cur)
                cur = None
            continue
        m = SCHOOL_RE.match(line)
        if m:
            if cur:
                recs.append(cur)
                cur = None
            name = clean_name(m.group(1))
            if is_school_heading(name):
                cur = {"name": name, "rawHeading": m.group(1), "section": section_state[0],
                       "region": rcode, "source": src, "lineStart": i + 1, "bodyLines": []}
            continue
        if cur is not None:
            cur["bodyLines"].append(line)
    if cur:
        recs.append(cur)

    out = []
    for r in recs:
        body = "\n".join(r.pop("bodyLines")).strip()
        r["lineEnd"] = r["lineStart"] + len(body.split("\n"))
        r["body"] = body
        r["aliases"] = aliases_for(r["name"], body)
        out.append(r)
    return out


def parse_updates(path):
    """解析一个月度案例分册：按 ## YYYY-MM-DD … 切块。"""
    text = open(path, encoding="utf-8-sig").read()
    lines = text.split("\n")
    src = os.path.basename(path)
    out, cur = [], None
    for i, line in enumerate(lines):
        m = UPDATE_SEC_RE.match(line)
        h2 = re.match(r"^##\s+(.*?)\s*$", line)
        if m:
            if cur:
                out.append(cur)
            inner = m.group(2)
            student, _, topic = inner.partition("—")
            cur = {"date": m.group(1), "student": student.strip(),
                   "topic": topic.strip() or student.strip(),
                   "source": src, "lineStart": i + 1, "bodyLines": []}
            continue
        if h2:
            if cur:
                out.append(cur)
            raw = h2.group(1)
            dm = re.match(r"^(\d{4}-\d{2}-\d{2})\s*(.*)$", raw)
            cur = {"date": dm.group(1) if dm else "",
                   "student": "", "topic": dm.group(2) if dm else clean_name(raw),
                   "source": src, "lineStart": i + 1, "bodyLines": []}
            continue
        if cur is not None:
            cur["bodyLines"].append(line)
    if cur:
        out.append(cur)

    for r in out:
        body = "\n".join(r.pop("bodyLines")).strip()
        r["lineEnd"] = r["lineStart"] + len(body.split("\n"))
        r["schools"] = sorted({clean_name(x) for x in SCHOOL_RE.findall(body)
                               if is_school_heading(clean_name(x))})
        # 保留完整正文：案例日志的价值就在正文里的校名与术语，只存摘要会漏检
        r["body"] = body
        r["summary"] = re.sub(r"\s+", " ", body)[:600]
        if not r["topic"]:
            r["topic"] = r["schools"][0] if r["schools"] else "(未命名)"
    return [r for r in out if r.get("topic")]


def fingerprint(paths):
    out = {}
    for p in paths:
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        out[os.path.basename(p)] = {"sha256": h.hexdigest(),
                                    "bytes": os.path.getsize(p)}
    return out


def collect_sources():
    reg, upd = [], []
    for fn in sorted(os.listdir(REF_DIR)):
        if not fn.endswith(".md"):
            continue
        if fn.startswith(REGISTRY_GLOB):
            reg.append(os.path.join(REF_DIR, fn))
        elif fn.startswith(UPDATES_GLOB) and fn not in UPDATES_SKIP:
            upd.append(os.path.join(REF_DIR, fn))
    return reg, upd


def build():
    reg_paths, upd_paths = collect_sources()
    schools = []
    for p in reg_paths:
        schools.extend(parse_registry(p, [""]))
    updates = []
    for p in upd_paths:
        updates.extend(parse_updates(p))

    # 同名合并（跨分册重复时保留来源最多的那条，并合并来源列表）
    merged = {}
    for r in schools:
        key = r["name"].lower()
        if key in merged:
            merged[key].setdefault("alsoIn", []).append(r["source"])
            continue
        merged[key] = r
    schools = sorted(merged.values(), key=lambda r: r["name"].lower())
    updates.sort(key=lambda r: (r["date"] or "0000", r["source"]))

    os.makedirs(DATA_DIR, exist_ok=True)
    man = {"schools": len(schools), "updates": len(updates),
           "sources": fingerprint(reg_paths + upd_paths + [os.path.join(REF_DIR, f)
                                                           for f in UPDATES_SKIP
                                                           if os.path.exists(os.path.join(REF_DIR, f))])}
    for fn, payload in (("schools.json", schools),
                        ("updates-index.json", updates),
                        ("manifest.json", man)):
        with open(os.path.join(DATA_DIR, fn), "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=1)
    return man


def check():
    """返回 (是否同步, 说明)。供 skill-budget.py 调用。"""
    man_path = os.path.join(DATA_DIR, "manifest.json")
    if not os.path.exists(man_path):
        return False, "索引不存在，请先跑 build-school-index.py"
    man = json.load(open(man_path, encoding="utf-8"))
    reg_paths, upd_paths = collect_sources()
    extra = [os.path.join(REF_DIR, f) for f in UPDATES_SKIP]
    cur = fingerprint([p for p in reg_paths + upd_paths + extra if os.path.exists(p)])
    old = man.get("sources", {})
    drift = []
    for k, v in cur.items():
        if k not in old:
            drift.append(f"新增源文件 {k}")
        elif old[k]["sha256"] != v["sha256"]:
            drift.append(f"源文件已改动 {k}")
    for k in old:
        if k not in cur:
            drift.append(f"源文件已删除 {k}")
    if drift:
        return False, "索引过期：" + "；".join(drift[:6])
    return True, f"索引与源文件同步（{man['schools']} 校 / {man['updates']} 条案例）"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只校验索引是否与源文件同步")
    args = ap.parse_args()
    if args.check:
        ok, msg = check()
        print(("KS_SCHOOL_INDEX_OK " if ok else "KS_SCHOOL_INDEX_STALE ") + msg)
        return 0 if ok else 1
    man = build()
    print(f"KS_SCHOOL_INDEX_BUILT 学校 {man['schools']} 条 / 案例 {man['updates']} 条 "
          f"/ 源文件 {len(man['sources'])} 个 → {DATA_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
