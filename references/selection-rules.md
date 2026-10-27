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

## 🔴 地区默认排除：提到「欧洲」时一律不看挪威、瑞典、葡萄牙（2026-10-23 定调，2026-10-27 增补葡萄牙，焊死）

**用户原话**：

- 2026-10-23：「提到欧洲的时候除非是特意说明，绝对不看挪威和瑞典。」
- 2026-10-27：「现在加上葡萄牙。」

**默认排除名单**（范围词命中「欧洲」时，以下国家整体剔除）：

| 国家 | 英文 | 加入日期 |
|---|---|---|
| 挪威 | Norway | 2026-10-23 |
| 瑞典 | Sweden | 2026-10-23 |
| 葡萄牙 | Portugal | 2026-10-27 |

> 📌 **名单是可增补的**：用户后续说「再加上 X」时，直接在表里加一行，并同步改本节标题、三个执行口径里的国名、以及 `rules-write.md` / `search-phase.md` / `SKILL.md` 里的索引行。

**规则**：用户（或方向书）给出的范围词里出现「欧洲」时，**上表中的国家一律整体排除**——不搜索、不写入、不进候选池、不计入「覆盖 N 人」的基数。

**触发本条的范围词**（命中任一即生效，不限于这些写法）：

- 中文：欧洲、欧陆、欧洲大陆、欧洲其他地区、北欧、欧盟
- 英文：Europe、continental Europe、EU、Nordic、Scandinavia

> `北欧` / `Nordic` / `Scandinavia` 同样排除——这些词本来就包含挪威与瑞典，不存在「北欧不等于挪瑞」的解释空间。

**仅有的纳入条件**：用户**当次明确点名**名单内国家的具体学校 / 具体导师，或明确说「挪威瑞典也可以」「葡萄牙也可以」「含北欧」。方向书里若原文点出该国具体学校，视为已点名；只写「欧洲」「北欧」不算。

**未列入本条的欧洲国家照常处理**：英国、爱尔兰、德国、荷兰、丹麦、芬兰、瑞士、奥地利、法国、意大利、西班牙、比利时等仍按用户给的排名带与方向要求正常搜索（本 skill 里英国/爱尔兰通常与「欧洲」并列提及，本条不波及）。

**三个阶段的执行口径**：

| 阶段 | 动作 |
|---|---|
| 搜索 | 列候选校时直接剔除**挪威 / 瑞典 / 葡萄牙**全部学校，不派子代理、不抓取 |
| 写入 | 发现名单内国家的导师一律**不写入**；已在表里的历史记录不属本条范围，但要在交付报告里单独列出并问用户是否处理 |
| 审核 | 表内出现名单内国家的记录且用户从未点名 → 标为「范围外（默认排除）」并在报告里点出，不要静默放过也不要自作主张删除 |

**不确定时问用户**，不要自己推断「这次应该可以」。本条与用户其他地区要求叠加时，**以更严格的为准**。

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

### 🔴 闸门二：跨学科先修背景（2026-10-07 用户第二次追问后补上）

**教训**：把上面那道闸门只理解成"排除设备/材料/物理"，仍会漏掉一整类错收——**需要另一门学科系统训练的方向**。用户紧接着追问："工程管理+项目管理背景，你确定可以做**城市治理**？他不是城规背景。"——不能。城市治理／空间规划是城市规划与公共政策学科的核心领地，需要规划理论、城市制度、政策分析训练；学生没有这个底子，RP 与套磁都会立不住。

**规则**：除了"研究对象对不对"，还要问"**方法需不需要另一门学科的先修训练**"。学生只带得动**管理／组织／经济／运营／数据**这一套方法。命中下面任一条即剔除：

| 方向 | 需要的学科先修 | 处理 |
|---|---|---|
| 城市治理、空间规划、城市与区域规划、城市设计、城市形态 | 城市规划 / 公共政策 | 剔除 |
| 建筑遗产保护、建筑设计、建筑史、遗产更新 | 建筑学 / 建筑史 | 剔除 |
| 工程与公共政策、城市创新、科技政策 | 公共政策 / 社会科学 | 剔除 |
| 城市研究、住房政策、社会工作取向的建成环境研究 | 社会科学 | 剔除 |
| 建筑物理、建筑设备、材料、结构、环境工程、地理信息 | 工科实验 / 模拟 / 测绘 | 剔除（闸门一） |
| 金融、经济、投融资、房地产金融与估值 | 经济学 / 金融学 | 剔除（用户常单独要求） |

**边界判断示例（工程管理/项目管理学生）**：
- ✅ 保留：基础设施**资产管理**（研究对象是资产与运维）、基建**项目**管理与交付、系统安全与**重大基建项目管理**、建设产业 LCA、**创新管理与多准则决策**、战略**设施管理**／使用后评价／工作场所管理。
- ❌ 剔除：**城市**治理与开发、城市与区域规划、建筑遗产保护与管理、工程与**公共政策**、城市创新；即使这些人挂在建设类院系（如港理工 CMI 里的城市治理／城市规化／城市设计方向）也要剔。

**关键提醒**：**不要因为某人在"对"的院系就放过他**。实测港理工 CMI（建设管理及智能学系）20 人里有 5 人（城市治理、建筑遗产保护与城市规划、城市化与地方治理、都市空间结构与土地利用、可持续规划设计）是城规/建筑方向，必须单独拎出来剔。**院系正确 ≠ 个人可带**。

**三轮收敛实测记录（工程管理+项目管理学生，UCL+港理工）**：195 → 75（剔金融经济 24 + 建筑技术/土木环境 96）→ **59**（再剔城规/建筑/政策 16）。**教训是：宁可一开始就按闸门收，也不要先铺 195 条再删三轮。**

### 🔴 闸门三：**博士项目的学位学科**也必须对口（2026-10-07 用户第三次追问后补上）

**教训**：用户接着问「确认项目都是相关学科下的小方向了吗？」——查下来 58 条挂在 **5 个博士项目**上，其中 6 条的**学位学科根本不是建设管理**：
- UCL CEGE 的 `Civil, Environmental and Geomatic Engineering MPhil/PhD`（3 条）——项目页所列学科是环境工程、结构、测绘、交通、基础设施、材料、岩土、流体，**学位是土木类**；
- PolyU CEE 的 RPg（2 条）——土木及环境工程；
- PolyU BEEE 的 RPg（1 条）——**建筑环境与能源工程**，正是上一轮整块剔除的学科。

这些人的**个人方向**（基建资产管理、基建系统分析、重大基建项目管理、建设产业 LCA、设施管理）看着对口，但学生读出来是**土木/建环的学位**，与「建设管理」不是同一学科。**只看导师个人方向不看项目的学位学科，是漏网最快的一类错收。**

**规则**：交付前必须对**「博士申请信息」这一列去重**，逐个回答「这个博士项目**授予什么学科的学位**」：

1. 用 `{博士申请信息}` 值做分组去重（实战：58 条 → 5 个 URL，一眼看出问题）。
2. 逐个打开项目页，读它的**学科归属**（项目名 + 学院/系名 + 项目页列的 disciplines），不要只看导师所属院系。
3. 判据：**学位学科 ⊆ 学生目标学科**才算 A 类（如 BSSC 的 `Sustainable Construction MPhil/PhD`、PolyU CMI 的 RPg）；学位学科属于其他一级学科（土木、建环、能源、规划）的，即使用人做的是该学科下的管理小方向，也要单独列出交给用户裁定，不要静默保留。
4. 同一份表里**只应出现学生目标学科的项目 URL**；若出现第三、第四个 URL，几乎一定有跨学科混入。

**另一类要单独报的：「学位学科对口，但小方向偏离主干」**——如医疗建筑与规划、建成环境社会科学、桥梁结构与工程韧性、增材制造与先进材料、法经济学与行业监管、基础设施与发展研究。这类不算错收，但要在报告里明确列为「内容边缘」交用户裁定，不要和核心人选混在一起。

**四轮收敛实测记录（同上学生）**：195 → 75 → 59 → **46**（再剔跨学科项目 + 小方向偏离共 12 条）。最终只剩 **2 个单位 / 2 个博士项目**：UCL BSSC 32 + PolyU CMI 14。

### 补「缺口方向」时的正确做法（2026-10-07 沉淀）

用户看完方向分布后说「XX 方向、YY 方向的补个别老师看看」时，**不要为凑方向而跨院系拉人**，否则立刻违反前面三道闸门。固定动作：

1. **先在已锁定的目标院系内翻**（本例：UCL BSSC 与 PolyU CMI 的完整师资名单，包括之前因各种口径剔掉的人）。缺口方向的对口人往往正是上一轮被剔的那几位——他们的**学位学科本来就对口**，只是当时被别的口径挡掉。
2. **回补即说明**：报告里必须写清「这个人此前因何被剔、现在为何回补」，不要静默复活。
3. **确实凑不出人的方向，如实报 0**，不要用相邻方向硬顶。本例实测：房地产与土地开发管理、建设法与合同争议管理、建筑产业政策与监管、建设教育与培训这四项，在两校建设管理学院内确无在职对口导师；其中「房地产」的正牌人选都在商学院式的地产金融组（属用户排除口径）。
4. **补完照常跑完整校验**：八列空值扫描 + 学校关联 + QS/Location 自动回填 + 本地/线上集合一致性 + 预览页重生成。
5. 补录记录同样置 `待确认导师 = 新加待check`。

**本轮实测**：46 → 53（循环建造 3：Bao／Josa／Rose；既有建筑改造与运维 2：Morhayim／Esther YUNG；房地产与土地 2：Ivy WONG／HOU Yuting），补齐了 2 个方向，另 3 个方向如实报 0。

### 🔵 用户说「有项目的学校可以尽可能多选一点，没有特别对口的，相关的供应链管理等也可以」（2026-10-12 孙雨璐美国加州轮沉淀）

这是**放宽「方向主题」口径**的指令——**只放宽主题，不放宽职级 / 链接四关 / 学位学科 / 目标学年**。固定动作：

1. **先划出「有项目的学校」**：只有存在**目标学年可申请对口博士项目**的学校才扩选；本校该学年不招（或根本没有研究型博士）的一律不扩，避免把无法投递的人塞进表。
2. **把对口院系的在职正式教职全量过一遍**，逐人读官网 `Areas of Expertise` / `Research Areas` / `Research Interests` **原文**，按下表判定：
   - 出现 `Supply Chain` / `Logistics` / `Freight` / `Inventory` / `Sustainable Operations` / `Circular` / `Business of Sustainability` / `Environmental` → **纳入**（供应链或绿色档）
   - 出现 `Operations Management` / `Service Operations` → **纳入相邻档**
   - 只有方法学描述（learning theory、provable algorithms、causal inference 等方法本身），无对象词 → **不纳入**
3. **分三档写入交付报告**（A 绿色·可持续 / B 供应链·运营管理 / C 相邻），**不要平铺成一张名单**——用户下一步是按档挑人。
   ⚠️ **注意**：本档划分只进交付报告，**不得写进表内备注**（备注禁用方向偏向与评价语）。
4. **备注必须照实写出每个人的「落点」与方法**，例：`副教授；运营管理与市场设计研究，落点为数字平台、电子商务与公共资源配置，方法含优化、博弈论与数据分析。` 不写落点就会出现「看着对口、实际落点在医疗运营 / 电力市场 / 广告投放」的整批失真。落点措辞**只能取自官网原文**，不得自行归纳。
5. **仍受闸门一约束**：研究对象是**材料、构件、车辆技术**的（建材 LCA、路面工程、电动车采用）即使挂在同一个系也不收。
6. **扩选后照常过独立对抗审核**：扩选批次最容易在「方向相关性」上失分，审核官通常把「仅挂靠运营管理大类」的人判 C 级。此时**保留记录并补写落点**优于直接删除——用户要的是「多选一点」，不是再筛一轮。

**本轮实测**：红框 10 校 → 首版 8 条；放宽口径后补 17 条 → **25 条**（USC 9 / UCI 5 / UCSD 4 / UCSB 4 / UCD 3），A 档 11 + B 档 8 + C 档 6；5 校因无对口 2027 博士项目如实报 0。


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

### ⚠️ 用户在写完后追问「这些人能不能用现有 RP 改 SOP 套」时：出**三档可用性分级**（2026-10-09 确立）

**场景**：表写完、单条字段也核过之后，用户会问一句「这些导师都能用现在的 RP 改成 SOP 去套吗？方向对吗？」。这问的不是「字段对不对」，而是**「这批人里有多少人真的能被这个学生的题打动」**。

**必须先固定的锚点**：把学生的每份 RP 提炼成 **1 个「研究域 + 机制 + 方法」三元组**，再拿它去比导师的方向。以心理学×消费/JDM 学生为例，锚点为：消费者行为 · 判断与决策（JDM）· 态度与说服 · 情绪与决策 · 亲环境行为 · AI×人类决策。**不要**用「心理学」「社会科学」这类过宽标签，否则满表都"对口"。

**三档定义（按「RP 改写量」而不是按"兴趣相似度"分）**：

| 档 | 判据 | 交付口径 |
|---|---|---|
| **A 核心对口** | 导师方向本身落在上述研究域内 → 现有 RP 稍作改写即可当 SOP | 可直接排套磁 |
| **B 部分相关** | 只共享机制词或邻近域，研究域不同（如「情绪调节」vs「情绪与消费决策」；「健康行为维持」vs「消费者粘性」） | 必须重写 SOP 落点，命中率低于 A，需向用户明说 |
| **C 不对口** | 落在另一个子学科：职业健康/职业压力、工业组织（领导力、组织气候、员工发声）、临床与法证、基础认知（记忆注意）、发展心理、种族群际、计算机学院的 HCI/AI | 不建议用现有 RP 套；报告里给出「整校移出」建议 |

**三条硬规矩**：
1. **A 档要再按「主打哪份 RP」二次分组**，逐人标明 `R1/R2/R3`——用户下一步就是按 RP 分批发信，分组错了等于没分。
2. **同校要分别判**：商学院营销组往往全是 A，同院组织行为（OB/HR）组往往全是 C。**不要按学校一刀切**（典型：Buffalo 管理学院 12 人里 6 人 A、6 人 C；UCF 8 人全 C）。
3. **C 档不能默默留着**：每校列出「C 档占满全域 → 建议整校移出」，并给一句理由；边界情形单列给用户裁定（同「禁止机械匹配」一节的第 3 步）。

**产出**：HTML（三档明细表 + 「三份 RP 各对应哪一批人」）+ CSV（列：档位 / 学校 / 排名 / 导师 / 建议主打 RP / 判据 / 官方备注原文 / recordId）。**判据列必须能回溯到官网备注原文**，不能只写"很匹配"。

**与前面几道闸的关系**：方向对不对口只是「能不能写」；收人前仍须过 `## 🔴 学生可执行性（Doability）` 的三道闸（标化/语言、跨学科先修背景、博士项目的学位学科）。**A 档 ≠ 可投**——还要叠加「不要 G + 目标学年有项目」。

### 🔴 分档只能靠「官网 research 原文」，绝不能靠表里的备注（2026-10-09 蒋元萍重判）

上一轮我用表内「备注」列给 81 人分了 A/B/C；用户追问一条（Ceren Gunsoy）就发现误判，随后要求**全量重判**。逐人回官网读 research 段落的结果：**A/B 档 81 人里，31 人其实不对口（其中 6 位原本被我放在 A 档）、11 人是边界**——分档错误率 ~38%。

**根因**：备注是我自己早先写的**摘要**，会把官网的框定词丢掉。例：Gunsoy 备注写「研究声誉管理、印象形成与健康行为」，官网原文是「**culture's role in** … reputation management, impression formation, and health behaviors … substance use」——主轴是**文化心理学**，三个机制词单独看却像通用社会认知。同理被误放进 A 档的：Doug Markant（官网是 Learning / Metacognition / Cognitive Science）、Barbara Sarnecka（Development of …）、Elizabeth Canning（equitable and inclusive contexts）、Jeanine Skorinko（stereotypes / DEI）、Sara Hodges（perspective taking）、Jeffrey Green（self-concept / nostalgia）。

**判定细则（只看研究对象，机制词一律不作依据）**：
- ✅ 研究对象 = 判断与决策 / 推理 / 风险与不确定性选择 / 态度形成与改变 / 说服 / 情绪对决策的影响 / 自我调节与目标追求 / 消费者行为 / AI 与人类决策。**应用领域（健康、医疗、法律、组织、教育）不构成排除理由**——「用决策方法研究医疗决策」仍是决策研究者。
- ❌ 研究对象 = 另一个构念：临床症状与治疗、发展轨迹、基础认知（记忆/注意/元认知）、人格与人生意义/幸福感本身、领导力与组织行为、员工健康与职业压力、群际与种族族裔身份、**文化差异本身**、医患沟通与健康差异、物质使用、亲密关系、测量与方法学、HCI 工程与计算机。
- ⚠️ 边界（保留但单列给用户）：决策确实是对象但框定词指向另一学科（计算精神医学、衰老认知神经、医疗场景）、或官网只有一句空话无域可判。
- **一句话口诀**：**用决策/态度的方法去研究别的构念 → 删；用别的方法去研究决策/态度本身 → 留。**

**商科/营销系老师怎么判：看发表期刊，不看职称与系名（2026-10-10 Charles Lindsey 案例）**
商学院营销系的老师，光看系名与研究方向关键词判不出真伪——「人工智能与营销、客户关系管理、电子商务、渠道管理、广告、品牌忠诚」这套词既可能是**行为消费者研究**，也可能是**数量营销/战略咨询**。决定性证据是**发表阵地**：
- 出现在 **Journal of Consumer Research / Journal of Consumer Psychology / Organizational Behavior and Human Decision Processes / Journal of Experimental Psychology: Applied** 这类刊 → **行为/实验取向的消费者研究者**，能带心理学式的实验与中介模型 → **判对口**。
- 只有 Journal of Marketing / Marketing Science 等管理类刊、且无心理学刊 → 偏数量或战略，需谨慎（多为建模与二手数据，心理学式的场景实验设计未必被接受）。
- 案例：Lindsey 官网列出他在 **JCR、JCP、JM、Marketing Science、OBHDP、JEP:Applied、Journal of Advertising** 均有发表 → 判对口。对口点集中在 **R3（电商、社交媒体外溢、广告、品牌忠诚 ≈ 消费者粘性）**；R1（绿色消费·情绪机制）与他无关；其 "AI and marketing" 只是**邻近**，不等于「AI×人类决策」。
- **同时必须记下他挂在哪个博士项目**（Lindsey 属 UB 管理学院 PhD in Management / Major in Marketing，不是心理系）——商学院博士与心理学博士的培养与录取逻辑不同，别把两者混为一谈。

**执行套路（81 人一轮走完，可复用）**：
1. 从**全表**（不是某个视图）导出待判名单 + 官网个人页 URL；视图会漏掉「只有美国校关联、缺 QS 关联」的记录。
2. 分 5 组、每组 ~17 人，**并行派子代理**去读官网，要求每人返回「KEEP/DELETE/BORDERLINE + 官网 research 原文逐字（加引号）+ 一句理由」，并明确禁止采信旧备注、禁止编造。子代理会给出比我更严的判断，**最终归类由我按上表统一裁定**（子代理倾向把「决策+医疗场景」判删，按细则应判留）。
3. 汇总后先跑**干跑**：打印三档人数与逐人名，确认无遗漏、无未判定。
4. 删除前 **重查 `选导意向`**（见 `school-updates-2026-10.md` 的同名硬门）→ 全量备份到 `*_backup.json` → 每批 8 条 `DELETE` + sleep 0.8s → 回读断言零残留、记录前后条数。
5. 报告分三块：**已删除（附官网原文）/ 边界保留（附我的倾向，等一句话）/ 保留**；每条都要带官网原文，用户会逐条挑刺。

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

---

> 📎 自 SKILL.md 迁入（2026-10-07）。

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

#### 硬门 C：学校层面的「核心方向」必须有人（2026-10-13 姜一丁 GSU 案例）

**判据**：当学生有一个**标识性核心方向**（不是「方向之一」，而是介绍这个学生时会先说的那个 —— 如姜一丁的**喜剧**），则**整所学校是否纳入，以「该校至少有一位活跃师资以该方向为研究方向」为准**。

- 只有「研究方向相邻」（产业、电视、媒介理论、区域研究等）**不足以支撑整校纳入** —— 这类师资可以进表，但前提是该校先过了这一关。
- 「活跃」= 非荣休、非纯教学岗（Education-Focussed / Lecturer / 访问教授）。
- 「沾边」不算：一篇合写章节、一次创作作品上过某频道、学生社团制作，都不构成「专门研究该方向」。
- **用户扩宽方向 ≠ 核心方向消失**：用户可以说「各种方向都可以」，同时仍然用核心方向判定整校去留。两者不冲突，不要拿「扩宽」当跳过本闸的理由。

**案例（姜一丁 / 佐治亚州立大学，2026-10-13）**：GSU 的 Moving Image Studies 博士点定位（cinema / television / new media 边界消解）+ 亚特兰大 CNN·Turner 在地资源 + 影视劳工师资，看起来与扩宽后的方向集合高度吻合，于是整校收了 5 条。用户追问「这个学校有专门研究喜剧的老师吗，没有的话就全部删了」→ 核查全系 **30 位师资**与全部 FLME 课程：**无一位研究喜剧、无一门喜剧课**；唯一沾边是 Ethan Tussey 2013 年一篇 SNL 论文集合写章节。**5 条全部删除。**

**流程倒置的教训**：正确顺序是 **先核核心方向有没有人 → 再判项目定位是否匹配 → 最后收人**。反过来（先被项目定位说服、收完人再回头核方向）会产出整校级别的返工。

**表达方式**：若某校核心方向缺人但项目/城市优势明显，**单独列出并说明取舍，交用户决定**，不要自行纳入、也不要自行扣除。

---

- **OSU**: `medicine.osu.edu/find-faculty/...` 路径常废弃，faculty 页面迁移到 `mcdb.osu.edu/people/...` 或其他子域名
- **CWRU/CCF**: `lerner.ccf.org/cvme/faculty/...` 可能改为 `my.clevelandclinic.org/staff/...`
- **TAMU**: 部分 faculty 页面在子域名如 `genetics.tamu.edu` 而非主站
- **USF**: `healthscholars.usf.edu` 子域名页面结构不稳定
- **旧 URL 返回 200 但内容为空**：curl 无法识别，必须 WebFetch

---

---

> 📎 自 SKILL.md 迁入（2026-10-07）。

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
