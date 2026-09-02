import json
import urllib.request

env = json.load(open('env.json'))
token = env['VIKA_TOKEN']

# Get records with empty 选导意向 (filter by SingleSelect being empty)
# First try to get first page of all records and check which ones have empty 选导意向
url = 'https://api.vika.cn/fusion/v1/datasheets/dstlVQ3Wx5UcFdYJx9/records?pageSize=100'
req = urllib.request.Request(
    url,
    headers={'Authorization': f'Bearer {token}'},
    method='GET'
)

try:
    with urllib.request.urlopen(req, timeout=20) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        data = result.get('data', {})
        total = data.get('total', 'N/A')
        records = data.get('records', [])
        print(f'Total records: {total}')
        print(f'Records on this page: {len(records)}')

        empty_count = 0
        editable_ids = []
        locked_count = 0

        for r in records:
            fields = r.get('fields', {})
            record_id = r.get('recordId')
            choice = fields.get('选导意向（点击选择）', '')
            if choice == '' or choice is None:
                empty_count += 1
                editable_ids.append(record_id)
                print(f'EDITABLE: {record_id} | 导师: {fields.get("导师", "")} | 状态: {fields.get("状态", "")}')
            else:
                locked_count += 1

        print(f'\nEditable (empty): {empty_count}')
        print(f'Locked: {locked_count}')
        print(f'Editable IDs: {editable_ids}')
except Exception as e:
    print(f'Error: {e}')
