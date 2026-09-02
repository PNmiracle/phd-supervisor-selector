#!/usr/bin/env python3
import urllib.request, urllib.error, json, re, os

token = ""
with open(os.path.expanduser("~/.zshrc")) as f:
    for line in f:
        m = re.match(r'export VIKA_TOKEN=(.+)', line.strip())
        if m:
            token = m.group(1).strip().strip('"').strip("'")
            break

if not token:
    print("ERROR: VIKA_TOKEN not found")
    exit(1)

BASE = "https://api.vika.cn/fusion/v1"

def vika(method, path, data=None):
    url = f"{BASE}{path}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, method=method, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "body": e.read()[:300]}
    except Exception as e:
        return {"error": str(e)}

# Get ALL pages
print("=== ALL RECORDS (paginated) ===")
all_records = []
page = 1
while True:
    r = vika("GET", f"/datasheets/dstmnEscdKenfRSEL0/records?maxRecords=500&pageNum={page}&cellFormat=string")
    if "error" in r:
        print(f"Page {page} Error: {r}")
        break
    recs = r.get("data", {}).get("records", [])
    total = r.get("data", {}).get("total", 0)
    all_records.extend(recs)
    print(f"Page {page}: {len(recs)} records (cumulative: {len(all_records)}/{total})")
    if len(recs) < 500 or len(all_records) >= total:
        break
    page += 1

print(f"\nTotal fetched: {len(all_records)}")

# Print all records with key fields
print("\n=== ALL RECORDS ===")
for rec in all_records:
    fields = rec.get("fields", {})
    supervisor = fields.get("导师", "")
    school = fields.get("学校", "")
    direction = fields.get("导师研究领域", "") or fields.get("研究方向", "")
    rid = rec.get("recordId", "")
    link = fields.get("选导意向（点击选择）", "")
    status = "LOCKED" if link else "EDITABLE"
    print(f"[{status}] {rid}: {supervisor} @ {school}")
    if direction:
        print(f"  Dir: {direction[:100]}")
