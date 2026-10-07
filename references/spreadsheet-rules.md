<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：Excel 回退模式下的列格式规则：列结构判定、序号列偏移陷阱、主页链接规则、备注、附加表、质量检查、常见边缘情况、国内学校表规则
> **什么时候读**：任务落在 Excel / 本地工作簿而非 Vika 时
> **什么时候不用读**：主力 Vika 模式（默认路径）——Vika 字段规则看 field-rules.md 与 notes-and-fields.md

---

# Supervisor Spreadsheet Rules

## Column Format Selection

### Decision Tree

When starting work, decide the column structure:

1. **User provided a template `.xlsx`?** → Use the template's exact column headers. Never rename or restructure them.
2. **No template, list includes US schools?** → Use simplified format WITH `美国USNEWS排名` column.
3. **No template, list is entirely non-US?** → Use simplified format WITHOUT `美国USNEWS排名` column.

### Main Columns (Simplified Format, Default)

- `导师`: supervisor name as shown on the profile.
- `Location`: country/region, e.g. `Hong Kong`, `Australia`, `United Kingdom`.
- `学校名字`: official English school name unless the user asks for Chinese.
- `QS排名`: current QS rank; use `QS 2026约XX` or `QS 2026待复核` if not verified.
- `美国USNEWS排名`: **only include this column when at least one US school is in the list.** Omit entirely for all-non-US lists.
- `Department`: department/school/center that owns the profile.
- `导师主页`: official profile page, team page, or official staff entry that visibly matches the person.
- `导师联系方式`: supervisor contact email. **Mandatory for domestic (China mainland) schools.** Fill with the supervisor's email address. For non-domestic schools, fill when available but not required.
- `博士申请信息`: official PhD/research degree/program application page.
  - ⚠️ **必须是「该项目」自己的项目/申请页，不能填全校统一的研究生申请总入口**（2026-09-17 用户明确要求）。同一学校不同院系的导师，该列应分别指向各自院系的研究学位项目页；只有**同院系**导师才允许共用同一 URL。
  - 反例（禁止）：`/study/postgraduate-research/how-to-apply`、`/postgraduate-research/how-to-apply/`、`/study/phd`、`/postgraduate/research/apply/` 这类 "How to apply" 总入口。
  - 正例：`dance.ucr.edu/phd-program/`、`dance.osu.edu/prospective-students/about-phd`、KCL 的 `/study/postgraduate-research/areas/<dept>-research-mphil-phd`。
  - 查找方法：先在学校 research degrees / course finder 列表页按院系找项目页；核对页面 H1 或 Key information 的 Award 与该项目对应，并实测 200。确实找不到项目页时，宁可留空或标注，也不要退回全校入口。
  - **批量自检**：该列写完后统计 URL 出现次数——若同一 URL 在**不同院系**记录间大量重复（尤其排在全表高频 URL 前列），基本就是误填了全校入口，必须回头逐条改。
  - ⚠️ **高发误填场景（2026-09-22 实测踩过）**：① 院系官网前端渲染、抓不到项目页 → 退回填了学院首页（如 `hss.cuhk.edu.cn/en`，该页根本没有入学信息）；② 项目页藏在**另一个子域**（如港中深人文社科学院的项目页在 `hsspg.cuhk.edu.cn`，不在 `hss.cuhk.edu.cn`）；③ 同一学校只抓到一个"看起来很正规"的列表页就全校通用。写完后务必按院系抽样打开确认页面 H1 是该项目名。
- `导师研究领域`: **必填**。用英文、分号分隔的研究方向关键词，取自官方页面的 `Research Field` / `Research Fields` / `Research` 段原文。
  - ⚠️ **易漏项**：批量写入时若某院系页面的字段标签与其他校不同（如港中深 SDS 用 `Research Field`、HSS 用 `Research`），提取脚本容易整批跳过而静默留空。**写入后必须跑一次空值扫描**（见下）。
- `其他导师信息`: same department/school staff list or official supervisor list.
- `备注`: short Chinese note based on profile content.
- `待确认导师`: quality gate column. AI sets to `新加待check` when creating new records; cleared manually after human review. Records with `新加待check` are invisible to students.

### Main Columns (Template Format)

When the user provides a template (typically `博士选导出选模版.xlsx`), match its headers exactly. The standard template has:

- `美国学校`: US school name — fill ONLY for US schools.
- `非美国学校`: Non-US school name — fill ONLY for non-US schools.
- `QS排名`: fill for all schools.
- `美国学校的Usnews排名`: fill ONLY for US schools; leave empty for non-US schools.

**Row-level rules for template format:**
- Each row belongs to exactly ONE school type (US or non-US).
- For US schools: fill `美国学校` + `QS排名` + `美国学校的Usnews排名`. Leave `非美国学校` empty.
- For non-US schools: fill `非美国学校` + `QS排名`. Leave `美国学校` and `美国学校的Usnews排名` empty.
- Both school types coexist in the same sheet; one column pair is empty per row.

### Column Detection on Existing Workbooks

When opening an existing workbook:
- Read the header row to detect which format is in use.
- Match by column header name, not by position.
- Do not assume the simplified format if a template format is detected.

### ⚠️ Column Offset Detection (序号列陷阱)

When the Excel has an `序号` column in the header but the data rows have no actual sequence numbers (the column is empty in the body), all subsequent data shifts left by one position. **This is a common error when importing from sheets that have header-only ordinal columns.**

**Detection steps:**
1. Parse the header row and note column positions
2. Read the first 3-5 data rows
3. Check if the `序号` column has values in the data rows
4. If `序号` is empty in all data rows → data is offset: column N in data maps to column N+1 in header

**Example:**
```
Header: [优先级, 序号, 学校, 学院/系, 导师姓名, 职称, 研究方向, ...]
Data:   [P0,     空,   NUS,  商学院,    Xiuping Li, 副教授, Consumer..., ...]
                     ↑ 实际是"学校"列的数据，不是"序号"
```

**Correction mapping:**
```python
# Offset detected: skip col 2 (序号), map data col 2 → header col 3 (学校)
# data_idx 0 → header col 1 (优先级)
# data_idx 1 → header col 3 (学校, skip 序号)
# data_idx 2 → header col 4 (学院/系)
# data_idx 3 → header col 5 (导师姓名)
# etc.
```

After confirming the offset pattern, apply it to ALL rows. Print a warning to the user about the detected offset.

## Homepage Link Rules

The supervisor homepage link must be openable and must visibly correspond to the supervisor. Never invent, infer, or keep a profile URL just because it follows a plausible pattern.

Accept:

- Official profile page with name and title.
- Official team page listing the person with title/email/team identity.
- Official staff list page only if individual profile pages do not exist and the page clearly lists the person.

Reject or move to `待确认`:

- 404 pages, security pages, search result pages, dynamic shells with no visible name, stale guessed URLs.
- A link that opens but does not mention the target person.
- A general school homepage pretending to be a supervisor homepage.

If the first profile URL is 404, blocked, stale, or mismatched, search Google/Bing with `supervisor name + university + department/profile`. Use the found URL only after opening it and confirming the page content matches the person. If no confirmed page is found, do not fill the row as a main-table supervisor.

For dynamic pages, use the browser if needed. Confirm visible name, title, department, research interests, or email.

If a profile has no public email but has a contact button, message form, or official page that can send a message, the profile can still be used. Note the contact route only when relevant.

## Remarks

> 🔴 **本节曾与 `notes-and-fields.md` 冲突，2026-10-07 修正（张天钰批次返工）。**
> 旧版本节无条件允许「方向关联描述」（`和你的XX方向能搭上`/`有交叉`/`与XX方向比较对口`）。
> 实际规则是**有前提的**：只有**学生持有方向梳理**时才允许；**学生没有方向梳理（含"不知道会有什么方向"的学生）时一律禁止**，必须改为自包含写法。
> 子代理只读本节、没读 `notes-and-fields.md`，于是给「不知道方向」的学生批量写了"很对口/高度对口/方向一致/可关注"，被用户当场发现。
> **写备注前必须同时读 `notes-and-fields.md`，以那里为准。**

Write `备注` from profile content, not generic claims. Use short Chinese phrases:

`职称；研究方向（中文关键词）；风险/注意事项。`

无方向梳理时的**自包含**写法：只客观写「导师做什么方向 + 用什么方法 + 什么通道/招生信息」，学生不依赖任何外部文档就能看懂。

允许的结尾（**仅有方向梳理时**）：
1. **方向关联描述**：`和你的XX方向能搭上` / `和你的XX方向有交叉` / `与XX方向比较对口` —— ⚠️ 学生无方向梳理时**禁止使用**。用 `你`，不用 `学生`，且必须写出具体方向名。
2. **备选标识**：`可以备选一下呢～` / `可以往XX方向靠～` / `可以往后放一放～` / `作为备选看看～` / `可以放后面一点～`，且**同一句里必须先写清"偏在哪"**，不得单独出现。⚠️ 同样以"学生有方向梳理"为前提。

**无论何种情况都禁止的判定/关联套语**：`很对口` / `高度对口` / `比较对口` / `方向对口` / `能搭上` / `有交叉` / `方向一致` / `有交集` / `可对接` / `可衔接` / `可切入` / `可关注` / `很契合` / `高度契合` / `很匹配` / `高度相关` / `完美匹配` / `匹配度最高` / `匹配面最广` / `直接对话` / `很有交集` / `核心人选` / `建议多看看`。

#### ⚠️ 职称位只写「等级」，禁止写成「职称（学科）」（2026-10-07 用户指出后确立）

**教训**：UCL／港理工等校师资名录页的 title 是**复合式**——`Professor of Project Leadership and Innovation`、`Lecturer in BIM and Management`、`Associate Professor`。把它压缩成中文时，如果把 `of/in` 后面那半截用括号塞在等级后面（`教授（项目领导与创新）`），会出三个问题：

1. **读者误读**：以为职称是"项目领导与创新教授"，实际职称只是 `Professor`；
2. **与研究方向段重复**：`教授（项目领导与创新）；项目管理、项目领导力、创新管理。`——括号那半截基本是废话；
3. **混入异质内容**：同一位置还会塞进行政职务、甚至把英文职务 `Associate Head (Research)` / `(Teaching)` 截成「（研究）」「（教学）」这类**无信息量的解析错误**。

**规则**（写职称时逐条套）：

| 括号里的东西 | 正确写法 |
|---|---|
| 讲席／学科方向（`of X` / `in X`） | **并入第二段「研究方向」**，与已有内容去重后只留一份；职称位只写 `教授` / `副教授` / `讲师` |
| 行政职务（中心主任、学院院长、项目主任、研究生副主任） | 移到职称后：`教授兼学院院长；…` 或 `讲师，研究生副主任；…` |
| 职称存疑（名录页与个人页不一致） | 写到**句末**：`…；学院师资总表标注为 Associate Professor，职称以个人主页为准。` |
| 纯角色词（research / teaching / 研究 / 教学，来自 `Associate Head (Research)`） | **直接丢弃**，不要写进备注 |

**写后自检（正则）**：`^[^；（）]+（` 命中即不合格——备注开头到第一个分号之间不得出现括号。

**合法写法示例**：`教授兼学院院长；基础设施工程与国际发展、基础设施规划、城市与区域规划、环境工程。` / `副教授，研究生副主任；数字建造管理、BIM 与 GIS 集成、数字孪生数据建模。`

Allowed examples:

- `副教授；可持续供应链、产业协作、循环经济。`
- `教授；文物材料、科技考古、保护研究。`
- `研究助理教授；遗产研究、澳门史、离散社群；需确认带博。`
- `讲师；空间叙事、城市遗产、视觉文化。`
- `教授；环境风险、政策评估、气候金融；"research focuses on climate finance and policy evaluation"。`
- `Reader；胃肠癌政策评估、健康经济学；有监督经验但名额需确认。`
- （**仅当学生持有方向梳理时**）`副教授；做心血管药物流行病学，但也有老年用药安全的方向；和你的药流方向能搭上，可以备选一下呢～`

Avoid:

- `主页写明`, `公开资料`, `方向集中在`.
- `方向一优先`, `方向二备选`, `方向三优先`.
- Long explanations, copied profile blurbs, or unexplained English phrases when Chinese notes are requested.
- Emoji symbols (🔥👍⚠️✅ etc.) — never use in notes
- Direction book internal references (方向1/方向2/TOP/SECONDARY) — students don't know about the direction book
- Internal tool names (Vika/表格/源数据) in notes
- Correction records (职称修正/Vika写/已确认) in notes
- Machine-scoring labels (高度相关/很匹配/完美匹配/匹配度最高/匹配面最广/很契合/直接对话/很有交集/核心人选)

**关于「导师主页」列 vs 备注中的文章链接：**
- `导师主页` 列必须填学校官网的导师个人 URL（禁止 Google Scholar / ResearchGate / PubMed 等第三方平台）
- 当导师主页信息极少（没有展现文章）时，在备注中补偿文章链接：`文章看这里 https://scholar.google.com/...`

Use careful risk labels instead of hard rejection language when the student may still want to inspect the person:

- `需确认带博`: promising profile but supervision eligibility is not explicit.
- `教学岗风险`: teaching/instruction/practice title or page focus.
- `研究岗风险`: research-only or fellow/postdoc profile without admission evidence.
- `更新偏旧`: no recent publications/projects/updates for roughly 3+ years.
- `方向相关但不完全贴合`: adjacent topic worth student review.
- `无合适导师`: school-level note when the school was searched but no usable person was found.

### 当学校匹配导师极少时（1-2位）

当某个学校符合学生方向的导师极少（仅1-2位）时，在备注末尾补充说明该系其他教师的主要方向，让学生有"已全面搜索"的信心。

正确写法：
- `教授；决策神经科学、风险与社会决策；该系教师主要研究临床/辅导实践方向，仅有一位与消费者决策相关。`
- `副教授；消费者判断与决策；该系以社会认知与神经犯罪学为主，仅此一位与消费者行为相关。`

要点：
1. 客观描述："该系教师主要研究XX方向"——陈述事实，不做评判
2. 给出数量："仅有一位与目标方向相关"——让学生知道已全面查看
3. 禁止主观：不要写"没有合适的"、"确实没有"、"不匹配"等评价性语言
4. **补充信息行只需填 `导师` 和 `备注`**：另起一行单独写入系/院的补充说明时，只填写导师名（如"XX大学XX系补充说明"）和备注内容，无需填写导师主页、博士申请信息、其他导师信息等字段。

这个补充说明可以放在备注末尾，用分号与前面的内容分隔。

## Extra Sheets

Add these sheets for researched lists:

- `说明与颜色图例`: color meaning, link rules, and note rules.
- `排除或待确认`: people/schools excluded or needing manual confirmation, with reason.
- `学校初筛` or region-specific screening sheet when scanning all schools in a region.

Highlight search batches or newly added rounds with distinct pale row fills. The legend must explain the fill colors.

## Quality Checks

Before final delivery:

1. Verify all main-table supervisor homepage links match the person, not just status code.
2. Verify PhD application and staff/supervisor list links are official and non-empty.
3. Search the workbook for banned note phrases.
4. Scan for formula errors if the workbook contains formulas.
5. **For mixed US/non-US lists**: verify no row has both `美国学校` and `非美国学校` filled. Verify US News ranking is only filled for US schools.
6. Render every worksheet or key range and visually check column widths, wrapping, row colors, and clipped text.
7. Keep existing user files unchanged; save a new workbook unless the user explicitly asks to overwrite.

## Common Edge Cases

- If one university has a supervisor PDF plus separate profile pages, use the PDF/list as eligibility evidence and the profile as `导师主页`.
- If a profile has no email but has a contact button or message link, note that the homepage can send messages.
- If a candidate has several research links, choose the one closest to the student's topic for `导师主页` and keep broader lab/department links in `其他导师信息`.
- If a school has no suitable candidate, do not invent one; add a school-level note explaining the mismatch.
- If a profile has several links, inspect the most topic-specific link first. For example, a lab/project page may show stronger fit than the general staff page, while the staff page may be better for identity verification.
- If a person appears relevant but outside the student's keywords, use a neutral note that invites review, such as `方向相关，可让学生判断兴趣`.
- If a candidate is likely unsuitable only because of title or supervision uncertainty, keep them out of the main table unless the user asked for borderline options.
- **When filling a template with mixed US/non-US schools**: sort rows so US schools are grouped together, non-US schools grouped together. This makes the empty cells less visually jarring.
- **When all schools are non-US in a template**: the `美国学校` and `美国学校的Usnews排名` columns remain in the header but all rows have them empty. This is correct behavior.

## 国内学校表格规则 (Domestic China School Column Rules)

国内（中国大陆）学校的导师记录在填写表格时，需额外遵守以下规则：

### 导师联系方式（必填）

`导师联系方式` 列为国内学校导师必填项。必须填入导师的 email 地址。

获取优先顺序：
1. 导师个人主页（标题栏/联系信息/页面底部）
2. 院系师资列表页
3. 百度学者、ResearchGate、学术论文通讯作者邮箱等其他来源

若通过非主页来源获取邮箱，须在备注中标注来源（如"邮箱来自百度学者"）。

### 导师主页（国内来源要求）

`导师主页` 必须使用 `.edu.cn` 域名的官方导师个人页面 URL。

若主页信息过少（仅有姓名+职称，无方向/论文/项目），：
- URL 仍填入 `导师主页` 列
- 备注中补充百度学者、百度百科、外部文章等链接

### 备注补充链接格式

备注中补充的外部链接需使用完整 URL，放在备注末尾，用分号与前文分隔：

```
教授；自然语言处理、知识图谱；百度学者 https://xueshu.baidu.com/...
```

---

> 📎 自 SKILL.md 迁入（2026-10-07）。

## Excel 模式（可选）

当用户上传 `.xlsx` 文件而非 Vika 链接时，使用 Excel 模式。详见 `references/spreadsheet-rules.md`（列格式选择、列偏移检测、备注规则、质量检查）。

**默认输出列**：`导师`, `Location`, `学校名字`, `QS排名`, `美国USNEWS排名`, `Department`, `导师主页`, `导师联系方式`, `博士申请信息`, `其他导师信息`, `备注`

- `美国USNEWS排名`：仅当列表中有美国学校时包含此列
- `导师联系方式`：**国内学校必填**（导师 email），海外学校选填

---
