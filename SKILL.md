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

## Optional Companion Skill

**tavily-search-pro** — AI-powered search platform that acts as **L4 fallback** when L1-L3 access methods all fail (WAF blocks curl+browser+search). Provides:
- **extract**: Server-side page content extraction (bypasses Cloudflare/Incapsula WAF)
- **search**: Alternative search engine with clean, unencrypted result URLs
- **crawl/map**: Site structure discovery for blocked university sites
- **research**: Deep department analysis with citations

Requires `TAVILY_API_KEY` environment variable. If installed, search automatically escalates to Tavily when all other access methods are blocked. See `references/search-techniques.md` (L4 section) and `references/school-strategies.md` (L4 layer).

## 搜索编排（首先阅读）

开始搜索任务前，阅读 `references/search-orchestrator.md`。它定义了：

- **状态追踪**：续传中断的搜索，跳过已完成的学校
- **智能优先级**：按预期产出（P0-P3 层级）对学校排序
- **分阶段策略**：先快速扫描所有学校（Pass 1），再深入验证有希望的学校（Pass 2）

---

---

## 📚 参考文件索引（按需读取；大文件请定位后局部读，不要整读）

本技能已于 2026-10-07 瘦身：原 274KB 正文按主题拆分至 `references/`，正文只保留核心流程、硬门与操作权限。**下表说明每个参考文件何时该读。**

| 参考文件 | 何时读 |
|---|---|
| `search-orchestrator.md` | **开始搜索任务前**（状态续传、学校优先级 P0-P3、Pass1/Pass2 分阶段） |
| `rules-write.md` | 📕 **执行任何写入前必读、可整读**（185 行）——写入前硬规则全集：导师主页要求、链接四关、备注禁令、职称、排除规则、去重、Funding 标注、字段一致性、Vika 写入机械硬门。**这是唯一需要「整读」的文件。** |
| `vika-school-link.md` | 给记录设**学校关联字段**时（识别新/老学生、创建学校记录、四层搜索主表、搜不到就停、验证） |
| `cases-rules.md` | ⚠️ **禁止整读**，按校名/关键词定位——案例复盘（404 大规模复盘、CityU 离任检测）、定级数据（Stipend 官方表）、某校特殊规则明细（美国通道表、港澳门槛表、UQ）、批量补字段方法论、港澳项目页 URL 底账 |
| `vika-guide.md` | Vika API 操作：写入前重新 GET、DELETE 上限、配额 309、分页 1000 行、批量修订备注、新版学生表结构 |
| `field-rules.md` | 校验/修正字段时：「博士申请信息」层级、职称、其他导师信息、链接检查 |
| `notes-and-fields.md` | 写「备注」「项目综合情况」等字段前（格式、语气、可追溯原则、备选/后放写法） |
| `evidence-discipline.md` | 从候选生成到决定写入之间的纪律（候选 ≠ 写入依据） |
| `verification-workflows.md` | 交付前机械复查 SOP、链接修复、链接健康审计、申请截止日核查、汇编文档批量核查 |
| `common-errors.md` | 交付前扫一遍高频错误 |
| `analysis-workflows.md` | 套磁结果归因分析、学生方向偏好逆向分析 |
| `access-channels.md` | 站点访问通道实测（curl vs WebFetch）、sitemap 找院系页、港澳/澳新抓取情报 |
| `school-strategies.md` | **学校策略库入口**（访问框架 L0–L4、更新协议、院系名录索引）。已按地区分册：`school-registry-uk / -au-nz / -hk-mo-cn / -sg-eu / -us-ca`、`access-framework`、`school-updates-log`（含 `school-updates-2026-08/-09/-10` 月册）——按目标校所在地区先开对应分册，再关键词定位 |
| `language-requirements.md` | 填「语言要求」列前（7 项必录清单、新旧分制换算、助教口语分档） |
| `selection-rules.md` | 判断导师是否合格、筛选口径与排除标准 |
| `search-techniques.md` | 抓取受阻时的通道选择与 L4 兜底（Tavily） |
| `spreadsheet-rules.md` | Excel 回退模式下的列格式规则 |
| `collaboration-workflow.md` | 「开始学生」/「结束学生」协作流程 |
| `lark-board-entry.md` | 任务来自飞书「选导任务管理看板」记录时 |

## 任务入口：飞书「选导任务管理看板」（2026-09-14 沉淀）

> 📎 本节全文已迁至 `references/lark-board-entry.md`。

## 🔴 维格空间行数上限：写入会被 309 拒绝（2026-09-20 实测，必须前置检查）

> 📎 本节全文已迁至 `references/vika-guide.md`。

## 学校站点访问通道：本机 curl 与 WebFetch 的实际差异（2026-09-20 实测）

> 📎 本节全文已迁至 `references/access-channels.md`（含 5 个子节）。

## 写入后的「检查一遍」：职称与「其他导师信息」是最容易出错的两处（2026-09-21 实测）

> 📎 本节全文已迁至 `references/field-rules.md`（含 5 个子节）。

## 接手别人的表时：先扫一遍历史批次的备注（2026-09-22 实测）

> 📎 本节全文已迁至 `references/field-rules.md`。

## 「博士申请信息」这一列：必须是项目页，不能是全校入口（2026-09-23 实测，125 条）

> 📎 本节全文已迁至 `references/field-rules.md`（含 4 个子节）。

## 语言要求核验（做"语言要求"列前必读）

见 `references/language-requirements.md`：每校必录 7 项（是否接受家考／托福总分／口语单项／助教口语／雅思是否可用／有效期以申请截止日还是开始日／建议递哪张成绩），含新旧分制换算、口语不足时的资助分档标尺、已核实校别样例，以及一条**已证伪**的常见谣言（"家考有效期缩短至 18 个月"）。

---

## 数据源检测

收到任务时，检测数据源：

1. **用户提供 Vika 分享链接**（如 `https://vika.cn/share/shrXXX/dstXXX/viwXXX`）：直接通过 Fusion API 操作 Vika 表格。**⚠️ 重要（2026-08-19 验证）**：分享链接页面通过 `dataPack` 接口只能看到**当前分享视图**的记录，可能不完整；若要获得完整表（全部视图的全部记录），必须用**个人 API Token** 调用 Fusion API `GET /datasheets/{dstId}/records`。发现差异时优先向用户索要 API Token 做完整读取，不要只依赖分享链接的 dataPack。
2. **分享链接只有 `shrXXX` 无 `dstXXX` 时提取 datasheetId（2026-08-31 验证）**：`curl -s -A "Mozilla/5.0..." "https://vika.cn/share/shrXXX"` 抓分享页 HTML，用正则 `grep -o 'dst[A-Za-z0-9]\{10,20\}'` 提取真实 datasheetId（页面 JS 配置会内嵌）。拿到 dstId 后即可用 Fusion API 只读（`GET /datasheets/{dstId}/fields`、`GET /datasheets/{dstId}/records?maxRecords=300&fieldKey=name`）。注意：分享 token 无写权限（写操作超时/失败），只读任务可直接用此路径；`POST /share/{shrXXX}/dataPack` 返回非 JSON 时不要依赖该接口。
2. **用户上传 `.xlsx` 文件**：操作本地电子表格
3. **用户同时提供**：优先 Vika 做 CRUD，Excel 做参考/填充源

---

## Excel 模式（可选）

当用户上传 `.xlsx` 文件而非 Vika 链接时，使用 Excel 模式。详见 `references/spreadsheet-rules.md`（列格式选择、列偏移检测、备注规则、质量检查）。

**默认输出列**：`导师`, `Location`, `学校名字`, `QS排名`, `美国USNEWS排名`, `Department`, `导师主页`, `导师联系方式`, `博士申请信息`, `其他导师信息`, `备注`

- `美国USNEWS排名`：仅当列表中有美国学校时包含此列
- `导师联系方式`：**国内学校必填**（导师 email），海外学校选填

---

## Vika 集成

**零依赖。** 所有操作使用 Python 3 标准库（`urllib` + `json`）——无需 `vika-cli`、npm 或第三方 SDK。仅需 API token 和任意 Python 3 安装。导入 Excel 时额外需要 `openpyxl`。

### 设置

1. 从 URL 解析：`datasheetId`（`dstXXX`）、`viewId`（`viwXXX`）
2. **Token 安全**：引导用户设置环境变量（不要在聊天中明文传递）：
   ```bash
   echo 'export VIKA_TOKEN=你的token' >> ~/.zshrc && source ~/.zshrc
   ```
3. Base URL: `https://api.vika.cn/fusion/v1`

> ⚠️ **CRITICAL — 绝不硬编码 token（2026-08-13 复盘）**：每个 Python 脚本里必须用 `os.environ.get("VIKA_TOKEN")` 读取，先 `source ~/.zshrc` 再运行。**绝对不要在脚本里写死 token 字符串**——之前因硬编码了错误的 token 值（只凭 `echo ${VIKA_TOKEN:0:8}` 看到前 8 位就脑补了后面 15 位），导致所有 API 请求返回 401，误判为"权限问题"浪费了多轮排查。诊断 token 是否失效的方法：调用 `GET /spaces`——能返回空间列表说明 token 有效（是表权限问题），返回 401 说明 token 本身失效或写错了。

### 操作前必做：过滤选导意向非空行

**每次执行增删改操作前，必须先获取所有记录并排除 `选导意向（点击选择）` 非空的行：**

```python
# 获取所有记录
result = vika("GET", "/records?maxRecords=200&fieldKey=name")
all_records = result["data"]["records"]

# 仅保留选导意向为空的行（这些是待编辑的行）
editable = [r for r in all_records if not r["fields"].get("选导意向（点击选择）")]

# 选导意向非空的行（这些是受保护的行，只能读取）
locked = [r for r in all_records if r["fields"].get("选导意向（点击选择）")]

# 所有增删改操作只针对 editable 列表中的 recordId
```

### 能力（记录级 CRUD）

| 操作 | 端点 | 备注 |
|------|------|------|
| 列出字段 | `GET /datasheets/{id}/fields` | 发现字段名和类型 |
| 列出记录 | `GET /datasheets/{id}/records?viewId=...&maxRecords=...` | 支持 filterByFormula、sort、分页 |
| 创建记录 | `POST /datasheets/{id}/records` | 每批最多 10 条。**body 必须是 `{'records': [{'fields': {...}}, ...], 'fieldKey': 'name'}`**——每条记录要包一层 `fields` 键；直接传裸字段映射会返回 HTTP 500 `api_params_instance_fields_error`（2026-09-14 实测踩坑） |
| 更新记录 | `PATCH /datasheets/{id}/records` | 发送 `{"records": [{"recordId":"xxx","fields":{...}}], "fieldKey": "name"}` |
| 删除记录 | `DELETE /datasheets/{id}/records?recordIds=recXXX` | recordIds 在 query parameter 中，非 request body |

### 关键限制

- **DELETE 请求格式**：recordIds 必须在 URL query parameter 中（`?recordIds=recXXX,recYYY`），不能在 request body 中。Helper 函数已自动处理此转换。
- MagicLookUp / OneWayLink 字段不可通过 API 写入。
- 每批最多 10 条记录，批次间加 0.3-0.5 秒延迟。

详细的 API 代码模板和操作指南见 `references/vika-guide.md`。

### ⚠️ 写入前必须重新 GET 当前记录（2026-09-15 实测教训，强制执行）

**同一张表可能在两轮之间被别人改过。** 本次实例：第一轮 GET 快照为 **68 条**记录、含「Greg Aldrich（Kansas State）」；几个小时后第二轮 GET 只剩 **65 条**——该记录已被删除，替换为「Julia Guazzelli Pezzali / Chad Paulk」两条，且申请页已改成正确的 Grain Science 链接。用户随后提出的"待修问题"里，K-State 那一项其实**已经不存在了**。

**若直接拿旧快照去 PATCH，会写到已不存在的 recordId，或把别人刚改好的值覆盖回去。**

**执行清单**：
1. **每次 PATCH / POST / DELETE 之前，重新 GET 一次全表**，不复用上一轮落盘的 `records.json`。
2. **前置断言**：用 `recordId` 存在性 + 待改字段的**当前值**做校验（如 `assert cur[rid][字段].startswith(旧首句)`），不匹配立即中止，不要"尽力而为"地写。
3. **先备份**：改前把原值 dump 到 `backup_before.json`，便于回滚。
4. **写完回读**：再 GET 一遍，逐字段比对确认。
5. **先核对再动手**：用户报的"待修项"可能已经被修掉了，逐条核实现状，避免改坏或重复报告。
6. **两类字段分两次请求**：URL 字段（导师主页 / 博士申请信息 / 其他导师信息）必须用**字段 ID + `fieldKey="id"`**；文本字段用**字段名 + `fieldKey="name"`**。两者不可混在同一请求里。

### 自然语言删除流程

当用户说"删除导师XXX"或"删除这条记录"时，按以下步骤操作：

1. **解析请求**：理解要删除什么（按导师名、按学校、按备注内容等）
2. **查找记录**：用 GET + filterByFormula 找到匹配的记录
   ```python
   # 按导师名查找
   filter_expr = urllib.parse.quote('{导师}="张三"')
   result = vika("GET", f"/records?filterByFormula={filter_expr}&maxRecords=200")
   records = result["data"]["records"]
   ```
3. **提取 recordIds**：从响应中提取 `recordId` 字段
4. **确认删除**：向用户展示找到的记录，确认是否删除
5. **执行删除**：使用正确格式调用 DELETE
   ```python
   # ✅ 正确格式
   vika("DELETE", "/records", {"records": [r["recordId"] for r in records]})
   ```
6. **验证结果**：删除后再次 GET 确认记录已移除

⚠️ **DELETE 格式陷阱**：必须发送 `{"records": ["recXXX"]}`，不能发送纯数组 `["recXXX"]`。

#### 🔴 DELETE 单次上限 10 条（2026-09-21 实测）

`DELETE /datasheets/{ds}/records?recordIds=a,b,c,...` **单次最多 10 条**，超过直接报错（**不是**静默失败）：

```
Can't update/delete/create more than $10 records in one single request
```

- 实测 **8 条/批最稳**；批间 `time.sleep(1)`。
- 注意与 POST/PATCH 的坑**性质不同**：DELETE 是**显式报错**（好排查），而 POST 超 10 条是 **HTTP 201 + success:true 但 `data.records` 返回空数组**（静默失败，回读才发现）。两个都要防。
- 删完必须 `GET` 回读，逐个确认 target recordId 已消失，并打印实际删除条数。

#### 🔴 删行前必须 dump 整行 `fields`，不能只看关键字段（2026-09-21 踩坑）

初筛「空行」时若只检查关键字段（导师/学校/备注等），会把**只保留了非关键字段的行**误判为垃圾行。实测：两条记录 8 个关键字段全空，但其中一条有 `确认套磁=True`、`状态=被拒绝`、`等邮件几天=12`、`选导时间`、`From` —— 是一条**真实处理过的套磁记录**（导师名字段丢失的孤儿行），删掉就丢了历史状态。

**规则**：
1. 判定「空行/垃圾行」时，必须 `print(rec["fields"])` 看**整行所有键**，不能只看白名单字段。
2. 只要该行含「选导时间 / 确认套磁 / 状态 / 套磁备注 / 你的反馈 / From / 状态变更日期」中任一字段，就**不是**可删的垃圾行，应报告给用户人工处置。

---

## 表格验证工作流（验证已有表格时触发）

> 📎 本节全文已迁至 `references/verification-workflows.md`（含 3 个子节）。

## 申请截止日期核查（2026-09-17 沉淀，CRITICAL）

> 📎 本节全文已迁至 `references/verification-workflows.md`（含 5 个子节）。

## 申请信息汇编文档的批量核查（2026-09-24 沉淀）

> 📎 本节全文已迁至 `references/verification-workflows.md`（含 8 个子节）。

## 学生方向偏好逆向分析（2026-09-14 贺禧案例沉淀）

> 📎 本节全文已迁至 `references/analysis-workflows.md`（含 4 个子节）。

## 套磁结果归因分析（2026-09-20 刘艺佳案例沉淀）

> 📎 本节全文已迁至 `references/analysis-workflows.md`（含 11 个子节）。

## 证据纪律：候选生成 ≠ 写入依据（2026-09-17 沉淀，务必执行）

> 📎 本节全文已迁至 `references/evidence-discipline.md`（含 3 个子节）。

## 搜索工作流（Vika 和 Excel 通用）

1. 解析学生背景、研究方向、硬排除条件、目标地区/学校、排名限制
2. **检测表格格式**（见 `references/spreadsheet-rules.md`）：Vika 模式从 URL 解析 datasheetId；Excel 模式若用户提供模板则沿用其列结构
3. 优先搜索官方大学来源
4. **SPA/动态站点**：先查 `references/search-techniques.md` L0-SPA 策略（找替代来源而非死磕 SPA 壳）；若无替代来源再探测 JS bundle 中的 API 端点
5. 按内容验证每个导师主页
6. 使用 `references/selection-rules.md` 判断指导资格
   - **国内学校**：走「国内学校选导规则」子章节（招生目录优先 → A/B/C 分类 → 邮箱必填 → 主页要求）
7. 使用 `references/spreadsheet-rules.md` 填写表格
   - **国内学校**：额外遵守「国内学校表格规则」子章节（导师联系方式必填、主页来源要求、备注链接格式）
8. **写入后立即设置学校关联字段**（见「学校关联字段必填」规则）：确定学校→查找/创建主表记录→设置OneWayLink→验证Location/QS/国内学校层次已同步
9. **飞行前检查清单**（见下方「飞行前检查清单」）：写入前逐项检查 1-10，特别关注 6a/6b/6c（主页类型+硬排除+方向核心度），任一不过则跳过该导师
10. **小批次审核触发**：累计每写完 10 条新记录（或搜完一个学校的全部导师）→ 立即暂停搜索 → spawn 独立的 supervisor-auditor 做对抗审核 → 修 P0 → PASS 后继续
11. 没找到合适导师的学校记录排除原因

---

## 搜索标准

- **搜索引擎为主要策略**查找个人导师资料。搜 `"[导师名] [大学] professor"` 获取真实 URL——不要猜测 URL
  - **国内学校**：使用百度搜索而非 Google。搜索 `"[导师名] [学校名] 教授"` 或 `"[导师名] [学校名] 博士导师"`
- 优先官方大学页面而非个人网站
- **禁止 URL 猜测**：不要通过命名规则构造 URL（失败率约 90%）
- **SPA/JS 渲染页面**：不接受 200 空壳。**优先尝试 L0-SPA 策略**（找替代来源：个人网站、ResearchGate、研究中心页面），不要死磕 SPA 壳。详见 `references/search-techniques.md` L0-SPA 节和 `references/school-strategies.md` 各学校策略
- **并行搜索**：使用 WorkBuddy Agent 工具对不同的学校/域名进行并行检查。给每个 Agent 清晰的独立任务

### 浏览器验证替代方案

WorkBuddy 不能打开真实浏览器，但可以通过以下方式验证：
1. **WebFetch** 工具获取页面实际内容验证
2. **WebSearch** 搜索 `"[Name] [University] professor"` 发现真实 URL
3. **DDG HTML 搜索**：`https://html.duckduckgo.com/html/?q=...` 返回纯 HTML

### 链接验证标准（验证已有表格时强制执行）

**❌ 禁止仅依赖 HTTP 状态码（curl/urllib）判断链接有效性。**

原因：
- 美国大学网站对 404 常返回 **200 + "Page Not Found" 页面内容**
- 旧 URL 路径废弃后可能重定向到院系统一搜索页，状态码仍是 200
- 必须通过 **WebFetch 读取实际页面内容** 才能判断真假

**✅ 正确做法：逐条 WebFetch 验证**

对每个导师主页 URL，必须：
1. **用 WebFetch 获取页面完整内容**
2. **检查页面是否包含导师姓名**（防止 404 伪装页）
3. **判断页面类型**：
   - ✅ **真正个人主页**：含 CV、Publication、Research、Contact、Biography 等专属信息
   - ⚠️ **实验室主页**：多人共用，需标注并在备注中补充个人页链接
   - ❌ **院系教师目录页**：全院教师列表，该导师只是其中一条
   - ❌ **第三方平台**：出版商简介、ORCID、LinkedIn、ResearchGate 等
   - ❌ **404 伪装页**：状态码 200 但内容显示 Not Found / 搜索页

### 导师主页类型前置过滤（搜索阶段强制执行 — 写入前硬门，不可跳过）

**在决定把导师写入表格前，必须先判断导师主页类型和研究方向是否属于硬排除项。这是写入前的硬门（pre-write gate），不是写入后的审计项（post-write audit）。跳过此步骤直接写入 = 偷懒，审核官会整批退回。**

**复盘教训（2026-08-10 优录-刘同学案例）**：7 条 P0 全部是因为写入前没执行此硬门——第三方平台页、医生预约页、CRM 聚合页、`__trashed` URL、线虫模型、纯生信、癌症主线。这些本应在搜索阶段就跳过，却一路漏到最终审核才被发现，浪费了 11% 的工作量。

#### 硬门 A：导师主页类型过滤

以下类型的页面直接跳过，不入表：

| 页面类型 | 判断标准 | 示例 |
|---------|---------|------|
| **第三方平台** | 域名非学校官方（`.edu` 或学校官方子域） | Loop.frontiersin.org、DovePress、ResearchGate、ORCID、Google Scholar、X-MOL、Aminer |
| **医生预约/诊所页** | 页面结构是医生 profile（含预约、就诊信息），无 Publications/Research Lab 板块 | NYU Langone `/doctors/...`、医院医师介绍页 |
| **CRM/中心聚合页** | 页面是研究中心/CRM 系统首页，非个人专属页 | USF `healthscholars.usf.edu/crm`、中心 landing page |
| **院系列表页** | 页面是全系教师列表，该导师只是其中一行 | `psych.zju.edu.cn/27612/list.htm` |
| **SPA 空壳** | 200 状态码但内容 < 1KB 或返回相同字节数的通用 HTML | 无实际内容的 JS 渲染壳 |

**判断方法**：
1. 用 WebFetch 打开候选 URL
2. 检查页面内容是否包含**导师姓名 + 职称 + 研究方向/论文列表**（至少两项）
3. 检查域名是否属于学校官方（`.edu`、学校官方子域、或学校官网明确列出的教师目录子域）
4. 第三方平台、医生预约页、CRM 聚合页 → **直接放弃该导师，不入表**

**例外**：SPA 壳但学校官方域名，且通过 WebSearch 能找到**替代可抓取来源**（如个人网站、实验室 WordPress 页）→ 用替代来源作为导师主页 URL。

#### 硬门 B：研究方向硬排除

以下研究方向属于**通用硬排除项**（与具体学生无关，所有学生一律排除），在搜索阶段发现即跳过，不入表：

| 硬排除项 | 判断标准 | 典型案例 |
|---------|---------|---------|
| **线虫/果蝇/酵母模式生物** | 实验室主线使用 C. elegans / Drosophila / Yeast 作为核心模式动物 | 心衰线虫模型、果蝇神经发育——即使涉及目标疾病，模式生物层级不对 |
| **纯计算生物学（>70% dry lab）** | 研究以生信分析、突变谱解析、计算建模为主，无 wet lab | 纯突变谱分析、纯数据库挖掘——即使方向关键词沾边 |
| **癌症生物学为主线** | 实验室主线是肿瘤/白血病/癌症机制，目标方向只是副业 | 白血病干细胞为主、iPSC 只是工具——即使有 iPSC 关键词 |
| **经济/卫生经济学身份标签** | 主页自述或部门身份为 health economist / 卫生经济学家 / 药物经济学家；研究以支付政策(provider payment)、保险福利设计(Medicare Part D)、成本建模(CEA/QALY/ICER)、经济负担为主方向 | 自述 "I am a health economist"；Division of Health Policy and Economics；研究 Part D 覆盖设计、支付激励、成本效果——**即使研究关键词含"理赔数据/药物政策/真实世界"，只要身份标签是经济学家即排除** |

**身份标签陷阱（2026-08-25 实战教训）**：Yuhua Bao 案例——表内研究领域字段写 "Health economist evaluating real-world effects of drug policies... using large claims data"，因含 `claims data / real-world / medication use` 命中方向1正面关键词，第一轮审核误判为 OK。**根因：只看关键词匹配，忽略句首 "Health economist" 身份标签。** 审核时必须先扫身份标签（economist/经济/payment/Part D/福利设计），命中即视为红线信号，再核对是否为主方向——不能因为同时命中"理赔数据"就放行。

**判断方法**：
1. 打开导师主页，阅读 Research Interests / Publication 列表
2. 目标方向关键词在主页/论文中出现频率是否 >50%（核心方向 vs "研究方向之一"）
3. 如果方向定义书有额外的学生专属排除项，一并对照
4. **先看身份标签，再看关键词**：字段/主页中的 `health economist`、`policy economics`、`payment design`、`cost-effectiveness`、`CEA/QALY/ICER` 是强红线信号，即使同段出现"理赔数据/药物安全/真实世界"等正面词也要以身份标签为准

**注意**：方向定义书中的学生专属排除项由各学生任务单独提供，不写入此通用规则。但 auditor 审核时必须拿到方向定义书原文，独立对照。

---

- **OSU**: `medicine.osu.edu/find-faculty/...` 路径常废弃，faculty 页面迁移到 `mcdb.osu.edu/people/...` 或其他子域名
- **CWRU/CCF**: `lerner.ccf.org/cvme/faculty/...` 可能改为 `my.clevelandclinic.org/staff/...`
- **TAMU**: 部分 faculty 页面在子域名如 `genetics.tamu.edu` 而非主站
- **USF**: `healthscholars.usf.edu` 子域名页面结构不稳定
- **旧 URL 返回 200 但内容为空**：curl 无法识别，必须 WebFetch

---

## 深度发现管线

1. **全面扫描**——通过 API 获取所有教师数据，按目标院系筛选
2. **过滤**——检查剩余教师的学位、专业、研究关键词
3. **优先级排序**——按与学生方向的匹配度排名
4. **验证**——通过 WebFetch 打开个人页面，确认研究内容
5. **扩展**——仅在用户明确要求时重新检查之前 404 的链接

---

---
## 导师转校处理流程（2026-08-07 新增）

若发现导师已从当前学校转到新学校，且新学校在选校范围内有合适的 PhD 项目，则**全面更新以下字段**：

1. **学校名字**：改为新学校的 recordId
2. **导师主页**：更新为新学校的官方 profile URL
3. **导师联系方式**：更新为新学校的邮箱
4. **Department**：更新为新学校的院系/职位
5. **所在PhD项目**：更新为新学校的 PhD 项目名称
6. **博士申请信息**：更新为新学校 PhD 项目 URL
7. **项目综合情况**：改为新学校的项目情况（Stipend/录取难度/业界出路等）
8. **有机化学前置要求** + **官方说明**：更新为新学校的官网依据
9. **备注**：标注转校信息（何时从何处转来），若新职位行政任务重（如 DVC Research）需标注"套磁前确认带生意愿"

**示例**：Mike Ryan 2026年3月从 Monash DVC Research 转到 Sydney DVC Research → 学校从 Monash (QS 31) 更新为 Sydney (QS 28)，主页、邮箱、PhD项目等全部更新。

---
## funding 预计情况：三段式格式（强制执行）

**【28年funding预估风险】和【funding预计情况】两列必须按三段式填写：**

| 段落 | 标题格式 | 内容 |
|------|---------|------|
| 第一段 | `【过往资助历史】` | 该PI历史上获得的主要资助、资助机构、持续时间 |
| 第二段 | `【现有在研资助】` | 当前活跃的资助项目、金额规模、到期时间、实验室现状 |
| 第三段 | `【2028年预测】` | 学生进入博士第二年（2028年）时的资金支持预判、风险点、续约概率 |

**禁止**只写零散描述不按三段式组织。格式要求：每段以`【】`中文标题开头，段落间用 `\n` 分隔。

## 项目综合情况字段结构

> 📎 本节全文已迁至 `references/notes-and-fields.md`（含 13 个子节）。

## 操作权限（CRITICAL — 所有操作前首先检查）

### 🚫 表格隔离：只操作用户指定的那张表

用户每次提供 Vika 分享链接时，从 URL 解析 `datasheetId`（`dstXXX`）。**本轮所有 CRUD 操作仅限于用户本次传入的这张表**。

**绝对禁止：**
- 操作用户未明确指定的其他 datasheet（即使 API token 有权限）
- 操作关联的学校主表（OneWayLink/MagicLookUp 引用的表）
- 通过 API 修改关联表的任何字段
- 在用户未给链接时自行假设或复用之前的 datasheetId

### 🚫 范围外记录保护：非目标范围记录禁止删除（2026-08-05 新增，CRITICAL）

**用户目标范围之外、但已存在于表格中的历史记录（如其他国家的学校、不在本轮目标州/排名范围内的学校），默认保留，禁止删除。**

删除操作是**高危且不可逆**的（Vika API 删除后无回收站恢复接口，只能网页端「时光机」整表回滚）。因此：

**绝对禁止：**
- 因"不在本轮目标范围"而主动删除已有记录（即使该记录可编辑、选导意向为空）
- 因"与当前学生需求不匹配"而批量清理历史记录
- 未经用户明确确认执行任何 DELETE 操作

**唯一允许删除的情形（全部满足才可删）：**
1. 用户在本轮任务中**明确点名**要求删除某条记录（如"删除导师XXX"），且已向用户展示待删记录并获确认
2. 质量维护场景：验证确认导师**已离任/页面永久 404/官方目录已无此人**（离任导师检测规则），且该记录不是本轮新增

**范围外记录的正确处理方式：**
- 保留原样不动；如需提示可在交付报告中向用户说明"表内存在 XX 条范围外历史记录，未做处理"
- 若用户明确要求清理，先列出将删除的记录清单，**等用户确认后再执行**

**删除流程铁律：任何 DELETE 调用前，必须在操作记录中留下理由（用户点名/离任验证），并在回传结果中逐条列出被删记录。**

### 🚫 选导意向保护：已填写=不可触碰

当 Vika 表中 `选导意向（点击选择）` 字段有值（非空/非 null）时：
- **禁止修改**该行的任何字段
- **禁止删除**该行
- **禁止覆盖**该行的备注、研究方向、导师主页等字段
- **仅可读取**，不可写入

这些是学生已经审阅并反馈过的记录，任何修改都会造成数据损失。

**操作前必须：**
1. 先 GET 所有记录
2. 过滤掉 `选导意向（点击选择）` 非空的行
3. 仅对 `选导意向` 为空的行执行增删改操作

### 📋 当前活跃表（由用户传入）

表的链接和 datasheetId 随每次任务由用户提供，不固定。首次操作时从链接解析并确认。

---

## 关键规则（CRITICAL）

> 📎 2026-10-07 二次拆分：原 `critical-rules.md`（876 行）已按内容性质拆为三本——
> - **`references/rules-write.md`**（185 行）：写入前硬规则全集，**可整读，写入前必读**
> - **`references/vika-school-link.md`**（291 行）：学校关联字段六步操作手册
> - **`references/cases-rules.md`**（392 行）：案例 · 数据 · 某校特殊规则明细 · 批量方法论，**按关键词定位，禁止整读**

## 飞行前检查清单（添加导师前强制执行）

```
[ ] 1. 搜索引擎搜索: "[Name] [University] professor"
[ ] 2. 打开个人页面: 确认姓名、职称、院系
[ ] 3. 检查研究: 阅读 Research Interests 部分
[ ] 4. 检查活跃状态: 非 Emeritus/Retired/Visiting
[ ] 5. 匹配方向: 研究关键词与学生方向对比
[ ] 6. 个人 URL: 验证是个人页面而非通用列表页
[ ] 6a. 主页类型检查: 非第三方平台/医生预约页/CRM聚合页/SPA空壳 → 否则直接跳过
[ ] 6b. 硬排除检查: 研究主线非线虫/果蝇/酵母模式生物、非纯计算(>70% dry lab)、非癌症生物学为主线 → 否则直接跳过，不入表
[ ] 6c. 方向核心度: 该方向是实验室主攻方向（非"研究方向之一"），在导师主页/论文中出现频率 >50%
[ ] 7. 写入记录: 所有检查通过后再写入
[ ] 8. 获取学校主表 ID: GET /datasheets/{id}/fields → 找 OneWayLink 字段的 property.foreignDatasheetId
[ ] 9. 设置学校关联: 写入后立即设置 OneWayLink → 验证 Location/QS/国内学校层次 已同步
[ ] 10. 批次审核触发: 累计每写完 10 条新记录 → 立即暂停搜索，spawn supervisor-auditor 做对抗审核
```

---

## ✅ 交付前机械复查 SOP（10 项，全部可脚本化）

> 📎 本节全文已迁至 `references/verification-workflows.md`。2026-10-07 新增两项：第 9 项「地区职称门槛闸门」（HK/MO 助理教授及以上；讲师序列一刀切，不自行套用「页面明示可带博」例外）与第 10 项「项目与学校覆盖完整性」（逐校核对博士学位课程总目录，防整所学校/整个项目缺席）。

## 🇭🇰 港城 / 港理 / 浸会 三校抓取口径（2026-09-24 黄肇启案例沉淀）

> 📎 本节全文已迁至 `references/school-strategies.md`（含 5 个子节）。

## 常见错误速查表

> 📎 本节全文已迁至 `references/common-errors.md`。

## 链接修复工作流（用户说"链接打不开/404"时触发）

> 📎 本节全文已迁至 `references/verification-workflows.md`（含 6 个子节）。

## 小批次强制审核（搜索阶段强制执行）

**不要等所有学校搜完再统一审核。每写完 10 条新记录，必须立即 spawn supervisor-auditor 做对抗审核。**

### 审核触发条件

| 场景 | 操作 |
|------|------|
| 写完 10 条新记录 | 立即停，spawn supervisor-auditor（独立 spawn，见下方「独立审核原则」） |
| 搜完一个学校的全部导师 | 即使不足 10 条，也 spawn auditor |
| auditor 返回 P0 | 修正后再继续搜索，不积压 |
| 选导顾问同一会话已处理 30+ 条 | 建议用户为新批次开新会话（长对话疲劳防范） |

### 修正后二次验证

收到 auditor 的 P0 清单后：
1. 对 P0 记录立即修正（换链接/改备注/删除）
2. 修正后重新 spawn auditor 验证同一批
3. 确认 PASS 后再进入下一轮搜索

### 独立审核原则（CRITICAL — 防止确认偏误和长对话疲劳）

**复盘教训（2026-08-10 优录-刘同学案例）**：同一个选导顾问在长对话中反复复查自己的产出，始终认为"没问题"；换一个新对话框让 auditor 独立审核，立即查出 7 条 P0。根因是：自己审自己填的东西，天然查不出"该不该留"的问题；长对话几十轮后对同一批记录产生"看过了"的疲劳性放过。

**因此，批次审核必须遵守以下原则：**

| 原则 | 要求 | 为什么 |
|------|------|--------|
| **独立 spawn** | 每次批次审核必须 spawn 一个**全新的** supervisor-auditor agent，不能复用选导顾问的上下文 | 选导顾问在填表过程中已经形成了"这些导师都合适"的先入为主，带着这个心态审核等于不审 |
| **新鲜视角** | auditor 拿到的只有：学生方向定义书原文 + 本批 10 条记录数据，没有选导顾问的判断过程和理由 | 让 auditor 独立判断"这条该不该留"，而不是"选导顾问的判断对不对" |
| **方向定义书独立验证** | auditor 必须亲自阅读学生方向定义书的**原文**，不能只看选导顾问转述的摘要 | 选导顾问在转述时可能无意识地缩小了方向范围（如把"干细胞+心血管"转述成"干细胞"），导致方向核心度判断失准 |
| **审核心态：有罪推定** | auditor 的立场是"每条记录默认有 P0，除非能证明它没有"。不是"默认没问题，除非发现问题" | 确认偏误让人倾向于"找到理由就放行"；有罪推定强制 auditor 主动找理由拒绝 |
| **长对话疲劳防范** | 若选导顾问在同一会话中已处理 30+ 条记录，必须建议用户为新批次开一个新会话 | 30 轮后注意力下降，对"看起来还行"的记录容易直接放过——优录-刘同学案例正是如此 |

### auditor 指令模板（升级版）

每次 spawn supervisor-auditor 时，传递以下指令：

```
你是一名选导审计官。你的立场是"有罪推定"——每条记录默认有 P0，除非你能证明它没有。

你将收到：
1. 学生方向定义书原文（你自己读，不信任任何人的转述）
2. 本批 X 条新记录数据

审核规则（逐条检查，一项不通过即标记 P0）：

A. 链接类型检查：
   - 导师主页必须是大学官方页面（.edu 或学校官方子域）
   - 排除：第三方平台（Loop/DovePress/ResearchGate/ORCID）、医生预约页、CRM聚合页、院系列表页、SPA空壳
   - 你要主动找理由判定不合格，而不是找理由放行

B. 方向核心度检查（必须独立读方向定义书）：
   - 你自己阅读学生方向定义书原文，不信任选导顾问的摘要
   - 该导师的研究方向是实验室主攻方向，还是只是"研究方向之一"？
   - 硬排除：线虫/果蝇/酵母模式生物？纯计算(>70% dry lab)？癌症生物学为主线？
   - 如果方向定义书写明了排除项，你必须逐条对照

C. URL 健康检查：
   - URL 不含 __trashed、_legacy、_old
   - 非 302 跳转到搜索页/列表页
   - WebFetch 能读取到导师姓名+职称+研究方向（非 WAF 挑战页）

D. 排除规则执行审计：
   - 选导顾问是否执行了飞行前清单的 6b（硬排除检查）和 6c（方向核心度）？
   - 如果备注出现 emoji 符号（🔥👍⚠️✅ 等） → P0（AI 痕迹）
   - 如果备注出现方向编号（方向1/方向2/TOP/SECONDARY） → P0（学生不知道方向书）
   - 如果备注出现⚠️标签、✅标签或工具名称（Vika/表格/源数据） → P0（AI 痕迹，人工操作不应出现）
   - 如果备注出现修正记录语言（职称修正/Vika写/已确认/已核实） → P0（元注释泄漏）
   - 如果备注出现外部链接（Google Scholar / ResearchGate / PubMed）且导师主页并非「信息极少」→ P0（应放导师主页列）
   - 如果备注出现方向偏向主观评价（方向偏X、没有非常符合的老师） → P1（语气不合格）
   - 如果备注出现「建议先确认 XX」「套磁前建议先确认带博」「建议先邮件确认」「确认带生意愿」这类把核实责任推给学生的表述 → P0（监督资格不明类必须改为 `未明确表明监督资格，可以后放～`；退休/年龄类改为 `……但现在应该到退休年龄了，可以后放～`；一律用全角波浪号）
   - **备注可追溯性审计（2026-09-17 新增）**：备注里出现的**事实性表述**——著作/论文/奖项、在研项目、招生或带生标注（"接受博士生""正在招收"）、以及"某页面把 XX 列为……"这类引述其他页面的说法——必须逐条在**该记录的三个链接页面**（`导师主页`/`博士申请信息`/`其他导师信息`）的正文里找到。**在三个链接里都找不到、又没有在备注里给出来源链接的 → P0**（学生打开链接会找不到，直接质疑整张表）。判断性表述（如"未明确表明监督资格，可以后放～"）不在此列
   - **来源链接写法审计（2026-09-17 新增）**：给出处时写成 `（XX页可见：<url>）`、`XX学者库页（<url>）标注……`、`这个链接<url>标注其……` 这类**来源页名称+括号的批注式写法**，或让"页面/名录/学者库/项目页"当句子主语的（`页面标注接收博士生`）→ **P1（AI 腔，语气不合格）**，需改为 `可以看这个链接：<url>` + 直接陈述事实（`欢迎博士生`）
   - **备选标识必须有理由（2026-09-28 新增，用户明确要求）**：备注写了 `可以备选一下呢～` / `可以往后放一放～` / `可以往XX方向靠～` 这类**优先级后缀，但同一句里没有写明"偏在哪"**（场景不对/方法不对/对象不对/不在体育交叉线上）→ **P0**。学生看到「明明写了能搭上，却让我后放」，会认为标注是随手加的，进而推翻整条记录（王灏案例：Kwon、Rouhani 两条被标备选但无理由，学生本人随后手动改成「优先套磁」）。修正＝补一句具体的偏离说明，保留后缀
   - 若发现**人工已填 `选导意向` 的记录，其备注仍与学生的选择冲突**（如学生标了"优先套磁"、备注却写"可以后放～"）→ 报 P1 并**交由用户决定**，不要自行回改已有人工决策的记录

输出格式：
- 逐条输出检查结果（A/B/C/D 各项 PASS 或 FAIL + 原因）
- 汇总：P0 清单（记录编号 + 原因 + 修正建议）
- 无 P0 则输出 "PASS — 本批 X 条记录全部通过强制验证清单"
```

---

## 写入后审计（强制执行）

每次批量写入 Vika 后，运行审计脚本：

```bash
python3 scripts/audit.py [DATASHEET_ID] [VIKA_TOKEN]
```

审计检查：
1. 交叉链接（URL 域名与 Department 不匹配）
2. 备注格式（缺少；分隔符、缺少句号）
3. 备注中是否有垃圾内容
4. 缺少必填字段（导师主页、博士申请信息、其他导师信息）
5. **国内学校**：检查 `导师联系方式` 是否为空，是否为有效 email 格式

## 链接健康审计（用户报"链接404/badcase"时，2026-08-04 新增）

> 📎 本节全文已迁至 `references/verification-workflows.md`。

## 🍁 加拿大批次专属陷阱（2026-09-24 王灏案例沉淀）

> 📎 本节全文已迁至 `references/school-strategies.md`（含 7 个子节）。

## 协作流程（"开始学生" / "结束学生"）

当用户说**"开始学生"**（或"提交更新"、"同步并提交"等）时，自动执行 pull -> branch -> commit -> push -> PR 全流程。当用户说**"结束学生"**时，先提取本轮搜索经验更新策略库，再自动执行同步流程。

**完整执行步骤见 `references/collaboration-workflow.md`。** 触发后按该文档的 11 步流程执行，无需用户懂 git。

---

## 🔁「回归本源方向」型任务：审核要比常规更狠（2026-09-24 王鹏涛案例沉淀）

> 📎 本节全文已迁至 `references/analysis-workflows.md`。

## 🌐 抓取通道实测补充（2026-09-24）

> 📎 本节全文已迁至 `references/access-channels.md`。

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

## 港澳·澳新院校抓取通道情报（2026-09-24 王润泽第三轮沉淀）

> 📎 本节全文已迁至 `references/access-channels.md`（含 8 个子节）。

## 🔎 找院系页的最快通道：先读 sitemap.xml（2026-09-24 验证有效）

> 📎 本节全文已迁至 `references/access-channels.md`（含 4 个子节）。

## 🆕 2026-09 新版学生表结构（统一学校主表）· 2026-09-29 实测

> 📎 本节全文已迁至 `references/vika-guide.md`（含 1 个子节）。

## 🗺️ 院系名录页索引 + 覆盖度台账（2026-09-29 实测）

> 📎 本节全文已迁至 `references/school-strategies.md`（含 4 个子节）。

## ⚠️ 「备选」与「后放」是两套机制，别混，也别只写一种（2026-09-29 王润泽批次复盘）

> 📎 本节全文已迁至 `references/notes-and-fields.md`。

## 🔁 批量修订已有记录的备注（2026-09-29 实操，可直接复用）

> 📎 本节全文已迁至 `references/vika-guide.md`（含 3 个子节）。
