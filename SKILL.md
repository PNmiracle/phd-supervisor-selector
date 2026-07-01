---
name: phd-supervisor-selector
description: Research and spreadsheet workflow for PhD supervisor selection. Use when the user asks Codex to search, screen, verify, expand, clean, or fill a supervisor list table for doctoral applications, including tasks mentioning 博士选导, 导师表, Supervisor List, 博导, PhD supervisor, supervisor homepage links, PhD application links, other staff links, remarks/备注, school scope, QS ranking, exclusions, or candidate fit.
---

# PhD Supervisor Selector

## Overview
## Search Orchestration (READ FIRST)

Before starting any search task, read `references/search-orchestrator.md`. It defines:
- **State tracking**: resume interrupted searches, skip already-completed schools
- **Smart prioritization**: rank schools by expected yield (P0-P3 tiers) so tokens go to high-value targets first
- **Phased strategy**: quick-scan all schools first (Pass 1), then deep-verify only promising ones (Pass 2)

Build source-backed supervisor lists for doctoral applicants. Search current university pages, judge whether a person is likely to supervise PhD students, fill the spreadsheet columns, and keep unusable or risky candidates out of the main table.

Supports two modes: **Vika (direct table CRUD)** and **Excel (local spreadsheet)**.


## Self-Improvement Protocol (AUTO)

This skill learns from every search. After searching each school, update the knowledge base so future searches are faster and smarter.

### Per-School Update (after EVERY school — success OR failure)

Update `references/school-strategies.md` immediately:

```bash
# Use the structured format. Fill in ALL fields you can.
```

**What to record:**

| Field | Required | Example |
|-------|----------|---------|
| Architecture | ✅ Always | `Pure Portal`, `Vue SPA`, `Static HTML`, `Cloudflare WAF` |
| Access method | ✅ Always | `curl → JSON API`, `browser → click tabs`, `search engine → profile URL` |
| Key endpoint | ✅ If found | `https://pure.arts.ac.uk/portal/en/persons/?format=json` |
| Failed attempts | ✅ If any | `Tried /api/staff → 404; JS bundle had no API paths` |
| Last verified | ✅ Always | `2026-06-26` |

**For schools NOT in the registry:** append a new entry.
**For schools already in the registry:** update `Last verified`, add to `Failed` if old strategy broke, replace `Access` if you found a better method.

### End-of-Session Commit

After the search session, commit accumulated learnings:

```bash
cd $SKILL_DIR && git add references/school-strategies.md && git commit -m "learn: [School1]→Arch1, [School2]→Arch2" && git push
```

This ensures every search session permanently improves the skill for all future sessions.

## Data Source Detection

When receiving a task, detect the data source:

1. **User provides a Vika share link** (e.g. `https://vika.cn/share/shrXXX/dstXXX/viwXXX`): operate directly on the Vika table via Fusion API. See §Vika Integration.
2. **User drops an `.xlsx` file**: work with local spreadsheet. See §Excel Workflow.
3. **User provides both**: prefer Vika for CRUD, Excel as reference/fill source.

## Vika Integration


**Zero dependencies.** All operations use Python 3 stdlib (`urllib` + `json`) — no `vika-cli`, npm, or third-party SDK needed. Just an API token and any Python 3 installation. For Excel import, `openpyxl` is the only extra: `pip install openpyxl`.

When the user provides a Vika share link, follow this workflow:

### Setup

1. Parse the URL to extract: `datasheetId` (`dstXXX`), `viewId` (`viwXXX`).
2. **Token security**: If the user pastes a token into the chat, accept it but also **remind them** to use the terminal method next time. Preferred flow:
   - Guide the user to run: `echo 'export VIKA_TOKEN=你的token' >> ~/.zshrc && source ~/.zshrc` (persists across all chats) or `echo 'export VIKA_TOKEN=你的token' > .vika_env && source .vika_env` (current chat only).
   - Codex reads `$VIKA_TOKEN` from environment — token never appears in chat history.
   - If `$VIKA_TOKEN` is set and valid, proceed. If not, guide the user to set it in their terminal.
3. Base URL: `https://api.vika.cn/fusion/v1`

### Capabilities (Record-level CRUD)

The Vika Fusion API supports full record-level operations:

| Operation | Endpoint | Notes |
|-----------|----------|-------|
| List fields | `GET /datasheets/{id}/fields` | Discover field names and types |
| List records | `GET /datasheets/{id}/records?viewId=...&maxRecords=...&fields=...` | Supports `filterByFormula`, `sort`, pagination |
| Create records | `POST /datasheets/{id}/records` | Batch up to 10 per call, use `fieldKey: "name"` |
| Update records | `PATCH /datasheets/{id}/records` | Send `{"records": [{"recordId":"xxx","fields":{...}}], "fieldKey": "name"}` |
| Delete records | `DELETE /datasheets/{id}/records` | Send JSON array of recordIds |

### Limitations

- **Cannot create/modify/delete fields** (schema). The Fusion API is record-only. Adding columns requires manual Vika UI.
- **Cannot write computed fields**: MagicLookUp, OneWayLink fields are read-only via API — write the source text/URL fields instead.
- Batch writes best at 10 records per request; add 0.3s delay between batches.

### Natural Language Operations

Users can issue requests in plain Chinese. Codex translates to API calls:
- "列出所有记录" → `GET /records`
- "筛选状态为待处理的导师" → `GET /records?filterByFormula={状态}="待发邮件"`
- "把 David Moreau 的状态改成等老师回复" → `PATCH /records`
- "新增一条导师叫 XXX" → `POST /records`
- "删除重复的条目" → compare names, `DELETE /records` duplicates

### Import from Excel to Vika

When importing Excel data into an existing Vika table:
1. Read Excel to extract all supervisor names.
2. Fetch existing Vika records (all, with `pageSize=200`).
3. Compare by 导师 name (strip whitespace) to find new entries.
4. Map Excel columns → Vika field names; skip linked/computed fields.
5. Batch-write new records using `fieldKey: "name"`.
6. Verify total count matches expected (original + new - overlap).

### Department Translation

Department must be written in English (or the original language of the institution). Format: **"University Name - Department Name"**. Do NOT translate to Chinese. Examples:
- "Department of Psychology, CUHK" → "CUHK - Department of Psychology"
- "University of Geneva, FPSE, Section des Sciences de l'Éducation" → "University of Geneva - FPSE, Section des Sciences de l'Éducation"
- "Victoria University of Wellington, School of Education" → "Victoria University of Wellington - School of Education"
- "University of Tübingen, IfE, Abteilung Sozialpädagogik" → "University of Tübingen - IfE, Abteilung Sozialpädagogik"

### Updating Existing Records

Use `PATCH` with recordId + field updates. Use `fieldKey: "name"` for Chinese field names. Batch 10 at a time.

### Duplicate Detection

Fetch all records, group by `导师` name (strip whitespace), keep the most complete record (most filled fields), delete others.

## Link Verification & Anti-Scraping Strategy

When encountering pages that fail `curl`/`urlopen` with 403, Cloudflare, JS challenge, or empty shell:

**1. Try harder before giving up:**
- Use the **in-app browser** (`browser` skill / Node REPL `mcp__node_repl__js`) to open the page. Many SPA/dynamic sites render correctly in a real browser.
- Click hidden tabs (e.g., "Research Interest", "Publications", "Biography") to reveal content.
- Check if the **grad school domain** (e.g., `gs.{uni}.edu.cn`, `fytgs.{uni}.edu.cn`) is on a different infrastructure and more accessible.
- Probe for **API endpoints** in the JS bundle before declaring failure.
- For staff lists, try the **university's API** directly (e.g., `?size=100000`) to bypass the UI entirely.
- If one subdomain is blocked, try **alternate subdomains** for the same university.

**2. Only after exhausting these methods**, mark with ⚠️:
- `⚠️{学校名}网站反爬/反机器人拦截，curl+浏览器均无法自动验证。需用户手动打开链接确认。`
- Keep the record in the table — never delete. The user needs to know which schools require manual attention.
- At minimum, all records **without** ⚠️ should have verified-openable links.

**3. ⚠️ format examples:**
- `⚠️Leeds Business School页面JS动态加载，浏览器可打开但内容未渲染。需手动验证。`
- `⚠️Edinburgh页面反爬拦截，curl 403 + 浏览器 Cloudflare。需手动搜索。`
- `⚠️McGill个人页重定向到搜索，API无此人数据。需手动确认。`

## Excel Workflow

(Existing Excel workflow remains unchanged)

### Core Workflow

1. Parse the student's profile, preferred research directions, hard exclusions, target regions/schools, ranking constraints, and any existing workbook/screenshot columns.
2. **Detect the spreadsheet format** (see `references/spreadsheet-rules.md`): if the user provides a template, adopt its column structure. If not, use the default simplified format.
3. Search official university sources first: supervisor profile, department staff list, PhD/research degree page, and supervisor list if available.
4. **For SPA/dynamic sites**: probe the JavaScript bundle for API endpoints before giving up (see `references/search-techniques.md`). Fetch complete datasets in one API call when possible.
5. Verify each supervisor homepage by content: the page must open and visibly match the person's name, role, department, or team identity. Do not accept a plain 200 status, dynamic shell, 404 page, or generic search page.
6. **Use the in-app browser** for content verification when curl is insufficient — especially for SPA personal pages, hidden tab content (Research Interest, Publications), and visual confirmation.
7. Judge supervision suitability using `references/selection-rules.md`.
8. Fill the spreadsheet using `references/spreadsheet-rules.md`.
9. When a school from the user's list has been searched but no suitable supervisor is found, record the school-level reason in `排除或待确认` / screening sheet.
10. Put uncertain, excluded, weak-fit, stale, or unverified people in a separate `排除或待确认` / screening sheet, not the main table.
11. Before delivery, run compact checks: no empty key links, no broken obvious links, no banned note phrases, no formula errors, and render a preview of every sheet.

### Required Output Columns

Two output formats are supported; see `references/spreadsheet-rules.md` for the full decision logic.

#### Simplified Format (default, no template provided)

`导师`, `Location`, `学校名字`, `QS排名`, `美国USNEWS排名`, `Department`, `导师主页`, `博士申请信息`, `其他导师信息`, `备注`

- `美国USNEWS排名`: **only include this column when US schools are present in the list.** When the entire list is non-US, omit it entirely.

#### Template Format (user provides an `.xlsx` template)

Follow the template's exact column headers. The standard template uses:

`导师`, `Location`, `美国学校`, `非美国学校`, `QS排名`, `美国学校的Usnews排名`, `Department`, `导师主页`, `博士申请信息`, `其他导师信息`, `备注`, `选导反馈`, `学生反馈`

Key rules for template format:
- US schools → fill `美国学校` + `美国学校的Usnews排名`; leave `非美国学校` empty
- Non-US schools → fill `非美国学校` + `QS排名`; leave `美国学校` and `美国学校的Usnews排名` empty
- Both `美国学校` and `非美国学校` can have data in the same spreadsheet but never in the same row

### URL Placement Rules

When filling `导师主页`, `博士申请信息`, `其他导师信息`:

- **`导师主页`**: Prefer the **official school/department page** that lists the supervisor (e.g., faculty directory, department staff page, lab team page). This is more stable and authoritative than a personal lab website.
- **个人主页** (personal lab/Google Scholar/ResearchGate): if more informative than the official page, put it here, but also **append the personal URL to `备注`** so it's not lost.
- **`博士申请信息`**: Prefer the department-level Research Postgraduate (RPG) programme page (e.g. /{dept}/study/research-postgraduate-programmes/ for PolyU, /{dept}/research-postgraduate-programme/ for CUHK). These have program-specific admission requirements. Fall back to the university graduate school page only when department-level pages are SPA/blocked. See references/school-strategies.md for per-school PhD URL patterns.
- **`其他导师信息`**: Official staff directory or supervisor list for the same department/school.

If only a personal page is available, use it for `导师主页` and note `⚠️仅有个人主页，无官方院系页面。` in 备注.

## Search Standards

- Browse current web pages for rankings, application links, staff lists, and profile pages.
- **Use search engines as the primary strategy** for finding individual supervisor profiles. Search `"[name] [school] professor"` on Google/Bing to discover the real profile URL — do not guess URLs from naming conventions. Guessed URLs have ~90% failure rate; search-returned URLs are current and accurate.
- Prefer official university pages over personal sites. Verify the search-result URL opens and matches the supervisor's identity before filling the spreadsheet.
- If the PhD program publishes a specific supervisor list, treat that list as binding eligibility evidence and only select names from it.
- If a common profile URL returns 404 or opens a non-matching page, search the supervisor name plus school again with Google/Bing or another web search to find the correct live URL. Do not keep guessed paths.
- **For SPA or JavaScript-rendered sites**: do not accept a 200-status empty shell. Read `references/search-techniques.md` for API discovery, URL pattern inference, and direct-path vs hash-route strategies.
- **For batch discovery**: use API endpoints to fetch all faculty at once (size=100000), then filter locally. This avoids pagination and page-by-page scraping.
- If a site blocks scraping or renders dynamically, use the browser when available and confirm visible page content manually, including clicking tabs like "Research Interest" to reveal hidden content.
- If PhD information is split across several pages, use the most relevant official research degree/program page and explain the merge briefly in the screening notes.
- If eligibility is scattered across a PDF/list and separate staff profiles, use the PDF/list for `博士申请信息` or evidence and the individual profile for `导师主页`.
- **For PhD program pages on unreachable subdomains**: check the graduate school domain (fytgs.{university}.edu.cn or gs.{university}.edu.cn) — these are often on the main university infrastructure and more accessible.
- **Use parallel sub-agents** (`spawn_agent` with explorer type) for independent checks of different schools or domains. Give each a clear, self-contained task; continue your own verification work while they run.

### Deprecated: URL Guessing

Do NOT construct URLs by guessing naming conventions (e.g., `university.edu/staff/firstname-lastname`). This fails ~90% of the time due to middle names, hyphenation, CMS restructuring, and staff turnover. Instead, use search engines to find the current live URL, or fall back to the sub-agent / API discovery pipeline.

### Deep Discovery Pipeline

Do not stop at the first batch of results. Use this funnel to maximize coverage:

1. **Full sweep** — fetch all faculty data via API, filter by target department
2. **Filter** — check degree, major, and research keywords of remaining faculty for relevance
3. **Prioritize** — rank by match to student directions; consider adjacent departments (e.g., Intelligent Transportation, Innovation/Policy for urban planning students)
4. **Verify** — open personal pages in browser, click Research Interest tabs for hidden content
5. **Expand (on-demand only)** — only re-check previously 404/unreachable links when the user explicitly requests it or when there is a clear signal (e.g., new academic year, known site migration). Routine automatic rechecking wastes tokens on structural 404s that rarely self-resolve.

Also see `references/search-techniques.md` for the full pipeline with code patterns.

### Remarks Style

Default Chinese note format:

`职称；研究关键词；风险/注意事项。`

Keep remarks short and specific. **Never use subjective evaluation phrases** such as `高度匹配`, `很匹配`, `完美匹配`, `方向非常契合`, or any similar judgment — these are misleading and risky. Describe facts, not opinions.

Do not use filler such as `主页写明`, `公开资料`, `方向集中在`, `方向一优先`, `方向二备选`, or similar ranking labels. If the user asks for Chinese-only notes, avoid English in the `备注` column.

Keep concise risk signals for teaching, adjunct, research-only, stale, 404, or supervision-uncertain profiles.

Examples:

- `副教授；博物馆研究、装饰艺术、珍奇柜；教学岗待确认。`
- `教授；文化遗产、建筑史、遗产保护；建筑遗产偏重。`
- `助理教授（教学）；策展与艺术史、中欧艺术交流；教学岗风险。`

### Workbook Shape

For new or rebuilt lists, include:

- Main sheet named after the student or requested list title.
- `说明与颜色图例`: explain row highlights, source rounds, and note/link rules.
- `排除或待确认`: record why schools or people were not included. Include ⚠️ notes for candidates found but unreachable, with URLs for user-side manual verification.
- Optional school screening sheet when the user asks to scan a region or all schools.

Highlight each newly added search round with a distinct pale color and describe the color meaning in the legend.

### Existing Workbook Handling

When the user drops a template `.xlsx`:

1. Read the template to detect its column structure. Do not overwrite column headers.
2. Fill data into the existing columns, matching by header name.
3. For mixed US/non-US lists, fill school names into the correct column (`美国学校` or `非美国学校`) based on the school's country.
4. Fill US News rankings only for US schools; leave the cell empty for non-US schools.
5. Append new rows for newly discovered supervisors; do not delete or rearrange existing rows.
6. Add new sheets (`说明与颜色图例`, `排除或待确认`) if the template does not already have them.


### CRITICAL: 导师主页 must be an INDIVIDUAL profile URL

**Never** use generic department/listing pages as `导师主页`. Every supervisor must have their own unique profile URL.

🚫 **BAD** (generic pages — do NOT use):
- `https://xxx.edu/psychology/faculty.html`
- `https://xxx.edu/apss/people/academic-staff/`
- `https://xxx.edu/sss/about-us/our-people`
- `https://xxx.edu/about/faculty`
- `https://xxx.edu/school/staff/`
- Any URL ending in: `faculty-members/`, `faculty-directory/`, `academic-staff/`, `our-people`, `about/faculty`, `/people/`, `/staff/`

✅ **GOOD** (individual pages — use these):
- `https://xxx.edu/psychology/people/jian-qiao-zhu/`
- `https://xxx.edu/en/people/faculty-members/chin-ming-hui.html`
- `https://xxx.edu/apss/people/academic-staff/prof-wu-yin/`
- `https://dr.xxx.edu/cris/rp/rp00166`

**Detection rule**: After writing records, scan ALL `导师主页` URLs. If a URL matches a generic pattern (no individual identifier in the path), find the correct individual profile URL immediately. If the individual page is JS-rendered and cannot be extracted by curl, mark in `备注` with `⚠️导师主页为系页面，需浏览器确认个人URL。`

**URL patterns per university** (add to school-strategies.md as discovered):

| University | Individual profile URL pattern |
|-----------|-------------------------------|
| CUHK Psychology | `https://www.psy.cuhk.edu.hk/en/people/faculty-members/{name-slug}.html` |
| PolyU APSS | `https://www.polyu.edu.hk/apss/people/academic-staff/prof-{name-slug}/` |
| NTU SSS | `https://dr.ntu.edu.sg/cris/rp/rp{id}?ST_EMAILID={emailuser}` |
| SMU SOCSC | JS-rendered; use browser to extract from `https://socsc.smu.edu.sg/about/faculty` |
| HKU Psychology | `https://psychology.hku.hk/people/{name-slug}/` |
| HKU Business | `https://www.hkubs.hku.hk/people/{name-slug}/` |
| CityU | `https://www.cb.cityu.edu.hk/people-and-research/people/people-details?eid={id}` |

### Post-Write URL Quality Scan

After EVERY batch write to Vika, run this check automatically:

```python
generic_patterns = ['faculty-members/', 'faculty.html', 'faculty-directory/', 
                    'academic-staff/', 'our-people', 'about/faculty', '/staff/', '/people/']
for record in new_records:
    if any(p in record.main_url.lower() for p in generic_patterns):
        # Check if URL has individual identifier after the generic part
        # e.g., /people/john-doe/ is OK, but /people/ is NOT
        # Flag for fix
```


## References

- Read `references/selection-rules.md` before deciding whether a candidate can enter the main table.
- Read `references/spreadsheet-rules.md` before creating, editing, or validating a supervisor spreadsheet.
- Read `references/search-orchestrator.md` before starting any search task to track state, prioritize schools, and resume interrupted work.
- Read `references/school-strategies.md` to check if the school has a known architecture and best access method before attempting access.
- Read `references/search-techniques.md` for SPA/API discovery, URL pattern inference, parallel sub-agent strategies, browser automation, and deep discovery pipelines.
- Read `references/vika-operations-guide.md` for the complete Vika table CRUD operations guide (list, create, update, delete, import, deduplicate, translate).
- Read `references/vika-api-patterns.md` for reusable Python code snippets for common Vika API calls.


### CRITICAL: Never modify records with select-intent already filled

When the user provides a Vika table that already has records with non-empty select-intent column:
- DO NOT modify, delete, or overwrite any record where select-intent is not empty. These records have already been reviewed by the student.
- ONLY operate on records where select-intent is empty: add new records with empty select-intent, update empty-record fields, or delete empty records.
- When verifying links and notes, skip records with non-empty select-intent entirely.

This rule applies to ALL operations: adding, updating, deleting, verifying, and batch processing.

### CRITICAL: Do NOT fill student-facing columns


### CRITICAL: NEVER modify records with existing 选导意向

When working on a Vika table that already has records, use this strict rule:

**Records where `选导意向（点击选择）` is NOT empty** → **DO NOT MODIFY, DO NOT DELETE, DO NOT UPDATE, DO NOT TOUCH**.

These records have been manually reviewed and categorized by the student. Changing them would corrupt the student's own work. Only the student modifies these records.

**Records where `选导意向（点击选择）` IS empty** → These are new records (written by the AI) that have not yet been reviewed by the student. You MAY modify these.

**Practical implementation**:
1. Before any PATCH or DELETE operation, always check `选导意向`:
   ```python
   records_to_modify = [r for r in records if not r['fields'].get('选导意向（点击选择）')]
   ```
2. When adding NEW supervisor records, always leave `选导意向` empty (see rule below).
3. When fixing data quality issues (URLs, notes, Department), ONLY fix records where `选导意向` is empty.
4. When doing bulk operations, FILTER OUT records with non-empty `选导意向` first.
5. NEVER delete or overwrite a record just because the data looks stale — if `选导意向` is filled, the student has purposefully kept that record.

**Why**: The student uses `选导意向` to track their application pipeline (优先套磁, 第二批套磁, 完全不考虑, etc.). These are the student's personal decisions. Modifying or deleting them would destroy weeks or months of the student's work.

**Examples**:
- ❌ BAD: "I see 5 old records with outdated URLs, let me fix all of them" → if `选导意向` is filled, DO NOT modify.
- ✅ GOOD: "These 3 records have empty `选导意向` → I can fix their URLs and notes."
- ❌ BAD: "This professor was rejected by the student, let me delete the record" → NEVER delete records with `选导意向`.
- ✅ GOOD: "I'll add 5 new Melbourne professors" → leave `选导意向` empty on all of them.

**When you MUST modify a record with existing 选导意向** (extremely rare, only upon explicit student request):
- The student must explicitly say "修改 XXX 记录" and specify exactly which record.
- Never batch-modify or guess.
When adding NEW supervisor records, **NEVER** set these columns:
- `选导意向（点击选择）` — for the student to choose
- `你的反馈（具体原因）` — for the student to write

New records must be added with these columns **empty**. Only the student fills them.


### CRITICAL: ✅ verification markers NEVER allowed in 备注

Do NOT include:
- `✅验证通过` / `✅已确认` / `✅页面确认` / `✅Google确认` — these are temporary verification notes, not research facts
- `Faculty页面已验证` / `个人页验证通过` / `已验证` — same, internal metadata
- Any `✅` followed by commentary

**⚠️ is allowed ONLY as a last resort** — when a page is genuinely blocked (Cloudflare/403) or a person's status is uncertain, and manual browser verification is needed. Use sparingly. Examples:
- OK: `⚠️Columbia Cloudflare封锁，浏览器可访问`
- OK: `⚠️个人页JS渲染，需浏览器确认`
- NOT OK: `⚠️在PolyU非HKU` — just state the fact without the marker




### CRITICAL: Never write enrollment/contact instructions in 备注

Do NOT include:
- `预计2026年秋入学，需提前联系` / `需发简历至xxx` / `需提前套磁`
- Any year-specific enrollment notes
- Email addresses or contact instructions

These are student-facing action items, not research facts. The `备注` column is for research keywords and risk signals only.


### CRITICAL: Never write direction-bias notes in 备注

Do NOT include these in `备注`:
- `方向偏X` / `偏X方向` — the student judges fit themselves
- `没有非常符合的老师` — subjective, risk of misleading
- `大多数相关的都在商学院` — unnecessary commentary

**"看看这个呢" / "这个看看有兴趣吗" are OK.** These are natural conversational markers when the user is uncertain about a candidate and wants to flag them for review. Keep them.

**If a supervisor might not fit**: describe their research factually, and use conversational markers if unsure. Let the student decide.


### CRITICAL: Exclude retired / emeritus / elderly professors

Do NOT add supervisors who are:
- Emeritus / Emerita Professor
- Honorary / retired status
- Clearly over retirement age (~70+) based on career timeline
- Not found in current university staff directory (likely retired)

If such a record already exists in the table, **delete it**.


---

## Pre-Flight Checklist (MANDATORY before adding ANY supervisor)

Before writing any supervisor record to the table, complete ALL of these steps. Skip NONE.

```
[ ] 1. GOOGLE SEARCH: Search "[Name] [University] professor" or "[Name] [University] [Department]"
       → NEVER guess URLs from naming conventions
       → If Google is blocked, use Bing, DuckDuckGo, or the university's own search
       → Copy the EXACT URL from the search result

[ ] 2. OPEN PROFILE PAGE: Navigate to the URL in the browser
       → Verify the page contains the person's NAME
       → Verify the page shows their TITLE and DEPARTMENT
       → If 404 or redirects to search → search again with different query

[ ] 3. CHECK RESEARCH: Find and read the "Research Interests" / "Forschungsschwerpunkte" section
       → For JS-rendered pages: CLICK tabs like "Research", "Forschung", "Publications"
       → Never add a supervisor whose research you haven't actually read
       → If research content is hidden behind JS and cannot be revealed → mark ⚠️

[ ] 4. CHECK ACTIVE STATUS: Verify the person is CURRENTLY active
       → Watch for: "Currently not an active member of staff", "Emeritus", "Emerita", 
         "pensioniert", "im Ruhestand", "retired", "Honorary", "Visiting"
       → Check u:find, HISinOne, or university directory for employment status
       → If inactive, emeritus, or retired → DO NOT ADD → DELETE immediately if already in table

[ ] 5. MATCH DIRECTIONS: Compare research keywords against student's stated directions
       → Direction 1 (Comparative/International Education): comparative education, international 
         education, education policy, global education, cross-cultural education
       → Direction 2 (Sociology of Education): sociology of education, social class, cultural 
         capital, educational inequality, social stratification, education equity
       → If research does NOT match either direction → DO NOT ADD
       → Do not add based on title alone (e.g., "Head of Education" ≠ sociology of education)

[ ] 6. INDIVIDUAL URL: Verify导师主页 is an INDIVIDUAL profile URL
       → NOT a department listing page /people/ or /staff/
       → NOT a research group page (unless no individual page exists)
       → If only a research group page is available → mark ⚠️ in 备注

[ ] 7. WRITE RECORD: Only after all 6 checks pass, write to Vika/Excel
```

## Common Mistakes (DO NOT REPEAT)

| Mistake | Example | Correct Approach |
|---------|---------|-----------------|
| Guessing URLs | `person.html?id=XXXX` never tried; assumed u:find was broken | Google search first: "Stefan Hopmann University Vienna u:find" |
| Adding by title alone | Added "Head of Education" without checking research (Sally Peters = early childhood) | Open profile → read research → verify match |
| Not verifying active status | Added Stefan Hopmann without checking u:find employment status | Check u:find, HISinOne, person search for "active member of staff" |
| Using generic department pages | Used `bildungswissenschaft.univie.ac.at/` for Hopmann instead of individual URL | Keep searching until individual profile URL is found |
| Adding without browser verification | Added Petra Herzmann/Matthias Proske with guessed URLs → both 404 | Open every profile page in browser before writing |
| Guessing URL patterns and giving up | Tried /ise/study/research-postgraduate-programmes/ (SPA shell) -> marked blocked | Search the parent page content to discover actual links instead of guessing URL variants. |

## Caution: Visiting / Guest Professors

Even well-known scholars in the field may hold **Visiting Professor** (访问教授 / Gastprofessor) appointments rather than permanent positions. Visiting professors typically:
- Cannot be primary PhD supervisors (co-supervision only at best)
- Have temporary appointments
- May not be present at the university year-round

**Always check the title on the profile page.** If it says "Visiting Professor", "Gastprofessor", "Adjunct Professor", or "Honorary Professor" → **DO NOT ADD**. Delete if already in table.

Example: Alexander W. Wiseman at Tübingen — internationally recognized comparative education scholar, but his profile showed "Visiting Professor" status → deleted from supervisor list.

---

## Meta-Rule: "反思" Trigger

When the user says **"反思"** (reflect), it means a mistake was caught. Immediately:

1. Fix the immediate issue (e.g., delete the wrong record, correct the URL)
2. Identify the ROOT CAUSE — what step was skipped or what assumption was wrong
3. Write the lesson into this SKILL.md:
   - If it's a new check → add to Pre-Flight Checklist
   - If it's a common mistake → add to Common Mistakes table
   - If it's a new category of professor to exclude → add to exclusion rules
4. Commit: `git add -A && git commit -m "reflect: {lesson}"`
5. Never defend the mistake — just fix it, learn from it, and move on

**Reflection examples:**
- User found Wiseman is Visiting Professor → added "Visiting/Guest Professors" section + exclusion rule
- User found Hopmann is inactive → added "Check active status" to Checklist
- User caught guessed URLs that returned 404 → reinforced "Google search first, never guess URLs"

---

## Session Post-Mortem: Student B (2026-06-29)

### Problems Encountered & Solutions

| Problem | Root Cause | Solution |
|---------|-----------|----------|
| Vika DELETE returned 400 for ALL records | API endpoint broken/format mismatch | Use PATCH to clear record fields as workaround |
| Cologne professor URLs 404 | Guessed `/personen/petra-herzmann/` (name slug); actual format is numeric IDs like `/33878` | Don't guess URLs — search or navigate from faculty page |
| Tübingen professor URLs 404 | Guessed `/institut/team/petra-bauer/` instead of actual `/abteilungen/sozialpaedagogik/personal/prof-dr-petra-bauer/` | Always extract href from the actual Personal page links |
| Added early childhood professor (Sally Peters) | Added by title "Head of Education" without checking research | Open profile page → read research → verify match BEFORE writing |
| Added emeritus/inactive professor (Hopmann) | Didn't check "Currently not an active member of staff" | Check u:find, person search, university directory for status |
| Added visiting professor (Wiseman) | Viewed reputation over employment status | Visiting/Guest/Adjunct professors → DO NOT ADD |
| Added LGBTQ psychologist (Sonja Ellis) | Didn't open profile to verify research area | Always open profile and read research content |
| All 4 Geneva profs had same team page URL | Didn't find individual notreequipe/equipe pages | Search Google for "[Name] [University] professor" to find real URLs |
| Hamburg profs missing 其他导师信息 | Sub-agent added records without full field set | Check all required fields after sub-agent completes |
| Department names in Chinese | Default behavior was Chinese translation | Changed to English format: "University Name - Department Name" |

### Discovered URL Patterns

| University | Correct Profile URL Pattern | Wrong Pattern Tried |
|-----------|---------------------------|-------------------|
| Tübingen IfE | `/abteilungen/{dept}/personal/prof-dr-{slug}/` | `/institut/team/{name}/` |
| Cologne HF | `hf.uni-koeln.de/{numeric_id}` (e.g., 33878) | `hf.uni-koeln.de/personen/{name-slug}/` |
| Hamburg EW | `ew.uni-hamburg.de/ueber-die-fakultaet/personen/{lastname}.html` | `ew.uni-hamburg.de/en/personal.html` |
| Vienna u:find | `ufind.univie.ac.at/en/person.html?id={numeric_id}` | `ufind.univie.ac.at/de/search.html?query=...` |
| Geneva FPSE | Various: `erdie/notreequipe/{slug}`, `edumij/equipe/{slug}`, `ggape/equipe/{slug}`, `satie/equipe/{slug}` | All used same SSED team page |

---

## Session Post-Mortem: Student B (2026-06-29~30)

### Timeline & Mistakes

| Stage | Mistake | Root Cause | Fix Applied |
|-------|---------|------------|-------------|
| Geneva profiles | All 4 used same SSED team page URL | Didn't search for individual notreequipe/equipe pages | Google search → found individual URLs |
| Hopmann added | Was "not active" since 2022 | Didn't check u:find employment status | Pre-Flight Checklist Step 4 |
| Wiseman added | Was "Visiting Professor" | Added by reputation, didn't read profile page | Visiting/Guest exclusion rule |
| Sally Peters added | Early childhood transitions, NOT comparative/sociology | Added by "Head of Education" title, didn't read research | Pre-Flight Checklist Step 3 |
| Sonja Ellis added | LGBTQ psychology, NOT education research | Never opened profile page | Pre-Flight Checklist Step 2 |
| Cologne URLs 404 | Guessed `/personen/petra-herzmann/` → actual is `/33878` | Guessed URLs instead of searching | Verification Gate: Google search first |
| Tübingen URLs 404 | Guessed `/institut/team/` → actual is `/abteilungen/.../personal/` | Didn't extract href from Personal page | Extract from actual page links |
| Vika DELETE failed | 400 on all DELETE calls | API format: `["recXXX"]` doesn't work, needs `{"recordIds": ["recXXX"]}` but both fail | PATCH clear workaround |
| GET cache staleness | Deleted records still appear in GET | Vika API caching bug | Verify in UI, not just API |
| Hamburg added without 其他导师信息 | Sub-agent didn't fill all fields | Didn't verify sub-agent output | Check all required fields after sub-agent |
| Paseka/Beck added without research verification | Profile pages too thin to confirm match | Didn't read research content | Deleted after verification |

### What Went Right

| Achievement | How |
|-------------|-----|
| VUW 6 supervisors | Extracted from School of Education JSON data |
| Geneva 4 individual URLs | Found by navigating research group sites |
| Tübingen 7 supervisors discovered | Navigated WiSo → IfE → Personal pages |
| Hamburg 2 confirmed | Verified individual profile pages work |
| Freiburg Personensuche + VL accessed | Found `uni-freiburg.link` shortlinks, bypassed main site 404s |
| All 7 dead ends diagnosed | Documented each barrier (HISinOne, Anubis, QIS login, JS shells) |

### Key Patterns Discovered

| University | Profile URL Pattern | Wrong Pattern Tried |
|-----------|-------------------|-------------------|
| Tübingen IfE | `/abteilungen/{dept}/personal/prof-dr-{slug}/` | `/institut/team/{name}/` |
| Cologne HF | `hf.uni-koeln.de/{numeric_id}` | `hf.uni-koeln.de/personen/{name-slug}/` |
| Hamburg EW | `ew.uni-hamburg.de/ueber-die-fakultaet/personen/{lastname}.html` | `ew.uni-hamburg.de/en/personal.html` |
| Vienna u:find | `ufind.univie.ac.at/en/person.html?id={id}` | `ufind.univie.ac.at/de/search.html?query=...` |
| Freiburg HISinOne | `uni-freiburg.link/personensuche` → `campus.uni-freiburg.de` | All erzwiss subdomain URLs |
| Göttingen eCampus | `ecampus.uni-goettingen.de` (200) → VL 0-text JS shell | All univz subdomain URLs |

## Session Post-Mortem: Student A (2026-06-30)

### What Went Wrong

| Problem | Root Cause | Fix Applied |
|---------|-----------|-------------|
| CUHK MAE 4人备注全错 | 用了泛知识而非主页内容（Darwin Lau写了"柔索驱动"实际是"机器人技术"） | 逐条进入/peoples/页面核对Research Interests原文 |
| PolyU ISE RPG页面找不到 | 猜了research-postgraduate-programmes（复数SPA壳）就放弃 | 翻study/父页面的内容链接，找到research-postgraduate-programme-mphil-phd（单数） |
| NTU 6人导师主页全undefined | 子代理创建记录时完全没填导师主页字段 | 逐个通过DDG搜索/Wayback Machine找到真实链接并补写 |
| Sam Kwong、Pai Zheng、Darwin Lau等标题写错 | 用了系列表页的旧职称 | 进个人页核实，Pai Zheng写的是Professor不是Associate |
| WANG Hao备注被改错 | 一个子代理把别人的研究方向写到了Wang Hao名下 | 回退到原始内容，注明子代理不可信 |
| 39条记录全部判为缺失字段的假阳性 | 用了fieldKey=id导致字段key是fldxxx，且URL字段是dict(text)不是string | 改用fieldKey=name，URL提取用val.get('text')而非val.get('link') |
| NTU RP ID全部猜错 | rp00930是Qu Jingyi不是Wei Tech ANG | 使用Wayback Machine确认entities/person/Name模式 |
| Sydney/UNSW/ANU交叉链接 | 批量构造URL时把Sydney模式套到了不同学校 | 逐条核对Department字段与URL域名匹配 |
| 子代理写入延迟/不一致 | 多个代理同时操作同一张表导致记录混乱 | 主代理在子代理完成后立即审计、修正 |

### What Worked

| Technique | Use Case | Example |
|-----------|----------|---------|
| DDG HTML搜索 | 发现正确的slug | cssamk（非sam-kwong）、wang-hao-victor（非wang-hao） |
| Wayback Machine | 绕过Cloudflare/SPA | 确认NTU实体页URL正确，提取Campolo研究方向 |
| Google Cache | 确认页面存在 | NTU entities/person/页面在缓存中有90K+内容 |
| 父页面链接扫描 | 发现SPA壳背后的真实链接 | ISE study/页->找到RPG子页 |
| CUHK /peoples/路径 | 与/people/区分 | /peoples/liao-wei-hsin/不是/people/liao-weihsin/ |
| CityU stfprofile | 绕过SPA的静态备用页 | cityu.edu.hk/stfprofile/cssamk.htm（但后来变成212壳） |
| NUS staff路径 | 与people路径区分 | cde.nus.edu.sg/me/staff/可用，/me/people/是SPA |
| Sydney name.html模式 | 统一构造个人页 | sydney.edu.au/.../academic-staff/{name}.html |

### Vika API Pitfalls

1. DELETE 400 bug: 所有DELETE请求返回400，需用PATCH改名字标记删除
2. 10记录限制: POST/PATCH每批最多10条，需分批+0.4s延迟
3. URL字段是dict: 值为{title, text, favicon}，用.get('text')取URL
4. fieldKey=id时字段名是fldXXX: 需用fieldKey=name才能用中文字段名
5. OneWayLink/MagicLookUp不可写: 学校名字、Location、QS排名通过API无法写入

### Title/Research Extraction Rules by School

| School | Title Location | Research Location | Pitfalls |
|--------|---------------|-------------------|----------|
| PolyU ISE | Professor; 在页面顶部 | Research Interests 在~9300字符处 | 别用导航菜单当研究方向（"Research Areas"在~1925处是菜单） |
| PolyU AAE | Professor of ... 在页面顶部 | Area of Specialisation 或 Biography | 页面把所有人都简写为"Professor"，实际职称需交叉核对 |
| CUHK MAE | /peoples/页标题在图片里 | Research Interests 在~1000字符处 | 用/peoples/不用/people/；slug姓在前 |
| NTU DR | entities/person/页的JSON里 | Research Keywords在JSON数据中 | 全是Angular SPA；需Wayback Machine提取 |
| NUS CDE | /me/staff/路径，页面SPA | SPA无法提取 | 仅确认URL可达，内容需浏览器 |
| Sydney | academic-staff路径，SPA | SPA无法提取 | 仅确认URL可达，内容需浏览器 |

### Sub-Agent Rules (from this session)

1. 子代理创建记录后，主代理必须立即审计：URL是否个人页、备注是否从主页提取、是否有交叉链接
2. 子代理不能信任自己的"已完成"声明——本次有代理声称"40条全部完整"但实际29条URL为空
3. 子代理之间可能冲突：hkust_search和sg_search同时操作NUS记录导致Wang Hao被覆盖
4. 子代理适合"搜索发现"，不适合"精确写入"——发现候选人后应由主代理完成写入和验证

## Browser Selection (CRITICAL)

When the skill calls for browser verification of profile pages, always use the in-app browser, NEVER the user Chrome browser.

Why:
- The user Chrome browser is their personal workspace — do not disturb it
- The in-app browser opens inside the Codex side panel, visible to the user but not intrusive
- Both browsers share the same Node REPL backend, so there is no technical reason to prefer Chrome

Implementation:
- In-app browser: import browser-client from browser plugin, then agent.browsers.get("iab")
- Chrome: import browser-client from chrome plugin, then agent.browsers.get("extension") — DO NOT USE

If neither browser works (both return empty evaluate() results), fall back to non-browser methods: DDG HTML search, Wayback Machine, Google Cache, ORCID API, Google Scholar. Do not escalate to Chrome as a fix for broken in-app browser — the issue is in the Node REPL layer, not the browser target.

Known limitation: In-app browser playwright.evaluate() may return empty strings for JavaScript-rendered pages due to sandbox restrictions. This is a known issue with the current browser-client implementation, not a reason to switch to Chrome.

## Post-Write Audit (MANDATORY)

After EVERY batch write to Vika (or after sub-agents complete their work), run the audit script:

```bash
python3 scripts/audit.py
```

The audit checks:
1. Cross-linked URLs (domain mismatch with Department field)
2. Note format (missing ；separator, missing trailing 。)
3. Garbage content in 备注
4. Missing required fields (导师主页, 博士申请信息, 其他导师信息)
5. URL accessibility (sample check on 1/3 of records)

If any issues are found, fix them immediately before reporting completion. The agent should NOT claim "all done" until audit passes clean.

### Audit + Different Model (Future)

When Codex supports model selection for sub-agents, the ideal workflow is:
1. Main agent completes search and writes records
2. Spawn audit sub-agent with a DIFFERENT model (e.g., Claude or o4-mini)
3. Audit agent runs checks and reports discrepancies
4. Main agent fixes discrepancies

This adversarial approach catches errors that a single model can miss (as demonstrated in the Student A session where the same model consistently wrote wrong 备注 for CUHK MAE professors).

---

## Session Sync Protocol

Every search session must follow this Git workflow:

**Session start:**
```bash
cd $SKILL_DIR && git pull --rebase || echo "⚠️ pull failed - manual intervention needed"
```

**During session:**
- Update `references/school-strategies.md` after each school search
- Do NOT commit after every single change — batch at end of session

**Session end:**
```bash
cd $SKILL_DIR && git add -A && git commit -m "session: [date] - [brief summary]" && git push
```

**Conflict handling:**
If `git push` fails due to conflicts (another session pushed changes):
1. `git pull --rebase` to get remote changes
2. Resolve conflicts manually
3. If auto-resolution fails, save local changes to a temp branch: `git checkout -b temp-$(date +%s) && git add -A && git commit -m "temp: unmerged changes"`

**Sub-agent learning:**
Sub-agents must NOT commit to the skill repo. Instead:
1. Sub-agent sends discovered patterns via message to main agent
2. Main agent writes to `references/school-strategies.md`
3. Main agent handles the commit

## Data Privacy: Student Name Anonymization (CRITICAL)

NEVER write the student real name into the skill repository. Use anonymized identifiers:
- Search state files: search-state/Student_A.md instead of search-state/actual-name.md
- Session post-mortems: Session Post-Mortem: Student A instead of real name
- Commit messages: session: Student A - HK+SG search instead of including real name
- School-strategies and other reference files: never mention student names

Supervisor names CAN be included — they are public information from university websites.

Anonymization protocol:
1. When creating a new search state file, use Student_{Letter} (A, B, C...) or a user-provided pseudonym
2. When writing session post-mortems, use the same anonymized identifier
3. Never include real name in commit messages
4. If a previous session already used a real name, rename the state file and update references

What to anonymize:
- Search state filenames and content
- Post-mortem section headers
- Git commit messages
- Any notes or comments in reference files

What NOT to anonymize:
- Supervisor names (public information)
- School names, URLs, research keywords
- Technical strategies and patterns discovered

Existing cleanup:
If real student names exist in the repo (search-state/ or SKILL.md post-mortems), rename immediately and update all references.

---

### CRITICAL: Never modify records with filled 选导意向

When operating on a Vika table that already has records:
- `选导意向（点击选择）` is a SingleSelect field the student uses to mark their decisions
- **If this field is NOT empty**, the student has already reviewed this record — DO NOT modify or delete it
- **Only operate on records where `选导意向（点击选择）` is empty**
- This applies to ALL operations: updating notes, changing URLs, deleting, etc.
- By default, all records written by the AI should have `选导意向（点击选择）` left empty


### CRITICAL: Never write to MagicLookUp or computed fields

MagicLookUp fields (QS排名, Location, 美国USNEWS排名) are read-only via the Fusion API.
- Do NOT include these fields in POST/PATCH requests — the API will return 400
- These fields are automatically computed from the linked school table
- The `学校名字` field should be a OneWayLink with the school's record ID in the linked table
- Write only writable fields: 导师, 学校名字, Department, 导师主页, 博士申请信息, 其他导师信息, 备注

### CRITICAL: Dedup — NEVER add a professor that already exists with 选导意向 filled

Before writing ANY new record to Vika, cross-check against existing records where `选导意向（点击选择）` is NOT empty.

**The check (every single time):**
```python
# Before adding new supervisor:
existing_reviewed = {r['fields'].get('导师','').strip().lower() 
                     for r in records if r['fields'].get('选导意向（点击选择）','')}
if new_name.lower() in existing_reviewed:
    # SKIP — this professor was ALREADY reviewed by the student
    print(f"SKIPPING {new_name}: already in student's reviewed list")
    continue
```

**Why**: Adding a new record for a professor the student has already evaluated creates confusion (two records for the same person, one with student notes and one without). The student shouldn't have to re-evaluate someone they already processed.

**Examples**:
- ❌ BAD: Adding "Jago Dodson" at RMIT → but there's already a Jago Dodson at RMIT with 选导意向=第二批套磁
- ✅ GOOD: Adding "Andrew Beer" at Adelaide → not found in any reviewed records, go ahead
- ⚠️ EDGE CASE: Kate Bishop at UTS (new) vs Kate Bishop at UNSW (reviewed) — might be different person at different university. Check profile page to confirm. If same person, skip. If different, check with user.

**Practical implementation**:
1. At start of any write session, fetch ALL existing records
2. Build a set of lowercase names from records with non-empty 选导意向
3. Before writing, check each new name against this set
4. Skip if found
5. Log all skips for the user to review

**Also applies to near-duplicates**: If names are very similar (e.g., "J. Dodson" vs "Jago Dodson"), flag for user review.
