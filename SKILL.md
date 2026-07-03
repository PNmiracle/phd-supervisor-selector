---
name: phd-supervisor-selector
description: 博士导师筛选与表格管理工具。当用户需要搜索、筛选、验证、扩充、清理或填充博士申请导师表时使用。支持关键词：博士选导、导师表、Supervisor List、博导、PhD supervisor、导师主页、博士申请信息、QS排名、备注、排除学校等。支持 Vika 在线表格和本地 Excel 两种模式。
agent_created: true
---

# PhD Supervisor Selector（博士导师筛选器）

## 概述

为博士申请者建立有据可查的导师列表。搜索各大学官方页面，判断导师是否具备 PhD 指导资格，填写表格各列，将不合格或高风险候选人排除在主表之外。

**支持两种模式：Vika（在线表格直接 CRUD）和 Excel（本地电子表格）。**

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

### Excel 列偏移检测（CRITICAL）

当 Excel 表头包含 `序号` 列但数据体该列为空时，所有后续数据会整体左移一列。**必须在解析 Excel 前检测此情况：**

1. 读取表头，确认是否有 `序号` 列
2. 读取前几行数据，检查 `序号` 列是否有实际值
3. 若表头有 `序号` 但数据行为空 → 数据从 `序号` 的下一列开始，需修正列映射
4. 修正方式：跳过空 `序号` 列，将表头第 N+1 列（学校等）映射到数据体第 N 列

示例错行情况：
```
表头: [优先级, 序号, 学校, 学院/系, 导师姓名, 职称, 研究方向, ...]
数据: [P0,      空,  NUS,  Business School,  Xiuping Li,  副教授,  Consumer..., ...]
                                            ↑ 实际是第4列数据，映射到表头第5列
```

正确映射：`数据[0]→优先级, 数据[1]→学校(跳过序号), 数据[2]→学院/系, 数据[3]→导师姓名, ...`

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

详细的 API 代码模板见 `references/vika-api-patterns.md`，完整操作指南见 `references/vika-operations-guide.md`。

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

## Excel 工作流

### 核心流程

1. 解析学生背景、研究方向、硬排除条件、目标地区/学校、排名限制
2. **检测表格格式**（见 `references/spreadsheet-rules.md`）：若用户提供模板，沿用其列结构；否则使用默认简化格式
3. 优先搜索官方大学来源
4. **SPA/动态站点**：探测 JS bundle 中的 API 端点再放弃
5. 按内容验证每个导师主页
6. 使用 `references/selection-rules.md` 判断指导资格
7. 使用 `references/spreadsheet-rules.md` 填写表格
8. 没找到合适导师的学校记录排除原因

### 默认输出列

`导师`, `Location`, `学校名字`, `QS排名`, `美国USNEWS排名`, `Department`, `导师主页`, `博士申请信息`, `其他导师信息`, `备注`

- `美国USNEWS排名`：**仅当列表中有美国学校时包含此列**

---

## 搜索标准

- **搜索引擎为主要策略**查找个人导师资料。搜 `"[导师名] [大学] professor"` 获取真实 URL——不要猜测 URL
- 优先官方大学页面而非个人网站
- **禁止 URL 猜测**：不要通过命名规则构造 URL（失败率约 90%）
- **SPA/JS 渲染页面**：不接受 200 空壳。见 `references/search-techniques.md`
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

保持备注简短具体。**禁止使用主观评价用语**如 `高度匹配`、`很匹配`、`完美匹配`。描述事实，不做评判。

示例：
- `副教授；博物馆研究、装饰艺术、珍奇柜；教学岗待确认。`
- `教授；文化遗产、建筑史、遗产保护；建筑遗产偏重。`
- `副教授；消费者判断与决策、跨期选择。`
- `助理教授；消费者决策、道德决策、自我概念清晰度。MIT PhD。`

### 当学校匹配导师极少时（1-2位）

**在备注末尾补充说明该系其他教师的主要方向**，让学生有"已全面搜索"的信心。使用客观描述，不要写"确实没有"等主观判断。

正确示例：
- `教授；决策神经科学、风险与社会决策、无创脑刺激；该系教师主要研究临床/辅导实践方向，仅有一位与消费者决策相关。`
- `副教授；消费者判断与决策；该系以社会认知与神经犯罪学为主，仅此一位与消费者行为相关。`

要点：
- 说明"该系教师主要研究XX方向"——客观陈述事实
- 说明"仅有X位与目标方向相关"——给出数量，让学生有"全面看过了"的感觉
- 不要写"没有合适的"、"确实没有"等主观评价

---

## 关键规则（CRITICAL）

### SPA 壳返回 200 ≠ 链接有效
200 状态码 + SPA 壳（同域所有请求返回相同字节数）→ **不能确认导师存在**。必须交叉验证。

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

### 禁止修改已填写选导意向的记录
当 Vika 表中 `选导意向（点击选择）` 非空时 → **不要修改、删除或覆盖**。这些都是学生已审阅的记录。

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

## 参考文献

- 决定候选人能否进入主表前，阅读 `references/selection-rules.md`
- 创建/编辑/验证表格前，阅读 `references/spreadsheet-rules.md`
- 开始搜索前，阅读 `references/search-orchestrator.md`
- 访问学校前，检查 `references/school-strategies.md`
- SPA/API 发现技巧，见 `references/search-techniques.md`
- Vika 完整 CRUD 操作指南，见 `references/vika-operations-guide.md`
- Vika API 代码模板，见 `references/vika-api-patterns.md`
