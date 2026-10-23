---
name: phd-supervisor-selector
description: 博士导师筛选与表格管理工具。面向留学机构，为不同方向的学生快速建立可核验的导师列表。搜索各大学官方页面，判断导师是否具备 PhD 指导资格，填写表格各列。主力支持 Vika 在线表格直接 CRUD，Excel 作为可选回退模式。
agent_created: true
---

# PhD Supervisor Selector（博士导师筛选器）

## 概述

为博士申请者建立有据可查的导师列表。搜索各大学官方页面，判断导师是否具备 PhD 指导资格，填写表格各列，将不合格或高风险候选人排除在主表之外。

**主力模式：Vika（在线表格直接 CRUD）。Excel 作为可选回退模式。**

## 🎯 五项验收口径（用户最在意的五项，优先级高于其他任何指标）

每次写表与交付前，**逐条自查这五项**。每项末尾是详解所在文件（需要时再打开，不要凭印象）。

1. **方向不能出错** — `导师研究领域` 与排除理由都必须来自**本人亲手打开的官方页面原文**，不得凭先验知识填写；**系页描述太泛不能作为排除理由**（必须打开个人页取到具体方向才能判）；关键词撞上 ≠ 真能接住学生的题目。→ `evidence-discipline.md`、`selection-rules.md`
2. **职称不能出错** — 职称以**院系或中心的教师名录页**为准；个人页标题、讲席头衔（`Chair`、`Professorial Fellow`、`apl. Prof.`）都不算职称；非英语职称不得直译（`Professeur associé` 是**副教授**）；且必须满足各地区最低职级（美国/港澳/欧陆：助理教授及以上；港澳讲师序列一刀切排除）。→ `field-rules.md`、`selection-rules.md`、`school-registry-hk-mo-cn.md`
3. **链接必须真实官网可达、且落在正确的页面** — **四关全过才算合格，"不是 404"远不等于合格**：
   - **① 能打开**：明确 404 / 410 / 域名解析失败＝坏链，必须替换。**但非 200 不等于坏链、也不等于放过**——403 / 429 / 202 / 超时 / `200 但字节数很小且无 title` 都可能是反爬或 JS 壳，必须换通道（WebFetch / 完整浏览器 UA）穿透看真实内容；穿透后显示 "page does not exist" 即为真失效（CityU 案例：403 的离任教授页就是这样查出来的）。
   - **② 落点对**：`curl -L -w "%{url_effective}"` 取最终 URL 与原 URL 比对。**能打开但已跳到院系搜索页 / 机构概览页 / 别的项目页，等于失效**（`oge.mit.edu/?p=589` 就是：打得开，但已不是原来那一页）。
   - **③ 是这个人的页**：抓到的正文必须含该导师姓或名——防「404 伪装成 200」「SPA 空壳」「跳转页」「通用列表页」；域名与所关联学校不一致要单独看（可能是已转校）。
   - **④ 层级对**：导师主页＝**个人页**（不可用 Google Scholar / ResearchGate / 院系首页）；`博士申请信息`＝**项目申请页**（不可用全校研究生院入口）；`其他导师信息`＝**该导师所在院系的教师名录页**（不可用站点根目录 / 搜索落地页）。
   - ⚠️ **禁止仅凭 HTTP 状态码判定**（正文「链接验证标准」已写明：美国校常对 404 返回 200 + "Page Not Found" 内容，旧路径废弃后则静默重定向到院系搜索页）→ `field-rules.md`、`verification-workflows.md`、正文「链接验证标准」
4. **备注按现行要求** — 格式 `职称；做…。`；正文**不得出现任何链接**（含 scholar.google / researchgate / orcid / linkedin）；不得出现"试试 / 再看看 / 失效"这类草稿语；不得出现 AI 痕迹语言与方向编号。自查法：去掉 `职称；` 前缀后，句子应当能回答"这个组做什么"；出现"创办 / 获得 / 担任 / 曾任"说明混进了履历。→ `notes-and-fields.md`、`field-rules.md`
5. **尽可能全面** — **先出候选池、再筛选，两段分开做**；任何抓取失败（超时 / 403 / 解析为空）**必须进「待重试」清单**，不得静默丢弃；报告里的"覆盖 N 人"必须与候选名单长度对账，**差额逐人说明去向**。→ `evidence-discipline.md`

---

## 🚦 写入前硬门速查（常驻正文，不要跳过）

> 这些规则**常驻正文**，因为漏掉代价高。每条后括号内是详解所在文件。

- 🏫 学校关联字段必填（六步操作）　→　`vika-school-link.md`
- 禁止向 MagicLookUp 或计算字段写入　→　`rules-write.md`

- 禁止修改已填写选导意向的记录　→　`rules-write.md`
- 新增记录去重　→　`rules-write.md`
- 排除退休/名誉教授　→　`rules-write.md`
- 🔴 提到「欧洲」时默认排除**挪威与瑞典**（除非用户当次明确点名）　→　`selection-rules.md`
- ⚠️ Vika 同记录多字段修改：必须合并为一次 PATCH　→　`rules-write.md`
- 禁止猜测 URL　→　`rules-write.md`
- 导师主页必须是个人 URL　→　`rules-write.md`
- 链接**四关**：能打开 + 落点对 + 是本人页 + 层级对（"不是 404"≠合格）　→　`field-rules.md` / `verification-workflows.md`
- 禁止在备注中出现 AI 痕迹语言　→　`rules-write.md`
- 禁止在备注中写入方向偏向　→　`rules-write.md`
- 国内学校搜索（不使用 Google）　→　`rules-write.md`
- Stipend 与 Funding 核实规则　→　`rules-write.md`
- Funding 字段中的推测性数据必须标注　→　`rules-write.md`
- NIH Grant 必须通过 NIH Reporter 交叉验证　→　`rules-write.md`
- 📛 备注自包含原则　→　`notes-and-fields.md`
- 📛 备注可追溯原则　→　`notes-and-fields.md`
- 📛 元注释禁止规则　→　`notes-and-fields.md`
- 链接层级三分法　→　`field-rules.md`
- 🚦 学生可执行性**三座闸门**（研究对象 / 跨学科先修背景 / **博士项目的学位学科必须对口**）　→　`selection-rules.md`
- 🚦 **硬门 C：学校层面的核心方向必须有人**（整校去留先过这一关；「方向相邻」不算）　→　`selection-rules.md`

## 搜索编排（首先阅读）

开始搜索任务前，阅读 `references/search-orchestrator.md`。它定义了：

- **状态追踪**：续传中断的搜索，跳过已完成的学校
- **智能优先级**：按预期产出（P0-P3 层级）对学校排序
- **分阶段策略**：先快速扫描所有学校（Pass 1），再深入验证有希望的学校（Pass 2）

---

## 📚 参考文件索引（按需读取；大文件请定位后局部读，不要整读）

本技能于 2026-10-07 完成两轮瘦身：原 274 KB 正文按主题拆入 `references/`，再按「必读 / 按需操作 / 禁整读案例」分成三层。**下表说明每个文件何时该读。**

### L1 必读（每次任务整读，每次任务整读的文件数上限 3）

| 文件 | 何时读 |
|---|---|
| `rules-write.md` | 📕 **任何写入动作之前必读、可整读**（≤200 行）——写入前硬规则全集 |
| `search-phase.md` | 任务形态是「搜索导师」时，开工前整读 |
| `write-phase.md` | 进入写入阶段前整读 |
| `review-phase.md` | 交付前 / 用户说「检查一遍」时整读 |

> 阶段手册**一次只读当前那本**，加上 SKILL.md 与 `rules-write.md`，合计恰好 3 份。

### L2 按需操作（按当前动作打开对应那一份）

| 文件 | 何时读 |
|---|---|
| `search-orchestrator.md` | 搜索编排细节（Step 0 身份硬门、项目底座、状态续传、P0-P3、Pass1/2、子代理派发） |
| `batch-audit.md` | 写完 10 条 / 搜完一所学校 / 要 spawn auditor 之前 |
| `vika-guide.md` | Vika 核心读写（§0–§5：Setup、建表、schema、读、批量创建、更新、删除） |
| `vika-batch-ops.md` | 批量补链 / 查空记录 / 跨校链接审计 / 批量补研究领域 / Excel 导入 |
| `vika-troubleshooting.md` | 写入失败（309 / POST 超时 / 返回 0 条 / 字段写不进）、批量修订备注、新版表结构 |
| `vika-school-link.md` | 给记录设**学校关联字段**时（识别新/老学生、建学校、四层搜索、搜不到就停） |
| `field-rules.md` | 校验/修正字段时：「博士申请信息」层级、职称、其他导师信息、链接检查 |
| `notes-and-fields.md` | 写「备注」「项目综合情况」「funding 三段式」等字段前 |
| `selection-rules.md` | 判断导师是否合格、筛选口径、排除标准、搜索标准、主页类型前置过滤、导师转校 |
| `verification-workflows.md` | 交付前机械复查 SOP、链接修复、链接健康审计、截止日核查、汇编文档核查 |
| `language-requirements.md` | 填「语言要求」列前（7 项必录清单、新旧分制换算、口语分档） |
| `spreadsheet-rules.md` | Excel 回退模式下的列格式规则与 Excel 模式说明 |
| `search-techniques.md` | 单校单页抓取技巧：SPA/JS 绕法、API 端点定位、URL 模式推断、浏览器验证、项目页发现、搜索降级 |
| `search-scaling.md` | 规模化与兜底：并行子代理任务设计、L4 Tavily（extract/search/crawl）、常见 HTTP 错误绕法 |
| `analysis-workflows.md` | 套磁结果归因分析、学生方向偏好逆向分析 |
| `common-errors.md` | 交付前扫一遍高频错误 |
| `collaboration-workflow.md` | 「开始学生」/「结束学生」协作流程 |
| `lark-board-entry.md` | 任务来自飞书「选导任务管理看板」记录时 |
| `acceptance-runbook.md` | 交付前三条验收怎么做（证据链抽检 / 链接抽检 / 真实任务复盘），含记录表模板 |

### L3 查询型数据（**禁止整读**，必须先用 `school-info.py` 或 grep 定位）

| 文件 | 何时读 |
|---|---|
| `school-strategies.md` | 学校策略库入口（访问框架 L0–L4、更新协议、院系名录索引） |
| `school-registry-uk / -au-nz / -sg-eu` | 按目标校所在地区 grep 校名 |
| `school-registry-hk-mo-cn` = `-hk` + `-mo-cn` | 港澳与中外合办；入口页指向两个分册 |
| `school-registry-us-ca` = `-us` + `-ca` + `-us-backlog` | 美加；入口页指向三个分册 |
| `school-updates-2026-08 / -09 / -10` | 带日期的案例日志，按校名/关键词定位；索引见 `school-updates-log.md` |
| `access-framework.md` | 各校 URL 模式、Vika School IDs、教师转校记录 |
| `access-channels.md` | 站点访问通道实测（curl vs WebFetch）、sitemap 找院系页、港澳澳新抓取情报 |
| `evidence-discipline.md` | 从候选生成到决定写入之间的纪律（候选 ≠ 写入依据） |
| `cases-rules.md` | 案例复盘、定级数据（Stipend 官方表）、某校特殊规则明细、批量方法论、项目页 URL 底账 |

## 🛠️ 脚本与数据索引

`scripts/` 下是本技能的机械闸门。**能脚本判定的，不要靠「有没有读到规则」保证。**

| 命令 | 用途 | 退出码含义 |
|---|---|---|
| `python3 scripts/audit-all.py <DATASHEET_ID>` | **交付前十项机械复查的唯一入口**（含链接四关、备注正则、职称门槛） | 0 通过 / 1 有 FAIL / 2 用法 / **3 结果不完整** |
| `python3 scripts/audit-all.py --self-test` | 纯离线回归：备注正则与职称门槛在既有正例/反例上是否仍正确 | 0 全过 |
| `python3 scripts/school-info.py <校名>` | 按校名取**单条**逐校情报（永不整读 markdown） | 0 有命中 / 1 无命中 / 2 索引过期 |
| `python3 scripts/skill-budget.py` | 检查是否超出第三节预算（防止半年后回涨） | 0 达标 / 1 超预算 |
| `python3 scripts/build-school-index.py` | 重建 `data/` 索引（源 markdown 改动后必须跑） | 0 成功 |

- `data/schools.json`、`data/updates-index.json` 是**机器读的索引**，不要用 Read 打开（会占满上下文）；一律走 `school-info.py`。
- `audit.py` / `link-audit.py` 已被 `audit-all.py` 取代，保留仅为兼容历史调用。
- 旧的 `search-state/` 是运行态数据（已 gitignore），不属于本索引范围。

## 语言要求核验（做"语言要求"列前必读）

见 `references/language-requirements.md`：每校必录 7 项（是否接受家考／托福总分／口语单项／助教口语／雅思是否可用／有效期以申请截止日还是开始日／建议递哪张成绩），含新旧分制换算、口语不足时的资助分档标尺、已核实校别样例，以及一条**已证伪**的常见谣言（"家考有效期缩短至 18 个月"）。

---

## 关键规则（CRITICAL）

> 📎 2026-10-07 二次拆分：原 `critical-rules.md`（876 行）已按内容性质拆为三本——
> - **`references/rules-write.md`**（185 行）：写入前硬规则全集，**可整读，写入前必读**
> - **`references/vika-school-link.md`**（291 行）：学校关联字段六步操作手册
> - **`references/cases-rules.md`**（392 行）：案例 · 数据 · 某校特殊规则明细 · 批量方法论，**按关键词定位，禁止整读**

## 协作流程（"开始学生" / "结束学生"）

当用户说**"开始学生"**（或"提交更新"、"同步并提交"等）时，自动执行 pull -> branch -> commit -> push -> PR 全流程。当用户说**"结束学生"**时，先提取本轮搜索经验更新策略库，再自动执行同步流程。

**完整执行步骤见 `references/collaboration-workflow.md`。** 触发后按该文档的 11 步流程执行，无需用户懂 git。

---

## 参考文献

- 决定候选人能否进入主表前，阅读 `references/selection-rules.md`
  - **国内学校**：重点阅读文档末尾的「国内学校选导规则」（招生目录优先、A/B/C 分类、邮箱必填）
- 创建/编辑/验证表格前，阅读 `references/spreadsheet-rules.md`
  - **国内学校**：重点阅读文档末尾的「国内学校表格规则」（导师联系方式列、主页来源、备注链接格式）
- 开始搜索前，阅读 `references/search-orchestrator.md`
- 访问学校前，检查 `references/school-strategies.md`
- SPA/API 发现技巧，见 `references/search-techniques.md`
- Vika 完整 CRUD 操作 + API 代码模板，见 `references/vika-guide.md`
- 协作流程（开始学生/结束学生），见 `references/collaboration-workflow.md`

---

## 📎 已迁出小节一览（原 SKILL.md 小节 → 现在在哪）

> 下方小节的正文已整体迁入 references/。本表只作导航，**不要在这里找规则**。

| 原小节 | 现在在哪 |
|---|---|
| 任务入口：飞书「选导任务管理看板」（2026-09-14 沉淀） | `lark-board-entry.md` |
| 🔴 维格空间行数上限：写入会被 309 拒绝（2026-09-20 实测，必须前置检查） | `vika-troubleshooting.md` |
| 学校站点访问通道：本机 curl 与 WebFetch 的实际差异（2026-09-20 实测） | `access-channels.md`（5 个子节） |
| 写入后的「检查一遍」：职称与「其他导师信息」是最容易出错的两处（2026-09-21 实测） | `field-rules.md`（5 个子节） |
| 接手别人的表时：先扫一遍历史批次的备注（2026-09-22 实测） | `field-rules.md` |
| 「博士申请信息」这一列：必须是项目页，不能是全校入口（2026-09-23 实测，125 条） | `field-rules.md`（4 个子节） |
| 表格验证工作流（验证已有表格时触发） | `verification-workflows.md`（3 个子节） |
| 申请截止日期核查（2026-09-17 沉淀，CRITICAL） | `verification-workflows.md`（5 个子节） |
| 申请信息汇编文档的批量核查（2026-09-24 沉淀） | `verification-workflows.md`（8 个子节） |
| 博士项目学位类型核查（PhD vs DVM/执业学位，2026-10-10 沉淀） | `verification-workflows.md`（见「博士项目学位类型核查」节） |
| 客户同步编辑表格的检测纪律（2026-10-10 沉淀） | `vika-batch-ops.md` |
| 学生方向偏好逆向分析（2026-09-14 贺禧案例沉淀） | `analysis-workflows.md`（4 个子节） |
| 套磁结果归因分析（2026-09-20 刘艺佳案例沉淀） | `analysis-workflows.md`（11 个子节） |
| 证据纪律：候选生成 ≠ 写入依据（2026-09-17 沉淀，务必执行） | `evidence-discipline.md`（3 个子节） |
| ✅ 交付前机械复查 SOP（10 项，全部可脚本化） | `verification-workflows.md` |
| 🇭🇰 港城 / 港理 / 浸会 三校抓取口径（2026-09-24 黄肇启案例沉淀） | `school-registry-hk.md` |
| 常见错误速查表 | `common-errors.md` |
| 链接修复工作流（用户说"链接打不开/404"时触发） | `verification-workflows.md`（6 个子节） |
| 链接健康审计（用户报"链接404/badcase"时，2026-08-04 新增） | `verification-workflows.md` |
| 🍁 加拿大批次专属陷阱（2026-09-24 王灏案例沉淀） | `school-registry-ca.md` |
| 🔁「回归本源方向」型任务：审核要比常规更狠（2026-09-24 王鹏涛案例沉淀） | `analysis-workflows.md` |
| 🌐 抓取通道实测补充（2026-09-24） | `access-channels.md` |
| 港澳·澳新院校抓取通道情报（2026-09-24 王润泽第三轮沉淀） | `access-channels.md`（8 个子节） |
| 🔎 找院系页的最快通道：先读 sitemap.xml（2026-09-24 验证有效） | `access-channels.md`（4 个子节） |
| 🆕 2026-09 新版学生表结构（统一学校主表）· 2026-09-29 实测 | `vika-troubleshooting.md` |
| 🗺️ 院系名录页索引 + 覆盖度台账（2026-09-29 实测） | `school-strategies.md`（4 个子节） |
| ⚠️ 「备选」与「后放」是两套机制，别混，也别只写一种（2026-09-29 王润泽批次复盘） | `notes-and-fields.md` |
| 🔁 批量修订已有记录的备注（2026-09-29 实操，可直接复用） | `vika-troubleshooting.md` |


---

## 🏫 PolyU BME → BEST 更名（2026-10-01，路径全变，务必更新）

**Department of Biomedical Engineering 于 2026-10-01 正式更名为 Department of Biomedical Engineering and Sports Technology（BEST）。**

| | 旧 | 新 |
|---|---|---|
| 系名 | Department of Biomedical Engineering | **Department of Biomedical Engineering and Sports Technology** |
| 站点 | `polyu.edu.hk/bme/` | **`polyu.edu.hk/best/`** |
| 师资名录 | `/bme/people/academic-and-teaching-staff/` | **`/best/people/academic-and-teaching-staff/`**（⚠️ urllib 返回 0，**必须 WebFetch**） |
| 博士项目 | `/bme/study/research-postgraduate-programme/` | **`/best/study/research-postgraduate-programme/doctor-of-philosophy-and-master-of-philosophy/`** |

- 更名动因是向**体育科技**扩张：新增 BSc in Sports Science and Technology、MSc in Sports Technology and Management；系主任仍为 **Ir Prof Ming ZHANG（Chair Professor of Biomechanics）**，同时兼任 Research Institute for Sports Science and Technology 主任。
- **已入库的 PolyU BME 记录（James CHEUNG、M.S. WONG 等）Department 字段仍是旧系名**，遇到这类机构变更要同步改，否则与官网对不上。
- 该系现有 **9 位 Research Assistant Professor**（Man Ting AU / Tony Linwei CHEN / Bingyang DAI / Yanhuan HUANG / Edmond LAM / Timothy LEE / Jingyu SHI / Matthew Qitao TAN / Meizi WANG / Quanxiang XIAN）——RAP 是否具备独立指导资格仍需逐个核。

## 👤 「即将入职」的学者怎么判（2026-10-21，Tian Tan 案例）

GitHub Pages / 个人站上写 *"I will join X in Spring 2027, actively recruiting PhD students"* 的人越来越多。**这类线索有价值，但不能直接入库。**

判定顺序：
1. **查目标院系官方师资名录有没有他** —— 没有 = 尚未入职，官方职称未知。`polyu.edu.hk/best/people/academic-and-teaching-staff/` 实测无 Tian Tan。
2. **职称无法取证就不要猜** —— 「博后转 AP」是常见路径，但也可能是 Research Assistant Professor（部分院校该序列不能独立带博）。**没有官方页面 = 无法确认，只能标「待确认」。**
3. **看邮箱域名** —— 仍是原单位（如 `@stanford.edu`）说明确实还没到岗。
4. **入库条件**：等他在目标校官网上出现个人页（含职称）后再收。此前只能放进「待入职观察名单」，写清预计到岗时间与联系方式。
5. **时间口径要说清**：2027 春季到岗 → 可接 2027 Fall 入学；但若学生要更早入学，此人不可用。

**判断「算法侧/硬件侧」的快速方法**：看一作论文的产出物是**模型+代码+数据集**，还是**样机+机构+实验台**。
- 前者（如 GaitDynamics 放出 Paper/Code/Data/Colab/HuggingFace 全套）＝纯数据侧，**给不了外骨骼机构与俘能硬件**；
- 后者才是硬件导师。**两者不可互相替代**，即使都叫「康复机器人」。
