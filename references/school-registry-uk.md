<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：英国院校逐校情报，含 UCL profiles JSON 接口与 403 反爬绕法、The Bartlett 院系速查
> **什么时候读**：目标校在英国时，按校名 grep 定位
> **什么时候不用读**：目标校不在英国；⚠️ 禁止整读，必须先用校名定位

---

# Registry: uk

> 本文档由 `school-strategies.md` 于 2026-10-07 拆分而来；入口请见 `school-strategies.md`。

## 🇬🇧 United Kingdom

#### University of the Arts London (UAL)
- **Architecture**: Pure Portal (JS-rendered)
- **Layer**: L2
- **Best method**: L3 — Google `site:researchers.arts.ac.uk "{name}"` → click first result in browser. Profile URL format: `researchers.arts.ac.uk/{id}-{slug}`.
- **Key endpoint**: Profile URLs use format `https://researchers.arts.ac.uk/{numeric-id}-{slug}` (NOT `/en/persons/{slug}`)
- **Failed**: `?format=json` does NOT work on UAL Pure; `/en/persons/{slug}` returns 404; `curl` alone cannot extract data
- **Last verified**: 2026-06-26

#### King's College London (KCL)
- **Architecture**: 双站并存 —— 官网 `www.kcl.ac.uk`（静态 HTML，curl 可抓）+ 研究门户 `kclpure.kcl.ac.uk`（Pure Portal，**JS 壳，curl 只拿到 ~6KB 空壳，必须用 WebFetch**）
- **Layer**: L1（官网个人页）/ L2（Pure）
- **Best method**:
  1. 按院系穷举教职员：`https://www.kcl.ac.uk/<dept>/about/people`（cmci / english / ecs / ghsm / ddh / music 等，支持 `?page=N`），页面直接给出「姓名 + 职称 + `/people/<slug>` 链接」三件套，是**最优入口**
  2. Pure 按机构列人（WebFetch）：`https://kclpure.kcl.ac.uk/portal/en/organisations/<slug>/persons/`（slug 如 `culture-media-creative-industries`、`digital-humanities`、`film-studies`），可翻页穷举，且标注 Person: Academic / Emeritus / Research，便于批量排除
  3. 个人页：`https://www.kcl.ac.uk/people/<slug>`
- **Key facts / pitfalls**:
  - **KCL 没有独立的舞蹈院系**，也没有专职 dance studies / 舞蹈教育 / Laban 动作分析的教研人员；舞蹈相关学者散落在 CMCI（Performing Arts）、English（Theatre & Performance Studies）、DDH、ECS。唯一做 dance anthropology 的 Ann R David 是 **Visiting Professor**（按规则排除）
  - **KCL 没有独立的 Department of Sociology**；社会学取向学者主要在 ECS（教育社会学/社会正义）与 GHSM（GHSM 自称 UK Sociology 前十）
  - **KCL 没有独立的 Department of Anthropology**；人类学学者分属 DID（国际发展，职称含 Anthropology）、GHSM（medical anthropology）、DDH（digital anthropology）
  - 职称提取：个人页脱标签文本中 `Contact details` 之前的最后一段即「姓名 + 职称」（如 `Dr Carla Finesilver Reader in Mathematics Education and Inclusion`）
  - **slug 变体要探测**：`/people/zeena-feldman` 404 → 正确 `/people/dr-zeena-feldman`；`/people/jamie-woodcock` 404 且官网无个人页 → 改用 `https://kclpure.kcl.ac.uk/portal/en/persons/jamie.woodcock/`（Pure 个人页亦属官方，可用作 导师主页）
  - **429 限流**：对 `www.kcl.ac.uk` 并发抓取超过约 10 路会触发 429，且**持续数分钟不恢复**（不是死链）。批量核验用串行 + 1.2 秒间隔，或改用 WebFetch 复核；不要据 429 判死
  - **`/people` 目录页**（`https://www.kcl.ac.uk/people`）为壳，不用；按院系 people 页更可靠
- **入学/申请页**: `https://www.kcl.ac.uk/study/postgraduate-research/how-to-apply`（200 已验证）
- **按院系的项目页**（`博士申请信息` 列用这个，不要用上面的申请总入口）: `https://www.kcl.ac.uk/study/postgraduate-research/areas/<dept>-research-mphil-phd`
  - 已实测 200 的五个：`english-research-mphil-phd`、`culture-media-and-creative-industries-research-mphil-phd`、`education-research-mphil-phd`、`global-health-and-social-medicine-research-mphil-phd`、`digital-humanities-research-mphil-phd`
- **Last verified**: 2026-09-16

#### Auckland University of Technology (AUT)
- **Architecture**: 双站 —— 官网 `www.aut.ac.nz`（**curl 403 WAF，需 WebFetch**）+ 学者门户 `academics.aut.ac.nz`（Symplectic "Discovery" SPA，curl 只得 ~2KB 空壳）
- **Layer**: L2
- **⭐ 关键技巧：学者门户有公开 JSON API，不渲染就能批量核验**
  - 个人档案：`https://academics.aut.ac.nz/api/users/<slug>` → 返回完整 JSON（~30KB）
  - 有用字段：`firstNameLastName` / `title` / `positions[].position`(职称) / `positions[].department`(所属系) / `customFilterOne`(Faculty) / **`customFilterThree`(Availability，含 `"Masters Research or PhD student supervision"` 即明确博导资格证据)** / `emailAddress.address` / `otherEmailAddresses[]`(备用邮箱，部分人主字段为空) / `tabSummaryAbout.value`(简介原文) / `labels[]`(Fields of Research) / `discoveryUrlId`(URL slug)
  - 用 curl 直接打 API，几十位候选一次核完，比逐个 WebFetch 渲染快一个数量级
- **按系穷举教职员**：`https://academics.aut.ac.nz/search?by=department&type=user&v=<系名>`（实测可用：`Teacher Education`、`Art & Design`、`Communication Studies`、`Occupational Therapy`、`Sport Leadership & Management`、`Nursing`、`Mental Health & Wellbeing`、`School of Social Sciences & Humanities`、`Rehabilitation`）
  - 陷阱：机构/研究中心名（如 `Health Rehabilitation Research Institute`）当系名查不到，改用所属系（如 `Rehabilitation`）
  - 另一可用形式：`?by=text&type=user&v=<关键词>`（通用全文检索）
  - ⚠️ **该 search 页是 SPA，且没有对应的公开 JSON 搜索端点（2026-09-18 实测）**：`/api/search`、`/api/users?by=…`、`/api/concepts`、`/api/groups`、`/api/users/search`、POST `/api/search` 一律 404；`/api/users/<任意字符串>` 会被当成 `discoveryUrlId` 查人，返回 `{"message":"discoveryUrlId: xxx returned no results."}` 而不是搜索结果。**所以「按系穷举」这条路在脚本里走不通**——要么用浏览器渲染该页，要么用 WebSearch 补人名，再回 `/api/users/<slug>` 逐个核档案。**不要因为脚本查不到就判定「该校/该方向无人」。**
- **个人页**：`https://academics.aut.ac.nz/<firstname.lastname>`（slug 可能带变体，从 API/检索结果取准确形式）
  - **AUT 官方子站的信息要区分「现职」与「历史遗留」**：`sprinz.aut.ac.nz` 等子站的团队/项目页可能仍列着已离任人员并写明「supervises Postgraduate research」，**这类团队页既不能当「导师主页」列使用，也不能当在职证据**，只能用于了解研究方向。要判在职，走下面的「三线交叉法」。
- **Key facts / pitfalls**:
  - **AUT 现行教职员中没有以舞蹈为本体的学者（2026-09-18 结论）**。曾一度认为 Jennifer Nikolai（原副教授，Coaching & Youth Sport Development／School of Sport & Recreation；当代舞实践者与表演研究学者，研究 camera-dancer dyad、动作捕捉与 VR，与教育学院 Andrew Gibbons 合著幼儿「舞蹈与冒险性游戏」研究）在职，**但三项交叉证据显示她已离开 AUT**：① 最新论文 *Dancing to Wellness in the Studio*（Dance Education in Practice，2026-09-14）作者机构标注为 "Independent Academic" 而非 AUT；② 学者门户 `/api/users/jennifer.nikolai` 返回 404（在职教师基本都有档案）；③ AUT「艺术与设计学院教职工」名单、Sport Leadership & Management、Sport and Exercise Science 三处「Our people」均无其名，原 CYD 系已无公开页面。**按「已离任导师不入主表」不要收录**；若机构能确认她仍在职，再按现职单位官方页补录。
  - **⭐ 离任检测「三线交叉法」（可推广到任何学校，2026-09-18 沉淀）**：第三方页面（会议站、期刊简介、聚合站、学校旧子站）会长期残留「某校教授」头衔，**不能作为在职证据**。判定是否仍在职，取以下三条独立证据交叉，≥2 条指向离任即可判离任：
    1. **最新成果的作者机构**：Crossref `https://api.crossref.org/works/<DOI>` → `author[].affiliation[].name`；或 ORCID `https://pub.orcid.org/v3.0/<orcid>/record` 的最新作品。若已改成 "Independent Academic"／其他机构，高度可疑。
    2. **官方院系「Our people」名单**：官网 department / academic-staff 页按系列出在职人员（AUT：`www.aut.ac.nz/research/academic-departments/<dept>`，或 `www.aut.ac.nz/study/study-options/<faculty>/academic-staff`）。⚠️ **先确认该系现在叫什么名字**——院系合并改名后旧系名页面会 404，容易误判成「该校没有这个系」。
    3. **研究门户个人档案**：在职研究人员通常有自动生成的档案（AUT 的 `/api/users/<slug>`）。查无此人时结合 ①② 判断；注意少数在职人员确实没有档案（门户按姓名列出但无链接），故此项单独不具决定性。
  - **Sharon Mazer 是 Professor Emerita of Theatre and Performance Studies → 按规则排除**（她方向最对口，勿误收）
  - **Andrew Denton 已离开 AUT**：2024-07 起任 University of Saskatchewan 新设 School for the Arts 首任院长，勿再按 AUT 收录（其旧页仍在第三方站挂 AUT 头衔）
  - **AUT 全校只有一个博士学位**：Doctor of Philosophy（code **AK3518**），**没有分院系的 PhD 项目页**。
    - ⚠️ `博士申请信息` 的正确填法（**2026-09-18 用户明确要求后修正，此前填法已被否决**）：填**该导师所属学科的研究生项目页** `https://www.aut.ac.nz/study/study-options/<area>`——该页列出本学科全部研究生课程，含 Doctor of Philosophy 入口（如 `.../study-options/communication-studies` 内即列出 `Doctor of Philosophy`）。**不要**统一填 `https://www.aut.ac.nz/courses/doctor-of-philosophy`（用户视其为「全校统一入口」）；要避开的还有 `https://www.aut.ac.nz/study/applying`（申请总入口）。
    - 学科 slug（AUT 官方 17 个分组）：`education`、`art-and-design`、`communication-studies`、`health-sciences`、`sport-and-recreation`、`social-sciences-and-public-policy`、`business`、`creative-technologies`、`engineering-computer-and-mathematical-sciences`、`hospitality-tourism-and-events`、`language-and-culture`、`law`、`science`、`architecture-and-built-environment`、`te-ara-poutama-maori-and-indigenous-development`
    - 判断依据（已实测）：AUT 官方研究生课程页 `/research/postgraduate-study-and-research/postgraduate-programmes` 按 17 学科分组，**PhD 链接在所有分组里完全相同**；`/study/study-options/education/courses/doctor-of-philosophy` → **404**；AUT 自己的博士链接带学科标记参数 `?source=%2F<area>`，但落地页仍是同一个
    - **唯一两个学科专属博士**：**Doctor of Education**（仅 Education 学科，`/study/study-options/education/courses/doctor-of-education`，code AK3685，**不对国际学生开放**）、**Doctor of Health Science**（仅 Health sciences，`/study/study-options/health-sciences/courses/doctor-of-health-science`）。给国际申请者填链接时**不要**用这两个。
  - 院系归属：Faculty of Design & Creative Technologies（Art & Design / Communication Studies / Future Environments / ECMS）、Faculty of Culture and Society（School of Education / Social Sciences & Humanities / Te Ara Poutama / Hospitality & Tourism）、Faculty of Health and Environmental Sciences（Sport & Recreation / Clinical Sciences / Public Health）、Faculty of Business, Economics and Law
  - School of Social Sciences and **Public Policy 已更名为 School of Social Sciences and Humanities**
  - 健康科学学部**没有 arts therapy / dance movement therapy 师资**；艺术与健康方向最近的是 Mental Health & Wellbeing 的 Keith Tudor（生态治疗）与 Nursing 的 Mandie Foster（儿童艺术参与）
- **匹配度复核要点（2026-09-18）**：判定「方向是否对口」前先看该导师所属**学院是否落在任务给定范围内**。本次任务的指定学院是「戏剧/舞蹈/社会学/教育学/文化研究」+「人类学/传媒」，而 AUT 实际能对上的只有 School of Education、School of Social Sciences & Humanities、School of Communication Studies 三个单位；Art & Design、Sport、Nursing、Occupational Therapy、Rehabilitation、Mental Health 的人员**全部属于范围外**，只能按「方法层面相近」记录，备注里要写明研究对象偏离，不要写成方向对口。
- **Last verified**: 2026-09-18

#### Royal College of Art (RCA)
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Leeds
- **Architecture**: Static HTML (staff profile pages)
- **Layer**: L1
- **Access**: Direct URL access to staff profiles at ahc.leeds.ac.uk/design/staff/
- **Key endpoint**: https://ahc.leeds.ac.uk/design/staff/
- **Failed**: —
- **Last verified**: 2026-06-26

#### University of Sussex
- **Architecture**: Static HTML 个人页（`www.sussex.ac.uk/profiles/{id}`），可 curl 直接抓；个人页**不显示邮箱**
- **Layer**: L1（抓个人页正文/研究方向）／L2（抓邮箱需走 vCard 接口）
- **邮箱获取 —— vCard 接口（2026-09-14 验证）**：Sussex 个人页正文里没有 email，页面上的 "What is this?" 是一个 **vCard 下载二维码**，真实端点是
  `https://www.sussex.ac.uk/profiles/vcard/download/{profileId}`（返回 `text/x-vcard`，文件名如 `Andy Medhurst.vcf`）。
  vCard 内一定有 `EMAIL;PREF;INTERNET:` 和 `TEL;WORK;VOICE:` 两个字段——**但要先读内容再判断**：
  - 字段有值 → 拿到官方邮箱
  - 字段为空（如 `EMAIL;PREF;INTERNET:` 后面什么都没有）→ **说明学校自己就没有公开该教师的邮箱**，此时不要猜测地址（`a.medhurst@` / `am123@` 之类一律不可信），改为给学院/学部总邮箱 + 总机号
- **案例（Andy Medhurst, profileId 1794）**：个人页 200、仍列 Senior Lecturer，但 vCard 的 EMAIL 与 TEL 均为空，且他已不在现 Faculty 名录页中 → 判定为**无公开邮箱**，只能经学院转达。这也印证该条备注「约 67-68 岁、退休年龄，建议先邮件确认是否仍收博士生」的风险提示
- **院系重组坑**：Sussex 已把原来的 School of Media, Film and Music 并入 **Faculty of Media, Arts and Humanities**（`www.sussex.ac.uk/mfm/`），旧页面上的 `mfm@sussex.ac.uk`（01273 877538）为历史地址；现行总邮箱是 `media-arts-humanities@sussex.ac.uk`。注意 `wwwstage.sussex.ac.uk` 是**测试域名**，上面能查到大量联系人邮箱但**不能当作现行信息**直接写入
- **Last verified**: 2026-09-14

#### University of Southampton
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### Kingston University
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### De Montfort University
- **Architecture**: Static HTML (staff profile pages)
- **Layer**: L1
- **Access**: Direct URL access to academic staff pages at dmu.ac.uk/academic-staff/
- **Key endpoint**: https://www.dmu.ac.uk/academic-staff/
- **Failed**: —
- **Last verified**: 2026-06-26

#### University of Edinburgh
- **Architecture**: JS-rendered profile directory (edwebprofiles.ed.ac.uk)
- **Layer**: L3
- **Access**: https://www.ed.ac.uk/profile/{name} → redirects to JS profile
- **Key endpoint**: https://www.ed.ac.uk/profile/alison-lenton
- **Failed**: —
- **Last verified**: 2026-06-26

#### University of Glasgow
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Brighton
- **Architecture**: Pure Portal (research.brighton.ac.uk)
- **Layer**: L2
- **Access**: Pure Portal JSON API → parse researcher profiles
- **Key endpoint**: https://research.brighton.ac.uk/persons/
- **Failed**: —
- **Last verified**: 2026-06-26

#### Nottingham Trent University (NTU)
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### Heriot-Watt University
- **Layer**: L2
- **Architecture**: Pure Portal (researchportal) + Static HTML (hw.ac.uk)
- **Best method**: Use hw.ac.uk profiles (not researchportal UUIDs). Format: `hw.ac.uk/profiles/uk/school/tex/faculty/{slug}`
- **Key URL / endpoint**: `https://www.hw.ac.uk/profiles/uk/school/tex/faculty/{slug}`
- **Failed**: researchportal.hw.ac.uk UUID-based URLs → 404
- **Last verified**: 2026-06-26

#### University College London (UCL) — Psychology
- **Architecture**: profiles.ucl.ac.uk numeric ID system (RESTRUCTURED 2025-2026)
- **Access**: Old PALS URLs 404 → new system https://profiles.ucl.ac.uk/{numeric-id}-{name}
- **Key endpoint**: https://profiles.ucl.ac.uk/2667-david-shanks
- **Failed**: All old pals.ucl.ac.uk URLs broken
- **Last verified**: 2026-06-26

#### 🔑 UCL 全站通用：profiles 的 JSON 接口 + 403 反爬的绕法（2026-10-07 实测，强烈建议照做）

**痛点**：`www.ucl.ac.uk` 对 curl/urllib **一律 403**（返回约 5.7KB 挑战页），批量核验个人主页时无法用"HTTP 200 + 页面含姓名"这套判据——`profiles.ucl.ac.uk/{id}-{slug}` 对 curl 虽返回 200，但只是约 3.3KB 的 `Discovery` JS 空壳，**正文里没有姓名**，会误判成"姓名未命中"。

**解法：profiles.ucl.ac.uk 有公开 JSON API，curl 可直读**（无需浏览器、无需 token）：

```bash
curl -s -A "Mozilla/5.0" "https://profiles.ucl.ac.uk/api/users/45469"
```

返回字段里有两个宝：

| 字段 | 含义 | 用途 |
|---|---|---|
| `positions[0].position` / `.department` | **官方在职职位 + 所属院系** | 职称唯一权威来源；可直接和名录页标题交叉校验（等级冲突应为 0） |
| `emailAddress` | 官方邮箱（可能是 dict，取 `.address`/`.value`） | 邮箱核验 |

- URL → ID：正则 `profiles\.ucl\.ac\.uk/(\d+)`；也支持 `profiles.ucl.ac.uk/{id}` 无 slug 形式。
- `/api/profile/{id}`、`/api/profiles/{id}` 均 404，**只有 `/api/users/{id}` 可用**。
- 前端配置在 `https://profiles.ucl.ac.uk/javascript/configuration.js`（内含 `publicApiUrl`）。
- 实测：194 条记录（139 条 UCL）8 并发全量核验约 1 分钟，姓名命中率 100%、职称等级冲突 0。

**UCL 院系级页面（www.ucl.ac.uk）只能用 WebFetch**：curl 的 403 是反爬，**不代表链接坏了**，不要据此剔除候选人。

#### UCL 建成环境（The Bartlett）—— 院系与链接速查（2026-10-07 实测）

| 单位 | 师资名录页（→`其他导师信息`） | 研究学位项目页（→`博士申请信息`） |
|---|---|---|
| The Bartlett School of Sustainable Construction (BSSC) | `/bartlett/construction/people/academics` | `/prospective-students/graduate/research-degrees/sustainable-construction-mphil-phd` |
| Bartlett School of Planning | `/bartlett/planning/people/academics` | `…/research-degrees/planning-mphil-phd` |
| Institute for Environmental Design and Engineering (IEDE) | `/bartlett/environment-energy-resources/environmental-design/people-institute-environmental-design-and-engineering` | `…/research-degrees/environmental-design-and-engineering-mphil-phd` |
| UCL Energy Institute | `/bartlett/environment-energy-resources/energy/people-ucl-energy-institute` | `…/research-degrees/ucl-energy-institute-mphil-phd` |
| Civil, Environmental and Geomatic Engineering (CEGE) | `/engineering/civil-environmental-geomatic-engineering/people/academic-staff` | `…/research-degrees/civil-environmental-and-geomatic-engineering-mphil-phd` |
| STEaPP | `/steapp/people` | `…/research-degrees/science-technology-engineering-and-public-policy-mphil-phd` |

（前缀统一为 `https://www.ucl.ac.uk`；`…/research-degrees/` = `https://www.ucl.ac.uk/prospective-students/graduate/research-degrees/`）

- **BSSC 带博证据的免费来源**：`https://www.ucl.ac.uk/bartlett/construction/people/phd-students` 逐个列出在读博士生及其 **supervisory team**——出现在这里的老师就是有实际带博记录，可直接写进备注的带博证据，不必依赖 `AVAILABILITY` 字段。
- **⚠️ 该页有滞后**：名单里会出现已离开 BSSC 的导师（如 Jacqui Glass、Jennifer Rode、Andrew/Andre Edkins、Eleni Papadonikolaki、Ling Ma）。**是否在职以 `people/academics` 名录页为准**，PhD students 页只用来补充"曾/正在带博"这一事实。
- **名录页 ≠ profiles 页**：职称以**名录页**为准（更细，如 `Professor of Facility Management Innovation`）；profiles 的 `positions` 用于复核等级。实测名录页把 Michael Pitt 标成 `Director of Teaching and Learning`（行政角色），会导致按"教学岗"被误剔——**行政头衔与教授头衔并存时，以教授头衔收录**。
- **Last verified**: 2026-10-07

#### Birkbeck, University of London
- **Architecture**: Static HTML + numeric profile IDs
- **Access**: https://www.bbk.ac.uk/our-staff/profile/{id}/{name}
- **Key endpoint**: https://www.bbk.ac.uk/our-staff/profile/8009667/ulrike-hahn
- **Failed**: Profile IDs can redirect to wrong person; verify the ID
- **Last verified**: 2026-06-26

#### University of Bristol
- **Architecture**: Main dept pages redirect to generic homepage; use RIS portal
- **Access**: https://research-information.bris.ac.uk/en/persons/{name}
- **Key endpoint**: https://research-information.bris.ac.uk/en/persons/stephan-lewandowsky
- **Failed**: All bristol.ac.uk/psychology people pages redirect to dept homepage
- **Last verified**: 2026-06-26

#### University of Warwick — Business School
- **Architecture**: Static HTML (WBS separate from main Warwick)
- **Access**: https://www.wbs.ac.uk/about/person/{name}/
- **Key endpoint**: https://www.wbs.ac.uk/about/person/neil-stewart/
- **Failed**: Old warwick.ac.uk/fac/sci/psych/people URLs 404 for Stewart (moved to WBS)
- **Last verified**: 2026-06-26
