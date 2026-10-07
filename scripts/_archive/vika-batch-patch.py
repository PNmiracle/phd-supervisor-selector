#!/usr/bin/env python3
"""
PATCH batch: fill in OneWayLink school links for 5 existing advisor records.
All PATCH operations confirmed working (PATCH times out at 15s, not the same as POST).
"""
import json, ssl, time
from urllib.request import Request, urlopen

with open('env.json') as f:
    token = json.load(f)['VIKA_TOKEN']

BASE = 'https://api.vika.cn/fusion/v1'
ADVISOR_TBL = 'dstmnEscdKenfRSEL0'
SCHOOL_TBL = 'dstMNzQU9Aa58DpgW3'
LINK_FLD = 'fldFfXtdDSST1'

ctx = ssl.create_default_context()
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def patch(table, records):
    """PATCH records (confirmed working)."""
    url = f'{BASE}/datasheets/{table}/records'
    body = json.dumps({'records': records}).encode()
    req = Request(url, data=body, headers=headers, method='PATCH')
    with urlopen(req, timeout=20, context=ctx) as r:
        return json.loads(r.read())

def post(table, fields, timeout=30):
    """POST a single record. May timeout if Vika is overloaded."""
    url = f'{BASE}/datasheets/{table}/records'
    body = json.dumps({'fields': fields}).encode()
    req = Request(url, data=body, headers=headers, method='POST')
    try:
        with urlopen(req, timeout=timeout, context=ctx) as r:
            return json.loads(r.read())
    except Exception as e:
        return {'error': str(e)}

def get_field_name(table, field_id):
    """Get field name by ID."""
    url = f'{BASE}/datasheets/{table}/fields'
    req = Request(url, headers=headers)
    with urlopen(req, timeout=10, context=ctx) as r:
        fields = json.loads(r.read())['data']['fields']
    for f in fields:
        if f['id'] == field_id:
            return f['name']
    return field_id

def get_school_recordId(school_en):
    """Find school recordId by English name."""
    url = f'{BASE}/datasheets/{SCHOOL_TBL}/records?maxRecords=200&pageSize=200&cellFormat=string'
    req = Request(url, headers=headers)
    with urlopen(req, timeout=15, context=ctx) as r:
        records = json.loads(r.read())['data']['records']
    for rec in records:
        if rec['fields'].get('学校全称', '') == school_en:
            return rec['recordId']
    return None

# ── Step 1: Create school records ─────────────────────────────────────────────
school_creates = []

def try_create_school(name_en, name_cn, qs, usnews, state):
    """Create school and return recordId."""
    body = {
        'fields': {
            '学校全称': name_en,
            '学校中文名': name_cn,
            '2027年QS排名': qs,
            '2026年QS排名': qs,
            '2026年USNews排名': usnews,
            '国家/地区': 'United States',
            '所在大洲': 'North America',
            '美国学校所在州': state
        }
    }
    result = post(SCHOOL_TBL, body, timeout=30)
    if 'error' in result:
        # Try with field ID key instead of name
        result = post_with_field_id(SCHOOL_TBL, body, timeout=30)
    if 'error' in result:
        print(f'  [SKIP] {name_en} POST failed: {result["error"]}')
        return None
    rid = result.get('data', {}).get('records', [{}])[0].get('recordId')
    print(f'  Created {name_en} → {rid}')
    return rid

def post_with_field_id(table, fields_body, timeout=30):
    """Try POST with field IDs."""
    # Get field IDs
    url = f'{BASE}/datasheets/{table}/fields'
    req = Request(url, headers=headers)
    with urlopen(req, timeout=10, context=ctx) as r:
        field_map = {f['name']: f['id'] for f in json.loads(r.read())['data']['fields']}

    # Translate field names to IDs
    id_fields = {}
    for k, v in fields_body['fields'].items():
        if k in field_map:
            id_fields[field_map[k]] = v
        else:
            id_fields[k] = v

    url2 = f'{BASE}/datasheets/{table}/records'
    body2 = json.dumps({'fields': id_fields}).encode()
    req2 = Request(url2, data=body2, headers=headers, method='POST')
    try:
        with urlopen(req2, timeout=timeout, context=ctx) as r:
            return json.loads(r.read())
    except Exception as e:
        return {'error': str(e)}

# Schools to create
schools_to_create = [
    ('Cornell University', '康奈尔大学', 17, 11, '纽约州'),
    ('University of Illinois Urbana-Champaign', '伊利诺伊大学香槟分校', 69, 33, '伊利诺伊州'),
    ('Kansas State University', '堪萨斯州立大学',  1001, 166, '堪萨斯州'),
    ('University of Georgia', '佐治亚大学', 304, 46, '佐治亚州'),
    ('Auburn University', '奥本大学', 380, 93, '阿拉巴马州'),
    ('West Virginia University', '西弗吉尼亚大学', 1001, 667, '西弗吉尼亚州'),
    ('University of Missouri', '密苏里大学哥伦比亚分校', 641, 102, '密苏里州'),
    ('Iowa State University of Science and Technology', '爱荷华州立大学', 449, 380, '爱荷华州'),
]

print('=== Step 1: School Records ===')
created_schools = {}
for name_en, name_cn, qs, usnews, state in schools_to_create:
    # Check if already exists
    existing = get_school_recordId(name_en)
    if existing:
        print(f'  [EXISTS] {name_en} = {existing}')
        created_schools[name_en] = existing
    else:
        rid = try_create_school(name_en, name_cn, qs, usnews, state)
        if rid:
            created_schools[name_en] = rid
        time.sleep(1)

print(f'\nCreated/existing schools: {created_schools}')

# ── Step 2: PATCH advisor records with school links ───────────────────────────
advisor_school_map = {
    'recId14ZthUEr': created_schools.get('Cornell University'),
    'recoohzKSR3bK': created_schools.get('University of Illinois Urbana-Champaign'),
    'recdxwBWh5hUx': created_schools.get('University of Illinois Urbana-Champaign'),
    'reco4VlhsBX1O': created_schools.get('Kansas State University'),
    'reccT92L2JHDB': created_schools.get('University of Georgia'),
    'recieA7bzXEgP': created_schools.get('University of Georgia'),
    'reccVvj7GXepx': created_schools.get('Auburn University'),
    'recc5fDCLkIhM': created_schools.get('West Virginia University'),
    'rechYajh5La5n': created_schools.get('Iowa State University of Science and Technology'),
    'recrYYgU1QYRR': created_schools.get('Iowa State University of Science and Technology'),
    # Amy Petry: create record + link separately (after Missouri school confirmed)
}

print('\n=== Step 2: PATCH Advisor Links ===')
records_to_patch = []
for advisor_rid, school_rid in advisor_school_map.items():
    if school_rid:
        records_to_patch.append({
            'recordId': advisor_rid,
            'fields': {LINK_FLD: [school_rid]}
        })
        print(f'  Will PATCH advisor {advisor_rid} → school {school_rid}')

if records_to_patch:
    result = patch(ADVISOR_TBL, records_to_patch)
    print(f'  PATCH result: code={result.get("code")} msg={result.get("message","")}')
    for rec_resp in result.get('data', {}).get('records', []):
        print(f'    {rec_resp["recordId"]} updated OK')
else:
    print('  No valid patches to apply')

# ── Step 3: Amy Petry (depends on Missouri school) ────────────────────────────
if created_schools.get('University of Missouri'):
    print('\n=== Step 3: Amy Petry Advisor Record ===')
    mo_school_rid = created_schools['University of Missouri']
    petry_fields = {
        '导师': 'Amy Petry',
        '导师主页': 'https://www.cafnr.missouri.edu/directory/amy-petry/',
        '导师联系方式': 'petrya@missouri.edu',
        '导师研究领域': 'Swine nutrition; dietary fiber utilization in gestating sows; bison nutritional physiology; swine biomedical models; mineral and vitamin requirements in bison',
        '备注': 'Assistant Professor; swine nutrition primary; bison nutrition secondary; monogastric nutrition; no GRE required; program admits fall/spring rolling; GRA via individual faculty support. Direction caveat: swine = livestock, not companion animal; listed with lenient interpretation per user guidance.',
        '待确认导师': '待确认',
        LINK_FLD: [mo_school_rid]
    }
    # Create Amy Petry record via POST (not PATCH — PATCH only updates existing records)
    post_result = post(ADVISOR_TBL, petry_fields, timeout=30)
    if 'error' in post_result:
        print(f'  [SKIP] Amy Petry POST failed: {post_result["error"]}')
    else:
        petry_rid = post_result.get('data', {}).get('records', [{}])[0].get('recordId')
        print(f'  Created Amy Petry → {petry_rid}')
        # PATCH to fill OneWayLink (POST can't set OneWayLink in single step)
        link_patch_result = patch(ADVISOR_TBL, [{'recordId': petry_rid, 'fields': {LINK_FLD: [mo_school_rid]}}])
        print(f'  Amy Petry link PATCH: code={link_patch_result.get("code")} msg={link_patch_result.get("message","")}')
else:
    print('\n  Missouri school not created; skipping Amy Petry write')

print('\n=== Done ===')
print(f'Schools created: {created_schools}')
