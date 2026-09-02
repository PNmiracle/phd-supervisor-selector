#!/usr/bin/env python3
"""Batch insert Guo Shurui supervisor candidates into Vika table."""
import json, ssl, time, sys
from urllib.request import Request, urlopen

with open('/Users/leyiqingxue/.workbuddy/skills/phd-supervisor-selector/env.json') as f:
    token = json.load(f)['VIKA_TOKEN']

BASE = 'https://api.vika.cn/fusion/v1'
DT = 'dstlVQ3Wx5UcFdYJx9'  # Guo Shurui table
ctx = ssl.create_default_context()
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def vika(method, path, data=None):
    url = f'{BASE}{path}'
    req = Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode('utf-8')
    with urlopen(req, timeout=30, context=ctx) as r:
        return json.loads(r.read())

# All 20 candidates with full data
CANDIDATES = [
    # === BATCH 1 ===
    {
        '导师': 'Farhana Sultana',
        '学校_rid': 'rece61lgVV0qx',
        'Department': 'Geography, Maxwell School, Syracuse University',
        'email': 'fsultana@syr.edu',
        '方向': 'Political ecology; water governance; climate justice; gender; South Asia',
        '主页': 'https://www.maxwell.syr.edu/geo/Sultana,_Farhana/',
        '申请': 'https://www.maxwell.syr.edu/geo/Geography-PhD-Program/',
        '档案': 'https://www.maxwell.syr.edu/geo/People/Faculty/Sultana/',
        '备注': '教授；政治生态学、水资源治理、气候正义、性别与发展、南亚地区。当前指导3名PhD学生（Brooklyn Montgomery、Avia Nahreen、Simran Sumbre，研究方向均为政治生态学+水资源治理+南亚）。Syracuse PhD项目72学分，全奖，GRE not required，Deadline January 1, 2027。建议申请前直接联系导师确认Fall 2027 advising availability。',
    },
    {
        '导师': 'Emily T. Yeh',
        '学校_rid': 'recCcM4y5KUvP',
        'Department': 'Department of Geography, University of Colorado Boulder',
        'email': 'emily.yeh@colorado.edu',
        '方向': 'Nature-society geography; political ecology; climate adaptation; Tibet/China; development',
        '主页': 'https://www.colorado.edu/geography/emily-yeh',
        '申请': 'https://www.colorado.edu/geography/graduate/phd-program',
        '档案': 'https://www.colorado.edu/geography/emily-yeh',
        '备注': '教授；自然社会地理、政治生态学、气候适应与山地环境、藏汉/中国、气候政治与政策、去碳化政治。课程含Climate Politics and Policy、Development Geography、Political Ecology。与郭书睿的气候适应与政治生态学方向高度匹配。需联系导师确认Fall 2027接收新生意愿。',
    },
    {
        '导师': 'Mara Goldman',
        '学校_rid': 'recCcM4y5KUvP',
        'Department': 'Department of Geography, University of Colorado Boulder',
        'email': 'mara.goldman@colorado.edu',
        '方向': 'Political ecology; science and technology studies; Indigenous knowledge; community-based conservation; gender; Africa',
        '主页': 'https://www.colorado.edu/geography/mara-goldman',
        '申请': 'https://www.colorado.edu/geography/graduate/phd-program',
        '档案': 'https://www.colorado.edu/geography/mara-goldman',
        '备注': '副教授；政治生态学、科技研究、原住民知识、社区保护、性别与资源获取、东非（肯尼亚、坦桑尼亚）、印度、蒙古等多地区。与郭书睿的气候适应与环境治理方向高度匹配，定性方法为主。需联系导师确认Fall 2027接收新生意愿。',
    },
    {
        '导师': 'Lindsay Naylor',
        '学校_rid': 'recixgtWRGFtP',
        'Department': 'Department of Geography, University of Delaware',
        'email': 'lnaylor@udel.edu',
        '方向': 'Feminist political geography; climate change adaptation; food and agricultural systems; gender',
        '主页': 'https://www.udel.edu/faculty/people/lindsay-naylor/',
        '申请': 'https://www.udel.edu/geography/graduate/phd-program/',
        '档案': 'https://www.udel.edu/geography/people/lindsay-naylor/',
        '备注': '副教授；女性主义政治地理学、气候变化适应、粮食与农业系统、性别研究。当前指导PhD学生Nusrat Mohana（研究孟加拉国与缅甸气候位移与性别），定性方法，与郭书睿的方向高度匹配。需联系导师确认Fall 2027接收新生意愿。',
    },
    {
        '导师': 'Richard Mbatu',
        '学校_rid': 'recHq4iWjnWHn',
        'Department': 'School of Geosciences, University of South Florida',
        'email': 'rmbatu@usf.edu',
        '方向': 'Political ecology; political economy of natural resources; global conservation; climate change; REDD+; Central Africa',
        '主页': 'https://www.usf.edu/geosciences/people/mbatu.aspx',
        '申请': 'https://www.usf.edu/geosciences/doctoral-program/index.aspx',
        '档案': 'https://www.usf.edu/geosciences/people/mbatu.aspx',
        '备注': '副教授；政治生态学、自然资源政治经济学、全球保护、气候变化、REDD+、中非。研究方向与郭书睿高度匹配。重要提示：USF博士项目要求仅full professors可担任dissertation advisor，Mbatu为Associate Professor，建议联系School of Geosciences Graduate Director确认其是否可在Tampa PhD项目担任导师，以及Fall 2027招生意愿。',
    },
    {
        '导师': 'Andrea K. Gerlak',
        '学校_rid': 'reciSLx0UAH51',
        'Department': 'School of Geography, Development & Environment, University of Arizona',
        'email': 'agerlak@arizona.edu',
        '方向': 'Water governance and policy; global environmental policy; transboundary waters; social-ecological systems; climate adaptation',
        '主页': 'https://profiles.arizona.edu/person/agerlak',
        '申请': 'https://geography.arizona.edu/graduate/phd',
        '档案': 'https://profiles.arizona.edu/person/agerlak',
        '备注': '教授/研究教授；水资源治理与政策、全球环境政策、跨国水资源、社会-生态系统、气候适应。2025-26学期有dissertation课程（证明当前active supervision），2026年指导PhD candidate获跨国水奖学金。与郭书睿的水资源治理+气候适应方向高度匹配。需联系导师确认Fall 2027接收新生意愿。',
    },
    {
        '导师': 'Margaret Wilder',
        '学校_rid': 'reciSLx0UAH51',
        'Department': 'School of Geography, Development & Environment, University of Arizona',
        'email': 'mwilder@arizona.edu',
        '方向': 'Human-environment geography; political ecology; critical water governance; US-Mexico border; climate vulnerability; water equity and justice',
        '主页': 'https://profiles.arizona.edu/person/mwilder',
        '申请': 'https://geography.arizona.edu/graduate/phd',
        '档案': 'https://profiles.arizona.edu/person/mwilder',
        '备注': '副教授；人类环境地理学、政治生态学、批判水资源治理、美墨边境水治理、气候脆弱性与适应、水公平与正义。官方档案明确写supervises several masters and doctoral students，定性方法。与郭书睿的政治生态学+水资源治理方向高度匹配。需联系导师确认Fall 2027接收新生意愿。',
    },
    {
        '导师': 'Todd Schenk',
        '学校_rid': 'recD1jCj2wDJF',
        'Department': 'School of Public and International Affairs / Geography, Virginia Tech',
        'email': 'todd.schenk@vt.edu',
        '方向': 'Climate adaptation; public participation; sustainable development; Vietnam and Mekong region',
        '主页': 'https://sspa.vt.edu/faculty/schenk-todd.html',
        '申请': 'https://sspa.vt.edu/academics/graduate-programs/phd-in-public-and-international-affairs.html',
        '档案': 'https://sspa.vt.edu/faculty/schenk-todd.html',
        '备注': '教授；气候变化适应、公众参与、可持续发展、湄公河流域治理（越南、泰国）。与郭书睿的气候适应+东南亚+定性方法方向高度匹配；官方PGG handbook明确列为其supporting faculty。需联系导师确认Fall 2027接收新生意愿和导师名额。',
    },
    {
        '导师': 'Nik Heynen',
        '学校_rid': 'recetH9PnLuoW',
        'Department': 'Department of Geography, University of Georgia',
        'email': 'nik@uga.edu',
        '方向': 'Urban political ecology; abolition ecology; environmental justice; social movements; racial capitalism',
        '主页': 'https://geography.uga.edu/people/faculty/nik-heynen',
        '申请': 'https://geography.uga.edu/graduate/phd-program',
        '档案': 'https://geography.uga.edu/people/faculty/nik-heynen',
        '备注': '杰出研究教授；城市政治生态学、废奴生态学、环境正义、社会运动、种族资本主义。当前指导PhD学生Jay Atkins和Jamie Jordan，研究含气候正义与种族正义。与郭书睿的政治生态学+环境正义方向有交集，但以城市+种族正义为主轴。需联系导师确认Fall 2027接收新生意愿。',
    },
    {
        '导师': 'Silvia Secchi',
        '学校_rid': 'reculX99RMAdk',
        'Department': 'Department of Geography, University of Iowa',
        'email': 'silvia-secchi@uiowa.edu',
        '方向': 'Climate adaptation; water sustainability; conservation policy; agricultural environmental impacts',
        '主页': 'https://clas.uiowa.edu/geography/people/silvia-secchi',
        '申请': 'https://geography.grad.uiowa.edu/',
        '档案': 'https://geography.grad.uiowa.edu/people/faculty',
        '备注': '副教授；气候变化适应、水资源可持续性、保护政策、农业环境影响。Alumni记录显示PhD supervision历史，方向高度相关，但研究使用integrated modeling方法，含有建模成分（需与郭书睿偏定性偏好做权衡）。需联系导师确认Fall 2027接收新生意愿。',
    },
    # === BATCH 2 ===
    {
        '导师': 'David Wrathall',
        '学校_rid': 'recVF83FGtuVn',
        'Department': 'College of Earth, Ocean, and Atmospheric Sciences (CEOAS) / Geography, Oregon State University',
        'email': 'david.wrathall@oregonstate.edu',
        '方向': 'Political ecology; climate hazards; climate change adaptation; social vulnerability; human migration',
        '主页': 'https://ceoas.oregonstate.edu/profile/wrathall',
        '申请': 'https://ceoas.oregonstate.edu/education/phd-program',
        '档案': 'https://ceoas.oregonstate.edu/profile/wrathall',
        '备注': '副教授；政治生态学、气候危害、气候变化适应、社会脆弱性、人类迁移。官方主页明确写Accepting for advising，IPCC AR6 WGII第8章主要作者，研究方向与郭书睿高度匹配。是目前所有候选中唯一明确标注接受新生的导师，建议优先联系。',
    },
    {
        '导师': 'Audrey Joslin',
        '学校_rid': 'recNp4BXQMo9u',
        'Department': 'Department of Geography and Geospatial Sciences, Kansas State University',
        'email': 'ajoslin@ksu.edu',
        '方向': 'Political ecology; environmental governance; conservation; market-based environmental initiatives; Latin America',
        '主页': 'https://www.k-state.edu/geography/people/faculty/joslin.html',
        '申请': 'https://www.k-state.edu/geography/graduate/phd.html',
        '档案': 'https://www.k-state.edu/geography/people/faculty/joslin.html',
        '备注': '副教授、研究生项目主任；政治生态学、环境治理、保护、市场化环境保护倡议、定性+混合方法。研究区域为厄瓜多尔安第斯山脉和大平原（美国），已在K-State建立政治生态学网络。与郭书睿的政治生态学方向高度匹配，方法为定性/混合（符合偏好）。2025年秋季有sabbatical，建议联系确认Fall 2027是否可接收新生。',
    },
    {
        '导师': 'Benjamin Warner',
        '学校_rid': 'rec7uiTsRfeCh',
        'Department': 'Department of Geography, University of New Mexico',
        'email': 'bwarner@unm.edu',
        '方向': 'Development geography; water governance; Central American development; agrarian adaptation; climate adaptation; mixed methods',
        '主页': 'https://geography.unm.edu/people/faculty/benjamin-warner/index.html',
        '申请': 'https://geography.unm.edu/graduate/phd-program/index.html',
        '档案': 'https://geography.unm.edu/people/faculty/benjamin-warner/index.html',
        '备注': '副教授；发展地理学、水资源治理与制度、中美洲发展、农业适应、气候变化适应、混合方法。方向与郭书睿的水资源治理+政治生态学+气候适应高度匹配，方法为混合（符合偏好）。需联系导师确认Fall 2027接收新生意愿及PhD supervision证据。',
    },
    {
        '导师': 'Marygold Walsh-Dilley',
        '学校_rid': 'rec7uiTsRfeCh',
        'Department': 'Department of Geography, University of New Mexico',
        'email': 'mwalshdi@unm.edu',
        '方向': 'Political ecology; food and agricultural systems; rural development; modernity and coloniality; agrarian change; climate change vulnerability; qualitative methods',
        '主页': 'https://geography.unm.edu/people/faculty/marygold-walsh-dilley/index.html',
        '申请': 'https://geography.unm.edu/graduate/phd-program/index.html',
        '档案': 'https://geography.unm.edu/people/faculty/marygold-walsh-dilley/index.html',
        '备注': '副教授；政治生态学、粮食与农业系统、农村发展、现代性与殖民性、农业变革、气候变化脆弱性、定性方法。研究区域为安第斯山脉。与郭书睿的政治生态学+农村发展方向高度匹配，定性方法（符合偏好）。需联系导师确认Fall 2027接收新生意愿。',
    },
    {
        '导师': 'Dean Hardy',
        '学校_rid': 'recizWDGgCF3g',
        'Department': 'School of the Earth, Ocean & Environment (SEOE) / Geography, University of South Carolina',
        'email': 'dhardy@sc.edu',
        '方向': 'Environmental justice; political ecology; climate change; sea level rise; flood risk; mixed methods',
        '主页': 'https://sc.edu/study/colleges_schools/artsandsciences/geography/our_people/our_people_directory/hardy_dean.php',
        '申请': 'https://sc.edu/study/colleges_schools/artsandsciences/geography/graduate/phd-in-geography',
        '档案': 'https://sc.edu/study/colleges_schools/artsandsciences/geography/our_people/our_people_directory/hardy_dean.php',
        '备注': '助理教授；环境正义、政治生态学、气候变化、海平面上升、洪水风险、混合方法（空间分析+访谈+参与式观察）。当前指导PhD学生Nelson Kowu（研究方向为社会环境系统与气候变化适应），方向与郭书睿高度匹配。2026年秋季有sabbatical，建议联系确认Fall 2027是否可接收新生。',
    },
    {
        '导师': 'Jessie Clark',
        '学校_rid': 'recvuGoqgMe3U',
        'Department': 'Department of Geography, University of Nevada Reno',
        'email': 'jessie.clark@unr.edu',
        '方向': 'Feminist geography; political geography; cultural geography; qualitative methods; Middle East',
        '主页': 'https://www.unr.edu/geography/people/jessie-clark',
        '申请': 'https://www.unr.edu/geography/graduate/phd',
        '档案': 'https://www.unr.edu/geography/people/faculty',
        '备注': '副教授、研究生项目主任；女性主义地理学、政治地理学、文化地理学、定性方法、中东地区。官方个人页明确写欢迎联系咨询指导机会，Grad Program Director身份说明参与博士项目运作。方向与郭书睿的定性方法方向高度匹配，中东地区为次要方向（学生可接受非洲）。需联系导师确认Fall 2027接收新生意愿。',
    },
    {
        '导师': 'Kate Berry',
        '学校_rid': 'recvuGoqgMe3U',
        'Department': 'Department of Geography, University of Nevada Reno',
        'email': 'kate.berry@unr.edu',
        '方向': 'Water governance; Indigenous geographies; cultural politics of water; environmental justice; legal geographies',
        '主页': 'https://www.unr.edu/geography/people/kate-berry',
        '申请': 'https://www.unr.edu/geography/graduate/phd',
        '档案': 'https://www.unr.edu/geography/people/faculty',
        '备注': '教授；水资源治理、原住民地理学、水资源文化政治、环境正义、法律地理学。方向与郭书睿的水资源治理+环境正义方向高度匹配。需联系导师确认Fall 2027接收新生意愿。',
    },
    {
        '导师': 'Nari Senanayake',
        '学校_rid': 'recqz6zyowgcP',
        'Department': 'Department of Geography, University of Kentucky',
        'email': 'nari.senanayake@uky.edu',
        '方向': 'Health-environment geography; political ecology; feminist geographies; agrarian livelihoods; South Asia',
        '主页': 'https://www.as.uky.edu/users/nse235',
        '申请': 'https://geography.as.uky.edu/graduate/phd',
        '档案': 'https://geography.as.uky.edu/people/faculty',
        '备注': '副教授；健康环境地理学、政治生态学、女性主义地理学、农业生计、南亚地区。Alumni记录显示指导2024 PhD（Nethmi Bathige：女性主义政治生态学+气候弹性农业+斯里兰卡）和2025 PhD（Aylin Castro：气候正义+环境正义）。Agrarian livelihoods是学生方向之一，但health-environment geography偏公共卫生方向，与学生硬排除线（公共健康/全球健康）有交叉，建议谨慎考虑。',
    },
    {
        '导师': 'Lauren Mullenbach',
        '学校_rid': 'rec4Sc3iY6VMm',
        'Department': 'Department of Geography and Environmental Sustainability, University of Oklahoma',
        'email': 'lauren.mullenbach@ou.edu',
        '方向': 'Urban environmental justice; climate adaptation planning; green space development; gentrification; wellbeing',
        '主页': 'https://www.ou.edu/mesonet/people/mullenbach',
        '申请': 'https://www.ou.edu/mesonet/graduate',
        '档案': 'https://www.ou.edu/mesonet/people/mullenbach',
        '备注': '助理教授；城市环境正义、气候适应规划、绿色空间发展、绅士化、福祉。方向与环境正义+气候适应匹配，但研究以城市为主（与郭书睿的农村生计/湄公河流域方向有差异）。需联系导师确认Fall 2027接收新生意愿及PhD supervision证据。',
    },
    {
        '导师': 'Gregory Simon',
        '学校_rid': 'recrlZYNooBrY',
        'Department': 'College of Architecture and Planning, University of Colorado Denver (Geography, Planning, and Design PhD)',
        'email': 'Gregory.Simon@ucdenver.edu',
        '方向': 'Human-environment interactions; political ecology; environmental policy and governance; critical hazards and disaster studies',
        '主页': 'https://clas.ucdenver.edu/people/faculty/g拗Simon',
        '申请': 'https://ucdenver.edu/planning/academics/phd',
        '档案': 'https://clas.ucdenver.edu/people/faculty/g拗Simon',
        '备注': '教授、研究生项目主任；人类环境互动、政治生态学、环境政策与治理、批判灾害研究。方向与郭书睿的环境治理+政治生态学方向高度匹配；Director of Graduate Studies身份说明参与博士项目运作。需联系导师确认Fall 2027接收新生意愿。',
    },
]

def build_record(c):
    return {
        'fields': {
            '导师': c['导师'],
            '学校名字': [c['学校_rid']],
            'Department': c['Department'],
            '导师联系方式': c['email'],
            '导师研究领域': c['方向'],
            '导师主页': {'url': c['主页'], 'text': c['导师']},
            '博士申请信息': {'url': c['申请'], 'text': 'PhD Program'},
            '其他导师信息': {'url': c['档案'], 'text': 'Faculty Page'},
            '备注': c['备注'],
        }
    }

# Process in batches of 10
BATCH_SIZE = 10
all_rids = []

for i in range(0, len(CANDIDATES), BATCH_SIZE):
    batch = CANDIDATES[i:i+BATCH_SIZE]
    records = [build_record(c) for c in batch]
    payload = {
        'records': records,
        'fieldKey': 'name'
    }
    print(f"\nWriting batch {i//BATCH_SIZE + 1}: {len(batch)} records ({[c['导师'] for c in batch]})")
    resp = vika('POST', f'/datasheets/{DT}/records', payload)
    if resp.get('code') == 200:
        created = resp['data']['records']
        print(f"  Created {len(created)} records")
        for rec in created:
            all_rids.append(rec['recordId'])
            print(f"    {rec['recordId']}: {rec['fields'].get('导师', '?')}")
    else:
        print(f"  ERROR: {resp}")
        sys.exit(1)
    if i + BATCH_SIZE < len(CANDIDATES):
        time.sleep(0.5)

print(f"\nTotal records created: {len(all_rids)}")
print("Record IDs:")
for rid in all_rids:
    print(f"  {rid}")

# Save record IDs to file
with open('/tmp/guosr_record_ids.json', 'w') as f:
    json.dump(all_rids, f)
print("\nRecord IDs saved to /tmp/guosr_record_ids.json")
