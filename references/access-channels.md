<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：站点访问通道实测记录：curl 与 WebFetch 的真实差异、先读 sitemap 找院系页、港澳与澳新抓取通道情报、别名/同人判定、维格分页上限、备注雷同度检查尺度、auditor 结论回验
> **什么时候读**：某校页面抓不到、curl 被拦、需要判断该用哪条通道时；写港澳/澳新院校前；排查「链接打得开但内容不对」时
> **什么时候不用读**：已知该校通道正常且不在港澳/澳新范围内时；只做 Vika 字段格式写入时（转 notes-and-fields.md）；只要查某校条目（转 school-registry-* 对应分册）

---

## 🔎 找院系页的最快通道：先读 sitemap.xml（2026-09-24 验证有效）（自 SKILL.md 迁入 2026-10-07）


当院系页/seo 结构不明、或站点改版导致老路径全 404 时，**不要去猜 URL，直接读 sitemap**。

```python
# 1) robots.txt 里通常写着 sitemap 位置
GET https://<site>/robots.txt            # -> Sitemap: https://<site>/sitemap.xml
# 2) sitemap.xml 可能只是索引，需再下一层
GET https://<site>/sitemap.xml           # -> <sitemapindex> 指向 main-sitemap.xml 等
GET https://<site>/main-sitemap.xml      # -> 真正的 <loc> 列表
# 3) 用正则把 URL 归类，一次看清全校组织结构
locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)
schools = sorted({m.group(0) for u in locs if (m := re.match(r"https://<site>/…/school/[^/]+/", u))})
```

实战体量参考：Adelaide `sitemap.xml` 1.36 MB / 11,002 条 URL；UOW `main-sitemap.xml` 542 KB / 4,946 条。**一次抓取换掉几十次盲猜**，比逐条试路径便宜得多。
注意：`sitemap.xml` 这类大文件偶发连接失败（urllib 返回 status 0），**必须带 3–4 次重试并落盘**。

#### Adelaide University（2026 改版后的真实结构）

```
https://adelaide.edu.au/about/school/<school-slug>/            # 学院首页
                                     .../our-people/           # 学院「Our people」
                                     .../our-research/         # 学院研究
                                     .../our-study-areas/      # 学院学习领域
https://adelaide.edu.au/about/college/engineering-and-information-technology/   # 学部
```
- 学院 slug 就是学院名 kebab 形式，例如 `electrical-and-mechanical-engineering`、`chemical-engineering`、`civil-engineering-and-construction-management`。全校共 29 个 `/about/school/` 条目。
- ⚠️ **学院 `our-people/` 只列院长等领导层**（SEME 只有 2 人），**不是完整师资名录**；学院也没有独立的 staff-list 子页（sitemap 里 SEME 只有 7 个页面）。因此「其他导师信息」填这个学院页即可——它至少是**该导师所在学院自己的页**，优于全校 `/people/`。
- **该校没有院系级博士项目页**。博士项目统一用 `https://adelaide.edu.au/study/degrees/doctor-of-philosophy/`（学位自己的页面，含入学要求/结构/申请）。别再填研究生院 hub（`/research/graduate-research-school/`）。
- 权威个人页仍是 `researchers.adelaide.edu.au/profile/<first.last>`（含 `Eligible to supervise Masters and PhD as Principal Supervisor`）；`adelaide.edu.au/people/<first.last>` 也可用。
- ⚠️ 老路径 `adelaide.edu.au/engineering-computer-mathematical-sciences/...` 与 `.../school-electrical-mechanical-engineering...` **全系列 404**，不要再用。

#### University of Wollongong（组织结构更正，重要）

⚠️ **不要因为搜不到 `School of Mechanical, Materials, Mechatronic and Biomedical Engineering` 的官网就判定「MMMB 系页面 404、名录页不合格」。**

UOW 工程学部（Faculty of Engineering and Information Sciences）**对外的 School 只有 3 个**：
- School of Computing and Information Technology
- **School of Engineering**
- School of Mathematics and Physics

「机械·材料·机电·生物医学」只是 **School of Engineering 内部的研究方向/学科分组**（在 `scholars.uow.edu.au` 的个人页里仍写作 `School of Mechanical, Materials, Mechatronic and Biomedical Engineering`），**没有独立网站**。
→ 所以 `https://www.uow.edu.au/engineering-information-sciences/school-of-engineering/our-people/` **就是正确的系级师资名录页**，无需替换。该页还会给出所有学术人员的**官方职称**（如 `Senior Professor Gursel Alici`、`Dr Winson Lee`），是核对职称最权威的一页。

- **博士项目页**：`https://www.uow.edu.au/research/graduate-research/future-students/higher-degrees-by-research/`（HDR 学位页）。不要填 `/research/graduate-research/` 这个研究生院 hub。
- **个人页**：`https://scholars.uow.edu.au/<slug>`（JS 渲染，urllib 4150 字节壳，**WebFetch 可读**），另有 `https://scholars.uow.edu.au/display/<firstname_lastname>` 会 301 到前者。页内有 `AVAILABILITY: Masters Research or PhD student supervision`。
- ⚠️ **邮箱在个人页顶部联系区块（ORCID / 电话 / 邮箱 / 单位），该区块是动态渲染的，WebFetch 有时能拿到、有时拿不到**。兜底顺序：① 同一 `<slug>` 下换 `/about`、`/grants`、`/publications` 子页重试；② 用站点限定搜索（`allowed_domains=["uow.edu.au","scholars.uow.edu.au"]`）确认官方页联系区块内容。
  ⚠️ 注意 UOW 邮箱有**新旧两套命名**：新式 `firstname_lastname@uow.edu.au`（`gursel_alici@`、`emre_sariyildiz@`、`chin-hsing_kuo@`、`winson_lee@`），旧式拼音缩写（如 Winson Lee 早年用 `ccwlee@uow.edu.au`）。**旧地址仍散落在各种 2020 年前后的招生帖里，不要采信**——若索引到的联系区块显示的是新式地址，说明抓取时序是新的，可用。

#### AMBER 组页 = 判断整组对口性最省 token 的一页

`https://uow.edu.au/research/advanced-manufacturing-technologies/applied-mechatronics-biomedical-engineering/`
一次给出：组使命方向原文（含 "Rehabilitation robotics"、"Mechanisms design and their application in biomedical engineering"）、**每位成员的研究方向原文**、以及**历届与在读博士生的课题标题**（如 "Soft Lower Limb Exosuit Design and Control"、"Wearable gait retraining"、"Model-based Analysis of Cerebral Palsy Gait in Children"）。
→ 先读这一页，再决定要不要逐个打开成员个人页，能省掉大量无效抓取。
**同类用法**：Auckland 的 Mechatronics doctoral 页（`.../mechatronics-engineering/doctoral.html`）也带 "Our people + Past research topics | Supervised by …" 双清单，等于一份「谁带过什么题」的现成证据。

#### 别名/同人判定：先查邮箱再合并

`scholars.uow.edu.au` 上同一人可能存在两个 slug（如 `display/winson_lee` 与 `winson-lee`）。**合并前先用 ORCID、电话、邮箱三者比对**，不要仅凭姓名相似就判同人；反之亦然——**姓名拼写不同（`Manish Sreenivasa` vs `Manish Narsipura Sreenivasa`）也可能是同一人**，要用 ORCID 确认。

---


---

## 港澳·澳新院校抓取通道情报（2026-09-24 王润泽第三轮沉淀）（自 SKILL.md 迁入 2026-10-07）


#### 香港

| 学校 | 通道与要点 |
|---|---|
| **CityU MNE** | 全站 WAF：**urllib 返回 212 字节壳，WebFetch 可完整读取**。师资名录 `cityu.edu.hk/en/mne/people/academic-staff`（注意要带 `/en/`），个人页 `.../mne-faculty/<slug>`。系级博士项目页 `cityu.edu.hk/catalogue/pg/202627/programme/MNE_P.htm`。 |
| **PolyU ME** | 个人页 `polyu.edu.hk/me/people/academic-teaching-staff/<slug>/`（urllib 可读，但正文在 2600 字符之后，需定向取 `Area of Specialization:`）。项目页 `polyu.edu.hk/study/pg/rpg/20263/me`。注意页面上 `Prof. XXX` 只是称呼，**职称要看 `Area of Specialization` 上方的头衔行**（如 ZHANG Dan 实为 `Chair Professor of Intelligent Robotics and Automation`）。 |
| **CUHK MAE** | 个人页真身是 `www4.mae.cuhk.edu.hk/peoples/<slug>/`（`?p=NNNN` 会 301 过去）。名录页 `.../people/academic-staff/`。**从名录页抓 `peoples/` 相对链接可一次拿全 45 位教师个人页**，比逐个搜省得多。项目页 `.../research-postgraduate-programme/`。 |
| **HKUST MAE** | 个人页 `facultyprofiles.hkust.edu.hk/profiles.php?profile=<姓-名-姓>`（可读）或 `mae.hkust.edu.hk/en/people/faculty/detail/<姓-名>`（可读，但导航很长，需定向取 `Research Interests`）。**注意 `Primary Faculty` 一页只列正聘，不含 affiliated/adjunct/emeritus 的独立名录页**，无法穷尽。 |
| **HKU DASE（原 IMSE）** | 名录页与个人页都是 JS 渲染：**urllib 常返回 0/空，WebFetch 可读**。项目页 `dase.hku.hk/teaching-and-learning/prospective-students/mphil-phd`。 |
| **HKU ME** | 个人页 `mech.hku.hk/academic-staff/<slug>/` 导航极大（500KB+），正文在 `Contact us Facebook Instagram` 之前约 2600 字符处 → 用 `rfind` 定位再往前取。 |
| **HKBU** | Physics / CS / Chemistry 三个系整体无「自供能康复机器人」对口（物理系两人命中柔性电子红线、一人命中材料红线）。 |

#### 澳门

- **UM（澳门大学）**：`feg.um.edu.mo/eme/academic-staff/` 可读（注意结尾斜杠）；个人页 `feg.um.edu.mo/people/<uid>/`。项目页是 `feg.um.edu.mo/eme/phd-programme/`——**`feg.um.edu.mo/eme/degrees/phd/` 会错误 301 到土木系**，别用。IAPME 全院为材料，直接排除。

#### 港科广（HKUST-GZ）

- `facultyprofiles.hkust-gz.edu.cn/faculty-personal-page?id=NNN` 是 **SPA 空壳（1522 字节）→ 不能作为入库依据**。
- 替代可用：`sysh.hkust-gz.edu.cn/?p=60/`（若为领导页）与 `sysh.hkust-gz.edu.cn/zh/about-systems-hub/our-people/faculty/`（**用 WebFetch 可拿到全院教师表，每行含「详情」= facultyprofiles 链接；但该链接仍是空壳**）。
- ⚠️ **一页含多位主任**：ROAS 领导页同时放了 Acting Thrust Head（Jun MA）与另一位教授（黄强）的主任寄语，**单次抓取可能只命中其中一段**——不要据此判定「页面无此人」（本轮 subagent 与我自己的第一次抓取都踩过）。
- 结论：**港科广的教授若只有 facultyprofiles 个人页，实际上无法取证录入**，应列入待补或改挂学院/学域页并在报告中说明。

#### 澳洲

- **Auckland（奥大）**：`profiles.auckland.ac.nz/<slug>` 是 JS 渲染（urllib 4150 字节），**WebFetch 可完整读取**。页面固定含 `GRADUATE SUPERVISION: PhD/Doctoral Accredited Supervisor` 与 `Has Current Supervision Opportunity` —— **招生资格的直接证据，务必顺手记进备注**。
  - slug 就是姓名的 kebab 形式（`k-aw`、`v-sorokin`、`andrew-mcdaid`、`minas-liarokapis`），但**会有失效 slug**（`a-mcdaid` 404），先 WebSearch 拿准确 URL。
  - 系名录页：`auckland.ac.nz/en/engineering/about-the-faculty/engineering/mechanical-engineering/contacts.html`（标题 "Our people"）。项目页：`auckland.ac.nz/en/study/study-options/find-a-study-option/mechatronics-engineering/doctoral.html`（同时是全系 People 与历届博士课题列表，**可一次看到导师带过什么题**）。
  - ⚠️ `profiles.auckland.ac.nz` 上可能出现**已转任 Honorary 的人**（本轮 Minas Liarokapis 页面首行即 `Honorary Academic`）——职务行不是 Professor 就不能按 Faculty 收录。
- **Adelaide（阿德莱德/Adelaide University）**：官网 2025-2026 改版，`adelaide.edu.au/engineering-computer-mathematical-sciences/...` 全系列 **404**。
  - 权威个人页：`researchers.adelaide.edu.au/profile/<first.last>`，页内含逐字 research interests 与 **`Eligible to supervise Masters and PhD as Principal Supervisor`**（vs 无资格时只有 `Projects leading to a research degree are available`）。
  - ⚠️ 该域名有 **SSL legacy renegotiation 问题**：urllib 时通时不通（报 `URLError`/返回 16 字节），**WebFetch 稳定可读**。
  - 人员目录 `adelaide.edu.au/people/`；研究生院 `adelaide.edu.au/research/graduate-research-school/`。**院系级师资名录页与院系级博士项目页都没找到**（本次用上述两页替代并在报告中注明）。
- **UOW（伍伦贡）**：`scholars.uow.edu.au/<slug>` 是 JS 渲染（urllib 4150 字节），**WebFetch 可读**，页内含 `AVAILABILITY: Masters Research or PhD student supervision`。
  - ⚠️ **School of Mechanical, Materials, Mechatronic and Biomedical Engineering 的官网页面 404**（`/school-of-mechanical-materials-mechatronic-and-biomedical-engineering/...` 各种写法都试过），只能用 `uow.edu.au/engineering-information-sciences/school-of-engineering/our-people/` 作名录页，需在报告中注明。
  - AMBER 组页 `uow.edu.au/research/advanced-manufacturing-technologies/applied-mechatronics-biomedical-engineering/` 一次给出全组成员与组方向原文（含"Rehabilitation robotics""Mechanisms design and their application in biomedical engineering"），**是判断该组是否对口最省 token 的一页**。
  - ⚠️ 注册在 `scholars.uow.edu.au` 的 `AVAILABILITY` 与个人页职称可能不一致，**职称以个人页标题行为准**。

#### 澳新 QS 前 200 的口径校验（2026-09-24）

topuniversities.com 已切到 2027 版，**不要用它判 2026**。QS 2026（本轮实核）：Melbourne 19 / UNSW 20 / Sydney 25 / ANU 32 / Monash 36 / UQ 42 / Auckland 65 / UWA 77 / Adelaide 82 / UTS 96 / RMIT 125 / Macquarie 138 / Curtin 183 / Wollongong 184 / Otago 197。**超出 200 的**：Deakin 207、QUT 226、Newcastle 227、Massey 230、La Trobe 233、Victoria Wellington 240、Canterbury 261、Griffith 268、Waikato 281、Swinburne 294、Tasmania 314、Flinders 387、WSU 400、AUT 410。
（注意：Flinders 的 Youhong Tang 是澳新最贴近 TENG 的学者之一，但 QS 387 出局——**范围硬门优先于方向匹配**。）

#### 🔧 维格主表分页上限 1000 行（2026-09-24 实测）

`GET /datasheets/{main}/records?pageSize=500&pageNum=N` **最多只能取到 1000 行**，第 3 页起返回空。用「全表扫描后建学校名索引」的做法会漏掉排名靠后的学校（本轮漏了港科广）。
**正确做法**：校验学校关联时改用 `GET /datasheets/{main}/records?recordIds=<rid>&cellFormat=string` 逐校精确查询——快且不会漏。
配套：`import_to_vika.py` 的学校解析必须用 recordIds 查询，不要依赖全表扫描。

#### 📝 备注雷同度检查的正确尺度（2026-09-24）

跨备注 15 字重复片段**不都是问题**，两类应放行：
1. **skill 规定的固定句式**（如 `未明确表明监督资格，可以后放～`）——多位 RAP 记录共用是设计使然。
2. **官方原文的事实性引述**（如 AMBER 组使命原文 `机构设计及其生物医学应用`）——那是 substance，不是套话外壳。
真正要改的是**连接语/评语壳**：`重合度比较高`、`都沾到`、`契合度` 这类（属机器打分语，要删）。`能搭上` 是 skill 明确允许的方向关联描述，**不要误删**。
同理，`可以备选一下呢～` 是 skill 规定的备选标识，**审核官若把它当"推销腔"报 P0，是误报**。

#### 🧑⚖️ auditor 结论必须逐条回验（2026-09-24）

本轮 auditor 报出的问题里，**至少两条是误报**：① 声称某导师个人页「不含职称」（实际页面标题下第二行就是 `Research Assistant Professor`）；② 把 skill 明文允许的 `可以备选一下呢～` 判为违规。**审核官不持有 skill 文本**，所以它只能按通用写作规范判断。
反向也成立：auditor 能抓到我们自己的真错——本轮它查出我把另一位老师的招生语「自费的也欢迎」误安在了 KANG Wenbin 头上（那句话其实出自 LINGHU Changhong 的 Position Available），是实打实的 P0。
**处理原则**：auditor 的每条结论都回到「我自己抓过的原文」里比对一次，再决定改不改；改完把被证伪的误报记下来，避免下轮重复劳动。

---


---

## 🌐 抓取通道实测补充（2026-09-24）（自 SKILL.md 迁入 2026-10-07）


| 现象 | 真相 | 做法 |
|---|---|---|
| 页面 200、正则却 0 命中姓名，疑似 SPA 空壳 | **多数是 gzip 响应体没解压**（southampton.ac.uk 等） | 读 `Content-Encoding` 头，命中 `gzip` 就 `gzip.decompress`；同时显式发 `Accept: text/html,application/xhtml+xml,*/*`。修正后 27 个 Southampton 个人页全部命中姓名 |
| `cityu.edu.hk/stfprofile/<slug>.htm` curl 返回挑战页 | Incapsula WAF | **WebFetch 可穿透并读到完整研究方向 + 论文列表**，不要因 curl 失败就剔除 |
| `profiles.ucl.ac.uk/<id>` curl 只回 11 字节 | SPA 壳 | WebFetch 可读（UCL 个人页内容完整） |
| `www.durham.ac.uk/staff/<slug>/` curl 返回 202 + 159 字节 | JS 挑战 | **WebFetch 可读到正文**（2026-09 实测成功，含完整 Research 段落）；不要沿用旧结论直接剔除 |
| `profiles.uts.edu.au/<name>` curl 只回 278 字节 | SPA | WebFetch 可读，页面直接给出 AVAILABILITY 与奖学金细节 |
| `researchers.adelaide.edu.au` / `researchers.mq.edu.au` 个人页 | 本轮 curl 直读正常（未触发反爬） | — |

**⚠️ Vika URL 字段回读是对象，不是字符串**：`{"text": "...", "title": "...", "favicon": ""}`。回读校验必须取 `.text`，否则会把全部记录误报成「导师主页与预期不符」。

**⚠️ 「课题组/研究中心人员页」不是错误链接**：本 skill 明确规定 `其他导师信息` 可填「该导师所在**院系或课题组**的教师名录页」。所以南安 ORC 分组的 HCF 名单、Bath 的 Optical Fibres Group members、Macquarie 的 MQ Photonics persons 都合规；auditor 若按「必须是系级名单」判定为 P0，属于**审核口径过窄的误报**，复核时要挡回去。

**⚠️ 写脚本常见迭代 bug**：`cands = {c['name']: c for c in list}` 之后写 `for c in cands`，迭代到的是 **key（字符串）**，再取 `c['name']` 就 `TypeError: string indices must be integers`。用 `cands.values()` 或直接迭代原始 list。

**⚠️ 主表同校多条重复记录**：同一所学校在主表里常有多条、QS 排名不同（Newcastle 137/180、Macquarie 133/138、QMUL 110/140、Bath 132/150）。**优先沿用表内既有条目所用的 recordId** 保持一致，并在交付报告里点名「显示排名超出区间系主表重复条目所致，需机构侧合并去重」——不要因为显示排名超界就删人。

---


---

## 学校站点访问通道：本机 curl 与 WebFetch 的实际差异（2026-09-20 实测）（自 SKILL.md 迁入 2026-10-07）


同一批任务里 100+ 个主页逐条核验，**先 curl 批量筛，再对非 200 / 无姓名命中的换 WebFetch 复核**是最省成本的组合。分类如下：

#### A. curl 被拦、WebFetch 可读（用 WebFetch 复核后即可写入）

| 站点 | curl 现象 | 说明 |
|---|---|---|
| `cityu.edu.hk/chem/people/...`（港城化学系） | 200 + 约 850 字节 Incapsula 挑战页 | WebFetch 可读到完整姓名/职称/Research Interests |
| `osc.wp.st-andrews.ac.uk/people/` | 403 | WebFetch 一次可拿到全部中心成员的研究方向原文 |
| `scholars.uow.edu.au/display/...` | 200 + "Discovery" JS 空壳（约 4 KB） | WebFetch 可读，且页面含 `AVAILABILITY: Masters Research or PhD student supervision`（**招生资格的直接证据，值得顺手记下**） |
| `profiles.warwick.ac.uk/...` | 同上 JS 空壳 | 改用 `warwick.ac.uk/fac/sci/chemistry/staff/<slug>/` 这类系级个人页（curl 可直接读） |
| `www.umass.edu/chemistry/about/directory/<slug>`、`mseg.udel.edu/people/<slug>/`、`www.empa.ch/...` | 403（Cloudflare / Azure WAF） | WebFetch 可读 |

#### B. 换了通道也读不到正文（**不要用第三方平台硬凑，直接剔除并记录**）

| 站点 | 现象 | 处理 |
|---|---|---|
| `www.durham.ac.uk/staff/<slug>/` | 202 + "JavaScript is disabled… verify that you're not a robot" | WebFetch 只能拿到姓名+职称，**拿不到研究方向原文** → 本轮 4 位 Durham 候选被剔除，报告中单列 |
| `www.chemistry.utoronto.ca/...` | 403 Forbidden（WebFetch 同样 403） | 剔除 |
| `profiles.newcastle.edu.au/...`、`experts.exeter.ac.uk/...` | JS 空壳且无姓名命中 | 纽卡斯尔可用 `newcastle.edu.au/profile/<slug>`（WebFetch 可读到姓名/职称，但研究方向要另找中心页） |
| `www.ualberta.ca/science/...` | 202 反爬 | 改用 `apps.ualberta.ca/directory/person/<shortname>`（curl 可读） |

#### C. 两个易踩的技术点

1. **Adelaide `researchers.adelaide.edu.au` 报 `SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED`** → 不是坏链。Python 里加一行即可：`ctx.options |= ssl.OP_LEGACY_SERVER_CONNECT`。该页还会直接给出 `Eligible to supervise Masters and PhD as Principal Supervisor`。
2. **主页 200 但没有导师姓名 ≠ 页面无效**：EPFL 的实验室页（如 `/labs/fimap/`）只有课题组内容、不含 PI 姓名 → 换 `people.epfl.ch/<first.last>`；ETH 的 `mat.ethz.ch/research/research-groups/...` 路径已废 → 换 `polychem.mat.ethz.ch`；KIT 的个人页换成 `itcp.kit.edu/<姓>/` 这类课题组页。**核验时要检查页面正文是否出现导师姓氏，而不是只看状态码。**

#### D. 排名口径：加拿大不要用 Maclean's 判"前 200"

美国学校用主表 `最新排名` 里的 `USNEWS xxx` 直接筛（本机可脚本化，直接列出 40–80 的候选校池，效率极高）。
**加拿大主表的排名字段是 Maclean's（医博类第 N / 综合类第 N），无法用来判"前 200"**——学生说"前 200"时按 **QS 世界排名**口径逐校核对，否则会把 QS 211/219 的学校（如卡尔加里、渥太华）误收进来。同理，德国/澳洲/英国也都是 QS 口径，主表 `最新排名` 就是 QS 数字，可直接筛。

##### ⚠️ 排名必须用「学生表实际关联的那张主表」判，不要用别的表（2026-09-21 踩坑）

**同一份数据里可能同时存在多张学校主表，排名口径和数值都不一样**，用错会直接误判：

| 主表 | 排名字段 | 例：纽卡斯尔大学 | 例：特拉华大学 |
|---|---|---|---|
| `dstX9F8Qy3QHfJCmJS`（旧） | `最新排名`（单列文本，QS/USNews 混写） | 179（在 200 内） | USNEWS76（在 40-80 内） |
| `dstMNzQU9Aa58DpgW3`（规范表，2200+ 校） | `2027年QS排名` / `2026年QS排名` / `2026年USNews排名` 三列独立 | **244 / 227（超出 200）** | **USNews 88（超出 80）** |

**正确做法**：拿到学生表后，先 `GET /datasheets/{ds}/fields` 找到 `OneWayLink` 类型字段（通常叫「学校」），读它的 `property.foreignDatasheetId` —— **那才是权威主表**。然后：

- 用该表的 **QS 最新年份**（有 2027 就用 2027）判英/澳/瑞/德/加的"前 200"；
- 用该表的 **`2026年USNews排名`** 判美国的 40–80；
- 学校名要按该表的 `学校全称`（主）/`学校中文名`/`学校英文缩写` 三个字段做**归一化匹配**（去 `\xa0`、去变音符、折叠空格），常见差异举例：`The University of Adelaide` → 规范名已改为 `Adelaide University`（阿德莱德与南澳合并）、`ETH Zurich - Swiss Federal Institute of Technology` → `ETH Zurich (Swiss Federal Institute of Technology)`、`Queen Mary University of London` → `Queen Mary University of London (QMUL)`、`The University of New South Wales (UNSW Sydney)` → `The University of New South Wales`。

**别忘了一件事**：学生可能在任务中途**换一张新表链接**说"填到这个表里"。这通常是把同一份列表复制到模板更规范的另一个空间（新表可能挂规范主表、带有 QS/USNEWS 两个独立 lookup 列）。接手时：

1. 解析新 `datasheetId`，**先探一条写入**（旧表可能因空间超限写不进去，新表所在的另一个空间往往能写）；
2. 读新表已有记录，与旧表基线做**集合比对**（正常是完全一致，说明是同一份列表的副本，本次只需写增量）；
3. 用**新表挂的主表**重新跑一遍排名口径校验，可能因此增删个别人选（本例就多剔了 2 位超范围的导师）；
4. 新表字段更全（多出 `导师研究领域`、`QS`、`USNEWS`），写入时按字段名匹配即可，第 1 步的 payload 基本可复用，只需换 `datasheetId` 和新的学校 recordId 映射。


---

## 🇬🇧🇪🇺 英国 + 欧陆建筑/土木类院校抓取实测（2026-10-21，张天钰第二轮 41 条）

| 学校 | 主站状态 | 可用通道与要点 |
|---|---|---|
| KTH | `www.kth.se/profile/<slug>?l=en` **curl 返回 302** 到 `/files/auth/silent/bounce`（JS 认证） | **用 cookie jar 随跳转即可拿到 200**：`curl -sL -c ck.txt -b ck.txt --max-redirs 6`。职称在 `id="profileName"` 后第一个纯文本行。WebFetch 也可读 |
| TUM | `cee.ed.tum.de/...` 503 / 000 | 改用官方个人页库 **`www.professoren.tum.de/en/<姓>-<名>/`**（200） |
| Manchester | `www.manchester.ac.uk` 会整站返回 **503 "Under maintenance"**（维护期数小时） | Pure 门户 **`research.manchester.ac.uk/en/persons/<slug>`** 全程可用，可核人名/职称/邮箱/研究领域；`博士申请信息` 只能等主站恢复 |
| TU Delft | `www.tudelft.nl` 同一波故障返回 **503** | **`research.tudelft.nl/en/persons/<slug>`** 与 `/en/organisations/<unit>/persons/` 全程可用（Pure），可核人名/职称/邮箱；个人页无叙述性简介时取 `Fingerprint` 关键词并注明来源 |
| KU Leuven | `wieiswie` 个人页被 ICTS 状态页拦截，返回 **429 + 跳 `status.kuleuven.io`** | 属站点级故障，**进待重试，不要硬凑职称** |
| KIT | `kit.edu`、`tmb.kit.edu`、`bgu.kit.edu` 全站 **"Currently not available"**（站方因 PHP 漏洞主动下线） | 整校进待重试 |
| UCD | `people.ucd.ie/<slug>` 是 Discovery 类 **JS 壳**（约 2 KB，无姓名） | 无 API 可挖 → 待重试，不得据此入库 |
| Uppsala | staff 页是 `?query=` 目录查询页 | 不是个人页，不能当 `导师主页` |
| Imperial | CEE 系无建设管理方向 | Laing O'Rourke 系相关人员多为教学岗（Research/Teaching Fellow）或兼职教授，按职称硬门排除 |
| KCL | **无土木院系** | 建设法中心授法学博士，不合学科口径 → 判无对口 |

**批量核验提醒**：`scripts/audit-all.py` 在 **90 条规模**上运行超过 20 分钟无输出（疑卡在链接检查阶段）。大规模表可先用自写机械检查过一遍（备注正则 / 职称位括号 / 第三方主页 / `博士申请信息` URL 去重 / 八列空值 / QS 回填），再对小样本跑脚本。

## 🔁 2026-10-22 全表体检补充（90 条 / 11 校）

| 学校 | 现象 | 正确通道 |
|---|---|---|
| ETH Zurich | `im/sc/cea.ibi.ethz.ch/people/person-detail.<ID>.html` → **200 但正文 "Person not found"**；人员目录页 `people.html` / `personen.html` 是 JS 空壳，列表拿不到 | **`https://ethz.ch/en/utils/search.<同一 base64ID>.html`**（200，完整档案）。ID 可从旧 person-detail URL 里直接取（`MTY5NDQ2` 等） |
| Edinburgh | `eng.ed.ac.uk` 全站 **401 `Pantheon \| Site Locked`**（含个人页 / 项目页 / 名录页） | 个人页 `https://www.research.ed.ac.uk/en/persons/<slug>`（**裸域名 research.ed.ac.uk 无 DNS，必须 www**）；项目页 `https://study.ed.ac.uk/programmes/postgraduate-research/947-engineering`；名录 `https://www.research.ed.ac.uk/en/organisations/school-of-engineering/` |
| PolyU | 并发抓取会整片超时（000），单线程 3–4s 间隔可稳定 200 | 顺序 + 间隔 ≥3s；个人页 slug 必须从 `/cmi/people/academic-staff/` 的 `href` 取 |
| Manchester | `www.manchester.ac.uk` **整站 503 Under maintenance**（持续数日）；`research.manchester.ac.uk/en/organisations/.../persons/` 被 Cloudflare 403 | 个人页 `research.manchester.ac.uk/en/persons/<slug>` 正常 200；项目页只能等主站恢复，勿改 URL |
| TU Delft | `research.tudelft.nl/en/organisations/.../persons/` Cloudflare 403，**个人页 200 正常** | 名录页可保留（浏览器可开）；姓名命中检查要按标题 `A.C. den Heijer` 这种缩写形式比对，否则误判 |
| KTH | `www.kth.se/profile/<slug>?l=en` 无 cookie 返回 302；`/directory/a/ai/aid?l=en` 需 cookie 才是 200 | **必须 cookie jar**：`curl -sL -c ck.txt -b ck.txt --max-redirs 6`。该 directory 页标题为 `Construction & Facilities Management \| Staff directory`，**是合格的系级名录页**，不要当搜索页判掉 |
| UCL | `profiles.ucl.ac.uk/<id>-<slug>` 是 SPA 壳（恒 3327 字节）；`www.ucl.ac.uk` 对 curl 403 | 用 `https://profiles.ucl.ac.uk/api/users/<id>`：`positions[0].position` 给职称、`tabSummaryAbout.value` 给研究简介（HTML，需 strip）、`customFilterFour` 含 `Supervision of research degrees` 即标示可带博 |

**UCL 带博证据三源**（本轮验证）：① `/api/users/<id>` 的 `customFilterFour`；② `https://www.ucl.ac.uk/bartlett/construction/people/phd-students` 页的在读博士生导师团队名单（35 人中 24 人命中，**这是最硬的证据**）；③ 个人页明文。

## 🇬🇧 英国扩校抓取实测（2026-10-23，张天钰第三轮 17 条 / 8 校）

| 学校 | 现象 | 做法 |
|---|---|---|
| Durham | `durham.ac.uk` 对 urllib 一律 **202 + 0 字节**（bot challenge），个人页与 staff 页都如此 | 换 **WebFetch** 可完整读取。判「站点挂了」之前必须先过一遍 WebFetch |
| Imperial | 同上（202 + 0），且 `civil-engineering/people/academic-and-research-staff/` 是 **404**，正确入口走 `engineering/departments/civil-engineering/...` | 先用 WebFetch 打开系首页看研究主题，再决定是否判「无对口」 |
| Bristol | 个人页 `bristol.ac.uk/people/person/<Name>-<uuid>/` 200；**Pure 名录页 `research-information.bris.ac.uk` 对 curl 403**（Cloudflare） | 名录页浏览器可开，保留；姓名命中检查会误判，改用页面标题判层级 |
| Birmingham / Nottingham / Leeds | 系师资名录页**客户端渲染**，HTML 里只有 1–2 条，grep 姓名必落空 | 不要据此判「名录页不对」；看 `<title>` 是否为该系 People 页即可 |
| UCD | `people.ucd.ie/<slug>` 对 urllib 只回 **2120 字节 JS 壳**；`ucd.ie/civileng/people/...` 404 | **WebFetch 能渲染**，可拿到姓名/职称/邮箱/BIO；正式链接就用 `people.ucd.ie` |
| KIT | `tmb.kit.edu` 已恢复；个人页邮箱常被混淆成 `sekretariat [at] tmb kit edu` | 教授个人页只给秘书处邮箱属正常，填秘书处地址并在备注注明 |

**判定「无对口」的证据标准**（本轮 18 校）：必须写出「该院系的研究组/研究主题清单」，例如 KU Leuven 40 人只归 5 组（建筑物理、材料与结构、结构力学、水工岩土、测绘）、TCD 土木 24 人分 5 支柱（能源、环境、岩土、结构、交通）。只写「没找到」不算证据。

**Warwick 特别提醒**：WMG 的 Complex Programme Management 教授 Naomi Brookes 已离职（现为 Leeds 的 Visiting Professor），在职的 Rezaei、Kapogiannis 均为 **Teaching Focussed**，按职级硬门不能收 —— 这类「名头在、人已走」的情况要用在职名单复核，不能靠记忆或旧资料。
