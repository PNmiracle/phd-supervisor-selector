#!/usr/bin/env python3
"""List all records summary in 郭书睿 table."""
import json, ssl
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
    with urlopen(req, timeout=30, context=ctx) as r:
        return json.loads(r.read())

all_records = []
page = 1
while True:
    r = vika('GET', f'/datasheets/{DS}/records?maxRecords=500&pageNum={page}&cellFormat=string')
    recs = r.get('data', {}).get('records', [])
    total = r.get('data', {}).get('total', 0)
    all_records.extend(recs)
    if len(recs) < 500 or len(all_records) >= total:
        break
    page += 1

for rec in all_records:
    fields = rec['fields']
    rid = rec['recordId']
    sup = fields.get('导师', '')
    school = fields.get('学校名字', '')
    if isinstance(school, list):
        school = ','.join(school)
    link = fields.get('选导意向（点击选择）', '')
    status = 'LOCKED' if link else 'EDITABLE'
    print(f'{status}\t{sup}\t{school}\t{rid}')
