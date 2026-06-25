# Vika Fusion API Patterns

Code patterns for direct Vika table CRUD via Python + urllib (no external deps).

## Auth & Setup

```python
TOKEN = os.environ.get("VIKA_TOKEN", "")
DATASHEET = "dstXXX"  # from URL
BASE = "https://api.vika.cn/fusion/v1"

def vika_req(method, path, body=None):
    url = f"{BASE}/datasheets/{DATASHEET}{path}"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    data = json.dumps(body).encode() if body else None
    req = Request(url, data=data, headers=headers, method=method)
    resp = urlopen(req)
    return json.loads(resp.read())
```

## URL Parsing

```
https://vika.cn/share/shrXXX/dstXXX/viwXXX
                              ^^^^^^  ^^^^^^
                           datasheetId  viewId
```

## Read All Records

```python
result = vika_req("GET", "/records?maxRecords=200&pageSize=200")
records = result["data"]["records"]
total = result["data"]["total"]
```

Page size max is 200. For >200 records, paginate with `pageNum` parameter.

## Read Fields/Schema

```python
fields = vika_req("GET", "/fields")
for f in fields["data"]["fields"]:
    print(f["id"], f["name"], f["type"])
```

## Filter Records

```python
# Filter by formula (Airtable-style)
path = '/records?filterByFormula={状态}="待发邮件"'
# URL-encode Chinese: urllib.parse.quote('{状态}="待发邮件"')
```

## Batch Create (up to 10 per call)

```python
records = [{"fields": {"导师": "XXX", "Department": "心理系"}} for ...]
result = vika_req("POST", "/records", {"records": records, "fieldKey": "name"})
```

`fieldKey: "name"` uses Chinese field names. Omit to use field IDs (`fldXXX`).

## Batch Update (up to 10 per call)

```python
updates = [
    {"recordId": "recXXX", "fields": {"Department": "心理学系(XX大学)"}},
    ...
]
result = vika_req("PATCH", "/records", {"records": updates, "fieldKey": "name"})
```

## Delete Records

```python
ids = ["recXXX", "recYYY"]
vika_req("DELETE", "/records", ids)
```

## Deduplication Pattern

```python
from collections import defaultdict
name_map = defaultdict(list)
for r in records:
    name = r["fields"].get("导师", "").strip()
    if name:
        name_map[name].append(r)

dupes = {k: v for k, v in name_map.items() if len(v) > 1}
# Keep most complete record, delete others
```

## Excel → Vika Import Pattern

```python
# 1. Read Excel names
excel_names = set()
# ... extract from openpyxl ...

# 2. Get Vika existing names
vika_names = set()
for r in vika_records:
    vika_names.add(r["fields"].get("导师", "").strip())

# 3. Find new
new = excel_names - vika_names

# 4. Batch write, skipping linked/computed fields
for batch in chunks(new, 10):
    vika_req("POST", "/records", {"records": batch, "fieldKey": "name"})
    time.sleep(0.3)
```

## Field Type Warnings

- **MagicLookUp**: computed, cannot write
- **OneWayLink**: link to another datasheet, cannot write directly
- **SingleText/Text/URL/Email**: can write
- **SingleSelect**: can write option name (must match existing option)
- **Checkbox**: can write `true`/`false`

## Rate Limiting

- Max 10 records per POST/PATCH/DELETE
- Add 0.3-0.5s delay between batches
- 175 records ≈ 15 batches ≈ 15-20 seconds total
