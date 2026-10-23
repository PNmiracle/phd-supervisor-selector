#!/usr/bin/env python3
"""
交付前机械复查入口脚本 (audit-all.py)
=====================================
把「交付前机械复查 SOP 10 项」+「链接四关」+「备注语言正则」+「地区职称门槛」
汇成一条命令，出可交付/不可交付的结论。

设计原则（2026-10-07 瘦身改造第 2 步）：
    能机械判定的项，从此不依赖「有没有读到规则」，只依赖「有没有跑脚本」。
    因此本脚本是唯一入口——不要再手写一次性检查脚本。

用法:
    # 最常用：全量十项
    python3 audit-all.py <DATASHEET_ID>

    # 明确指定凭据（不落盘、不回显）
    VIKA_TOKEN=xxx python3 audit-all.py <DATASHEET_ID>
    python3 audit-all.py <DATASHEET_ID> --token-file ~/.vika-token

    # 只跑部分检查（跳过联网项，用于快速自查）
    python3 audit-all.py <DATASHEET_ID> --only notes,fields,title

    # 带学校关联反查（第 5 项）与覆盖完整性（第 10 项）
    python3 audit-all.py <DATASHEET_ID> --main-table-id dstXXX --expected-programs expected.txt

    # 只出机器可读结果
    python3 audit-all.py <DATASHEET_ID> --json /tmp/audit.json --quiet

参数:
    DATASHEET_ID            选导表 datasheetId（必填）
    --token-file PATH       从文件读 token（首行）；也可用环境变量 VIKA_TOKEN
    --only LIST             逗号分隔，只跑这些检查；见 --list-checks
    --skip LIST             逗号分隔，跳过这些检查
    --main-table-id ID      学校主表 datasheetId，用于第 5 项关联反查
    --expected-programs F   逐校总目录里方向对口的项目页 URL 清单（每行一条），
                            用于第 10 项覆盖完整性差集
    --fields LIST           逗号分隔，覆盖必填字段清单
    --max-urls N            链接检查上限（默认 120，0 表示不限）
    --json PATH             同时写出机器可读结果
    --quiet                 不打印逐条明细，只打印汇总
    --no-fail               有 FAIL 也返回 0（仅用于观察，不要用于交付门禁）
    --list-checks           列出全部检查项后退出

退出码:
    0  全部通过
    1  有 FAIL（不可交付）
    2  用法或凭据错误
    3  网络/接口错误，结果不完整（不要当作通过）

凭据安全:
    token 只从环境变量或 --token-file 读取，从不打印、从不写入输出文件。
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict

VIKA_BASE = "https://api.vika.cn/fusion/v1"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# ── 检查项登记表 ────────────────────────────────────────────────────────────────
CHECKS = [
    ("fields",   "1. 字段完整性（含学校关联、导师名重复）"),
    ("name",     "2. 主页命中导师姓名（title / 正文含姓氏）"),
    ("email",    "3. 邮箱域名与主页域名同根"),
    ("links",    "4. 三列链接可达且落点正确（四关：能开 / 落点对 / 是本人页 / 层级对）"),
    ("school",   "5. 学校关联反查（学校名与排名对得上）"),
    ("notes",    "6. 备注语言正则扫（emoji / 方向编号 / 工具名 / 修正语言 / 机器打分 / 元注释 / 误指代）"),
    ("title",    "7+9. 职称：备注首段必须是真实职称，且不低于地区门槛"),
    ("gates",    "8. 三硬门槛待核清单（GRE / 招生年份 / 停招，需人工读官网原文）"),
    ("coverage", "10. 项目与学校覆盖完整性（与总目录清单做差集）"),
    ("evidence", "11. 证据链抽检（抽 3–5 条，看备注/研究领域能否在三个链接正文中找到出处）"),
]
CHECK_IDS = [c[0] for c in CHECKS]

# ── 备注语言正则（第 6 项） ─────────────────────────────────────────────────────
EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF\u2b00-\u2bff\ufe0f\u2705\u26a0]"
)
NOTES_RULES = [
    ("emoji",             "备注含 emoji 符号", EMOJI_RE),
    ("direction-index",   "备注含方向编号（方向N / TOP / SECONDARY / TERTIARY）",
     re.compile(r"方向\s*[0-9０-９]|方向[一二三四五六七八九十]|TOP\s*方向|SECONDARY|TERTIARY|核心匹配")),
    ("tool-name",         "备注含内部工具名或元指代",
     re.compile(r"Vika|维格|源数据|源表|本表|表内|本表其他记录|同一张表|该表|表格")),
    ("amendment",         "备注含修正记录语言",
     re.compile(r"职称修正|已确认|已核实|核实过|以\S{1,6}官方为准|严重高估|写错|更正为")),
    ("machine-score",     "备注含机器打分语言",
     re.compile(r"高度相关|很匹配|完美匹配|匹配度最高|匹配面最广|很契合|直接对话|很有交集|核心人选|契合度")),
    ("meta-note",         "备注含元注释 / 警告标签",
     re.compile(r"【[^】]{0,12}(错误|修正|确认|提示|注意)[^】]{0,12}】|⚠️|✅|❌")),
    # 只抓「指代读者」的语境。注意不要匹配「特拉华大学生物力学」这类「大学生」误报。
    ("wrong-pronoun",     "备注用「学生」指代读者（应用「你」）",
     re.compile(r"(?:和|与|给|向|该|该名|这位|这名)学生")),
    ("draft-language",    "备注含草稿语",
     re.compile(r"试试|再看看|失效|待补|TBD|TODO|待定")),
    ("deadline-task",     "备注把核实责任推给学生",
     re.compile(r"建议先确认|套磁前建议先确认|建议先邮件确认|建议先联系确认")),
    ("guiding-link",      "备注含「文章看这个链接」以外的引导性语言",
     re.compile(r"点击查看|建议阅读|详见链接|请查看链接")),
    ("unlinked-url",      "备注正文出现链接（禁止；仅允许 `文章看这里 <url>` 形式）",
     re.compile(r"(?<!文章看这里 )https?://")),
]

# 用户焊死的固定写法，不算「职称位不在认可集内」
FIXED_TITLE_PHRASES = ("未明确表明监督资格", "应该到退休年龄", "可以后放")

# ── 职称（第 7 + 9 项） ────────────────────────────────────────────────────────
# ✅ 口径已定（2026-10-13 用户裁定）：
#   **英澳的 Senior Lecturer / 高级讲师算合格职称**；「讲师序列一刀切排除」只适用于港澳。
#   依据：规则原文（field-rules.md / rules-write.md §7）只把该排除限定在港澳；且**已交付的**
#   《万文睿 -Supervisor List》(dst3Yxt6clXFzvwZovd 同空间) 表内实际存在「高级讲师」6 条、
#   「讲师」9 条、「Reader」2 条 —— 改行为前本脚本会把那批已交付的记录判为 FAIL。
#   实现：scan_title 接收记录的 Location，港澳仍拦 讲师/lecturer；其他地区放行。
#   港澳门槛说明位置：school-registry-hk-mo-cn.md「HK 地区职称门槛」、
#   selection-rules.md「Region and Title Heuristics」。
TITLE_OK = ("教授", "副教授", "助理教授", "讲座教授", "特聘教授", "杰出教授",
            "高级副教授", "首席教授", "chair professor",
            "高级讲师", "senior lecturer",
            # 英制 Reader 是正式教职（等同副教授级）、通常带博；2026-10-14 加入
            "reader")
TITLE_LOW = ("讲师", "lecturer", "teaching fellow", "instructor",
             "professor of practice", "research assistant professor", "研究助理教授",
             "兼职", "兼職", "adjunct", "visiting", "客座", "emeritus", "荣誉教授",
             "名誉教授", "博士生导师", "博导", "硕导", "导师资格")
# 只在港澳生效的排除项（英澳的 Senior Lecturer / Lecturer 是正式教职，通常可带博）
HK_MO_ONLY_LOW = ("讲师", "lecturer")
HK_MO_REGIONS = ("Hong Kong SAR", "Macao SAR", "香港", "澳门", "澳門")

REQUIRED_FIELDS_DEFAULT = [
    "导师", "Department", "导师主页", "导师联系方式", "导师研究领域",
    "博士申请信息", "其他导师信息", "备注",
]

URL_FIELDS = ["导师主页", "博士申请信息", "其他导师信息"]


# ── 基础工具 ───────────────────────────────────────────────────────────────────
class Findings:
    """按 check id 收集结果。severity: FAIL / WARN / INFO"""

    def __init__(self):
        self.items = []        # (check, severity, record_label, message)
        self.notes = []        # 流程性说明
        self.incomplete = []   # 导致结果不完整的错误

    def add(self, check, severity, label, message):
        self.items.append((check, severity, label, message))

    def fail(self, check, label, message):  self.add(check, "FAIL", label, message)
    def warn(self, check, label, message):  self.add(check, "WARN", label, message)
    def info(self, check, label, message):  self.add(check, "INFO", label, message)

    def by_check(self):
        d = defaultdict(list)
        for it in self.items:
            d[it[0]].append(it)
        return d

    def count(self, severity):
        return sum(1 for it in self.items if it[1] == severity)


def read_token(args):
    if args.token_file:
        try:
            with open(os.path.expanduser(args.token_file), encoding="utf-8") as fh:
                tok = fh.readline().strip()
            return tok or None
        except OSError as e:
            print(f"[ERROR] 无法读取 token 文件: {e}", file=sys.stderr)
            sys.exit(2)
    return os.environ.get("VIKA_TOKEN") or os.environ.get("VIKA_API_TOKEN") or None


def vika_get(datasheet_id, token, path):
    req = urllib.request.Request(
        f"{VIKA_BASE}/datasheets/{datasheet_id}{path}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read())
        except Exception:
            raise RuntimeError(f"HTTP {e.code}")
    except Exception as e:
        raise RuntimeError(str(e)[:120])


def fetch_records(datasheet_id, token, findings):
    """翻页拉全量记录（主表和选导表都走这里）。"""
    out, page = [], 1
    while True:
        try:
            r = vika_get(datasheet_id, token,
                         f"/records?maxRecords=500&pageNum={page}&fieldKey=name")
        except RuntimeError as e:
            findings.incomplete.append(f"拉取 {datasheet_id} 第 {page} 页失败：{e}")
            return out
        data = r.get("data") or {}
        recs = data.get("records") or []
        out.extend(recs)
        total = data.get("total") or 0
        if len(recs) < 500 or page * 500 >= total:
            break
        page += 1
        time.sleep(0.15)
    return out


def field_url(val):
    """Vika URL 字段可能返回 dict {text,link} 或纯字符串。"""
    if not val:
        return ""
    if isinstance(val, dict):
        return (val.get("link") or val.get("text") or "").strip()
    if isinstance(val, list):
        return field_url(val[0]) if val else ""
    return str(val).strip()


def field_text(val):
    """文本/公式/关联字段统一转成可读字符串。"""
    if val is None:
        return ""
    if isinstance(val, str):
        return val
    if isinstance(val, dict):
        return str(val.get("text") or val.get("title") or "")
    if isinstance(val, list):
        return "; ".join(field_text(v) for v in val)
    return str(val)


def rec_label(fields, rid):
    name = field_text(fields.get("导师")) or field_text(fields.get("导师姓名")) or "(未填姓名)"
    return f"{name} [{rid[:10]}]"


def norm_url(u):
    u = u.split("#")[0].rstrip("/")
    u = re.sub(r"^http://", "https://", u)
    return u


def same_landing(orig, final):
    """落点判定：忽略 http→https、加/去 www、尾斜杠差异。"""
    def key(u):
        u = norm_url(u)
        host = re.sub(r"^(https://)?(www\.)?", "", u)
        return host
    return key(orig) == key(final)


def domain_root(host):
    parts = [p for p in host.split(".") if p]
    if len(parts) >= 3 and parts[-2] in ("com", "edu", "org", "gov", "net", "co", "ac"):
        return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


# ── 链接检查（第 2、4 项共用一次抓取） ─────────────────────────────────────────
def curl_probe(url, tmp_dir, idx):
    """返回 dict(code, size, title, final, body_head)"""
    tmp = os.path.join(tmp_dir, f"p{idx}.html")
    try:
        r = subprocess.run(
            ["curl", "-sL", "--compressed", "-m", "30", "-o", tmp,
             "-w", "%{http_code}|%{size_download}|%{url_effective}",
             "-A", UA,
             "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
             "-H", "Accept-Language: en-US,en;q=0.9",
             url],
            capture_output=True, text=True, timeout=45,
        )
        parts = (r.stdout or "").strip().split("|")
        code = parts[0] if parts else "ERR"
        size = parts[1] if len(parts) > 1 else "0"
        final = parts[2] if len(parts) > 2 else url
    except Exception as e:
        return {"code": "ERR", "size": "0", "title": "", "final": url,
                "body_head": "", "err": str(e)[:80]}
    title, head = "", ""
    try:
        with open(tmp, "rb") as fh:
            raw = fh.read()
        m = re.search(rb"<title[^>]*>(.*?)</title>", raw[:120000], re.I | re.S)
        if m:
            title = re.sub(r"\s+", " ", m.group(1).decode("utf-8", "ignore")).strip()[:120]
        body = re.sub(rb"<script.*?</script>", b" ", raw[:200000], flags=re.S | re.I)
        body = re.sub(rb"<style.*?</style>", b" ", body, flags=re.S | re.I)
        body = re.sub(rb"<[^>]+>", b" ", body)
        head = re.sub(r"\s+", " ", body.decode("utf-8", "ignore")).strip()[:4000]
    except Exception:
        pass
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass
    return {"code": code, "size": size, "title": title, "final": final, "body_head": head}


# ── 姓名比对与 JS 页面兜底（2026-10-14 增加，用于消除误报） ──────────────────
TEXT_FOLD = str.maketrans({
    "\u2019": "'", "\u2018": "'", "\u02bc": "'", "\u00b4": "'", "`": "'",
    "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "-", "\u2212": "-", "\u00a0": " ",
})
_CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser",
)
_js_render_cache = {}


def fold_text(s):
    """统一弯引号 / 破折号 / 不间断空格，便于姓名比对。"""
    return (s or "").translate(TEXT_FOLD).lower()


def chrome_render_text(url, timeout=45):
    """用无头浏览器渲染 JS 页面并返回可见文本；不可用时返回 ""。（结果缓存）"""
    if not url:
        return ""
    if url in _js_render_cache:
        return _js_render_cache[url]
    binary = next((b for b in _CHROME_CANDIDATES
                   if os.path.sep in b and os.path.exists(b)), None)
    if binary is None:
        _js_render_cache[url] = ""
        return ""
    tmp_dir = tempfile.mkdtemp(prefix="audit_js_")
    text = ""
    try:
        r = subprocess.run(
            [binary, "--headless=new", "--disable-gpu", "--no-sandbox",
             f"--user-data-dir={tmp_dir}", "--no-first-run",
             "--no-default-browser-check", "--virtual-time-budget=15000",
             "--dump-dom", url],
            capture_output=True, text=True, errors="replace", timeout=timeout,
        )
        raw = r.stdout or ""
        body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
        body = re.sub(r"<style.*?</style>", " ", body, flags=re.S | re.I)
        body = re.sub(r"<[^>]+>", " ", body)
        text = re.sub(r"\s+", " ", body).strip()
    except Exception:
        text = ""
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        try:
            subprocess.run(["pkill", "-f", "audit_js_"], capture_output=True, timeout=10)
        except Exception:
            pass
    _js_render_cache[url] = text
    return text


def classify_link(probe, mentor_lastname, field_name):

    """返回 (severity 或 None, 说明)。None 表示通过。"""
    code = probe["code"]
    size = int(probe.get("size") or 0)
    title = probe.get("title") or ""
    final = probe.get("final") or ""
    head = probe.get("body_head") or ""

    if code in ("404", "410"):
        return "FAIL", f"真 {code}（坏链，必须替换）"
    if code == "000" or code == "ERR":
        return "WARN", f"本机不通（{code}）：可能是域名被墙，换 WebFetch 或该校其它域名复测，勿直接判死"

    # 软 404：200 但正文是 Page Not Found
    if code == "200" and re.search(r"page not found|404 not found|page does not exist|"
                                   r"找不到页面|页面不存在", (title + " " + head), re.I):
        return "FAIL", "返回 200 但正文是 Not Found（软 404）"

    if not same_landing(probe.get("url_original", ""), final) and final:
        return "FAIL", f"落点变了：跳到了 {final[:110]}"

    if code == "403":
        return "WARN", "403：可能是 WAF 也可能是离任页已删，必须 WebFetch 穿透后看正文"
    if code in ("429", "202"):
        return "WARN", f"{code}：反爬或排队，换通道穿透复测"
    if code == "200" and size < 2000 and not title:
        return "WARN", f"200 但仅 {size}B 且无 title：疑似 SPA 壳 / WAF 壳，必须穿透"
    if code == "200" and not title:
        return "WARN", "200 但无 title：换通道确认内容"

    if field_name == "导师主页" and mentor_lastname:
        ln = fold_text(mentor_lastname)
        if len(ln) >= 3 and ln not in fold_text(title + " " + head):
            # 纯 curl 抓不到姓名时，可能是 JS 渲染页（Pure / SPA / 员工门户）。
            # 用无头浏览器复测一次，仍找不到才判 FAIL。
            rendered = chrome_render_text(probe.get("url_original") or probe.get("final") or "")
            if rendered and ln in fold_text(rendered):
                return None, ""
            if rendered:
                return "FAIL", f"页面未出现导师姓氏「{mentor_lastname}」（第三关「是本人页」不过；已用无头浏览器复测）"
            return "WARN", (f"curl 抓取未见导师姓氏「{mentor_lastname}」，且本机无无头浏览器可复测"
                            "（JS 渲染页常见）——请换通道确认是否本人页")
    return None, ""


def scan_notes(text):
    """扫描一段备注文本，返回 [(rule_id, severity, 命中片段)]。check_notes 与自检共用。"""
    out = []
    if not text:
        return out
    for rule_id, _desc, rx in NOTES_RULES:
        m = rx.search(text)
        if not m:
            continue
        if rule_id == "unlinked-url" and "文章看这里" in text:
            leftover = re.sub(r"文章看这里\s*\S+", "", text)
            if not re.search(r"https?://", leftover):
                continue
        sev = "WARN" if rule_id in ("draft-language",) else "FAIL"
        out.append((rule_id, sev, m.group(0)[:40]))
    return out


RULE_DESC = {rid: desc for rid, desc, _ in NOTES_RULES}


def scan_title(text, location=""):
    """判定备注首段的职称位。返回 (severity, 说明) 或 None（通过）。

    location：记录的 Location 字段。2026-10-13 用户裁定——**英澳的 Senior Lecturer /
    高级讲师算合格职称**，「讲师序列一刀切排除」只适用于港澳，故按地区放行。
    """
    text = (text or "").strip()
    if not text:
        return None
    first = re.split(r"[；;]", text)[0].strip().strip("。.")
    if any(ph in first for ph in FIXED_TITLE_PHRASES):
        return "INFO", f"职称位为固定写法「{first[:24]}」，按规则放行"
    low = first.lower()
    in_hkmo = any(k in (location or "") for k in HK_MO_REGIONS)
    ok_hits = [t for t in TITLE_OK if t in low]
    hit_low = []
    for t in TITLE_LOW:
        if t not in low:
            continue
        # 「高级讲师」⊃「讲师」：非港澳放行；港澳仍一并拦截
        if any(t in ok for ok in ok_hits) and not in_hkmo:
            continue
        if t in HK_MO_ONLY_LOW and not in_hkmo:
            continue
        hit_low.append(t)
    if hit_low:
        return "FAIL", f"职称位「{first[:28]}」命中排除项 {hit_low}（讲师序列 / 兼任 / 资格描述一律排除）"
    # 非港澳的「讲师 / Lecturer」是正式教职（英澳 Lecturer ≈ 助理教授、通常可带博），视为合格
    if not in_hkmo and any(t in low for t in HK_MO_ONLY_LOW):
        return None
    if not any(t in low for t in TITLE_OK):
        return "WARN", f"职称位「{first[:28]}」不在认可职称集内，需人工确认（可能是资格描述而非职称）"
    return None


# ── 证据链抽检（第 11 项） ─────────────────────────────────────────────────────
EVIDENCE_FIELDS = ("备注", "导师研究领域")
STOP_PHRASES = ("可以备选一下呢", "可以往", "方向能搭上", "有交叉", "比较对口",
                "未明确表明监督资格", "可以后放", "现在应该到退休年龄", "文章看这里")


def extract_phrases(text, skip_first=False):
    """把字段文本拆成「事实性短语」候选。

    skip_first=True 用于 `备注`：它的首段是职称位，不是事实陈述。
    含套话（关联句 / 备选标识 / 来源链接提示）的整段**整段丢弃**——
    剥离套话后剩下的往往是「和你的设计史」这类残句，留着只会误报。
    """
    if not text:
        return []
    out = []
    for i, seg in enumerate(re.split(r"[；;。\n]", text)):
        s = seg.strip().strip("（）()　 ")
        if skip_first and i == 0:
            continue
        if any(sp in s for sp in STOP_PHRASES):
            continue
        if len(s) < 4 or len(s) > 80:
            continue
        out.append(s)
    return out


def _cn(s):
    return re.sub(r"[^\u4e00-\u9fa5]", "", s)


def phrase_support(phrase, corpus):
    """(是否有出处, 原因)。拉丁词要求整词命中；中文用 4-gram 覆盖率 ≥50%。"""
    corpus_l, cn_corpus = corpus.lower(), _cn(corpus)
    miss = [w for w in re.findall(r"[A-Za-z][A-Za-z0-9\-&.]{2,}", phrase)
            if w.lower() not in corpus_l]
    if miss:
        return False, f"英文词未出现：{', '.join(miss[:3])}"
    cn = _cn(phrase)
    if not cn:
        return True, ""
    if len(cn) < 8:
        return (True, "") if cn in cn_corpus else (False, f"短语未出现：{cn}")
    grams = [cn[i:i + 4] for i in range(len(cn) - 3)]
    ratio = sum(1 for g in grams if g in cn_corpus) / len(grams)
    return (True, "") if ratio >= 0.5 else (False, f"中文 4-gram 覆盖率仅 {ratio:.0%}")


def check_evidence(records, f, probes, url_meta, top):
    """抽 N 条，验证备注与导师研究领域能否在三个链接正文中找到出处。

    产出的是一份**候选清单，不等于错误**：反爬 / SPA 壳导致抓不到正文的记录会被跳过并标注，
    而不是误报。人工/LLM 需按清单回原页复核。
    """
    picked = 0
    for rec in records:
        if picked >= top:
            break
        fl = rec.get("fields", {}) or {}
        label = rec_label(fl, rec["recordId"])
        urls = [u for u in url_meta if any(r == rec["recordId"] for _, _, r in url_meta[u])]
        if not urls:
            continue
        corpora, home_healthy = [], False
        home_url = field_url(fl.get("导师主页"))
        for u in urls:
            p = probes.get(u) or {}
            corpora.append((p.get("title") or "") + " " + (p.get("body_head") or ""))
            # 「首页是健康的」复用链接四关的判定，不另设阈值——避免两套标准漂移
            if u == home_url:
                sev, _ = classify_link(p, "", "")
                if sev is None:
                    home_healthy = True
        corpus = "\n".join(corpora)
        picked += 1
        # 可用性判定看**总正文长度**，不能只看中文字数——英美校页面正文几乎全是英文
        if len(re.sub(r"\s+", "", corpus)) < 800:
            f.warn("evidence", label,
                   "三个链接都没抓到足够正文（403 / SPA 壳 / 本机不通，或 <800 字符）→ "
                   "无法机械判定，需人工打开核对")
            continue
        for fname in EVIDENCE_FIELDS:
            # 只有「备注」有职称首段；「导师研究领域」整段都是事实
            phrases = extract_phrases(field_text(fl.get(fname)), skip_first=(fname == "备注"))
            if not phrases:
                continue
            bad = []                       # [(短语, 原因)]
            for ph in phrases:
                ok, why = phrase_support(ph, corpus)
                if not ok:
                    bad.append((ph, why))
            if not bad:
                f.info("evidence", label, f"{fname}：抽样短语均在链接正文中找到出处")
                continue
            for ph, why in bad:
                if fname == "导师研究领域" and home_healthy:
                    f.fail("evidence", label,
                           f"{fname}：「{ph[:34]}」在首页正文中找不到出处（{why}）"
                           f"——研究领域必须来自本人打开的官网原文，请回原页核对后改写或删除")
                else:
                    f.warn("evidence", label,
                           f"{fname}：「{ph[:34]}」在三个链接正文中找不到出处（{why}）"
                           f"——复审：可能是同义改写，也可能是照抄了别处的摘要")
    if picked == 0:
        f.info("evidence", "(抽检)", "没有命中链接探针的记录，本次未抽到样本")


# ── 各项检查 ───────────────────────────────────────────────────────────────────
# 学校说明行（导师列为空）按设计只有「学校关联 + 备注」，其余列不适用
SCHOOL_ROW_REQUIRED = ["学校名字", "备注"]


def check_fields(records, required, f):
    for rec in records:
        rid = rec["recordId"]
        fl = rec.get("fields", {}) or {}
        label = rec_label(fl, rid)
        req = SCHOOL_ROW_REQUIRED if not field_text(fl.get("导师")).strip() else required
        for name in req:
            if not field_text(fl.get(name)).strip():
                f.fail("fields", label, f"缺字段 {name}")
        link_fields = [k for k, v in fl.items()
                       if isinstance(v, list) and v and isinstance(v[0], str)
                       and re.fullmatch(r"rec[a-zA-Z0-9]+", v[0])]
        if not link_fields:
            f.fail("fields", label, "未设置学校关联（OneWayLink）")
    names = defaultdict(list)
    for rec in records:
        fl = rec.get("fields", {}) or {}
        n = field_text(fl.get("导师")).strip()
        if n:
            names[n.lower()].append(rec["recordId"])
    for n, ids in names.items():
        if len(ids) > 1:
            f.fail("fields", n, f"同表内导师名重复 {len(ids)} 条：{ids}")


def check_notes(records, f):
    for rec in records:
        fl = rec.get("fields", {}) or {}
        label = rec_label(fl, rec["recordId"])
        for field_name in ("备注", "招生分析", "项目综合情况"):
            text = field_text(fl.get(field_name))
            if not text:
                continue
            for rule_id, sev, hit in scan_notes(text):
                f.add("notes", sev, label, f"{field_name}：{RULE_DESC[rule_id]} → 「{hit}」")


def check_titles(records, f):
    for rec in records:
        fl = rec.get("fields", {}) or {}
        # 学校说明行（导师列为空）没有职称，跳过职称检查
        if not field_text(fl.get("导师")).strip():
            continue
        label = rec_label(fl, rec["recordId"])
        res = scan_title(field_text(fl.get("备注")), field_text(fl.get("Location")))
        if res:
            sev, msg = res
            f.add("title", sev, label, msg)


def check_email(records, f, probes):
    for rec in records:
        fl = rec.get("fields", {}) or {}
        label = rec_label(fl, rec["recordId"])
        mail = field_text(fl.get("导师联系方式")).strip().lower()
        m = re.search(r"[\w.+-]+@([\w.-]+)", mail)
        if not m:
            continue
        host = field_url(fl.get("导师主页"))
        mh = re.search(r"https?://([^/]+)", host)
        if not mh:
            continue
        eh, hh = domain_root(m.group(1)), domain_root(mh.group(1))
        if eh != hh:
            sev = "WARN"
            f.add("email", sev, label, f"邮箱域名 {m.group(1)} 与主页域名 {mh.group(1)} 不同根")


def check_gates(records, f):
    """第 8 项无法机械判定，输出待核清单，避免交付时静默跳过。"""
    progs = defaultdict(list)
    for rec in records:
        fl = rec.get("fields", {}) or {}
        u = field_url(fl.get("博士申请信息"))
        if u:
            progs[norm_url(u)].append(field_text(fl.get("导师")))
    f.info("gates", "(清单)", f"需人工读官网原文核对的项目页共 {len(progs)} 个（GRE / 招生年份 / 停招 / 先修课）")
    for u, names in sorted(progs.items()):
        f.info("gates", "(清单)", f"{u}  ← {len(names)} 条记录")


def check_coverage(records, f, expected_file):
    """第 10 项：本轮记录的项目页集合 与 逐校总目录清单 做差集。"""
    if not expected_file:
        f.info("coverage", "(提示)",
               "未提供 --expected-programs，第 10 项无法机械判定："
               "请逐校打开「博士学位课程总目录」导出对口项目页 URL 清单后再跑一次。"
               "注意范围性否定 ≠ 全局否定（漏项根因是被写死院系范围）。")
        return
    try:
        with open(os.path.expanduser(expected_file), encoding="utf-8") as fh:
            expected = {norm_url(l.strip()) for l in fh if l.strip() and not l.startswith("#")}
    except OSError as e:
        f.incomplete.append(f"读 expected-programs 失败：{e}")
        return
    actual = {norm_url(field_url((rec.get("fields") or {}).get("博士申请信息")))
              for rec in records}
    actual.discard("")
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    for u in missing:
        f.fail("coverage", "(差集)", f"总目录里有、本轮记录没有挂靠：{u}（整所学校/项目缺席？）")
    for u in extra:
        f.warn("coverage", "(差集)", f"本轮记录里有、总目录清单没有：{u}（清单漏了 or 链接不对）")


def check_school_link(records, f, main_table_id, token):
    if not main_table_id:
        f.info("school", "(提示)", "未提供 --main-table-id，第 5 项跳过（学校名/排名未反查）")
        return
    main = fetch_records(main_table_id, token, f)
    if not main:
        return
    idx = {}
    for rec in main:
        fl = rec.get("fields", {}) or {}
        for k in ("学校", "学校全称", "学校中文名", "学校英文缩写"):
            v = field_text(fl.get(k)).strip().lower()
            if v:
                idx.setdefault(v, fl)
    for rec in records:
        fl = rec.get("fields", {}) or {}
        label = rec_label(fl, rec["recordId"])
        linked = None
        for k, v in fl.items():
            if isinstance(v, list) and v and isinstance(v[0], str) and re.fullmatch(r"rec[a-zA-Z0-9]+", v[0]):
                linked = v[0]
        if not linked or linked not in {r["recordId"] for r in main}:
            f.warn("school", label, "关联的学校 recordId 在指定主表中找不到（可能指向了别的主表）")
            continue
        row = next((r for r in main if r["recordId"] == linked), None)
        if not row:
            continue
        mf = row.get("fields", {}) or {}
        school_name = next((field_text(mf.get(k)) for k in ("学校", "学校全称", "学校中文名")
                            if field_text(mf.get(k))), "")
        declared_rank = field_text(fl.get("QS排名") or fl.get("美国USNEWS排名"))
        real_rank = field_text(mf.get("排名") or mf.get("2026年QS排名") or mf.get("2025年USNews排名"))
        if declared_rank and real_rank and declared_rank.strip() != real_rank.strip():
            f.warn("school", label,
                   f"排名反查不一致：记录写 {declared_rank}，主表 {school_name} 为 {real_rank}")
        f.info("school", label, f"关联主表学校 = {school_name}")


# ── 自检用例（来自 notes-and-fields.md 的既有正例/反例，改正则必须让这里仍然全过） ──
SELF_TEST_OK = [
    "副教授；做消费者判断与决策、跨期选择。",
    "教授；文化遗产和建筑史研究。",
    "助理教授；消费者决策、道德决策；MIT PhD。",
    "副教授；做心血管药物流行病学，但也有老年用药安全的方向；和你的药流方向能搭上，可以备选一下呢～",
    "教授；心血管疾病流行病学，主持哥伦比亚大学MESA现场中心，做亚临床动脉粥样硬化、肥胖和代谢综合征的人群研究；和慢病预防方向能搭上。",
    "教授；交通网络与多方式出行、交通韧性；方法能接上，但应用场景在道路养护与安全，没有赛事和体育；和你的工程仿真方向能搭上，可以备选一下呢～",
    "副教授；交通工程与交通安全，做行人流实时计数与非机动车安全分析；不过他做的是行人流量测，不做疏散仿真、也不涉及体育场景，只能算半个对口；和你的赛事客流疏散仿真方向能搭上，可以备选一下呢～",
    "未明确表明监督资格，可以后放～",
    "教授；做心血管药物流行病学；文章看这里 https://scholar.google.com/citations?user=xxx",
    # 「大学生」是合法词，不能被误指代规则命中
    "副教授；生物力学与运动损伤，曾参与特拉华大学生物力学实验室的临床测量研究。",
]
SELF_TEST_BAD = [
    ("⚠️【职称修正】Vika写\"副教授\"——实际为 Assistant Professor", "meta-note"),
    ("教授；做心血管药物流行病学；⚠️ 已确认此教授仍在职", "meta-note"),
    ("教授；交通网络与多方式出行；和学生的方向能搭上。", "wrong-pronoun"),
    ("方向1核心匹配", "direction-index"),
    ("教授；消费者判断与决策；匹配度最高。", "machine-score"),
    ("教授；消费者判断与决策；本表其他记录里也有人做这个。", "tool-name"),
    ("教授；消费者判断与决策；该导师信息待补。", "draft-language"),
    ("教授；消费者判断与决策；套磁前建议先邮件确认是否仍收博士生。", "deadline-task"),
    ("教授；消费者判断与决策；详见链接确认。", "guiding-link"),
    ("教授；消费者判断与决策；文章看这里 https://a.com/x 也可以点击查看 https://b.com", "guiding-link"),
]
# (备注, Location)：港澳讲师序列仍一刀切排除
SELF_TEST_TITLE_LOW = [
    ("讲师；消费者判断与决策。", "Hong Kong SAR"),
    ("Senior Lecturer；设计史。", "Hong Kong SAR"),
    ("高级讲师；消费者判断与决策。", "Macao SAR"),
    ("Professor of Practice；城市设计。", "United States"),
    ("Research Assistant Professor；交通工程。", "United States"),
    ("Emeritus Professor；建筑史。", "United Kingdom"),
    ("博士生导师；消费者行为。", "China (Mainland)"),
]
# 2026-10-13 用户裁定：英澳 Senior Lecturer / 高级讲师 算合格职称，不得误拦
SELF_TEST_TITLE_ALLOWED = [
    ("高级讲师；服装技术应用研究，涉及计算机辅助样板与放码。", "United Kingdom"),
    ("Senior Lecturer；设计史。", "United Kingdom"),
    ("高级讲师；功能服装与无缝针织研究。", "Australia"),
    ("Reader；服装生产工程与管理研究。", "United Kingdom"),
]
SELF_TEST_TITLE_FIXED = [
    "未明确表明监督资格，可以后放～",
    "教授；建筑史；不过现在应该到退休年龄了，可以后放～",
]


def self_test():
    """纯离线，校验备注正则、职称门槛与落点判定仍在既有正例/反例上表现正确。"""
    ok = True

    wrong = [(t, sorted({r for r, _, _ in scan_notes(t)}))
             for t in SELF_TEST_OK if scan_notes(t)]
    for t, hit in wrong:
        ok = False
        print(f"  ❌ 正例被误报 {hit}：{t[:52]}")
    print(f"  正例 {len(SELF_TEST_OK)} 条：{'全部放行' if not wrong else '有误报'}")

    missed = []
    for t, expect in SELF_TEST_BAD:
        hit = {r for r, _, _ in scan_notes(t)}
        if not hit:
            missed.append((t, expect, "未命中任何规则"))
        elif expect not in hit:
            missed.append((t, expect, f"命中了 {sorted(hit)}"))
    for t, expect, why in missed:
        ok = False
        print(f"  ❌ 反例未按预期拦截（期望 {expect}）：{why} ← {t[:52]}")
    print(f"  反例 {len(SELF_TEST_BAD)} 条：{'全部拦截' if not missed else '有漏报'}")

    low_miss = []
    for t, loc in SELF_TEST_TITLE_LOW:
        res = scan_title(t, loc)
        if not res or res[0] != "FAIL":
            low_miss.append(t)
            ok = False
            print(f"  ❌ 讲师序列未被拦截：{t[:40]}（{loc}）→ {res}")
    print(f"  讲师序列 {len(SELF_TEST_TITLE_LOW)} 条：{'全部拦截' if not low_miss else '有漏报'}")

    allow_miss = []
    for t, loc in SELF_TEST_TITLE_ALLOWED:
        res = scan_title(t, loc)
        if res and res[0] == "FAIL":
            allow_miss.append(t)
            ok = False
            print(f"  ❌ 英澳 Senior Lecturer 被误拦：{t[:40]}（{loc}）→ {res}")
    print(f"  英澳高级讲师 {len(SELF_TEST_TITLE_ALLOWED)} 条：{'全部放行' if not allow_miss else '有误拦'}")

    fixed_miss = []
    for t in SELF_TEST_TITLE_FIXED:
        res = scan_title(t)
        if res and res[0] == "FAIL":
            fixed_miss.append(t)
            ok = False
            print(f"  ❌ 固定写法被误拦：{t[:44]} → {res}")
    print(f"  固定写法 {len(SELF_TEST_TITLE_FIXED)} 条：{'全部放行' if not fixed_miss else '有误报'}")

    url_cases = [
        ("https://a.edu/p/x", "https://a.edu/p/x/", True),
        ("http://a.edu/p", "https://a.edu/p", True),
        ("https://www.a.edu/p", "https://a.edu/p", True),
        ("https://a.edu/p/x", "https://a.edu/search?q=x", False),
        ("https://a.edu/p/x", "https://b.edu/p/x", False),
        ("https://a.edu/p/x#sec", "https://a.edu/p/x", True),
    ]
    url_bad = 0
    for a, b, want in url_cases:
        if same_landing(a, b) != want:
            url_bad += 1
            ok = False
            print(f"  ❌ 落点判定错：{a} vs {b} 期望 {want}")
    print(f"  落点判定 {len(url_cases)} 条：{'全部正确' if not url_bad else '有错误'}")

    # 证据链抽检的两个回归点（2026-10-07 各踩过一次）
    ev = []
    # ① 备注首段是职称位，必须跳过；但「导师研究领域」没有职称位，整段都要查
    got = extract_phrases("副教授；设计史与物质文化。", skip_first=True)
    if got != ["设计史与物质文化"]:
        ev.append(f"备注首段未正确跳过：{got}")
    got2 = extract_phrases("量子计算与拓扑绝缘体", skip_first=False)
    if got2 != ["量子计算与拓扑绝缘体"]:
        ev.append(f"研究领域被误当职称段丢弃：{got2}")
    # ② 含套话的整段应整段丢弃，不能剥离套话后留下「和你的设计史」这类残句
    got3 = extract_phrases("副教授；设计史与物质文化；和你的设计史方向能搭上，可以备选一下呢～",
                           skip_first=True)
    if got3 != ["设计史与物质文化"]:
        ev.append(f"套话段未整段丢弃（期望只剩事实段，实得 {got3}）")
    # ③ 出处判定
    corpus = "Professor X. Her research focuses on design history and material culture. 设计史与物质文化。"
    for ph, want in (("设计史与物质文化", True), ("量子计算与拓扑绝缘体", False),
                     ("material culture", True), ("quantum computing", False)):
        got_ok, _ = phrase_support(ph, corpus)
        if got_ok != want:
            ev.append(f"出处判定错：{ph} 期望 {want} 实得 {got_ok}")
    for m in ev:
        ok = False
        print(f"  ❌ 证据链：{m}")
    print(f"  证据链抽检回归 {len(ev)} 项失败（共 6 项检查）")

    print("\n" + ("KS_AUDIT_ALL_SELFTEST_OK" if ok else "KS_AUDIT_ALL_SELFTEST_FAIL"))
    return 0 if ok else 1


# ── 主流程 ─────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(add_help=True, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("datasheet_id", nargs="?")
    ap.add_argument("--token-file")
    ap.add_argument("--only")
    ap.add_argument("--skip")
    ap.add_argument("--main-table-id")
    ap.add_argument("--expected-programs")
    ap.add_argument("--fields")
    ap.add_argument("--max-urls", type=int, default=120)
    ap.add_argument("--evidence-top", type=int, default=5,
                    help="第 11 项抽检几条记录的证据链（默认 5，对应「抽 3–5 条」）")
    ap.add_argument("--json")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-fail", action="store_true")
    ap.add_argument("--list-checks", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    if args.list_checks:
        for cid, desc in CHECKS:
            print(f"{cid:10s} {desc}")
        return 0

    if not args.datasheet_id:
        print(__doc__)
        return 2

    token = read_token(args)
    if not token:
        print("[ERROR] 缺少 token。请设置环境变量 VIKA_TOKEN，或用 --token-file 指定文件。", file=sys.stderr)
        print("        （token 不会被打印或写入输出）", file=sys.stderr)
        return 2

    only = set(x.strip() for x in args.only.split(",")) if args.only else set(CHECK_IDS)
    skip = set(x.strip() for x in args.skip.split(",")) if args.skip else set()
    unknown = (only | skip) - set(CHECK_IDS)
    if unknown:
        print(f"[ERROR] 未知检查项：{sorted(unknown)}；用 --list-checks 查看。", file=sys.stderr)
        return 2
    todo = [c for c in CHECK_IDS if c in only and c not in skip]

    f = Findings()

    print(f"=== 交付前机械复查 · {args.datasheet_id} ===")
    print(f"检查项：{', '.join(todo)}\n")

    records = fetch_records(args.datasheet_id, token, f)
    if not records:
        print("[ERROR] 未取到记录，或接口失败。", file=sys.stderr)
        return 3
    print(f"记录总数：{len(records)}\n")

    required = (args.fields.split(",") if args.fields else REQUIRED_FIELDS_DEFAULT)

    if "fields" in todo:
        check_fields(records, required, f)

    # 链接与姓名、邮箱共用一次抓取
    probes = {}
    url_meta = {}
    need_links = any(c in todo for c in ("links", "name", "email", "evidence"))
    if need_links:
        for rec in records:
            fl = rec.get("fields", {}) or {}
            mentor = field_text(fl.get("导师"))
            for fname in URL_FIELDS:
                u = field_url(fl.get(fname))
                if u:
                    url_meta.setdefault(u, []).append((mentor, fname, rec["recordId"]))
        urls = list(url_meta)
        if args.max_urls and len(urls) > args.max_urls:
            f.incomplete.append(f"去重 URL {len(urls)} 个，超过 --max-urls {args.max_urls}，只检查了前 {args.max_urls} 个")
            urls = urls[:args.max_urls]
        print(f"去重 URL {len(url_meta)} 个，本轮检查 {len(urls)} 个\n")

        tmp_dir = tempfile.mkdtemp(prefix="audit_all_")
        for i, u in enumerate(urls):
            p = curl_probe(u, tmp_dir, i)
            p["url_original"] = u
            probes[u] = p
            mentors, fields_hit = {m for m, _, _ in url_meta[u]}, {fn for _, fn, _ in url_meta[u]}
            if "links" in todo:
                last = next((m.strip().split()[-1] for m, fn, _ in url_meta[u]
                             if fn == "导师主页" and m.strip().split()), "")
                sev, msg = classify_link(p, last if "导师主页" in fields_hit else "", 
                                         "导师主页" if "导师主页" in fields_hit else "")
                label = f"{'/'.join(sorted(mentors))[:40]} [{p['code']} {p['size']}B]"
                if sev:
                    f.add("links", sev, label, f"{u[:100]} → {msg}")
                else:
                    f.info("links", label, f"{u[:100]} → OK")
            if not args.quiet:
                flag = "ok" if not probes[u].get("title") else "ok*"
                print(f"  [{p['code']}] {p['size']:>8}B {flag} {u[:96]}")
            time.sleep(0.08)
        try:
            os.rmdir(tmp_dir)
        except OSError:
            pass

        if "email" in todo:
            check_email(records, f, probes)

    if "notes" in todo:
        check_notes(records, f)
    if "title" in todo:
        check_titles(records, f)
    if "school" in todo:
        check_school_link(records, f, args.main_table_id, token)
    if "evidence" in todo:
        check_evidence(records, f, probes, url_meta, args.evidence_top)
    if "gates" in todo:
        check_gates(records, f)
    if "coverage" in todo:
        check_coverage(records, f, args.expected_programs)

    # ── 报告 ───────────────────────────────────────────────────────────────
    by = f.by_check()
    print("\n=== 逐项结果 ===")
    for cid, desc in CHECKS:
        if cid not in todo:
            print(f"  [跳过] {desc}")
            continue
        items = by.get(cid, [])
        fails = sum(1 for it in items if it[1] == "FAIL")
        warns = sum(1 for it in items if it[1] == "WARN")
        mark = "❌" if fails else ("⚠️" if warns else "✅")
        print(f"  {mark} {desc}：FAIL {fails} / WARN {warns}")

    detail = [it for it in f.items if it[1] in ("FAIL", "WARN")]
    if detail and not args.quiet:
        print("\n=== 需处理明细 ===")
        for cid, sev, label, msg in detail:
            print(f"  [{sev}] ({cid}) {label}\n        {msg}")

    gates = by.get("gates", [])
    if "gates" in todo and not args.quiet and gates:
        print("\n=== 第 8 项：三硬门槛待核清单（必须人工读官网原文）===")
        for _, _, _, msg in gates:
            print(f"  {msg}")

    if f.incomplete:
        print("\n=== ⚠️ 结果不完整 ===")
        for m in f.incomplete:
            print(f"  {m}")

    fails, warns = f.count("FAIL"), f.count("WARN")
    print("\n=== 结论 ===")
    if f.incomplete:
        print(f"⚠️ 结果不完整（{len(f.incomplete)} 处），不得据此判定通过。FAIL {fails} / WARN {warns}")
        code = 3
    elif fails:
        print(f"❌ 不可交付：FAIL {fails} / WARN {warns}")
        code = 1
    else:
        print(f"✅ 机械项全过：FAIL 0 / WARN {warns}（WARN 需人工判断，不等于通过）")
        code = 0

    if args.json:
        payload = {
            "datasheetId": args.datasheet_id,
            "records": len(records),
            "checksRun": todo,
            "fail": fails, "warn": warns,
            "incomplete": f.incomplete,
            "items": [{"check": c, "severity": s, "label": l, "message": m}
                      for c, s, l, m in f.items],
            "verdict": {0: "pass", 1: "fail", 3: "incomplete"}[code],
        }
        with open(os.path.expanduser(args.json), "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        print(f"机器可读结果：{args.json}")

    if args.no_fail:
        return 0
    return code


if __name__ == "__main__":
    sys.exit(main())
