#!/usr/bin/env python3
"""
逐校情报查询 (school-info.py)
=============================
按校名取**单条**情报，永不整读 markdown。

用法:
    python3 scripts/school-info.py HKU
    python3 scripts/school-info.py "University of Melbourne"
    python3 scripts/school-info.py 港科广 --updates      # 只查月度案例日志
    python3 scripts/school-info.py UCL --all             # 列出全部命中（只看名字）
    python3 scripts/school-info.py cityu --json
    python3 scripts/school-info.py --list                # 列出索引里全部学校

输出:
    默认打印最佳命中 1 条的正文 + 来源文件与行号区间。
    **只需要看那一段时**，用行号做定向读取，不要 Read 整个文件：
        例：Read references/school-registry-hk-mo-cn.md offset=<lineStart> limit=<行数>

退出码:
    0  有命中
    1  无命中（索引里有 95 所校；确认校名拼写，或用 --list 看有什么）
    2  索引不存在或已过期 → 先跑 scripts/build-school-index.py

⚠️ 索引与源文件可能不同步（源 markdown 被改过）。本脚本每次都会校验指纹，
   过期时直接报错而不是给出旧数据。
"""

import argparse
import json
import os
import re
import subprocess
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SKILL_DIR, "data")


def load(name):
    p = os.path.join(DATA_DIR, name)
    if not os.path.exists(p):
        print(f"[ERROR] 索引不存在：{p}\n        先跑：python3 scripts/build-school-index.py",
              file=sys.stderr)
        sys.exit(2)
    return json.load(open(p, encoding="utf-8"))


def ensure_fresh():
    """索引过期就报错，不给旧数据（宁可失败也不要给出与源文件不一致的结论）。"""
    mf = os.path.join(DATA_DIR, "manifest.json")
    if not os.path.exists(mf):
        return
    r = subprocess.run(
        [sys.executable, os.path.join(SKILL_DIR, "scripts", "build-school-index.py"), "--check"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print("[ERROR] 逐校索引已过期，结果不可信。请先跑：\n"
              "        python3 scripts/build-school-index.py\n"
              f"        （{r.stdout.strip() or r.stderr.strip()}）", file=sys.stderr)
        sys.exit(2)


def score(rec, q):
    """命中打分。顺序很关键：**别名精确匹配必须排在名字子串之前**，
    否则查 HKU 会先被 HKUST 的名字子串命中而返回错误学校。"""
    ql = q.lower()
    name = (rec.get("name") or rec.get("topic") or "").lower()
    if name == ql:
        return 100
    for a in rec.get("aliases", []):
        if a.lower() == ql:
            return 90
    if ql in name:
        return 70
    for a in rec.get("aliases", []):
        if ql in a.lower():
            return 60
    for s in rec.get("schools", []):
        if ql in s.lower():
            return 55
    hay = (rec.get("body") or rec.get("summary") or "").lower()
    if ql in hay:
        return 30
    return 0


def search(records, q, deep=True):
    hits = []
    for r in records:
        s = score(r, q)
        if s or (deep and q.lower() in json.dumps(r, ensure_ascii=False).lower()):
            hits.append((s or 10, r))
    hits.sort(key=lambda x: (-x[0], x[1].get("name") or x[1].get("topic", "")))
    return hits


def print_school(r, idx, total):
    print(f"=== 命中 {idx}/{total} ===")
    print(f"校名    : {r['name']}")
    if r.get("aliases"):
        print(f"别名    : {', '.join(r['aliases'])}")
    print(f"地区分册: {r['region']}   所属小节: {r.get('section','')}")
    print(f"来源    : references/{r['source']}  行 {r['lineStart']}-{r['lineEnd']}"
          f"（共 {r['lineEnd'] - r['lineStart'] + 1} 行）")
    if r.get("alsoIn"):
        print(f"其他分册: {', '.join(r['alsoIn'])}")
    print("-" * 70)
    print(r.get("body", "").strip())
    print("-" * 70)


def print_update(r, idx, total):
    print(f"=== 命中 {idx}/{total} ===")
    print(f"日期    : {r.get('date') or '(未标注日期)'}   学生: {r.get('student') or '(未标注)'}")
    print(f"主题    : {r['topic']}")
    if r.get("schools"):
        print(f"涉及学校: {', '.join(r['schools'][:12])}")
    print(f"来源    : references/{r['source']}  行 {r['lineStart']}-{r['lineEnd']}")
    print("-" * 70)
    print(r.get("summary", "").strip())
    print("-" * 70)


def main():
    ap = argparse.ArgumentParser(add_help=True, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="?")
    ap.add_argument("--updates", action="store_true", help="只查月度案例日志")
    ap.add_argument("--schools-only", action="store_true", help="只查逐校情报（默认两者都查）")
    ap.add_argument("--all", action="store_true", help="列出全部命中（只名字）")
    ap.add_argument("--top", type=int, default=1, help="打印前 N 条正文（默认 1）")
    ap.add_argument("--no-deep", action="store_true", help="不做正文全文匹配，只匹配校名与别名")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--list", action="store_true", help="列出索引里全部学校")
    ap.add_argument("--no-fresh-check", action="store_true")
    args = ap.parse_args()

    if not args.no_fresh_check:
        ensure_fresh()

    schools = load("schools.json")
    updates = load("updates-index.json")

    if args.list:
        for r in schools:
            al = f"  ({', '.join(r['aliases'])})" if r.get("aliases") else ""
            print(f"  [{r['region']}] {r['name']}{al}")
        print(f"\n共 {len(schools)} 所；月度案例 {len(updates)} 条。")
        return 0

    if not args.query:
        print(__doc__)
        return 2

    q = args.query
    deep = not args.no_deep
    hits_s, hits_u = [], []
    if not args.updates:
        hits_s = search(schools, q, deep)
    if not args.schools_only:
        hits_u = search(updates, q, deep)

    if args.as_json:
        print(json.dumps({"query": q,
                          "schools": [r for _, r in hits_s[:args.top]],
                          "updates": [r for _, r in hits_u[:args.top]]},
                         ensure_ascii=False, indent=1))
        return 0 if (hits_s or hits_u) else 1

    if args.all:
        for _, r in hits_s:
            print(f"  [{r['region']}] {r['name']}")
        for _, r in hits_u:
            print(f"  [更新日志 {r.get('date') or '—'}] {r['topic'][:50]}  ← {r['source']}")
        if not hits_s and not hits_u:
            print(f"无命中：{q}")
            return 1
        return 0

    if not hits_s and not hits_u:
        print(f"无命中：{q}")
        print("提示：用 --list 看索引里都有哪些学校；或用 --all 做模糊搜索。")
        return 1

    for i, (s, r) in enumerate(hits_s[:args.top], 1):
        print_school(r, i, len(hits_s))
        print()
    for i, (s, r) in enumerate(hits_u[:args.top], 1):
        print_update(r, 1, len(hits_u))
        print()

    if len(hits_s) > args.top:
        print(f"（另有 {len(hits_s) - args.top} 条逐校命中，用 --all 查看："
              + "; ".join(r["name"] for _, r in hits_s[args.top:args.top + 6]) + "）")
    if len(hits_u) > args.top:
        print(f"（另有 {len(hits_u) - args.top} 条案例命中，用 --updates --all 查看）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
