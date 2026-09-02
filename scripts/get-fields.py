import json
import urllib.request

env = json.load(open('env.json'))
token = env['VIKA_TOKEN']

# Simple GET to get field info
url = 'https://api.vika.cn/fusion/v1/datasheets/dstlVQ3Wx5UcFdYJx9/fields'
req = urllib.request.Request(
    url,
    headers={'Authorization': f'Bearer {token}'},
    method='GET'
)

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        fields = result.get('data', {}).get('fields', [])
        print(f'Total fields: {len(fields)}')
        for f in fields:
            print(f"  {f['id']} | {f['name']} | type={f.get('type','?')} | property={json.dumps(f.get('property',{}))[:80]}")
except Exception as e:
    print(f'Error: {e}')
