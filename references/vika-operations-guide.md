# Vika Table Operations Guide

Complete guide for all common Vika table operations via Fusion API. All patterns use Python 3 stdlib only — no SDK, no CLI, no npm.

---

## 0. Quick Setup (Token + Datasheet)

> 🔐 **Token security**: Never paste your API token into the chat. Set it in terminal:
>
> **One-time (persists across all chats):**
> ```bash
> echo 'export VIKA_TOKEN=uskXXXXXX' >> ~/.zshrc && source ~/.zshrc
> ```
> **Temporary (current chat only):**
> ```bash
> echo 'export VIKA_TOKEN=uskXXXXXX' > .vika_env && source .vika_env
> ```
> The agent reads `$VIKA_TOKEN` from the environment — the token stays on your machine only.

```python
import os, json
from urllib.request import Request, urlopen

TOKEN = os.environ.get("VIKA_TOKEN", "")
DATASHEET = "dstXXX"  # From URL: https://vika.cn/share/shrXXX/dstXXX/viwXXX
BASE = "https://api.vika.cn/fusion/v1"

def vika(method, path, body=None):
    url = f"{BASE}/datasheets/{DATASHEET}{path}"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    
    # DELETE uses query parameter ?recordIds=recXXX,recYYY (not request body)
    if method == "DELETE" and body:
        if isinstance(body, list):
            record_ids = ",".join(body)
            url += f"?recordIds={record_ids}"
            data = None
        elif isinstance(body, dict) and "records" in body:
            record_ids = ",".join(body["records"])
            url += f"?recordIds={record_ids}"
            data = None
        else:
            data = json.dumps(body).encode() if body else None
    else:
        data = json.dumps(body).encode() if body else None
    
    req = Request(url, data=data, headers=headers, method=method)
    try:
        resp = urlopen(req)
        raw = resp.read()
        return json.loads(raw) if raw else {"code": 0, "message": "OK", "data": {}}
    except Exception as e:
        try:
            if hasattr(e, 'read'):
                raw = e.read()
                body = json.loads(raw) if raw else {}
                raise Exception(f"API {getattr(e,'code','?')}: {body.get('message',str(e))}")
        except Exception:
            pass
        raise
```

---

## 1. View Table Schema

```python
result = vika("GET", "/fields")
for f in result["data"]["fields"]:
    print(f"{f['name']:20s} [{f['type']}]")
    if f['type'] == 'SingleSelect':
        opts = [o['name'] for o in f.get('property',{}).get('options',[])]
        print(f"  Options: {opts}")
```

---

## 2. List Records

### 2.1 All Records
```python
result = vika("GET", "/records?maxRecords=200&pageSize=200")
records = result["data"]["records"]
total = result["data"]["total"]
for r in records:
    f = r["fields"]
    print(f"{r['recordId'][:12]}  {f.get('导师','')}  {f.get('Department','')}")
```

### 2.2 Filtered by Formula
```python
# URL-encode Chinese: urllib.parse.quote('{状态}="待发邮件"')
from urllib.parse import quote
filter_expr = quote('{状态}="待发邮件"')
path = f"/records?filterByFormula={filter_expr}&maxRecords=200"
result = vika("GET", path)
```

### 2.3 By Specific View
```python
result = vika("GET", "/records?viewId=viwXXX&maxRecords=200")
```

### 2.4 Only Specific Fields
```python
# Use Chinese field names, URL-encoded
from urllib.parse import quote
path = f"/records?fields={quote('导师,Department,备注')}&maxRecords=200"
result = vika("GET", path)
```

---

## 3. Create Records (Batch up to 10)

```python
# Use fieldKey: "name" for Chinese field names
new_records = [
    {"fields": {"导师": "张三", "Department": "心理学院(XX大学)", "备注": "教授；决策研究"}},
    {"fields": {"导师": "李四", "Department": "商学院(YY大学)", "备注": "副教授；消费者行为"}},
]
result = vika("POST", "/records", {"records": new_records, "fieldKey": "name"})
print(f"Created {len(result['data']['records'])} records")

# For batch > 10, loop with delay:
import time
for i in range(0, len(all_records), 10):
    batch = all_records[i:i+10]
    vika("POST", "/records", {"records": batch, "fieldKey": "name"})
    time.sleep(0.3)
```

---

## 4. Update Records

### 4.1 Update Specific Fields
```python
updates = [
    {"recordId": "recXXX", "fields": {"Department": "心理学院(香港大学)", "状态": "待发邮件"}},
    {"recordId": "recYYY", "fields": {"备注": "教授；认知神经科学；在招博士"}},
]
vika("PATCH", "/records", {"records": updates, "fieldKey": "name"})
```

### 4.2 Update URL Fields

**⚠️ CRITICAL**: URL-type fields (导师主页, 博士申请信息, 其他导师信息) do NOT work with `fieldKey="name"`. The API returns 200 but silently fails to update the URL values. **Must use field IDs without fieldKey parameter.**

```python
# ❌ WRONG — silently fails for URL fields
updates = [
    {"recordId": "recXXX", "fields": {
        "导师主页": "https://www.university.edu/department/faculty/prof-name",
        "博士申请信息": "https://gradschool.university.edu/phd/program"
    }},
]
vika("PATCH", "/records", {"records": updates, "fieldKey": "name"})

# ✅ CORRECT — omit fieldKey, use field IDs
# First get field IDs from GET /fields, then:
updates = [
    {"recordId": "recXXX", "fields": {
        "fldYm8R3l4Bnu": "https://www.university.edu/department/faculty/prof-name",
        "fldI3KsjPCYWp": "https://gradschool.university.edu/phd/program"
    }},
]
# No fieldKey in the request body
req = Request(
    f"{BASE}/datasheets/{DATASHEET}/records",
    data=json.dumps({"records": updates}).encode(),
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
    method='PATCH'
)
```

### 4.3 Update SingleSelect / Checkbox
```python
# SingleSelect: use the option name exactly as it appears
vika("PATCH", "/records", {"records": [
    {"recordId": "recXXX", "fields": {"状态": "待发邮件"}}
], "fieldKey": "name"})

# Checkbox: use true/false
vika("PATCH", "/records", {"records": [
    {"recordId": "recXXX", "fields": {"确认套磁": True}}
], "fieldKey": "name"})
```

### 4.4 Bulk Department Translation
```python
# Get all records, build translation map, batch update
records = vika("GET", "/records?maxRecords=200&pageSize=200")["data"]["records"]

dept_map = {
    "Department of Psychology": "心理学院",
    "CUHK Business School": "香港中文大学商学院",
    # ...
}

updates = []
for r in records:
    dept = r["fields"].get("Department", "")
    if dept in dept_map:
        updates.append({"recordId": r["recordId"], "fields": {"Department": dept_map[dept]}})

# Batch update
for i in range(0, len(updates), 10):
    vika("PATCH", "/records", {"records": updates[i:i+10], "fieldKey": "name"})
    time.sleep(0.3)
```

---

## 5. Delete Records

### 5.1 Delete by ID
```python
# ✅ CORRECT — pass record IDs as list or {"records": [...]} object
# The `vika` function automatically converts to ?recordIds=recXXX query parameter
vika("DELETE", "/records", ["recXXX", "recYYY"])
# or
vika("DELETE", "/records", {"records": ["recXXX", "recYYY"]})
```

⚠️ **Critical**: Vika DELETE API expects recordIds in the URL query parameter, NOT in the request body. The `vika` function handles this automatically.

### 5.2 Deduplicate (Keep Most Complete)

```python
records = vika("GET", "/records?maxRecords=200&pageSize=200")["data"]["records"]

from collections import defaultdict
name_map = defaultdict(list)
for r in records:
    name = r["fields"].get("导师", "").strip()
    if name:
        name_map[name].append(r)

to_delete = []
for name, recs in name_map.items():
    if len(recs) > 1:
        # Keep the one with most filled fields
        recs.sort(key=lambda r: sum(1 for v in r["fields"].values() if v), reverse=True)
        to_delete.extend(r["recordId"] for r in recs[1:])

if to_delete:
    # ✅ CORRECT — pass list directly, `vika` function handles query parameter conversion
    vika("DELETE", "/records", to_delete)
    print(f"Deleted {len(to_delete)} duplicate records")
```

---

## 6. Import from Excel to Vika

```python
import openpyxl

# 1. Read Excel
wb = openpyxl.load_workbook("select.xlsx", data_only=True)
ws = wb["Sheet1"]
headers = [ws.cell(1, c).value for c in range(1, ws.max_column+1)]

# 2. Get existing Vika names
existing = vika("GET", "/records?maxRecords=200&pageSize=200")["data"]["records"]
existing_names = {r["fields"].get("导师","").strip() for r in existing}

# 3. Map Excel columns -> Vika fields
FIELD_MAP = {
    "导师": "导师",
    "Department": "Department",
    "导师主页": "导师主页",
    "博士申请信息": "博士申请信息",
    "其他导师信息": "其他导师信息",
    "备注": "备注",
}

# 4. Build new records (skip existing, skip linked/MagicLookUp fields)
new_records = []
seen = set()
for row in range(2, ws.max_row+1):
    name = ws.cell(row, headers.index("导师")+1).value
    if not name: continue
    name = name.strip()
    if name in existing_names or name in seen: continue
    seen.add(name)

    fields = {}
    for excel_col, vika_col in FIELD_MAP.items():
        if excel_col in headers:
            val = ws.cell(row, headers.index(excel_col)+1).value
            if val and str(val).strip() not in ("", "None"):
                fields[vika_col] = str(val).strip()
    if fields.get("导师"):
        new_records.append({"fields": fields})

# 5. Batch write
for i in range(0, len(new_records), 10):
    batch = new_records[i:i+10]
    vika("POST", "/records", {"records": batch, "fieldKey": "name"})
    time.sleep(0.3)

print(f"Imported {len(new_records)} new records")
```

---

## 7. Fill Missing Links

```python
# Get records with missing fields
records = vika("GET", "/records?maxRecords=200&pageSize=200")["data"]["records"]

LINK_MAP = {
    "导师名": ("phd-program-url", "staff-list-url"),
    # ...
}

updates = []
for r in records:
    name = r["fields"].get("导师", "").strip()
    phd = r["fields"].get("博士申请信息", "")
    other = r["fields"].get("其他导师信息", "")

    phd_ok = isinstance(phd, dict) and phd.get("text", "")
    other_ok = isinstance(other, dict) and other.get("text", "")

    if name in LINK_MAP and (not phd_ok or not other_ok):
        phd_url, other_url = LINK_MAP[name]
        fields = {}
        if not phd_ok: fields["博士申请信息"] = phd_url
        if not other_ok: fields["其他导师信息"] = other_url
        if fields:
            updates.append({"recordId": r["recordId"], "fields": fields})

for i in range(0, len(updates), 10):
    vika("PATCH", "/records", {"records": updates[i:i+10], "fieldKey": "name"})
    time.sleep(0.3)
```

---

## 8. Check for Blank Records

```python
records = vika("GET", "/records?maxRecords=200&pageSize=200")["data"]["records"]

blanks = []
for r in records:
    f = r["fields"]
    has_name = f.get("导师", "").strip()
    if not has_name:
        blanks.append(r["recordId"])

if blanks:
    print(f"Found {len(blanks)} blank records: {blanks}")
    # vika("DELETE", "/records", blanks)  # Uncomment to delete (pass list directly)
```

---

## 9. Non-Writable Fields (Important!)

These fields **cannot** be written via Fusion API — they are computed or linked:

| Field Type | Examples | Why |
|-----------|----------|-----|
| MagicLookUp | Location, QS排名, USNEWS排名 | Computed from linked records |
| OneWayLink | 美国地区学校, 非美国地区学校 | Link to another datasheet |
| Formula | 等邮件几天 | Auto-calculated |
| LastModifiedTime | 状态变更日期 | Auto-generated |
| CreatedBy / CreatedTime | From, 选导时间 | Auto-generated |

---

## 10. Rate Limits & Best Practices

- **10 records max** per POST/PATCH/DELETE request
- **0.3-0.5s delay** between batches
- 175 records ≈ 15 batches ≈ 15-20 seconds
- Use `fieldKey: "name"` for Chinese field names
- Always `strip()` names before comparison
- URL fields accept plain strings (API wraps them)

---

## 11. Cross-School Link Audit (跨校链接审计)

审查已有表格时，必须检查「博士申请信息」和「其他导师信息」的 URL 域名是否与导师实际所在学校一致。跨校链接错误会导致学生点开错误的申请页面。

### 审计脚本

```python
import re

records = vika("GET", "/records?maxRecords=200&pageSize=200")["data"]["records"]

# School domain mapping (add as needed)
SCHOOL_DOMAINS = {
    "Nanyang Technological University": ["ntu.edu.sg"],
    "National University of Singapore": ["nus.edu.sg"],
    "Hong Kong Polytechnic University": ["polyu.edu.hk"],
    "Chinese University of Hong Kong": ["cuhk.edu.hk"],
    "University of Hong Kong": ["hku.hk"],
    "University of Sydney": ["sydney.edu.au"],
    # ...
}

issues = []
for r in records:
    f = r["fields"]
    name = f.get("导师", "")
    dept = f.get("Department", "")
    
    # Determine expected school domain from Department field
    expected_domains = []
    for school_key, domains in SCHOOL_DOMAINS.items():
        if school_key.lower() in dept.lower():
            expected_domains = domains
            break
    
    if not expected_domains:
        continue  # Skip if school not in mapping
    
    # Check PhD application link
    phd = f.get("博士申请信息", "")
    if isinstance(phd, dict):
        phd = phd.get("text", "")
    if phd:
        phd_domain = re.search(r'https?://([^/]+)', phd)
        if phd_domain:
            phd_domain = phd_domain.group(1)
            if not any(d in phd_domain for d in expected_domains):
                issues.append(f"  ⚠ {name}: 博士申请信息域名({phd_domain}) ≠ 预期({expected_domains})")
    
    # Check other info link
    other = f.get("其他导师信息", "")
    if isinstance(other, dict):
        other = other.get("text", "")
    if other:
        other_domain = re.search(r'https?://([^/]+)', other)
        if other_domain:
            other_domain = other_domain.group(1)
            if not any(d in other_domain for d in expected_domains):
                issues.append(f"  ⚠ {name}: 其他导师信息域名({other_domain}) ≠ 预期({expected_domains})")

if issues:
    print(f"Found {len(issues)} cross-school link issues:")
    for issue in issues:
        print(issue)
else:
    print("No cross-school link issues found.")
```

### 修复方式

找到正确链接后，使用 field ID（非 fieldKey="name"）PATCH URL 字段：

```python
# Get field IDs first
fields = vika("GET", "/fields")
field_map = {f["name"]: f["id"] for f in fields["data"]["fields"]}

updates = [
    {"recordId": "recXXX", "fields": {
        field_map["博士申请信息"]: "https://correct-url.edu/phd",
        field_map["其他导师信息"]: "https://correct-url.edu/staff"
    }}
]
# PATCH without fieldKey for URL fields
req = Request(
    f"{BASE}/datasheets/{DATASHEET}/records",
    data=json.dumps({"records": updates}).encode(),
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
    method='PATCH'
)
```

---

## 12. Batch Research Area Completion (批量补全研究领域)

当表格中多条记录的「导师研究领域」为空时，通过 WebFetch 逐个抓取导师主页，提取 research interests 并批量写入。

### 工作流

1. GET 所有记录，筛选出「导师研究领域」为空的记录
2. 对每条记录，WebFetch 其「导师主页」URL，prompt 提取 research interests
3. 汇总提取结果，批量 PATCH（每批 10 条，fieldKey="name"）
4. 注意：WebFetch 同时检查是否为 Emeritus/Retired，发现则标记删除

```python
# Step 1: Find records with empty research area
records = vika("GET", "/records?maxRecords=200&pageSize=200&cellFormat=string")["data"]["records"]

needs_research = []
for r in records:
    f = r["fields"]
    if not f.get("导师研究领域", ""):
        homepage = f.get("导师主页", "")
        if isinstance(homepage, dict):
            homepage = homepage.get("text", "")
        if homepage:
            needs_research.append({
                "recordId": r["recordId"],
                "导师": f.get("导师", ""),
                "导师主页": homepage
            })

print(f"Found {len(needs_research)} records needing research area")

# Step 2: WebFetch each homepage (done via WebFetch tool, not in this script)
# Step 3: Batch PATCH with extracted research areas
# Text fields work fine with fieldKey="name"
updates = [
    {"recordId": "recXXX", "fields": {"导师研究领域": "Robotics, Control, Manufacturing Automation"}},
    # ... up to 10 per batch
]
vika("PATCH", "/records", {"records": updates, "fieldKey": "name"})
```

### 注意事项

- `导师研究领域` 是文本字段，可以用 `fieldKey="name"` 正常 PATCH（不同于 URL 字段）
- WebFetch 时同时检查 Emeritus/Retired 状态，发现则立即删除该记录
- 使用 `cellFormat=string` 参数获取纯文本值，避免嵌套对象解析问题
