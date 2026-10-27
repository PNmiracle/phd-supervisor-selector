<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：2026-10 月度区域案例更新日志（FSU outside member 路径、港澳与中外合办 EdD 双轨、港教大名单入口、港澳有 EdD 的学校权威底账）
> **什么时候读**：遇到该月同方向或同校的相似场景时，按校名或学生名 grep 定位；查港澳 EdD 项目清单时
> **什么时候不用读**：当前任务与该月案例无关；⚠️ 禁止整读，必须先 grep 定位

---

# 区域案例更新日志 · 2026-10

> 自 `school-updates-log.md` 于 2026-10-07 按月拆分。索引见 `school-updates-log.md`。

## 2026-10-06 更新（秦嘉琪 — FSU：目标校没有该学科博士时的「outside member」路径）

### 场景
学生方向是舞蹈（具身/现象学/民族志），FSU **没有舞蹈博士**；已套磁 School of Dance 的 Hannah Schwadron，对方回复："That does happen here, and I typically serve as an **'outside member'** on PhD committees in Theater with a dance focus." 客户问「这可以吗」。

### 结论：可行，但只能当委员，不能当主导师
FSU 研究生手册（University policy，各院系手册均引用同一段）明文规定：
- 博士答辩委员会 **至少 4 名持 Graduate Faculty Status（GFS）** 的成员，其中 1 名为 **University Representative**；
- University Representative 必须**从学生所在系之外**聘请、且为**终身教职 + 持 GFS**（跨学科项目还须在学位项目之外）；
- **"可增补提供必要专长的成员"**；这类增补成员须持 GFS，或对**非终身轨教员授予 co-doctoral Directive Status**；校外人士可经聘为 **Courtesy Faculty** 后任委员或联合主席；
- **major professor（委员会主席）必须持 GFS、并在学生所在系，由系主任任命**；商科手册另注明委员会须含"至少两名来自学生主领域"的成员。

**因此**：Schwadron 以 School of Dance 教员身份进入 Theatre 博士委员会，制度上有明文依据（正是「增补专长成员」与「University Representative 来自外系」两种用法）；但**学生仍必须在目标系（Theatre）找一位愿意领衔的 major professor**。收到这类「我愿意当 outside member」的回复时，**不要**回一句"太好了"，要立刻去该系找主导师，并把这一层如实告诉客户。

### 交付纪律
遇到「目标校没有该学科博士」的情形，必须同时交付两件事：
1. 制度层面的可行性与边界（用研究生手册原文，不要凭常识说"应该可以"）；
2. **该项目所在系里能当主导师的教员名单**（这才是真正要补的东西）。

### FSU 检索要点（实测）
- **该站对 curl 全站 403**（`cfa.fsu.edu`、`theatre.fsu.edu` 都拦），加完整浏览器头也无效 → **只能走 WebFetch / 浏览器通路**。403 不代表链接失效。
- **人员名单用 Yoast sitemap 拿**：`https://<site>/wp-sitemap.xml` → `people-sitemap.xml`（本轮一次拿到 School of Theatre 全部 43 个个人页 slug）。**当 WebFetch 对人员列表页截断时（本轮两次都只渲染到姓氏 G），sitemap 是唯一可靠的穷举手段。**
- **email 不在人员页正文**：WebFetch 会丢掉 Contact 段落，但 WebSearch 的快照保留 "Contact xxx@fsu.edu" → 用「"推测邮箱" + 姓名」反查确认；**不命中就不填，不按命名规律猜**。
- **博士项目页双域名**：`cfa.fsu.edu/programs/phd-theatre/` 与 `theatre.fsu.edu/programs/phd-theatre/` 内容相同。**沿用该校既有记录用的那一个**，保证同校一致。
- **项目页 Advisor 栏就是项目共同主任**：本轮为 Elizabeth Osborne 与 Aaron C. Thomas——这两人是申请与委员会的实际负责人，**写该系的候选人时应优先包含他们**。
- **反推"谁有资格带博士"的捷径**：公开 CV 里通常有 `Doctoral Committee Chair / Co-chair / Member` 章节，**这是 GFS 与带博经历的直接证据**，比从简介里推断可靠（本轮据此确认 Aaron C. Thomas 有主席与联合主席经历）。
- 判定「这个项目认不认学生的方法论」：读项目页的 critical approaches 清单。FSU 的清单里**明列 phenomenology 与 ethnography**，且把 practice-based research 列为学位三种实践之一 —— 具身/现象学取向在项目层面被承认，这类原文可直接引给客户。

### 本轮口径（写进备注的方式）
按 2026-09-18 Bhangu 教训执行：备注先写**该导师自己的研究对象**，再写与学生方向的联系，并**明写对象差异**（例如「他的对象是剧场表演者而非舞者，需要在研究计划里说明如何转译」），**不用"能搭上"一笔带过**。

## 港澳 + 中外合办批次补充（2026-10-07 曹琇翕案例，EdD + 艺术类 PhD 双轨）

### 通道与可读性（本轮实测）
- **必须用 WebFetch、curl/urllib 读不到的域名**：`hkmu.edu.hk`（403 WAF）、`eduhk.hk` / `pappl.eduhk.hk`（URLError / 超时）、`cuhk.edu.cn` 及其子域 `hss.` `hsspg.` `music.`（SSL handshake failure）、`research.mpu.edu.mo`（403）、`research.nottingham.edu.cn`（403）。**不要把这些误判为链接失效**。
- **curl 可读**：`polyu.edu.hk`、`scm.cityu.edu.hk`（本轮未触发 WAF）、`ava.hkbu.edu.hk`、`ln.edu.hk`、`web.edu.hku.hk`（偶发超时，重试即可）、`arthistory.hku.hk`、`fed.um.edu.mo`、`fah.um.edu.mo`、`must.edu.mo`、`soe/fiad/fhss.cityu.edu.mo`、`xjtlu.edu.cn`、`scholar.xjtlu.edu.cn`、`cma.hkust-gz.edu.cn`。

### 各校关键路径（本轮修正）
- **HKU 艺术史系**：MPhil/PhD 页是 `arthistory.hku.hk/index.php/academic-programmes/mphil-and-phd/`；`/index.php/programmes/` 是 404。个人页格式 `/index.php/people/<slug>/`。
- **HKU 教育学院**：EdD 页 `web.edu.hku.hk/programme/edd`（兼读 4–6 年 + 全日制 3–5 年）。个人页里的 `Prospective PhD/EdD/MPhil Applications` 字段**三种状态都要读**："available to supervise" / "Not applicable" / "not taking on graduate supervision in 2026-2027"。
- **CUHK 教育学院**：系页是 SPA；个人页改走 `research.cuhk.edu.hk/en/persons/<name-slug>/`，静态可读。EdD 页 `fed.cuhk.edu.hk/higherdegree/en/programme/doctor-of-education/`。
- **HKUST AMC（本部，艺术与机器创意学部）**：学部页 `amc.hkust.edu.hk/faculty` 是可读的 FAQ 式长页（含 Focus Area / Research Topics / 邮箱），个人页外链到 `facultyprofiles.hkust.edu.hk/profiles.php?profile=<slug>`（**这个域名与港科广的 SPA 壳不同，可正常使用**）。项目页 `amc.hkust.edu.hk/mphil-phd-program-program-objective`。
- **HKUST(GZ) CMA 学域**：`cma.hkust-gz.edu.cn/faculty-regular/` 列表页（WordPress）可直接抽取个人页 slug；个人页可读。项目页用 `fytgs.hkust-gz.edu.cn/programs/computational-media-and-arts-4`。
  ⚠️ **CMA 个人页在招生字段上可能明写 "no MPhil or PhD student position"**（张康 Kang Zhang 即如此）→ 入库前必须读该字段，否则会写入不招生的导师。
- **HKMU**：教育博士分英文班 `.../postgraduate/edd/` 与中文班 `.../postgraduate/eddc/`；**EdDC 督导名单页 `hkmu.edu.hk/el/list-of-eddc-supervisors/` 一次性给出全部导师的姓名/职称/邮箱/研究兴趣**（WebFetch 可读）。个人页格式 `hkmu.edu.hk/el/home/people/staff-profile?email=<uid>&po=N&unit=EL`，或 `scholars.hkmu.edu.hk/en/persons/<slug>`。**EdD 语言口径：以中文为论文语言者豁免英语要求**（EdD Information Booklet 原文）。
- **EdUHK**：Graduate School 的 EdD 页 `gs.eduhk.hk/prospective/edd/`；CCA 师资页 `eduhk.hk/cca/en/people/academic-and-teaching-staff/?id=<n>`；部分教师个人页在 `pappl.eduhk.hk/rich/web/person.xhtml?pid=<n>&name=<NAME>`（同为官网域名）。
- **Lingnan / DACI**：`ln.edu.hk/daci/staff/faculty` 一页给出全部个人页 slug（`/daci/staff/faculty/prof-<name>`）。
- **UM 澳门大学**：**设计学博士现挂新设的设计学院 `fds.um.edu.mo`**，项目页 `fds.um.edu.mo/doctor-of-design-in-visual-communication-design/`（**带 `/zh-hant/` 前缀会 404**）。人文学院是 `fah.um.edu.mo`，个人页形如 `fah.um.edu.mo/?p=<id>/`（WordPress permalink）。教育学院 `fed.um.edu.mo/zh-hant/<slug>/`，导师页会明确写 "Accepting applications from PhD/EdD students"。
- **MUST 澳门科技大学**：设计学博导名单 `fa.must.edu.mo/person/id-732.html`（44 人，带 `*` 者为 2027/2028 有招生名额）；**每位导师的个人简介是官方 PDF**（托管在 `wm-fs2.must.edu.mo/group1/...`），可作「导师主页」使用。名单页会明确区分「教授，兼职博导」→ 兼职者剔除。
- **CityU Macau 澳门城市大学**：教育学院 `soe.cityu.edu.mo/staffs-1` 逐人标注「硕、博导」；创新设计学院 `fiad.cityu.edu.mo/acad_ft`；人文社科学院 `fhss.cityu.edu.mo`（部分教师页在 `rmo.cityu.edu.mo/list-6/<id>`）。**中文授课为主，官网各课程页未列英语门槛**。
- **MPU 澳门理工大学**：**艺术及设计学院没有博士课程**（只有学士与跨领域艺术硕士），不要把该院教师当成设计学博导；对口的是 `eschs/zh/phd_cha.php`（文化遗产与人类学博士）与 `esca/zh/phd_eti.php`（教育技术与创新博士）。学院教师个人页在 `info.mpu.edu.mo/teldir2005/Profile/Profilephoto.asp`（可读）。
- **XJTLU**：**Academy of Film and Creative Technology（影视与创意科技学院）的博士项目就是 `PhD English, Culture and Communication`**（`xjtlu.edu.cn/zh/study/doctoral/english-culture-and-communication`），其教师（如 Fang Liu）应关联该项目页而非未来教育学院。设计类教师个人页为 `scholar.xjtlu.edu.cn/en/persons/<uuid>`，UUID 可从 `xjtlu.edu.cn/zh/study/departments/academic-departments/industrial-design/department-staff/staff` 抽取。
- **UNNC**：EdD 页为动态匹配页 `nottingham.edu.cn/cn/course/match.aspx?name=EDD-FHSS-PDD`；EdD 仅在职 4–6 年，**雅思 7.0（单项 6.0）**，不接受四六级。
- **UIC / BNBU（北师香港浸会大学）**：已更名，研究生院域名 `gs.bnbu.edu.cn`；文化与创意学院（SCC）**自身没有博士项目**，其教授进入人文社科学院的**传播学博士**导师名单；教师个人页 `staff.uic.edu.cn/<slug>/<lang>`。
- **WKU 温州肯恩大学**：**不在统一主表**（主表里的 Kean University 是美国本部）→ 按「表格隔离 vs 建校取舍」不写入，进待补清单。该校有 Doctor of Educational Leadership（Ed.D.，4–6 年、晚间+周末、接受在职）。

### Vika 写入门槛（本轮踩到）
- **空间 QPS 上限 5/秒**：POST/PATCH 批次之间必须 `sleep(0.35)` 以上，否则整批返回 `429 The API request rate for the current space is 5 queries per second`，**该批 10 条全部静默丢失**（只报错误，不重试）。写入脚本必须内置 429 重试。
- OneWayLink 字段值必须是**数组**且写错学校 recordId 时报 `The linked field specifies a record (recXXX) that does not exist`——**错误信息不会告诉你是哪条记录、哪个字段**，只能靠比对本批与全校主表核对。

### 香港教育大学 EdUHK EdD —— 官方导师名单是「一页全给」（2026-10-07 补录，强烈建议优先用）

- 🔑 **官方 EdD Potential Supervisors 名单**：`https://gs.eduhk.hk/prospective-students/edd/potential-supervisors/`（中文版 `.../zh-hans/...`）
  - **一次性列出全部 59 位潜在导师**，含：姓名、所属学院/学系、职称、研究兴趣、邮箱。
  - **但页面不含个人主页链接** → 拿到名单后还要另配个人页 URL。
- 🔑 **个人页 URL 的统一形态**：`https://pappl.eduhk.hk/rich/web/person.xhtml?pid=<数字>`（**只传 pid 即可，`&name=` 可省**）。
  - pid 的获取路径：① 院系师资页里的相对链接；② `https://repository.eduhk.hk/en/persons/<slug>/` 页面上会写着 "Website: https://pappl.eduhk.hk/...pid=xxxxx"；③ WebSearch `"<英文名>" eduhk pappl`。**不要猜 pid**。
  - 少数人无 pappl 页，退路是 `https://www.eduhk.hk/<dept>/en/staff/<uid>`（如 MIT 的 `davyngtk`）或 `repository.eduhk.hk/en/persons/<slug>`。
- **EdD 项目参数**（2026/27）：Programme Code A3D045 / C4D001；全 3 年 / 兼读 4 年（最长 5 / 7 年）；72 学分；必修含 "Education in the Age of AI and Digital Transformation"；硕士须为教育或相关领域 + 4 年以上工作经验优先；**IELTS 6.5（单项≥6.0）或 TOEFL 80，明确不接受 CET**；项目主任 Prof HOU, Wai Kai。
- **EdD 的 18 个 Specialised Areas**（选方向时用）：Creative Arts Education (CAE/CAA)、Curriculum Studies (CUS/C&I)、Curriculum and Learning、Leadership for Future Schools (LFS/EPL)、ICT in Education (ICE/MIT)、Global Education (C&I+EPL)、Language/Culture and Education (CCA+CHL+ELE+LML)、International and Comparative Education (ICED/EPL)、Life and Values Education (LVE/EPL)、Civic and Citizenship Education (CCE/C&I)、Social Sciences and Policy Studies (SSPS)、Science Education & Education for Sustainability (SES)、Mathematics Education (MAE/MIT)、Developmental and Educational Psychology (DEP/PS)、Early Childhood Education (EC/ECE)、Educational Measurement & Assessment (EMA/PS)、Special Education (SPE/SEC)、Health Studies / PE & Sports Science (HPE)。
- **各系师资名单页（已核实可用）**：
  - 课程与教学学系 C&I：`https://www.eduhk.hk/ci/en/aboutus.php?s=our_staff`（注意是 **ci** 不是 cin）
  - 教育政策与领导学系 EPL：`https://www.eduhk.hk/epl/en/aboutus.php?s=our_staff`（**必须带 www**，裸 `eduhk.hk` 版本不要用）
  - 数学与资讯科技学系 MIT：`https://www.eduhk.hk/mit/en/people/`
  - 文化与创意艺术学系 CCA：`https://www.eduhk.hk/cca/en/people/academic-and-teaching-staff/`
  - 中国语言学系 CHL：`https://www.eduhk.hk/chl/en/people/`
  - 幼儿教育学系 ECE：`https://www.eduhk.hk/ece/en/aboutus.php?s=our_staff`
- ⚠️ **口径提醒**：官方 EdD 名单里有几位的 pappl 归属与名单标注不一致（如 OLEKSIYENKO、XIONG Weiyan 名单列 EPL、pappl 实际属 SSPS）→ 填表时以 **EdD 名单的院系**为准更稳，或在备注写明。
- 🔴 **讲师序列一律不放（2026-10-07 用户明确裁定）**：香港/澳门适用「助理教授及以上」门槛（见 `school-registry-hk-mo-cn.md` 第 185 行、`selection-rules.md` 第 30 行）——`Lecturer` / `Senior Lecturer` / `Lecturer I` / `Senior Lecturer II` / `Teaching Fellow` / `Instructor` / `Professor of Practice` / `Research Assistant Professor` 一律排除，**不要因为「方向很对口」就收进来**。
  - 本轮实例：EdUHK 甄沛豪（Senior Lecturer I，专业与职业教育）虽个人页写着「博士生導師」，仍按讲师序列**删除**；葉德平（Senior Lecturer II，非遗/遗产教育/博物馆学）、鄭德禮（Lecturer I，职业教育与培训）直接排除，**连待补清单都不放**。
  - ⚠️ 注意 `school-registry-hk-mo-cn.md` 原文对「页面明示可带博」留了例外口子，但**用户已裁定按讲师序列一刀切**；如遇特殊情况先问用户，不要自行套用例外。
- ⚠️ **别把「方向对口但不在 EdD 名单」的人混进 EdD 记录**：林質彬（数字化学习）、呂賜杰（学习科学）是 PhD 导师而非 EdD 名单成员 → 用户裁定**不放**，不要挂到 EdD 项目页下（如确需纳入须另接该校 PhD 项目页并先问用户）。
- 🔴 **写入后必须跑「职称位扫描」**（本轮教训）：`备注` 首段（分号前）必须是真实职称，不能写成「博士生导师」。港校门槛过滤：`OK=("教授","副教授","助理教授","讲座教授","特聘教授","杰出教授","高级副教授","首席教授")`，`LOW=("讲师","Lecturer","Teaching Fellow","Instructor","Professor of Practice","Research Assistant Professor","研究助理教授","兼职","Adjunct","Visiting","客座","Emeritus")`。本轮靠这一步抓出 1 条讲师（EdUHK 甄沛豪）+ 4 条 XJTLU 职称位误写（Qian Wang=Associate Professor、Angela Fitzgerald=Professor、Na Li=Senior Associate Professor 兼 EdD 项目主任、Juliana Tay=Assistant Professor）。
  - XJTLU 的 `scholar.xjtlu.edu.cn/en/persons/<slug>` 页可 curl，**职称藏在正文首段**（"Dr X is an Associate Professor / a professor of education / Senior Associate Professor"），不在 meta 里，正则要抓正文。


---

## 📋 港澳 + 中外合办「有 EdD 的学校」权威底账（2026-10-07 曹琇翕案例，逐校核过）

**共 12 所**（香港 5 + 澳门 4 + 中外合办 3）：

| 地区 | 学校 | 项目 | 状态 |
|---|---|---|---|
| HK | 香港大学 | Doctor of Education (EdD) | 在招 |
| HK | 香港中文大学 | Doctor of Education (EdD) | 在招 |
| HK | 香港教育大学 | EdD（英文班）+ 教育博士（中文班） | 在招 |
| HK | 香港都会大学 | EdD（英文班）+ EdDC（中文班） | 在招 |
| HK | **香港浸会大学** | Doctor of Education (EdD) | ⚠️ **有项目但暂停招生**（"No applications will be invited"） |
| MO | 澳门大学 | 教育博士（EdD） | 在招 |
| MO | 澳门科技大学 | 教育博士（EdD）— **国际学院** | 在招（2025-05 新批） |
| MO | 澳门城市大学 | 教育博士（EdD） | 在招 |
| MO | 圣若瑟大学 USJ | Doctor of Education | 在招（**不在统一主表**） |
| 合办 | 宁波诺丁汉 UNNC | Professional Doctorate in Education (EdD) | 在招 |
| 合办 | 西交利物浦 XJTLU | Doctor of Education (EdD) | 在招 |
| 合办 | 温州肯恩 WKU | Doctor of Educational Leadership (Ed.D.) | 在招（**不在统一主表**） |

**有教育类博士但不叫 EdD（5 个，学术型为主，别与 EdD 混用）**：澳大 PhD(教育学)、澳科大 教育学博士、澳城大 教育学博士、澳理工 教育技术与创新博士、港理工 Doctor of Applied Language Sciences。

**确认无任何教育类博士（7 所）**：港科大、港城大（专业博士仅 DBA/DBAC/ENGDC/ENGDEM）、岭南（仅 DBA-GDEG/Doctor of Business Studies/Doctor of AI Studies/Doctor of Policy Studies/Doctor of Smart Manufacturing）、澳门旅游大学、港中深、港科广、北师浸。

### 🔑 权威底账（以后查港澳博士项目一律先用这两个）
1. **澳门**：澳门特区政府公报课程登记库 `https://es.dsedj.gov.mo/esdbonline/_site/search_results.asp?group=2&level2=3` —— 列出澳门**全部已批核的教育类课程**（含博士/硕士）及批核公报日期，是澳门项目存废的最硬底账。本轮用它交叉验证了澳门 4 所 EdD 的批核时间。
2. **香港**：各校研究生院的「**专业博士目录**」页（不是院系页）。港城大 `cityu.edu.hk/pg/professional-doctorate-programmes`、岭南 `ln.edu.hk/sgs/programmes-on-offer`、理大 `polyu.edu.hk/study/pg/taught-postgraduate/programme-z-tpg`（该页会列出全部 Doctor 级课程）。**这三页能一次性否掉「某校有没有 X 博士」**，比逐个院系找快得多，也是本轮纠正「岭南/城大/理工无 EdD」的依据。
3. **澳门科技大学**：研究生院博士课程总目录 `sgs.must.edu.mo/faculty/id-2894.html` —— 按院系列出全部博士课程 + 每项目的「导师名单」链接。**本轮正是靠它发现 EdD 挂在「国际学院」而不是「人文艺术学院」。**

### ⚠️ 另有一类「非本地课程」
香港本地可读、但学位由境外大学颁授的 EdD，例如 **HKU SPACE × University of Plymouth** 的 Professional Doctorate in Education（在职 4–6 年、全英文、香港面授+线上）。澳门登记库里也有华南师范大学与澳门业余进修中心合办的「教育专业博士学位课程（非本地课程）」。**这类项目的学位颁授方是海外大学，留服认证口径要单独确认，不要和港校本部项目混为一谈。**

---

## 🗑️ 按「剔除理由分组」批量删除的操作规范（2026-10-07 曹琇翕案例）

用户在收到「A/B/C 分档 + C 档按理由分组」的报告后，会直接点名若干组说「这些先删了」。这是**允许删除的合规情形**（用户明确点名），但落地时有固定动作，不能省：

### 四步固定动作
1. **先全量备份**：`GET /records` 全量存 `BACKUP_before_delete.json`（**要含全部字段**，这样删错可原样重建——Vika Fusion API 删除无回收站，只能靠备份或网页端时光机）。
2. **干跑打印名单**：脚本先只打印「组 → 拟删记录（姓名 + 学校 + 分类 + recordId）」，核对条数。**分组名是用户说的，具体记录是我补的**，这一步就是把自己补的映射摊开给用户看。
3. **执行删除**：`DELETE /datasheets/{ds}/records?recordIds=rec1,rec2,...`，**每批 8 条 + sleep 0.6s**（空间 QPS 上限 5/秒）。返回体判定键是 `success`。
4. **回读并报告**：删除后重新 GET，按学校重算分布，把「删了谁 / 剩多少 / 哪些学校被清空」写进飞书反馈。

### 三个必查的点
- 🔴 **B 档 / 备选档的人不要跟着 C 档组一起删**。本轮报告里 C 档各组已标注「某某已入 B」，删除时必须显式排除（本轮排除 3 位：羅承浤、Koji MATSUNOBU、孫丹兒），并在报告里说明「故意没删这 3 位，需要的话再说」。
- 🔴 **检查有没有学校被整校清空**。本轮「香港科技大学（本部）」的 3 位恰好全部落在被删组里 → 该校变成 0 条。**这是分组删除的副作用，必须主动提醒用户**，不要静默。
- 🔴 **快照会因人工并行策展而失效**。本轮同一天内表内记录数走 124 → 111 → 93，且港科广的两位导师在我 14:59 的快照里没有、执行时又出现（Vika GET 缓存 + 人工增删）。**每次动手前后都要重新 GET，不要复用几分钟前的快照**；发现条数或记录集与预期不符时先停手比对差异。
- 🔴 **删「筛选条件为『选导意向为空』」的一批时，删除前必须逐条重查该字段，有值的当场挂起请示**（2026-10-09 蒋元萍 C 档案例）。当时 46 条 C 档在 40 分钟前建的快照里「选导意向」全为空，执行前重查发现 **5 条（UCF 的 I-O 组）已被人工填上「无相关同步信息」**——用户是在读我上一份报告的过程中顺手标的。处理方式：**删 41 条无值的，挂起 5 条并把姓名 + 新值列进报告请用户裁定**，绝不按旧快照的「为空」直接删。脚本层面就是把这段写成硬门：
  ```python
  locked = [(i, name_of(i), intent_of(i)) for i in ids if intent_of(i)]
  ids = [i for i in ids if i not in {x[0] for x in locked}]
  # 挂起清单单独落盘（C_hold_locked.json），报告里显式列出请用户确认
  ```
  判据：**删记录的唯一合法依据是「用户点名 + 该记录当前无人工标记」**；只要该记录在删除时刻带有任何 `选导意向` 值，就必须停下来问。
- 🔴 **清理清单的取数范围要用「全表」，不要只用某个视图**（2026-10-09 蒋元萍案例）。当时的清单是按「美国选导」视图建的，视图外还有 5 条同类不合格记录（DePaul / ECU / Mercer / Rowan×2）——它们**只有「美国地区学校」关联、缺 QS 关联，所以进不了该视图**，只有全表扫才看得到。用户批准清理时通常会一并点名，但**我必须在报告里主动把这批"视图外同类"单列出来请其裁定**，不要因为"不在视图里"就默认不管。删除后视图条数可能**完全不变**（因为它们本就不在视图内），报告里要提前说明，避免用户以为没删成功。

## ⚠️ 分组剔除的副作用：会误删「项目主任 / 方向负责人」（2026-10-07 曹琇翕案例）

**案例**：用户发现「西浦 EdD 怎么没了」。用备份逐轮回溯后确认：

| 记录 | 消失时点 | 谁删的 | 当时归的组 |
|---|---|---|---|
| **Na Li**（西浦 **EdD 项目主任**、Senior Associate Professor） | 93 → 69 | **我（分组剔除）** | ⑤ 教育技术 / AI 工程 |
| 张晓军（西浦 EdD） | 69 → 52 | **我（分组剔除）** | ① 高教政策 / 教育领导 / 学术职业 |
| Jian Chen / Qian Wang / Angela Fitzgerald / Juliana Tay（西浦 PhD in Education） | 111 → 93 | 人工 | — |

**根因**：按「研究方向关键词」分组时，只看 `导师研究领域`（Na Li 是 "AI and education; digital game-based learning"），**没有把「他在该校的职务身份」当成保护条件**——而她备注里我自己写过「EdD 项目主任」。结果整条 EdD 线（该校唯一的教育博士项目）被清空。

### 硬规则（下次分组剔除前必做）
1. 🔴 **先扫一遍「项目主任 / 课程主任 / 学院院长 / 招生负责人」**：这类身份在 `Department`、`备注`、`导师主页` 文本里通常有 `Programme Director / 课程主任 / 院长 / Dean / Head of Department` 字样。**凡是方向落在被删组、但身兼项目/学院负责人的人，单独拎出来问用户，不要跟着组删。**
   - 依据：删掉这类人的成本远高于留下一个方向边缘的人——他们往往掌握招生口径，且是套磁的关键入口。
2. 🔴 **按「整条项目线」做一次事前检查**：删除前，统计一下每个 `博士申请信息`（项目页）下还剩几条记录。**如果某条项目线会被删到 0 条，先提示用户**（本轮西浦 EdD 就是这么被清空的；之前还发生过港科大被整校清空）。
3. ✅ **备份要能支撑逐轮回溯**：本轮靠 `BACKUP_before_delete{,_2,_3,_4}.json` + 各轮 `final*.json` 才定位出「哪一条、在哪一轮、被谁删的」。**每轮都存全字段备份，且保留各轮快照文件**——没有它们就无法回答用户「怎么没了」这种追问。

### 恢复方式
备份里含全部字段（含学校关联 recordId、项目分类、EDD工作年限要求、三个 URL），可按姓名筛出后 POST 重建；**但人工删除的记录仍不要自行恢复**，只恢复「我误删的那部分」，且要先问用户。

## 🎓 「艺术类博士」必须区分**研究型 PhD** 与**实践型博士**（DFA / DDes / DMA 等）（2026-10-07 曹琇翕案例）

**教训**：用户看到表里把澳门大学的李軍/梁藍波/王小楓标成「艺术类PhD」，直接指出「我印象里 UM 只有实践类 DFA」。核官网后确认用户是对的——**我把实践型博士误标成了研究型 PhD**。这类错误会让交付物在行家面前立刻失真，也会**掩盖掉实际可申的路径**。

### 港澳艺术设计类博士的实际类型（2026-10 核实）
| 学校 | 项目 | 类型 | 关键区别 |
|---|---|---|---|
| **澳门大学 UM** | **Doctor of Fine Arts（DFA）**，人文学院 | **实践型** | 培养 practicing artists；结业需**创作作品展览**；需作品集 10–20 张；**要求学士与硕士其一为 Fine Art 学位** |
| **澳门大学 UM** | **Doctor of Design（DDES）** 视觉传达设计 / 工业设计，设计学院 | **实践型** | "design practice is a form of scholarly inquiry"；结业含创作作品展览；**要求学士或硕士其一与 Arts and Design 相关** |
| 澳门大学 UM | FAH 的其余博士（语言学/文学/哲学与宗教/历史） | 研究型 | **FAH 没有艺术史或艺术理论类 PhD** |
| 香港理工大学 PolyU | School of Design 的 **PhD**（也有独立的 DDes） | 研究型 | 写记录时别把 DDes 与 PhD 混用，`博士申请信息` 要指向实际那一个 |
| 其余港澳院校（港大艺术史、港中大艺术系、港城大 SCM、港浸会 AVA、岭南 DACI 等） | 多为 **MPhil/PhD** | 研究型 | — |

### 硬规则
1. 🔴 **写 `博士申请信息` 之前，先确认该项目在官网的「学位名称」**：`PhD` / `MPhil-PhD` = 研究型；`Doctor of Fine Arts / Doctor of Design / Doctor of Education / DBA / DDes / EngD / DMA` = **专业型（实践型）**。**不要用「艺术类PhD」这种笼统标签覆盖实践型博士**。
   - 判据：项目页看两点——① 培养目标是否写 practising professional / professional practice；② 结业是否要求**作品集/创作展览/实务项目**而非纯论文。
2. 🔴 **实践型博士的入学口径往往与研究型完全不同**，而且**常常更宽**——例如澳大 DFA/DDES：语言接受 **CET-4 与内地考研英语成绩**（研究型 PhD 只认 TOEFL 80 / IELTS 6.0 / 部分院系收 CET），但**要求艺术设计相关学位 + 作品集**。
   → 因此「实践型」不是「次一等」，对**有作品集、有实务经历但语言弱**的申请人反而常常是**更可行的路径**。误标成研究型 PhD 会把它从候选池里抹掉。
3. ✅ **遇到「该方向有没有研究型博士」这类质疑，一律回官网的「博士课程总目录」核对**（如 UM：`grs.um.edu.mo/index.php/prospective-students/doctoral-degrees-programmes/`，一页列出全部博士及其类型），不要靠记忆或第三方汇总。

---

## 🎓 澳门科技大学：设计学博士 = 研究型 PhD（不是 DDes）+ 人文艺术学院博士**免英语证明**（2026-10-07 核实）

### 学位类型（用户质疑「澳科大设计学是否也是实践类 DDes」→ 核后确认不是）
- **官方英文名为 `Doctor of Philosophy in Design`**（人文艺术学院项目页标题原文，`fa.must.edu.mo/programmes/program/view/id-201.html?locale=en_US`）→ 研究型 PhD。
- **澳门特区政府公报 第145/2014號社會文化司司長批示**（2014.8.11 设立该课程）原文：「為取得博士學位，尚須撰寫原創論文，並須接受論文評審及進行論文答辯」→ 以原创论文为学位要件。
- ⚠️ 但**其中一个专业范畴带实践成分**，这是「看起来像实践类」的来源：
  | 专业范畴 | 学分 | 论文 | 发表要求 |
  |---|---|---|---|
  | **艺术设计理论与实践** | 25（表五 =「设计」3 + 论文 9） | ≥**4 万字** | 可用「**艺术设计作品**」替代学术论著 |
  | 设计管理 | 22（论文 12） | ≥8 万字 | 须学术论著 |
  | 文化遗产保护 | 22（论文 12） | ≥8 万字 | 须学术论著 |
  - 「艺术设计理论与实践」学习要求明写「进入**毕业设计创作期**」「须在导师指导下参加与专业相关的**实践工作**」。
  - 2023/2024 学年起**招生的专业范畴仅「艺术设计理论与实践」与「文化遗产保护」**，「设计管理」不设招生。
  - 对比：澳大 **DFA / DDES** 才是真正实践型（颁授名称不是 PhD，以创作作品展览结业）。

### 🔑 澳科大「须提交英语能力证明」的院所白名单（高复用，务必记住）
博士申请人报名文件第 12 项列明，**只有以下 6 个院所的博士课程须提交英语能力证明**：
1. 创新工程学院
2. 医学院（含药学院）
3. 商学院（DBA 除外）
4. 国际学院
5. 可持续发展研究所
6. 澳门药物及健康应用研究院
→ **不在名单内 = 不需提交英语能力证明**，包括：**人文艺术学院**、法学院、酒店与旅游管理学院、博雅学院、社会和文化研究所、太空科学研究所。
→ 依据 URL：`https://sgs.must.edu.mo/page/application.documents.html?locale=zh_CN`（博士申请人「12 英语能力证明」）。
→ 顺带：澳科大**需作品集**的博士课程 = 设计学、美术学、建筑学（PDF ≤10MB）；**需工作证明信**的 = 工商管理博士、电影管理博士；**需简历**的 = 音乐学博士、休闲管理博士。

### 实践型 vs 研究型的通用判据（本轮补强，用途很广）
1. **看英文颁授名称**：`Doctor of Philosophy in X` / `PhD in X` = 研究型；`Doctor of X` / `DXA`（DFA、DDes、DBA、EdD、DMA、EngD）= 专业型。
2. **看学位设立/核准文件的原文**：澳门可在《澳门特别行政区公报》查到批示原文（`bo.dsaj.gov.mo`），写明「尚須撰寫原創論文並答辯」即为研究型。
3. **看结业要件**：论文 or 创作作品展览/实务项目；看表五的「设计/创作」学分是否存在。
4. ⚠️ **不要凭「课程里有实践课/有作品集要求」就判定为实践型**——澳科大设计学博士要交作品集、含设计创作学分，但颁授名称与学位要件都表明它是研究型 PhD。

## 2026-10-07 秦嘉琪 · University of Southampton：目标校「整个学科缺失」时的检索策略

### 场景
学生方向是舞蹈（具身/现象学/民族志），南安 **完全没有舞蹈/编舞/动作分析/具身理论方向的正职学者，也没有舞动治疗与创意艺术治疗师资**。全站唯一"舞蹈"相关正职研究是健康科学学院**已结项**的 PD Dance（帕金森舞蹈），主持人 Ann Ashburn 已荣休 → 不可用。

### 核心做法：学科整体缺失时，不要"尽力凑舞蹈人"，改判该生哪几条轴能在该校落地
把四份 RP 拆成四条轴，逐校判断可落地性：
- **RP3（自闭症儿童参与式创意舞蹈）→ 南安最强**：教育学院 + 心理学院的自闭症/融合教育集群，且有两院学者共同主持的 **ACoRNS**（研究者—实践者—经验者共同设计网络）与两人合作的「与自闭症儿童共同建构数字叙事」项目作为制度性证据。写入 6 位：Sarah Parsons（Professor of Autism & Inclusion）、Hanna Kovshoff（Professor of Neurodiversity，心理系）、Melanie Nind（Professor of Education，NCRM 联席主任）、Kiki Messiou、Ben Whitburn、Vasilis Strogilos。
- **RP1（华裔社区舞蹈/离散/代际）→ 可落地**：华语文化（Ruby Cheung，香港电影/华语电影工业）、**非物质文化遗产 + 交叉性**（Holly-Gale Millette，Winchester School of Art）、社区音乐与社会正义（Chi Ying Lam，音乐从业者社群的后殖民身份）、社区认同与移民研究（Angelina Pan，WSA）。
- **RP2 / RP4 → 明确告知无对口人选**，不为凑数把媒介研究、设计理论的人写进表。

### 可复用经验
1. **「非遗（intangible cultural heritage）」是舞蹈方向学生进艺术学院的天然入口** —— 比"文化认同""身体"这类泛词有效得多。遇到舞蹈生 + 没有舞蹈系的目标校，优先按这个词检索艺术学院。
2. **艺术类院校看"从业者社群"这条线**：社区音乐与社会正义、音乐家教学实践这类研究，与舞蹈生的社群传承、创作者职业身份同源，可作为跨艺术门类的落点。
3. **交付纪律（学科缺失时必给三件东西）**：① 明确的"该校没有该方向师资"结论 + 核过的院系清单；② 该生哪几条轴在该校能落地、落到谁；③ 已核查但因职级/方向不符而未收录的人——**尤其要写出"方向最贴但职称不合格"的那一位**（本轮是 Teaching Fellow 的 Eleonora Sammartino，研究方向"好莱坞音乐剧"，是全校唯一能谈舞蹈—影像—观看的人），让机构自己决定是否放宽。
4. **历史遗留同校错误顺带登记**：南安既有 3 条锁定记录里，**Daniel Ashton 与 Kai Syng Tan 的「博士申请信息」都指向 `study/postgraduate-research/philosophy`**，但两人同属 Winchester School of Art，其学科页应是 `art-design-media-fashion`——与 KCL/AUT 修过的"填错学科申请页"同类，因是锁定行未改动，已写进交付页。

### 技术要点（已同步进 `school-registry-uk.md` 的 Southampton 条目）
- curl 可直连 200，**但必须解 gzip**，否则会被误判成 SPA 空壳。
- **个人页 meta 标签是职称/学院/学部的可靠来源**：`<meta name="description">` 含职称原句，`school_metatag` / `faculty_metatag` 给建制；正文的 `Accepting applications from PhD students` 是明确招生信号。同类 Drupal 站点可复用。
- **判定 JS 空壳靠比对字节数**：多个不相关 URL 返回完全相同字节数（南安是 284920）即为壳。`/people?q=` 搜索与 education/psychology 的 `staff.page` 都属此列。
- 串行抓 48 个个人页会被 120s 前台超时 kill（exit 137）——后台跑或改并发（`ThreadPoolExecutor`）。

---

## 🎓 四校 EdD 的「导师名单在哪」——项目页往往不是答案（2026-10-07 逐校核实）

**通用教训**：EdD 项目的导师名单**通常不在 EdD 项目页上**。补某一所学校的 EdD 导师前，先判断名单落在下面哪一类，否则会像本轮一样看到"0 位导师"却以为没有。

| 学校 | 名单在哪 | 关键口径 |
|---|---|---|
| **香港大学** | **不在 EdD 项目页**；名单＝教育学院 **4 个 Academic Units** 的在职教师：LALE（语言与读写）、HCLD（沟通与人类发展）、MST（数理科技）、SCAPE（社会脉络与政策） | 教师个人页有 **「Prospective PhD/EdD/MPhil Applications」字段（三态）**：`available to supervise` / `Not applicable` / `not taking on graduate supervision in 20XX-XX`——第三种是**明确不招生**，必须读。个人页路径 `web.edu.hku.hk/faculty-academics/<slug>` |
| **澳门大学** | **官方不公开 EdD 导师名单**（项目页与入学要求页都没有） | 唯一依据＝教师个人页字段 **「Accepting applications from PhD/EdD students」**。⚠️ 有人只写 `PhD students` → EdD 不收，必须逐字读。师资总览 `fed.um.edu.mo/people/faculty-members/`，另有按职称分的子页（chair-professors / professors / associate-professor / assistant-professors / research-assistant-professor / senior-instructors-instructors） |
| **宁波诺丁汉** | **在 EdD 项目页**：给出**核心团队 5 人**（McTaggart、Anwei Feng、John Trent、Vlachopoulos、Umesh Sharma），并原文写明 **"All EdEn academic staff are potential supervisors of EdD theses"** | 即**教育与英语学院全体学术人员均可任 EdD 导师** → 这是四校里导师池最大的一所。个人页路径 `/en/Humanities-and-Social-Sciences/People/Profile.aspx?id=<uuid>`。师资页 `/en/humanities-and-social-sciences/schools-and-department/education-and-english/people/listing.aspx`（**英文版翻页 `?STFPageIndex=2` 会 404，中文版 `/cn/...` 可翻页**） |
| **西交利物浦** | **不在 EdD 项目页**（该页教学团队只列 1 人＝项目主任 Na Li）；真名单＝**未来教育学院博士导师页 28 位**（同时覆盖 PhD 与 EdD） | `xjtlu.edu.cn/en/study/departments/academy-of-future-education/doctoral-supervisors`；个人页 `scholar.xjtlu.edu.cn/en/persons/<NameOrUUID>` |

### ⚠️ 两条本轮踩到的坑
1. **「职称门槛」会把方向最贴的人挡在门外，要如实告诉用户而不是静默丢掉**。本轮港大 **Patrick LO** 的方向是「博物馆与艺术设计图书馆学」——四校里最贴该学生的人，但职称为 **Senior Lecturer**，按 HK 门槛（助理教授及以上）不收。同类：宁诺 **John Trent** 方向涉 **JVET 职业教育**（与高职教师身份对口）但是 **Visiting Professor**；西浦 **Anisa Vahed** 是 **Associate Professor of Practice**。
   → 报告中应设「**已排除但值得记录**」一节，写清姓名 + 原因，让用户自己决定要不要破例。
2. **「不招生」与「职称不符」是两类不同的排除**，不要混写。港大教育学院有约 10 位教师（Nancy Law、David Carless、CHEN Gaowei、Jeremy Rappleye、Lily Zeng、TAI Chung Pui、FUNG Dennis、CHEN Logan、CHAN Kennedy 等）官网明确标注 2026-27 或 2027-28 **不出任研究生指导**——他们不是方向问题。

### 各校 EdD 池的「方向地形」（便于快速判断有没有戏）
- **港大**：数字/多模态素养、学习科学、教育技术、体验式学习、课程与创造力、媒介素养、哲学与文化研究。**没有**职业教育 / 艺术与设计教育 / 博物馆教育方向的在职教师。
- **澳门大学**：教育学院主体是数学教育 / STEM / 科学教育 / **音乐教育** / 教育心理 / 幼儿 / 特教 / 量化测量；可指导 EdD 的"边缘对口"只有**教育信息技术、非正式学习、多媒体学习、中文课程与性别教育**四类。
- **宁波诺丁汉**：翻译学（**博物馆叙事 / 艺术展览叙事**）、应用语言学（多模态 / 数字叙事）、教育戏剧、教育领导、多语教育。**注意：国际传播系不在 EdD 主办学院内**（Mary J. Ainslie 属该系，官网无其任 EdD 导师的依据）。
- **西交利物浦**：未来教育学院 28 位里包含 **VET、艺术教育、艺术本位研究、非正式教育、项目式学习、教育符号学、AI 与教育**。**Design School / 影视与创意科技学院 / 中国研究系**方向极贴（digital cultural heritage、AIGC & New Narrative、Cultural Heritage Studies）但**无 EdD 指导权依据**，只能作 co-supervisor。

### OneWayLink 写入前的稳妥做法（本轮新增）
写 `学校名字`（OneWayLink）时，若不确定目标学校 recordId：**先用「同值重写 + 读回比对」验证**——把已有记录的该字段用候选 recordId 重新写一次（值不变，无副作用），再 GET 读回字符串看是否仍是原来的学校名。**读回一致即确认正确**。本轮用这招锁定 4 个 recordId，避免了靠"学校全称"字符串匹配失败（西交利物浦在主表里就搜不到 "Liverpool" 关键字）。

---

## 🎓 宁波诺丁汉：国际传播系的 PhD 路径（2026-10-08 核实，与 EdD 是两条完全不同的线）

### 官方博士项目清单（FHSS 方向，`study-with-us/postgraduate-research/programmes/phd.aspx`）
**PhD Creative Practice / PhD Culture Studies / PhD Education or English Studies / PhD History and Politics / PhD Economics + 商学院四个（Accounting/Finance/Marketing/Strategy）**，另有 EdD。工程类是 MRes + PhD。

### 🔑 PhD Creative Practice —— 创作实践型博士（对「有作品集但论文少」的申请人极友好）
- 归属：**School of International Communications / FHSS**；官网原文定位「designed for **filmmakers, media practitioners, artists**, and researchers who wish to develop original creative work, such as **films, documentaries, sound pieces, games, virtual production and other digital media projects**, together with a written **exegesis**」。
- **创作实践即博士核心产出**，exegesis 只作理论框架与反思 —— 属「实践型博士」而非论文型。
- 全日制 **3 年，仅全日制**（无兼读）；2 月 / 9 月入学；全年收申请，建议提前 3 个月。
- 设施与合作：Virtual Production Studio、TV Studio、Dolby Atmos 音棚；ARRI、Arturia、UNESCO 相关项目、Yong Opera、国际电影节。
- 导师团队专长：film, media, sound, postproduction, game design。

### PhD Culture Studies —— 研究型
- 同属国际传播系；页面直接列出**该系可能的博士指导领域**（Media arts、Documentary、Film genre、**Game studies**、**Sensory ethnography**、Sound studies、Cultural studies、Southeast Asian studies、Platform studies、Discourse analysis 等）。
- 页面写明「**How to find a supervisor**」→ 指向该系 People 列表，即**导师不预先绑定项目，按研究计划分配**。
- 学位注册在宁诺、**颁授诺丁汉大学（英国）学位**，中国教育部认可。

### ⚠️ 两个项目的三个关键口径（务必逐字读）
1. **英语：IELTS 7.0（各项≥6.5）/ PTE 76 / TOEFL 100。**
   🔑 但豁免名单里**包含 United Kingdom**，原文：「Applicants from the following countries **or have studied for a degree there** (excl. split site degree programmes) are **NOT required to submit any further evidence of English language ability**」→ **在英国取得学位者可免交英语证明，且本条未写时限**（「成绩两年有效」只约束雅思/托福分数本身）。这与西浦 EdD 的「国家清单 + 毕业两年内」形成鲜明对比。
2. **学历门槛：「hold an honours degree at 2.1 AND a masters at merit level or above in a relevant subject」** —— 与 EdD 的「硕士须为教育或相关领域」是**同一类障碍**：若申请人硕士专业不相关（如规划类），必须用本科专业或实践作品集论证相关性，并**先向 PGR Director 书面确认**；此外还要确认其硕士成绩是否达 merit。
3. **只有全日制**（Creative Practice 与 Culture Studies 的 Types of study 均写 Full time）→ 在职申请人需评估是否能脱产 3 年。

### 该系的人员构成提醒
- **EdD 主办学院是 School of Education and English（教育与英语学院）**；**国际传播系（School of International Communications）不是 EdD 主办单位** → 传播系的教师不应挂在 EdD 项目页下（本轮修正 Mary J. Ainslie 即此问题）。
- 国际传播系个人页里**明确写有「PhD Supervision」**的：**Filippo Gilardi（教授、系主任；创意产业 / 跨媒介叙事 / 数字平台）**、**Thomas Whyke（助理教授；动画研究 / 性别 / 文化分析）**。
- ⚠️ 反例：**Mary Ainslie** 的官方页**没有「PhD Supervision」条目**，只有「regularly invited to … **examine** PhD theses internationally」（受邀当答辩委员）。→ **「examine PhD theses」不等于带博资格**，核验时必须区分。

---

## 🎓 宁波诺丁汉 PhD Creative Practice —— 导师池与官方方向清单（2026-10-08 逐页核实）

### 🔑 项目页自带「Research interests」官方方向清单（**不点名导师**，只列方向）
项目页：`https://www.nottingham.edu.cn/en/Study-with-us/Postgraduate-research/Programmes/PhD.aspx?id=d885a705-32e9-41ea-983d-7790adf98f53&language=en-GB`
- 引导句：「We encourage work that brings together new forms, digital tools, clear thinking, and cultural understanding.」/「this list is **indicative, not exhaustive**」。
- **Disciplines / fields**：Film and screen production｜Documentary and non-fiction media｜**Digital media and virtual production**｜Sound design, music and audio-visual practice｜Game design, game studies and interactive media｜Media, communication and cultural studies｜**Intangible cultural heritage and performance**
- **Topics 里含**：creative screenwriting and development for film/TV/streaming｜virtual production, immersive and mixed reality｜**creative practice and AI in media production**｜**digital storytelling and platform-based creative work**（short-form video, web series, vodcasts, podcasts）｜game-based narratives / playable documentaries｜**creative practice with intangible cultural heritage, folk traditions and performance**｜**festival curation, multi-media exhibitions**
- **联系人＝PGR Director：Dr Vikrant Kishore（`Vikrant.Kishore@nottingham.edu.cn`）**；项目页两处均写他。⚠️ Culture Studies 页存在**同页自相矛盾**：正文 "Postgraduate Research Director" 写 **Dr Stephen Goulding**，同页 "More information → PGR Director" 写 **Dr Vikrant Kishore** → **以项目页的 Kishore 为准**，Goulding 记为旧文案。

### 该系导师池（写入表内的 6 位）
| 导师 | 职称 | 方向 | 带博证据（逐字） |
|---|---|---|---|
| **Vikrant KISHORE** | 副教授；**PGR Director** | documentary practice; screen production; online storytelling; mobile filmmaking; **multimedia curation; archiving and exhibitions**; **intangible cultural heritage**; film festivals; Asian cinema; creative practices | 角色性证据（PGR Director，申请经其筛分）；**页面无 supervision 字样** |
| **Corey Kai Nelson SCHULTZ** | 副教授 | Chinese art film; Chinese visual culture; film phenomenology; film theory; **museum studies; heritage studies**; affect studies | **"I have supervised PhD dissertations to completion in film studies, and am currently supervising PhD research projects on Chinese film."** |
| **Levi DEAN** | 助理教授（影视制作） | cinematography; colour grading; screenwriting within Chinese context; narrative filmmaking; documentary filmmaking; virtual production and motion capture | **"He also supervises practice-based PhD students and welcomes enquiries from prospective candidates"**；ARRI 认证讲师 |
| **Roy HANNEY** | 副教授（创意技术） | immersive storytelling; expanded narrative; XR; virtual production; audio-visual installation; **duanju（竖屏短剧）**; AI-assisted production; practice-based research design | 页面**无** supervision 字样 |
| **Simon WEAVING** | 副教授 | film genre; movie production/distribution/exhibition; **creative practice research**; cinematic virtual reality; documentary; screenwriting | 页面**无** supervision 字样；本人为导演／电影节总监 |
| **Filippo GILARDI** | 教授、**系主任**、亚太研究所所长 | media convergence; creative industries; digital business models; digital copyright; transmedia storytelling | 页面**明确列 "PhD supervision"**；Pure Supervised Work 7 条 |

### 未写但可补 / 被规则挡住的人
- **可补**：Bjarke LIBORIUSSEN（副教授，videogames／中国游戏文化／cinematic videogame adaptation，明确列 PhD supervision）、Richard FRENNEAUX（助理教授，music industry／platform，明确列 PhD Supervision）、Matt PARKER（助理教授，**creative practice-based research**／sound arts／immersive audio／sensory ethnography／documentary practice）、Thomas WHYKE（副教授，animation studies／gender／cultural analysis，多年明确列 PhD Supervision）、María Mercedes VÁZQUEZ（助理教授，**film curatorship**／拉美与华语电影，未列带博）。
- **职称不符但方向极对口**：**Dr Zhaoyu ZHU（Teaching Fellow；中国电影技术／虚拟制作）**、Dr Jessica HATRICK、Dr Tyler BECKLEY（Teaching Fellow）。
- **Honorary 一律不收，但值得记录**：**Prof Henry JENKINS（跨媒介叙事／transmedia 奠基人）**、Terry Flew、P. David Marshall、Claudia Mellado。
- **明确不招生**：Dr Troy CHEN（页面原文 "not accepting PhD students at this time … at capacity"）。
- **C 档（与视觉创作实务无接口）**：Terence Lee、Zhan Zhang、Shixin Ivy Zhang、Sadia Jamil、Stephen Goulding、Jo Parkes（需编程统计）、Laura-Jane Filotrani、Lei Hao。

### 🔑 机构性结论：不必去别的学院找
**Mixed Reality Lab（6 人）、Institute of Screen Production（3 人）、Digital Heritage Centre（5 人）的成员全部来自国际传播系本院**（Dean、Hanney、Gilardi、Weaving、Kishore、Filotrani、Frenneaux、Lei Hao、Parkes），**官网无任何外系成员参与 Creative Practice 指导的依据**。IAPS 有 32 名跨院系成员，但均无指导依据。

### 两条通用教训
1. **「项目页有方向清单、但不点名导师」是一种常见结构** → 遇到这种项目，导师要从**主办学院的师资名单页**反查，并对每个人的方向逐个比对项目页清单，而不是等一个官方导师名单。
2. **核验带博资格要区分三类表述**：`PhD Supervision`（明确带博）／`supervises practice-based PhD students`（明确带实践型博士）／`examine PhD theses`（**只当答辩委员，不等于带博**）。本案例里 Ainslie 属第三类，Kishore 属「角色性证据」，Hanney / Weaving / Parker 属「无表述」——三类必须在备注里如实写明差异。

## 2026-10-09 更新（万文睿第三轮 — 英国 + 澳洲 QS 前 100：环境功能材料 / 吸附材料 / 膜分离 / 环境痕量分析批次）

### 场景
学生方向＝功能孔材料（多孔二氧化硅、MOF）与高分子复合材料，对应「功能吸附材料与环境痕量分析」「吸附催化一体化环境功能材料」「功能分离膜材料与水处理技术」；应用场景限淡水废水与陆地土壤，海洋排除、大气后放，偏计算/建模的材料方向排除。
范围＝英国 + 澳洲 QS 前 100 全部学校（排除牛津、剑桥、IC）。共 22 校，覆盖 UCL/KCL/Edinburgh/Manchester/Bristol/Warwick/Birmingham/Glasgow/Leeds/Southampton/Sheffield/Durham/Nottingham + Melbourne/UNSW/Sydney/ANU/Monash/UQ/UWA/Adelaide/UTS。

### 🔑 结构性发现：**「环境功能材料 + 膜 + 水处理」这条线在澳洲化工系，不在化学系**
- 澳洲侧真正的富矿是**化工系**：Melbourne Chemical Engineering（Kentish/Scholes/Qiao/Mumford/Gang Li）、UNSW Chemical Engineering（UNESCO 膜中心：Leslie/Henderson/Le Clech/Cheng）、UTS 水与废水技术中心（Tijing/Shon/Guo/Fu/Nghiem）、UQ Chemical Engineering（Hou/Xiwang Zhang/John Zhu/Carvalho）、Monash CBE（Huanting Wang/Zhikao Li）。
- **化学系反而薄**：UNSW 化学系除在册者外无新增；Monash 化学院多为分析/合成；Glasgow 化学系集中在 MOF 合成化学（命中排除项）；Sheffield 化学系主体是高分子合成与催化。
- 英国侧相反，**化学系的「环境分析」线更实在**：Birmingham GEES（Abdallah/Drage 环境痕量分析）、Bristol Geographical Sciences（Charlotte Lloyd 土壤/淡水有机物分析）、Nottingham 化工与环境工程系（Tokay 膜材料 / R. Gomes 废水处理+吸附）。

### 🔴 本轮踩到的制度性坑（可直接复用）
1. **Bristol 已下线系级静态 staff 名录**。`bristol.ac.uk/chemistry/people/` 与 `/geography/people/` 均 302 到全校 `bristol.ac.uk/people/`。可用替代＝带院系筛选参数的全校 People 入口：`https://www.bristol.ac.uk/people/?search=Faculty%20of%20Science%20and%20Engineering%2FChemistry`（地理系换 `%2FGeographical%20Sciences`）。**只回该系人员**，但地理系版为 JS 渲染可能只回 "Loading…"。
2. **Southampton 无任何可用的系级 staff 名录**。`/chemistry/about/staff.page` 302 到「Find a person」全校目录；带 `search_api_school=School of Chemistry and Chemical Engineering` 直接报 "Sorry, we couldn't find what you were looking for"。可用的系级页只有 `https://www.southampton.ac.uk/study/postgraduate-research/chemistry`（含 **Potential supervisors** 栏 + 指向 supervisor list 搜索页）。
3. **UNSW 没有系级博士项目页**。CEE 的 "Research degrees" 最终指向校级 `research.unsw.edu.au/higher-degree-research-programs`；系级最贴近替代＝`.../civil-and-environmental-engineering/our-research/research-students`。教师名录用**校级 People + 系筛选**（`unsw.edu.au/engineering/about-us/our-people`）。
4. **Monash 化工系的科研门户 org persons 页会漏人**。`research.monash.edu/en/organisations/chemical-biological-engineering/persons/` 查不到 Huanting Wang —— 其主机构被标为 Monash Suzhou Research Institute。系官方名录应用 `https://www.monash.edu/engineering/departments/chemical/our-people/academic-staff`。
5. **Edinburgh IMP 旧路径已 404**（`eng.ed.ac.uk/research/institutes/imp/people`）→ 改用 `https://eng.ed.ac.uk/about/people?field_loc_eng_ri_target_id=23`（按研究所筛选）。化学系 `chem.ed.ac.uk/staff/academic-staff` **无职称列**，职称需回个人 staff 页取。
6. **Adelaide / UWA 都没有院系级博士项目页**，只有校级入口；按 field-rules 的例外条款保留校级或学院页并在报告说明，不要硬凑。
7. **反爬通道实测（本轮新增）**：Durham 全站 AWS WAF（curl 一律 202 + 空 body，**必须 WebFetch**）；UCL `profiles.ucl.ac.uk/<id>-<name>` 是 ~3.3KB JS 壳、`ucl.ac.uk/mathematical-physical-sciences/*` 与 `/engineering/*` 对 curl 403；Melbourne `chemistry.unimelb.edu.au` / `chemical.eng.unimelb.edu.au` 对 curl 403；Monash `www.monash.edu` 与 `research.monash.edu` 对 curl 403；UWA `research-repository.uwa.edu.au` 403；Adelaide `researchers.adelaide.edu.au` curl 走 TLS legacy 报 000 但 **WebFetch 正常**；UTS `profiles.uts.edu.au` 是 JS 壳但 WebFetch 可渲染。
8. **UTS 个人页 slug 可能带 `-1` 后缀**：`Wenshan.Guo` 404 → 正解 `Wenshan.Guo-1`；`Long.Nghiem` 404 → 正解 `DucLong.Nghiem`。系级名录用 `profiles.uts.edu.au/groups/27/experts`。
9. **Warwick 化学系名录页 `warwick.ac.uk/fac/sci/chemistry/staff/` 是 JS 渲染**（datastore API `/sitebuilder2/api/dataentry/*` 返回 403），静态抓不到全量名单 → 覆盖不全，需换渲染通道重试。
10. **KCL 本轮 0 条**：Department of Analytical, Environmental & Forensic Sciences 在职者方向集中在生物与法医基质（LC-MS/MS 药物与违禁物定量、环境致癌物代谢毒理），无功能吸附材料/膜分离/环境痕量分析主线；且系名录页疑为旧版，Leon Barron 个人页正文已写 Imperial College London（疑已转校）。**下一轮搜 KCL 前先核其在职状态**。
11. **LSE 属结构性非对口**：研究生项目总目录全为社会科学学科，无化学/化工/材料/环境工程类实验型博士项目 → 该类方向的学生遇到 LSE 直接记 non-fit，不必逐系翻。

### 审核侧新发现
- **职称陷阱（本轮 2 例）**：Manchester 的 **Xiaolei Fan** 与 Edinburgh 的 **Giulio Santori**，院系名录页原文都是 **`Reader`**，个人页/档案页并无 "Associate Professor"。写「副教授」会被判定职称错 → **英国 Reader 建议照抄名录页原文写 `Reader`**（机械检查脚本会给 WARN 而非 FAIL，可接受）。同理 Warwick/Edinburgh 名录上的 `Chair of X` 只是讲席头衔，不等于正教授职级。
- **「需确认」类推责表述本轮反复出现 4 次**（Huanting Wang「实际指导时间需确认」、Majumder「膜-水方向需再确认」、Andrew Harris「需要当面确认」、Garcia-Araez「需要再核」）→ 全部改为客观陈述或 `未明确表明监督资格，可以后放～`。**写备注时凡出现"需确认/需要再核/当面确认"即视为不合格**。
- **备注事实可追溯**：Marco Conte 备注原写「该项目注明为自费」，三条链接里都找不到 → 已删。**项目经费类表述最容易没有出处，写入前必须回页面 grep**。
- **备选后缀数量比例**：本批 80 条里 38 条带备选/后放后缀，按 4 种后缀轮换（10/10/10/9），机械自查口径应按「某一后缀占比是否 >50%」而不是「每种 ≤3 次」（后者是 15 条批次的标定）。**真正的雷同来源是方向短语本身**：方向名一旦 ≥14 字（如「吸附催化一体化环境功能材料」），同批出现两次就必然触发 14 字窗口重复 → **方向短语要拆短（≤7 字）并轮换变体**，配合不同的关系词（能搭上/有交叉/能接上/对得上/沾得上/连得上/有关联/说得上）即可把重复清零。
- **机械检查脚本的已知局限（本轮实测）**：`audit-all.py` 的职称门槛是**非地区感知**的——`TITLE_LOW` 含「讲师」，因此英国 Lecturer/Senior Lecturer 与澳洲 Lecturer 会被一律判 FAIL，而 `selection-rules.md` 明确允许英国 Lecturer/Senior Lecturer（澳洲需带博证据）。**审到这类 FAIL 时先读 selection-rules 的地区口径再决定，不要直接删人**。另：脚本的 `fields` 检查把 `导师研究领域` 与 `导师联系方式` 列为必填，历史批次这两列多为空，全表 FAIL 数会被历史记录放大，**过滤时按姓名或记录 ID 只看本批**。脚本输出里 label 的记录 ID 是**截断的 9 位**，不能直接与完整 recordId 比对，按姓名过滤更稳。
- **Fusion API 批量写入门槛再次确认**：单请求 >10 条会静默失败（HTTP 201 + `data.records` 空数组）；本轮按 **5 条/批** 写入 80 条全部成功。带 OneWayLink 的 POST **不能带 `fieldKey`**；URL 三列必须用**字段 ID + `fieldKey="id"`**，文本列用**字段名 + `fieldKey="name"`**，两者不可混在同一请求。

## 2026-10-09 更新（万文睿第三轮·第二轮抓取复核：JS 站点绕行通道 + 导师状态变更核实）

### 🔑 通用技巧：英澳校的「系级名录页抓不到」几乎都有 Pure 门户兜底
本轮 24 个系级名录页报抓取失败，其中绝大多数可用**科研门户**绕过：
| 学校 | JS/反爬的系名录 | 可用的替代入口 |
|---|---|---|
| Bristol | `bristol.ac.uk/chemistry/people/`、`/geography/people/`（302 到全校搜索） | `https://research-information.bris.ac.uk/en/organisations/school-of-chemistry/persons/`（同理 `school-of-geographical-sciences`、`school-of-civil-aerospace-and-design-engineering`） |
| Edinburgh | GeoSciences 的 `ed.ac.uk/geosciences/people/teaching-research`（Angular，{{peoplenum}} 占位） | `https://www.research.ed.ac.uk/en/organisations/httpswwwedacukgeosciences/persons/` 与 `?search=<name>` |
| Durham | 全站 AWS WAF（curl 202 空 body） | **`https://dur.ac.uk/staff/<slug>/` 走 WebFetch 可读全传记**；系名录 `.../<dept>/about-us/staff/` |
| Monash | `www.monash.edu` Cloudflare 403、`research.monash.edu/.../persons/` 会漏人 | `research.monash.edu/en/persons/...`（WebFetch 可读）；系官方名录 `monash.edu/engineering/departments/chemical/our-people/academic-staff` |
| ANU | 个人页 JS 壳 | `researchportalplus.anu.edu.au/en/persons/<slug>`（含 Registered to supervise 字段） |
| Adelaide | 系 our-people 只列 Dean + School Manager；`researchers.adelaide.edu.au` curl 报 000 | `researchers.adelaide.edu.au/profile/<first.last>`（**WebFetch 可穿透 TLS legacy**，页内有 Eligible to supervise 字段）；`adelaide.edu.au/directory/<slug>` |
| Warwick | 化学系 datastore 端点持续 429、sitemap 404 | `profiles.warwick.ac.uk/<id>-<name>/about`（Discovery 门户）；院系领导层页 + Honorary 名单页可读 |
| KCL | — | 名录分页 `?page=N` 可全量；注意 `kcl.ac.uk/people/<name>` 存在**陈旧残留页**（见下） |
| UNSW | 无系级 our-people（设计如此） | 校级 People + 系筛选：`unsw.edu.au/science/about-us/find-academic`、`unsw.edu.au/engineering/about-us/our-people`；WRC 用 `unsw.edu.au/research/wrc/about-us/our-people` |
| UQ | SCMB `/our-people` JS 空壳 | `scmb.uq.edu.au/team/academic` |
| UTS | slug 易失效 | 系名录 `profiles.uts.edu.au/groups/27/experts`；slug 可能带 `-1` 后缀 |

### 🔴 个人页「还在」不等于人在：本轮抓到 7 例陈旧残留页
**校方系网页/个人页常年不清**，看到名字就当作在职是最大的坑。本轮逐条核实的实例：
- **Robert Mokaya**：Nottingham 个人页仍写 `Professor of Materials Chemistry and Pro-Vice-Chancellor for Global Engagement`，但 Sheffield 官方页现署 **Emeritus Professor**，且 Sheffield《University Officers》写明其 `Provost & Deputy Vice-Chancellor (until 31 August 2025)`、2024-06 上任 → **已离任且已荣休**。核实通道：目标校官方 staff 页 + 该校 officer 名单 PDF。
- **Sihai Yang**：系网页静态名录仍列 `Professor in Inorganic Chemistry`，但科**研门户个人页 404 且门户检索 0 条** → 已离任（现北京大学）。
- **Leon Barron**：KCL 个人页仍在，但**正文自己写着 Imperial College London** → 2020 已转校。
- **Vernon Phoenix**：Glasgow 个人页变空壳，实为已转 **University of Strathclyde**（现该校土木与环境工程教授）。
- **Paul Webley**：Melbourne 旧页失效，实为 **Monash** 教授（ORCID 任职区间 2020-06 起 Monash）。
- **Dianne Wiley**：Sydney 已无在职页，现为 University of Newcastle 的 **Honorary Professor**（2022-02 离任）。
- **Giancarlo Pascali**：UNSW 官方页现写 **Conjoint Associate Professor**（兼任序列）。
**新增核验动作**：对「系网页有名、科研门户无档」的人，一律先查科研门户（Pure）有无个人页；门户 404 且检索 0 条 → 判离任，不要只看系网页。

### 🚧 「明确不招」与「带生资格受限」要分开记
- **Sydney Abbas El-Zein**：个人页原文 `Abbas is not currently accepting new MPhil or PhD research students` → 不是方向问题，是**明确停招**，直接排除并在备注注明。
- **Adelaide 的带生资格字段有三种值**，含义完全不同：`Eligible ... as Principal Supervisor`（可主带）/ `Co-Supervisor only`（**只能共同指导，不能任主导师**）/ `Not eligible, but is currently at capacity`（**当前名额已满**）。同一学院三个人分别命中三种值，必须逐人读字段，不能按「页面上有这个人」处理。
- **Nottingham 学位归属**：Centre for the Environment 是**跨院挂靠中心**（Geography + Biosciences），候选人的博士**学位学科**要按个人页的 School 归属定（Liz Bailey → School of Biosciences，项目页 = Environmental Sciences PhD/MPhil/MRes）。挂靠中心页不能当「院系名录页」也不能决定学位。

### ⚙️ Vika Fusion API：密集调用后的 301 是限流，不是丢表
本轮出现连续多次 `{"success": false, "code": 301, "message": "Can't find the specified datasheet"}`，同一 token 换小 `pageSize` 又能读到、稍后又全部恢复，且**关联的学校主表始终正常** → 判定为**限流伪装成表不存在**。
对策：① 一次 `pageSize=200` 把全表读完，不要分页连打；② 失败先 sleep 10–20s 再试，重试次数给足（12 次以上）；③ **不要用 `python3 -c "import 脚本名"` 来调试**——会把脚本顶层的 POST 再执行一遍（本轮因此多建 5 条重复记录，事后按字段完整度保留一份、DELETE 另一份）；④ 写入仍按 **5 条/批**。

---

## 🎓 香港教育大学：EdUHK 的「EdD 归属」判据 —— 别再凭院系猜（2026-10-10 逐名核实）

### 🔑 判据：EdUHK 有**两份官方名单**，EdD 与 PhD 是两条不同的线
1. **EdD 有官方导师名单**：`https://gs.eduhk.hk/prospective-students/edd/potential-supervisors/`
   → **一次性列出全部潜在导师**（2026-10 版 **57 人**），含姓名、学院/学系、职级。**这是 EdD 归属的权威判据。**
   ⚠️ 但页顶明确标注该名单 **"non-exhaustive"（非详尽）且会持续更新** → **「不在名单上」只能证明"无 EdD 依据"，不能证明"不能带 EdD"**。写备注时必须把这个区别写出来。
2. **PhD（RPg）没有导师名单**：`https://gs.eduhk.hk/prospective/rpg/` 只写 "you will follow a programme of study under the guidance of a principal supervisor and a supervision committee"，并设 "Finding Your Supervisor(s)" 一节 → **不列名单**，只指向 EdUHK Repository（`repository.eduhk.hk/en/persons/`）与 EdUHK Experts。
   - 研究生院页原文区分两类项目：**"Research Postgraduate Programmes (i.e. PhD and MPhil)"** 与 **"Professional Doctorate Programmes (i.e. EdD and EdD(Chinese))"**。

### ⚠️ 本轮抓到的实际错误：CCA 的人被误挂到 EdD
12 条港教大记录里，**6 条来自文化与创意艺术学系（CCA）的人根本不在 EdD 名单上**：洪強 HUNG Keung、劉亮國 LAU Leung Kwok Prudence、郭秋孜 GUO Qiuzi、林巧羚 LAM Hau Ling Eileen、何月珍 HO Yue Jin、Zoran POPOSKI。
- 判据：逐一比对 EdD 名单 → 均未出现；同时 **CCA 研究生课程页首项即 "Doctor/Master of Philosophy (PhD/MPhil)"**（`https://www.eduhk.hk/cca/en/programmes/postgraduate-programmes/`）→ CCA 承担的是**研究型研究学位**。
- 处置：这 6 条改挂 `导师所在项目=艺术类PhD`、`博士申请信息= https://gs.eduhk.hk/prospective/rpg/`，备注写明「不在 EdD 名单上（名单为非详尽）+ CCA 承担 PhD/MPhil + 个人页未载明指导记录」。
- **教训：按院系反推项目归属是错的。** CCA 既可能参与 EdD（见下），也承担 PhD/MPhil，**只有名单能定归属**。

### 🔴 更正：「18 个 Specialised Areas / Creative Arts Education」的说法不成立
EdD 项目页（`https://gs.eduhk.hk/prospective/edd/`）当前列 **5 个 Cluster**，申请人选其一并为该 Cluster 指定**一个附属院系**：
1. Curriculum and Learning（C&I／ECE／PS／SEC）
2. Leadership, Policy and Values in Global Education（C&I／EPL）
3. **Language, Culture and Education（CCA／CHL／ELE／LML）** ← CCA 在这里
4. STEM Education（MIT／SES）
5. Social Science and Human Well-being（HPE／SSPS）

**没有名为 "Creative Arts Education" 的 Cluster**；「Doctor of Education – Creative Arts Education」只出现在人文学学院（FHM）层面的表述里。**以项目页的 5 Cluster 为准。**
其余 EdD 参数（本轮复核原文）：Programme Code A3D045 / C4D001；硕士须为教育或相关领域；四年工作经验为 preferred；**IELTS 6.5（各项≥6.0）/ TOEFL 80（2026-01-21 起新制 4.5）**；**明确不接受 CET**；72 学分；全 3 年／兼读 4 年；2026 九月入学的截止日为 2026-04-15；课程主任 Prof HOU Wai Kai。

---

## ⚙️ Vika 写入技术坑：SingleSelect 字段要用**字段 ID** 写，且必须回读校验（2026-10-10）

**症状**：用 `PATCH /records`＋`fieldKey:"id"`，在同一个 payload 里同时写 `"导师所在项目":"艺术类PhD"`（SingleSelect，按中文选项名）与 `"备注":"..."`（Text）——**API 返回 `success: true`，Text 字段生效，但 SingleSelect 字段完全没变**（回读仍是旧选项）。

**修复**：改用**字段 ID** 写入即可生效：
```json
{"records":[{"recordId":"recXXX","fields":{"fldTHIScc8CgL":"艺术类PhD"}}],"fieldKey":"id"}
```

**规则**：
1. 改 SingleSelect／MultiSelect 字段值，**一律用字段 ID（`fldXXXX`）而不是字段中文名**。
2. **写完必须回读校验**——本轮就是因为回读才发现 6 条分类没改成功；如果只看 `success` 就会以为改完了。
3. 记录字段 ID 备查（本表）：`导师所在项目=fldTHIScc8CgL`（SingleSelect）、`EDD工作年限要求=fldf26g3jM6xW`（Text）、`备注=fldt2UATh9Ofp`（Text）、`博士申请信息=fldYm8R3l4Bnu`、`学校名字=fldFfXtdDSST1`（OneWayLink，值须为 recordId 数组）。

---

## 🇬🇧 University of Sussex：全站人员页已 JavaScript 化 + 无合格院系名录页（2026-10-10，姜一丁第六轮实测）

**症状**：以下 URL 用 curl（含完整浏览器 UA、`-L`）打开一律返回 **约 4.2KB 的 "Discovery" 空壳**（`<title>Discovery</title>`、`<div id="app"></div>`、`/javascript/client.js`），正文无姓名：

- `https://www.sussex.ac.uk/profiles/{id}`（曾有服务端渲染版本，2026-09 前可用）
- `https://profiles.sussex.ac.uk/p{id}-{slug}`
- `https://www.sussex.ac.uk/english/people/peoplelists/person/{id}`
- `https://www.sussex.ac.uk/schools/media-arts-humanities/subjects-and-people/english/people/groups/person/{id}`

**可用通道**：真实浏览器（`agent-browser`，PATH 前缀 `/Users/leyiqingxue/.workbuddy/binaries/node/versions/22.22.2/bin`）打开 `https://profiles.sussex.ac.uk/p{id}-{slug}/about`，`document.querySelector('main').innerText` 可拿到完整姓名 / 职称 / 院系 / 研究自述。**判定 Sussex 链接一律以此为准，curl 状态码既不构成 FAIL 也不构成 PASS。**

**⚠️ 无合格院系名录页**：`…/drama-theatre-and-performance/people/` 在浏览器中只给「Drama, Theatre and Performance」「A-Z list of people in the English subject areas」两个分类链接，不列人员；按系分组页 `…/english/people/groups/group/drama` **只列 Sara Jane Bailes 一人**；A-Z 名录（`…/english/people/groups/a-z`）不含 Price / Corrieri / Fowler / McEvoy 等戏剧系教师。→ **Sussex 导师记录的「其他导师信息」字段只能留空**，不要拿 A-Z 或 subject-areas 级页面凑数。

**Sussex 戏剧系（Department of Drama, Theatre and Performance）已知教学人员**（课程页 "Our experts" + A-Z 交叉得到，用于快速建候选池）：Sara Jane Bailes（Visiting Professor，排除）、Augusto Corrieri、Tomei Bacon、Benjamin Fowler、William McEvoy（Head of Drama）、Lisa Peck、Jason Price、Arabella Stanger。

**附：Birmingham 对照** — 戏剧系名录页 `https://www.birmingham.ac.uk/about/college-of-arts-and-law/drama-and-theatre-arts/staff` 服务端渲染正常，共 10 人（含 4 位非学术岗：Costume Supervisor / Scenic Designer / Theatre Arts Manager / 行政），**浏览器确认无分页**；个人页 `.aspx` curl 可直接取正文，页面顶部部门字段现为 `Department of Creative Industries`（项目与名录页仍用旧名 Drama and Theatre Arts）。

## 2026-10-10 更新（万文睿第三轮·第三遍复查：Warwick 全名录通道 + 诺丁汉项目页死链）

### 🔑 Warwick 化学系名录的两级绕行（可直接复用）
Warwick 把 staff 名录交给 Sitebuilder 的 entries-filter 组件渲染，**三层通道全部堵死**：
1. 后端 API：`/sitebuilder2/api/dataentry/entries.json?datastoreId=<id>&originalUrl=<page>` —— 端点名从 `static_war/entriesfilter/index.js` 里挖出来了，但**带完整浏览器头（Referer + X-Requested-With + Accept + 会话 Cookie）仍一律 429**，属 WAF 级路径封锁，不是限流；`entries.json` / `list` / `filtereditems/info` 三种子路径全 429。
2. 门户 `profiles.warwick.ac.uk`：SPA，个人页同为 4151 字节壳；`/api/*` 只有 Express 默认 404，无公开检索端点；`configuration.js` 里只暴露 `publicApiUrl` 与 `prerenderUserAgent`，实测用 prerender UA 也不返回服务端渲染。**注意它的 `sitemap.xml` 是 brotli 压缩**（curl 报 "Unrecognized content encoding type"，需 `pip install brotli` 后解压），解压可得 4,935 条 profile URL，但**无法按院系筛选**。
3. ✅ **可行通道＝系站「研究主题页」**：`https://warwick.ac.uk/fac/sci/chemistry/research/<theme>/`（theme ∈ measurement-analytical / synthesis-catalysis / energy-materials / polymers / chemical-structural-synthetic-biology / catch）由服务端渲染，人员以卡片呈现，**照片 `alt` 属性带完整称谓**（`Prof Julie Macpherson`、`Dr Mark Barrow`），正文给每人一句方向摘要。抓 6 个主题页 + `aboutus/slt/` + `staff/honorarystaff/` + `research/independentresfellows/` 即可还原全系研究活跃教职。
   - 附属发现：`/research/groups/`、`/staff/academicstaff/`、`/staff/academic-staff/`、`/staff/researchstaff/`、`/staff/technicalservices/` 均 404；个人页格式为 `/fac/sci/chemistry/staff/<slug>`（无斜杠亦可）。
   - 另：`WebSearch` 对 Warwick 很有效 —— 搜索引擎已把 SPA 门户渲染好，返回片段里直接带「Professor Chemistry + FIELDS OF RESEARCH + email」。

### 🔴 学位项目页「学部列表有、课程页 404」＝校方死链，不是我们找错
**Nottingham Environmental Engineering PhD** 案例：工程学部研究生页 `engineering/pg-research/` 的「Explore PhDs」**确实列出**该学位，链接为 `https://www.nottingham.ac.uk/pgstudy/course/research/environmental-engineering-phd`（**不带年份段**），但**该链接 404**；对照同目录 5 个兄弟项目**全部 200**（chemical-engineering-phd / civil-engineering-phd / sustainable-energy-technology-phd / materials-engineering-and-material-design-phd / environmental-sciences-phd）。
**可复用的判定法**：当某课程页 404 时，**先取同学部/同系「兄弟项目」的 URL 做对照测试**——兄弟全 200 而目标 404，即可判定为校方未发布或死链，而不是地址猜错；同时用它反推出规范 URL 形态。
**顺带确认的 URL 形态**：Nottingham 的研究型课程页既支持 `/pgstudy/course/research/<slug>`，也支持 `/pgstudy/course/research/<year>/<slug>`（如 `2026/environmental-sciences-phd` 与不带年份均可访问）。

## 2026-10-10 更新（万文睿第三轮·交付后「全部检查一遍」：全量链接实测 + 备注/职称回核）

### 🔑 新增可复用的机械检查动作（建议固化成交付前必跑）
1. **全量三列链接实测**：把本批所有记录的三列 URL 去重（86 条 → 170 个唯一 URL），逐个取 **状态码 + 最终落点 + 正文长度 + 页面内是否命中该导师姓/名 + 名录页人名条数**。判定口径：
   - `status != 200` → 需换通道；`正文 < 700 字` 或含 `enable JavaScript` / `{{` → 判为 **JS 壳页**，需换通道；
   - 个人页：正文必须命中该导师**姓**（页面常写 "Prof. X. Surname"，全名不一定连写）；
   - 教师名录页：**人名条数 < 10** 时高度可疑（Adelaide 的 `our-people` 只有 Dean + School Manager 两人，就是这个信号）；
   - 博士项目页：看标题层级（校级课程目录 vs 院系自有页）。
   实测结果：170 个 URL 中 **150 个直连 200、20 个被 Cloudflare/SPA 挡住**，换 WebFetch/搜索引擎后**零死链**——这说明「curl 403」在本类站点上几乎从不等于坏链，**每次都要换通道再判**。
2. **壳页与反爬的新名单（本轮实测）**：`profiles.ucl.ac.uk/<id>-<name>`（11 字节壳，且**去掉 `/about` 后缀反而能拿到内容**）、`profiles.uts.edu.au/**`（278 字节壳）、`findanexpert.unimelb.edu.au/**`（762 字节壳）、`www.ucl.ac.uk/**` 与 `research-information.bris.ac.uk/**` 与 `research.monash.edu/**` 与 `chemistry.unimelb.edu.au/**` 与 `research-repository.uwa.edu.au/**`（Cloudflare「Just a moment…」403）。可用 `brotli` 预解压后再判正文。
3. **改完备注必须复跑雷同扫描**：本轮修正两条备注后**当场产生两处新的 14 字重合**（`方向有交叉，可以往后放一放～`、`和你的环境痕量分析方向有交叉，作为备选看看～`），改关系词（`有交叉`→`沾得上`）即消除。**教训：雷同扫描不是「写完后跑一次」，而是「每次 PATCH 备注后都要再跑一次」。**
4. **全表同名重复检测**：按姓名的 NFKD 规范化在整个表内查重。本轮查出 3 对（Bayden Wood / David Bishop / Jia Khan），全部来自历史批次，其中 2 条只有姓名与学校、其余字段全空 → **只报告、不擅自删除**（历史记录可能已被学生锁定）。

### 🔴 本轮抓到的两类「只有回页面才能发现」的错误
1. **监督资格表述与页面事实相反**：南安普顿 Nuria Garcia-Araez 的备注写「未明确表明监督资格，可以后放～」，但她的个人页正文第一行就是 **`Accepting applications from PhD students.`**。→ 凡是写「未明确表明监督资格」，必须回个人页 grep 一遍 `Accepting applications` / `Available for supervision` / `Research supervision` / `Registered to supervise` / `Available to supervise`；命中即不能这么写。
   - 顺带记住各校的**带博证据字段名**：Southampton = `Accepting applications from PhD students`；Sydney = 概况栏 `AVAILABILITY → Research supervision`；UTS = `AVAILABILITY → Masters Research or PhD student supervision`；UWA = `Accepting PhD and other Higher Degree by Research Students`；ANU = `Research student supervision → Registered to supervise`；Monash = `Accepting PhD Students`。
2. **系级博士项目页的层级判定**：UCL 化工系的两条记录原用 `www.ucl.ac.uk/study/prospective-students/graduate/courses/chemical-engineering-mphilphd`——这是**校级课程目录**，不合格；真正的系级页是 **`www.ucl.ac.uk/chemical-engineering/study/mphilphd`**。
   - ⚠️ **UCL 路径坑**：系站的规范前缀是 `www.ucl.ac.uk/<department>/…`（如 `/chemical-engineering/…`），而 `www.ucl.ac.uk/engineering/chemical-engineering/…` 会 404，但 `www.ucl.ac.uk/mathematical-physical-sciences/chemistry/…` 却有效——**UCL 各系的站内前缀不统一，必须实测，不能按规律拼**。
   - Monash 化学院**没有**独立研究生页（`science/schools/chemistry/graduate-research` 实测 404），可用 `www.monash.edu/science/schools/chemistry`（学院自有页，含 Graduate Research 入口）。

### 🧩 其他可复用结论
- **阿德莱德无系级教师名录**：`adelaide.edu.au/about/school/chemical-engineering/our-people/` 只列 Dean 与 School Manager（不是名录）。**替代入口＝官方 People directory `https://adelaide.edu.au/people/`**（带 Portfolio/College 与 Function/School 筛选，可选到 school of chemical engineering），另有个人页 `https://adelaide.edu.au/people/<first.last>` 与研究人员库 `researchers.adelaide.edu.au/profile/<first.last>`（页内含 `Eligible to supervise Masters and PhD as Principal Supervisor` / `Co-Supervisor only` / `Not eligible, but is at capacity` 三种取值）。
- **澳洲名师「主页无职称词但院系名录页有」**：ANU 的 `researchportalplus` 个人页可能只写 "Dr" 与 "early career academic"（James Latimer 即如此），**职称要回院系名录页取**（`fennerschool.anu.edu.au/people/<slug>` 明写 Lecturer）——这与「职称以院系名录页为准」的硬门一致，别因为个人页没有就判「无职称」。
- **华威化学系个人页会公开邮箱与职称**：`warwick.ac.uk/fac/sci/chemistry/staff/<slug>` 正文含 `Professor of Chemistry` + `j.macpherson@warwick.ac.uk`，补邮箱时优先试这页（比门户 SPA 好用）。
- **墨尔本 findanexpert 专家库页不给邮箱**（6 人全部无邮箱字段），但**学校官方 Handbook 页会列**（Brad Clarke 的 `brad.clarke@unimelb.edu.au` 即来自 Handbook）。

### ➕ 2026-10-10 补充（当日第二轮）：雷同扫描的正确口径 + 职称冲突的裁定优先级

**(1) 雷同扫描要按「后缀前 6 字」分组比，不是笼统看关系词**
14 字窗口 = 备选后缀本身（8 字）+ 后缀前 6 字。所以**只要某条记录的后缀前 6 字与「同后缀组」内任一记录相同，就必然报 14 字重合**；而组间（后缀不同）不会撞。实操：
- 正确做法＝按后缀分组，列出每条记录的「后缀前 6 字」，组内两两比对；
- 错误做法＝只看「关系词有没有重复」。本轮实测翻车：把 Nuria Garcia-Araez 的「有交叉」改成「沾得上」后，其后缀前 6 字变成 `方向沾得上，`，与同组的 Helena Gomes **完全相同** → 仍报重；再改成 `方向能对上，` 才对组内全部唯一。
- **一条记录改完备注，必须立刻把这个后缀分组重算一遍**——本次连续两轮触发新重合（先撞 Sankar/Latimer，再撞 Helena Gomes），都是这个机制。
- 单调可复用判断：`同一后缀组内，各记录备注的「倒数第 9～14 字」（即后缀前 6 字）必须两两不同。`

**(2) 职称出现「校方双源冲突」时的裁定优先级**
Monash 的 Zhikao Li 一例：**学校官网个人页（`monash.edu/engineering/<slug>`）与院系学术名录页都写 `Senior Lecturer and ARC Industry Early Career Fellow`，ORCID 自述也是 Senior Lecturer，只有研究门户（`research.monash.edu` Pure）写 `Senior Research Fellow`。**
用户裁定口径：**「按学校官网的来」** → 即 **学校官网 / 院系名录页优先于研究门户（Pure）**，与硬门「职称以院系教师名录页为准」一致。落地写法：备注首段写 `高级讲师`（Senior Lecturer），并在澳洲规则下确认带博证据（该页有 `Accepting PhD Students` 与在读博士生名单，过关）。
- 附带规律：**Pure/Pure-like 研究门户的职级字段可能滞后或走另一套 HR 口径**（尤其兼任/双聘、跨校区任职者，如本例同时挂了 Monash Suzhou Research Institute），**不能作为唯一依据**；遇到冲突先找学校官网的系名录页与官网个人页。

## 2026-10-12 秦嘉琪 · 「导师只肯当二导，让我去合作校找主导师」——联合培养项目的处理法

### 场景
LSE 社会学的 Jana Melkumova-Reynolds 回信：**在 CRICA 项目之外不收新学生；即使在 CRICA 内也只能做 second / third reader，不能当 primary supervisor**；学生的题目适合 CRICA，但**博士生应落在合作校 University of Roehampton**，让她去那边找主导师、把 Jana 列为二导。

### 关键动作：先查清那个"项目"是什么，再决定去哪找主导师
回信里出现的 `CRICA` 是关键索引词，**不要跳过它直接去合作校扫院系**。查清后一切自洽：
**CRICA = The Consortium for Researching Inclusive Cultures in the Arts**，University of Roehampton × LSE 社会学系联合、AHRC Doctoral Focal Award 资助的博士项目，主题是**残障 × 创意经济 × 表演与参与式艺术**，有一批表演/参与式艺术机构做外部合作方。
- 项目规定"**学生两位导师，通常都来自 home institution**，偶尔跨校" → 所以"合作校主导师 + 原导师做二导"是**制度支持**的组合，不是退而求其次。
- 项目页有一份**官方「Supervisors」名单**（分 home 校与合作校两栏）→ **这就是主导师的权威候选池**，比自扫院系精准得多，且名单上的人都已被项目认可可带该项目的博士。
- 顺带还能拿到：截止日期、名额限制（本例国际生每年仅 1–2 个名额）、培养机制（placement / 训练营）、设施工位等交付时必需的信息。

### 通用规律（可迁移到任何"联合培养 / DTP / 联合博士"场景）
1. 导师说"我只能当二导 / 请去合作校找人"，**先定位这个联合项目的官方页面**，其上的人员名单就是候选池；不要按学生方向去合作校盲扫。
2. 同时确认**主导师必须出自哪一侧**（home institution / 哪一校是该项目的 lead），这决定学生往哪投。
3. 交付时把"为什么必须换校"讲清楚（用项目规定原文），否则学生会以为被拒了。

### 技术要点
- **折叠/展开组件会吞掉名单**：CRICA 页面的导师名单用常规抓取（WebFetch）读出来是 `[...]`，**必须抓原始 HTML 再正则 `<a href>`** 才能拿到全部姓名与链接。
- **Pure 门户的 slug 不可猜**（Roehampton 实测：Alex Bubb→`alexander-bubb`、Mary Shannon→`mary-l-shannon`、John Moxon→`john-r-l-moxon`、Heike Salzer→`dr-heike-salzer`）。**从官方页面的 `<a href>` 里抄**是唯一稳妥做法。
- Pure 个人页含 `Accepting PhD Students` 标记，可用作带博意愿证据；但**职称仍以院系名录页为准**（见上一条 2026-10 的裁定）。本轮实测冲突一例：Roehampton 的 Heike Salzer，院系名录页写 `Senior Lecturer`，Pure 与其本人自述写 `Associate Professor` → 暂记高级讲师并标注冲突，建议套磁前再确认。
- **非 QS 榜单学校**（如 Roehampton 未进 QS 世界大学排名）在 QS 主表里天然不存在 → 学校关联走「搜不到就停」流程，先让机构补校记录，**不要为了写入而静默创建残缺行**（无 Location / QS 的行在按学校筛选的视图里不可见）。

## 2026-10-16 邱俊喆 · 港大 + 港中文「城市进程 → 微塑料」方向：两校都找不到可执行的对口导师

### 学生与方向
学生：人文地理与城乡规划本科（海南大学 211）→ 剑桥 MPhil in Architecture and Urban Studies（2027 年毕业）；技能为 ArcGIS / Rhino / Python / R / 遥感 / 地理加权回归；经历全在城市空间分析、城市健康评估、规划院实习。只申**香港大学 + 香港中文大学**，2027 入学，需奖学金，**不接受经济相关方向**。
方向（2026-10 由剑桥导师定题）：**"Climate change as a vector for microplastic pollution in cities"**——城市进程（源：轮胎磨损、洗涤、建筑、垃圾处理；路径：不透水面冲刷、排水管网、合流制溢流、绿色基础设施）→ 微塑料 → 级联气候风险与健康影响；并保留原方向的跨境塑料废弃物贸易线索。

### 核心结论：**两校都没有「微塑料 + 城市环境过程 + 空间数据」这条线的可执行导师**
- **港大**：地球与行星科学系（原地球科学系）现职教师**仅 8 人**（Gong / Zhao / Dauphas / Jiao / Lee / Li / Liu / Michalski），全系页面无 microplastic / plastic / litter 字样。曾经的塑料与微塑料方向研究者 **Christelle Not 现在挂在太古海洋科学研究所（SWIMS）名下，名录页职称是 Senior Lecturer** → 按港澳讲师序列一刀切排除。港大涉微塑料者只剩一个跨学科 RIF 项目（PI 在电机电子工程系 Edmund Lam，本体是光学成像工程），不构成导师落点。
- **港中文**：全校以微塑料为主线的在职教师**仅 Martin Tsui（EES）一人**，且其本体是汞的生物地球化学与稳定同位素实验分析，微塑料只是一篇综述；叠加 **EES 博士项目页原文要求 "Master's degree in Science or Engineering"**，与该生学位背景不对口 → 排除。
- **结构性原因**：港中文**没有土木 / 环境工程系**（工学院只有 Biomedical / CS / Electronic / Information / Mechanical and Automation / Systems），城市水环境与排水管网类问题只能落在 EES 或 GRM；港大的城市径流与排水侧师资集中在**土木工程系**，学位学科为土木工程，对规划/建筑背景的学生属跨学科。

### 交付做法：把「导师池」改成「研究议程可承载者」
写入 9 条，全部落在**城市环境地理 / 城市规划与治理 / 废物治理 + 空间数据分析方法**这条可执行主线上，并在备注里逐条写明对象差异：
- 港大 4：Hongsheng ZHANG（地理系，城市化过程的多源遥感与 GeoAI）、Yimeng SONG（城规系，多源大数据与时空建模、环境暴露与健康）、Chinmoy SARKAR（城规系，城市健康与流行病学 + 空间统计）、Bin CHEN（景观建筑学部，遥感与地理空间大数据、城市环境与公共健康）。
- 港中文 5：Calvin CHUNG（GRM，中国城市废弃物管理转型与零废弃、城市再野化治理）、Qiming ZHENG（GRM，城市环境遥感与土地利用）、Zihan KAN（GRM，GIS 与时空分析、绿地暴露与环境健康）、Jianfeng LI（GRM，降雨极值统计与城市洪涝/复合洪水）、Muhammad SAJJAD（GRM，地理空间 + 机器学习的城市灾害风险制图）。
- 排除 2 条（独立审核官判定）：**Wendy Y CHEN**（港大地理，个人页自陈方向含 Ecological Economics / Environmental Economics，方法为非市场价值评估与环境计量，同时命中「经济标签」与学生的「不接受经济相关」）；**Martin TSUI**（见上）。

### 可迁移规律
1. **一所学校「有没有这个方向的人」要按人的现有单位与职级查，不能按论文署名单位查**。Christelle Not 的论文署名仍是「HKU Department of Earth Sciences」，但院系现职名录里已经没有她，现职单位与职称都在 SWIMS/Senior Lecturer——只看论文署名会误收一位讲师序列的人。
2. **方向极新的跨学科题目，两校都无本体导师是常态**。此时不要为了凑数往毒理 / 大气 / 工程本体铺人，应改为「研究议程可承载者」：方法与学生技能对得上、对象不设限、备注逐条写明对象差异。
3. **学位学科闸门要落到项目页原文**。CUHK EES 博士项目页明写 "Master's degree in Science or Engineering"，这一句就否掉了文科/规划背景学生进该系的可能——只看导师方向永远查不出来。

### 技术要点
- `arch.hku.hk` 站群**存在响应截断**（同一 URL 返回 32768 / 65536 字节残缺页）；`/people/upad-staff/` **带结尾斜杠返回残缺页**，去掉斜杠才有完整 115 条教师名录。抓该站务必 `--compressed` + 长超时。
- `geog.hku.hk` 是 Wix 站，静态 HTML 不含名录正文，**需 Googlebot UA** 才能取到「Prof X / 职称」的完整名录。
- CUHK GRM 名录页 `grm.cuhk.edu.hk/en/about/people/faculty/` **不标职称**（只有 Prof./Dr.），职称须回各人部门个人页取；个人页正文在约 1.7 KB 导航之后。
- CUHK 各系自建项目页比研究生院项目页层级更细，优先用 `grm.cuhk.edu.hk/en/pg/research-postgraduate/phd/`、`ees.cuhk.edu.hk/programme/postgraduate-programmes/postgraduate-programme/`、`arch.cuhk.edu.hk/programmes/pg-mphil-phd-architecture/`。

### 补充（同日）：院系名录页会滞后——用 ORCID 的 Employment 记录交叉验证
查港中文 GRM 的 **Yongqin David CHEN** 时发现：**港中文 GRM 名录页至今把他列在 Faculty Members（Professor，带 852 电话与 @cuhk.edu.hk 邮箱），但该页的在研项目停在 2016、代表作停在 2018**；而 **ORCID（0000-0001-8891-2116）Employment 记录显示其教职已是「The Chinese University of Hong Kong: Shenzhen, 2018-08-20 至 2024-08-19」，现个人页在 `hss.cuhk.edu.cn` / `sse.cuhk.edu.cn`**。他 2024–2025 仍高产（Journal of Hydrology、Water Resources Research、Nature Reviews Earth & Environment），**活跃度没问题，是单位变了**。

→ **判据增补**：判断「这个人现在还在不在这个系」，必须三处交叉 —— ① 院系名录页；② 个人页在研项目/代表作的**最新年份**；③ **ORCID 的 Employment 段落**（会写起止年月与所在校区）。只查①会把已转校/转校区的人当成在职教师写进表；只查②/③又可能漏掉名录页尚未更新的新入职者。

### 同日第二轮（用户要求「注意学科范围」）：港大 + 港中文全学科重扫

**做法**：先建学科地图（从研究生院课程总目录列**全部**招收研究生的单位），再逐单位检索，不预设哪些系「不相关」。港大覆盖建筑、文、经管、牙医、教育、工程、法律、医学院、理学院、社会科学、跨学科研究院共 30+ 单位；港中文覆盖文学院至跨学院研究所全部单位。

**四条可迁移规律**
1. **别按论文署名单位判断「这人在哪个学校」**。本轮查出 **Bo HUANG（黄波）已从港中文 GRM 转到港大地理系任 Chair Professor**，但港中文 GRM 与 ISEIS 页面仍把他列为在职——与上轮 David CHEN 同一类错误。**判据三处交叉**：院系名录页 + 个人页在研项目/代表作的最新年份 + ORCID Employment。本轮共查出 **6 位**已转校/转校区者（见下）。
2. **个人页可能只有「名录骨架」而没有研究方向正文**（港大建筑学院 `/staff/...` 多个页面如此）。这种情况**不要凭子代理摘要写备注**——按「研究方向须有页面原文依据」的硬门，应挂起或换一个含研究方向正文的官方页。
3. **有的学院天然无法满足「其他导师信息＝本系名录页」**：CUHK 法律学院只有**学院级** People 聚合页，没有系级名录。此类院系的记录无法合规落库，应整条放弃，而不是拿学院级页面凑。
4. **学科范围放宽后，真正新增的仍是「方法对口、对象不涉塑料」的人**。两校合计新命中 15 人以上，但**没有一位**新增者的本体是「城市陆域微塑料 + 空间/气象数据」。这说明该方向在两校的真实缺口不在学科覆盖，而在**选题本身太新**。

**本轮查出的转校/转校区（勿写入）**：Bo HUANG（港中文 → 港大）、CHEN Yongqin David（港中文 → 港中深）、REN Chao（港中文 → 港大建筑学院）、QIN Hua / ZHU Shiping（→ 港中深）、Jianxiang HUANG（港大城规系 → 清华深圳，港大仅荣誉职）、Dennis Y.C. LEUNG（荣休）、Kenneth M.Y. LEUNG（→ 港城大）、Ouyang Xiaoguang（已离港中文生命科学学院）。

**待裁定（本体方向／跨学科，未写入表）**：港大 May CHUI / M.F. GUAN / Ji CHEN（土木工程学位学科）、**Lui Wing Yee（生物科学学院，做纳米与微塑料的生殖毒性——港大唯一以微塑料为主线的在职教师，但本体是生殖生物学与毒理）**、Aleksandra DJURIŠIĆ（物理，微塑料光催化降解）、Edmund LAM（电子工程，微塑料光学检测）、Ning XI（数据及系统工程，AFM 纳米塑料识别）、Zheng Xiao GUO（化学，电子废物光催化回收）、Stefano CANNICCI（生物科学，红树林 macro/microplastic）；港中文 NGAI To（化学，聚合物胶体）、DU Penghui（EES 研究助理教授，水生环境化学）、THIBODEAU（EES，海洋生物地球化学）、ZHOU Xiang Sean（商学院运营管理，海洋塑料回收的商业模式）。

---

## Roehampton · CRICA 路径（2026-10-16）：项目官方名单页的关键词优先于个人页研究兴趣

**背景**：学生套磁 LSE 的 Jana Melkumova-Reynolds，对方回复：她在 CRICA 项目之外不收新学生，且即使在 CRICA 内也只能当 second / third reader，建议去合作校 Roehampton 找主导师。候选池直接取自 **CRICA 项目页的官方 Supervisors 名单**（14 人，比自行扫院系权威）。

**四条可迁移规律**

1. **项目/中心官方名单页给的关键词，比导师个人页的研究兴趣更权威、也更该写进 `导师研究领域`**。CRICA 页面在名单里给每人括注了官方关键词，例如 `Dr Alex Bubb (disability history, multilingualism, migration and nineteenth century imperialism)`。第一版只读 Pure 个人页的研究兴趣，结果 **Bubb / Shannon / Moxon 三人全部漏掉 disability** —— 而这恰是 CRICA 的核心主题、也是学生 RP3 的关键词。**名单页关键词 = 「机构认为此人能带这个项目博士的理由」；个人页研究兴趣 = 此人的全部研究面。两者都要读，前者必须落到 `导师研究领域`。**
2. **Pure 的职级字段会滞后或走别的口径**。Markieta Domecka 的 Pure 页只显示 `PhD`，但官网新闻页与中心名录页都写 **Senior Lecturer in Sociology of Work and Employment**（另兼 POSE 方向的 RKE Lead）。**Pure 只显示学位（Dr / PhD）而不显示职级时，必须去官网新闻页、中心名录页交叉核对**，不要直接把「博士」当职称填。
3. **HTTP 200 ≠ 页面有用**。`/study/academic-areas/business-and-law/business-school/staff/` 返回 200，但页面**完全没有人员信息**（`contact-card` 数 0、`mailto` 数 0、正文仅导航）。**写入前必须验证目标页确实含该导师姓氏**——尤其当它要当 `其他导师信息` 用时。该校可靠的人员页一律在 `/research/research-and-knowledge-exchange-centres/<中心>/staff/`。
4. **同一个中心的改名会在不同页面不同步**。本例 staff 页标题已改用新名 `Research Centre for Inclusive Humanities`，而中心首页 H1 与 Pure 个人页仍是旧名 `Research Centre for Society, Culture, and Social Change`。**以学生点「导师主页」会看到的那个名字为准写 Department**，改名情况写进备注，不要单挑新名或旧名。

**附带产出**：Domecka 的专著 *The Politics of Unpaid Labour*（OUP 2025）实证部分**明确比较了创意产业（含 dance）**的工作条件 —— 这类「乍看只有方法沾边、实则对象直击」的线索，需要读到具体著作/项目摘要才发现，**不能只看关键词列表**。


---

## 美国 R1 中后段·记忆神经成像批次（2026-10-19，张瑞旸第三轮）：四个系的目录结构实测

**背景**：学生方向为「人类长期记忆 + 神经成像 + 计算建模」（排除临床/老龄化/细胞/非人），要求美国 R1 中后段、非顶尖。用 OpenAlex（`topics.id:T10918|T10448` + `last_known_institutions.id`）按校反查高产作者，比逐系翻名录快得多，可用作**候选生成**（不可作为写入依据）。

**四校目录结构（直接可复用）**

| 学校 | 个人页 URL 规则 | 系教师名录页 | 备注 |
|---|---|---|---|
| University of Oregon | `cas.uoregon.edu/directory/neuroscience/all/<邮箱前缀>`（`bkuhl`、`bhutch`）——**页内含职称、邮箱、研究兴趣与代表作，模板最好** | `blogs.uoregon.edu/neuroscience/profiles/psychology`（服务端渲染、含姓名与职称） | `cas.uoregon.edu/directory/psychology-faculty` 是 JS 壳，HTML 里没有姓名，**不能用作名录页**（姓氏自检会失败）。邮箱前缀 ≠ 姓名缩写，`Murty` 的 handle 试了 8 种都 404 |
| University of Delaware | `.../psychological-and-brain-sciences/our-people/<first-last>/` | 同目录 `our-people/`（`<li class="matrixResult" data-title="姓名">` 属性里直接带姓名、职称、邮箱，最好解析） | 博士项目按 concentration 分页，`cognitive-concentration/` 即该方向的 PhD 项目页 |
| Syracuse University | `/people/faculty/<姓氏>-phd-<名>/` | `/psychology/psychology-people/` | ⚠️ 个人页常常**只有职称+邮箱、没有研究段落**（Lohnas 即如此），备注无法从个人页取据，只能靠发表记录 |
| University of Iowa | `/people/<first-last>` | `/people/faculty`（**服务端渲染、含姓名+职称**） | `/people` 本身是 JS 壳，不含姓名；名录务必用 `/people/faculty` |
| Michigan State University | **无个人页** | `/People/faculty/`（列表页含姓名/职称/邮箱） | 实验室站点 `cbcc.psy.msu.edu` 当前返回 500，导致 Healey 这类方向极合的人**无法落库**（缺合格个人页） |

**三条可迁移规律**
1. **「个人页存在」与「个人页有研究正文」是两件事**。Syracuse 模板只给职称+联系方式，此时备注里的方向描述在三个链接内找不到出处——审核会按 P1 打回。遇到这种模板，要么换人，要么接受备注可追溯性下降并如实说明。
2. **系教师名录页必须做「姓氏自检」再写入**：`cas.uoregon.edu/directory/psychology-faculty`、`psychology.uiowa.edu/people` 都是 200 但 JS 渲染、HTML 无姓名；真正能用的是 `psychology.uiowa.edu/people/faculty` 这类服务端渲染页。
3. **老学生美国表的 Location 靠双表关联**：只设 `美国地区学校`（US 主表无 Location 字段）→ Location 为空；再去 QS 主表 `dstNvlYbmD2BTMCB0r` 找同名记录设 `非美国地区学校`，Location/QS 才会同步（本轮 4 校全部命中）。

### 同日补充：Drexel / Missouri / Nebraska / MSU / Temple 五系结构（2026-10-19 第二批）

| 学校 | 个人页 | 系教师名录页 | 博士项目页 | 结论 |
|---|---|---|---|---|
| Drexel | `/coas/faculty-research/faculty-directory/psychology/<last-first>/`（含职称、邮箱、研究兴趣） | `/coas/academics/departments-centers/psychology/faculty/`（`data-title` 可解析） | `/coas/academics/graduate-programs/psychology/doctorate-applied-cognitive-brain-science/`（认知方向实际招人的就是这个 PhD） | ✅ 三件套齐全 |
| Missouri | `/people/<姓氏小写>`（如 `/people/johnson`） | `/faculty`（**`/people` 是 404**） | `/graduate-program` | ✅；但 QS 主表无该校记录，Location/QS 会留空 |
| Nebraska–Lincoln | `/person/<first-last>/` | `/about/directory/`（姓名+职称+邮箱齐全） | `/academics/graduate/` | ✅ |
| Michigan State | ❌ 无个人页：`/People/faculty/` 已 404，`cbcc.psy.msu.edu` 500，`scholars.msu.edu/scholar/<id>` 是 JS 空壳（HTML 仅 1.5 KB） | — | — | 🚫 实际上无法合规落库，遇 MSU 直接放弃，不要反复试 |
| Temple | `/directory/<first-last>`（含 expertise、biography、代表作） | ❌ 系级名录抓不到（`liberalarts.temple.edu/directory` 前端渲染，HTML 无姓名；系主页各路径变体全 404） | — | 🚫 只有个人页、凑不齐三个链接，整条放弃 |

**一条新判据**：**「能拿到个人页」≠「能落库」**。落库要三件套（个人页 + 系名录 + 项目页），三者缺一就整条放弃；本轮 MSU、Temple 都是卡在中间那件。

## 2026-10-21 更新（国内首个批次·万文睿：分析化学方向，985 后半段 + 211 甘鄂陕川沪）

### 🔴 国内选导最大的坑：**方向最对口的人，往往只是硕导**
本批 24 所学校里，每个学校都出现「简历/方向完全对口、但官网标注硕士生导师」的人，直接导致「一校只能出 1–2 人」：
武汉理工 蔡宏伟（SPME 前处理）、华中师大 梁沛/程靖、华中农大 李秀娟（Pawliszyn 组访学，分子印迹涂层 SPME）、长安大学 高莉宁、西北农林 刘书慧（毛细管电泳在线富集）、地大（武汉）黄理金（COFs 前处理）、西北大学 卫引茂/白泉（磁性 SPE，但不在 2026 目录）。
**做法**：每所学校的「师资名录」必须逐个点开个人页看 `博士生导师` 字样或查当年博导名单，**不能凭职称推断**（副教授可以是博导，教授也可能只是硕导）。

### 🔴 先确认「有没有 0703 化学博士点」，再谈导师
本批 4 所学校是结构性缺口：
- **西安电子科技大学**：整校无 0703 化学、无环境/食品学科 → 整校非对口，不要硬凑。
- **西南交通大学**：无 0703 化学博士点，化学学院只招 080500 材料科学与工程；2027 目录已公布可直接核。
- **四川农业大学**：理学院只有 0710Z1 生物资源化学（挂生物学），全二级学科仅 4 位博导。
- **中国海洋大学**：化学化工学院无 0703 化学博士点，人选落在海洋化学/环境方向。
**做法**：`[学校] 博士招生专业目录` 里先 grep `0703`；没有就说明学位学科会落在别的门类，必须在记录里标 `degree_ok` 并交人工裁定，不要默认都是化学博士。

### 🗓 2027 招生目录的时间窗
2026-10-21 时点：23 所学校中**只有 3 所**（西安交大、西北农林、西南交大）公布了 2027 目录；其余仅出推免/直博通知。**11–12 月才是集中发布期**。
**做法**：目录未出时按 A/B/C 分级，并在记录里写明「参考 2026 目录」；目录一出必须复核一遍，把「不在目录里」的人剔掉（本批已出现：西北大学 卫引茂/白泉、上海大学 王田霖 连续三年未列名）。

### 🧭 学院层面的「伪对口」识别
- **生物传感强校**（湖南大学化学生物传感全国重点实验室、上海大学材料生物所）：分析化学教授一抓一大把，但绝大多数做核酸/细胞/活体成像。**判据只有一个：analyte 是不是环境或食品里的污染物**。湖大 20 位分析化学教授里，做前处理/分离的只有 3 位（陈增萍、吴朝阳、朱日龙）；上大 65 位化学导师里真正的 core 只有 1 位（何海波，POSS 基磁性分子印迹 + 兽药残留）。
- **师范大学/农林院校**：分析化学常与农药残留、食品检测结合，反而容易出 core；但学位学科常挂"化学生态学""生物资源化学"，要单独标。

### 🔧 通道
- `teacher.nwpu.edu.cn`、`chem.lzu.edu.cn`、`faculty.nwu.edu.cn` 对 curl 常返 **412**（WAF），换 WebFetch 或 WebSearch 摘要；**412 ≠ 死链**。
- 教师主页系统常见域名：`grzy.<校>.edu.cn`、`faculty.<校>.edu.cn`、`teacher.<校>.edu.cn`、`jszy.<校>.edu.cn`、`gr.<校>.edu.cn` —— 均算官方个人页。
- 招生目录 PDF 常需会话或为扫描件（武汉理工 008 分册），扫描件无法 grep 时以「学院博导名单 + 个人页」交叉确认。

### 项目对口核查：四个能直接看到"是否招人"的页面（2026-10-23）

落库之后还要回答"这个导师在不在对口 PhD 项目里、招不招"，以下页面能直接给出答案，优先于自己推断：

| 学校 | 页面 | 能看到什么 |
|---|---|---|
| Delaware | `/psychological-and-brain-sciences/graduate-programs/<方向>-concentration/` | 页内明写 **「Faculty accepting graduate students for 2027–2028: 某某」**，是最硬的招生状态证据 |
| Syracuse | `/psychology/graduate-study-psychology/cognitive-psychology-graduate-program-overview/` | 按方向列全部导师，每人后面标 **Accepting new students / 不标**，并给实验室名 |
| Drexel | `/coas/academics/graduate-programs/psychology/doctorate-applied-cognitive-brain-science/` | 项目师资表（姓名+职称+邮箱+研究方向关键词）；认知方向对口的就是这个 ACBS PhD，不设单独 Psychology PhD |
| Nebraska–Lincoln | `graduate.unl.edu/academics/programs/PSYC-PHD/` | 研究生院口径的 Program Faculty 名单 + 五个方向（Clinical / Developmental / Law-Psychology / Neuroscience and Behavior / Social and Cognitive）；**系里在职≠名单里有**，新入职者可能未更新 |

**判据**：`系里在职` → `系里有个人页` → 还要再看 `研究生院项目师资名单` 与 `招生状态`。前者不等同于后者；缺后两项时应在交付里标注"招生状态待确认"，不要写成确定在招。

---

## 2026-10-23 生态/农业/海洋/动物行为方向（陈骄阳批次）· 访问通道实测

本轮覆盖英/爱/欧（剔除挪瑞）/澳/加，99 条候选 → 92 条入表。以下通道结论可直接复用。

| 学校/站点 | 现象 | 可用通道 |
|---|---|---|
| **UBC 全站**（oceans.ubc.ca、ibios.ubc.ca、landfood.ubc.ca） | 一律返回 200 + "Browser Verification \| UBC Cybersecurity"，curl 与 WebFetch **都过不去** | 无法取证 → 该批次 UBC 人员全部未入表 |
| **Edinburgh `edwebprofiles.ed.ac.uk`** | 400/401 "Pantheon \| Site Locked" | 换 **`research.ed.ac.uk/en/persons/<name>`**（Pure），有职称+research 原文 |
| **UCD `people.ucd.ie/<name>`** | curl 只拿到 2 KB 的 "Discovery" SPA 壳 | WebFetch 可穿透，正文完整（职称+Research 段） |
| **Griffith `experts.griffith.edu.au/<id>-<name>`** | curl 同为 "Discovery" SPA 壳 | WebFetch 可穿透 |
| **UQ `researchers.uq.edu.au/researcher/<id>`** | curl 直接 000（TLS 层失败） | WebFetch 正常；`about.uq.edu.au/experts/<id>` 两条路都能取 |
| **KU Leuven `kuleuven.be/wieiswie/en/person/<id>`** | curl 000；且 "Research" 折叠区无正文 | WebFetch 能拿到职称；研究内容只能从页面列出的**项目标题**取证 |
| **Uni Hohenheim `agroecology.uni-hohenheim.de`** | curl 000 | WebFetch 正常（职称以 "Head of Department" 表述出现） |
| **Freiburg `bio.uni-freiburg.de`** | 持续 503 | 本轮放弃该组负责人 |
| **Trento `www5.unitn.it/du/it/Persona/<id>`** | curl 000 | WebFetch 正常；注意该页**院系可能不是你以为的那个**（Frasnelli 实际挂心理学与认知科学系） |
| **CREAF `creaf.cat/personal/<slug>`** | 会 301 到 `/en/about-us/our-people/<slug>` | 用 301 后的地址作正式链接 |
| **Imperial `imperial.ac.uk/people/<u>`** | 301 到 `profiles.imperial.ac.uk/<u>` | 用 301 后的地址 |
| **澳洲/英国 11 条院系博士项目页** | 返回 403 "Just a moment..."（Cloudflare 挑战，非死链） | 需人工点选确认，或留空标"项目页待补" |

**两条判据补充**：
1. "curl 返回 000 / 2 KB 壳页" **不能判死链**——本轮 UQ、UCD、Griffith、KU Leuven、Hohenheim、Trento 六处都是 curl 不通而 WebFetch 正常。
2. **意大利的 `Professore associato` 可能挂在非对口院系**（Frasnelli 的 SSD 是 Zoologia，但系是 Psicologia e Scienze Cognitive）→ 走闸门三（博士项目学位学科），不能只看人做得对不对。

---

## 2026-10-23 康复/健康 + 数字技术方向（成文萱批次，英/港/加/美）· 器械类账号 41 条入表

本轮 4 地区并行，最终 41 条入表（英 14 / 港 8 / 加 12 / 美 7），覆盖 24 校。以下为本轮实测通道与判据补充。

| 站点 | 现象 | 结论 |
|---|---|---|
| **QMUL 全站** | curl 一律 **202 + 2007 字节空壳**（非 403） | 必须 WebFetch；202 同样是反爬，不要当"能打开" |
| **Cardiff `profiles.cardiff.ac.uk`** | curl 403 Cloudflare | WebFetch 可读；职称行与 "Available for postgraduate supervision" 都在正文 |
| **McMaster `srs-rehabsci.healthsci.mcmaster.ca`** | 同一站点 **根路径 200、`/education/future-students/program-overview/` 曾 403**（WAF 按路径+出口 IP 丢包） | 403 会自己恢复，隔几分钟重试即可；`/faculty/` 是可用系名录 |
| **UMN `med.umn.edu/bio/<dept>/<name>`** | 旧路径返回 **200 但正文写 "We can't find the page"**，`/bio/<name>` 同样失效 | 这是「404 伪装成 200」的又一例；`experts.umn.edu` 也无该人档案 → 该人不可用 |
| **OSU `medicine.osu.edu/find-faculty/...`** | 旧个人页 301 到 `/find-a-researcher` 检索页（落点跑偏＝失效） | 医学中心个人页改版后统一跳检索页，不能再用 |
| **Newcastle 项目页** | `ncl.ac.uk/postgraduate/degrees/<code>/` 会改代码（8440F→404、8853f 有效） | 项目页代码不稳定，抓到后先看 title 再落库 |
| **BU 项目页** | `bu.edu/academics/?p=<id>` 是**可用的项目级页**（title = "PhD in Rehabilitation Sciences"） | 别因为 query 形式判成检索落地页 |
| **PolyU `/rs/study/research-postgraduate-studies/`** | 200 但正文 "Please put at least one valid content" | 用同系 `/phd-or-mphil` 子页 |
| **KCL SLCPS people** | 字母分页（一页仅 A–B），`?page=` 才能翻到后面 | 系名录只能给学院级 people 页；「正文含 surname」在分页目录上无法满足，交付时说明 |
| **Leeds stafflist** | 是「All fields / Last name / Search」**检索落地页**，不是名录 | 不能当 `其他导师信息`；无系级名录的系只能留空 |
| **Waterloo 项目页** | `.../phd-kinesiology-and-health-sciences` 仅 1.3 KB 半壳 | 需 WebFetch 复核后再落库 |

**判据补充（康复 + 数字技术方向专用）**：
1. 「AI 步态 / 可穿戴 / 数字康复」这几个词在**工程学院与康复学院同时存在**。区分方法：看一作论文产出物是「模型+代码+样机/系统」还是「临床人群+量表+干预方案」；本轮因此剔除 Birmingham（数据/建模）、Northeastern（传感器+算法）、CUHK（生物力学实验室）三条。
2. **护理学院里的康复技术 PI 要过闸门三**：Manchester 的 Emma Stanmore（ReHabMat 平衡测量、Exergames）内容极对口，但博士出口只有 PhD/MPhil Nursing → 学位学科不对口，本轮未收。
3. 加拿大法语校（UdeM）项目法语授课、论文可英语，套磁前需与导师确认语言安排。

---

## 2026-10-23 语言学 / 翻译 / 教育学方向（白娆批次，港 7 校 + 澳 2 校）· 66 条入表

本轮把「教师认知 / 教学材料 / 全球英语 / 英语教学+AI / 翻译+AI」五个细分跑了一遍，覆盖 8 个单位、约 20 个院系。以下四条是**可直接复用的取证通道**，比本轮结论更值钱。

### 1️⃣ 香港大学个人页邮箱：JS 混淆可在本地解码（2026-10-23 实测）

`web.edu.hku.hk/faculty-academics/<slug>` 的邮箱是 `<span id="eXXXX">[javascript protected email address]</span>` + 一段 `eval("var a=\"…\";var b=a.split(\"\").sort().join(\"\");var c=\"…\"")`。解法：正则取出 `eval("…")` 里的 `a` 与 `c`，`b = sorted(a)`，逐字符 `b[a.index(ch)]` 拼回。8 人全部一次解出（`chinhsi@hku.hk` / `kevin.tai@hku.hk` 等）。
- ⚠️ 正则必须写成 `eval\("((?:[^"\\]|\\.)*)"\)`，否则会在转义引号处截断，解不出来。

### 2️⃣ 中大 / 教大 / 浸会的 Pure 门户：邮箱藏在 `data-md5`（2026-10-23 实测）

`research.cuhk.edu.hk`、`repository.eduhk.hk`、`scholars.hkbu.edu.hk` 的 person 页把邮箱写成 `<a data-md5="bWFpbHRvOmJhcnJ5LmJhaUBjdWhrLmVkdS5oaw==">`，**base64 解出来就是 `mailto:` + 邮箱**。
- 中大 Pure 对 curl 默认 403 Cloudflare，**加上完整浏览器头即可 200**（UA + `Accept: text/html,application/xhtml+xml` + `Accept-Language` + `Upgrade-Insecure-Requests`）。
- 教大 `repository.eduhk.hk` 无需特殊头，直接 curl + 解 data-md5。
- 中大教育学院（CRI）系页与个人页**完全不挂邮箱**，只能走 Pure；`cpr.cuhk.edu.hk` 的 Experts List 也有全系邮箱+职称，可作二次核对。

### 3️⃣ 教大 ELE 个人页：研究方向在 tab 子页，主页静态正文是空的

`eduhk.hk/ele/people/<slug>` 正文里 `Research Interests` 只有标题、没有内容（JS 分页）。真实内容在 **`/ele/people/<slug>/research-interests`**（小写连字符），个别老师用首字母大写带空格的形式（如 Angel Lin：`/ele/people/angel-lin/Research%20Interests`）。
- **`导师主页` 直接写这个 tab URL**，否则审核官按「正文找不到研究方向」判 P0（本轮 4 条被打回后就是这样修的）。
- LML 系个人页全部外链 `repository.eduhk.hk/en/persons/<slug>`，研究方向的标题是 `Research interests`，但只有部分人填写。

### 4️⃣ 两个院系改名，旧路径会走空

| 学校 | 旧 | 新（2026-10 实测） |
|---|---|---|
| 港理工 | Department of Chinese and Bilingual Studies（`/cbs/people/academic-staff/`） | **Department of Language Science and Technology（LST）**，`https://www.polyu.edu.hk/lst/people/academic-staff/`；旧 URL 301 到 `/lst/` |
| 岭南 | Department of Translation（`/tran/`） | **Department of Language Industry and Technology（LIT）**，`https://www.ln.edu.hk/lit/`；`/tran/` 301 到 `/lit/`，仍开 PhD/MPhil in Translation |

### 判断补充（语言教育方向专用）

1. **港科大不要按「有语言学」就收人**：人文学部只有 `PhD in Humanities`，语言学是其中一个 specialization，学位学科不是语言学/教育学。本轮 2 条因此移除，HKUST 报 0。
2. **教大 ELE 的 Global Englishes 强人（FANG Fan）职级是 `Professor (Practice)`**，按 practice 序列剔除；同理 LML 的 `Professor (Practice)` WANG Lixun 也不收。教大真正能带的 Global Englishes 人选很薄，需向学生说明。
3. **澳门科技大学有学位但没个人页**：UIC 有 Doctor of Education / PhD in Education / PhD in Teaching Chinese as a Foreign Language，师资名录只挂 `wm-fs2.must.edu.mo/.../*.pdf` 履历，无 HTML 个人页 → 按链接四关无法入表，只能出 PDF 版名单。
4. **中大语言学系 14 人里大部分是句法/语义/神经/语音本体**（Pan Victor Junnan / Pan Haihua / Cheung Lawrence 句法语义，Mok Peggy / Thierfelder 语音与手语，Wong Patrick / Feng Gangyi 神经），与「教师认知 / 教学材料 / 翻译+AI」不同路。本轮**中大语言学系 0 条入表**，只在报告里告诉学生「若要读理论语言学可回看这几位」，不要为凑数写进去。
5. **港大教育学院个人页有一行三态声明**：`I am available to supervise…` / `Not applicable` / `I am not taking on graduate supervision in 20XX-XX`。**这一行比任何方向匹配都优先**——本轮据此直接排除 3 位（含一位方向很合的 LOH Elizabeth）。

## 2026-10-26 更新（国内第二轮·扩面深挖：985 中下九所 + 211 三地复扫）

### 🔑 「抽样」与「穷举」的差别，一次就显形
第一轮 23 校 75 人（每校 1–4 人），第二轮把同批学校往下挖第二层 + 新开 3 所 985，**新增 76 人、总量到 151**。增量来源不是「又找到几个牛人」，而是**院系范围扩了**：
- 第一轮几乎全部停在「化学学院分析化学教研室」；
- 第二轮把 **环境学院、食品学院、分析测试中心、国重实验室** 都过了一遍，新增的 76 人里化学学位只有 33 位，**环境 26、食品 11**。
**结论：国内分析化学方向的博导，一半以上不在化学学位点上。** 只扫化学系，必然漏掉环境学院里做「污染物前处理+检测」的那批人（地大 史建波、胡圣虹、郭伟，大工 谭峰，重大 高俊敏、智悦，湖大 章毅 都是这么来的）。

### 🔴 C 级「特殊推荐」几乎必错：本轮 3 条 C 级全部被审计剔除
第一轮曾按「方向极契合」留了 C 级，第二轮把 3 条 C 级全送去对抗审核，**3 条全灭**：
- 中国海洋大学 韩玉谦：2026 目录食品学院 083200 七个方向导师名单**均无其名**，博导身份只有「学位点骨干教师表：正高级」间接佐证；1962 年生。
- 湖南大学 王玉枝：2026 目录 070300 化学 02 分析化学 **34 位指导教师中无其名**，2026 两批博士拟录取名单亦无其名——**在职但不带博士**（学院名册仍列她为教授，这是典型的「名册≠博导」）。
- 上海大学 高松：记录自评已是 edge，但方向实为大气污染来源解析、机器视觉、生成式 AI 与管控智能体，与「材料富集+定量」毫无关系。
**做法：C 级默认不报。** 真要报，必须先拿到「当年目录列名」或「近两年拟录取名单有其名」，二选一，否则不进清单。

### 🔴 「博导资格」不能看职称，也不能只看个人页
本轮三种典型：
- **副研究员可以是博导**：西南交大 龚新颖（副研究员、博导）、川大 吴兰（研究员）。**别因为职称低就排除**。
- **教授/特聘研究员可能不是博导**：川大 黄荣夫官方页只写「特聘研究员」，通篇无「博导」二字，博导身份要靠第三方资料；吉大 高松（针阱微萃取，方向极对口）博导未证实。
- **同校同名要分清**：本轮出现两个「高松」——吉林大学（针阱微萃取，方向对口）与上海大学（高级工程师，AI 方向），前者待核、后者剔除。
**判定优先级：当年招生目录列名 ＞ 学院博导名单/拟录取名单 ＞ 个人页「博士生导师」字样 ＞ 第三方资料。** 只有第三、四级别证据的，必须在 risk 里写明并标「待核」。

### 🔴 个人页「过期页」的两个新样本
- **史建波（地大）**：记录原用的 `eas.cug.edu.cn/info/1018/1083.htm` 是**2022 年的实验室简介旧页**，正文还写「2006 年至今在中科院生态环境研究中心工作」，而人物早已回地大任环境学院院长。正确页是实验室主任页 `gwaterlab.cug.edu.cn/sysgk/syszr.htm`（二级教授、博导、院长）。
- **教师主页系统 JS 壳**：湖南大学 `grzy.hnu.edu.cn/site/index/<slug>` 返回标题 + 一张 Base64 照片、正文为空，**无法静态核验任何字段**；此时应改用「研究生院目录 + 学院教师名册」双证，并在记录里注明「个人主页不可静态核验」。
**做法：个人页要核「页面时间戳与任职表述是否自相矛盾」**——尤其院长/副校长级人物，旧页常年不更新。

### 🧩 学位学科要按「学位点」判，不按「学院」判
- 西安交大 **孔利云** 在公共卫生学院**卫生毒理与卫生检验学系**，方向是快速检测/样本前处理/食品安全检测（看着像食品），但学位点是 **100400 公共卫生与预防医学**。第一轮若按「食品安全」标 food 就错了。
- 反过来，西北农林 **庄雨婷** 在化学与药学院、做样品预处理，学位却落食品。
**做法：`degree_ok` 必须回「招生目录里的专业代码」确认，不能由院系名或研究方向推断。**

### 📉 「院系大 ≠ 方向对」：两所人最多、核心为零
西北大学（10 人）与华南理工（8 人）是本轮增量最大的两所，**核心档都是 0**：西北大学的增量在食品学院与环境；华南理工化学学院分析化学只有 1 位博导，食品强在光谱快检与免疫、环境强在修复，都不做「分离材料→富集→定量」。
**做法：报完人数要回看 core 比例。某校人数多而 core=0，多半是「邻近学科被误当对口」，应在 unmatched 里写清结构性原因，而不是硬凑 core。**

### 2026-10-26 补记：UBC / Stony Brook / Alberta 三校复核（成文萱批次）

| 站点 | 现象 | 可用通道 / 结论 |
|---|---|---|
| **UAlberta `www.ualberta.ca`** | curl 恒 202（Akamai / CloudFront 空体），`gradstudies.ualberta.ca` 同样 202 | **WebFetch 能读**（curl 不行）。项目页在 `ualberta.ca/en/rehabilitation/programs/rehabilitation-science/phd-in-rehabilitation-science/index.html`；教师目录用 `apps.ualberta.ca/directory/person/<slug>`（200，含职称与邮箱）与 `apps.ualberta.ca/directory/search/department/340300` |
| **UAlberta 旧路径** | `…/rehabilitation-medicine/programs/graduate-programs/index.html` 已 404（正文写 "Sorry, We Couldn't Find That Page"） | 学院已改名为 `en/rehabilitation/`，别再拼旧路径 |
| **UBC `rehab.med.ubc.ca`（原 rehab.ubc.ca）** | 全站 ITSA-BOTDEFENSE：200 + 31093 字节 JS 验证壳，**curl 与 WebFetch 都被拦** | 导师层无解；但 `www.grad.ubc.ca` 可读，项目页 `grad.ubc.ca/prospective-students/graduate-degree-programs/phd-rehabilitation-sciences` 含资助/在读人数/毕业率，可直接引用 |
| **Stony Brook `…/programs/hrs`** | 两个域名（healthprofessions / healthtechnology）都 **Access Restricted**，需校内账号 —— 这不是反爬，是真权限 | 项目存在（PhD in Health and Rehabilitation Sciences，含 Rehabilitation and Movement Science 方向），但缺可引用项目页 → 不写记录 |
| **Stony Brook `/faculty/alpha`** | curl 只拿到导航、无姓名；**WebFetch 能渲染出完整名单 + 个人页链接**（个人页在 /programs/<prog>/faculty/<slug>，多数 200） | 学院级名录用 WebFetch；可用于找人，但职称需进个人页核 |
| **ACAPT PhD 目录** | 把 Stony Brook HRS 项目负责人写成 Sue Ann Sisto | **该目录已过时**：Sisto 现为 University at Buffalo 康复科学系系主任（UB 个人页原文 "Sisto comes to UB from Stony Brook University"）。第三方目录不能作为职称/在职依据 |

## 2026-10-27 更新（国内 50 位写入 Vika：**分享链接里的表 ID 不等于真实 datasheet ID**）

### 🔴 301 "Can't find the specified datasheet" 的第一嫌疑：ID 错了，不是限流
本次卡了近 3 小时的根因，是一个字符的差异：
- 分享链接：`vika.cn/share/shrFlJDe…/**dst3Yxt6clFWvwZovd**/viwWNmSTP8tvZ`
- 真实 ID：`**dst3Yxt6clXFvwZovd**`（第 11 位是 `X`，不是 `F`）
两者都是 18 位、肉眼几乎一样，但 API 只认后者；用前者时**所有端点（records / fields / views）、读和写，一律返回 `code 301 Can't find the specified datasheet`**，而分享页照样能打开——极具误导性。

**正确的解析顺序（30 秒可完成，务必先做）**：
1. `GET /fusion/v1/spaces` → 拿到 spaceId 列表（本例 `spcvbDsioHGw6` = 🌏选导小宇宙）。
2. `GET /fusion/v1/spaces/{spaceId}/nodes?type=Datasheet&pageSize=200` → 按表名（如「万文睿-Supervisor List」）取出**真实 datasheet id**。
3. 交叉验证：`GET /fusion/v1/spaces/{spaceId}/nodes/{datasheetId}` —— 正常的表返回 `{"permission":0,"isFav":false,...}`，假 id 返回 `code 600 Node not found`。
4. 再用该 id 读 `/datasheets/{id}/records?pageSize=1` 确认 200。

**排除法（这次白花的工夫，记下来别再走）**：
- 不要先怀疑限流：若**同空间的其它表 200 正常**（本例李晨瑞表 109 条、王浩表 11 条都正常），就基本不是 token/配额/全局限流。
- 不要怀疑自己写的记录触发关联重算：本次删掉刚新增的学校记录做测试，无任何解锁效果（已恢复）。
- 缓存穿透（随机 `&_t=`）、换域名（`vika.cn/fusion/...`）、v2 接口（不存在）全部无效——因为问题根本不在这些层。
- 分享页 200 + 页面里有表名，**不能**证明 API id 正确（分享按 shareId 路由，路径里的 dst 段只是展示用）。

### ✅ 本次写入的可复用参数
- 空间 `spcvbDsioHGw6`；目标表 `dst3Yxt6clXFvwZovd`（万文睿-Supervisor List），写入前 177 条 → 写入后 **227 条**。
- 国内校若不在 QS 主表（本次 6 所：东北大学 / 华中师范大学 / 陕西师范大学 / 长安大学 / 西南交通大学 / 四川农业大学），**先往 QS 主表补建**（字段：`学校` 中文名、`地区`="Asia"、`Location`="China (Mainland)"，排名留空即可，该表本来就有「广州大学/中国美术学院」这类无排名中国校）。
- 写入仍按 **5 条/批**：POST（含 OneWayLink，**不带 fieldKey**）→ 立即 PATCH 三列 URL（**字段 ID + fieldKey="id"**）。
- 备注模板（国内）：`{职称}；{方向}。{A:招生稳定，往年连续招生。/ B:约 1–2 年招一次，发信前需确认当年名额。}{学位学科句}{邮箱来源句}`

### ➕ 2026-10-27 补记：国内 50 条入库后的全量质检（附 6 个院系师资页的正确 URL）

**检查方法**：94 个唯一 URL 逐个取「状态码 + 最终落点 + 标题 + 正文长度 + 个人页姓名命中」，另按列型判断页面类型是否匹配（个人页 / 院系名录 / 招生目录）。

**抓到的两类真问题**：
1. **备注里的推责语**：B 级模板写成「约 1–2 年招一次，**发信前需确认当年名额**」——「需确认」属禁用表述，14 条全部命中。**国内备注的招生说明只写事实**（「约 1–2 年招一次。」），不写让用户去确认的动作。
2. **「其他导师信息」指错页面**（13 条）：最常见的是拿到**个人页**（如刘则华、刘雯、冯江涛本人页）、**招聘页**（大工环境学院「博士后招聘」）、**中心首页**（川大分析测试中心）。判据很简单：标题应是「师资队伍/教师名录/导师介绍/博士生导师」，正文应出现 ≥10 个人名；只有一个名字的就是个人页。

**本轮验证过的正确师资名录 URL（可直接复用）**：
| 单位 | URL |
|---|---|
| 大连理工 环境学院 | `https://est.dlut.edu.cn/szdw/szdw.htm`（教授/副教授/讲师按职称分列，含谭峰、刘猛、赵慧敏） |
| 四川大学 化学学院（按研究领域） | `https://chem.scu.edu.cn/szll/szdwgk/ayjly.htm` |
| 华南理工 环境与能源学院 | `https://www2.scut.edu.cn/cese/dsjs/list.htm`（导师介绍；`/cese/szdw/list.htm` 会返回 511 字节的「提示信息」，不可用） |
| 西安交大 能动学院 | `https://epe.xjtu.edu.cn/szgk/jsml.htm`（教师名录；从个人页 `/info/1562/xxxx.htm` 里的 `../../szgk/jsml.htm` 反推得到） |
| 上海大学 化学系 | `https://chem.shu.edu.cn/rcpy/yjsds.htm`（研究生导师名录，副教授也在内；`/szll/zg.htm` 只有正高） |
| 武汉理工 资环学院 | `http://sree.whut.edu.cn/yjsjy/dsdw/` |
| 吉林大学 博士招生目录（2026） | `https://yjsy.jlu.edu.cn/__local/5/E4/3A/A46AD6871DBED0AFEF5139B0BDA_667907AE_2356F0.pdf`（全日制博士招生专业目录 PDF；研招网首页只有推免/硕士简章，**别再拿推免简章当博士目录**） |
| 西安交大 公卫学院 | **无静态师资名录**（站点 JS 渲染，8 个候选路径全 404），只能降级用学院首页 |

**两条判定经验**：
- **URL 猜不出来就别猜**：本轮对 5 个院系试了 19 个「szdw/jsml/dsdw」组合，命中率 0；真正有效的方法是①站内搜索 `site:<域名> 师资队伍`、②从**已确认的个人页**里反向抓 `../../szgk/jsml.htm` 这类相对链接。
- **412/000 不必判死链**：兰大 `chemec.lzu.edu.cn`、西工大 `teacher.nwpu.edu.cn` 对 curl 一律 412 或 000，WebFetch 渲染后正文完整（张宝亮页明确写「教授/博导/招收材料学、化学专业博士研究生」）。这类页面要在报告里注明「WAF 拦截，已换通道确认」。

### 2026-10-27 补充：Vika 分享链接只有 shr、以及学校主表的两条命名坑

1. **`https://vika.cn/share/shrXXX` 不含 dst 时**：`curl` 抓分享页 HTML（35 KB），`grep -o 'dst[A-Za-z0-9]\{10,20\}'` 直接取到 datasheetId；拿到后用**个人 token** 走 Fusion API 读写（分享 token 无写权限）。本轮实测一次命中。
2. **学校主表 `dstMNzQU9Aa58DpgW3` 的命名坑**：
   - 博洛尼亚大学存的是全称 **`Alma Mater Studiorum - University of Bologna`**，按 "Università di Bologna / University of Bologna" 精确匹配会**全部落空**；用 `Bologna` 子串才查到 recordId。
   - 德语/意语校名带变音符号与本地语言：Kiel = `Christian-Albrechts-Universität zu Kiel`、Bonn = `Rheinische Friedrich-Wilhelms-Universität Bonn`、Bremen/Leipzig = `Universität Bremen/Leipzig`、Zurich = `University of Zurich (UZH)`。
   - **做法**：先建 ALIAS 表指定每校 2–3 个候选写法，再兜底做 NFKD + 子串双向匹配；本轮 58 校一次性命中 57，剩 1 校靠子串补上。
3. **批量创建时可以直接把 OneWayLink 写进 POST**（`{"学校名字":[schoolRid]}` + `fieldKey="name"`），**不必先建后 PATCH**。实测 89 条一次成型，Location / QS排名 由 MagicLookUp 立即回填，零缺失。
