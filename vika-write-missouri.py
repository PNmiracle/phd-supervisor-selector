#!/usr/bin/env python3
import json, ssl, time
from urllib.request import Request, urlopen

with open('env.json') as f:
    token = json.load(f)['VIKA_TOKEN']

BASE = 'https://api.vika.cn/fusion/v1'
SCHOOL_TBL = 'dstMNzQU9Aa58DpgW3'
ADVISOR_TBL = 'dstmnEscdKenfRSEL0'
SCHOOL_LINK_FLD = 'fldFfXtdDSST1'

ctx = ssl.create_default_context()
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def vika(method, path, body=None, timeout=150):
    url = f'{BASE}/{path}'
    data = json.dumps(body).encode() if body else None
    req = Request(url, data=data, headers=headers, method=method)
    print(f"  [{time.strftime('%H:%M:%S')}] Sending {method} to {path}...", flush=True)
    with urlopen(req, timeout=timeout, context=ctx) as r:
        return json.loads(r.read())

# Step 1: Create Missouri school
print("Creating Missouri school...")
mo = vika('POST', f'datasheets/{SCHOOL_TBL}/records', {
    'fields': {
        '学校全称': 'University of Missouri',
        '学校中文名': '密苏里大学哥伦比亚分校',
        '2027年QS排名': 641,
        '2026年QS排名': 641,
        '2025年QS排名': 586,
        '2026年USNews排名': 102,
        '2025usnews': '102',
        '国家/地区': 'United States',
        '所在大洲': 'North America',
        '美国学校所在州': '密苏里州'
    }
}, timeout=150)
mo_id = mo.get('data',{}).get('records',[{}])[0].get('recordId')
print(f"Missouri school recordId: {mo_id}")

# Step 2: Create Iowa State school
print("Creating Iowa State school...")
ia = vika('POST', f'datasheets/{SCHOOL_TBL}/records', {
    'fields': {
        '学校全称': 'Iowa State University of Science and Technology',
        '学校中文名': '爱荷华州立大学',
        '2027年QS排名': 449,
        '2026年QS排名': 449,
        '2025年QS排名': 369,
        '2026年USNews排名': 380,
        '2025usnews': '380',
        '国家/地区': 'United States',
        '所在大洲': 'North America',
        '美国学校所在州': '爱荷华州'
    }
}, timeout=150)
ia_id = ia.get('data',{}).get('records',[{}])[0].get('recordId')
print(f"Iowa State school recordId: {ia_id}")

# Step 3: Create Amy Petry advisor with Missouri school link
print("Creating Amy Petry advisor...")
petry = vika('POST', f'datasheets/{ADVISOR_TBL}/records', {
    'fields': {
        '导师': 'Amy Petry',
        '导师主页': 'https://www.cafnr.missouri.edu/directory/amy-petry/',
        '导师联系方式': 'petrya@missouri.edu',
        '导师研究领域': 'Swine nutrition; dietary fiber utilization in gestating sows; bison nutritional physiology; swine biomedical models; mineral and vitamin requirements in bison',
        '备注': 'Assistant Professor; swine nutrition primary research focus; bison nutrition secondary; monogastric nutrition; no GRE required for Animal Sciences PhD; program admits fall/spring with rolling basis; GRA via individual faculty support. Direction caveat: swine = livestock, not companion animal, listed with lenient interpretation per user guidance.',
        '待确认导师': '待确认',
        SCHOOL_LINK_FLD: [mo_id]
    }
}, timeout=150)
petry_id = petry.get('data',{}).get('records',[{}])[0].get('recordId')
print(f"Amy Petry recordId: {petry_id}")

print("\n=== All done ===")
print(f"Missouri school: {mo_id}")
print(f"Iowa State school: {ia_id}")
print(f"Amy Petry advisor: {petry_id}")
