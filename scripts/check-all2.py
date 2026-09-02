#!/usr/bin/env python3
import urllib.request, urllib.error, json, re

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
    url = "%s%s" % (BASE, path)
    headers = {"Authorization": "Bearer %s" % token, "Content-Type": "application/json"}
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, method=method, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": "HTTP %s" % e.code, "body": e.read()[:300]}
    except Exception as e:
        return {"error": str(e)}

# Get all pages
all_records = []
page = 1
while True:
    r = vika("GET", "/datasheets/dstmnEscdKenfRSEL0/records?maxRecords=500&pageNum=%d&cellFormat=string" % page)
    if "error" in r:
        print("Page %d Error: %s" % (page, r))
        break
    recs = r.get("data", {}).get("records", [])
    total = r.get("data", {}).get("total", 0)
    all_records.extend(recs)
    print("Page %d: %d records (total so far: %d/%d)" % (page, len(recs), len(all_records), total))
    if len(recs) < 500 or len(all_records) >= total:
        break
    page += 1

print("\nTotal records fetched: %d" % len(all_records))

# Print all
for rec in all_records:
    fields = rec.get("fields", {})
    sup = fields.get("导师", "")
    sch = fields.get("学校", "")
    direction = fields.get("导师研究领域", "") or fields.get("研究方向", "")
    rid = rec.get("recordId", "")
    link = fields.get("选导意向（点击选择）", "")
    status = "LOCKED" if link else "EDIT"
    print("[%s] %s: %s @ %s" % (status, rid, sup, sch))
    if direction:
        print("  Dir: %s" % direction[:100])
