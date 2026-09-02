import json
import urllib.request

env = json.load(open('env.json'))
token = env['VIKA_TOKEN']

# Check school table fields
url = 'https://api.vika.cn/fusion/v1/datasheets/dstMNzQU9Aa58DpgW3/fields'
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
            fid = f.get('id','')
            fname = f.get('name','')
            ftype = f.get('type','?')
            print(f'  {fid} | {fname} | type={ftype}')
except Exception as e:
    print(f'Error: {e}')
