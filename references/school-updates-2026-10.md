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
