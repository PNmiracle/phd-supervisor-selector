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

## Fit Judgement

Fit can be strong even when keywords are indirect, if the supervisor's research methods, objects, or field can support the student's project. Use notes like:

- `高度匹配`: directly matches the student's preferred research object and method.
- `相关`: adjacent field, likely useful but not exact.
- `偏重`: has one useful component but leans toward a risk area (e.g., `方法偏重` for a supervisor strong in methods but different application domain; `应用偏重` for the right application but different methodology).
- `需确认带博`: profile is promising but eligibility is unclear.
- `教学岗风险`, `研究岗风险`, `更新偏旧`, etc. for concise risks.

Do not overfit by title alone. Check publications, projects, current research, supervised students, and program requirements where possible.

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
