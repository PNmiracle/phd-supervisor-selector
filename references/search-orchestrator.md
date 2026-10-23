<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：搜索编排：Step 0 学生身份确认硬门、项目底座硬门（课程总目录 + 官方博导名单）、状态续传、学校优先级 P0-P3、Pass1/Pass2 分阶段、子代理派发约定、状态更新与学习回路
> **什么时候读**：开始任何搜索任务之前必读
> **什么时候不用读**：非搜索任务：纯审核已有表、纯分析类、纯链接修复；任务已在进行中且状态文件已建立时（只需回看状态文件）

---

# Search Orchestrator

Session-aware search coordination with state tracking, smart prioritization, and standardized sub-agent dispatch. Read this before starting ANY search task.

## 0. Confirm Current Student (BEFORE ANY STATE ACCESS) — HARD GATE

Before touching `search-state/` or any existing state file, you MUST establish the current student's identity from the **current task message**, not from the directory listing.

**Hard rules:**
- `{student_name}` must come from the user's **current message** explicitly stating who this task is for (e.g., "帮 X 同学筛导师", "这是 X 的方向清单").
- **NEVER** run `ls search-state/` and pick a file to "resume". The directory contains state files from dozens of past students; treating any of them as the current context is the #1 cause of cross-student contamination (wrong directions, wrong Vika table, wrong school list loaded).
- **NEVER** `cat` a state file whose name does not match the confirmed current student.
- If the current message does not name a student, you MUST ask the user "这是哪位同学的任务？" before reading any state file. Do not guess, do not proceed on assumption.
- Only after the name is confirmed may you `cat` that one file. If it doesn't exist, create a new one — do not "fall back" to a different student's file.

> ⚠️ **复盘教训（2026-08-28）**：用户发来新学生的列表，agent 未确认姓名就直接 resume 了目录里一份完整的历史 state 文件（含方向、Vika 表、学校优先级），导致整轮操作指向错误学生。根因：skill 把"resume existing state"设为第一步却没规定姓名来源，agent 顺手 ls 了目录就误命中。

## 0.5 项目底座：先抓「学校课程总目录 + 项目官方博导名单」（HARD GATE，2026-10-07 曹琇翕案例沉淀）

**在派发任何搜索子代理之前**，必须为每所目标学校先建立「项目底座」，只用两类官方页面：

1. **学校自己的博士学位课程总目录**（研究生院 / 教务处 / study 页的 course list，按院系列出全部博士课程）
2. **每个对口项目的官方博导名单页**（potential supervisors / supervisor list / 导师名单）

### 为什么（两个真实失误）
- **漏掉整个项目**：曹琇翕（艺术+教育方向）的澳门清单里，我把「澳门科技大学 → 人文艺术学院」写进了子代理指令。代理在该院系范围内查完，如实回「无教育博士」→ 我直接把「该校无 EdD」写进交付物。**实际上澳科大 EdD 挂在「国际学院（University International College）」，2025-05 才获批新设，根本不在我给的那个学院里。**
- **导师池过薄**：香港教育大学 EdD，我只从「文化与创意艺术学系 + 教育政策与领导学系」两个系筛出 7 人（其中 6 人做的是艺术类 PhD、不是 EdD），而官方 EdD 的 **Potential Supervisors 名单一次给出 59 人**。我是靠后面偶然搜到才补的。

### 硬规则
1. **项目是否存在，只认「学校自己的课程总目录」**——不认院系页、不认第三方聚合站、不认自己的先验判断。
2. 🔴 **子代理报「该校没有 X 项目」时，必须在课程总目录上复核后才能写进交付物**。子代理的否定结论**只在它被指定的范围内成立**；把「院系内没有」当「学校没有」是这一轮最大的一类错误。
3. 🔴 **派发子代理时不要预指定院系**。只给「学校 + 方向关键词」，让代理自己从总目录定位院系。在指令里写死学院名，等于把错误前件传下去，代理越听话越会漏。
4. **专业博士（EdD / DBA / DDes / DClinPsy / EngD 等）几乎都有独立的 "potential supervisors" 名单页**，而且常常由**研究生院**维护（不在院系站点里）→ 优先抓它，比从院系师资页逐个筛准确得多、也快得多。
5. **新设项目是最容易漏的一类**：近两年新批的项目（常挂在新建学院下，如「国际学院」「未来教育学院」「教育科学学院」）在老的院系索引里找不到。抓总目录时留意「拟开办 / 新开办」标注。

### 已知可用的「项目底座」入口
| 学校 | 总目录 / 官方博导名单 |
|---|---|
| 香港教育大学 EdUHK | EdD 官方潜在导师名单（59 人）：`gs.eduhk.hk/prospective-students/edd/potential-supervisors/`（中文版 `/zh-hans/`） |
| 澳门科技大学 MUST | 研究生院博士课程总目录（按院系列出，每项目带「导师名单」链接）：`sgs.must.edu.mo/faculty/id-2894.html?locale=zh_CN`；国际学院教育/教育学导师名单：`uic.must.edu.mo/person/id-15199.html?locale=zh_CN` |
| 香港都会大学 HKMU | EdDC 督导名单：`hkmu.edu.hk/el/list-of-eddc-supervisors/` |
| 西交利物浦 XJTLU | 未来教育学院博导名单：`xjtlu.edu.cn/en/study/departments/academy-of-future-education/doctoral-supervisors` |
| 澳门理工大学 MPU | 报考条件与课程页：`mpu.edu.mo/admission_local/zh/pg_routes.php`（注意：艺术及设计学院**无博士课程**） |

> ⚠️ 顺带一条交付纪律：**交付报告里的「重点人选」表不要手写**。手写表格会静默漏掉整所学校——港教大 EdD 就是这样从 A 线重点人选表里消失的。应当**从表内数据脚本生成**（如按学校分组取前 N 条），再人工微调。

## 1. Check for Existing State

Before searching any school, check for a state file — but **only after Step 0 has confirmed the current student's name**:

```bash
# Path: {SKILL_DIR}/search-state/{student_name}.md
# {SKILL_DIR} = the directory containing this skill's SKILL.md file.
# For most agents: ~/.workbuddy/skills/phd-supervisor-selector/
cat "{SKILL_DIR}/search-state/{student_name}.md" 2>/dev/null
```

If the file exists, resume from the recorded state. If not, create one and track progress as you go.

### State File Format

```markdown
# Search State: {student_name}
Updated: {ISO timestamp}

## School Status

| School | Status | Strategy Used | Candidates Found | Notes |
|--------|--------|---------------|------------------|-------|
| UAL - Chelsea | completed | API + browser | 3 | Pure portal, API worked |
| RCA | completed | curl + browser | 5 | Staff page direct parse |
| University of Leeds | in_progress | search engine | 2 | Curl blocked, using fallback |
| University of Edinburgh | pending | - | - | - |
| Kingston University | blocked | - | 0 | Staff page 404, DNS issues |

## Known 404 URLs (do not re-check)
- https://www.kingston.ac.uk/staff/profiles/design/
- https://www.southampton.ac.uk/art/research/staff.page

## Successful Strategies (also update school-strategies.md)
> After discovering a working strategy for a school, record it BOTH here AND in `references/school-strategies.md` for long-term reuse across different students.

> 💡 **Before trying access methods from scratch, check `references/school-strategies.md` first.** It records which access layer (L1/L2/L3) and architecture each school uses. L1 = direct curl, L2 = API mining, L3 = search engine fallback. The layer tells you the path; the keywords depend on the student's discipline. It records which architecture each school uses (Pure Portal, Vue SPA, Static HTML, etc.) and which access method worked. If the school is in the registry, use the recorded strategy. If not, record your findings after the search.

- Pure portal API: https://pure.ual.ac.uk/portal/en/persons/?format=json
- Vue SPA faculty list: pattern found in app.js → /api/faculty/page
- Simple HTML parse: worktribe.com staff profiles

## Last Search Context
- Target directions: {user's research directions}
- QS range: {min}-{max}
- Regions: {UK, Australia, ...}
- Hard exclusions: {list}
```

### ⚠️ state 是快照，不是日志（2026-10-07 焊死）

实测 27 个 state 文件里最大的一个已到 **88 KB / 366 行**，其中一半是 `## Session ... 更新`、`## Batch N Final Results`、`### 待处理` 这类**过程日志**，同一个小标题重复出现多次；而上面规范要求的四段（`School Status` / `Known 404 URLs` / `Successful Strategies` / `Last Search Context`）它只有一段。

**根因**：把 state 当成 append-only 的会话流水账在写。规范要的是**当前状态快照**——快照天然有界，日志会无限增长。

**硬规则：**

1. **改 state 用覆盖，不用追加。** 更新 `School Status` 的某一行是改那一行，不要再写一段「本轮更新」。
2. **三类内容禁止写进 state**，各有更合适的落点：

| 不写进 state 的内容 | 应该写到哪 |
|---|---|
| 会话过程日志（「本轮完成工作」「PATCH v3 已完成」「修复记录」） | 不需要留存；要溯源就看 Vika 表本身 |
| 批次结果（「Batch 15 Final Results」） | 结论并入 `School Status` 的候选数一栏，明细不留 |
| 待处理 / 待办清单 | 做完即删；跨轮遗留的并入 `school-updates-<YYYY-MM>.md` 当条 |
| 跨校通用教训、新发现的通道 | `school-registry-<地区>.md` 或 `school-updates-<YYYY-MM>.md`（§8 本就要求「同时更新」） |

3. **上限：单文件 ≤200 行 且 ≤20,000 字。** `scripts/skill-budget.py` 会检查并报 WARN。
   **它不会自动清理**——state 里是学生记录，任何压缩/归档都必须逐个人工确认。
4. **学生完成后冻结**：一位学生的选导任务结束（表已交付且 P0 清空）→ 把文件移到 `search-state/_closed/`，之后不再改。
   **归档只搬不删**，且搬之前先做独立备份。

> ⚠️ `search-state/` 已被 `.gitignore` 排除，**没有版本历史**。所以任何压缩/归档动作前必须先独立备份：
> ```bash
> tar -czf ~/.workbuddy/backups/<skill>-search-state-$(date +%Y%m%d-%H%M%S).tar.gz <skill>/search-state
> ```

### Status Values

| Status | Meaning |
|--------|---------|
| `pending` | Not yet searched |
| `in_progress` | Currently searching |
| `completed` | Fully searched, results added to table |
| `completed_dry` | Fully searched, no matching candidates found |
| `blocked` | All access methods failed, documented in 排除表 |
| `skipped` | Not in scope (wrong region, no relevant dept, etc.) |

## 2. Smart School Prioritization (BEFORE searching)

Before diving into individual schools, spend 2 minutes sorting the target school list by expected yield:

### Priority Tiers

分层逻辑是**目标院系的规模和匹配概率**，不是学校排名。同一个学校对不同学生可能在不同层。

| Tier | Criteria | How to identify |
|------|----------|----------------|
| **P0 — Gold Mines** | 目标院系大（30+ 教师）、研究方向与学生高度重叠 | 院系有独立博士项目 + 多位教师做学生方向 |
| **P1 — Likely Hits** | 目标院系中等规模（10-30 教师），有部分匹配教师 | 院系存在且有博士项目，部分教师方向相关 |
| **P2 — Possible** | 院系存在但规模小或方向交叉为主 | 仅 2-5 位教师与学生方向沾边 |
| **P3 — Long Shots** | 无独立目标院系，需跨院系寻找 | 学生方向需要创造性匹配（如工业工程→机械工程自动化方向） |

### Prioritization Heuristics

1. **Department size matters**: A school with a 50-person target faculty is worth 10x more effort than one with 3 loosely related staff.
2. **Advisor experience bias**: If the student's previous successful matches came from a certain type of school (e.g., UK research-intensive, AU Group of Eight), prioritize similar schools.
3. **Cache advantage**: Schools with known working strategies (from state file) go first — they'll be fastest.
4. **User urgency**: If user says "先搜英国", don't start with Australia.

### Action

Before searching, output a quick priority matrix:

```
Search Priority (预计 20 所):
P0: 目标院系最大的 4-5 所 — 先攻
P1: 院系中等、部分匹配的 5-6 所 — 第二波
P2: 院系小或方向交叉的 5-6 所 — 第三波
P3: 需跨院系寻找的 — 最后扫尾
```

Then search P0 first, report results, advance to P1.

## 3. Phased Search Strategy (Token-Efficient)

Do NOT deep-search every school in one go. Use a two-pass approach:

### Pass 1: Quick Scan (all P0+P1 schools, ~30 min)
- Light touch: check if relevant department EXISTS
- Use: curl, API, or browser — whichever is fastest
- Output: binary yes/no per school
- Skip: schools with no relevant department

### Pass 2: Deep Verify (only schools that passed Pass 1)
- For each school with a relevant department: full discovery pipeline
- Use: API → filter → verify personal pages → fill table
- Parallelize: 3-5 schools at a time via sub-agents

This prevents wasting 20 minutes deep-searching a school that turns out to have no relevant department.

## 4. Standardized Sub-Agent Dispatch

When spawning sub-agents, use this template:

```
Task: Search {school_name} for PhD supervisors in {direction}

School: {full_school_name}
Target Department: {department_name(s)}
Student Directions: {list of directions with keywords}
Hard Exclusions: {list}

Steps:
1. Navigate to {school_url} — locate the staff/faculty directory for {department}
2. If directory found: extract all relevant staff names, titles, profile URLs
3. For each potential match: open profile page, check:
   - Research interests match student directions?
   - Evidence of PhD supervision?
   - Not excluded by title (teaching-only, emeritus, etc.)
4. Report back in this format:

FOUND:
- Name | Title | Profile URL | Research Keywords | PhD Supervision Evidence | Match Notes

NOT FOUND / BLOCKED:
- Reason (no department, all blocked, no matches, etc.)

Report back ONLY the structured list above. Do not narrate your process.
```

### Parallel Coordination

- Spawn ALL sub-agents for a tier at once
- Do your own verification work while they run
- Collect results, deduplicate, and fill the table
- Mark school status in the state file immediately


### Verification Gate (before writing ANY record)

For each candidate found, before filling the spreadsheet:

```
1. Take the name → Google "{name}" "{university}" professor
2. Click the search result → verify the page contains the person's name + research info
3. Use the verified URL for 导师主页
4. If search fails or page is blocked → mark ⚠️, include the search query
```

**Never construct URLs from patterns.** Even if you found the person via a staff directory, verify their individual profile URL via search engine. URL formats change; search engines always have the live URL.

## 5. State Update Protocol

After completing each school, update the state file immediately:

```bash
# After searching University of Leeds:
# Update status: completed, candidates: 3, strategy: curl + browser
```

If the search is interrupted, the state file IS the resume point. Next session reads it and continues where you left off.

## 6. Incremental Update (Future Sessions)

When the same student comes back for a "refresh" search:

1. Read the state file — all previously `completed` schools are already done
2. ONLY search `pending` or `blocked` schools
3. For `completed` schools, only re-check if:
   - More than 3 months since last search
   - User explicitly requests re-check
   - Known site migration or new academic year signal
4. For `blocked` schools: try ONE new approach (different domain, search engine), then leave blocked if still fails



## 8. Post-Search Learning Loop (CRITICAL)

After completing EACH school, before moving to the next:

```
1. Update school-strategies.md ← what architecture? what method worked? what failed?
2. Update state file ← mark school status, candidate count
3. (If new strategy discovered) Note it in "Successful Strategies" section above
```

This 30-second step compounds: every search makes every future search faster.

### State persistence

- **Per school**: update the state file and `school-strategies.md` immediately after completing the school
- **End of session**: ensure all state files are saved. (Optional: if the skill directory is a git repo, commit changes. Do not auto-commit without user confirmation.)

## 7. Optimization Principles

- **Check school-strategies.md first**: Before accessing a school, look it up in the registry. Known architecture → known approach → no wasted attempts.
- **Cache aggressively**: Store working API endpoints, URL patterns, department names
- **Fail fast**: If 3 attempts to access a school fail, mark `blocked` and move on. Come back at the end.
- **Batch writes**: Fill the spreadsheet in batches of 5-10, not one by one
- **Report progress**: After each P-tier completion, tell user: "P0 done: found 12 candidates across 4 schools. Starting P1."
- **Token budget awareness**: Each school deep-search costs ~5000-15000 tokens. Prioritization ensures tokens go to high-yield schools first.

## 🔍 「找人」而非「找系」——每校四入口协议（2026-10-13 用户口径，最高优先级）

**背景**：曾把「学校有没有服装/纺织院系」当作判断对口与否的依据，给 91 所学校写了「该校无服装或纺织院系」。
用户明确纠正：**学生不在意学校有没有这个专业/院系，只在意有没有做对口研究的老师；老师在商学院、计算机学院、
设计学院、工程学院、人机交互、运动科学等任何院系都算。**「没有纺织系」这种写法会让人以为没认真找。

### 强制协议
每所学校必须依次翻以下**四个入口**，全部翻过仍无人，才可判「无对口」：

1. **商学院**（运营管理 / 供应链 / 信息系统 / 市场营销 / 商业分析）→ 找 fashion / apparel / textile / retail 的供应链与数字化研究；
2. **设计 / 艺术 / 工业设计学院**→ 找 garment / body scanning / functional clothing / adaptive clothing / wearables；
3. **计算机 / 电子工程系**→ 找 virtual try-on / 3D human / garment simulation / e-textiles / wearable computing；
4. **站内检索或搜索引擎**：`[school] fashion supply chain research faculty`、`[school] apparel textile wearable professor` 等。

补充入口（按需）：运动科学 / 康复医学（功能服装）、人因工程 / 工业工程（人体测量）、心理与消费研究（时尚消费）。

### 命中判定
**研究对象或应用场景涉及服装、纺织品、可穿戴、人体测量、零售/时尚/纺织服装行业** 即算对口。
**不算对口**：纯纤维制备 / 纺织材料化学 / 复合材料且与服装关联弱；纯设计创作 / 设计史论；
可持续中与材料或环境强相关（LCA、回收工艺）；纯服饰史 / 考古；**以及完全不涉及上述对象的通用 CV / HCI / 供应链**。

### 说明行措辞（不得再写「无院系」）
> 已核对全校各院系（含商学院、设计学院、计算机学院、工程学院等），未见从事服装、纺织服装产业或可穿戴方向研究的在职教师。

若该校**确有对口师资但不进表**，备注须写明原因，例如：
> 已核对全校各院系；管理学院有从事服装供应链劳工治理研究的教师，其所在的 MRes/PhD Management 项目强制要求 GMAT 或 GRE 成绩。

### 反思
本次按此协议重扫 91 所「无对口」学校，**31 所其实藏着对口导师**，净新增 78 人 / 53 校。
代价是要翻四倍的页面，但漏掉的是真实可用的导师——宁慢勿漏。

## 🧭 找不到「系级名录页 / 系级博士项目页」时的六条排查顺序（2026-10-14 实战总结）

判定「该校确实没有该层级页面」之前，必须按下面顺序试完，否则极易误判：

1. **先试站点自身语言的路径，再试英文路径**。
   反例：Politecnico di Torino 三个系的名录页被判「已下线」，实际是路径判断错误 ——
   正确路径是 `/<系域>/en/personale/elenco`（意大利语 *personale* = 人员，*elenco* = 名册），
   而当时只试了 `/en/staff`。德/法/意/西/葡/荷的院系站普遍保留母语路径。
2. **去学校的研究门户找「按组织单元列人」的页**。
   例：The University of Sydney 的 School of Computer Science 系级名录不在 `sydney.edu.au` 站内，而在
   `profiles.sydney.edu.au/groups/<unit_id>/experts`（Pure 门户的组织单元页）；学校主站的 our-people 页是
   **学院级跨系聚合**，不合规。同理可用 `pure.<domain>` / `research.<domain>` / `researchportal.<domain>`。
3. **看系页的导航栏与 sitemap**，不要只看 URL 猜。多语言站的导航里常有「People / Staff / Members / Personale / Mitarbeitende / Membres / Personal」等入口。
4. **读官方 PDF / DOCX / 课程手册**。系级名录与邮箱有时只存在于官方附件（例：曼大 FSE Doctoral Academy Contacts 是一份 .docx，网页 HTML 里搜不到邮箱）。
5. **区分「项目页」与「介绍页」**。院系的「研究生项目」列表页（列出学位与代码，如 `AS950 Doctor of Philosophy (Science)`）可以作为**学院/系级项目页**；
   而「研究方向介绍页」「研究中心页」「实验室成员页」都不合格。
6. **系里不设博士时怎么办**。若该校博士只能走全校跨学科项目（如 WSU 的 IIDP），
   **全校研究生院入口不合规**，但**系级页面里说明该系参与该项目的那一页**（如 `amdt.wsu.edu/academics/`）可以填，
   并在交付报告里注明「该系不设独立博士，博士路径为 XXX」。

### 反例记录（用于对照，别再误判）
| 情形 | 曾经的处理 | 实际结论 |
|---|---|---|
| Polito DIGEP/DIMEAS/DISAT 的 `/en/staff` 404 | 判「名录页已下线」并清空 | **错**。正确路径 `/<系域>/en/personale/elenco`，三条均 200 |
| Sydney School of Computer Science 无系级 people 页 | 判「只有学院级聚合页」 | **错**。研究门户有组织单元页 `profiles.sydney.edu.au/groups/177744/experts` |
| QMUL `eecs.qmul.ac.uk/phd/` 跳学院首页 | 判「层级丢失」并清空 | **对**，但可替换为现行页 `qmul.ac.uk/eecs/phd/`（学院自己的 Research degrees 页） |

## ⚠️ Vika PATCH：同一 recordId 在一批里出现多次会**整批失效**（2026-10-14 实测）

给同一个人补两个不同字段时，若把两条 `{"recordId": 同一个id, "fields": {...}}` 放进同一批 PATCH，
接口返回 `data.records` 为 **0 条**（既不合并也不报错）。批量前必须**按 recordId 合并 fields**：

```python
agg = {}
for name, (field_key, url) in PLAN.items():
    agg.setdefault(record_id, {})[field_key] = url      # 合并
items = [{"recordId": rid, "fields": fs} for rid, fs in agg.items()]   # 每批 ≤5 条记录
```
（此前还遇到「返回条数少于提交条数」的情况，同样是同 recordId 被合并所致 —— 判成功的唯一标准是**回读**。）
