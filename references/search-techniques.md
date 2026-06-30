# Search Techniques for PhD Supervisor Discovery

Practical techniques for discovering supervisor profiles, bypassing website limitations, and scaling verification efficiently.

## SPA / JavaScript-Rendered Sites

Many university faculty profile systems are single-page applications (SPA) that return empty HTML shells to curl. Do not give up at a 200 status with no content.

### Find the API Endpoint

1. Download the SPA's main JavaScript bundle (e.g., `app.{hash}.js` or `chunk-vendors.{hash}.js`).
2. Search the bundle for API path patterns:
   ```bash
   curl -sL "$SPA_URL/js/app.*.js" | tr ',' '\n' | grep -i 'api\|baseurl\|faculty\|profile\|page'
   ```
3. Look for patterns like `/api/.../page`, `/api/.../list`, `/api/.../primary/{id}`.
4. Once found, test with curl. Common parameters: `pageNum`, `pageSize`, `facultyType`, `excludeJobTypes`, `dataSourcesCodes`.

### Call the API for Complete Data

Always try to fetch the full dataset in one call:
```
/api/.../page?size=100000&pages=1&facultyType=GZ&languageType=en
```
This avoids pagination and gives you all faculty records to filter locally. Total counts (e.g., `"total": 439`) confirm you got everything.

### Extract Structured Fields

Key fields to extract from each record:
- `enName`, `name` (Chinese name), `email`
- `jobs[]`: `jobEnName` (title), `departmentEnName` (thrust/department), `parentEnName` (hub/school)
- `website` (personal/lab site), `permaLink` (institutional repository)
- `degreeEnName`, `schoolName`, `majorEnName` (educational background)
- `rsidentifier[]`: Google Scholar, ORCID, ResearcherID, ScopusID
- `lastName`, `firstName` (needed for URL construction)

### Filter by Target Department

After getting all records, filter locally:
```python
for item in lists:
    for job in item.get('jobs', []):
        if job.get('departmentEnName') == 'Thrust of Urban Governance and Design':
            # This person is in the target department
```

## URL Pattern Inference

### Hash Routes vs Direct Paths

SPA frameworks (Vue, React) often have two routing systems:
- **Hash routes**: `/#/faculty-personal-page/{name}/{email}` — often don't render standalone content
- **Direct paths**: `/faculty-personal-page/{name}/{email}` — often the "real" page that renders fully

When hash routes fail, check the JS bundle for route definitions:
```bash
grep -oE '(path:\s*"[^"]*personal[^"]*"|name:\s*"[^"]*personal[^"]*")' app.js
```

### Constructing Personal Profile URLs

Once the URL pattern is understood, construct it from API data:

```
https://{host}/faculty-personal-page/{LASTNAME}-{FIRSTNAME}/{email_username}
```

Where:
- `LASTNAME` = UPPERCASE from API's `lastName` field
- `FIRSTNAME` = as-is from API's `firstName` field (may contain spaces for multi-word names)
- `email_username` = part before `@` in email

Always verify constructed URLs by opening them in the browser. Do not assume the pattern works for all; test at least one, then batch-verify all.

## Parallel Sub-Agent Strategy

When checking multiple independent targets (different schools, domains, or systems), use `spawn_agent` with `agent_type: "explorer"` to run checks in parallel.

### When to Parallelize

- Checking different schools simultaneously (e.g., CUHKSZ + UIC + UNNC)
- Verifying multiple candidate profile pages when they are on different domains
- Searching for PhD program pages across different university subdomains

### Sub-Agent Task Design

Give each sub-agent a clear, self-contained task:
- Specific URLs to check with curl
- What to look for (program names, faculty lists, research keywords)
- What format to report back in

Example:
```
Check CUHKSZ for urban planning faculty:
1. curl https://hss.cuhk.edu.cn/en - check for faculty listing
2. curl https://sse.cuhk.edu.cn/en - check for related programs
3. Search for keywords: urban, planning, geography, transportation
4. Report: which URLs work, any faculty found, their profile URLs
```

### Coordination

- Spawn all sub-agents in one batch for maximum parallelism
- Continue your own work (browser verification, API queries) while they run
- Collect results and integrate into the spreadsheet

## Browser Automation for Verification

Use the in-app browser (`browser:control-in-app-browser` skill) for content verification that curl cannot do.

### Verifying Personal Pages

For each candidate URL:
```javascript
await tab.goto(profileUrl, { waitUntil: "networkidle", timeoutMs: 10000 });
var text = await tab.playwright.evaluate(() => document.body.innerText);
// Check that the page contains the person's name, title, department
```

### Accessing Hidden Content (Tabs/Accordions)

Many profile pages hide research interests behind clickable tabs:

```javascript
// Click the RESEARCH INTEREST tab to reveal content
var researchTab = tab.playwright.getByRole("tab", { name: "RESEARCH INTEREST" });
await researchTab.click();
// Then extract the now-visible text
```

### Batch Verification Pattern

Verify multiple candidate pages sequentially in one session:
```javascript
var candidates = [
  { name: "Name1", url: "https://..." },
  { name: "Name2", url: "https://..." },
];
for (var c of candidates) {
  await tab.goto(c.url, { waitUntil: "networkidle" });
  // Extract and record content
}
```

## Deep Discovery: Full-to-Filter-to-Verify Pipeline

Don't stop at the first batch of results. Systematically expand:

1. **Full sweep**: Get ALL faculty from the target department via API
2. **Filter**: For each person not yet in the spreadsheet, check degree, major, and research keywords for relevance
3. **Prioritize**: Rank by match to student's directions. Look at PhD institution, research keywords, and department fit
4. **Verify**: Open personal pages for top candidates, click research interest tabs
5. **Expand**: Look at adjacent departments that may have relevant faculty (e.g., Intelligent Transportation, Innovation/Policy/Entrepreneurship)

### Cross-Department Expansion

When the primary department has been exhausted:
- Check if the university has related thrusts/departments in adjacent fields
- Same API call covers ALL departments — just change the filter
- Example: Urban Governance → also check Intelligent Transportation, Innovation Policy & Entrepreneurship, Data Science

## Handling Unreachable Subdomains

Some university subdomains may be unreachable from the sandbox (DNS issues, geo-blocking, firewalls):
- Document the URLs that were tried and failed
- If a sub-agent discovers content via curl but the browser can't reach it, record the findings in the `排除或待确认` sheet with a ⚠️ note
- Suggest the user verify the unreachable URLs from their own browser
- Do NOT add candidates to the main table if their profile pages cannot be verified

## PhD Program Page Discovery

When the department's own website is unreachable, look for the graduate school's program catalog:
1. Visit `fytgs.{university}.edu.cn` or `gs.{university}.edu.cn` (graduate school)
2. Look for "Postgraduate Programs" or "Program Catalog"
3. Search for the target program name
4. The graduate school page is often on the main university domain and more accessible

Construct program URLs following the pattern:
```
https://fytgs.{university}.edu.cn/programs/{program-slug}
```

Where `program-slug` uses hyphens and lowercase (e.g., `urban-governance-and-design`).

## Search Engine Fallback (Degraded Mode)

When APIs and direct URL access both fail:
- Use DuckDuckGo/Google with site-specific queries: `site:{university}.edu {name} {department}`
- Search for the person's Google Scholar, ORCID, or ResearchGate profile as secondary evidence
- Always verify found URLs by opening them; never use search result snippets as evidence


### DDG HTML Search (CRITICAL - when Bing/Google are blocked)

When Bing and Google return encrypted URLs or block curl/browser, use DuckDuckGo's HTML-only search:

**URL**: https://html.duckduckgo.com/html/?q=ENCODED+QUERY

This returns plain HTML with unencrypted result URLs that can be parsed with regex. Essential for discovering:
- Slug patterns unknown to the search agent (e.g. cssamk vs sam-kwong, wang-hao-victor vs wang-hao)
- Official staff profile pages on non-standard paths (e.g. cityu.edu.hk/stfprofile/cssamk.htm)
- SPA-blocked school profile URLs that only appear in search results

**DDG result link format**: //duckduckgo.com/l/?uddg=URL_ENCODED_TARGET - decode with urllib.parse.unquote()

**Last verified**: 2026-06-30

