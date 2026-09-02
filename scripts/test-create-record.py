import json
import urllib.request

env = json.load(open('env.json'))
token = env['VIKA_TOKEN']

# Test: try to create one new record
url = 'https://api.vika.cn/fusion/v1/datasheets/dstlVQ3Wx5UcFdYJx9/records'

# First, let's get the school ID for Syracuse from the master school table
school_url = 'https://api.vika.cn/fusion/v1/datasheets/dstMNzQU9Aa58DpgW3/records?pageSize=200'
school_req = urllib.request.Request(
    school_url,
    headers={'Authorization': f'Bearer {token}'},
    method='GET'
)

try:
    with urllib.request.urlopen(school_req, timeout=20) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        schools = result.get('data', {}).get('records', [])
        print(f'Found {len(schools)} schools in master table')
        for s in schools:
            name = s.get('fields', {}).get('学校名字', '')
            if 'Syracuse' in name or 'syracuse' in name.lower():
                print(f'  Syracuse: {s.get("recordId")} | {name}')
except Exception as e:
    print(f'School lookup error: {e}')
