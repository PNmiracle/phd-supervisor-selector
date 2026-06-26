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

Department 字段须填入中文，格式为 **学校名+部门名**（学校名在前，不加括号）。将英文系名翻译为中文，并在前面加上对应大学的中文名。常见模式：
- "Department of Psychology" → "大学名心理学系"
- "CUHK Business School" → "香港中文大学商学院"
- "Winchester School of Art, University of Southampton" → "南安普顿大学温彻斯特艺术学院"
- "School of Fashion and Textiles" → "学校名服装与纺织学院"

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
- **`博士申请信息`**: Always use the official graduate school or department PhD program page.
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

### CRITICAL: Do NOT fill student-facing columns

When adding NEW supervisor records, **NEVER** set these columns:
- `选导意向（点击选择）` — for the student to choose
- `你的反馈（具体原因）` — for the student to write

New records must be added with these columns **empty**. Only the student fills them.
### CRITICAL: Exclude retired / emeritus / elderly professors

Do NOT add supervisors who are:
- Emeritus / Emerita Professor
- Honorary / retired status
- Clearly over retirement age (~70+) based on career timeline
- Not found in current university staff directory (likely retired)

If such a record already exists in the table, **delete it**.

