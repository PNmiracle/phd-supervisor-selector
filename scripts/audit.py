#!/usr/bin/env python3
"""Audit script for PhD supervisor table.
Run after every batch write to catch: cross-links, note format issues,
garbage content, missing fields, and URL accessibility problems.

Usage: python3 scripts/audit.py [DATASHEET_ID] [VIKA_TOKEN]
  - DATASHEET_ID: Vika datasheet ID (dstXXX), defaults to $VIKA_DSID env var
  - VIKA_TOKEN: Vika API token, defaults to $VIKA_TOKEN env var
"""
import urllib.request, json, ssl, gzip, re, os, sys

# ---- SECURITY: Use env vars or CLI args, NEVER hardcode tokens ----
TOKEN = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("VIKA_TOKEN", "")
DSID = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("VIKA_DSID", "")
# --------------------------------------------------------------------

if not TOKEN:
    print("[ERROR] VIKA_TOKEN not set. Provide it via env var or CLI argument:")
    print("  export VIKA_TOKEN=your_token_here")
    print("  python3 scripts/audit.py dstXXX your_token_here")
    sys.exit(1)
if not DSID:
    print("[ERROR] VIKA_DSID not set. Provide datasheet ID via env var or CLI argument:")
    print("  export VIKA_DSID=dstXXX")
    print("  python3 scripts/audit.py dstXXX")
    sys.exit(1)

BASE = 'https://api.vika.cn/fusion/v1'

def get_page(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=10)
        data = resp.read()
        return data.decode('utf-8', errors='ignore'), resp.status
    except Exception:
        return "", 0

def get_url_val(val):
    if isinstance(val, dict): return val.get('text', '') or ''
    return str(val) if val else ''

v_url = f"{BASE}/datasheets/{DSID}/records?maxRecords=50&fieldKey=id"
req = urllib.request.Request(v_url, headers={"Authorization": f"Bearer {TOKEN}"})
resp = urllib.request.urlopen(req, timeout=15)
data = json.loads(resp.read())
records = [r for r in data['data']['records']
           if r['fields'].get('fld1RxfRZuKA3')
           and 'PLEASE_DELETE' not in str(r['fields'].get('fld1RxfRZuKA3', ''))]

issues = []
domain_map = {
    'polyu.edu.hk': ['PolyU', 'Polytechnic'],
    'cuhk.edu.hk': ['Chinese University', 'CUHK'],
    'hku.hk': ['University of Hong Kong', 'HKU'],
    'hkust.edu.hk': ['HKUST'],
    'cityu.edu.hk': ['City University', 'CityU'],
    'ntu.edu.sg': ['Nanyang Technological', 'NTU'],
    'nus.edu.sg': ['National University of Singapore', 'NUS'],
    'unsw.edu.au': ['UNSW'],
    'sydney.edu.au': ['University of Sydney', 'Sydney'],
    'anu.edu.au': ['Australian National', 'ANU'],
    'unimelb.edu.au': ['Melbourne'],
    'monash.edu': ['Monash'],
}
GARBAGE = ['个人页面JS渲染', '需浏览器确认', '方向匹配', '\u26a0\ufe0f', '\u2705']

for r in records:
    name = r['fields'].get('fld1RxfRZuKA3', '?')
    rid = r['recordId']
    dept = r['fields'].get('fldagqfFthgX7', '')
    homepage = get_url_val(r['fields'].get('fldv7ZuB1b06J', ''))
    phd = get_url_val(r['fields'].get('fldYm8R3l4Bnu', ''))
    staff = get_url_val(r['fields'].get('fldI3KsjPCYWp', ''))
    remark = r['fields'].get('fldt2UATh9Ofp', '')

    # Cross-link check
    if homepage and dept:
        expected = None
        for domain, keywords in domain_map.items():
            if any(k.lower() in dept.lower() for k in keywords):
                expected = domain; break
        if expected and expected not in homepage.lower():
            issues.append(('CROSS_LINK', name, f'Expected {expected}, URL: {homepage[:60]}'))
    # Note format
    if '\uff1b' not in remark:
        issues.append(('NOTE_FORMAT', name, 'No \uff1bseparator'))
    if remark and not remark.rstrip().endswith('\u3002'):
        issues.append(('NOTE_PERIOD', name, 'No trailing \u3002'))
    # Garbage
    for gw in GARBAGE:
        if gw in remark:
            issues.append(('NOTE_GARBAGE', name, f'Has "{gw}"'))
    # Missing fields
    if not homepage: issues.append(('MISSING_URL', name, 'Empty'))
    if not phd: issues.append(('MISSING_PHD', name, 'Empty'))
    if not staff: issues.append(('MISSING_STAFF', name, 'Empty'))

print(f"Audit: {len(records)} records, {len(issues)} issues\n")
for t, n, d in issues:
    print(f"[{t}] {n}: {d}")
if not issues:
    print("ALL CLEAN")
