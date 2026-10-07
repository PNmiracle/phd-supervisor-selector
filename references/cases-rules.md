<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载 -->
> **本文含**：案例复盘、定级数据表、某校特殊规则明细、批量处理方法论——即从原 `critical-rules.md` 中剥离出来的「非规则」部分。**本文不含任何「写入前必读」硬规则**，硬规则全部在 `rules-write.md`。
> **什么时候读**：① 某校抓不到页面时按校名 grep 定位；② 用户报链接问题要查历史复盘时；③ 要批量补字段（文章链接 / 实验室 / 邮箱）时；④ 遇到用 `rules-write.md` 判不了的边界情形时。
> **什么时候不用读**：⚠️ **禁止整读**。本文是案例库不是规则书，写入前不需要读。只要判某条规则怎么做 → `rules-write.md`；只要调 Vika API → `vika-guide.md`。
> **已知重复**：C1/C2/C3 与 `school-registry-us-ca.md`、`school-registry-hk-mo-cn.md`、`access-channels.md` 存在重叠，后续收敛时应向分册归并，不要在这里继续追加。

---

# 案例 · 数据 · 明细（cases-rules）

> 本文由 `critical-rules.md` 于 2026-10-07 拆分而来。硬规则见 `rules-write.md`，学校关联六步操作见 `vika-school-link.md`。

## A. 定级数据

### A1. Stipend 官方数字参考（2025-2026 学年）

表格中常见的 stipend 数据存在系统性偏差，下表为逐校核实后的官方数字。**新批次仍须重新核实，本表只用于对照可疑数据。**

| 学校/项目 | 常见错误数据 | 官方数据 | 偏差 |
|----------|------------|---------|------|
| CWRU BSTP | ~$37K+/yr | **$38,000** | 轻微低估 |
| OSU BSGP | ~$34K/yr | **$33,980** | 基本准确 |
| UB PPBS | ~$32K/yr | **$31,000-$35,000**（来源不一）| 在范围内 |
| TAMU Medical Sciences (Medical Physiology) | ~$32K/yr | **$35,000** | **-$3,000** |
| TAMU Genetics | ~$32K/yr | **$32,000** | 准确 |
| USF Medical Sciences | ~$30K/yr | **$37,000** | **-$7,000（严重）** |
| Rochester GDSC/CMPP | ~$35K/yr | **$35,100** | 基本准确 |
| UW-Madison CMB | $37K+/yr | **$37,000** | 基本准确 |

**关键教训**：
- USF Medical Sciences 的 stipend 被系统性严重低估（$30K vs 实际 $37K）
- TAMU 不同 track（Medical Physiology vs Genetics）stipend 不同，不能统一填写
- 不同来源（学校官网、研究生院、具体项目页面）的数字可能不一致，需标注来源

## B. 案例复盘

### B1. 大规模 404 复盘（2026-07-14）

黄肇启选导任务中，60 条记录的 `博士申请信息` 和 `其他导师信息` 出现大面积 404。三个根因：

**根因 1：URL 猜测（占 90%+）** — 所有出错 URL 都是在写表时按路径命名规则直接构造的，没有经过 WebSearch 验证：

| 字段 | 猜测的路径 | 真实路径 |
|------|-----------|---------|
| HKU SAAS 博士申请 | `/programmes/research-postgraduate` | `/programme/rpg/mphil-phd` |
| HKU Nursing 博士申请 | `/education/postgraduate/` | `/education/doctor-of-philosophy-programme` |
| CUHK SPHPC 博士申请 | `/programmes/` | `/mphil-phd-programme/` |
| HKUST ECE 博士申请 | `/pg/` | `/admissions/postgraduate` |
| HKUST LifeSci 博士申请 | `/programmes/` | 在 `prog-crs.hkust.edu.hk` 子域名 |
| HKU BS 博士申请 | `/programmes/research-postgraduate/` | `phd.hkubs.hku.hk/admissions/...` |
| PolyU Nursing 博士申请 | `/sn/study/` | `/study/pg/rpg/2026/sn` |
| HKU SAAS 院系列表 | `/staff` | `/staff_teaching.php` |
| HKUST CSE 院系列表 | `/people/faculty/` | `/admin/people/faculty/` |
| HKUST LifeSci 院系列表 | `/people/` | `/faculty-members/` |
| HKUST ECE 院系列表 | `/people/` | 无系级列表页，用 `facultyprofiles.hkust.edu.hk` |
| HKUST Math 院系列表 | `/people/faculty/` | 无系级列表页，用 `facultyprofiles.hkust.edu.hk` |

**核心教训**：博士申请信息页和院系列表页的 URL 结构在各校各系之间**没有统一规律**。`/programmes/`、`/people/`、`/staff`、`/pg/`、`/study/` 这些常见路径在大量真实站点上都是 404。必须先 WebSearch 搜到真实页面再写进表，一步都不能省。

**根因 2：大学网站持续重组** — CUHK SPHPC 的院系列表页从 `/people/` 迁到 `/academic-staff/`，原 URL 直接 404。这类重组是常态，不是偶发事件。

**根因 3：CityU WAF 干扰诊断** — CityU 全站 Incapsula WAF 使自动化工具看到的返回码异常（403/404/超时/空壳），容易与真 404 混淆。必须区分「WAF 拦截」（全站系统性问题）与「真 404」（URL 本身失效）。

**更早的一次教训（2026-07-07）**：12 个「其他导师信息」链接中 **4 个已失效**（NUS × 2、NTU × 1、CityU × 1），原因同样是大学重组了网站结构。**旧记录里的 URL 永远不能当作已验证。**

### B2. SPA 壳经典案例

- **CUHK STA（2026-07-13）**：`/people/faculty/{name}/` 所有 URL 返回完全相同的 114KB 首页 HTML（SPA 壳），浏览器 JS 加载后才显示个人内容。**正确格式是 `/peoples/{slug}/`**（静态 HTML，可直接验证研究方向）。详见 `school-registry-hk-mo-cn.md` CUHK 章节。
- **HKUST(GZ)（2026-07-23）**：`facultyprofiles.hkust-gz.edu.cn` 全站 SPA，所有页面返回完全相同的 1522 字节 HTML 壳。URL 格式从 `?name=XXX` 查询参数改为 `/faculty-personal-page/NAME/shortname` 路径格式，但两种格式 SPA 行为一致。**自动化工具无法区分旧 URL 失效与新 URL 有效——200 ≠ 内容正确。** DSA 学域的替代来源为 `dsa.hkust-gz.edu.cn/blog/YYYY/MM/DD/name-slug`（WordPress 格式，可直接抓取内容）。

### B3. CityU 离任导师被误判为「有效」的案例（2026-08-04）

> **本节的规则（WAF 现状 / 403 判读 / 离任三步检测 / 链接格式选择 / 写后复验 / 审计豁免）统一维护在
> `school-registry-hk.md` 的 CityU 条目**——那里是执行搜索时按校名打开的第一落点。
> 本节只留案例经过与旁证，不再重复规则。

**触发**：审计一笔 CityU 记录时，`scholars.cityu.edu.hk` 返回 403。当时的分册口径只写了「403 是 WAF 正常现象，不要删记录」，于是这条被放过。**实际该教授的页面已经被删除（已离任）**——403 在这里不是反爬，是页面不存在。

**发现方式**：三步交叉验证（穿透 WAF 看正文 → 查 CityU 学术人员目录 → 查系级现任教职员列表）。穿透后 `scholars` 页显示 "The page does not exist"；学术人员目录里该人被标为 **Visiting Professor**；系级现任教授/副教授/客座/兼任三组均无此人。

**旁证**：WebSearch 该导师姓名 + 原校，南京大学官网写明「原香港城市大学创意媒体学院教授（2012 年至 2024 年）」。

**这次案例的产出**：分册里「403 一律当作 WAF 正常」的口径被作废——**状态码判不了这件事，必须穿透看正文**（具体规则见分册）。


### B4. CUHK(SZ) 教师 URL ID 不稳定（2026-07-23 验证）

CUHK(SZ) 数据科学学院的 `sds.cuhk.edu.cn/teacher/XXX` 的 ID 不是稳定标识符。2026 年 7 月大规模重组中，同一学院教授被分散到多个子域名和路径格式：

| 变化类型 | 示例 | 旧 URL | 新 URL |
|----------|------|--------|--------|
| teacher ID 变更 | 李爽 | `/teacher/273` | `/teacher/472` |
| 路径格式切换 | 王子卓 | `/teacher/254` | `/node/59` |
| 跨子域名迁移 | 罗智泉 | `sds.cuhk.edu.cn/teacher/478` | `sse.cuhk.edu.cn/teacher/184` |
| 个人网站 | 丁宏强 | `sds.cuhk.edu.cn/teacher/378` | `myweb.cuhk.edu.cn/chrisding/Home/Index` |

**要点**：① 每次会话重新搜索，不信任上次存的 ID；② 不能按旧 ID 推断新 ID（无规律）；③ 同一学院同时存在 `/teacher/XXX`、`/node/XXX`、`myweb.cuhk.edu.cn`、`gklbdc.cuhk.edu.cn`、`sse.cuhk.edu.cn`、`mscfe.cuhk.edu.cn` 等多种格式；④ **Python SSL 握手失败 ≠ 链接失效**——`sds.cuhk.edu.cn` 在 urllib 报 `SSLV3_ALERT_HANDSHAKE_FAILURE`，但 WebFetch 与浏览器可正常访问，先用 WebFetch 测再判死。

## C. 某校特殊规则明细

### C0. 「排名带内是否有对口博士项目」实测名单（2026-09-20）

用户说「先看 USNews 60-100」时**不要默认这个区间里的学校都有会计博士**。实测一整轮：USNews 2026 排名 60-100 的学校里，逐校实开项目页后**只有 3 所**（Rutgers 75 / Drexel 80 / CU Boulder 97）确有会计博士；同区间被硬门排除 8 所——**Delaware、American、Howard、NC State、Marquette**（均无商科博士或会计不在其中）、**UIC**（Accounting 方向官方目录写 `Admission ... is suspended`）、**Binghamton**（PhD in Management 现行只列 Finance/LOS/Marketing/MIS，**未列 Accounting**）、**RPI**（会计不在当年招生学科）。

其他要点：
- 「学院有会计系 / 有会计教授」≠「有会计博士项目」。Delaware、American、Howard 都有会计系，但一个会计博士都没有。
- **项目页写了 ≠ 当前招生**：GWU 有 accountancy 博士项目，但博士页曾出现「no longer accepting admissions for Fall 2026 or Fall 2027」；Fordham 的 PhD 页只举例 finance / management，未显式列 Accounting。这类一律标「存疑」不写入。
- 「项目存在」之外还要看**方法与范式是否对口**：Minnesota Carlson 有会计博士且师资强，但项目页自述 "#1 in analytical financial accounting"（分析式理论），对排斥纯理论的学生要在备注提示「本项目允许分析式或实证两种研究范式」。
- 「关键词撞上但方法不对口」最隐蔽，必须落到**个人主页的方法学描述**判断：同一所 UvA，Veenman / Thuerheimer 是归档实证，而 Kroos（管理会计）、Maas（行为会计）、O'Dwyer（质性）即属偏离；UOW 会计组整体偏社会/环境/批判会计；VU 的 Anna Gold 是行为审计（实验+质性）。发现偏离时**保留记录但如实写明方法**并加「可以备选一下呢～」。

### C1. 美国大学站点访问通道与 WAF 绕过（2026-09-20 沉淀）

美国部分大学对自动化工具（curl / urllib）返回 **403（Cloudflare/WAF）或 000（域名不通）**。遇到时**不要直接判死或跳过**，按 L1 curl/urllib → L2 WebFetch → L3 WebSearch 逐级尝试。

**已验证「curl 403，但 WebFetch 可读」**

| 站点 | curl | WebFetch | 备注 |
|---|---|---|---|
| `bme.engineering.gwu.edu` / `www.bme.seas.gwu.edu`（GWU BME） | 403（Cloudflare） | ✅ 可读 | `bme.engineering.gwu.edu/faculty-directory` 能读全系名单；个人页偶发被拦，用 WebSearch 兜底 |
| `www.ecs.baylor.edu`（Baylor 工程与计算机学院） | 403 | ✅ 可读 | WebFetch 该页能直接拿到 `ecs.baylor.edu/person/<slug>` 个人页链接 |
| `bme.udel.edu`（Delaware BME） | 403 | ✅ 可读 | 同上 |

**已验证「整个域名本机不通（000），须换该校其他域名」**

| 学校 | 不通的域名 | 该用的域名 |
|---|---|---|
| Indiana University Bloomington | `ise.iu.edu`、`eng.iu.edu` | **`luddy.iu.edu`**（Luddy 学院站，ISE 系在此，个人页格式 `luddy.iu.edu/people/<姓>-<名>.html`） |
| Howard University | `engineering.howard.edu` | **`profiles.howard.edu`**（个人页 `/<slug>`）、**`cea.howard.edu`**（学院人员列表）、**`gs.howard.edu`**（研究生院项目页） |
| Michigan State University | `engineering.msu.edu`、`egr.msu.edu`（curl 与 WebFetch 均失败） | 只能靠 WebSearch 取线索；若导师有独立实验室站（如 Jinxing Li 的 `labli.net`）可用独立站作「导师主页」，但须在备注与报告中如实说明该 URL 未能在本机验证 |

**关键原则**：
1. **403 ≠ 链接失效，但也 ≠ 链接有效**。必须换通道穿透读正文，确认页面含该导师姓名/职称/方向，才算核验通过。
2. **先读院系名单页、再提取个人页 href**：让 WebFetch 输出每位 faculty 的 href，比猜 URL 后缀可靠得多（Howard 的 `profiles.howard.edu/<slug>`、IU 的 `luddy.iu.edu/people/<姓>-<名>.html` 都是这样拿到的）。
3. **URL 有效但本机不可验证时必须如实标注**（如 MSU 申请页 URL 系按搜索索引推断），不得当作「已验证通过」。
4. **第三方平台的任职信息必须回官网复核**：本轮靠 CV/ORCID 查出 Howard 的 Tao Wei 已转南卡罗来纳大学、MSU 的 Peter Lillehoj 已转 Rice，而 LinkedIn / Aminer / ApplyKite 等仍标原校。凡来源为第三方平台的导师，一律回官方 profile 或官方 CV 交叉确认。
5. **无对口博士项目 ≠ 无对口导师**：核验一所学校前先确认其博士项目是否真存在（如 SMU 只有 M.S. Biomedical Instrumentation，博士仅设机械/电气/运筹；Baylor 的 BME 只是机械系下的方向）。若项目不对口，即使有对口导师也不写入，并在反馈中说明原因。

### C2. 港澳院校博士语言门槛与导师资料入口（2026-09-20 实测，符日星案例）

港澳任务的**第一决策变量是语言门槛**（大量学生无雅思托福，或只想走中文项目）。下列口径全部来自当场打开的官方页面，写备注时可直接引用。

**语言门槛速查（不同学院差别极大，务必逐校核对）**

| 学校 | 门槛 | 官方依据要点 |
|---|---|---|
| **香港都会大学 HKMU** | **可绕开** | 「The English language proficiency requirements are **not applicable to** applicants who will work on a Chinese Language education topic, **or whose thesis is to be presented in Chinese**」；另有「waived if the applicant's previous studies at the **Bachelor's degree or above level** adopted English as the medium of instruction」。入口 `hkmu.edu.hk/tc/admissions/research-postgraduate/entry-requirements/` |
| **澳门城市大学 CityU Macao** | **可绕开** | 文化产业研究博士页脚原文「**註：授課語言為中文及英文**」+「**論文可以中文或英文撰寫**」，全页无英语硬门槛。⚠️ **不要写成「中文学制，无需雅思托福」**——官网口径是中英文授课，写「中文学制」属失真 |
| **澳门科技大学 MUST** | **可绕开** | 传播学博士 / 数字媒体博士项目页授课语言栏为「中文/英文」，**未列语言成绩**。入口 `fa.must.edu.mo/programmes/program/view/id-200.html`（传播学）、`id-199`（数字媒体） |
| **北师香港浸会大学 UIC/BNBU（传播学博士）** | 🔴 **严格（易写错）** | **传播学博士全英文授课，只认托福 79 / 雅思 6.5，不接受大学英语六级**。流传很广的「CET-6 500 + CET-SET 口语 B 可替代」**仅适用于理工科技学院开设的专业**，不要套到传播学博士上（2026-09-20 首轮真实写错过）。入口 `gs.bnbu.edu.cn/graduate/graduate1/yjxyjskc/Communication.htm` |
| **港科大 HKUST（清水湾）** | ⚠️ **只认本科学位** | 官方 FAQ `fytgs.hkust.edu.hk/admissions/faq` 的豁免条件**只有「本科学位为英文授课」**；「硕士学位为英文授课能否豁免」在该页**只有提问标题、没有答案**（即官网未确认）。同校社会枢纽页 `soch.hkust-gz.edu.cn/?p=51/` 写「硕士（或以上）英文授课亦可免」，与研究生院口径冲突。**首轮写成「官方 FAQ 明示硕士英文授课亦可免」属过度解读，已更正** |
| **港科大（广州）HKUST(GZ)** | ⚠️ 口径冲突 | 研究生院页 `fytgs.hkust-gz.edu.cn/adm-req` 只写「**bachelor's degree** … medium of instruction was English」；社会枢纽课程页 `soch.hkust-gz.edu.cn/?p=51/` 写「硕士（或以上）英文授课亦可免」。**两处口径不一致：备注里两说并陈并附链接，不要单取一侧** |
| **澳门大学 UM** | ⚠️ 分院系 | 官方 PDF `grs.um.edu.mo/wp-content/uploads/Academic-Units-English-Language-Proficiency-Requirements-for-PhD-Programmes-2526.pdf`：社会科学学院博士「CET 6 score of 500 or above is accepted」，**但「For PhD in Communication, the requirement of IELTS score must be 6.5 or above with no sub-score lower than 5.5」——传播学博士不能用六级替代**。⚠️ 极易写错：不要笼统写「社科学院六级可替代」 |
| **香港中文大学 CUHK（新传博士）** | 严 | 雅思 **7.0** / 托福 **92**（高于研究生院一般标准）。入口 `gs.cuhk.edu.hk/programmes/social-science/phd-communication` |
| 港大 / 港理工 / 港城大 / 港浸会 / 岭南 / 教大 / 港中深 | 常规需雅思托福 | 逐校研究生院页面 |

**导师资料入口（实测可用）**
- **澳科大 MUST**：博导按方向分组名单页 `fa.must.edu.mo/person/id-744.html`（传播学）、`id-736.html`（数字媒体）、`id-735.html`（电影管理）、`id-732.html`（设计学）。**每位导师的「导师主页」即 `wm-fs2.must.edu.mo/...pdf` 官方简介**，须下载后用 `pypdf` 抽取（WebFetch 读 PDF 返回乱码）。名单页标「教授，兼職博導」者为校外兼任，一律排除。
- **香港都会大学**：RPG 招生页 `admissions.hkmu.edu.hk/rpg/as` **一次给出全院导师姓名 + 职称 + 研究方向关键词**（最省 token）；个人页为 `www.hkmu.edu.hk/as/people/staff-profile/?email=<login>&unit=AS&po=N`。
- **岭南大学 DACI**（数码艺术及创意产业系，2024 年由 Visual Studies 改组）：`ln.edu.hk/daci/staff/faculty`，是港澳「数字文化 + 创意产业」密度最高的一个系。
- **UIC/BNBU 文化与创意学院**：师资页 `scc.bnbu.edu.cn/en/staff/members.htm` 为 JS 渲染；教授个人简介可用 `bnbu.edu.cn/info/<id>.htm` 形式的官方页。

- **只给有「不需要英语成绩」通道的学校写**。符日星这批保留 4 所共 30 条：香港都会大学（选中文论文即不适用英语要求）、澳门城市大学、澳门科技大学（中英文授课、项目页未列语言成绩）、澳门理工大学（报考条件未列英语要求）。

**抗抓站点（curl 失败但 WebFetch 可穿透，勿判死链）**：`hkmu.edu.hk`（403）、`eduhk.hk`（SSL legacy renegotiation）、`myweb.cuhk.edu.cn` / `hss.cuhk.edu.cn` / `gs.cuhk.edu.cn`（SSL handshake）、`cityu.edu.hk`（WAF 返回 83 字节壳）、`soch.hkust-gz.edu.cn`（经代理偶发 502）。

**Vika 写入两步法（2026-09-20 确认，可复用）**：一次请求**不能混用** `fieldKey="name"` 与 `fieldKey="id"`。新建记录因此分两步：
1. **POST** `/records`，`fieldKey="name"`，只带文本字段 + `OneWayLink`（值必须是数组）→ 拿 `recordId`；MagicLookUp（Location / QS排名）会自动填充。
2. **PATCH** `/records`，`fieldKey="id"`，只带 URL 字段的**字段 ID**（`导师主页` / `博士申请信息` / `其他导师信息`）。
3. 每批 5 条，逐批校验返回条数；任一批返回 0 条立即停。

### C3. 港澳／内地合办院校抓取与语言门槛情报（2026-09-21 第二轮沉淀）

**BNBU（北师香港浸会大学，原 UIC）**
- **个人页直接可抓**：`https://staff.bnbu.edu.cn/<username>/cn` 为**服务端渲染**，正文含「姓名 / 职称 / 邮箱 / 办公室 / 主要任职 / 交叉任职 / 研究领域 / 教育背景 / 导师类型」。`<username>` 从 `https://staff.bnbu.edu.cn/unit/SCC/cn.html` 与 `.../unit/FHSS/cn.html` 的成员链接取（这两个 unit 页本身是 AJAX 空壳，抓不到列表，只能从 WebSearch 摘要或个人页 slug 猜测后逐个验证）。
- ⚠️ **约 1/4 的教师个人页没有「研究领域」栏目**（实测 41 人中 11 人缺失：黄煜、许夏营、朱润萍、王元新、欧文杰、胡帆、Anilesh Kumar、董天策、庞胜楠、闫虹、Lin Zhu）。**缺这项就不能录入**——`导师研究领域` 必须来自页面原文，`/en` 英文版同样没有。
- ⚠️ 少数页面「研究领域：」标签会**重复出现两次**，解析时要允许跳过重复标签，否则整段被误判为空（黄小薇就是这种情况）。
- **部分页面带「导师类型：博士」字段**，这是带博资格的正面证据，务必写进备注（实测：Geuntae PARK、周超、计雨含、云启栋、吴晓苹）。
- 🔴 **语言政策极易搞错（2026-09-21 更正）**：BNBU **传播学博士**（人文社科学院，官网 `gs.bnbu.edu.cn/graduate/graduate1/yjxyjskc/Communication.htm`）**所有课程全英文授课，语言要求只有托福 79 或雅思 6.5，不接受大学英语六级**。那个流传很广的「CET-6 500 分 + 口语 B 可替代雅思托福」**仅适用于理工科技学院开设的专业**。**不要再把六级政策套到传播学博士上**（这是首轮真实犯过的 P0）。
- 文化与创意学院（SCC）**自身没有博士项目**；该院教授可进入人文社科学院的传播学博士导师名单（庄以仁、原源均在名单内）。

**香港科技大学（广州）HKUST(GZ)**
- `https://facultyprofiles.hkust-gz.edu.cn/faculty-personal-page?id=xxx` 是**纯前端渲染**（1522 字节壳，WebFetch 也读不到内容）→ **不可作为入库依据**。UGOD / IPE 学域的教师只有枢纽名单页（`soch.hkust-gz.edu.cn/academics/ugod/faculty/`、`.../ipe/faculty/`，可读，含姓名/职称/邮箱，但**无研究方向**）→ 这批人**无法填 `导师研究领域`，不要录入**，写进待补清单。
- ✅ **CMA（计算媒体与艺术）学域例外**：`https://cma.hkust-gz.edu.cn/faculty-regular/<slug>/` 是 WordPress、服务端渲染、可读，含职称/邮箱/Research Areas。slug 列表从 `https://cma.hkust-gz.edu.cn/faculty-regular/` 的**相对 href** 提取（`href="/faculty-regular/xxx/"`）。
- 🔴 **语言口径两处不一致（2026-09-21 复核实测）**：港科大官方 FAQ 的豁免条件**只有「本科学位为英文授课」**；页面里虽有一个「硕士学位为英文授课能否豁免」的**提问标题，但没有对应答案**。社会枢纽页另写「硕士（或以上）英文授课亦可免」，与研究生院口径冲突。引用时必须对准导师所属枢纽（CMA 属信息枢纽，只有本科口径适用）。

**香港中文大学（深圳）CUHK-SZ**
- 域名对 urllib 会 **SSL handshake failure**，**必须用 WebFetch**。
- 个人页两套：`https://myweb.cuhk.edu.cn/<user>`（英文，Name/Title/Research/Email 齐全）与 `https://hss.cuhk.edu.cn/teacher/<id>`（中文，研究领域用分号分隔）。**`hss.cuhk.edu.cn/teacher/<id>` 的 id 不稳定**，每次重新搜。
- HSS 下设「计算社会科学学科部」，是计算传播集群的集中地；跨文化交流学科部的教学序列（Assistant Professor (Teaching)）**不具博导资格**。

**澳门**
- **USJ（圣若瑟大学，澳门）不在统一主表**（主表里的 USJ 是黎巴嫩的 Saint Joseph University of Beirut）→ 按「表格隔离 vs 建校取舍」规则**不写入**，进待补清单。该校 `Doctor of Global Studies` 官网列名 14 位博导，数字媒体艺术方向对口。
- **MPU（澳门理工大学）在主表**（`Macau Polytechnic University`）。该校**没有设计学／视觉艺术博士**；对口的是**文化遗产与人类学博士**（`mpu.edu.mo/eschs/zh/phd_cha.php`，授课语言中文／英文，报考条件页未列英语要求）。艺术及设计学院的教师**个人页只有研究主题标签、没有研究领域表述**（`research.mpu.edu.mo`，对 urllib 返回 403，用 WebFetch），录入前要斟酌。

**抓取通用坑**
- **别用英文名去匹配中文页面**：BNBU `/cn` 页标题是中文，用 `Mei Wu` 去命中「吴玫」必然假阴性，会误判成「页面无内容」。**正确做法是解析页面自身的字段行**（`English` 之后依次是 姓名 / 职称），而不是拿外部名字去 `in` 判断。
- 校园网个人页的 `len` 判断要看**去标签后的正文长度**，不要只看原始 HTML 大小（BNBU 页 33KB HTML 里正文只有几百字，全被 CSS/JS 占掉）。

### C4. UQ（The University of Queensland）特殊规则（2026-09-17 沉淀）

UQ 不反爬，**urllib + 普通 UA 即可直接抓取**，但有以下几个坑：

**1. 官方导师主页的两种 URL 与权威判定**

| 格式 | 示例 | 特征 | 建议 |
|---|---|---|---|
| **专家库页（权威）** | `https://about.uq.edu.au/experts/{数字ID}` | 含 `Availability` 段落，是判断招生资格的唯一权威来源 | **写入表里的「导师主页」用这个** |
| 院系 profile 页 | `https://business.uq.edu.au/profile/{ID}/{slug}` | 会自动跳转/引用专家库 ID；部分 ID 已失效返回 404 | 仅作为查找入口，不要写进表 |

**`business.uq.edu.au/profile/{ID}` 的 ID 与专家库 ID 不是同一个数字**，不能互推。用 `?search=` 搜到人后再取专家库 ID。

**2. 专家搜索的正确参数是 `search`（其他都无效）**
```
✅ https://about.uq.edu.au/experts/search?search=Trevor%20Russell   → 命中正确人员
❌ ?name= / ?q= / ?keyword= / ?query=                                 → 一律返回 A 开头的全量字母序列表（假结果，极易误判为"查无此人"）
✅ ?research-field={数字}                                              → 按 UQ 研究领域码筛选（如 4917）
```
**踩坑记录**：`?name=` 会静默返回全量列表而非报错，若不做校验会得出「该导师不存在」的错误结论——**必须校验返回的第一条姓名是否与查询词相关**。

**3. 招生资格判定：抓 `Available for supervision`** — 专家库页固定含以下两句话之一，这是 UQ 官方的 HDR 招生状态，直接决定要不要写入：
- `... is: Available for supervision` → 可写入
- `... is: Not available for supervision` → **不写入**（即使方向极对口）

**注意区分**：`Not available` 不等于离任——很多人是因为**已带满学生**。这类人（如 UQ 的 Clair Sullivan、Morteza Namvar、Katie Williams 等方向极对口者）应记录为「方向对口但暂不带人」，作为次级线索或第二导师候选，**不要当作不合格而丢弃**。

**3b. ⚠️「教职员名单里有名字」≠「主页有效」（2026-09-20 踩坑，CRITICAL）**

UQ 存在一类**「在册但无已发布主页」**的情况：人名仍出现在院系 `our-people` 教职员列表里，但个人主页已经下线：

| 姓名 | 名单中 | 主页实访结果 |
|---|---|---|
| Peter Liesch（IB 讲席教授、学科召集人，曾任 AIB 主席） | ✅ 仍在 IB 名单 | `business.uq.edu.au/profile/23/peter-liesch` → **"Profile not found"**；`experts/118` → 404 |
| Tapani Rinta-Kahila | ✅ 仍在 IS 名单 | `business.uq.edu.au/profile/7312/...` → **404** |

**规则**：**院系名单只用于发现人名，绝不能用它证明主页有效。** 每个候选人必须实访主页确认三件事：① 页面能打开（非 404）；② 页面出现 `Available for supervision`；③ 页面内容里有该人的姓名/职称/院系。**三者缺一 → 不写入表格。** UQ 的 "Profile not found" 页文案是「该地址可能不正确，或此人当前没有已发布的个人主页」，遇到即判定不可写入（可能已退休、转为兼职/名誉、或已离任）。

**3c. ⚠️ 同名歧义：按名字检索会命中错误的人** — UQ 有同名教职人员。实例：**Anna Jenkins** —— 商学院创业方向副教授 与 医学院精神科医生（Royal Brisbane and Women's Hospital 高级专科医师）同名，`?search=Anna Jenkins` 会命中**医生**那位。**规则**：命中后必须核对**院系（School）+ 职位类型**是否与目标一致（如目标在商学院，则卡片应显示 `School of Business`）。不一致就换关键词重搜或放弃，**不要凭名字直接采信**。

**4. 批量核验脚本模板**
```python
import re, urllib.request
def plain(html):
    t = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)
# 专家库页
t = plain(urllib.request.urlopen(f"https://about.uq.edu.au/experts/{rid}").read().decode("utf-8","ignore"))
avail = "NOT" if "Not available for supervision" in t else ("OK" if "Available for supervision" in t else "UNKNOWN")
```

**5. 高价值机构入口（找「同一方向还有谁」时优先查这些页，比关键词搜人高效得多）**

| 入口 | URL | 说明 |
|---|---|---|
| **Future of Health Research Hub** | `business.uq.edu.au/team/future-health-experts` + `business.uq.edu.au/files/118219/researcher-capability-foh.pdf` | 商学院 20+ 位做医疗的学者全名单，**PDF 内含每人完整研究兴趣，一次抓完最省 token** |
| **Queensland Digital Health Centre (QDHeC)** | 挂靠 `chsr.centre.uq.edu.au`（该域名 2026 年已改版，会跳转到 HMBS 学院页，需经 WebSearch 找当前路径） | 数字健康中心 |
| **Centre for Online Health** | 医学院侧，远程医疗研究 | 找 telehealth/虚拟医疗导师 |
| **RECOVER 伤害研究中心** | `recover.centre.uq.edu.au` | 内含「Technology-enabled rehabilitation」项目页，**直接列出招生项目和 contact 邮箱** |

**PDF 抓取提示**：UQ 的能力清单 PDF 用 WebFetch 会返回二进制乱码，必须先 `curl -o` 下载再用 `pypdf` 抽取：
```python
from pypdf import PdfReader
text = "\n".join(p.extract_text() or "" for p in PdfReader("foh_capability.pdf").pages)
```

**6. 「同一方向还有谁」的学科定位法** — 不要只按学生方向的关键词搜人。先判断学生的方向**落在哪个培养单位**：
- 医疗**信息化 / 数字化转型 / IS** → UQ Business School 信息系统组（BIS）
- 医疗**服务与患者体验 / 管理控制 / 领导力变革** → Future of Health Hub（营销/会计/管理）
- 医疗**技术干预 / 远程医疗** → 医学院 Centre for Online Health、RECOVER

按单位列全名单后逐个核 `Available for supervision`，比逐校关键词搜索的覆盖率高得多，也更容易解释「为什么这位对口」。

### C5. 港澳「已核实可用」项目页 / 系名单页 URL 底账（2026-09-22 起累积）

`博士申请信息` 必须是项目自己的博士项目页（规则见 `rules-write.md` §2.1），`其他导师信息` 必须是该导师**本人所在系**的名单页（不是学院级/跨系聚合页）。下表是逐条实测过的底账，**用时仍须 WebFetch 复验一次**。

**港大各系 people / 项目页**

| 院系 | `其他导师信息`（系名单页） | `博士申请信息`（项目页） |
|---|---|---|
| JMSC（新闻及传媒研究中心） | `jmsc.hku.hk` | `jmsc.hku.hk/rpg-programme-overview/` |
| 中文学院 | `web.chinese.hku.hk/en/people/academic_staff/` | `chinese.hku.hk/en/postgraduate/programme_information` |
| 社会学系 | `sociology.hku.hk/people/` | `sociology.hku.hk/mphil-phd-sociology` |
| 地理系 | `geog.hku.hk/staff` | `geog.hku.hk/mphil-phd` |
| SMLC（现代语言及文化学院） | `web.smlc.hku.hk/teachingstaff` | `web.smlc.hku.hk/postgraduate` |
| 比较文学系 | `complit.hku.hk/index.php/faculty/` | `complit.hku.hk/index.php/mphil-phd/` |
| 政治与公共行政学系 | `ppaweb.hku.hk/people?people_type=faculty-members` | `ppa.hku.hk/research-postgraduate/mphil-phd-studies/` |
| 港大商学院 | — | `phd.hkubs.hku.hk/admissions/...` |
| 建筑学院 SAAS | `hku.hk/.../staff_teaching.php` | `hku.hk/programme/rpg/mphil-phd` |
| 护理学院 | — | `hku.hk/education/doctor-of-philosophy-programme` |

**港科大 / 港科广**

| 单位 | `博士申请信息` |
|---|---|
| 人文 `huma.hkust.edu.hk/teaching/pg/phd` | 跨学科 `emia.hkust.edu.hk/iip` |
| 公共政策 `ppol.hkust.edu.hk/mphil-phd-program-overview` | 艺术与机器创意 `amc.hkust.edu.hk/mphil-phd-program-program-objective` |
| 港科广·计算媒体与艺术 `fytgs.hkust-gz.edu.cn/programs/computational-media-and-arts-4` | （学域自建站没有项目页，项目页挂在研究生院域的 `/programs/…` 下——**这仍是项目页，不是统一入口**） |

**其他港澳校**

| 学校/院系 | `博士申请信息` |
|---|---|
| 港中文·新传 | `gs.cuhk.edu.hk/programmes/social-science/phd-communication` |
| 港浸会·传理学院 | `gs.hkbu.edu.hk/programmes/doctor-of-philosophy-master-of-philosophy-school-of-communication` |
| 港城大·创意媒体 | `scm.cityu.edu.hk/programmes/postgraduate/phd` |
| 港城大·媒体与传播 | `cityu.edu.hk/com/Page.aspx?p=PHD_Introduction` |
| 港理工·英文及传意 | `polyu.edu.hk/engl/study/research-postgraduate-programme/applying-for-research-study/` |
| 港理工·设计 | `polyu.edu.hk/sd/study/rpg/phd/` |
| 港理工·护理 | `polyu.edu.hk/study/pg/rpg/2026/sn` |
| 岭南·文化研究 | `ln.edu.hk/cultural/programmes/mphil-phd` |
| 岭南·数码艺术及创意产业 | `ln.edu.hk/daci/programmes/postgraduate/postgraduate` |
| 港中深·人文社科学院 | 按项目分：计算社会科学 `hsspg.cuhk.edu.cn/mphilphdcss`、城市学 `mphilphdus`、全球研究 `mphilphdgs`（**用「博士生导师」子页核对某人挂哪个项目**，如 `mphilphdus/phdadvisor` 里有王宁馨） |
| 教大（**PhD 是全校统一学位、不按学系分设项目页**） | 用学系 RPg 页：LCS `eduhk.hk/lcs/programmes/research-postgraduate`；CCA `eduhk.hk/cca/en/programmes/postgraduate-programmes/research-postgraduate-programmes/` |
| 都会大学（**无分项目博士页**，PhD 统一授予、按学院开设） | 用院系官网 RPg 页 `hkmu.edu.hk/as/programmes-courses/rpg/` |

**港大各系名单页 URL 的原始教训（2026-09-21 全表复查）**：港大 12 条记录的 `其他导师信息` 全部指向 JMSC 名单页，但其中 8 人实际分属社会学系、地理系、SMLC、中文学院、比较文学系、政治与公共行政学系。查法是「读 `Department` 字段 → 定位该系官方 people 页 → 逐条替换 → 用页内是否出现该导师姓氏批量自检」（繁体页面需简繁映射）。

## D. 批量处理方法论


### D1. 「文章链接」「实验室」字段的批量补全（2026-09-20 沉淀）

需求量级：101 位导师 × 2 个字段。**不要逐人 WebSearch**（成本极高），用下面三级流水线。

**字段惯例（照抄表内既有记录）**：
- **文章链接**（Text）：填**作者主页类链接**，优先级 Google Scholar > OpenAlex 作者页 > 实验室 publications 页 > 导师主页。可用 `https://scholar.google.com/citations?user=<ID>&hl=en` 形式。
- **实验室**（Text）：填**中文描述**，格式 `<实验室名或「姓氏 课题组」>；研究方向：<方向；主页：<url>>`。方向直接取自本表「导师研究领域」字段，不要另编。

**L1 从导师主页抓 Google Scholar（零成本，覆盖约 1/3）**
```python
# 抓每个「导师主页」，正则找 scholar 链接
re.findall(r'https?://scholar\.google\.[a-z.]+/citations\?[^"\'\s<>]*', body)
# 同时找实验室站：href 含 lab|group|research，排除 scholar/linkedin/twitter/orcid/researchgate/pubmed
```

**L2 用 OpenAlex API 补作者页（覆盖剩余大部分）**：`https://api.openalex.org/authors?search=<姓名>&per_page=8`
- **必须用 `last_known_institutions` 与所关联学校比对**来定候选，不能无脑取第一条（本轮 100 条里有 21 条第一候选是**同名他人**）。
- **学校→机构关键词映射要写对**：Penn State → `pennsylvania state`（不是 `penn state`）、VT → 注意 OpenAlex 常写 `Virginia Tech` 而非 `Virginia Polytechnic Institute`。映射错会把正确候选误判为不匹配。
- 学校名可直接拼进 search query 会**降低**命中率，不要那样做；用姓名搜索 + 机构过滤更准。
- 限流：并发 ≤ 6，条目间 sleep 0.1~0.2s；触发 429 就停。
- **写完后必须逐条回验**：`GET /authors/{id}` 看 `display_name` + `last_known_institutions` + `topics`。**论文数 < 12 的条目基本是名字歧义或合并错误**；topics 与该导师方向明显不符（如做软电子的被判为研究肠道菌群）一律弃用。

**L3 兜底**：L2 判不可靠的，改用该导师的**实验室 publications 页**或**导师主页**（安全优先）。

**收尾**：实验室站 URL 要过滤掉**学校通用页**（`research.mines.edu`、`njit.edu/njitresearch`、`bme.unc.edu/research-areas`、`luddy.iu.edu/research` 等只是学院总览页）和**第三方站**（如 `thriveoncollaboration.org`、`researchstash.com`）。

### D2. 邮箱抓不到时的两条路（2026-09-21 沉淀）

- **Cloudflare 邮箱混淆解码**：岭南大学等站点的个人页把邮箱写成 `data-cfemail="HEX"` 或 `/cdn-cgi/l/email-protection#HEX`，正则抓不到、WebFetch 才能渲染。可自行解码：**首字节为 XOR 密钥，其后每字节与密钥异或即得明文**：
  ```python
  def cfdecode(h):
      k = int(h[:2], 16)
      return ''.join(chr(int(h[i:i+2], 16) ^ k) for i in range(2, len(h), 2))
  ```
- **院系名单页往往一次给出全院邮箱**：如 CUHK 新传 `research.cuhk.edu.hk/en/organisations/school-of-journalism-and-communication/persons/`、UM 传播系 `comm.fss.um.edu.mo/people/academic-staff/`、CUHK 中文系 `chi.cuhk.edu.hk/about-us/people`、港大政治 `ppaweb.hku.hk/people`。先抓名单页，比逐人开个人页高效得多。
- 若官网确实未公开邮箱（部分 CityU / 港科广 / UIC 教师），**留空即可**——海外院校邮箱为选填。

## E. 拆分去向说明（2026-10-07）

原 `critical-rules.md` 的内容分流如下，出现「找不到某条」时按此表查：

| 原内容 | 现在在哪 |
|---|---|
| 所有「写入前必须遵守」的硬规则 | `rules-write.md`（可整读，≤200 行） |
| 学校关联字段六步操作全文 | `vika-school-link.md` |
| 案例、数据表、某校明细、批量方法 | 本文（A–D 节） |
| Vika API 代码模板与机械操作 | `vika-guide.md` |
| 链接四关的逐条判定口径 | `field-rules.md`、`verification-workflows.md` |
| 地区职称口径与排除标准 | `selection-rules.md` |
| 语言门槛核验清单 | `language-requirements.md` |
| 某校抓取架构 | `school-registry-<地区>.md` |
