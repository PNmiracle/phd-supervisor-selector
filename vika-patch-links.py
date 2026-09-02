#!/usr/bin/env python3
"""PATCH OneWayLink for 5 existing advisor records. PATCH confirmed working."""
import json, ssl
from urllib.request import Request, urlopen

with open('env.json') as f:
    token = json.load(f)['VIKA_TOKEN']

ADVISOR_TBL = 'dstmnEscdKenfRSEL0'
LINK_FLD = 'fldFfXtdDSST1'

ctx = ssl.create_default_context()
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def get_school_recordId(name_en):
    url = f'https://api.vika.cn/fusion/v1/datasheets/dstMNzQU9Aa58DpgW3/records?maxRecords=200&pageSize=200&cellFormat=string'
    req = Request(url, headers=headers)
    with urlopen(req, timeout=15, context=ctx) as r:
        records = json.loads(r.read())['data']['records']
    for rec in records:
        if rec['fields'].get('学校全称', '') == name_en:
            return rec['recordId']
    return None

# Known school IDs (will verify first)
test_schools = [
    'Cornell University',
    'University of Illinois Urbana-Champaign',
    'Kansas State University',
    'University of Georgia',
    'Auburn University',
    'West Virginia University',
    'University of Missouri',
    'Iowa State University of Science and Technology',
]

print('=== Checking existing school records ===')
school_ids = {}
for name in test_schools:
    rid = get_school_recordId(name)
    school_ids[name] = rid
    print(f'  {name}: {rid}')

# Advisor records to patch
advisor_map = {
    'recId14ZthUEr': school_ids.get('Cornell University'),
    'reco4VlhsBX1O': school_ids.get('Kansas State University'),
    'recc5fDCLkIhM': school_ids.get('West Virginia University'),
    'rechYajh5La5n': school_ids.get('Iowa State University of Science and Technology'),
    'recrYYgU1QYRR': school_ids.get('Iowa State University of Science and Technology'),
}

print('\n=== PATCH OneWayLink ===')
patches = []
for arid, srid in advisor_map.items():
    if srid:
        patches.append({'recordId': arid, 'fields': {LINK_FLD: [srid]}})
        print(f'  PATCH {arid} → {srid}')

if patches:
    url = f'https://api.vika.cn/fusion/v1/datasheets/{ADVISOR_TBL}/records'
    body = json.dumps({'records': patches}).encode()
    req = Request(url, data=body, headers=headers, method='PATCH')
    with urlopen(req, timeout=20, context=ctx) as r:
        result = json.loads(r.read())
    print(f'Result: code={result.get("code")} success={result.get("success")}')
    for rec in result.get('data', {}).get('records', []):
        print(f'  {rec["recordId"]}: updatedAt={rec.get("updatedAt")}')
else:
    print('No valid patches (schools not yet in table)')
