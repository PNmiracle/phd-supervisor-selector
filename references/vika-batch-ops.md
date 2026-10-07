<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载 -->
> **本文含**：Vika 批量与运维操作——Excel 导入、补缺失链接、查空记录、跨校链接审计、批量补研究领域。
> **什么时候读**：要批量补/改字段、查空记录、做跨校链接审计时。
> **什么时候不用读**：只是新建/更新/删除单条记录时——看 `vika-guide.md`。

> 本文由 `vika-guide.md` 于 2026-10-07 按职能拆分而来；入口与核心读写见 `vika-guide.md`。
---

## 6. Import from Excel to Vika

```python
import openpyxl

wb = openpyxl.load_workbook("select.xlsx", data_only=True)
ws = wb["Sheet1"]
headers = [ws.cell(1, c).value for c in range(1, ws.max_column+1)]

existing = vika("GET", "/records?maxRecords=200&pageSize=200")["data"]["records"]
existing_names = {r["fields"].get("导师","").strip() for r in existing}

FIELD_MAP = {
    "导师": "导师", "Department": "Department", "导师主页": "导师主页",
    "博士申请信息": "博士申请信息", "其他导师信息": "其他导师信息", "备注": "备注",
}

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

for i in range(0, len(new_records), 10):
    vika("POST", "/records", {"records": new_records[i:i+10], "fieldKey": "name"})
    time.sleep(0.3)

print(f"Imported {len(new_records)} new records")
```

---


## 7. Fill Missing Links

```python
records = vika("GET", "/records?maxRecords=200&pageSize=200")["data"]["records"]

LINK_MAP = {
    "导师名": ("phd-program-url", "staff-list-url"),
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

blanks = [r["recordId"] for r in records if not r["fields"].get("导师", "").strip()]

if blanks:
    print(f"Found {len(blanks)} blank records: {blanks}")
    # vika("DELETE", "/records", blanks)  # Uncomment to delete
```

---


## 9. Cross-School Link Audit

审查已有表格时，必须检查「博士申请信息」和「其他导师信息」的 URL 域名是否与导师实际所在学校一致。

```python
import re

records = vika("GET", "/records?maxRecords=200&pageSize=200")["data"]["records"]

SCHOOL_DOMAINS = {
    "Nanyang Technological University": ["ntu.edu.sg"],
    "National University of Singapore": ["nus.edu.sg"],
    "Hong Kong Polytechnic University": ["polyu.edu.hk"],
    "Chinese University of Hong Kong": ["cuhk.edu.hk"],
    "University of Hong Kong": ["hku.hk"],
    "University of Sydney": ["sydney.edu.au"],
}

issues = []
for r in records:
    f = r["fields"]
    name = f.get("导师", "")
    dept = f.get("Department", "")

    expected_domains = []
    for school_key, domains in SCHOOL_DOMAINS.items():
        if school_key.lower() in dept.lower():
            expected_domains = domains
            break
    if not expected_domains:
        continue

    for field_name in ["博士申请信息", "其他导师信息"]:
        val = f.get(field_name, "")
        if isinstance(val, dict):
            val = val.get("text", "")
        if val:
            domain = re.search(r'https?://([^/]+)', val)
            if domain:
                domain = domain.group(1)
                if not any(d in domain for d in expected_domains):
                    issues.append(f"  {name}: {field_name} domain ({domain}) != expected ({expected_domains})")

if issues:
    print(f"Found {len(issues)} cross-school link issues:")
    for issue in issues:
        print(issue)
else:
    print("No cross-school link issues found.")
```

---


## 10. Batch Research Area Completion

当表格中多条记录的「导师研究领域」为空时，通过 WebFetch 逐个抓取导师主页，提取 research interests 并批量写入。

```python
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
# Step 2: WebFetch each homepage (via WebFetch tool)
# Step 3: Batch PATCH with extracted research areas (text fields work with fieldKey="name")
```

---
