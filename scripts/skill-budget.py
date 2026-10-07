#!/usr/bin/env python3
"""
技能预算闸门 (skill-budget.py)
==============================
检查技能是否超出既定预算，超了**直接报错退出非零**。

为什么需要它：2026-10-07 之前，本技能从 274 KB 整理过一次，但一个月内 references
又靠「按时间追加案例日志」长回来。**没有预算上限，半年后会回到原点。** 这是唯一能
防止回涨的机制——所以它必须能被随时跑、且失败能被看见。

用法:
    python3 scripts/skill-budget.py            # 检查并以退出码表达结论
    python3 scripts/skill-budget.py --quiet    # 只输出结论行
    python3 scripts/skill-budget.py --json /tmp/budget.json

退出码:
    0  全部在预算内
    1  有超预算项（不要无视；要么拆文件，要么按下面第 3 步合法上调预算）
    2  用法错误

预算来源：技能改造方案（2026-10-07）第三节「目标结构」的预算表。
调整预算的正确做法：先说明为什么现有预算不合理，改本文件顶部的 BUDGET 常量，
**不要**为了让检查变绿而临时放宽。
"""

import argparse
import json
import os
import re
import subprocess
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF_DIR = os.path.join(SKILL_DIR, "references")

# ── 预算（唯一事实来源） ───────────────────────────────────────────────────────
BUDGET = {
    "skill_lines":            300,      # L0 常驻正文
    "skill_chars":          12000,
    "required_read_lines":    200,      # 任何被标「必读/整读」的文件
    "reference_lines":        500,      # 任何 references 单文件（超了就拆）
    "read_aloud_files":         3,      # 每次任务需「整读」的文件数上限
}

# 每次调用技能都会被读到的（L0）
LAYER0 = ["SKILL.md"]

# 每次任务需要整读的（L1 规则 + 当前阶段手册；阶段手册一次只读一本）
ALWAYS_READ = ["references/rules-write.md"]
PHASE_READ_ONE_OF = ["references/search-phase.md",
                     "references/write-phase.md",
                     "references/review-phase.md"]

# 明确不参与 200 行线的例外（这些是按需定位的案例库/查询型数据，不是必读）
NOT_REQUIRED_READ = {"cases-rules.md"}


def lines_of(path):
    with open(path, encoding="utf-8-sig") as fh:
        return fh.read()


def count(text):
    return len(text.split("\n")), len(text)


def report(rows, quiet):
    """rows: [(级别, 名称, 实测, 预算, 说明)]"""
    if not quiet:
        print(f"{'级别':<6}{'对象':<42}{'实测':>10}{'预算':>10}  说明")
        print("-" * 100)
        for lvl, name, got, bud, note in rows:
            mark = {"OK": "OK", "FAIL": "FAIL", "WARN": "WARN"}[lvl]
            g = f"{got}" if got != "" else "-"
            b = f"{bud}" if bud != "" else "-"
            print(f"{mark:<6}{name[:41]:<42}{g:>10}{b:>10}  {note}")


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--json")
    ap.add_argument("--skip-selftest", action="store_true")
    args = ap.parse_args()

    rows, fails, warns = [], [], []

    # 1. L0 常驻正文
    for rel in LAYER0:
        p = os.path.join(SKILL_DIR, rel)
        if not os.path.exists(p):
            rows.append(("FAIL", rel, "", "", "文件不存在"))
            fails.append(rel)
            continue
        text = lines_of(p)
        n, c = count(text)
        for key, got, unit in (("skill_lines", n, "行"), ("skill_chars", c, "字")):
            bud = BUDGET[key]
            if got > bud:
                rows.append(("FAIL", f"{rel}（{unit}）", got, bud,
                             f"超出 {got - bud}{unit}，需把成节内容迁到 references/"))
                fails.append(f"{rel}:{key}")
            else:
                rows.append(("OK", f"{rel}（{unit}）", got, bud, ""))

    # 2. 被标「必读 / 整读」的文件 ≤200 行
    for rel in ALWAYS_READ + PHASE_READ_ONE_OF:
        p = os.path.join(SKILL_DIR, rel)
        if not os.path.exists(p):
            rows.append(("FAIL", rel, "", "", "文件不存在"))
            fails.append(rel)
            continue
        n, _ = count(lines_of(p))
        bud = BUDGET["required_read_lines"]
        if n > bud:
            rows.append(("FAIL", rel, n, bud, "标着必读却读不完——拆成规则本 + 案例本"))
            fails.append(rel)
        else:
            rows.append(("OK", rel, n, bud, ""))

    # 3. references 单文件 ≤500 行
    oversized = []
    if os.path.isdir(REF_DIR):
        for fn in sorted(os.listdir(REF_DIR)):
            if not fn.endswith(".md") or fn in NOT_REQUIRED_READ:
                # NOT_REQUIRED_READ 仍受 500 行约束，只是不参与 200 行线；这里继续检查
                pass
            if not fn.endswith(".md"):
                continue
            n, _ = count(lines_of(os.path.join(REF_DIR, fn)))
            if n > BUDGET["reference_lines"]:
                oversized.append((fn, n))
    for fn, n in oversized:
        rows.append(("FAIL", f"references/{fn}", n, BUDGET["reference_lines"],
                     f"超 {n - BUDGET['reference_lines']} 行，按预算规则应拆"))
        fails.append(f"references/{fn}")
    if not oversized:
        rows.append(("OK", "references/*.md（单文件行数）", "全部达标", BUDGET["reference_lines"], ""))

    # 4. 每次任务需整读的文件数 ≤3（SKILL.md + rules-write + 1 本阶段手册）
    n_read = len(LAYER0) + len(ALWAYS_READ) + 1
    bud = BUDGET["read_aloud_files"]
    if n_read > bud:
        rows.append(("FAIL", "每次任务需整读的文件数", n_read, bud, "阶段手册只能读当前那本"))
        fails.append("read_aloud_files")
    else:
        rows.append(("OK", "每次任务需整读的文件数", n_read, bud,
                     "SKILL.md + rules-write.md + 当前阶段手册"))

    # 5. 逐校索引是否与源文件同步（防止索引悄悄过期后给出旧情报）
    idx = os.path.join(SKILL_DIR, "scripts", "build-school-index.py")
    if os.path.exists(idx):
        r = subprocess.run([sys.executable, idx, "--check"], capture_output=True, text=True)
        ok = r.returncode == 0
        rows.append(("OK" if ok else "FAIL", "逐校索引与源文件同步",
                     "", "", (r.stdout or r.stderr).strip()[:80]))
        if not ok:
            fails.append("school-index-stale")

    # 6. audit-all.py 自检（改正则后必须仍全过）
    if not args.skip_selftest:
        aa = os.path.join(SKILL_DIR, "scripts", "audit-all.py")
        if os.path.exists(aa):
            r = subprocess.run([sys.executable, aa, "--self-test"], capture_output=True, text=True)
            ok = "KS_AUDIT_ALL_SELFTEST_OK" in (r.stdout or "")
            rows.append(("OK" if ok else "FAIL", "audit-all.py 自检", "", "",
                         "备注正则与职称门槛回归通过" if ok else "自检未通过，改正则后必须让它恢复绿色"))
            if not ok:
                fails.append("audit-all-selftest")

    report(rows, args.quiet)

    verdict = "pass" if not fails else "fail"
    line = (f"KS_SKILL_BUDGET_{verdict.upper()} 超预算 {len(fails)} 项"
            + ("：" + ", ".join(fails[:8]) if fails else "（全部在预算内）"))
    print("\n" + line)

    if fails:
        print("\n处置：① 拆文件（首选）→ ② 把规则/案例分离 → "
              "③ 只有在现有预算确实不合理时才改脚本顶部 BUDGET，并说明理由。")

    if args.json:
        with open(os.path.expanduser(args.json), "w", encoding="utf-8") as fh:
            json.dump({"verdict": verdict,
                       "budget": BUDGET,
                       "fail": fails,
                       "rows": [{"level": l, "name": n, "got": g, "budget": b, "note": note}
                                for l, n, g, b, note in rows]},
                      fh, ensure_ascii=False, indent=1)

    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
