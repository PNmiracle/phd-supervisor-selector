#!/usr/bin/env python3
"""Check current state of 郭书睿 selection table."""
import json, ssl, sys
from urllib.request import Request, urlopen

with open('/Users/leyiqingxue/.workbuddy/skills/phd-supervisor-selector/env.json') as f:
    token = json.load(f)['VIKA_TOKEN']

BASE = 'https://api.vika.cn/fusion/v1'
DS = 'dstlVQ3Wx5UcFdYJx9'
ctx = ssl.create_default_context()
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def vika(method, path):
    url = f'{BASE}{path}'
    req = Request(url, headers=headers, method=method)
    try:
        with urlopen(req, timeout=30, context=ctx) as r:
            return json.loads(r.read())
    except Exception as e:
        return {'error': str(e)}

print('=== FIELDS ===')
r = vika('GET', f'/datasheets/{DS}/fields')
if 'error' in r:
    print(f'Fields Error: {r}')
    sys.exit(1)
for f in r['data']['fields']:
    fname = f['name']
    ftype = f['type']
    fid = f['id']
    if ftype == 'OneWayLink':
        fds = f.get('property', {}).get('foreignDatasheetId', '')
        print(f'  OneWayLink: {fname} -> {fds} [id={fid}]')
    else:
        print(f'  {fname} ({ftype}) [id={fid}]')

print('\n=== RECORDS (paginated) ===')
all_records = []
page = 1
while True:
    r = vika('GET', f'/datasheets/{DS}/records?maxRecords=500&pageNum={page}&cellFormat=string')
    if 'error' in r:
        print(f'Page {page} Error: {r}')
        break
    recs = r.get('data', {}).get('records', [])
    total = r.get('data', {}).get('total', 0)
    all_records.extend(recs)
    if len(recs) < 500 or len(all_records) >= total:
        break
    page += 1

print(f'Total fetched: {len(all_records)} / {total}')
locked = [x for x in all_records if x['fields'].get('选导意向（点击选择）')]
editable = [x for x in all_records if not x['fields'].get('选导意向（点击选择）')]
print(f'LOCKED (选导意向非空): {len(locked)}')
print(f'EDITABLE: {len(editable)}')

print('\n=== EDITABLE RECORDS ===')
for rec in editable:
    fields = rec['fields']
    rid = rec['recordId']
    print(f'  {rid}')
    for k, v in fields.items():
        sv = str(v)
        print(f'    {k}: {sv[:150]}')

print('\n=== ALL RECORD KEYS (sample) ===')
if all_records:
    for k in all_records[0]['fields'].keys():
        print(f'  {k}')
