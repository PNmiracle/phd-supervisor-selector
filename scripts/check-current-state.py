#!/usr/bin/env python3
import urllib.request, urllib.error, json, re, os

# Read token from ~/.zshrc
token = ""
with open(os.path.expanduser("~/.zshrc")) as f:
    for line in f:
        m = re.match(r'export VIKA_TOKEN=(.+)', line.strip())
        if m:
            token = m.group(1).strip().strip('"').strip("'")
            break

if not token:
    print("ERROR: VIKA_TOKEN not found in ~/.zshrc")
    exit(1)

print(f"Token: {token[:8]}...")

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
        body = e.read()
        return {"error": f"HTTP {e.code}", "body": body[:500]}
    except Exception as e:
        return {"error": str(e)}

# Get fields
print("\n=== FIELDS ===")
r = vika("GET", "/datasheets/dstmnEscdKenfRSEL0/fields")
if "error" in r:
    print(f"Fields Error: {r}")
else:
    for f in r["data"]["fields"]:
        fname = f["name"]
        ftype = f["type"]
        fid = f["id"]
        if ftype == "OneWayLink":
            fid_ds = f.get("property", {}).get("foreignDatasheetId", "")
            print(f"  OneWayLink: {fname} -> {fid_ds}")
        else:
            print(f"  {fname} ({ftype}) [id={fid}]")

# Get all records
print("\n=== RECORDS ===")
r = vika("GET", "/datasheets/dstmnEscdKenfRSEL0/records?maxRecords=500&cellFormat=string")
if "error" in r:
    print(f"Records Error: {r}")
else:
    records = r.get("data", {}).get("records", [])
    total = r.get("data", {}).get("total", 0)
    print(f"Total: {len(records)} / {total}")
    for rec in records:
        fields = rec.get("fields", {})
        supervisor = fields.get("导师", "")
        school = fields.get("学校", "")
        direction = fields.get("研究方向", "")
        rid = rec.get("recordId", "")
        link = fields.get("选导意向（点击选择）", "")
        status = "[LOCKED]" if link else "[EDITABLE]"
        print(f"  {status} {rid}: {supervisor} @ {school}")
        if direction:
            print(f"    Direction: {direction[:80]}")
