<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载 -->
> **本文含**：规模化与兜底：并行子代理的任务设计与协调、L4 Tavily（extract/search/crawl/research）、常见 HTTP 错误与对应绕法、可选配套技能。
> **什么时候读**：L1–L3 通道全部失效（WAF 挡住 curl + 浏览器 + 搜索引擎）时；要用多个子代理并行抓一大批学校时。
> **什么时候不用读**：单校单页能直接抓到时——看 `search-techniques.md`。

---

# 搜索规模化与 L4 兜底

> 本文由 `search-techniques.md` 于 2026-10-07 按「单页技巧 / 规模化兜底」拆分而来；入口见 `search-techniques.md`。

## Parallel Sub-Agent Strategy

When checking multiple independent targets (different schools, domains, or systems), launch parallel sub-agents to run checks concurrently.

> **Tool note**: The exact sub-agent launch command varies by coding agent. In WorkBuddy, use the `Agent` tool with `subagent_type="Explore"`. In Codex, use `spawn_agent`. In other agents, use the equivalent parallel/sub-agent feature.

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

## Tavily Search-Pro Integration (L4 Fallback)

When ALL L1-L3 methods fail — WAF blocks curl, browser, and search engines; DDG returns empty; Google encrypts URLs — use tavily-search-pro as a server-side proxy to bypass client-side anti-crawl protections.

**Prerequisites**: `TAVILY_API_KEY` environment variable must be set. See tavily-search-pro skill for installation.

### Extract — Bypass WAF to Read Blocked Pages

When WebFetch/curl return 403 (Cloudflare, Incapsula, etc.) for a professor's profile page, use Tavily extract to pull content via server-side fetch:

```bash
TAVILY_API_KEY="$TAVILY_API_KEY" "$HOME/.workbuddy/binaries/python/envs/default/bin/python3" "$HOME/.workbuddy/skills/tavily-search-pro/lib/tavily_search.py" extract "https://scholars.cityu.edu.hk/en/persons/dani-madrid-morales" --format markdown
```

**When to use**:
- WebFetch returns 403/Cloudflare challenge page
- curl gets Incapsula WAF response
- Browser also blocked by anti-bot
- You already know the URL but can't read its content

**Extract with query reranking** — when extracting a long page, use `--query` to pull only the relevant sections:
```bash
... extract "https://blocked-site.edu/profile/john-smith" --query "research interests PhD supervision"
```

### Search — Alternative Search Engine When Google/DDG Fail

When DDG HTML search returns empty or Google encrypts URLs, use Tavily search for clean, unencrypted results:

```bash
TAVILY_API_KEY="$TAVILY_API_KEY" "$HOME/.workbuddy/binaries/python/envs/default/bin/python3" "$HOME/.workbuddy/skills/tavily-search-pro/lib/tavily_search.py" search "John Smith NUS professor psychology" --include-domains nus.edu.sg
```

**Advantages over DDG/Google**:
- Returns unencrypted, directly usable URLs
- Can filter by domain (`--include-domains`) for site-specific search
- Can include LLM-synthesized answers (`--answer`) for quick relevance assessment
- Works even when search engines block automated queries

**News/Finance modes** — for finding recent faculty announcements:
```bash
... news "NUS new psychology professor 2026" --time month
... finance "university faculty hiring trends" --time year
```

### Crawl — Discover Faculty Pages on a Blocked Site

When you can't access a department's faculty listing page directly, use Tavily crawl to discover all professor profile URLs:

```bash
TAVILY_API_KEY="$TAVILY_API_KEY" "$HOME/.workbuddy/binaries/python/envs/default/bin/python3" "$HOME/.workbuddy/skills/tavily-search-pro/lib/tavily_search.py" crawl "https://www.cityu.edu.hk/com/" --instructions "Find all faculty and professor profile pages" --limit 20
```

**When to use**:
- Department staff page is blocked by WAF
- Need to discover profile URL patterns (slugs, UUIDs) for a school
- Want to find all staff-related pages on a domain

### Map — Sitemap Discovery for URL Pattern Mining

When you need to understand a university site's structure to find faculty page patterns:

```bash
TAVILY_API_KEY="$TAVILY_API_KEY" "$HOME/.workbuddy/binaries/python/envs/default/bin/python3" "$HOME/.workbuddy/skills/tavily-search-pro/lib/tavily_search.py" map "https://www.otago.ac.nz/" --max-depth 2 --limit 100
```

**When to use**:
- Need to discover all staff-related URL paths on a domain
- Want to find `/staff/`, `/people/`, `/faculty/` patterns
- URL pattern mining before individual searches

### Research — Deep Department Analysis

For comprehensive research on a specific department's PhD supervision landscape:

```bash
TAVILY_API_KEY="$TAVILY_API_KEY" "$HOME/.workbuddy/binaries/python/envs/default/bin/python3" "$HOME/.workbuddy/skills/tavily-search-pro/lib/tavily_search.py" research "PhD supervisors in consumer psychology at NUS Business School" --model pro
```

**When to use**:
- Initial scan of a department's research landscape
- Finding supervisors whose profiles are scattered across multiple subdomains
- Comprehensive overview before targeted individual searches

### L4 Escalation Protocol

**Rule**: Only use L4 after L3 has been **confirmed** to fail. L4 consumes Tavily credits (1-2 per call, research costs more), so reserve it for genuine blockers.

**Escalation flow**:
1. Try L1 (curl) → fails with 403/WAF
2. Try L2 (API mining) → no API found or JS bundle inaccessible
3. Try L3 (DDG/Google search) → empty results or encrypted URLs
4. **Escalate to L4** → use appropriate Tavily mode

**Cost-aware usage**:
| Mode | Credits | When appropriate |
|------|---------|-----------------|
| extract | 1-2 per URL | Known URL but content blocked |
| search | 1-2 | Need to find URLs via search |
| crawl | 1-2 per page | Discovering site structure |
| map | 1 | URL pattern mining |
| research | varies | Deep department analysis (use sparingly) |

**After L4 success**: Record the strategy in `school-strategies.md` with `Layer: L4` so future sessions skip L1-L3 and go directly to Tavily for that school.

## Common HTTP Error Patterns and Tavily Solutions

Real-world examples from link verification batches. Each pattern has a specific L4 solution.

### Pattern 1: SPA Empty Shell (e.g., Curtin University staffportal)

**Problem**: The staff profile portal is a React/Vue SPA. `curl`, WebFetch, and even Tavily extract all return ~2KB of JS shell with zero extractable content. Status is 200, but there's no HTML content to parse.

**L1 result**: 200 OK, ~2KB empty shell
**Browser result**: Works fine (browser renders the SPA)
**Tavily extract**: Also returns empty shell (server-side fetch still gets JS, not rendered content)
**Solution**: L0-SPA — skip the staff portal entirely. Use alternative academic identity sources:
1. WebSearch `"[Name] Curtin University professor research"`
2. Find personal websites (tamaleaver.net, wishcrys.com), ResearchGate, research center pages
3. WebFetch alternative sources for full content
4. Cross-reference: 2+ independent sources confirmed = verified

**Rule of thumb**: 200 status + <5KB response on a known profile URL = SPA shell. Do NOT keep trying the same URL — switch to L0-SPA immediately. The content exists but it's client-side rendered.

### Pattern 2: 406 Not Acceptable on HEAD Requests (e.g., VUW, UoA)

**Problem**: Some servers reject HEAD requests but accept GET. `curl -I` returns 406, but `curl -sL` or browser GET works fine.

**L1 result**: 406 on HEAD, 200 on GET
**Tavily solution**: Not needed — just switch from HEAD to GET. But if GET also returns blocked content (SPA shell), use Tavily extract:

```bash
... extract "https://www.vuw.ac.nz/staff/jane-doe" --format markdown
```

**Rule of thumb**: 406 on HEAD ≠ broken URL. Always retry with GET before escalating. Only escalate to L4 if GET also fails or returns empty content.

### Pattern 3: SSL Certificate Errors on .edu.cn Sites (e.g., BNBU-UIC)

**Problem**: Some Chinese .edu.cn sites use SSL certificates that Python's certificate bundle doesn't recognize. `curl` and `python requests` throw SSL errors, but browsers (which have broader CA trust stores) work fine.

**L1 result**: SSL: CERTIFICATE_VERIFY_FAILED
**Browser result**: Works fine (broader CA trust)
**Tavily solution**: `extract` mode — Tavily's server infrastructure handles SSL negotiation independently from local Python, bypassing the certificate issue entirely:

```bash
... extract "https://faculty.uic.edu.cn/en/profile/zhang-san" --format markdown
```

**Rule of thumb**: SSL errors on .edu.cn sites are a Python/curl limitation, not a broken URL. Tavily extract completely sidesteps the problem by fetching from its own servers. This is the most reliable L4 use case for Chinese university sites.

### Pattern 4: 500 Internal Server Error on Old URLs (e.g., Jonathan Zhu at CityU)

**Problem**: A professor's old profile URL returns 500. The page may have moved to a new system (e.g., CityU Scholars portal) but the old URL wasn't properly redirected.

**L1 result**: 500 Internal Server Error
**L3 result**: Search `"Jonathan Zhu CityU professor"` → find new URL on scholars.cityu.edu.hk
**Tavily solution**: `search` mode — find the current working URL when the old one is dead:

```bash
... search "Jonathan Zhu CityU professor" --include-domains cityu.edu.hk,scholars.cityu.edu.hk
```

Then `extract` the new URL to verify content:

```bash
... extract "https://scholars.cityu.edu.hk/en/persons/jonathan-zhu" --format markdown
```

**Rule of thumb**: 500 on an old URL → don't mark as broken immediately. Search for the current URL. Tavily search+extract combo is the fastest way to find and verify the replacement.

### Quick Reference: Error → L4 Mode Mapping

| Error | Meaning | Solution | Notes |
|-------|---------|----------|-------|
| **SPA shell (200 + <5KB)** | JS-rendered portal, no content in response | **L0-SPA**: find alt sources (personal site, ResearchGate) | Do NOT retry same URL — client-side render, impossible to extract server-side |
| **403** | WAF blocked (Cloudflare/Incapsula) | extract | Most common L4 use case |
| **429** | Rate limited | extract | URL is valid, Tavily uses different rate pool |
| **406** | HEAD rejected | extract (only if GET also fails) | First retry with GET |
| **500** | Server error on old URL | search → extract | Find replacement URL first |
| **SSL error** | Python cert issue (.edu.cn) | extract | Tavily bypasses local cert validation |
| **Timeout/DNS** | Network unreachable | search | Can't extract if site is genuinely offline |

---

> 📎 自 SKILL.md 迁入（2026-10-07）。

## Optional Companion Skill

**tavily-search-pro** — AI-powered search platform that acts as **L4 fallback** when L1-L3 access methods all fail (WAF blocks curl+browser+search). Provides:
- **extract**: Server-side page content extraction (bypasses Cloudflare/Incapsula WAF)
- **search**: Alternative search engine with clean, unencrypted result URLs
- **crawl/map**: Site structure discovery for blocked university sites
- **research**: Deep department analysis with citations

Requires `TAVILY_API_KEY` environment variable. If installed, search automatically escalates to Tavily when all other access methods are blocked. See `references/search-techniques.md` (L4 section) and `references/school-strategies.md` (L4 layer).

---

> 📎 自 SKILL.md / search-phase.md 迁入（2026-10-07）。
