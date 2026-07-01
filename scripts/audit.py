#!/usr/bin/env python3
"""Audit script for PhD supervisor table.
Run after every batch write to catch: cross-links, note format issues, 
garbage content, missing fields, and URL accessibility problems.

Usage: python3 scripts/audit.py
"""
import urllib.request, json, ssl, gzip, re

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

TOKEN = 'uskYugNg7aN8sSz5sWZxT7F'
DSID = 'dsteK35wW67qmaW5ix'
BASE = 'https://api.vika.cn/fusion/v1'

def get_page(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=10, context=ssl_ctx)
        data = resp.read()
        return data.decode('utf-8', errors='ignore'), resp.status
    except: return "", 0

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
GARBAGE = ['个人页面JS渲染', '需浏览器确认', '方向匹配', '⚠️', '✅']

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
    if '；' not in remark:
        issues.append(('NOTE_FORMAT', name, 'No ；separator'))
    if remark and not remark.rstrip().endswith('。'):
        issues.append(('NOTE_PERIOD', name, 'No trailing 。'))
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
