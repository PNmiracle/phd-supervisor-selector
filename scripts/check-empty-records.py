import json, subprocess

env = json.load(open('env.json'))
token = env['VIKA_TOKEN']

# Check empty records
payload = {
    "pageSize": 2,
    "filter": {
        "conjunction": "and",
        "conditions": [{
            "fieldName": "选导意向（点击选择）",
            "operator": "is_empty"
        }]
    }
}

result = subprocess.run(
    ['curl', '-s', '-X', 'POST',
     'https://api.vika.cn/fusion/v1/datasheets/dstlVQ3Wx5UcFdYJx9/records',
     '-H', f'Authorization: Bearer {token}',
     '-H', 'Content-Type: application/json',
     '-d', json.dumps(payload)],
    capture_output=True, text=True
)
data = json.loads(result.stdout)
print('Total empty records:', data.get('data', {}).get('total', 'N/A'))
print('PageToken:', data.get('data', {}).get('pageToken', 'N/A'))
records = data.get('data', {}).get('records', [])
for r in records:
    fields = r.get('fields', {})
    print('Record ID:', r.get('recordId'))
    for k, v in fields.items():
        print(f'  {k}: {v}')
