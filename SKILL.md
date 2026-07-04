---
name: phd-supervisor-selector
description: 博士导师筛选与表格管理工具。面向留学机构，为不同方向的学生快速建立可核验的导师列表。搜索各大学官方页面，判断导师是否具备 PhD 指导资格，填写表格各列。主力支持 Vika 在线表格直接 CRUD，Excel 作为可选回退模式。
agent_created: true
---

# PhD Supervisor Selector（博士导师筛选器）

## 概述

为博士申请者建立有据可查的导师列表。搜索各大学官方页面，判断导师是否具备 PhD 指导资格，填写表格各列，将不合格或高风险候选人排除在主表之外。

**主力模式：Vika（在线表格直接 CRUD）。Excel 作为可选回退模式。**

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

## 数据源检测

收到任务时，检测数据源：

1. **用户提供 Vika 分享链接**（如 `https://vika.cn/share/shrXXX/dstXXX/viwXXX`）：直接通过 Fusion API 操作 Vika 表格
2. **用户上传 `.xlsx` 文件**：操作本地电子表格
3. **用户同时提供**：优先 Vika 做 CRUD，Excel 做参考/填充源

---

## Excel 模式（可选）

当用户上传 `.xlsx` 文件而非 Vika 链接时，使用 Excel 模式。详见 `references/spreadsheet-rules.md`（列格式选择、列偏移检测、备注规则、质量检查）。

**默认输出列**：`导师`, `Location`, `学校名字`, `QS排名`, `美国USNEWS排名`, `Department`, `导师主页`, `博士申请信息`, `其他导师信息`, `备注`

- `美国USNEWS排名`：仅当列表中有美国学校时包含此列

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
| 创建记录 | `POST /datasheets/{id}/records` | 每批最多 10 条，使用 `fieldKey: "name"` |
| 更新记录 | `PATCH /datasheets/{id}/records` | 发送 `{"records": [{"recordId":"xxx","fields":{...}}], "fieldKey": "name"}` |
| 删除记录 | `DELETE /datasheets/{id}/records?recordIds=recXXX` | recordIds 在 query parameter 中，非 request body |

### 关键限制

- **DELETE 请求格式**：recordIds 必须在 URL query parameter 中（`?recordIds=recXXX,recYYY`），不能在 request body 中。Helper 函数已自动处理此转换。
- MagicLookUp / OneWayLink 字段不可通过 API 写入。
- 每批最多 10 条记录，批次间加 0.3-0.5 秒延迟。

详细的 API 代码模板和操作指南见 `references/vika-guide.md`。

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

---

## 搜索工作流（Vika 和 Excel 通用）

1. 解析学生背景、研究方向、硬排除条件、目标地区/学校、排名限制
2. **检测表格格式**（见 `references/spreadsheet-rules.md`）：Vika 模式从 URL 解析 datasheetId；Excel 模式若用户提供模板则沿用其列结构
3. 优先搜索官方大学来源
4. **SPA/动态站点**：先查 `references/search-techniques.md` L0-SPA 策略（找替代来源而非死磕 SPA 壳）；若无替代来源再探测 JS bundle 中的 API 端点
5. 按内容验证每个导师主页
6. 使用 `references/selection-rules.md` 判断指导资格
7. 使用 `references/spreadsheet-rules.md` 填写表格
8. 没找到合适导师的学校记录排除原因

---

## 搜索标准

- **搜索引擎为主要策略**查找个人导师资料。搜 `"[导师名] [大学] professor"` 获取真实 URL——不要猜测 URL
- 优先官方大学页面而非个人网站
- **禁止 URL 猜测**：不要通过命名规则构造 URL（失败率约 90%）
- **SPA/JS 渲染页面**：不接受 200 空壳。**优先尝试 L0-SPA 策略**（找替代来源：个人网站、ResearchGate、研究中心页面），不要死磕 SPA 壳。详见 `references/search-techniques.md` L0-SPA 节和 `references/school-strategies.md` 各学校策略
- **并行搜索**：使用 WorkBuddy Agent 工具对不同的学校/域名进行并行检查。给每个 Agent 清晰的独立任务

### 浏览器验证替代方案

WorkBuddy 不能打开真实浏览器，但可以通过以下方式验证：
1. **WebFetch** 工具获取页面实际内容验证
2. **WebSearch** 搜索 `"[Name] [University] professor"` 发现真实 URL
3. **DDG HTML 搜索**：`https://html.duckduckgo.com/html/?q=...` 返回纯 HTML

---

## 深度发现管线

1. **全面扫描**——通过 API 获取所有教师数据，按目标院系筛选
2. **过滤**——检查剩余教师的学位、专业、研究关键词
3. **优先级排序**——按与学生方向的匹配度排名
4. **验证**——通过 WebFetch 打开个人页面，确认研究内容
5. **扩展**——仅在用户明确要求时重新检查之前 404 的链接

---

## 备注风格

**默认使用中文填写备注**，即使 Excel 源数据的研究方向为英文也需翻译为中文关键词。格式：`职称；研究方向（中文关键词）；风险/注意事项。`

### 🎯 语气要求：像面对面和学生说话

备注是给申请学生看的，语气要自然、有"人味"，像坐在旁边帮 ta 梳理信息的口吻。

- **不要**写"符合XX方向""匹配XX方向"——太机械，像机器打分
- **要**写"可以往XX方向贴合""可以试试往XX靠""和XX方向能搭上"——有商量感，留余量
- **不要**堆砌术语关键词——写完要读一遍，想象你是说给一个紧张的申请者听的
- **要**写短句，多用"，"和"；"，少用长定语句
- 信息量要保持，但语气要松弛——是"帮你梳理"不是"给你打分"

### 📊 匹配度分级（备注结尾标识）

每条备注结尾根据匹配度加一句标识，让学生一眼能判断优先级：

| 级别 | 标识语 | 触发条件 |
|------|--------|----------|
| 🔥 强匹配 | `特别推荐看一下～` | 方向多重重叠 + 顶刊发表 + 正在招博士/有成熟指导记录 |
| 👍 一般匹配 | `比较相关～` | 研究方向与学生1-2个目标方向直接相关，有合理发表记录 |
| 👀 弱相关 | `可以备选一下哈～` | 方向有一定交叉但非核心对应，或资历/职称偏早期 |

**禁止使用主观评价用语**如 `高度匹配`、`很匹配`、`完美匹配`。描述事实，不做评判。

示例：
- `副教授；研究博物馆、装饰艺术、珍奇柜这些；教学岗，辅导资格待确认。`
- `教授；做文化遗产和建筑史，可以往遗产保护方向靠；建筑遗产方面偏重一些。`
- `副教授；消费者判断与决策、跨期选择，和品牌传播能搭上。`
- `助理教授；消费者决策、道德决策、自我概念清晰度；MIT PhD，可以关注一下。`
- `副教授；做数字消费者行为和 AI 在营销里的应用，品牌传播和媒介技术都能搭上；Nature和JMR都有发，正在招博士生。特别推荐看一下～`

### 当学校匹配导师极少时（1-2位）

**在备注末尾补充说明该系其他教师的主要方向**，让学生有"已全面搜索"的信心。使用客观描述，不要写"确实没有"等主观判断。

正确示例：
- `教授；决策神经科学、风险与社会决策、无创脑刺激；这个系老师主要做临床和辅导实践方向，只有这一位和消费者决策搭边。`
- `副教授；消费者判断与决策；这个系以社会认知和神经犯罪学为主，就这一位和消费者行为能搭上。`

要点：
- 说明"这个系老师主要做XX方向"——客观陈述事实
- 说明"只有这一位和XX搭边"——给出数量，让学生有"全面看过了"的感觉
- 不要写"没有合适的"、"确实没有"等主观评价

**补充信息行写入规则**：当需要另起一行单独写入系/院的补充说明（如某系无匹配导师）时，只需填写 `导师` 和 `备注` 两个字段，无需填写导师主页、博士申请信息等其他字段。

---

## 操作权限（CRITICAL — 所有操作前首先检查）

### 🚫 表格隔离：只操作用户指定的那张表

用户每次提供 Vika 分享链接时，从 URL 解析 `datasheetId`（`dstXXX`）。**本轮所有 CRUD 操作仅限于用户本次传入的这张表**。

**绝对禁止：**
- 操作用户未明确指定的其他 datasheet（即使 API token 有权限）
- 操作关联的学校主表（OneWayLink/MagicLookUp 引用的表）
- 通过 API 修改关联表的任何字段
- 在用户未给链接时自行假设或复用之前的 datasheetId

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

### SPA 壳返回 200 ≠ 链接有效
200 状态码 + SPA 壳（响应 <5KB，同域所有请求返回相同字节数）→ **不能确认导师存在**。立即切换到 **L0-SPA 策略**：通过 WebSearch 找替代来源（个人网站、ResearchGate、研究中心页面），不要在 SPA 壳上浪费尝试。详见 `references/search-techniques.md` L0-SPA 节。

### 导师主页必须是个人 URL
禁止使用通用院系列表页。每位导师必须有自己唯一的个人主页 URL。

### 禁止在备注中使用 ✅
✅ 标记是临时验证备注，不是研究事实。⚠️ 仅在页面真的被封锁时用作最后手段。

### 禁止在备注中写入报名/联系方式
不要写 "预计2026年入学"、"需发简历至xxx" 等内容。

### 禁止在备注中写入方向偏向
不要写 "方向偏X"、"没有非常符合的老师" 等主观评价。

### 排除退休/名誉教授
不添加 Emeritus、退休、约 70 岁以上、或不在当前教职员目录中的导师。

### 禁止修改已填写选导意向的记录（见上方「操作权限」）

当 Vika 表中 `选导意向（点击选择）` 非空时，该行即被锁定——不得修改、删除或覆盖。详见「操作权限 → 选导意向保护」。

### 禁止向 MagicLookUp 或计算字段写入
QS排名、Location、美国USNEWS排名等字段通过 API 只读。

### 新增记录去重
写入新记录前，检查是否已经存在于已有选导意向的记录中。

---

## 飞行前检查清单（添加导师前强制执行）

```
[ ] 1. 搜索引擎搜索: "[Name] [University] professor"
[ ] 2. 打开个人页面: 确认姓名、职称、院系
[ ] 3. 检查研究: 阅读 Research Interests 部分
[ ] 4. 检查活跃状态: 非 Emeritus/Retired/Visiting
[ ] 5. 匹配方向: 研究关键词与学生方向对比
[ ] 6. 个人 URL: 验证是个人页面而非通用列表页
[ ] 7. 写入记录: 所有 6 步检查通过后再写入
```

---

## 常见错误速查表

| 错误 | 示例 | 正确做法 |
|------|------|---------|
| 猜测 URL | 直接构造 URL 而不搜索 | 先用搜索引擎搜索 |
| 仅凭职称添加 | 看到 "Head of Education" 就加，未检查研究 | 打开个人页 → 读研究 → 确认匹配 |
| 未验证活跃状态 | 添加已退休教授 | 检查大学教职员状态 |
| 使用系列表页作导师主页 | 用 /people/ 而非 /people/john-doe/ | 找到个人 URL |
| SPA 壳当有效 | 200 响应但无内容 | 交叉验证姓名和内容 |

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

---

## 协作流程（"同步技能" / "结束学生"）

当用户说**"同步技能"**（或"提交更新"、"同步并提交"等）时，自动执行 pull -> branch -> commit -> push -> PR 全流程。当用户说**"结束学生"**时，先提取本轮搜索经验更新策略库，再自动执行同步流程。

**完整执行步骤见 `references/collaboration-workflow.md`。** 触发后按该文档的 11 步流程执行，无需用户懂 git。

---

## 参考文献

- 决定候选人能否进入主表前，阅读 `references/selection-rules.md`
- 创建/编辑/验证表格前，阅读 `references/spreadsheet-rules.md`
- 开始搜索前，阅读 `references/search-orchestrator.md`
- 访问学校前，检查 `references/school-strategies.md`
- SPA/API 发现技巧，见 `references/search-techniques.md`
- Vika 完整 CRUD 操作 + API 代码模板，见 `references/vika-guide.md`
- 协作流程（同步技能/结束学生），见 `references/collaboration-workflow.md`
