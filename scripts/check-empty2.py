import json
import urllib.request
import urllib.parse

env = json.load(open('env.json'))
token = env['VIKA_TOKEN']

url = 'https://api.vika.cn/fusion/v1/datasheets/dstlVQ3Wx5UcFdYJx9/records'
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

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(
    url,
    data=data,
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    },
    method='POST'
)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        total = result.get('data', {}).get('total', 'N/A')
        page_token = result.get('data', {}).get('pageToken', 'N/A')
        print(f'Total empty records: {total}')
        print(f'PageToken: {page_token}')
        records = result.get('data', {}).get('records', [])
        for r in records:
            fields = r.get('fields', {})
            print('Record ID:', r.get('recordId'))
            for k, v in fields.items():
                print(f'  {k}: {v}')
except Exception as e:
    print(f'Error: {e}')
    # Try GET to get total count
    req2 = urllib.request.Request(
        url + '?pageSize=1',
        headers={'Authorization': f'Bearer {token}'},
        method='GET'
    )
    try:
        with urllib.request.urlopen(req2, timeout=10) as resp2:
            result2 = json.loads(resp2.read().decode('utf-8'))
            total2 = result2.get('data', {}).get('total', 'N/A')
            print(f'GET total records: {total2}')
    except Exception as e2:
        print(f'GET Error: {e2}')
