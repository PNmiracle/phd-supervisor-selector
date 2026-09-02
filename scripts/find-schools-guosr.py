#!/usr/bin/env python3
"""Search school main table for candidate US schools."""
import json, ssl
from urllib.request import Request, urlopen

with open('/Users/leyiqingxue/.workbuddy/skills/phd-supervisor-selector/env.json') as f:
    token = json.load(f)['VIKA_TOKEN']

BASE = 'https://api.vika.cn/fusion/v1'
SCHOOL_TBL = 'dstMNzQU9Aa58DpgW3'
ctx = ssl.create_default_context()
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def vika(method, path):
    url = f'{BASE}{path}'
    req = Request(url, headers=headers, method=method)
    with urlopen(req, timeout=30, context=ctx) as r:
        return json.loads(r.read())

# pull all schools
all_records = []
page = 1
while True:
    r = vika('GET', f'/datasheets/{SCHOOL_TBL}/records?pageSize=500&pageNum={page}&cellFormat=string')
    recs = r.get('data', {}).get('records', [])
    total = r.get('data', {}).get('total', 0)
    all_records.extend(recs)
    print(f'Page {page}: {len(recs)} (cumulative {len(all_records)}/{total})')
    if len(recs) < 500 or len(all_records) >= total:
        break
    page += 1

print(f'Total schools: {len(all_records)}')

targets = ['Syracuse', 'Colorado Boulder', 'Delaware', 'Florida State', 'South Carolina',
           'Arizona', 'Georgia', 'Washington', 'Kentucky', 'Iowa', 'Oregon State',
           'Washington State', 'New Mexico', 'Oklahoma', 'Nevada Reno', 'South Florida',
           'Kansas State', 'Ohio State', 'Colorado Denver', 'UMass', 'Virginia Tech']

for rec in all_records:
    fields = rec['fields']
    name = fields.get('学校全称', '') or fields.get('学校中文名', '') or ''
    rid = rec['recordId']
    for t in targets:
        if t.lower() in name.lower():
            us = fields.get('2025年USNews排名', '') or fields.get('美国学校所在州', '') or ''
            print(f'{rid}\t{name}\tUSNews={us}')
            break
