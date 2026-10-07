<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：抓取技术：SPA 替代源策略、API 端点定位、URL 模式推断、并行子代理设计、浏览器验证、不可达子域处理、DDG 降级搜索、Tavily L4 兜底
> **什么时候读**：常规通道抓不到正文、需要换技术手段时；要批量并行抓取并设计子代理任务时
> **什么时候不用读**：通道正常、单页可读时；只做写入或字段校验时

---

# Search Techniques for PhD Supervisor Discovery

Practical techniques for discovering supervisor profiles, bypassing website limitations, and scaling verification efficiently.

## SPA Workaround — Alternative Academic Identity Sources (L0)

When a university's staff profile portal is a pure SPA that returns empty HTML shells (<5KB, status 200), do NOT waste time trying to crack it. Instead, find the scholar's academic footprint on alternative platforms.

### The Alternative Source Strategy

Scholars maintain academic identities on multiple platforms — most are server-rendered:

| Source | Reliability | Access Method | What You Get | Real Examples |
|--------|-------------|---------------|-------------|---------------|
| Personal academic website | **High** | WebFetch | Research areas, CV, projects, PhD students, teaching | tamaleaver.net, wishcrys.com |
| Research center/lab page | **High** | WebFetch | Role, funded projects, collaborators, research themes | digitalchild.org.au/team-members/, ierlab.com/about/ |
| ResearchGate | **Med-High** | WebFetch | All publications, research areas, stats, co-authors | researchgate.net/profile/Michele-Willson |
| ORCID | **Medium** | WebFetch | Structured profile, affiliations, limited pubs | orcid.org/0000-0002-3703-3020 |
| Google Scholar (snippet) | **Medium** | WebSearch | Citation count, research field tags | "Cited by 2,517 - Internet Studies - Disability Studies" |

### Discovery Workflow

```
For each professor at an SPA school:
1. WebSearch "[Name] [University] professor research"
2. Scan results — ignore staffportal URLs, look for:
   → Personal domain (.net, .com)
   → Research center (.org.au, .edu.au but NOT staffportal)
   → ResearchGate (researchgate.net)
   → ORCID (orcid.org)
3. WebFetch 2-3 alternative sources
4. Cross-reference: 2+ sources confirming same research = verified
5. Combine: research areas (personal site) + publications (ResearchGate) + citations (Scholar)
```

### Known SPA Schools & Their Alternative Sources

| School | SPA Portal | Working Alternatives |
|--------|-----------|---------------------|
| **Curtin University** | staffportal.curtin.edu.au (React SPA, ~2KB shell) | tamaleaver.net, wishcrys.com, digitalchild.org.au, researchgate.net |
| **Victoria University of Wellington** | people.wgtn.ac.nz (Angular SPA, 4150B shell) | researchgate.net, ORCID, Google Scholar snippets |
| **University of Auckland** | profiles.auckland.ac.nz (SPA shell) | researchgate.net, ORCID, Google Scholar snippets |
| **BNBU-UIC** | staff.uic.edu.cn (SPA, but sometimes loads in browser) | Google Scholar, ORCID |

### When L0-SPA is the RIGHT choice

- Staff portal returns <5KB (confirmed SPA shell)
- No discoverable API endpoint in JS bundle
- Tavily extract also returns empty (server-side fetch still gets JS shell)
- BUT: scholar is well-known enough to have a personal website or ResearchGate presence

### When to escalate instead

- Scholar has NO alternative online presence (very junior, no personal site, no ResearchGate)
- Scholar's only verified presence is on the SPA portal → escalate to L3 (browser verification) or L4 (Tavily)
- Need hyper-specific data only on the staff portal (office hours, phone number, grant amounts)

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

## Browser Automation for Verification

Use browser automation to verify page content that curl cannot access (JS-rendered content, hidden tabs, etc.).

> **Tool note**: The exact browser tool varies by coding agent. In WorkBuddy, use the `Agent` tool to fetch and verify URLs, or use an available browser skill. In other agents, use the equivalent browser automation feature. If no browser tool is available, use WebFetch as a fallback and note any limitations.

### Verifying Personal Pages

For each candidate URL, use a browser tool or WebFetch to:
1. Navigate to the profile URL
2. Wait for the page to fully render (if using browser automation)
3. Extract the page text content
4. Verify the page contains the person's name, title, and department

If using browser automation, the steps are:
- Go to the URL and wait for network idle
- Extract `document.body.innerText`
- Check for the person's name and research keywords

If browser automation is unavailable, use WebFetch and note any JS-rendered content that could not be verified.

### Accessing Hidden Content (Tabs/Accordions)

Many profile pages hide research interests behind clickable tabs. If using browser automation:
1. Locate the tab (e.g., "RESEARCH INTEREST", "Publications")
2. Click to reveal hidden content
3. Extract the now-visible text

If using WebFetch only, check whether the content appears in the static HTML. If not, note: "研究兴趣可能在JS标签页中，需浏览器验证."

### Batch Verification Pattern

Verify multiple candidate pages sequentially:
- For each candidate, fetch the page content
- Extract name, title, department, research interests
- If JS-rendered content is missing, note it
- Record findings in the table's 备注 field

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

## 数据源检测

收到任务时，检测数据源：

1. **用户提供 Vika 分享链接**（如 `https://vika.cn/share/shrXXX/dstXXX/viwXXX`）：直接通过 Fusion API 操作 Vika 表格。**⚠️ 重要（2026-08-19 验证）**：分享链接页面通过 `dataPack` 接口只能看到**当前分享视图**的记录，可能不完整；若要获得完整表（全部视图的全部记录），必须用**个人 API Token** 调用 Fusion API `GET /datasheets/{dstId}/records`。发现差异时优先向用户索要 API Token 做完整读取，不要只依赖分享链接的 dataPack。
2. **分享链接只有 `shrXXX` 无 `dstXXX` 时提取 datasheetId（2026-08-31 验证）**：`curl -s -A "Mozilla/5.0..." "https://vika.cn/share/shrXXX"` 抓分享页 HTML，用正则 `grep -o 'dst[A-Za-z0-9]\{10,20\}'` 提取真实 datasheetId（页面 JS 配置会内嵌）。拿到 dstId 后即可用 Fusion API 只读（`GET /datasheets/{dstId}/fields`、`GET /datasheets/{dstId}/records?maxRecords=300&fieldKey=name`）。注意：分享 token 无写权限（写操作超时/失败），只读任务可直接用此路径；`POST /share/{shrXXX}/dataPack` 返回非 JSON 时不要依赖该接口。
2. **用户上传 `.xlsx` 文件**：操作本地电子表格
3. **用户同时提供**：优先 Vika 做 CRUD，Excel 做参考/填充源

---

---

> 📎 自 SKILL.md 迁入（2026-10-07）。

---

> 📎 自 SKILL.md / search-phase.md 迁入（2026-10-07）。

## 深度发现管线

1. **全面扫描**——通过 API 获取所有教师数据，按目标院系筛选
2. **过滤**——检查剩余教师的学位、专业、研究关键词
3. **优先级排序**——按与学生方向的匹配度排名
4. **验证**——通过 WebFetch 打开个人页面，确认研究内容
5. **扩展**——仅在用户明确要求时重新检查之前 404 的链接

---

---

---

> 📎 自 SKILL.md 迁入（2026-10-07）。
