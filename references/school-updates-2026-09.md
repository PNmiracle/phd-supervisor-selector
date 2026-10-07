# 区域案例更新日志 · 2026-09

> 自 `school-updates-log.md` 于 2026-10-07 按月拆分。索引见 `school-updates-log.md`。

## 2026-09-09 更新（王莺艺 — 英澳新税收治理/数字政府方向 URL 修正）
- **Sheffield SPIR PhD 申请页**: `/spir/research/phd` 404 → 正确 `https://sheffield.ac.uk/spir/phd/apply`（含 entry reqs & 联系导师指引）
- **Bristol School for Policy Studies 博士申请**: `/sps/research/postgraduate-research/` 404 → 正确 `https://bristol.ac.uk/sps/study/postgraduate/`（列出 PhD Social Policy 等项目）
- **Nottingham Politics 研究学位**: `/politics/study/postgraduate/research/index.aspx` 404 → 正确 `https://www.nottingham.ac.uk/politics/study/postgraduate-research/`（含 PIR PhDs 页）
- **ANU RegNet 人员列表**: `regnet.anu.edu.au/people` 返回 403 Access denied → 正确 `https://regnet.anu.edu.au/people-0/`（含 Henne Director 简介）
- **UCL curl 403 误报**: ucl.ac.uk 对 curl 返回 403(约 5-6KB 挑战页)，WebFetch 可正常读取 → 勿据 curl 判死 UCL URL
- **Sydney staff profile 2118B 壳**: sydney.edu.au/arts/.../profiles/*.php curl 仅返回 2118B SPA 壳，WebFetch 能渲染真实内容（Elbra/Mikler 均验证有效）→ 与 profiles.sydney.edu.au 同属 SPA，验证一律走 WebFetch
- **UCL IIPP 博士申请页** (bartlett/public-purpose/study/mphilphd/apply) supervisor 候选列表：Mazzucato/Kattel/Roll/Ryan-Collins/Rikap/Alves — **不含 David Eaves**，Eaves 需先邮件确认收生

## 2026-09-14 重要方法论：区分「公共政策路径」与「政治经济学路径」
**教训**：学生方向若表述为"公共政策视角下研究 X（如税收）"，**不能只搜政治学系/国际关系系**。Political Economy / IPE 与 Public Policy / Public Administration 是两条不同路径：
- **政治经济学(IPE)路径**：研究 X 的政治逻辑、成因与后果（为何征税、税制政治、避税政治、财政意识形态）→ 政治学系、政治经济学系、IR 系
- **公共政策/公共行政(PP/PA)路径**：研究 X 的政策设计、执行、遵从与评估（征管、合规、交付、监管执行）→ Public Policy School、Public Administration Dept、Social Policy Research Centre
- 学生若为实务背景（如税务系统），通常适配 PP/PA 路径而非 IPE。**搜索时必须两条线并行覆盖**

**各区 PP/PA 路径的重镇（税收/财政/数字政府方向）**：
- **UCL School of Public Policy**（隶属 Dept of Political Science）：设 Public Finance 岗——Mike Seiferling（官方 Supervision Topics 明列 Fiscal Policy (especially tax systems)、Fiscal Transparency/Corruption；前 IMF）；Colin Provost（监管执行与合规）。另 UCL 政治学有 "Public Policy, Management and Regulation" 研究集群（含 public finance、progressive taxation）
- **Birmingham DPAP / INLOGOV**（英国公共行政重镇）：May Chu（中国场景监管执行）、Slava Jankin（Centre for AI in Government 创始主任）、Catherine Needham（监管效果，标 Accepting PhD Students）；Stephen Jeffares 为 INLOGOV 博招负责人（套磁入口）；Peter Watt 为 Emeritus 不可招
- **ANU Crawford**：除 TTPI 的 Breunig（经济学路径）外，Social Policy Institute 主任 Peter Whiteford（tax-transfer policies，OECD 8 年）为公共政策路径；David Stanton 为 Honorary 仅可副导；TTPI 其余成员多为经济学路径
- **UNSW Social Policy Research Centre (SPRC)**：属 Arts, Design & Architecture 学部非商学院——Bruce Bradbury（税收-转移支付、印花税改革）
- 反向确认无候选：Sydney Policy Lab（唯一公共财政者 Gareth Bryant 为 IPE 路径）、Auckland PPI（性别预算/气候/家暴，无税收）、Monash MPP、UTS IPPG（涉税者 Roman Lanis 属会计系）
- 陷阱：Melbourne 的 Christopher Hoy 做纳税遵从 RCT（题目最贴合）但属商学院 Melbourne Institute → 按"排除商科"规则不收

**备注写法规则（用户两次指出后确立）**：
- 研究**实质前置**、学科标签**后置**；不要以"XX政治经济学，"开头
- 对 IPE 路径导师，句末补一句客观路径说明（"取径为国际政治经济学，侧重…的政治分析，而非征管执行视角"），让学生自行判断，不得删除学科归属信息

---

## 2026-09-18 更新（于洋 — 体育/运动科学方向·美国游泳研究的地理错位）

### 结论：美国竞技游泳科研在学术岗位上是结构性缺席，不是排名档位选错

做水生方向（游泳/水上项目）的美国在职学者散落在 **#26 到 #232**，60-100 恰好切在空处。以后遇到"游泳/水上项目"方向的学生，**先讲清楚美国是弱地理区**，再决定策略。

### 全美清单（2026-09 核实）

| US News | 学校 | 人 | 方向 | 能带博 |
|---|---|---|---|---|
| #26 | UNC 教堂山 | Battaglini（运动生理）＋ McLaughlin（数学/流体力学）＋ Mahaney（计算机） | 与 USA Swimming 合作水槽 PIV、手部受力、公开水域波浪槽，为 LA28 备战 | 有 EXSS 博士，但非游泳博士方向 |
| #26 | UVA | Ken Ono（**数学系**） | USA Swimming 技术顾问（2016 起），防水加速度计/陀螺仪数据分析、CFD | ❌ 不能当运动科学导师 |
| #69 | Pittsburgh | Elizabeth Nagle | 水生环境生理、水槽游泳最大摄氧量测试 | ❌ **Professor of Practice**，且**不在** PhD in Exercise Physiology 官方导师名册（7 人名单无她） |
| **#73** | **Indiana Bloomington** | **William D. Ramos** | 水上环境与人的体验、溺水预防、水安全、娱乐性用水、项目设计；**IU 水上运动研究所主任**；红十字会科学顾问委员会水上分委员会主席 | ✅ PhD in **Health & Wellness Design**（可带博）—— 60-100 内唯一水生方向在职导师 |
| #73 | Indiana Bloomington | Joel Stager、Dave Tanner | 竞技游泳生理/生物力学（Counsilman Center） | ❌ 均 **Emeritus**，中心页面已下线 |
| #169 | Hawaiʻi Mānoa | **Jan Prins** | 「Biomechanics as related to Competitive Swimming and Aquatic Rehabilitation」，Aquatic Research Laboratory，水下高速摄像＋运动学 | ✅ PhD in Education（Kinesiology track），在职副教授 |
| #232 | UNLV | **John Mercer** | 「biomechanics and physiology of endurance performance with a special emphasis on swimming」 | ✅ 原 Kinesiology PhD 停招 → PhD in Interdisciplinary Health Sciences |
| 无全国排名 | Cal State LA | George Crocker | Swim Performance Lab（水槽＋代谢车） | ❌ 不授博士 |

**真正「在职＋方向写游泳＋能带博」全美仅 Prins（#169）与 Mercer（#232）两人。**

### 结构性原因（四条，都有出处，可直接引用）

1. **2018 年第 XIII 届国际游泳生物力学与医学大会（筑波）**会后综述：*"only two USA organizations contributed their research: Indiana University and Swimming Technology Research."* —— 23 国参会，美国只投两家。
2. **Lombardo & Emiah (2014), *SpringerPlus* 3:307**：2000–2012 年 NIH 从未就"竞技表现"课题招标，NIH 与 NSF 均未资助；而美国高校终身教职评价依赖这两家经费 → 研究被推向临床/健康人群。
3. **美国无联邦体育部**。前 USOC 运动科学顾问 Wade Gilbert 原话："most of the high-level research in athletics is coming out of Canada, Australia, and England, and that's because those countries have federal oversight of sport, federal ministries of sport." 澳 AIS 有 50+ 运动科学家、游泳馆 30 台水上/水下摄像机＋出发台内置测力板；英 UK Sport 伦敦周期年投约 1.6 亿美元。
4. **岗位形态错位**：懂游泳的科学人编制在 USA Swimming / USOPC / 大学体育部（如 Auburn 的 "Director of Performance Science" Tyler McGill），做内部报告，不带博士。

### 策略含义

- **游泳/水上项目方向的学生，澳、新、欧洲才是主战场**：AIS、葡萄牙（Barbosa、Marinho、Morais）、西班牙（Arellano、Veiga）、法国（Seifert）、意大利（Zamparo）。
- 美国方向若必须做，只有三条路：① 接受"生物力学工具迁移"（测力台/动作捕捉/可穿戴可复用，非游泳本身）；② 破档投 Prins/Mercer；③ 跨学科切入 UNC/UVA。
- **"水上项目"口径要问清**：若含赛艇/皮划艇/帆船，可选面会明显扩大；若仅指游泳/跳水/水球/花游，则按上表。

### 方法论教训（重要）

- **审核 agent 报的"没有"不能直接采信**。曾据其汇总结论断言"60-100 内无水生导师"，实际漏了 IU 的 Ramos。**要穷尽到院系师资页逐个比对**，而不是依赖汇总。
- **agent 报的职务必须回官网核**。agent 称 Ramos 是 Aquatics Institute 主任，官网个人页出现次数为 0；改查 **IU 官方新闻页**（news.iu.edu / newsinfo.iu.edu）才核实到。规则：**职称以院系目录页为准，职务以官方新闻/公告为准**。
- **US News 排名逐年变动，机构主表可能落后一年**。2026 版相对 2025 版：Penn State #63→#59（跌出 60-100）、Iowa #98→#102（跌出）。交付前应对照当年榜单复核，**发现冲突时报给机构定口径，不擅自增删记录**。

---

## 2026-09-20 更新（刘艺佳 — 兽医/动物免疫方向 · 英澳新加欧 28 校访问路径）

学生方向：动物基因工程疫苗学与分子免疫学 / 病原分子诊断与免疫检测 / 寄生虫-宿主互作。命中「兽医/动物科学/传染病免疫」这一学科簇。**下面这些路径对任何兽医、动物科学、免疫学、传染病方向的学生都可直接复用。**

### 高价值检索入口（按省力程度排序）

| 学校 | 层 | 关键入口 | 要点 |
|---|---|---|---|
| **University of Cambridge** | L1 | `https://www.vet.cam.ac.uk/people?field_available_to_supervise_mph_value=1` | **官方博导名单**：该复选框参数直接筛出"Supervises doctoral students"，22 人。`/directory` 与 `/sd-classification/...` 均为 404 |
| **University of Bristol** | L2 | 官网 Algolia 索引：appId `RFW6CI5PBU`，索引 `prod_PROFILES`（前端 search-only key 公开） | 人员页是 **Gatsby SPA**，curl 只能取壳。用 Algolia 按 `categories.lvl1:Faculty of Health and Life Sciences > Bristol Veterinary School` 过滤，**154 人一次取全**。个人页 `https://www.bristol.ac.uk/person/<uuid-slug>/` 可 curl |
| **Royal Veterinary College** | L1 | `https://www.rvc.ac.uk/about/our-people/people-finder?page=1..54` | 官方 People Finder 分页有效，共 **371 个人页**。个人页 `https://www.rvc.ac.uk/about/our-people/<slug>`。主页常带 "I have successfully supervised N PhD students" + "happy to hear from potential research students" |
| **University of Edinburgh (vet)** | L1+L3 | `https://vet.ed.ac.uk/roslin/people/immunology`、`/virology`；个人页用 Pure | `vet.ed.ac.uk` 可 curl（带 UA）。**Pure（`research.ed.ac.uk`）对 curl 返回 403**，需用浏览器类抓取；但 Pure 主页的 **"Accepting PhD Students"** 字段是最强带博证据（还会列 Current/Previous PhD Students） |
| **University of Glasgow** | L1 | `https://www.gla.ac.uk/schools/bohvm/staff/`（学院 A-Z 全员名录） | 站内检索为 JS 渲染不可用，改抓目录页 + 逐个 `staff/<slug>/`。注意新学院名 **School of Biodiversity, One Health & Veterinary Medicine** |
| **University of Liverpool** | L1 | `https://www.liverpool.ac.uk/infection-veterinary-and-ecological-sciences/staff/infection-biology-and-microbiomes/` | 系名录页 curl 可读全部姓名+职称+官方邮箱；个人页 `people/<slug>` 研究正文由 **profiles.liverpool.ac.uk** 注入，需交叉核 |
| **University of Nottingham (vet)** | L1 | `https://www.nottingham.ac.uk/vet/people/index.aspx` | 含 A-Z Directory，公开姓名/职称/电话/官方邮箱；个人页 `/vet/people/<slug>` |
| **University of Oxford (Jenner)** | L3 | `https://www.jenner.ac.uk/team` | **对无 UA 的请求返回 403，必须带浏览器 UA**。个人页 `/team/<slug>` |
| **The University of Melbourne** | L1 | 个人页 `https://findanexpert.unimelb.edu.au/profile/<id>-<slug>` | 学院目录页 `mvs.unimelb.edu.au/about/our-people/academic-staff`；APCAH 另有人页 |
| **The University of Sydney** | L3 | `https://profiles.sydney.edu.au/<name>/about` | 组页 `profiles.sydney.edu.au/groups/177812/experts` 只返回标题，需逐人搜索命中。个人页含 **AVAILABILITY: Research supervision** 字段 |
| **The University of Queensland** | L1 | `https://about.uq.edu.au/experts/<id>`；QAAFI 用 `qaafi.uq.edu.au/node/<id>`；兽医学院用 `veterinary-science.uq.edu.au/profile/<id>/<slug>` | 个人页直连可读，含 "Available for supervision" 明文 |
| **Adelaide University** | L1 | `https://researchers.adelaide.edu.au/profile/<user>` 或 `/node/<id>` | ⚠️ 校名 2026 年已由 University of Adelaide 合并为 **Adelaide University**。个人页含 **"Eligible to supervise Masters and PhD as Principal Supervisor"** 字段，还有 "email supervisor to discuss availability" |
| **University of Guelph (OVC)** | L0-SPA | 博导名单 `https://calendar.uoguelph.ca/graduate-calendar/graduate-programs/pathobiology`；人员页 `https://ovc.uoguelph.ca/pathobiology/people/faculty/<name>` | **OVC 站点是 Next.js 客户端渲染，curl 拿不到正文**，必须用浏览器渲染后取 `document.body.innerText`。**研究生院 calendar 页标注 "Graduate Faculty" 是最可靠的博导证据** |
| **University of Calgary (UCVM)** | L1 | 官方 PhD 页 `https://grad.ucalgary.ca/future-students/explore-programs/veterinary-medicine-phd` | ⭐ 该页直接标注 **"Accepting Inquiries" / "Seeking Students"**，是最省力的在招信号源。个人页 `profiles.ucalgary.ca/<slug>` |
| **University of Saskatchewan (WCVM/VIDO)** | L1 | grad 项目页 `https://grad.usask.ca/programs/vaccinology-immunotherapeutics.php`（含 Research supervisors 名单）；VIDO 团队页 `https://vido.org/team/` | WCVM 系页 `wcvm.usask.ca/departments/vetmicro/vetmicro-people/` 可 curl |
| **Utrecht University** | L1 | `https://research-portal.uu.nl/en/persons/<slug>` | ⭐ **`/persons/<slug>/supervised/` 子页直接列出其博士论文清单**，是最强的博导证据源。学院单元用 `research-portal.uu.nl/en/organisations/<unit>/persons/` |
| **Wageningen (WUR)** | L1 | `https://research.wur.nl/en/persons/<slug>/` | ⭐ **项目区会写明 `Promotor` / `Co-promotor`**，是最强博导证据。个人页 `wur.nl/en/persons/<slug>` |
| **Ghent University** | L1 | `https://research.ugent.be/web/person/<slug>-0/en` 及其 `/projects/en` | ⭐ 项目页**逐条标注 "As PhD Supervisor" / "As Promotor" / "As Administrative supervisor"**，还常带中国籍博士生姓名，可作 CSC 友好度间接信号 |
| **University of Copenhagen** | L1 | `https://researchprofiles.ku.dk/en/persons/<slug>` 与 `research.ku.dk` | CV 子页含 supervision 原文。**兽医学在 `ivh.ku.dk`** |
| **University of Bern (Vetsuisse/IVI)** | L1 | `https://www.ivi.unibe.ch/research/<div>/group_<name>/`；寄生虫用 `https://www.ipa.vetsuisse.unibe.ch/research/group_<name>/` | IVI 是瑞士国家级兽医病毒学与免疫学研究所，**四个研究组按 Division 分列（Immunology / Virology）**，组页标题即 "Prof. Dr. XXX" |
| **Vector / Vetmeduni Vienna** | L1 | `https://www.vetmeduni.ac.at/en/<institute>/faculty-and-staff` | ⚠️ **`www.vetsuisse.uzh.ch` NXDOMAIN，`www.vetbakt.uzh.ch` 根路径 curl exit 56** → UZH 改用 `ivb.uzh.ch` / `vetparasitology.uzh.ch` |
| **TiHo Hannover** | L1 | `https://www.tiho-hannover.de/en/clinics-institutes/special-units-and-research-centers/research-center-for-emerging-infections-and-zoonoses/research/research-groups` | ⭐ RIZ 研究组总表**含各组研究方向英文原文**，一次看清全院布局 |
| **NMBU** | L3 | 用 WebFetch（非 curl） | ⚠️ **NMBU 全站 curl 返回 403（反爬）**，必须用浏览器类抓取 |
| **SLU** | L1 | `https://www.slu.se/en/profilepages/<首字母>/<姓名>/` | ⚠️ SLU **无系级员工总表页**，只能逐人 profilepages 核验。个人页常含 "I have supervised N PhD students" |
| **University College Dublin (UCD)** | L1+L3 | 院系页 `https://www.ucd.ie/vetmed/about/staffprofiles/`；个人页 `https://people.ucd.ie/<邮箱本地部分>` | `staffprofiles` 可 curl；`people.ucd.ie` 是 JS 应用需浏览器类抓取 |
| **Murdoch University** | L1 | `https://www.murdoch.edu.au/schools/veterinary-medicine/about/our-people` | 一次 WebSearch 即返回完整 staff 列表（含职称）；个人页 `profiles.murdoch.edu.au/myprofile/<slug>/` |
| **Massey University** | L1 | `https://www.massey.ac.nz/massey/learning/colleges/college-of-sciences/about/veterinary-and-animal-sciences/staff-list.cfm?stref=<id>` | 参数式 URL。**职衔栏会出现 "Doctoral Supervisor" 字样**，可直接判定带博资格 |
| **University of Otago** | L1 | `https://www.otago.ac.nz/microbiology-and-immunology/our-people` | 个人页 `/<name>` 直连可读 |
| **University of Auckland** | L1 | `https://profiles.auckland.ac.nz/<slug>` | ⭐ 页内含 **"GRADUATE SUPERVISION / PhD/Doctoral Accredited Supervisor / Has Current Supervision Opportunity"** 字段，同时判定带博资格与在招状态 |
| **DTU (National Veterinary Institute)** | — | ❌ **判为 completed_dry** | 丹麦兽医法定应急任务 **2019–2020 年由 DTU 移交 University of Copenhagen + Statens Serum Institut (SSI)**。DTU Vet 的兽医病毒学/免疫学团队随之流失（Lars Erik Larsen、Graham Belsham → KU；Gregers Jungersen → SSI；Wilhelm Gerner → 英国 Pirbright）。`dtu.dk` 的 institute 页与 `orbit.dtu.dk` 人员页均 404（机构已重组）。**以后丹麦兽医方向直接看 KU，不要耗时间在 DTU** |

### 学科特有教训

1. **"Emeritus / Adjunct 陷阱"在兽医方向特别密集**。本轮因此排除 8 位方向极对口的人：Eva Nagy（Guelph，重组禽用病毒疫苗，Emeritus）、Davor Ojkic（Guelph，检验开发，Adjunct）、Eileen Devaney（Glasgow，Emeritus）、Huub Savelkoul（Wageningen，Emeritus）、Eric Cox / Freddy Haesebrouck / Richard Ducatelle（Ghent，Emeritus）、Lorne Babiuk（Alberta，Visiting）、Fiona Tomley（RVC，官网自述 semi-retired）、Stig Milan Thamsborg（Copenhagen，2026-10 满 70）。**兽医系资深教授多，筛人时必须逐个看职称后缀与主页自述状态，不能只看方向。**
2. **"组名 / 项目名"是兽医方向最可靠的匹配证据**，比个人研究描述更硬。因此应优先抓：课题组名（Bern 的 `Group Hemphill: Drugs and vaccines against apicomplexans`）、在研项目名（Liverpool 的 `pen-side diagnostic test for fluke`）、博士生课题名（Liverpool 的 `Design of Protein-Subunit and Multi-Epitope Vaccines Against Mycoplasma gallisepticum`）。
3. **欧陆"岗位制 vs CSC"要单独核**。荷兰 UD、丹麦 lektor、瑞典 docent 是否可任博士主导师因校而异；德国 apl./PD 通常**不能**独立任主导师（本轮剔除 TiHo 的 apl. Prof. Hans-Joachim Schuberth、Bern 的 PD Dr. Gert Zimmer、Gießen 的 PD Dr. Simone Häberlein）。**PD / apl. / Akademischer Oberrat 一律先按"资格待确认"处理。**
4. **专业强校必须手工补进学校主表**。本轮 3 所（Royal Veterinary College、Vetmeduni Vienna、TiHo Hannover）在原「非美国学校主表」中不存在，需先建记录再关联，否则 QS排名 / Location 两个 MagicLookUp 字段无法自动填充。**兽医、艺术、音乐类专业院校普遍不在 QS 综合榜，选导前应先查主表是否收录。**
5. **CSC 接收意向基本查不到官网明示证据**。可用的间接信号只有「组内中国籍博士生集中」（本轮最强的是 Ghent 的 Bert Devriendt，组内 6 名中国籍博士生）与「与中国高校合作发表」。**这一项只能靠套磁时直接问，不要指望从官网筛。**

---

## 2026-09-21 更新：URL 复核方法与 4 个高频踩坑（跨学科通用）

批量写完导师记录后必须做一遍「检查一遍」复核。以下四个坑在本轮 48 条里全部踩到，且**都属于"URL 看起来对、实际不对"或"验证手段用错"的类型**，任何学科都会遇到。

### 坑 1：导航页冒充个人页（最容易漏）

**现象**：URL 路径结构完全合理，HTTP 200，页面很大（80KB+），但**正文里没有这个人**。

实例：Vetmeduni Vienna 的 `<institute>/faculty-and-staff` 只是**入口导航页**，真正含人名的页在子路径：
- `.../faculty-and-staff/institute-director`（所长）
- `.../faculty-and-staff/contact/scientific-staff`（科研人员）
- `.../about-us/head`（Unit 负责人）

**规则**：填写「导师主页」后，必须验证**页面正文里出现该导师的姓名**（不只是 URL 或 title 命中）。`HTTP 200 + 页面很大` 完全不代表对。

### 坑 2：JS SPA 的 "app shell" 被误判为"页面有问题"

**现象**：curl 返回 200 但只有 2KB 左右的壳，title 是应用名。

本轮遇到的三个系统：
| 学校 | 系统 | curl 返回 |
|---|---|---|
| University of Sydney | `profiles.sydney.edu.au/<name>/about` | 2.1KB，title = **"Discovery"** |
| University College Dublin | `people.ucd.ie/<email-local-part>` | 2.1KB，title = **"Discovery"**（同一套产品） |
| University of Melbourne | `findanexpert.unimelb.edu.au/profile/<id>` | 6.2KB，title = **"Pardon Our Interruption"**（**Imperva 反爬**，不是 SPA） |

**处理**：这不是"链接错了"，而是"curl 验不了"。两条替代路径：
1. **搜索引擎快照最有效**——`WebSearch "姓名" "学校"` 时，Bing/Google 常直接返回官方页面（含 `profileprint/<id>` 这类打印版）的**全文**，可用于核对姓名、职称、邮箱、研究方向。Melbourne 的 Imperva 就是这么绕过的。
2. 浏览器类抓取（render 后取 `document.body.innerText`）。

**注意 Melbourne 的额外发现**：`findanexpert.unimelb.edu.au/profileprint/<id>`（打印版）在搜索结果里能拿到全文，是绕过 Imperva 的关键；profile ID 是稳定标识，**slug 部分写错（拼写、多余前缀）也不影响 ID 命中**，但为规范起见仍应改成搜索结果显示的规范 slug。

### 坑 3：slug 是模型"拼"出来的，不是从页面抄的

本轮 48 条里有 2 条 slug 拼写有问题：
- `4100-amir-hadjoormohammadi` —— 正确拼写应是 `Hadjinoormohammadi`（少了一个 n）
- `189843-prof-abdul-jabbar` —— 多了 `prof-` 前缀

**规则**：slug 必须**逐字符从搜索结果或页面的实际 href 复制**，不能凭姓名拼。ID 部分对、slug 部分错是最危险的组合——点开可能仍能到达，但一旦站点改路由就会 404。

### 坑 4："emeritus/retired" 关键词扫描几乎全是误报

本轮 48 条扫出 5 条含 `emeritus`，**逐条读上下文后确认 100% 是误报**，全部来自页面**导航栏/侧边栏里的"他人的条目"**：
- Bristol 的人员页侧栏列出全系名录，里面有 `Emeritus Professor Adam Finn`
- UQ 站点导航里有 `Celebrating Emeritus Professor Ian Frazer AC`
- McGill 寄生虫所页面导航里有 `Professors Emeritus/Emerita` 这一**分类标签**，而被检对象本人的条目写的是 `Assistant Professor`

**规则**：**禁止用关键词命中直接判定退休风险**。必须回到该导师自己的条目/简介段落里读上下文。反过来也成立——真正的 emeritus 有时写成 `semi-retired`、`no longer accepting students`、`Prof. emer.`，关键词表要一并覆盖。

### 复核清单（批量写完后按顺序跑）

1. **链接连通性**：curl 带浏览器 UA 逐个验，记录 HTTP 码与字节数。**字节数 < 3KB 的一律进人工复核队列**（多为 SPA 壳）。
2. **姓名命中**：正文里是否出现该导师姓名（拆姓名 token 匹配，注意 `Prof.`/`Dr.` 要去掉）。
3. **域名一致性**：URL 域名是否属于该导师所在学校。注意**例外**：Oxford 的 Jenner Institute 用 `jenner.ac.uk`（不是 ox.ac.uk）、McGill 的 Institute of Parasitology 用 `mcgill.ca/parasitology/`、UQ 的 QAAFI 用 `qaafi.uq.edu.au`——这些是合法子域，不要误判。
4. **退休风险**：按坑 4 的方式读上下文，不用关键词直判。
5. **备注用语**：扫机构禁用判定词（`很匹配`/`高度相关`/`完美匹配`/`核心人选`/`很契合`/`高度契合`/`很有交集` 等），改成 `和你的XX方向能搭上`/`可以往XX方向靠`/`比较对口` 这类客观关联表述。
6. **全域去重**：按「导师」名与**全表**（不只是本轮新增）比对；同时报告空姓名行数，并确认这些空行是否为本轮产生。
7. **字段完整性 + 只读列**：「选导意向」「状态」这类由学生/流程填的列应保持为空；MagicLookUp（QS排名/Location）只有在成功关联学校记录后才会自动填充——**若为空，先查学校是否存在于学校主表**（专业强校常缺，需先补建）。

---

## 2026-09-21 补充：院系人员页的职称会滞后数年 ⚠️

**本轮实证**：University of Guelph 的 OVC 官方人员页在 2026-09 仍写 Leonardo Susta 为 **"Assistant Professor"**，但：
- ORCID 与 Frontiers Loop 记 **"2020–present Associate Professor / 2014–2020 Assistant Professor"**
- 本人维护的 The Conversation 页面同样记 "2020–present Associate Professor"
- ResearchGate 的 "Current position" 栏亦为 "Professor (Associate)"

即**官方院系页比事实滞后约 6 年**。

**规则**：查实「近年职称变动 / 是否已升职 / 是否已跳槽」时，按以下优先级：

| 优先级 | 来源 | 特点 |
|---|---|---|
| 1 | **ORCID 的 Employment 段** | 精确到月，研究者本人或机构导入，一手雇佣记录 |
| 2 | **机构自己的 Research Portal**（如 `researchportal.<uni>`、`research.ugent.be`、`researchportal.helsinki.fi`、`profiles.ucalgary.ca`） | 由科研管理系统生成，通常同步及时 |
| 3 | **研究者自维护的第三方页**（The Conversation / Frontiers Loop / ResearchGate "Current position"） | 本人维护，更新及时但不权威 |
| 4 | 院系简介页 / 人员目录 | ⚠️ **常滞后数年，只能作方向与联系方式的来源，不能作职称与在职状态的判据** |

**注意这不违背"只信官方页面"的纪律**：ORCID Employment 段与机构 Research Portal 都属可核验的一手记录；真正不可靠的是「手工维护的院系简介页」。

**同类实证（离职/跳转的正确判据）**：
- Rebecca Traub：院系目录页只显示"在职"，看不出她刚从 CityU HK 回巢。ORCID Employment 给出完整轨迹 Murdoch(PhD) → Melbourne 2018-2022 → CityU HK 2024-02~2025-05 → **Murdoch 2025-10 至今**。
- 反过来也成立：院系页常见「人已离职但页面还在」，判断在职必须看最近一条 Employment 的起止日期是否为 `to present`。

---

## 2026-09-24 补充：QS 综合排名在兽医/农业方向的适用边界（重要）

**客户会问「为什么选了排名以外的学校」。** 回答前必须先把口径来源说清楚，再给精确数据，不要含糊。

### 两类「排名之外」，性质完全不同，不能混为一谈

| 类型 | 特征 | 代表作 | 处理 |
|---|---|---|---|
| **① 独立学科院校** | 不隶属任何综合性大学，**QS 综合榜根本不会收录**（不是"排名低"，是"不在同一个榜上"） | 兽医：Royal Veterinary College（伦敦）、TiHo Hannover、Vetmeduni Vienna、SLU、NMBU；另有音乐、艺术类院校同理 | 属于「专业强校」的本意，向客户说明时要点出"综合榜无此校" |
| **② 综合性大学但排名靠后** | 在综合榜上有名次，只是 >300 | Guelph（504）、Saskatchewan（378）、Murdoch（423）、NMBU（791） | **这才是真正超出客户原始口径的部分**，必须主动承认并让客户决定去留 |

### 兽医方向的实证（2026-09 刘艺佳案例）

- 独立兽医院校若按 QS 综合榜筛，会**系统性错杀该领域最好的学校**——RVC 在 QS 兽医学学科排名常年全球第 1–2，综合榜上找不到它。
- 因此选导时应同时查 **QS 学科排名（Veterinary Science / Agriculture）**，而不是只给综合排名。给客户交付时，两类院校要分开列，并标出"综合榜未收录"的原因。
- 本次 48 位中：QS 前 300 共 35 位（21 所），300 之外 7 位（4 所综合性大学），综合榜未收录 6 位（3 所独立兽医院校）。

### 标注纪律（客户选择「保留但标注」时的做法）

- 在 `备注` 末尾统一追加固定句式，避免与旧表述重复：
  - 有综合名次但超 300：`QS 综合排名 504（不在前 300 之内）。`
  - 独立院校：`该校为独立兽医院校，QS 综合榜未收录。`
- 写入前先正则清掉旧的「学校 QS…」表述，否则会叠加两次。
- 交付 HTML 的卡片头加徽章区分（前 300 绿 / 其外橙），客户一眼能筛。

---

## 通用纪律：用分页 API 判断「记录是否存在」时不要单次断言

**2026-09-24 实证**：用 Vika 分页接口（`pageSize=100&pageNum=N`）连续两次拉全表，先后得到 175 条与 176 条——**同一条查询在短时间内返回了不一致的记录集**。我基于其中一次做了「某条记录未写入」的判断，并向客户报告了一个并不存在的缺失（实际 48 条一条不缺）。

**规则**：
1. 断言行级存在性时，必须**交叉验证**：换 `fieldKey` 参数、换字段组合、或用 `recordId` 直接取，不要只凭一次搜索的零命中。
2. 优先用**恒等式校验**：`当前总记录数 = 原有条数 + 本轮新增条数`。本次 176 = 128 + 48，恒等式成立即说明无缺失；当时我看到 175 就应立刻意识到是分页问题而非数据问题。
3. 向客户报告「数据缺失」这类结论前，**至少复核一次**。缺失类结论一旦报错，会让客户对整批数据失去信任。

---

## 2026-09-24 「博士申请信息」列的正确填法（客户明确要求，务必遵守）

**客户原话：「博士申请链接需要是各个项目具体的申请链接，不要是全校统一的入口。」**

即：不要填 `https://www.ed.ac.uk/studying/postgraduate`、`https://grad.usask.ca/admissions/` 这类**全校总入口**，要填学生点进去就能看到该项目、并能申请的那一页。

### 各国博士项目的层级与命名规律

| 国家/地区 | 结构 | 项目页长什么样 | 实例 |
|---|---|---|---|
| **英国** | 按学科设研究学位（research degree），几乎每校都有学科级项目页 | `PhD in <学科>` / `<学科> PhD` | Cambridge `PhD in Veterinary Medicine`；Bristol `Veterinary Sciences PhD`；Glasgow `Parasitology PhD/MSc (Research)`；Liverpool `Infectious Diseases PhD` |
| **英国（牛津特例）** | 博士叫 **DPhil**，按系的项目命名 | `DPhil in <系名>` | Oxford NDM `DPhil in Clinical Medicine`（⚠️ IITM 项目已停招） |
| **澳洲** | 少数校按学科设专属 PhD（最好），多数是统一 PhD + Faculty 归口 | `Doctor of Philosophy – <学科>` 带 course code | Melbourne `Doctor of Philosophy – Veterinary Science (DR-PHILVET)`（最理想）；Massey `PhD Veterinary Science (118900)`；UQ/Murdoch/Adelaide/Sydney/Otago 为统一 PhD + 学院页 |
| **加拿大** | 按**系/所**设 graduate program 页，质量最高 | `<学科> PhD` / `MSc and PhD Thesis programs in <学科>` | Guelph `Pathobiology PhD`；Saskatchewan `Veterinary Microbiology M.Sc./Ph.D.`、`Vaccinology and Immunotherapeutics`（**独立跨院系项目**）；McGill 寄生虫所 `MSc and PhD Thesis programs in Parasitology` |
| **欧洲大陆** | 无统一项目页，走 **doctoral school / Promotionsbüro / 岗位制** | 结构化项目的官网页，或博士注册办公室页 | Bern `GCB PhD Program`（Dr. phil. nat.）；TiHo `PhD Programme "Animal and Zoonotic Infections"`；Vetmeduni `PhD One Health Doctoral Programme`；FU Berlin `Promotionsbüro` |
| **荷兰 / 比利时 / 挪威** | 岗位制，**先有导师和经费才有博士** | 院系 PhD track 说明页 + 招聘门户 | Utrecht 兽医学院 `phd-track`；Ghent `PhD at the Faculty of Veterinary Medicine`；NMBU `PhD Programme in Veterinary Science` |

**给客户交付时必须附一句体系说明**（否则学生会以为可以直接网申）：欧陆博士绝大多数是「先联系导师 + 经费/岗位先行」，不存在统一的公开申请系统；CSC 申请者的落地入口是各校岗位招聘页与 CSC 专项页。

### 四条实测坑（本轮全部踩到）

1. **`OneWayLink` 字段在 `fieldKey=name` 模式下返回的是关联记录的 recordId 数组**，不是显示值。用 `str(field)` 去匹配校名会全部失败，必须维护「recordId → 校名」反查表（学校主表导出后反转，外加本轮新建学校的 ID）。**症状：批量写入时大量显示"未映射"，但按人名匹配的那几条却成功。**
2. **反爬返回 403 / 202 ≠ 链接错**。本轮 4 条（Melbourne 403 Imperva、Otago 403 Cloudflare、NMBU 403、Alberta 202 Akamai）在浏览器可正常打开，地址规范正确。判定规则不变：**只有 404 才说明路径错。**
3. **独立学科院校没有按学科拆分的项目页**。RVC 是单一学院制，PhD 为全机构统一研究学位，不存在 `PhD in Pathobiology`；TiHo 的博士归 HGNI 研究生院下的三个结构化项目。遇到这类机构，填它最具体的那个博士入口即可，**不要为了"具体"而编造不存在的项目页**。
4. **同校不同院系必须分别填**。本轮 3 处：McGill 动物科学系 vs 寄生虫所；UQ QAAFI 动物科学中心 vs 兽医科学学院；Saskatchewan 兽医微生物系 vs 疫苗学与免疫治疗项目（后者是跨院系独立项目，Tikoo 是其主任）。**按人名映射比按校名映射更可靠**——先查 `BY_PERSON`，再回落到 `BY_SCHOOL`。

### 验证纪律

- 28 所机构 → 31 个唯一 URL（去重后）。**串行 curl 全部验证会超过 120s 前台超时被 kill**（exit 137），必须放后台跑。
- 验证脚本要**同时记录 HTTP 码与字节数**；字节数可与上一次的值比对，**若某条码为 000 但字节数与上一条完全相同，说明 curl 失败、读的是上一个残留文件**，需重测（本轮就出现 2 条假 000，重测均 200）。
- 交付 HTML 时把「博士项目」名称单独显示出来（徽章样式），链接放下面小字，这样客户一眼能看出是哪个项目而不是哪个学校。
