# Search Orchestrator

Session-aware search coordination with state tracking, smart prioritization, and standardized sub-agent dispatch. Read this before starting ANY search task.

## 1. Check for Existing State (FIRST STEP)

Before searching any school, check for a state file:

```bash
cat ~/.codex/skills/phd-supervisor-selector/search-state/{student_name}.md 2>/dev/null
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

## Successful Strategies (reuse for similar schools)
- Pure portal API: https://pure.ual.ac.uk/portal/en/persons/?format=json
- Vue SPA faculty list: pattern found in app.js → /api/faculty/page
- Simple HTML parse: worktribe.com staff profiles

## Last Search Context
- Target directions: {user's research directions}
- QS range: {min}-{max}
- Regions: {UK, Australia, ...}
- Hard exclusions: {list}
```

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

| Tier | Criteria | Examples |
|------|----------|----------|
| **P0 — Gold Mines** | Known strong art/design schools with large fashion/textile departments | UAL, RCA, University of Leeds, Southampton, NTU (UK) |
| **P1 — Likely Hits** | Schools with dedicated fashion/design/textile departments | Kingston, Heriot-Watt, De Montfort, RMIT, UTS |
| **P2 — Possible** | Schools with related depts (art history, cultural studies, anthropology) but no dedicated fashion program | Various |
| **P3 — Long Shots** | Schools where match requires creative interpretation of "design" | Engineering-heavy schools, business schools |

### Prioritization Heuristics

1. **Department size matters**: A school with a 50-person fashion faculty is worth 10x more effort than one with 3 loosely related staff.
2. **Advisor experience bias**: If the student's previous successful matches came from UK art schools, prioritize similar schools.
3. **Cache advantage**: Schools with known working strategies (from state file) go first — they'll be fastest.
4. **User urgency**: If user says "先搜英国", don't start with Australia.

### Action

Before searching, output a quick priority matrix:

```
Search Priority (预计 20 所):
P0: UAL (5 colleges), RCA, Leeds, Southampton — 先攻
P1: Kingston, Heriot-Watt, De Montfort, NTU — 第二波
P2: Edinburgh, Glasgow, Brighton — 第三波
P3: Others — 最后扫尾
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

This prevents wasting 20 minutes deep-searching a school that turns out to have no fashion department.

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

## 7. Optimization Principles

- **Cache aggressively**: Store working API endpoints, URL patterns, department names
- **Fail fast**: If 3 attempts to access a school fail, mark `blocked` and move on. Come back at the end.
- **Batch writes**: Fill the spreadsheet in batches of 5-10, not one by one
- **Report progress**: After each P-tier completion, tell user: "P0 done: found 12 candidates across 4 schools. Starting P1."
- **Token budget awareness**: Each school deep-search costs ~5000-15000 tokens. Prioritization ensures tokens go to high-yield schools first.
