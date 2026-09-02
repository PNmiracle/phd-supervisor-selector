import json
import urllib.request

env = json.load(open('env.json'))
token = env['VIKA_TOKEN']

# Search for schools using a filter on 学校全称
# Try Syracuse first as a test
url = 'https://api.vika.cn/fusion/v1/datasheets/dstMNzQU9Aa58DpgW3/records'

search_terms = [
    'Syracuse', 'Colorado Boulder', 'South Florida', 'Minnesota',
    'Indiana University', 'Florida State', 'Delaware', 'South Carolina',
    'Virginia Tech', 'Washington', 'Oregon State', 'Washington State',
    'Nevada Reno', 'New Mexico', 'Oklahoma', 'Arizona'
]

found = {}

for term in search_terms:
    payload = json.dumps({
        "pageSize": 5,
        "filter": {
            "conjunction": "and",
            "conditions": [{
                "fieldName": "学校全称",
                "operator": "contains",
                "value": [term]
            }]
        }
    }).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            records = result.get('data', {}).get('records', [])
            for r in records:
                fields = r.get('fields', {})
                name = fields.get('学校全称', '')
                rid = r.get('recordId')
                usnews = fields.get('2026年USNews排名', '')
                print(f'  [{term}] {rid} | {name} | USNews: {usnews}')
                found[name] = rid
    except Exception as e:
        print(f'Error searching {term}: {e}')

print('\n=== Summary ===')
for name, rid in found.items():
    print(f'{rid} | {name}')
