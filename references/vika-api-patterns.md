# Vika Fusion API Patterns

Code patterns for direct Vika table CRUD via Python + urllib (no external deps).

## Auth & Setup

```python
TOKEN = os.environ.get("VIKA_TOKEN", "")
DATASHEET = "dstXXX"  # from URL
BASE = "https://api.vika.cn/fusion/v1"

def vika_req(method, path, body=None):
    import json
    from urllib.request import Request, urlopen
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
            data = json.dumps(body).encode()
    else:
        data = json.dumps(body).encode() if body else None
    
    req = Request(url, data=data, headers=headers, method=method)
    try:
        resp = urlopen(req)
        # DELETE may return 204 No Content with empty body
        raw = resp.read()
        return json.loads(raw) if raw else {"code": 0, "message": "OK", "data": {}}
    except Exception as e:
        if hasattr(e, 'read'):
            try:
                raw = e.read()
                body = json.loads(raw) if raw else {}
                raise Exception(f"API {getattr(e,'code','?')}: {body.get('message',str(e))}")
            except:
                pass
        raise
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
# ✅ CORRECT — pass record IDs as list or {"records": [...]} object
# vika_req automatically converts to ?recordIds=recXXX,recYYY query parameter
ids = ["recXXX", "recYYY"]
vika_req("DELETE", "/records", ids)
# or
vika_req("DELETE", "/records", {"records": ids})
```

⚠️ **Critical**: Vika DELETE API expects recordIds in the URL query parameter (`?recordIds=recXXX,recYYY`), NOT in the request body. The `vika_req` function handles this automatically for DELETE requests.

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

## Known API Issues

### DELETE Format (Critical)

**Vika DELETE API uses query parameter, NOT request body.**

❌ **Wrong** (sends recordIds in request body):
```
DELETE /records
Body: {"records": ["recXXX"]}
```

✅ **Correct** (sends recordIds in URL query parameter):
```
DELETE /records?recordIds=recXXX,recYYY
```

The `vika_req` helper function handles this automatically: when `method="DELETE"` and `body` is provided, it converts the body to query parameter format.

**Example**:
```python
# These both work correctly (vika_req handles the conversion):
vika_req("DELETE", "/records", ["recXXX", "recYYY"])
vika_req("DELETE", "/records", {"records": ["recXXX", "recYYY"]})
```

### GET Cache Staleness
After DELETE or PATCH, subsequent GET requests may return stale data from an API cache. The Vika UI typically reflects changes faster than the API. Always verify in the UI after making changes.

### URL Field PATCH with fieldKey="name" Returns 200 but Silently Fails (2026-07-02)

**Problem**: When PATCHing URL-type fields (e.g., 博士申请信息, 其他导师信息, 导师主页) with `fieldKey="name"` in the request body, the API returns 200 success but the URL field values are NOT actually updated.

**Root Cause**: URL-type fields behave similarly to OneWayLink/MagicLookUp fields when `fieldKey="name"` is used — the API cannot resolve the field correctly.

**Solution**: Omit `fieldKey` entirely and use field IDs (`fldXXX`) as keys instead. Get field IDs from `GET /fields`.

```python
# ❌ WRONG — returns 200 but URL fields are NOT updated
updates = [
    {"recordId": "recXXX", "fields": {
        "博士申请信息": "https://example.com/phd",
        "其他导师信息": "https://example.com/faculty"
    }}
]
vika("PATCH", "/records", {"records": updates, "fieldKey": "name"})

# ✅ CORRECT — omit fieldKey, use field IDs
updates = [
    {"recordId": "recXXX", "fields": {
        "fldYm8R3l4Bnu": "https://example.com/phd",
        "fldI3KsjPCYWp": "https://example.com/faculty"
    }}
]
# No fieldKey parameter in request body
req = Request(url, data=json.dumps({"records": updates}).encode(), ...)
```

**Note**: This ONLY affects PATCH operations on URL-type fields. Text/SingleSelect/Checkbox fields still work fine with `fieldKey="name"`.

## Critical Discovery: OneWayLink/MagicLookUp Write Workaround (2026-06-30)

**Problem**: Vika Fusion API rejects `OneWayLink` and `MagicLookUp` fields with "Lookup field can't be edited" when using `fieldKey=name` parameter.

**Root Cause**: When `fieldKey=name` is present in the URL query string, the API treats ALL field values as plain text and rejects references to linked record IDs. This affects both POST (create) and PATCH (update).

**Solution**: Remove `fieldKey=name` from the URL when PATCHing linked fields. Use the default field key mode (which uses field IDs internally).

```python
# ❌ CORRECT - PATCH with fieldKey=name
url = f'{base}/datasheets/{ds}/records?fieldKey=name'
# This fails for OneWayLink fields

# ✅ CORRECT - PATCH without fieldKey
url = f'{base}/datasheets/{ds}/records'
# No fieldKey parameter - this allows setting OneWayLink/MagicLookUp fields

# POST (create) still cannot set these fields regardless of fieldKey mode
```

**Workaround for creating records with linked fields**:
1. POST record WITHOUT `非美国地区学校` and `Location` fields (use `fieldKey=name` for regular fields)
2. PATCH the record WITHOUT `fieldKey=name` to set `非美国地区学校: [school_record_id]`
3. `Location` and `QS排名` will auto-fill after school link is set

**Note**: This only works for PATCH, NOT for POST. Records must be created first, then school link patched in a separate call.
