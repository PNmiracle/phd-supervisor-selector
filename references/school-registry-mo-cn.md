<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载 -->
> **本文含**：澳门各校 + 内地中外合办院校逐校情报（含合办校导师名单与语言门槛入口）。
> **什么时候读**：目标校在澳门或中外合办（UNNC / XJTLU / CUHK-SZ / BNBU-UIC / DKU / NYU Shanghai / HKUST-GZ）时，按校名 grep 定位。
> **什么时候不用读**：目标校不在该范围；⚠️ 禁止整读，必须先用校名定位。

> 本文由 `school-registry-hk-mo-cn.md` 于 2026-10-07 按地区拆分而来；总入口见 `school-strategies.md`，本地区入口见 `school-registry-hk-mo-cn.md`。
---

## 🇲🇴 Macau

#### University of Macau (UM)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: fss.um.edu.mo for Psychology
- **Key endpoint**: https://fss.um.edu.mo/
- **Failed**: —
- **Last verified**: 2026-06-26

#### Macau University of Science and Technology (MUST)
- **Architecture**: Cloudflare WAF
- **Layer**: L3
- **Access**: BLOCKED all automated attempts. No psychology department exists — psych coursework embedded in FHSS.
- **Key endpoint**: —
- **Failed**: curl → 403 (Cloudflare); browser blocked; Google Scholar shows engineering-only decision-making research; Chinese search yields no psych JDM faculty
- **Last verified**: 2026-06-26


## 🇨🇳 Sino-foreign Joint Programs

#### CUHK Shenzhen
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: hss.cuhk.edu.cn for Applied Psychology
- **Key endpoint**: https://hss.cuhk.edu.cn/en/taxonomy/term/21
- **Failed**: —
- **Last verified**: 2026-06-26

##### CUHK(SZ) 环境/双碳方向补充（2026-08-17 验证）
- 理工学院 SSE `sse.cuhk.edu.cn/faculty/{slug}`、公共政策学院 SPP `spp.cuhk.edu.cn/teacher/{id}`、人文社科学院 HSS `hss.cuhk.edu.cn/teacher/{id}`、数据科学学院 SDS `sds.cuhk.edu.cn/teacher/{id}` 均为可抓取静态页；个人网站走 `myweb.cuhk.edu.cn/{slug}`。
- 环境/能源/双碳/公共政策/空间数据相关院系：SSE（能源经济、智能电网）、SPP（能源政策、可持续转型）、HSS（计算可持续、城市学、地理空间分析）、SDS（时空统计）。
- 研究生院 `gs.cuhk.edu.cn/page/16/`（研究型专业列表）、申请 `pgapply.cuhk.edu.cn`。

#### NYU Shanghai
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: shanghai.nyu.edu for Psychology / Neural Science
- **Key endpoint**: https://shanghai.nyu.edu/academics/graduate/phd-programs
- **Failed**: —
- **Last verified**: 2026-06-26

#### HKUST(GZ)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: Hub structure; Society Hub has 4 thrusts (CNCC, FTEC, IPE, UGOD). No behavioral/cognitive science thrust. No Psychology dept.
- **Key endpoint**: https://soch.hkust-gz.edu.cn/
- **Failed**: No psychology/behavioral science thrust area; no relevant department
- **Last verified**: 2026-06-26

##### HKUST(GZ) IPE 学域补充（2026-08-05 验证）
- **IPE 学域教师列表（WordPress 可抓取）**: https://soch.hkust-gz.edu.cn/academics/ipe/faculty/ — 完整 26 人名单，含姓名/职称/邮箱/SPA 个人页链接
- **官方博士招生手册 PDF**: `soch.hkust-gz.edu.cn/wp-content/uploads/2026/04/PhD-in-Innovation-Policy-and-Entrepreneurship_CN-2026-27-Intake-*.pdf` — 权威在招导师名单，与 faculty 列表有出入，优先以此交叉验证
- **facultyprofiles.hkust-gz.edu.cn 全站 SPA**：`?id=X` 与 `/faculty-personal-page/NAME/slug` 两种格式均返回 1522B Loading 壳，WebFetch/curl 均无法确认内容 → 个人主页必须用替代来源
- **替代主页来源（已验证可抓取）**：
  - 官网人员页：`hkust-gz.edu.cn?p=6493/`（Ye Qi 格式）、`/people/slug/` 只覆盖高级管理人员（如 hui-xiong）
  - 个人网站：luoyec.github.io（Luoye Chen）、qianping-ren.com（Qianping Ren）、seonaparklab.github.io（Seona Park CARE lab）、coreyxu.com（Cloudflare 403 但内容可 WebFetch）、personal.hkust-gz.edu.cn/dxie（Danyang Xie）
  - HKUST 官方页：ppol.hkust.edu.hk/people/detail/（Corey Xu、Xun Wu）、aging.hkust.edu.hk（Corey Xu）
  - 前任机构官方页：dbaswiss.ceibs.edu/he_jinyu（Jinyu He，CEIBS）、sece.xmu.edu.my/（Kok Sin Woon，厦大马校兼职）
- **博士申请信息**: IPE 项目页 `pcc.hkust-gz.edu.cn/postgraduate/program-catalog/innovation-policy-and-entrepreneurship-5` + 申请系统 `fytgs.hkust-gz.edu.cn`（WebFetch 可渲染）
- **Last verified**: 2026-08-05

##### HKUST(GZ) 环境/双碳方向补充（2026-08-17 验证）
- 社会枢纽 CNCC/UGOD 教师列表页（WordPress 可抓取，含姓名/职称/邮箱 + facultyprofiles ?id）：
  - CNCC 碳中和与气候变化 `soch.hkust-gz.edu.cn/academics/cncc/faculty/`
  - UGOD 城市治理与设计 `soch.hkust-gz.edu.cn/academics/ugod/faculty/`
- 功能枢纽 SEE 教师页 `funh.hkust-gz.edu.cn/zh/academics/sustainable-energy-and-environment/faculty-members/` 为 SPA（正文 "Loading"），无法抓取名单；SEE 导师个人页可用 facultyprofiles `?id=X`（如郑君瑜 id=243）。
- **facultyprofiles ?id 交叉核对方法**：直接 WebSearch `"[导师名] facultyprofiles.hkust-gz.edu.cn"` 可拿到含真实姓名/职称/邮箱的搜索结果摘要，比抓 SPA 壳可靠；再与 WordPress 学域列表核对 id。
- 注意 UGOD 有同名双条目（Lingbo LIU id=737 与 id=740，仅 740 带邮箱），写表前核对 email 与 id 匹配。

##### 🎯 HKUST(GZ) 研究方向 JSON 接口——SPA 破解（2026-09-21 验证，优先级最高）
**这是目前拿到港科广研究方向原文最快、最权威的方法，应优先于上文的替代来源与 WebSearch。**

```bash
# slug = faculty-personal-page/<SLUG>/<slug> 的最后一段（如 season / ningningding / shuosun）
curl -s "https://facultyprofiles.hkust-gz.edu.cn/api/itdcms-rpc/profile/primary/<slug>"
# 返回 JSON：data.profile.enName（姓名）+ data.resumes[resumeType=RESEARCH_INTEREST].detail[].content（研究方向原文）
```
- 前端调用方式见 `/js/app.237189e1.js`（`getFacultyByPrimaryKey`）。SPA 空壳页 + 此接口 = 完整个人资料。
- **必须用 `data.profile.enName` 校验身份**：slug 命中失败时接口会返回一个 **150+ 条的聚合兜底列表**（内容是港科广全体研究方向的并集），看起来"有数据"但完全不属于本人。`enName` 为空 = 未命中，该 slug 作废。
- slug 取自 WordPress 学域列表页里的个人页链接末段；DSA 用 `dsa.hkust-gz.edu.cn/faculty/`，社会枢纽 FTEC/IPE/UGOD 用 `soch.hkust-gz.edu.cn/academics/<thrust>/faculty/`（后者的名单是 JS 渲染，抓不到链接，见下）。
- ⚠️ **`RESEARCH_INTEREST` 字段可能是陈旧数据，必须以 `overviews`（Biography）交叉校验**。实例：Sung Hun KIM 的结构化字段存的是"程序员生产力／挖掘软件仓库／静态分析"（他早年的软件工程方向），而同一接口的 Biography 写的是"recommendation systems, neural search (NLP), source code generation"（现任方向）。**两者冲突时以 Biography 为准，且不要只凭结构化字段下结论。**
- 另外可用 `/api/itdcms-rpc/profile/primary/<slug>` 的 `person`/`jobs` 等字段核对职称与所在学域。

##### 🎯 HKUST(GZ) 社会枢纽（FTEC/IPE/UGOD）师资名单 API（2026-09-21 验证）
WordPress 站点，师资名单由 `ThrustFacultyData.js` 动态拉取，页面本身抓不到姓名。直接用其 REST 接口：
```bash
curl -s "https://soch.hkust-gz.edu.cn/wp-json/university/v1/getOfficialThrustList?affiliatedUnits=SOCIHUB&departmentPkCode=<code>"
# FTEC 金融科技        = 10011A10000000000H2S
# IPE  创新创业与公共政策 = 10011A10000000000H2U
# UGOD 城市治理与设计    = 10011A10000000000H2Y
# CNCC 碳中和与气候变化  = 10011A100000000259HQ
```
返回 `CURRENT_FACULTY_ADVISORS`（当届在册师资）+ `ACTING_HEAD`，每条含 `enName`/`name`/`email`/`jobs[0].jobEnName`（职称）/`schoolName`（博士院校）/`majorEnName`（博士专业）/`website`，可据此区分 tenure-track / Adjunct / Professor of Practice。

##### 🇭🇰 七校博士项目 GMAT/GRE 要求（2026-09-22 逐项目官方页面复核，可直接引用）

**判定口径（务必区分）**：
- **免 G** = 官方写 not required / optional；**或材料清单里根本不出现 GMAT/GRE**；**或 GMAT 仅作英语能力可选替代**（TOEFL/IELTS/GMAT 三选一）。
- **要 G** = 官方明确要求提交，或列为必需。
- 「考了加分」≠「必需」；「可用来顶英语成绩」≠「要考」。这两种都判免 G，但要在备注里写清口径。

**逐校结论（本项目实测）**

| 学校 | 校级页（发问时直接给这一页） | 结论 |
|---|---|---|
| HKU | `gradsch.hku.hk/prospective_students/application/admission_requirement` | 免 G，**仅两处例外**：Faculty of Business and Economics 要 GMAT/GRE；Psychology 系非心理学本科者要 GRE Subject Test in Psychology |
| CUHK | `gs.cuhk.edu.hk/admissions/requirements` | 免 G。校级页里 GMAT 只出现在**英语能力测试**列表（`GMAT: Band 21 (Verbal)`），无全校统一 G 要求；商学院为项目专属要求 |
| HKUST | `fytgs.hkust.edu.hk/admissions/Admission-to-Hong-Kong-Campus/submitting-an-application/admission-requirements` | 免 G。官方 RPg 指引原文：`Required only if there is a program-specific requirement on public examination achievements e.g. GMAT, GRE ... In general, only research programs in the School of Business and Management require GMAT/GRE` |
| PolyU | `polyu.edu.hk/study/pg/research-postgraduate/2023/admission-requirements-rpg` | 免 G（统一页只有 General + English 两节）。⚠️ **但统一页不覆盖院系级要求**——理大商科项目页（如 `…/rpg/2027/mm`）硬性写 `Others GMAT Focus Edition/ GMAT/ GRE results are required.` |
| CityU | `cityu.edu.hk/pg/research-degree-programmes/entrance-requirements` | 免 G。**唯一提 G 的地方是 College of Business 条目**：`A high score in GRE or GMAT with supporting proof will be an added advantage though this is not a mandatory requirement. Please note that individual Departments in the College may adopt a higher standard.` ⚠️ 商学院 Management 系页面用词更强（`strongly encouraged to take the GMAT or GRE`），仍非必需 |
| HKUST(GZ) | `fytgs.hkust-gz.edu.cn/admissions/before-submitting-an-application/documents-required/` | 免 G。材料清单第 5 项：`Public Exam Score Reports — Required only if there is a Program-Specific Requirement on public examination achievements, e.g. GMAT, GRE`。四个学域（DSA/FTEC/IPE/UGOD）项目页入学要求都只有 General + English 两项 |
| CUHK(SZ) | `gs.cuhk.edu.cn/en/page/26` | 免 G（GMAT 仅作英语三选一）。**但经管学院例外，见下** |

**⚠️ 最关键的坑：港中大（深圳）经管学院 6 个 MPhil-PhD 里只有 Management 免 G**

用同一个模板，肉眼比对「最低入学要求」末尾有没有这一条：
```
- Taken the GRE General Test or GMAT.
```
以及材料清单里有没有这一项：
```
GRE or GMAT score report
```

| 项目 | page id | 有无 "Taken the GRE General Test or GMAT" + 材料含 G | 判定 |
|---|---|---|---|
| Management | 3255 | ❌ 都没有 | **免 G** |
| Economics | 1957 | ✅ 都有 | 要 G |
| Finance | 1958 | ✅ 都有 | 要 G |
| Accounting | 1959 | ✅ 都有 | 要 G |
| Marketing | 2098 | ✅ 都有 | 要 G |
| Information Management and Business Analytics | 2107 | ✅ 都有 | 要 G |

**新增发现：港中大（深圳）人文社科学院有 5 个 MPhil-PhD 项目，均免 G**
- 项目：Applied Psychology / Global Studies / Urban Studies / Computational Social Science / Sustainable Development（另 Translation Studies 已暂停招生）。
- 官方站是**独立子域** `hsspg.cuhk.edu.cn`（不是 `hss.cuhk.edu.cn`），项目页 URL 规律：`hsspg.cuhk.edu.cn/en/<slug>/{requirements,application,phdadvisor}`，slug 为 `mphilphdap` / `mphilphdgs` / `mphilphdcss` / `mphilphdus` / `mphilphdsd`。
- 入学要求页只有学位门槛 + 英语；英语测试列表含 `GMAT: Band 21 (Verbal)` 但**只作可选项**，全页 `GRE` 出现 0 次。→ 免 G。
- **`phdadvisor` 页是前端渲染**，curl 拿不到导师姓名，需用 WebSearch 或各教师个人页（`myweb.cuhk.edu.cn/<slug>`）反查所属学部。

**⚠️ 港中大（深圳）人文社科学院「学院首页 ≠ 项目页」的坑**：`hss.cuhk.edu.cn/en` 是学院首页，**完全没有入学信息**，也没有指向项目页的导航链接（导航只有 Division 层级）。写表时「博士申请信息」必须用 `hsspg.cuhk.edu.cn` 的项目页，不要用学院首页。

##### 🎯 港中大（深圳）经管学院 SME 师资 JSON:API（2026-09-21 验证，含按学术领域筛选）
SME 的师资检索页是 Drupal + JS 渲染，直接抓页面拿不到姓名，但 **JSON:API 全开**：
```bash
# 全部师资（分页，每页 50）
curl -s 'https://sme.cuhk.edu.cn/jsonapi/node/teacher?page%5Boffset%5D=0&page%5Blimit%5D=50'
# 按学术领域筛选（academic_type 的 drupal_internal__target_id）
curl -s 'https://sme.cuhk.edu.cn/jsonapi/node/teacher?filter%5Bacademic_type.meta.drupal_internal__target_id%5D=31'
```
- **领域 term id**（取自 `/en/teacher-search` 的 Academic Field 下拉）：Accounting=161、**Economics=32**、Finance=33、**Management=31**、Marketing=34、**Information Systems & Operations Management=216**
- 每条 `attributes` 里可直接用：`title`（中文名）、`school_post`（职称/职务）、`research_field`（研究方向原文）、`body.value`（简介）、`email`、`cuhk_website_link.uri`（`myweb.cuhk.edu.cn/<slug>` 个人站）、`path.alias`（`/teacher/<id>`）
- **注意**：`academic_field` / `research_field` 在 `attributes` 里可能为 null，领域归属在 `relationships.academic_type`；`supervisor` 字段指的是**博士后的合作导师**，不是博士指导资格，别误读。
- **教师页 `sme.cuhk.edu.cn/en/teacher/<id>` 是 JS 渲染**（HTML 里读不到研究领域）→ 写表时 `导师主页` 优先挂 `myweb.cuhk.edu.cn/<slug>` 个人站，研究领域在个人站可读可核。

##### 港中大（深圳）经管学院管理学方向的实测结论（2026-09-21）
- MPhil-PhD in **Management** 的 16 位官方师资（学术领域=Management）集中在**组织行为、战略管理、创新创业、人力资源管理**（企业社会责任、非市场化战略、组织吸引力、伦理决策…），与"数据科学/机器学习/数据挖掘/金融量化"几乎无交集；全学院唯一沾边的是做**计算社会科学**的潘歆乐。
- 因此遇到"学生想走港中深管理（因为免 G）"的需求时，**先把这份名单和方向结论给学生看**，再决定是否收录，不要为了填满免 G 口子而把战略/OB 师资整批写入。
- 参考：管理学博士课程为 Microeconomic Theory / Organizational Behavior / Strategic Management / Research Methods in Behavioral Studies & Strategic Management / Econometrics，本质是管理学实证训练。

##### 港中大（深圳）与港城大 研究方向提取要点（2026-09-21 验证）
- **CUHK-SZ SDS 教师页**（`sds.cuhk.edu.cn/en/teacher/<id>`）：结构固定为 `Education Background → Academic Area → Research Field → Personal Website`，**"Research Field" 字段就是研究方向原文**；用"取 Biography 之前一段"的方式提取最稳（先找 `Biography` 位置再回看前 700 字符）。
- **CUHK-SZ HSS 教师页**：用 `Research Fields` 字段；教师个人站 `myweb.cuhk.edu.cn/<slug>`（部分页面 1KB 左右，够读 Education Background 与 Research）。
- **CUHK STA/SOC 教师页**：内容块的字段名是单数 `Research Interest`；页面导航里也有 `Research Areas`，**优先匹配单数形式并取最后一次出现**，否则容易抓到导航菜单。
- **CUHK-SZ 教师中文名不都在官网出现**（如 LI Yujie 页面只有英文名）→ 核不到中文名时用官方英文名，不要自行猜写中文。
- **CityU**：`cb.cityu.edu.hk/dao/.../detail?eid=xxx` 的正文是 `{{{staffResearchAreas}}}` 模板占位符（JS 渲染），抓不到；改用 **CityU Scholars** `scholars.cityu.edu.hk/en/persons/<name-slug>`（含 `Research Interests/Areas` 字段，可 curl），slug 形如 `tze-kin-alan-wan`。营销/传播等系站也常返回 84B WAF 壳，需 WebFetch 穿透。

##### 对抗审核的已知误报模式（2026-09-21 记录）
- **把 WAF/SPA 拦截当死链**：`facultyprofiles.hkust-gz.edu.cn`（SPA 壳）、`web.socialwork.hku.hk` / `datascience.hku.hk` / `research.cuhk.edu.hk`（Cloudflare 403）、`saasweb.hku.hk`（curl 000）、`cityu.edu.hk/stfprofile`（Incapsula 壳）——这些在浏览器里都正常，**审核前必须把这份"已知不可穿透清单"连同穿透方式一起交给审核官**，否则会大量误报。
- **把渲染截断当"页面没有"**：审核官用 WebFetch 读到的 markdown 可能丢掉 JS 标签页里的内容（如港大社会学 ABEL 的 "I am happy to supervise doctoral students…" 实际在页面源码里）。判定"页面无此句"前，必须用 curl + grep 原文复核一次。

#### BNBU / UIC (北师香港浸会大学, Zhuhai)
- **Architecture**: Static HTML (general) + Vue SPA (FHSS comm department)
- **Layer**: L1 (general) / L3 (FHSS comm)
- **Access**: 9 PhD programs exist but none in psychology. Applied Psychology is undergraduate-only. FHSS Communication department faculty page is hash-routed SPA.
- **Key endpoint**: https://gs.uic.edu.cn/ (graduate school) / https://fhss.bnbu.edu.cn/comm_en/faculty/faculty.htm (comm faculty SPA)
- **Profile URL**: https://fhss.bnbu.edu.cn/comm_en/faculty/faculty.htm#/{username}/en (hash fragment, SPA-rendered)
- **Failed**: No psychology PhD program; behavioral decision research happens in math/stats depts but not a dedicated track; individual HTML pages don't exist for comm (all SPA hash-routed)
- **⚠️ PhD supervision**: UIC is primarily a teaching institution. MPhil/PhD offered through HKBU co-supervision. Assistant Professors may have limited supervision capacity.
- **Last verified**: 2026-07-01

##### BNBU/UIC 环境/数据方向补充（2026-08-17 验证）
- **研究型硕博专业仅 6 个**：计算机科学、概率论与数理统计、生物学、应用数学、传播学、会计学与企业管理（仅博士）。**无环境科学/公共政策独立专业**，环境方向需挂靠"生物学"（生命科学系），空间/统计方向挂靠"概率论与数理统计"。
- 研究生院导师名录页（静态 HTML，含姓名/职称/研究方向/邮箱，可抓取）：
  - `gs.bnbu.edu.cn/graduate/graduate1/yjxyjskc/Probability_and_Mathematical_Statistics.htm`（统计 PMS）
  - 类似 `.../Biology.htm`、`.../Computer_Science.htm` 等
- 教师个人页多为 SPA：`fst.bnbu.edu.cn/xxx/faculty/faculty.htm#/{username}/en`（hash 锚点，抓取只有导航栏）；`staff.uic.edu.cn/{username}/cn` 为旧域名遗留静态页（仍有效但内容为旧版）。写表时优先用 `gs.bnbu.edu.cn` 导师名录页，或 `staff.uic.edu.cn` 旧页 + 备注标注。
- 申请系统 `rpgadmission.bnbu.edu.cn`。

#### Duke Kunshan University
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: Masters-only institution; 5 Master's programs, zero PhD programs
- **Key endpoint**: https://dukekunshan.edu.cn/en/academics/graduate
- **Failed**: No PhD programs of any kind; Duke Durham has relevant programs but DKU does not
- **Last verified**: 2026-06-26

#### UNNC (Nottingham Ningbo)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: No Psychology dept. Business School (NUBS China) has ICBBR (behavioural business research centre).
- **Key endpoint**: https://www.nottingham.edu.cn/en/business/
- **PhD link**: NUBS China PhD available for behavioural economics/consumer behavior route
- **Failed**: No psychology-specific PhD; business school only
- **Last verified**: 2026-06-26

##### UNNC 环境/地理/ESG 方向补充（2026-08-17 验证）
- 理工科学院 FoSE 个人页格式：`nottingham.edu.cn/en/engineering/staffprofile/{slug}.aspx`、`nottingham.edu.cn/en/people/match.aspx?name={slug}`（均可抓取）。地理科学系、建筑与建筑环境系、化学与环境工程系在 FoSE 下。
- 研究门户（Pure，可抓取）：`research.nottingham.edu.cn/en/persons/{slug}`。
- NUBS China 个人页：`nottingham.edu.cn/en/Business/People/Profile.aspx?id={uuid}`。
- 博士申请：`nottingham.edu.cn/en/study-with-us/postgraduate-research/`；申请系统 `oaas.nottingham.edu.cn`。

##### UNNC 语言学/教育学方向补充（2026-09-01 验证，席天凌案例）
- **人文社科学院 → School of Education and English（教育与英语学院）教师列表**：`nottingham.edu.cn/en/humanities-and-social-sciences/education-and-english/people/listing.aspx`（静态 HTML，L1，可 curl；共 3 页，用 `?STFPageIndex=N` 翻页；第 3 页为 Teaching Fellow 教学岗）。
- **博士项目页**：`nottingham.edu.cn/en/course/PHD-FHSS-EES`（教育学/英语 PhD，研究方向含 Applied linguistics、SLA、Intercultural communication、World Englishes、TESOL、Multilingualism 等）。申请流程：先联系导师获同意再正式申请。
- 关键导师（2026-09 在任）：Anwei Feng（Chair Professor 多语教育，明确欢迎博士申请）、Douglas Bell（Prof ESP/EAP/TESOL）、Robert Weekly（AP World Englishes/语言政策）、Derek Irwin（Prof SFL/跨语言）、Dan Shi（AP SFL 英语教育）。
- **排除案例**：Yu Liu（SLA 但用眼动追踪/心理语言学方法 → 学生排除较强认知分析时不可用）；Curtis Green-Eneix（主页明确 "not accepting any new PhD students"）。

##### UNNC 商学院 + 理工科人机交互方向补充（2026-09-10 验证，蒋元萍案例 — 创业/AI/幸福感/人机交互方向）
- **NUBS China 全部学术教师一页表格（L1 静态，直接 curl 可解析 name→UUID）**：`nottingham.edu.cn/en/business/people/academic.aspx`（含三个系 EMM / FAE / IBM 的分组姓名+职称）。个人页统一为 `nottingham.edu.cn/en/Business/People/Profile.aspx?id={uuid}&language=en-GB`，curl 即返回 Pure 版完整简介（Research Interests + Personal profile + 邮箱），**无需浏览器**。
- **中文个人页**：把 `/en/` 换成 `/cn/`（`nottingham.edu.cn/cn/People/Profile.aspx?id={uuid}`）→ 拿到中文姓名与中文职称（英文页没有中文名）。
- **邮箱提取**：页面为防爬把 `@` 去掉，形如 `Email Haibo.Zhou nottingham.edu cn` → 正则还原为 `@nottingham.edu.cn`。另有 `/en/people/{slug}` 形式的短链（如 `/en/people/alain-chong`、`/en/people/lin-huang`）。
- **博士申请页（商学院）**：`nottingham.edu.cn/en/business/programmes/phd-programme/phd-programme.aspx`（同目录下另有 `application-details.aspx` / `supervisors.aspx` / `programme-structure.aspx`）。要点：3 年制；**必须先联系导师并取得同意再申请**；IELTS 6.5(min 6.0)、TOEFL 87；中国本科均分 78–83；有全奖（cover 学费+保险+住宿+生活费）；NUBS 要求 9 月入学；入学前有导师+RKE 委员会面试。
- **理工科学院（FoSE）个人页**：`nottingham.edu.cn/en/science-engineering/staffprofile/{slug}.aspx`（如 `xu-sun-.aspx`）或 `nottingham.edu.cn/en/info-hub/staff-profile.aspx?id={uuid}`。院系列表：`.../department/cs/people.aspx`、`.../department/mmme/people.aspx` 等（静态可解析）。
- **UNNC 研究生（PhD）总入口**：`nottingham.edu.cn/en/study-with-us/postgraduate-research/home.aspx`（FoSE 等非商学院导师的「博士申请信息」用它，不要误填成商学院的 PhD 页）。
- **⚠️ research.nottingham.edu.cn（Pure 门户）全站 Cloudflare Turnstile 验证码**，curl/WebFetch 均被拦（返回 ~1.4KB 挑战页）；但上面的 `www.nottingham.edu.cn/.../Profile.aspx?id=` 路径不设验证，可替代使用。
- **⚠️ 职称陷阱**：UNNC 部分教师职称带 `(T&L)`（Teaching & Learning 教学轨，如 Xuan Feng、Feranita）——教学轨科研产出通常很少，**不宜作为博士生第一导师**，写入前须核对主页职称尾部标记。
- **⚠️ 方向陷阱**：`理工科学院 = 只做工程不做行为实验` 是错误概括。FoSE 的计算机系与机械材料制造工程系**设有人机交互团队**（Boon Giin Lee 任 HCI Lab 副主任、主页明示持续招博士生；孙煦 Xu Sun 为拉夫堡大学人机交互博士、正指导 10 位博士生含 9 位第一导师），做 HCI / Human-AI Interaction / 情感与认知计算 / 人因。凡 RP 涉及人机交互、人因、用户实验者，必须扫 FoSE 这两系。
- **Last verified**: 2026-09-10

#### XJTLU (Xi'an Jiaotong-Liverpool)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: No Psychology dept in HSS (only China Studies, International Studies, Media, Linguistics). IBSS offers PhD in Business.
- **Key endpoint**: https://www.xjtlu.edu.cn/en/academics/schools/ibss
- **Failed**: No psychology department; IBSS business PhD only
- **Last verified**: 2026-06-26

##### XJTLU 环境/城市规划/ESG 方向补充（2026-08-17 验证）
- **研究门户（Pure，全校教师统一入口，可抓取，含研究方向/邮箱）**：`scholar.xjtlu.edu.cn/en/persons/{slug或uuid}`。这是写 XJTLU 导师主页的首选来源。
- 相关院系：理学院健康与环境科学系 HES（大气/温室气体/全球变化）、设计学院城市规划与设计系 UPD（GIS/可持续城市）、IBSS（ESG/供应链/气候计量经济）、人文社科学院中国研究/国际研究（气候政策）。
- 博士申请：`xjtlu.edu.cn/en/admissions/doctoral/how-to-apply`（全年开放，学费9.9万/年）。博士专业含环境科学、商学、城市规划与设计等。

##### XJTLU 语言学/教育学方向补充（2026-09-01 验证，席天凌案例）
- **应用语言学系（Department of Applied Linguistics）中文教研人员列表**：`xjtlu.edu.cn/zh/study/departments/academic-departments/department-of-applied-linguistics/department-staff/academic-staff`（含姓名/职称/研究方向/邮箱，可直接抓取）。⚠️ 英文版同路径为 SPA 壳（只有 "Academic Staff" 标题），用中文版。
- **Pure slug 大小写敏感**：`scholar.xjtlu.edu.cn/en/persons/RiningWei/`、`/BinZou`、`/HongLiu/`、`/TanjunLiu`、`/stevejeaco`、`/zhoulinruan` 均有效；猜测 `binzou`/`hongliu` 小写会 404。
- **博士项目**：`xjtlu.edu.cn/en/study/doctoral/english-culture-and-communication`（PhD English, Culture and Communication，含 applied linguistics、language pedagogy、TESOL、SLA；学位由 University of Liverpool 授予）；另有 `xjtlu.edu.cn/en/study/doctoral/phd-in-education`（PhD Education，由 Academy of Future Education 提供，偏教育管理/教育技术）。
- 关键导师（2026-09 在任）：Rining Wei（副教授，双语教育/TESOL，明确博导+MA TESOL 主任）、Bin Zou（教授，AI语言教学/CALL）、Zhoulin Ruan（教授，SLA/学术写作，⚠️现任副校长，行政岗风险）、Stephen Jeaco（高级副教授 EAP/TESOL/语料库）、Hong Liu（副教授，双语/语码转换，社会+认知双维度）、Tanjun Liu（副教授，语料库，明确欢迎语料库博士）。
- **排除案例**：Darcy Sperlich（心理语言学/形式语言学，主页明确不指导 general language learning and teaching）；Dawei Wei（语言习得+心理语言学 → 学生排除较强认知分析时不可用）；Esther Pascual（语言与认知）。
