#!/usr/bin/env python3
"""
杨子怡 Finance PhD 选导 - 第三批导师写入
包含: Syracuse (8条), Buffalo (10条), South Carolina (14条)
每条记录包含导师名、主页、邮箱、研究方向、备注（职称+研究方向）
"""
import os, urllib.request, json, ssl

TOKEN = os.environ.get('VIKA_TOKEN', '')
DS_ID = 'dstTaEDF3fNsdzd6zv'
BASE = 'https://api.vika.cn/fusion/v1'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

def app_obj(url):
    return {'title': url, 'text': url, 'favicon': ''}

def api(method, path, body=None):
    url = f'{BASE}{path}'
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method, headers=HEADERS)
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.loads(r.read())

def post_single(record):
    return api('POST', f'/datasheets/{DS_ID}/records', {'records': [record]})

def post_records(records):
    return api('POST', f'/datasheets/{DS_ID}/records', {'records': records})

# ─── Syracuse University Whitman (8 tenure-track faculty) ───────────────────
# 筛选标准: Assistant Professor / Associate Professor / Full Professor (排除 Practice/Clinical/Emeritus)
# Finance PhD: STEM, 本科可申, Dec 1-Jan 15 deadline, 2027 Fall 确认招生
syracuse_faculty = [
    {
        '导师': 'David Weinbaum',
        '备注': 'Professor; 实证资产定价、衍生品定价（PhD level授课教师）',
        '导师主页': app_obj('https://whitman.syracuse.edu/faculty-and-research/faculty-staff-directory/details/dweinbau'),
        '导师联系方式': 'dweinbau@syr.edu',
        '导师研究领域': '实证资产定价、衍生品定价、期权交易、波动率风险',
        '其他导师信息': app_obj('https://whitman.syr.edu/academic-areas/finance/finance-faculty'),
        '博士申请信息': app_obj('https://whitman.syr.edu/graduate/phd-programs/finance-and-managerial-statistics/'),
        'Department': 'Finance, Whitman School of Management, Syracuse University',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Amber Anand',
        '备注': 'Edward Pettinella Professor (Full Professor); 实证资产定价、衍生品与风险管理',
        '导师主页': app_obj('https://whitman.syracuse.edu/faculty-and-research/faculty-staff-directory/details/amanand'),
        '导师联系方式': 'amanand@syr.edu',
        '导师研究领域': '实证资产定价、衍生品与风险管理',
        '其他导师信息': app_obj('https://whitman.syr.edu/academic-areas/finance/finance-faculty'),
        '博士申请信息': app_obj('https://whitman.syr.edu/graduate/phd-programs/finance-and-managerial-statistics/'),
        'Department': 'Finance, Whitman School of Management, Syracuse University',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Si Cheng',
        '备注': 'Associate Professor; 主动基金管理与 ESG、因子模型、机器学习应用',
        '导师主页': app_obj('https://whitman.syracuse.edu/faculty-and-research/faculty-staff-directory/details/scheng24'),
        '导师联系方式': 'scheng24@syr.edu',
        '导师研究领域': '主动基金管理与 ESG、因子模型、机器学习、资产定价',
        '其他导师信息': app_obj('https://whitman.syr.edu/academic-areas/finance/finance-faculty'),
        '博士申请信息': app_obj('https://whitman.syr.edu/graduate/phd-programs/finance-and-managerial-statistics/'),
        'Department': 'Finance, Whitman School of Management, Syracuse University',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Erasmo Giambona',
        '备注': 'Professor (Falcone Chair in Real Estate Finance); 房地产金融、合同可执行性、董事会多元化',
        '导师主页': app_obj('https://whitman.syracuse.edu/faculty-and-research/faculty-staff-directory/details/egiambon'),
        '导师联系方式': 'egiambon@syr.edu',
        '导师研究领域': '房地产金融、对冲与合同可执行性、董事会性别多元化、供应链风险管理',
        '其他导师信息': app_obj('https://whitman.syr.edu/academic-areas/finance/finance-faculty'),
        '博士申请信息': app_obj('https://whitman.syr.edu/graduate/phd-programs/finance-and-managerial-statistics/'),
        'Department': 'Finance, Whitman School of Management, Syracuse University',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Candace Jens',
        '备注': 'Assistant Professor; 信用周期、企业投资、因果推断、预防性储蓄',
        '导师主页': app_obj('https://whitman.syracuse.edu/faculty-and-research/faculty-staff-directory/details/cejens'),
        '导师联系方式': 'cejens@syr.edu',
        '导师研究领域': '信用周期、预期与企业投资、因果推断、预防性储蓄与投资',
        '其他导师信息': app_obj('https://whitman.syr.edu/academic-areas/finance/finance-faculty'),
        '博士申请信息': app_obj('https://whitman.syr.edu/graduate/phd-programs/finance-and-managerial-statistics/'),
        'Department': 'Finance, Whitman School of Management, Syracuse University',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Yu Shan',
        '备注': 'Assistant Professor; 银行与金融中介、FinTech、消费金融、社会网络',
        '导师主页': app_obj('https://whitman.syr.edu/faculty-and-research/faculty-staff-directory/details/yshan03'),
        '导师联系方式': 'yshan03@syr.edu',
        '导师研究领域': '银行与金融中介、FinTech、消费金融、社会网络、系统性风险',
        '其他导师信息': app_obj('https://whitman.syr.edu/academic-areas/finance/finance-faculty'),
        '博士申请信息': app_obj('https://whitman.syr.edu/graduate/phd-programs/finance-and-managerial-statistics/'),
        'Department': 'Finance, Whitman School of Management, Syracuse University',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Ravi Shukla',
        '备注': 'Associate Professor; 金融（市场微观结构方向）',
        '导师主页': app_obj('https://whitman.syr.edu/faculty-and-research/faculty-staff-directory/details/rkshukla'),
        '导师联系方式': 'rkshukla@syr.edu',
        '导师研究领域': '金融、市场微观结构',
        '其他导师信息': app_obj('https://whitman.syr.edu/academic-areas/finance/finance-faculty'),
        '博士申请信息': app_obj('https://whitman.syr.edu/graduate/phd-programs/finance-and-managerial-statistics/'),
        'Department': 'Finance, Whitman School of Management, Syracuse University',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Lai Xu',
        '备注': 'Associate Professor; 金融（研究方向待确认）',
        '导师主页': app_obj('https://whitman.syr.edu/faculty-and-research/faculty-staff-directory/details/lxu100'),
        '导师联系方式': 'lxu100@syr.edu',
        '导师研究领域': '金融',
        '其他导师信息': app_obj('https://whitman.syr.edu/academic-areas/finance/finance-faculty'),
        '博士申请信息': app_obj('https://whitman.syr.edu/graduate/phd-programs/finance-and-managerial-statistics/'),
        'Department': 'Finance, Whitman School of Management, Syracuse University',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
]

# ─── University at Buffalo (10 tenure-track faculty) ────────────────────────
# 筛选标准: tenure-track 教授（Assistant Professor / Associate Professor / Full Professor）
# Management PhD Finance Track: STEM, 72 credits beyond bachelor's, 本科直博符合
buffalo_faculty = [
    {
        '导师': 'Isaac Ehrlich',
        '备注': 'SUNY Distinguished Professor; 法律经济学、人力资本、健康经济学、金融市场',
        '导师主页': app_obj('https://management.buffalo.edu/faculty/academic-departments/finance/faculty/isaac-ehrlich.html'),
        '导师联系方式': 'ieh@buffalo.edu',
        '导师研究领域': '法律经济学、人力资本、健康经济学、金融市场、社会保障',
        '其他导师信息': app_obj('https://mgt.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        '博士申请信息': app_obj('https://management.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        'Department': 'Finance, School of Management, University at Buffalo',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Kee Chung',
        '备注': 'Louis M. Jacobs Professor (曾任系主任); 市场微观结构、公司治理、金融市场',
        '导师主页': app_obj('https://management.buffalo.edu/faculty/academic-departments/finance/faculty/kee-chung.html'),
        '导师联系方式': 'khchung@buffalo.edu',
        '导师研究领域': '市场微观结构、公司治理、金融市场',
        '其他导师信息': app_obj('https://mgt.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        '博士申请信息': app_obj('https://management.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        'Department': 'Finance, School of Management, University at Buffalo',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Veljko Fotak',
        '备注': 'Associate Professor; 主权财富基金、政府所有权、跨境资本流动',
        '导师主页': app_obj('https://management.buffalo.edu/faculty/academic-departments/finance/faculty/veljko-fotak.html'),
        '导师联系方式': 'vfotak@buffalo.edu',
        '导师研究领域': '主权财富基金、政府所有权、跨境资本流动、政府干预与市场',
        '其他导师信息': app_obj('https://mgt.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        '博士申请信息': app_obj('https://management.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        'Department': 'Finance, School of Management, University at Buffalo',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Sahn-Wook Huh',
        '备注': 'Associate Professor; 资产定价、市场微观结构、实证公司金融、外汇',
        '导师主页': app_obj('https://management.buffalo.edu/faculty/academic-departments/finance/faculty/sahn-wook-huh.html'),
        '导师联系方式': 'shuh@buffalo.edu',
        '导师研究领域': '资产定价、市场微观结构、实证公司金融、外汇经济学、行为金融',
        '其他导师信息': app_obj('https://mgt.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        '博士申请信息': app_obj('https://management.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        'Department': 'Finance, School of Management, University at Buffalo',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Feng Jiang',
        '备注': 'Associate Professor; 高管薪酬、并购、公司治理、网络经济学',
        '导师主页': app_obj('https://management.buffalo.edu/faculty/academic-departments/finance/faculty/feng-jack-jiang.html'),
        '导师联系方式': 'fjiang6@buffalo.edu',
        '导师研究领域': '高管薪酬、并购、公司治理、网络经济学、行为金融',
        '其他导师信息': app_obj('https://mgt.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        '博士申请信息': app_obj('https://management.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        'Department': 'Finance, School of Management, University at Buffalo',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Scott Laing',
        '备注': 'Assistant Professor; 资产定价（研究方向待确认）',
        '导师主页': app_obj('https://management.buffalo.edu/faculty/academic-departments/finance/faculty/scott-laing.html'),
        '导师联系方式': 'sl4@buffalo.edu',
        '导师研究领域': '资产定价',
        '其他导师信息': app_obj('https://mgt.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        '博士申请信息': app_obj('https://management.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        'Department': 'Finance, School of Management, University at Buffalo',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Luca Xianran Lin',
        '备注': 'Assistant Professor; 公司金融（研究方向待确认）',
        '导师主页': app_obj('https://management.buffalo.edu/faculty/academic-departments/finance/faculty/luca-xianran-lin.html'),
        '导师联系方式': 'lxianranlin@buffalo.edu',
        '导师研究领域': '公司金融',
        '其他导师信息': app_obj('https://mgt.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        '博士申请信息': app_obj('https://management.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        'Department': 'Finance, School of Management, University at Buffalo',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Dominik Roesch',
        '备注': 'Associate Professor; 资产定价、公司金融（研究方向待确认）',
        '导师主页': app_obj('https://management.buffalo.edu/faculty/academic-departments/finance/faculty/dominik-roesch.html'),
        '导师联系方式': 'droesch@buffalo.edu',
        '导师研究领域': '资产定价、公司金融',
        '其他导师信息': app_obj('https://mgt.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        '博士申请信息': app_obj('https://management.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        'Department': 'Finance, School of Management, University at Buffalo',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Artem Streltsov',
        '备注': 'Assistant Professor; 公司金融（研究方向待确认）',
        '导师主页': app_obj('https://management.buffalo.edu/faculty/academic-departments/finance/faculty/artem-streltsov.html'),
        '导师联系方式': 'astrelts@buffalo.edu',
        '导师研究领域': '公司金融',
        '其他导师信息': app_obj('https://mgt.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        '博士申请信息': app_obj('https://management.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        'Department': 'Finance, School of Management, University at Buffalo',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Cristian Tiu',
        '备注': 'Associate Professor; 资产配置、风险管理（研究方向待确认）',
        '导师主页': app_obj('https://management.buffalo.edu/faculty/academic-departments/finance/faculty/cristian-tiu.html'),
        '导师联系方式': 'ctiu@buffalo.edu',
        '导师研究领域': '资产配置、风险管理',
        '其他导师信息': app_obj('https://mgt.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        '博士申请信息': app_obj('https://management.buffalo.edu/degree-programs/phd-in-management/program/finance.html'),
        'Department': 'Finance, School of Management, University at Buffalo',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
]

# ─── University of South Carolina (14 tenure-track faculty) ──────────────────
# 筛选标准: tenure-track 教授（Assistant Professor / Associate Professor / Full Professor）
# Finance PhD: 2027 Fall 确认招生，隔年偶数年，本科可申
sc_faculty = [
    {
        '导师': 'Allen N. Berger',
        '备注': 'Carolina Distinguished Professor; 金融机构、信贷市场、金融中介',
        '导师主页': app_obj('https://sc.edu/study/colleges_schools/moore/directory/berger_allen.php'),
        '导师联系方式': 'aberger@moore.sc.edu',
        '导师研究领域': '金融机构、信贷市场、金融中介、小额信贷',
        '其他导师信息': app_obj('https://sc.edu/study/colleges_schools/moore/study/finance/our_people'),
        '博士申请信息': app_obj('https://www.sc.edu/study/colleges_schools/moore/study/phd_programs/admission_requirements/'),
        'Department': 'Finance, Darla Moore School of Business, University of South Carolina',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Wendi Du',
        '备注': 'Assistant Professor; FinTech、创新、AI在金融中的应用',
        '导师主页': app_obj('https://sc.edu/study/colleges_schools/moore/directory/du_wendi.php'),
        '导师联系方式': 'wendi.du@moore.sc.edu',
        '导师研究领域': 'FinTech、创新、AI在自然语言处理中的应用、可持续金融',
        '其他导师信息': app_obj('https://sc.edu/study/colleges_schools/moore/study/finance/our_people'),
        '博士申请信息': app_obj('https://www.sc.edu/study/colleges_schools/moore/study/phd_programs/admission_requirements/'),
        'Department': 'Finance, Darla Moore School of Business, University of South Carolina',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Ai He',
        '备注': 'Assistant Professor; 金融（研究方向待确认）',
        '导师主页': app_obj('https://sc.edu/study/colleges_schools/moore/directory/he_ai.php'),
        '导师联系方式': 'ai.he@moore.sc.edu',
        '导师研究领域': '金融',
        '其他导师信息': app_obj('https://sc.edu/study/colleges_schools/moore/study/finance/our_people'),
        '博士申请信息': app_obj('https://www.sc.edu/study/colleges_schools/moore/study/phd_programs/admission_requirements/'),
        'Department': 'Finance, Darla Moore School of Business, University of South Carolina',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Chao Jiang',
        '备注': 'Associate Professor; 实证资产定价、内幕交易、行为金融',
        '导师主页': app_obj('https://sc.edu/study/colleges_schools/moore/directory/jiang_chao.php'),
        '导师联系方式': 'chao.jiang@moore.sc.edu',
        '导师研究领域': '实证资产定价、内幕交易、行为金融、公司金融',
        '其他导师信息': app_obj('https://sc.edu/study/colleges_schools/moore/study/finance/our_people'),
        '博士申请信息': app_obj('https://www.sc.edu/study/colleges_schools/moore/study/phd_programs/admission_requirements/'),
        'Department': 'Finance, Darla Moore School of Business, University of South Carolina',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Da Ke',
        '备注': 'Associate Professor; 投资、家庭金融、行为金融',
        '导师主页': app_obj('https://sc.edu/study/colleges_schools/moore/directory/ke_da.php'),
        '导师联系方式': 'da.ke@moore.sc.edu',
        '导师研究领域': '投资、家庭金融、行为金融',
        '其他导师信息': app_obj('https://sc.edu/study/colleges_schools/moore/study/finance/our_people'),
        '博士申请信息': app_obj('https://www.sc.edu/study/colleges_schools/moore/study/phd_programs/admission_requirements/'),
        'Department': 'Finance, Darla Moore School of Business, University of South Carolina',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Hugh Hoikwang Kim',
        '备注': 'Associate Professor; 资产定价、投资者行为、生命周期投资组合选择',
        '导师主页': app_obj('https://sc.edu/study/colleges_schools/moore/directory/kim_hugh.php'),
        '导师联系方式': 'hugh.kim@moore.sc.edu',
        '导师研究领域': '资产定价、投资者行为、生命周期投资组合选择、金融机构',
        '其他导师信息': app_obj('https://sc.edu/study/colleges_schools/moore/study/finance/our_people'),
        '博士申请信息': app_obj('https://www.sc.edu/study/colleges_schools/moore/study/phd_programs/admission_requirements/'),
        'Department': 'Finance, Darla Moore School of Business, University of South Carolina',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Dongmei Li',
        '备注': 'Moore Term Professorship; 投资、创新',
        '导师主页': app_obj('https://sc.edu/study/colleges_schools/moore/directory/li_dongmei.php'),
        '导师联系方式': 'dongmei.li@moore.sc.edu',
        '导师研究领域': '投资、创新',
        '其他导师信息': app_obj('https://sc.edu/study/colleges_schools/moore/study/finance/our_people'),
        '博士申请信息': app_obj('https://www.sc.edu/study/colleges_schools/moore/study/phd_programs/admission_requirements/'),
        'Department': 'Finance, Darla Moore School of Business, University of South Carolina',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Aaron Mora',
        '备注': 'Assistant Professor; 资产定价、计量经济学、机器学习、产业组织',
        '导师主页': app_obj('https://sc.edu/study/colleges_schools/moore/directory/mora_aaron.php'),
        '导师联系方式': 'aaron.mora@moore.sc.edu',
        '导师研究领域': '资产定价、计量经济学、机器学习、产业组织',
        '其他导师信息': app_obj('https://sc.edu/study/colleges_schools/moore/study/finance/our_people'),
        '博士申请信息': app_obj('https://www.sc.edu/study/colleges_schools/moore/study/phd_programs/admission_requirements/'),
        'Department': 'Finance, Darla Moore School of Business, University of South Carolina',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Gregory R. Niehaus',
        '备注': 'Professor (Interim Dean); 保险经济学、公司养老金、公司金融',
        '导师主页': app_obj('https://sc.edu/study/colleges_schools/moore/directory/niehaus_gregory.php'),
        '导师联系方式': 'gregn@moore.sc.edu',
        '导师研究领域': '保险经济学、公司养老金、公司金融',
        '其他导师信息': app_obj('https://sc.edu/study/colleges_schools/moore/study/finance/our_people'),
        '博士申请信息': app_obj('https://www.sc.edu/study/colleges_schools/moore/study/phd_programs/admission_requirements/'),
        'Department': 'Finance, Darla Moore School of Business, University of South Carolina',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Eric A. Powers',
        '备注': 'Associate Professor (Chair); 公司金融、固定收益证券',
        '导师主页': app_obj('https://sc.edu/study/colleges_schools/moore/directory/powers_eric.php'),
        '导师联系方式': 'epowers@moore.sc.edu',
        '导师研究领域': '公司金融、固定收益证券',
        '其他导师信息': app_obj('https://sc.edu/study/colleges_schools/moore/study/finance/our_people'),
        '博士申请信息': app_obj('https://www.sc.edu/study/colleges_schools/moore/study/phd_programs/admission_requirements/'),
        'Department': 'Finance, Darla Moore School of Business, University of South Carolina',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Madeline Marco Scanlon',
        '备注': 'Assistant Professor; 实证公司金融、政治经济学、劳动经济学',
        '导师主页': app_obj('https://sc.edu/study/colleges_schools/moore/directory/scanlon_madeline.php'),
        '导师联系方式': 'madeline.scanlon@moore.sc.edu',
        '导师研究领域': '实证公司金融、政治经济学、劳动经济学',
        '其他导师信息': app_obj('https://sc.edu/study/colleges_schools/moore/study/finance/our_people'),
        '博士申请信息': app_obj('https://www.sc.edu/study/colleges_schools/moore/study/phd_programs/admission_requirements/'),
        'Department': 'Finance, Darla Moore School of Business, University of South Carolina',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Matthew Souther',
        '备注': 'Associate Professor; 公司金融（研究方向待确认）',
        '导师主页': app_obj('https://sc.edu/study/colleges_schools/moore/directory/souther_matthew.php'),
        '导师联系方式': 'matthew.souther@moore.sc.edu',
        '导师研究领域': '公司金融',
        '其他导师信息': app_obj('https://sc.edu/study/colleges_schools/moore/study/finance/our_people'),
        '博士申请信息': app_obj('https://www.sc.edu/study/colleges_schools/moore/study/phd_programs/admission_requirements/'),
        'Department': 'Finance, Darla Moore School of Business, University of South Carolina',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Sergey Tsyplakov',
        '备注': 'Associate Professor; 公司金融、实物期权、计算金融',
        '导师主页': app_obj('https://sc.edu/study/colleges_schools/moore/directory/tsyplakov_sergey.php'),
        '导师联系方式': 'sergey@moore.sc.edu',
        '导师研究领域': '公司金融、实物期权、计算金融',
        '其他导师信息': app_obj('https://sc.edu/study/colleges_schools/moore/study/finance/our_people'),
        '博士申请信息': app_obj('https://www.sc.edu/study/colleges_schools/moore/study/phd_programs/admission_requirements/'),
        'Department': 'Finance, Darla Moore School of Business, University of South Carolina',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
    {
        '导师': 'Donghang Zhang',
        '备注': 'W.W. "Hootie" Johnson Endowed Chair (Professor); IPO、公司金融、市场微观结构',
        '导师主页': app_obj('https://sc.edu/study/colleges_schools/moore/directory/zhang_donghang.php'),
        '导师联系方式': 'zhang@moore.sc.edu',
        '导师研究领域': 'IPO、公司金融、市场微观结构',
        '其他导师信息': app_obj('https://sc.edu/study/colleges_schools/moore/study/finance/our_people'),
        '博士申请信息': app_obj('https://www.sc.edu/study/colleges_schools/moore/study/phd_programs/admission_requirements/'),
        'Department': 'Finance, Darla Moore School of Business, University of South Carolina',
        '非美国地区学校': ['recM2cm7uJC6i'],
    },
]

all_records = syracuse_faculty + buffalo_faculty + sc_faculty
print(f'总计写入 {len(all_records)} 条记录 (Syracuse {len(syracuse_faculty)} + Buffalo {len(buffalo_faculty)} + SC {len(sc_faculty)})')

# 分批 POST（每批 20 条）
batch_size = 20
total_success = 0
total_failed = 0
all_new_rids = []

for i in range(0, len(all_records), batch_size):
    batch = all_records[i:i+batch_size]
    batch_ok = 0
    batch_fail = 0
    for rec in batch:
        try:
            resp = post_single(rec)
            records = resp.get('data', {}).get('records', [])
            r = records[0] if records else {}
            rid = r.get('recordId')
            name = r.get('fields', {}).get('导师', '(unknown)')
            if r.get('createdAt'):
                print(f'  ✅ {rid} → {name}')
                all_new_rids.append(rid)
                batch_ok += 1
            else:
                code = r.get('code')
                msg = r.get('message', '')
                print(f'  ❌ {name}: [{code}] {msg}')
                batch_fail += 1
        except Exception as ex:
            print(f'  ❌ ERROR: {ex}')
            batch_fail += 1
    total_success += batch_ok
    total_failed += batch_fail
    print(f'  Batch {i//batch_size+1}: {batch_ok}/{len(batch)} success')

print(f'\n总计: {total_success}/{len(all_records)} 成功, {total_failed} 失败')
print(f'新记录ID: {all_new_rids}')
