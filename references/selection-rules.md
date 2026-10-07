<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：导师合格性筛选规则：证据优先级、筛选轮次、地区职称口径、通常排除项、方向匹配判据（术语重合 ≠ 方向匹配）、备注证据要求、方向均衡复核、学校级筛查、国内学校选导四条规则
> **什么时候读**：判断某位导师是否合格、或为整张表确定筛选口径时；用户要求「某方向全排除」时
> **什么时候不用读**：只改链接、字段格式或语言要求时；写备注文字本身（转 notes-and-fields.md）

---

# Supervisor Selection Rules

## Evidence Priority

Use the strongest available evidence, in this order:

1. The PhD program publishes an eligible supervisor list; only choose names from that list.
2. The profile says the person supervises PhD/research students or is accepting doctoral students.
3. The profile has a `supervision`, `students`, `graduate supervision`, or similar section.
4. The CV/profile lists current or former PhD students.
5. The biography mentions PhD supervision, doctoral committees, or current/past doctoral students.
6. The title and employment type imply possible PhD supervision, with regional caution below.

If evidence is weak but the person is otherwise promising, move them to `排除或待确认` or mark the exact risk in `备注`.

## Selection Rounds

Use a staged judgement when explicit evidence is not available:

1. First pass: select only names from an official PhD supervisor list or profiles that clearly say the person can supervise PhD/research students.
2. Second pass: if no official list exists, prioritize people with a `supervision` section, supervised-student history, or biography evidence of doctoral supervision.
3. Third pass: only when the list is still thin, use title and region heuristics. In this pass, mark uncertainty plainly in `备注` or put the person in `排除或待确认`.

If several profiles in the same school share a pattern, use that pattern. For example, when only profiles with `available to supervise PhD students` appear among otherwise similar staff, select the marked profiles first.

## Region and Title Heuristics

When there is no explicit supervision evidence:

- United States, Hong Kong, Macau, and Europe except the UK/Ireland: normally require `Assistant Professor` or above. Do not select plain `Lecturer`.
- Singapore: normally require `Assistant Professor` or above unless a profile explicitly states doctoral supervision.
- UK and Ireland: `Lecturer` and `Senior Lecturer` may be acceptable when the school uses the UK system, but add a note if supervision eligibility is not explicit.
- Australia and New Zealand: `Lecturer` and `Senior Lecturer` may supervise in some universities. Check whether the profile or research degree page says they can supervise or are available for supervision.
- Other regions: `Lecturer` or above may be acceptable if the profile is research-active and the program allows it.
- Research fellow, research assistant professor, postdoc, or equivalent: include only if the profile or PhD page clearly indicates supervision/admission eligibility.

When only a title is visible and no other supervision evidence is available:

- United States, Hong Kong, Macau, and most of continental Europe: do not select `Lecturer`.
- Singapore: normally do not select `Lecturer`.
- UK and Ireland: `Lecturer` and `Senior Lecturer` can be considered, but note `需确认带博` when the page does not say it directly.
- Australia and New Zealand: `Lecturer` and `Senior Lecturer` can be considered only with supporting evidence or when no better match exists; note the supervision risk.
- For old UK-system titles used outside the UK, judge by the institution's actual rule and profile evidence rather than the title word alone.

## Usually Acceptable Titles

`Chair Professor`, `Professor`, `Associate Professor`, `Assistant Professor`, `Reader`, and equivalent full-time research/teaching-and-research faculty titles.

`Distinguished Professor` and `Honorary Professor` can be included only if the page also supports current supervision or the fit is exceptional.

## Usually Exclude

Exclude from the main table unless strong contrary evidence exists:

- `Adjunct Professor`, `Visiting Professor`, `Emeritus Professor`. **Do not include emeritus/retired professors. Delete them immediately if found.**
- `Teaching Professor`, `Professor of Instruction`, `Professor of Practice`, `Industry Professor`.
- `Clinical Professor`, `Practical Professor`, studio/practice-only faculty.
- Research-only staff, postdocs, fellows, and lab staff without doctoral supervision evidence.
- Very junior profiles with only 1-3 papers and no other research evidence.
- **Age/heavily senior profiles**: anyone clearly over ~70 or whose career timeline suggests full retirement. Do not include; delete if already in table.
- Inactive profiles: no recent publications, projects, or updates for roughly 3+ years, especially for senior scholars.
- Profiles where the person looks mainly teaching, instruction, industry practice, or professional-service oriented rather than research active.
- People whose title or page suggests they cannot independently supervise doctoral students, unless the PhD page explicitly says they can.
- Obvious mismatch with the student's hard exclusions.

## 🔴 学生可执行性（Doability）—— 收人前必过的第一道闸（2026-10-07 用户指出后确立）

**教训**：学生是「工程管理 + 项目管理」背景（无科研经历），我按"**院系属于建成环境**"取人，把 UCL 的 IEDE（建筑物理与环境设计）、Energy Institute（建筑物理/城市能源建模）和港理工的 BEEE（建筑环境与能源工程）整块拉了进来，一口气写了 195 条。用户直接质问："副教授；零能耗建筑、可再生能源系统、建筑储能、暖通……**这种建筑方向的他能做？**"——不能。这些课题的研究对象是建筑设备与物理过程，方法是工程实验 + 热工/流体数值模拟，与该生背景完全不搭。最终删掉 96 条，195 → 75。

**根因**：用**院系归属**代替了**学生可执行性**。同一个学院里可能同时存在"学生做得动"和"完全做不动"两类导师，必须逐人看研究对象与方法，而不是看院系名字。

**规则**：判断"相关"时加一道闸，**研究对象**优先级最高：

| 学生背景 | 能做（研究对象 = 工程/项目/资产本身） | 做不了（研究对象 = 设备/构件/材料/物理过程/地球空间） |
|---|---|---|
| 工程管理 / 项目管理 | 建设项目与项目管理、组织与治理、重大工程与基建交付、数字建造（BIM/数字孪生/AI 应用）、设施与建成资产管理、采购与供应链、建设法规与合约、建设产业组织、可持续建造的**管理与政策**侧、城市开发与更新管理、基建规划与经济评价 | 暖通空调、建筑储能、可再生能源系统、零能耗建筑、围护结构传热、建筑能耗模拟、建筑物理、照明、声学、室内空气品质、火灾动力学/结构抗火、建筑材料、结构/岩土/流体、环境工程（水/气/废物技术）、遥感/GNSS/InSAR/地理信息、纯 AI/GIS 方法 |

**自检动作**：写完表后随机抽 10 条，问自己"**这个课题学生从本科硕士背景出发能做什么具体贡献？**"——答不上来的就是错收。

**大型/宽口径任务的正确做法**：铺开阶段就**按"可执行方向"分档**，而不是按院系铺。交付时把"核心区（直接可做）"与"相邻区（需迁移）"分开标注，让用户一眼看清哪些是真正能落地的。

**⚠️ 提示词写"可能相关的老师都选了给他看看"时，不等于"整个学院都拉进来"**：仍须套用本闸门。「都不知道方向」的学生需要的恰恰是**可执行的方向清单**，不是院系花名册。

## Fit Judgement

Fit can be strong even when keywords are indirect, if the supervisor's research methods, objects, or field can support the student's project.

### ⚠️ 术语重合 ≠ 方向匹配：必须读「博导声明里的范围限缩」（2026-09-18 用户指出后确立）

**教训**：曾把一位医学人类学者选进舞蹈方向学生的表里，理由是她的简介里出现 "phenomenological experiences, conceptions and theories of the body, labour and embodiment"——但那只是**理论词汇重合**：她的研究对象是南亚（印度）的癌症与疼痛医疗化，田野点在癌症医院。学生四份 RP 无一与医学、疾病或南亚相关。用户一眼看出问题并要求删除。

**根因**：从「理论术语」而不是「研究对象 + 博导声明的适用范围」判断匹配。

**规则**：
1. **研究对象（研究谁/研究什么）优先级高于理论术语**。理论框架相同（都用现象学、都用具身理论、都用民族志）不足以构成可指导关系。
2. **必须读主页博导声明的原文，识别是否含范围限缩**。常见限缩句式：
   - `happy to supervise PhD projects ... related to my geographical and conceptual areas of expertise`
   - `interested to supervise PhD students in the following areas: A; B; C`
   - `welcomes PhD enquiries from candidates wishing to pursue projects in the above subject areas`
3. 命中限缩句式时，**逐项把声明里的领域与学生的题目对照**：
   - 反例（应删）：声明 = "我的地理与概念专长领域"，而地理 = 南亚、概念 = 医学人类学；学生题目 = 竞技国标舞 → 不覆盖 → 不进主表
   - 正例（保留）：声明含 `diaspora`，学生题目含华裔离散 → 覆盖
   - 正例（保留）：声明含 `Arts-based and post-qualitative educational research`，学生题目含创意舞蹈教育 → 覆盖
4. 备注里**不得用理论词汇重合替代匹配结论**。若只是方法/理论层面沾边而对象不同，须写明对象差异（如"研究的是南亚癌症与疼痛的医学人类学，与你的题目在研究对象上不同"），不能一律以"和你的XX方向能搭上"收尾。

**自检手法**（批量写完必做）：扫一遍所有主页，正则抓取博导声明句
`(?:happy|welcome|welcomes|interested|keen)[^.]{0,90}(?:supervis|PhD|doctoral)[^.]{0,180}\.`
逐条核对是否限缩、限缩项是否覆盖学生方向。

**When to use `可以备选一下呢～` / `可以往XX方向靠～`** (only when both conditions are met):
- Bottom line: supervisor's research does NOT touch anything the student absolutely won't consider
- Trigger: research partially matches the student's direction but also diverges, worth letting the student consider

Direction-fit phrases (`和你的XX方向能搭上`/`有交叉`/`比较对口`) are also allowed as objective overlap descriptions — use `你`, not `学生`. They can be used alone or combined with the backup marker.

Correct usage:
- `教授；做心血管药物流行病学，但也有老年用药安全的研究方向；和你的药流方向能搭上，可以备选一下呢～`
- `副教授；做药物经济学和卫生技术评估，也有糖尿病慢病管理方向；可以往慢病预测模型方向靠～`

**Never use verdict labels** like `建议多看看`、`比较匹配`、`高度相关`、`很匹配`、`完美匹配`、`匹配度最高`、`匹配面最广`、`很契合`、`直接对话`、`很有交集`、`核心人选` — these are forbidden machine-scoring language. The remark should contain title, research direction, and optionally a direction-fit phrase or backup marker when the trigger condition is met. Let the student judge fit from the research description.

Do not overfit by title alone. Check publications, projects, current research, supervised students, and program requirements where possible.

### ⚠️ 用户要求「某方向全排除」时：**禁止用关键词机械匹配**（2026-10-07 实测）

**场景**：写完表后用户说「XX 相关的全排除」（如"金融经济相关的全排除"）。

**踩过的坑**：先用正则扫 `职称 + 导师研究领域` 里的 `financ|econom|investment|valuation|banking…`，命中 40 条——但其中大半是**误报**。

**根因**：UCL `profiles.ucl.ac.uk` 个人页会附一段官方的 **`FIELDS OF RESEARCH` 分类标签**，`Banking, finance and investment`、`Applied economics` 是很常见的通用标签，会大面积误伤：
- Mike Raco（城市治理）、John Tomaney（区域规划）、Jung Won Sonn（经济地理）、Dabo Guan、Kell Jones（建设采购）、Julia Stegemann（环境工程）等都被这条标签带出；
- 反过来，**只扫英文会漏**：`Climate finance`、`Real estate economics` 常常只出现在**中文备注**或 `positions` 里（如 Xi Liang 的"气候金融、碳市场"、Roberto Cardinale 的"基建项目管理与金融"）。

**正确做法（三步，别省第二步）**：
1. **双通道召回**：英文正则扫 `职称 + 研究领域`，**同时**用中文正则扫 `备注 + 职称`（`金融|经济|投资|地产|估值|财政|财务|资本|融资|信贷|银行`）。两条并集才是候选池。
2. **逐条读研究领域正文再定夺**——判据收紧为「**职称或研究领域核心落在该方向上**」。只做交叉学科应用的（如 AI 用于房地产、资产管理里的全生命周期成本）不排除。
3. **把边界情形单独列给用户裁定**，不要自己默默留或默默删。报告里分三块：① 已剔除（含理由）② 边界保留（含理由）③ 校验结果。

**删除前后必做**：删除后**回读全表**核对条数与"被剔姓名 0 残留"；本地 payload/预览页同步删掉同批记录，并断言 `线上集合 == 本地集合`（差集须为空）。删记录不丢数据——`payload.json` 里留着完整字段，随时可重新导入，报告里可以这样告知用户以降低其顾虑。

## Remarks Evidence

Prefer remarks grounded in one of these evidence types:

- Direct keyword overlap with the student's direction, such as field terms, methods, materials, regions, populations, or theoretical frames.
- The supervisor's publications, projects, biography, grants, or supervised students match the student's topic even when the profile keywords are broader.
- Adjacent but potentially useful fit that should be shown to the student for judgement, such as related management, media, heritage, environment, health, finance, spatial, or cross-cultural work.
- Direction fit is good but supervision status is uncertain; say so briefly instead of overstating eligibility.

When writing a positive note, include the reason, not just a verdict. When the fit is only adjacent, use language like `可让学生判断兴趣`, `方向相关但不完全贴合`, or a short domain-specific risk.

## Direction Balance Review (审查已有导师表时必做)

当用户要求"审查现有导师的匹配度"或"重新选一下"时，不仅要逐条判断匹配度，还必须检查**整张表的方向分布是否与学生的实际工作方向一致**。

### 步骤

1. **明确学生的核心工作方向**：从备注、对话上下文、学生背景中提取。注意区分"学生感兴趣的多个方向"和"学生当前实际在做的主要方向"。
2. **逐条分类现有导师**：按方向归为三类：
   - **A 类 — 强匹配**：直接属于学生当前主要工作方向的院系/研究领域
   - **B 类 — 有交叉**：研究方向与学生工作方向有方法学或应用层面的交叉
   - **C 类 — 偏离**：研究方向与学生当前工作方向基本无关
3. **统计分布**：如果 C 类占比超过 40%，或 A 类占比低于 30%，向用户报告方向失衡问题
4. **提出方案**：建议删除 C 类，补充 A 类方向的新导师，使 A 类占比达到 50% 以上

### 注意事项

- 学生的"兴趣方向"和"实际工作方向"可能不同。以**实际工作方向**为主轴判断匹配度
- 同一个学生可能有多个方向，需要确认哪个是当前主要工作
- 不要只看导师所在系名，要看具体研究内容（同系不同方向的导师匹配度可能差很大）

## School-Level Screening

If a school is in the user's list but no suitable person is found, record it in a screening sheet with a specific reason. This is mandatory for user-specified school scopes: every searched school with no suitable supervisor must be logged in `学校初筛` or `排除或待确认` with the school name, search status, and concrete reason.

- No relevant department or PhD route found.
- Relevant department exists but all profiles are practice/teaching/technical-heavy rather than research-active.
- Staff page is dynamic or blocked and no individual page can be verified.
- The PhD route lacks funding or does not admit research students.
- No supervisor list, but other staff links may deserve a future manual pass.
- A relevant person exists but has no clear PhD supervision evidence, stale publications, or a title that is risky in that region.
- The school has a relevant PhD program, but the available staff are only loosely related to the student's direction.

Keep these notes factual and brief.

## 国内学校选导规则 (Domestic China School Rules)

以下规则适用于中国大陆高校的博士导师筛选。与海外学校共同存在时，国内学校走这套逻辑，海外学校走原有通用逻辑。

### 规则一：招生目录优先

首先查看目标学校/学院官网是否已发布**2027年博士研究生招生简章及招生目录**。

- **已公布 2027 招生目录**：仅可选择招生目录中列出的导师。目录以外任何导师（无论名气大小）均不可选。
- **未公布 2027 招生目录**：进入规则二的招生可能性判断。
- 2027 招生目录 vs 2026/2025 招生目录：如果 2027 未出但 2026 已出，不可直接用 2026 替代——进入规则二。但可将 2026 目录中连续多年出现的导师标记为"往年连续招生"作为辅助参考。

搜索招生目录时，优先搜索：
- `[学校名] 2027年博士研究生招生专业目录`
- `[学校名] [院系名] 2027年博士招生`
- `[学校名] 研究生院 2027年博士招生简章`

### 规则二：招生可能性分类（A/B/C 三级）

当 2027 招生目录未公布时，根据导师的招生稳定性分为三级：

**A 级 — 稳定招生。直接选择。**
- 学术大牛，有在研国家级重大/重点项目（如国自然重点、973/863、国家重点研发计划等）
- 历年几乎每年都在招生目录上，招生记录连续
- 判断依据：个人主页/实验室页面显示在研项目、近两年有博士招生公告、往年招生目录连续出现
- 备注可标注"往年连续招生"或"有在研重大项目"

**B 级 — 间接招生。可以选择。**
- 普通教授/副教授，每 1-2 年招一次博士生
- 有在研项目但非重大项目，近三年有博士招生记录
- 判断依据：个人主页显示在研课题、近三年招生目录中有出现但不连续
- 备注可标注招生频率（如"近三年招生 2 次"）

**C 级 — 波动招生。不选择（除非有特殊推荐理由并注明）。**
- 年纪过大（约 60 岁以上且近两年无博士生招生记录）
- 即使是大牛，但已多年（3 年以上）未出现在招生目录中
- 更偏向行政事务（如院长/副校长/党委书记等）而非一线教学研究，近三年无博士生指导记录
- 判断依据：个人主页多年未更新、近三年招生目录未出现、以行政头衔为主

C 级如确有特殊推荐理由（如方向极度契合且该方向无其他导师可选），可保留但必须在备注开头明确标注 `C级波动招生，特殊推荐理由：XXX`。

### 规则三：导师联系方式（邮箱必填）

国内学校的每一位导师，必须将 **email** 填入 `导师联系方式` 列。

- 优先从导师个人主页获取（标题栏、联系信息区、页面底部）
- 若无主页或主页无邮箱，从院系师资列表页获取
- 若以上均无，通过百度学者、ResearchGate、学术论文通讯作者邮箱等其他来源查找——并在备注中标注邮箱来源
- 禁止在该列填写非邮箱内容（如网址、电话等）

### 规则四：导师主页要求

国内学校导师的 `导师主页` 必须使用**国内官网学校的导师个人主页 URL**。

- **URL 必须是完整的原始链接**（`https://` 开头），**禁止**使用重命名的纯文本占位符（如"XXX个人主页""暂未找到"等）。即使暂时找不到，也必须填入一个有效的 URL 或留空后标注，不允许用文本替代 URL
- 优先使用学校官网的教师个人页面（通常包含研究方向、论文、项目等）
- 若无个人主页，或主页信息过少（仅含姓名+职称，无研究方向/论文/项目等实质性内容），则该主页 URL 仍填入 `导师主页` 列
- 同时必须在备注中补充其他效度较高的专业平台链接：
  - 百度学者（百度学术）个人页面
  - 百度百科词条
  - 外部文章/采访链接（含有导师研究方向说明的新闻稿、学术报道等）
  - 论文作者页面（如知网作者页、万方学者页等）
- **佐证规则**：若通过并行搜索多个页面（如百度学者+论文+新闻）推论出导师研究方向符合学生方向，而该信息在导师主页上无法看到，则必须将对应的外部链接放在备注中作为佐证

备注中的补充信息格式示例：
- `教授；自然语言处理、知识图谱、大模型应用；主页信息较少，百度学者页 https://xueshu.baidu.com/... 显示主要方向为 NLP。`
- `副教授；文化遗产保护、建筑史；无个人主页，百度百科 https://baike.baidu.com/... 显示研究方向为古建筑保护。`

### 国内学校搜索优先级

1. 首先搜索学校官网（`.edu.cn` 域名）的招生目录和导师页面
2. 若官网无法访问或无相关信息，使用百度搜索 `[导师名] [学校名] 教授` 或 `[导师名] [学校名] 博士导师`
3. 辅助来源：百度学者、百度百科、知网、万方、学校研究生院公告
