# Vika Table Operations Guide

Complete guide for all common Vika table operations via Fusion API. All patterns use Python 3 stdlib only — no SDK, no CLI, no npm.

---

## 0. Quick Setup (Token + Datasheet)

```python
import os, json
from urllib.request import Request, urlopen

TOKEN = os.environ.get("VIKA_TOKEN", "")
DATASHEET = "dstXXX"  # From URL: https://vika.cn/share/shrXXX/dstXXX/viwXXX
BASE = "https://api.vika.cn/fusion/v1"

def vika(method, path, body=None):
    url = f"{BASE}/datasheets/{DATASHEET}{path}"
    h = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    data = json.dumps(body).encode() if body else None
    r = Request(url, data=data, headers=h, method=method)
    try:
        resp = urlopen(r)
        return json.loads(resp.read())
    except Exception as e:
        body = json.loads(e.read()) if hasattr(e, 'read') else {}
        raise Exception(f"API {getattr(e,'code','?')}: {body.get('message',str(e))}")
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
```python
# URL fields can be set as plain strings
updates = [
    {"recordId": "recXXX", "fields": {
        "导师主页": "https://www.university.edu/department/faculty/prof-name",
        "博士申请信息": "https://gradschool.university.edu/phd/program"
    }},
]
vika("PATCH", "/records", {"records": updates, "fieldKey": "name"})
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
vika("DELETE", "/records", ["recXXX", "recYYY"])
```

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
    # vika("DELETE", "/records", blanks)  # Uncomment to delete
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
