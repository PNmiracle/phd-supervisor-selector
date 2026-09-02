# School Strategy Knowledge Base

Living registry of which access layer to use for each university. Discipline-agnostic — works for fashion, engineering, psychology, anything.

---

## Universal Access Framework (L0-SPA → L1 → L2 → L3 → L4)

Not every school needs a unique trick. Most fall into one of five layers:

| Layer | Name | When to use | Method | Requires |
|:---:|------|-------------|--------|----------|
| **L0-SPA** | Alternative Source Workaround | SPA returns empty shell, no accessible API, but scholars have personal sites/ResearchGate/etc. | WebSearch → find alternative domains → WebFetch personal sites/ResearchGate/research center pages | Nothing |
| **L1** | Direct Access | curl returns full HTML content | `curl` → parse staff list → extract names/links | Nothing |
| **L2** | API Mining | curl returns empty shell (SPA) but API exists | Download JS → grep `api\|baseUrl` → call API with `?size=1000` | JS bundle access |
| **L3** | Search Engine Fallback | curl blocked (403/WAF) OR JS renders but no API | Google `site:{uni} "{name}" professor` → click result in browser | In-app browser |
| **L4** | Tavily Extract/Crawl | L3 fails (WAF blocks even search, encrypted URLs, DDG empty) | `tavily-search-pro extract/crawl/search/research` → bypass client-side WAF via server-side fetch | `TAVILY_API_KEY` env var |

### Decision Tree

```
For each professor, identify the school →
Check school-strategies.md for that school's known layer

├── L0-SPA: Skip staff portal → WebSearch for alternative sources
│   ├── Found personal website → WebFetch (rich HTML, full content)
│   ├── Found ResearchGate → WebFetch (publications + research areas)
│   ├── Found research center page → WebFetch (role + projects)
│   └── Combine all sources → verified research profile
│
├── L1: curl → 200 + HTML table/links → parse directly
│
├── L2: curl → 200 + empty shell (<5KB) → hunt API in JS bundle
│   ├── API found → call API, filter results
│   └── No API → escalate to L3
│
├── L3: curl blocked (403/WAF) → search engine per name
│   ├── Search results found → verify in browser
│   └── Search blocked/encrypted → L4
│
└── L4: Tavily fallback for WAF/blocked pages
```

### L0-SPA — Alternative Source Strategy (NEW)

When a university's staff profile portal is pure SPA (returns <5KB empty HTML shell, status 200 but no content):

**Why SPA portals fail**: React/Vue/Angular render content client-side. WebFetch, curl, and even Tavily extract only receive the JS shell. The actual professor data never reaches the server response.

**Key insight**: Scholars maintain academic identities on MULTIPLE platforms — most are server-rendered and accessible:

| Source | Reliability | Access | Typical Content |
|--------|-------------|--------|-----------------|
| Personal academic website | **High** | WebFetch | Research areas, projects, CV, PhD students, teaching |
| Research center/lab page | **High** | WebFetch | Role description, funded projects, collaborators |
| ResearchGate | **Med-High** | WebFetch | All publications, research areas/tags, citation stats, co-authors |
| ORCID | **Medium** | WebFetch | Structured profile, affiliations, limited publication list |
| Google Scholar (snippet) | **Medium** | WebSearch | Citation count, research field tags (from search result snippet) |

**Discovery workflow**:
1. WebSearch `"[Name] [University] professor research"`
2. Scan results for non-staffportal domains (wordpress.com, .net, researchgate.net, .org.au, ORCID)
3. WebFetch 2-3 alternative sources for each professor
4. Cross-reference: research areas from personal site + publications from ResearchGate + citations from Scholar

**Reliability rule**: A research direction confirmed by 2+ independent alternative sources = verified. Single-source data = noted with source.

### L4 — Tavily Search-Pro Integration

When all L1-L3 methods fail (WAF blocks curl+browser+search, DDG returns empty, Google encrypts URLs), use tavily-search-pro as a server-side proxy that bypasses client-side anti-crawl protections.

**Command location**: `$HOME/.workbuddy/skills/tavily-search-pro/lib/tavily_search.py`
**Python runtime**: `$HOME/.workbuddy/binaries/python/envs/default/bin/python3`
**Required**: `TAVILY_API_KEY` environment variable set
**Note**: 如果 `tavily-search-pro` skill 未安装，L4 层不可用。通过 WorkBuddy 推荐市场安装，或跳过 L4 直接用 L3 搜索引擎兜底。

| Tavily Mode | When to Use | Example |
|-------------|-------------|---------|
| **extract** | WebFetch/curl blocked by WAF (403, Cloudflare, Incapsula) | Extract a professor's profile page content when direct access is blocked |
| **search** | Search engines return encrypted URLs or no results; DDG HTML empty | Search `"John Smith NUS professor"` when Google/DDG fail |
| **crawl** | Need to discover all faculty pages on a university site | Crawl a department's website to find all professor profile URLs |
| **map** | Need a sitemap of faculty-related URLs | Map `nus.edu.sg` to discover all staff directory paths |
| **research** | Deep analysis of a department's faculty composition | Research `"NUS Psychology department PhD supervisors"` for comprehensive results |

**L4 Command Syntax**:
```bash
TAVILY_API_KEY="$TAVILY_API_KEY" "$HOME/.workbuddy/binaries/python/envs/default/bin/python3" "$HOME/.workbuddy/skills/tavily-search-pro/lib/tavily_search.py" <mode> "query" [options]
```

**L4 Escalation Rule**: Only escalate to L4 after L3 has been attempted and confirmed to fail. L4 consumes credits (1-2 per call), so reserve it for genuine blockers.

### Why this works for any discipline

The layer is about **how the university website is built**, not what subject you're searching. A Vue SPA at an engineering school needs the same L2 API-hunting as a Vue SPA at an art school. The keywords change; the access method doesn't.

---

## Architecture → Layer Mapping

| Architecture | Default Layer | Notes |
|-------------|:---:|-------|
| Static HTML | **L1** | Direct curl + parse |
| Worktribe | **L1** | `/staff/profiles/` pattern |
| Pure Portal (with API) | **L2** | `?format=json` or `ws/api/persons/search` |
| Pure Portal (no API) | **L3** | JS-rendered, API blocked → search engine |
| Vue SPA | **L2** | JS bundle → API endpoint |
| React SPA | **L2** | JS bundle → API endpoint |
| Cloudflare WAF | **L3→L4** | curl blocked → browser + search engine → Tavily extract/crawl |
| Imperva/Incapsula | **L3→L4** | Browser may also be blocked → Tavily extract fallback |
| Custom CMS | **L1→L3** | Try L1 first, escalate if blocked |

---

## School Registry

Format: Architecture + Layer + Access method + Endpoints + Failures

### Per-School Template

```markdown
#### School Name
- **Layer**: L1 / L2 / L3
- **Architecture**: Static HTML / Pure Portal / Vue SPA / etc.
- **Best method**: [one sentence]
- **Key URL / endpoint**: [URL]
- **Failed**: [what didn't work]
- **Last verified**: YYYY-MM-DD
```

---

## School Entries

### 🇬🇧 United Kingdom

#### University of the Arts London (UAL)
- **Architecture**: Pure Portal (JS-rendered)
- **Layer**: L2
- **Best method**: L3 — Google `site:researchers.arts.ac.uk "{name}"` → click first result in browser. Profile URL format: `researchers.arts.ac.uk/{id}-{slug}`.
- **Key endpoint**: Profile URLs use format `https://researchers.arts.ac.uk/{numeric-id}-{slug}` (NOT `/en/persons/{slug}`)
- **Failed**: `?format=json` does NOT work on UAL Pure; `/en/persons/{slug}` returns 404; `curl` alone cannot extract data
- **Last verified**: 2026-06-26

#### Royal College of Art (RCA)
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Leeds
- **Architecture**: Static HTML (staff profile pages)
- **Layer**: L1
- **Access**: Direct URL access to staff profiles at ahc.leeds.ac.uk/design/staff/
- **Key endpoint**: https://ahc.leeds.ac.uk/design/staff/
- **Failed**: —
- **Last verified**: 2026-06-26

#### University of Southampton
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### Kingston University
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### De Montfort University
- **Architecture**: Static HTML (staff profile pages)
- **Layer**: L1
- **Access**: Direct URL access to academic staff pages at dmu.ac.uk/academic-staff/
- **Key endpoint**: https://www.dmu.ac.uk/academic-staff/
- **Failed**: —
- **Last verified**: 2026-06-26

#### University of Edinburgh
- **Architecture**: JS-rendered profile directory (edwebprofiles.ed.ac.uk)
- **Layer**: L3
- **Access**: https://www.ed.ac.uk/profile/{name} → redirects to JS profile
- **Key endpoint**: https://www.ed.ac.uk/profile/alison-lenton
- **Failed**: —
- **Last verified**: 2026-06-26

#### University of Glasgow
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Brighton
- **Architecture**: Pure Portal (research.brighton.ac.uk)
- **Layer**: L2
- **Access**: Pure Portal JSON API → parse researcher profiles
- **Key endpoint**: https://research.brighton.ac.uk/persons/
- **Failed**: —
- **Last verified**: 2026-06-26

#### Nottingham Trent University (NTU)
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### Heriot-Watt University
- **Layer**: L2
- **Architecture**: Pure Portal (researchportal) + Static HTML (hw.ac.uk)
- **Best method**: Use hw.ac.uk profiles (not researchportal UUIDs). Format: `hw.ac.uk/profiles/uk/school/tex/faculty/{slug}`
- **Key URL / endpoint**: `https://www.hw.ac.uk/profiles/uk/school/tex/faculty/{slug}`
- **Failed**: researchportal.hw.ac.uk UUID-based URLs → 404
- **Last verified**: 2026-06-26

#### University College London (UCL) — Psychology
- **Architecture**: profiles.ucl.ac.uk numeric ID system (RESTRUCTURED 2025-2026)
- **Access**: Old PALS URLs 404 → new system https://profiles.ucl.ac.uk/{numeric-id}-{name}
- **Key endpoint**: https://profiles.ucl.ac.uk/2667-david-shanks
- **Failed**: All old pals.ucl.ac.uk URLs broken
- **Last verified**: 2026-06-26

#### Birkbeck, University of London
- **Architecture**: Static HTML + numeric profile IDs
- **Access**: https://www.bbk.ac.uk/our-staff/profile/{id}/{name}
- **Key endpoint**: https://www.bbk.ac.uk/our-staff/profile/8009667/ulrike-hahn
- **Failed**: Profile IDs can redirect to wrong person; verify the ID
- **Last verified**: 2026-06-26

#### University of Bristol
- **Architecture**: Main dept pages redirect to generic homepage; use RIS portal
- **Access**: https://research-information.bris.ac.uk/en/persons/{name}
- **Key endpoint**: https://research-information.bris.ac.uk/en/persons/stephan-lewandowsky
- **Failed**: All bristol.ac.uk/psychology people pages redirect to dept homepage
- **Last verified**: 2026-06-26

#### University of Warwick — Business School
- **Architecture**: Static HTML (WBS separate from main Warwick)
- **Access**: https://www.wbs.ac.uk/about/person/{name}/
- **Key endpoint**: https://www.wbs.ac.uk/about/person/neil-stewart/
- **Failed**: Old warwick.ac.uk/fac/sci/psych/people URLs 404 for Stewart (moved to WBS)
- **Last verified**: 2026-06-26

### 🇦🇺 Australia

#### University of Melbourne
- **Architecture**: findanexpert SPA (Pure Portal variant) — /display/person-* returns same SPA shell for all slugs ⚠️; /profile/{id}/{slug} has unique individual profile IDs but still 0-byte SPA via curl
- **Layer**: L3 (curl useless for content; browser required)
- **Access**: curl returns 200 with 0 bytes (SPA shell). MSD pages (msd.unimelb.edu.au) return 403 via curl. Browser renders findanexpert correctly.
- **Key endpoint**: `https://findanexpert.unimelb.edu.au/profile/{id}/{slug}` — individual profile pages with unique IDs
- **Individual profile URL pattern**: `https://findanexpert.unimelb.edu.au/profile/{numeric_id}/{name-slug}`
- **Staff directory**: `https://findanexpert.unimelb.edu.au/college/1/faculty-of-architecture-building-and-planning`
- **PhD info**: `https://study.unimelb.edu.au/find/study-areas/architecture-building-and-planning/`
- **⚠️ CRITICAL**: /display/person-* endpoint matches ANY slug with same SPA shell → DO NOT use to verify affiliation. Use /profile/{id} format or browser verification.
- **⚠️ David Beynon lesson**: findanexpert returned 200 for "person-david-beynon" but he was actually at UTAS. Always browser-verify or use /profile/{id} format.
- **Failed**: /display/ endpoint is unreliable; MSD direct pages 403
- **Last verified**: 2026-06-30

#### University of Sydney
- **Architecture**: Symplectic Elements Discovery portal (profiles.sydney.edu.au). All individual profiles and group pages are pure SPAs (2118 bytes shell). CSS/JS loaded dynamically.
- **Layer**: L3 (Symplectic Elements SPA)
- **Best method**: Main education page (sydney.edu.au/arts/schools/sydney-school-of-education-and-social-work.html) returns 67KB with some profile links embedded. Individual profiles require browser verification.
- **Key endpoint**: profiles.sydney.edu.au/{username} (SPA)
- **Failed**: All API paths (v1/api/individuals, api/rest/v1, etc.), model.json feeds, JSON/RDF format parameters, print view
- **Last verified**: 2026-06-30

#### UNSW Sydney
- **Architecture**: Adobe Experience Manager (AEM) SPA for listing pages. Individual staff profiles at unsw.edu.au/staff/{slug} return real content (100-500KB) with research data embedded in HTML. Research profile pages (research.unsw.edu.au/people/{slug}) also accessible. Main domain may trigger Cloudflare, but staff sub-pages consistently work with curl.
- **Layer**: L2 (Adobe AEM SPA, staff profiles accessible)
- **Best method**: Use known staff names to construct unsw.edu.au/staff/{slug} URLs. Parse HTML for research keywords, publications, grants. School of Education research strengths include "Sociology of education." VERIFIED 2026-07-01 with 6 profiles.
- **Key endpoint**: https://www.unsw.edu.au/staff/{slug}
- **PhD application**: https://www.unsw.edu.au/study/research-degrees
- **Note**: Ben Newell moved from UCL/others → UNSW; not at Carleton
- **Failed**: AEM model.json returns minimal structure only; Our People listing page is SPA; newsroom expert finder API returns HTML only; newsroom.unsw.edu.au/find-an-expert redirects/times out; research.unsw.edu.au/people search returns SPA
- **Last verified**: 2026-07-01

#### QUT
- **Architecture**: Cloudflare WAF (全站)
- **Layer**: L3
- **Access**: BLOCKED — needs manual browser from user side
- **Key endpoint**: https://www.qut.edu.au/research/our-people
- **Failed**: curl + browser both blocked
- **Last verified**: 2026-06-26

#### Macquarie University
- **Architecture**: Pure research portal (researchers.mq.edu.au)
- **Access**: https://researchers.mq.edu.au/en/persons/{name}/
- **Key endpoint**: https://researchers.mq.edu.au/en/persons/abas-mirzaei/
- **Last verified**: 2026-06-26

#### RMIT University
- **Architecture**: Pure Portal (academics) + Cloudflare WAF
- **Layer**: L3
- **Access**: Cloudflare WAF blocks all curl access; browser required
- **Key endpoint**: https://www.rmit.edu.au/contact/staff-contacts/academic-staff/
- **Profile URL pattern**: academics.rmit.edu.au/{name-slug} (SPA)
- **Last verified**: 2026-07-01

#### University of Technology Sydney (UTS)
- **Architecture**: UTS Profiles (SPA) + Cloudflare/Imperva
- **Layer**: L3
- **Access**: Cloudflare/Imperva blocks all curl access; browser required
- **Key endpoint**: profiles.uts.edu.au/{Firstname}.{Lastname}/about (SPA shell)
- **Last verified**: 2026-07-01

#### Deakin University
- **Architecture**: Pure Portal SPA (experts.deakin.edu.au) + Cloudflare WAF (deakin.edu.au CMS pages)
- **Layer**: L3
- **Access**: experts.deakin.edu.au/{slug} returns "Discovery" SPA shell (~2KB). Individual profiles require browser. deakin.edu.au/about-deakin/people blocked by Cloudflare.
- **Key endpoint**: https://experts.deakin.edu.au/{slug}
- **PhD application**: https://www.deakin.edu.au/study/find-a-course/research-degrees
- **Note**: experts.deakin.edu.au is the consistent URL pattern.
- **Failed**: deakin.edu.au/about-deakin/people/{name} → 403 Cloudflare
- **Last verified**: 2026-07-01

#### Curtin University (2026-07-03 update — SPA CORRECTION)

⚠️ **Previous assessment was incorrect.** staffportal.curtin.edu.au is a **pure React SPA** — all profile pages return ~2KB empty HTML shells to WebFetch/curl, even though browsers render them fine. about/our-people also uses JS accordions with no static content.

- **Architecture**: React SPA (staffportal) + WordPress (personal sites) + JS accordion (about pages)
- **Layer**: L0-SPA (SPA Workaround — skip staffportal entirely, use ALTERNATIVE sources)
- **Accessible** (WORKING):
  - **Personal academic websites**: tamaleaver.net, wishcrys.com (WordPress, static HTML, full content)
  - **Research center pages**: digitalchild.org.au/team-members/ (ARC Centre — server-rendered, full profiles)
  - **ResearchGate**: profiles with publications, stats, research areas (server-rendered)
  - **Google Scholar**: search snippets give research tags + citation counts
  - **ORCID**: structured profile data
- **Blocked**: staffportal.curtin.edu.au ALL pages (SPA shell, ~2KB, zero extractable content), about/our-people (JS accordion, no names visible)
- **SPA Workaround Strategy** (L0):
  1. WebSearch `"[Name] Curtin University professor research"` → find alternative domains
  2. Prioritize: personal WordPress sites > research center pages > ResearchGate > Google Scholar
  3. WebFetch alternative sources for detailed content
  4. Combine data: personal site for research areas + ResearchGate for publications + Scholar for citations
- **Verified examples**:
  - Tama Leaver: tamaleaver.net (full profile, research, books, teaching awards) + digitalchild.org.au (CI role)
  - Crystal Abidin: wishcrys.com (full profile, 250+ pubs, h-index 42, awards) + ierlab.com (lab director)
  - Michele Willson: researchgate.net (43 pubs, Monash PhD, research areas) + ORCID
  - Mike Kent: Google Scholar snippet (cited 2,517, Internet Studies/Disability Studies/eLearning) + ResearchGate
- **Last verified**: 2026-07-03

### 🇭🇰 Hong Kong

#### University of Hong Kong (HKU)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: browser → psychology.hku.hk faculty page; business school via hkubs.hku.hk
- **Key endpoint**: https://psychology.hku.hk/faculty-members/
- **Failed**: —
- **Last verified**: 2026-06-26

#### Chinese University of Hong Kong (CUHK)
**CRITICAL — Must follow this workflow for ALL CUHK departments:**

1. **Always start from the staff listing page** (all are server-rendered static HTML, L1)
2. **Extract every name + profile URL from the listing page** — do NOT construct URLs from memory or search snippets
3. **Verify each person is still in the current listing** before writing to Vika

| Department | Staff Listing URL | Individual Profile Pattern | Slug Format |
|-----------|-------------------|---------------------------|-------------|
| Psychology | `psy.cuhk.edu.hk/en/people/faculty.html` | `faculty-members/{slug}.html` | Firstname-lastname (e.g. `qian-wang`, `helene-fung`). Note: NO `prof-` prefix |
| Social Work | `web.swk.cuhk.edu.hk/en-gb/people/full-time-teaching-staff` | `full-time-teaching-staff/{id}-prof-{slug}` | Numeric ID prefix (e.g. `144-prof-ngai-sek-yum-steven`) |
| Educational Psychology | `fed.cuhk.edu.hk/eps/en/people/academic-staff/` | `eps/en/peoples/{slug}/` | `prof-{firstname}-{lastname}` (e.g. `prof-hawk-skyler`, `prof-chui-tsz-yeung-harold`) |
| MAE (Engineering) | Uses `/peoples/` NOT `/people/` for individual profiles | `peoples/{slug}/` | Surname-first (e.g. `lau-darwin-tat-ming`) |
| Statistics & Data Science | `sta.cuhk.edu.hk/pcat/faculty/` | `peoples/{slug}/` | Abbreviated slug (e.g. `jwang`, `hywong`, `bdai`, `ylin`, `ligen`, `tonysit`, `cyyau`, `ywei`, `jiachengzh`, `zxlin`) |

**STA 特殊规则（2026-07-13 验证）：**
- `/people/faculty/{name}/` 是 SPA 壳 — 所有自动化工具拿到相同首页 HTML（114KB），必须用 `/peoples/{slug}/` 替代
- pcat/faculty 列表页是静态 HTML，可直接抓取获取正确 slug
- 个人 `/peoples/` 页面为静态 HTML，包含完整研究方向信息

**Common pitfalls (learned 2026-07):**
- Psych dept changed slug format — removed `prof-` prefix from URLs (e.g. `prof-wang-qian` → `qian-wang`)
- SWK dept completely rebuilt their site — old `/en/people/teaching-staff/` → new `/en-gb/people/full-time-teaching-staff/{ID}-{slug}`
- Education dept moved from `/en/people/` → `/eps/en/peoples/`
- Several professors listed on old sites had moved to other institutions (HKU, etc.) — always cross-check against current listing page
- **Do NOT trust search engine snippets alone** — always open the listing page to confirm the person is still there

- **Architecture**: Static HTML (all 3 departments above) + JS-rendered (business school)
- **Layer**: L1 (Psych, SWK, Edu Psych) / L2-L3 (Business)
- **Failed**: Psych/SWK/Edu pages occasionally change URL patterns without redirect; always verify via listing page
- **Last verified**: 2026-07-07
- 

#### HKUST
- **Architecture**: Static HTML
- **Layer**: L2→L3
- **Access**: Web accessible; no Psychology dept (only Division of Social Science). Target Business School Marketing dept.
- **Key endpoint**: https://mark.hkust.edu.hk/faculty-and-staff/directory (Business School Marketing)
- **Also**: https://bm.hkust.edu.hk/faculty (Business School general) — has "Leadership and Behavioral Decision-making" research area. Management dept may have additional behavioral faculty.
- **PhD link**: https://prog-crs.ust.hk/pgprog/2022-23/mphil-phd-mark
- **Failed**: No Psychology PhD
- **Last verified**: 2026-06-26

#### City University of Hong Kong (CityU)
- **Architecture**: Incapsula WAF (main domain + stfprofile) + Cloudflare WAF (scholars subdomain)
- **Layer**: L3→L4 (Fully blocked from curl/WebFetch/urllib; search engine fallback required)
- **WAF 现状（2026-07-13 验证）**:
  - CityU 全站 Incapsula WAF，自动化工具（curl、Python urllib、WebFetch）**全部被拦截**
  - stfprofile 页面：200 返回 Incapsula JS 挑战页（约 200-1000 字节），不是真正死链
  - scholars.cityu.edu.hk：**403 Forbidden**（自动化访问），浏览器正常
  - **自动化审计脚本检测 CityU 链接时必然全部报死链/SPA壳，这是已知的系统性问题**
  - 链接有效性必须由人在浏览器中确认，不要因为 WAF 拦截就删除记录
- **Primary workflow — Scholars Portal (ALL departments, mandatory)**:
  1. 浏览器打开 https://scholars.cityu.edu.hk/en/persons/ — CityU 统一教师数据库
  2. 搜索导师姓名
  3. 打开个人页面，复制 URL（格式: `scholars.cityu.edu.hk/en/persons/{name}({uuid})`）
  4. 写入 Vika 的 `导师主页` 列
  5. **备用格式**: stfprofile 页面 `www.cityu.edu.hk/stfprofile/{slug}.htm`，优先级高于 scholars（因为至少返回 200 而非 403）
- **写入后复验规则（WAF 调整版）**:
  - WebFetch 验证 CityU 链接时，预期返回：stfprofile → 200 + ~200-1000字节（JS挑战）；scholars → 403
  - 以上两种结果都不是死链信号，**不删除记录**
  - **仅以下情况才删除**：Google/DDG 搜不到该导师、系页面已移除、或浏览器确认 404
  - 交付前提示用户在浏览器中抽查 CityU 链接
- **自动化审计的 CityU 豁免**：
  - 计算链接通过率时，可将 CityU 记录从分母中扣除
  - 例如：55 条中 15 条 CityU，非 CityU 40 条全通过 → 实际链接率 100%（而非 73%）
  - WAF 拦截 ≠ 链接质量缺陷
- **Subdomain probe results** (2026-07-13):
  - www.cityu.edu.hk/stfprofile/*: Incapsula WAF（200 + 约 200-1000 字节 JS 挑战）
  - scholars.cityu.edu.hk: 403 Forbidden（自动化工具）；浏览器正常
  - www6.cityu.edu.hk: Incapsula
  - www2/www3.cityu.edu.hk: SSL EOF
  - sgs.cityu.edu.hk: SSL EOF
  - cb.cityu.edu.hk/staff/: 可直接访问（商学院）
- **ORCID Discovery Method** (when all search engines fail):
  1. `curl "https://pub.orcid.org/v3.0/search/?q=affiliation-org-name:%22City+University+of+Hong+Kong%22"` → get ORCID IDs
  2. `curl "https://pub.orcid.org/v3.0/{orcid}/person"` → get researcher names and details
  3. Cross-reference found names with target department
  4. Search found names on scholars.cityu.edu.hk for profile verification (in browser)
  5. If profile found, write to Vika; if not, mark with note in 备注
- **Failed**: 全部自动化方案对 CityU 主页/教师资料页无效；ssweb.cityu.edu.hk blocked by Incapsula
- **Last verified**: 2026-07-13

#### Hong Kong Polytechnic University (PolyU)
- **Architecture**: JS-rendered
- **Layer**: L3
- **Access**: polyu.edu.hk/apss/ for Applied Social Sciences; polyu.edu.hk/mm/ for Marketing
- **Key endpoint**: https://www.polyu.edu.hk/apss/people/academic-staff/
- **PhD link**: https://www.polyu.edu.hk/apss/study/research-postgraduate-programme/
- **Individual profile pattern**: `polyu.edu.hk/apss/people/academic-staff/prof-{slug}/`
- **Note**: Recently posted JDM faculty job on SJDM, confirms active JDM research presence
- **Failed**: JS-rendered needs browser
- **Last verified**: 2026-06-26

#### Hong Kong Baptist University (HKBU)
- **Architecture**: Adobe AEM (main domain) + Pure Portal SPA (scholars portal) + separate infra for comm subdomain
- **Layer**: L3→L4 (Scholars portal blocked, comm subdomain network-unreachable)
- **Access**: Psychology lives within Dept of Education and Psychology (educ.hkbu.edu.hk), NOT standalone psych dept. Also check Business School at busrpg.hkbu.edu.hk.
- **Key endpoint**: https://educ.hkbu.edu.hk/?page_id=20398
- **PhD link**: https://educ.hkbu.edu.hk/?page_id=20338
- **PhD programme (Communication)**: gs.hkbu.edu.hk/programmes/doctor-of-philosophy-master-of-philosophy-school-of-communication
- **Accessible**: gs.hkbu.edu.hk (Grad School), scholars.hkbu.edu.hk (Pure Portal, JS-only for people), hkbu.edu.hk (main domain, Adobe AEM — all guessed URLs return 63KB 404 templates)
- **Blocked**: socsc.hkbu.edu.hk → connection refused; comm.hkbu.edu.hk (SSL timeout — all protocols); scholars portal API (403); scholars portal UUID-based person pages return 31-byte empty shells
- **Note**: HKBU has the strongest communication school in HK.
- **Wayback Machine**: scholars organization page archived (235KB) but person data still JS-rendered in archive
- **Failed**: socsc.hkbu.edu.hk connection refused; browser attempt failed; comm.hkbu.edu.hk SSL timeout
- **Last verified**: 2026-07-01

#### Lingnan University
- **Architecture**: Static HTML (Cultural Studies department accessible; other subdomains may be blocked)
- **Layer**: L1 (Cultural Studies) / L4 (other subdomains — all URLs return 234 bytes)
- **Access (Psychology)**: ln.edu.hk/psy/ — fully accessible via browser; applied/counseling focus
  - Key endpoint: https://www.ln.edu.hk/psy/about-us/people/academic-staff
  - PhD link: https://www.ln.edu.hk/rpg/
- **Access (Cultural Studies)**: ln.edu.hk/cultural/ — direct curl works
  - Key endpoint: https://www.ln.edu.hk/cultural/people/faculty
  - Profile URL: https://www.ln.edu.hk/cultural/people/faculty/prof-{name-slug}
- **Blocked**: ln.edu.hk/daci, ln.edu.hk/visualstudies return 234 bytes; uni-directory returns 404; staffdir.htm too thin
- **Last verified**: 2026-07-01

#### Education University of Hong Kong (EdUHK)
- **Architecture**: Static HTML
- **Layer**: L1 (via browser)
- **Access**: eduhk.hk/ps/en/ for Psychology dept; accessible via browser
- **Key endpoint**: https://www.eduhk.hk/ps/en/aboutus.php?s=our_staff
- **PhD link**: https://www.eduhk.hk/gradsch/
- **Failed**: Previous attempt via network blocked; browser works
- **Last verified**: 2026-06-26

### 🇸🇬 Singapore

#### National University of Singapore (NUS)
- **Architecture**: Static HTML + custom profiles (fass.nus.edu.sg); Full SPA (cde.nus.edu.sg)
- **Layer**: L1 (fass.nus.edu.sg) / L3 (cde.nus.edu.sg)
- **Access**: fass.nus.edu.sg/psy for Psychology; bschool.nus.edu.sg for Business
- **Key endpoint**: https://fass.nus.edu.sg/psy/people/
- **NUS CDE (College of Design & Engineering)**: ALL cde.nus.edu.sg pages return SPA shells (212 chars). Use browser for individual profile verification. Individual staff pages accessible via /me/staff/{slug}/ (NOT /me/people/{slug}/). Example: cde.nus.edu.sg/me/staff/wang-hao-victor/ (slug: wang-hao-victor, NOT wang-hao). Discovery: DDG HTML search "Wang Hao NUS mechanical engineering".
- **Failed**: All CDE subpages return SPA via curl; Bing search returns encrypted URLs
- **Last verified**: 2026-06-30

#### Nanyang Technological University (NTU)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: ntu.edu.sg/sss for Psychology; ntu.edu.sg/business for NBS
- **Key endpoint**: https://www.ntu.edu.sg/sss/about-us/our-people
- **Failed**: —
- **Last verified**: 2026-06-26

#### Singapore Management University (SMU)
- **Architecture**: SITE RESTRUCTURED 2025-2026; old socsc.smu.edu.sg profiles broken. New platform at faculty.smu.edu.sg (JS-rendered, search required).
- **Layer**: L1→L3 (old static → new JS-rendered)
- **Access**: New platform at https://faculty.smu.edu.sg/ (JS-rendered, search required)
- **Key endpoint**: https://faculty.smu.edu.sg/profile/david-chan (confirmed via Google)
- **Failed**: All socsc.smu.edu.sg individual profile URLs now broken
- **Last verified**: 2026-06-26

### 🇲🇴 Macau

#### University of Macau (UM)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: fss.um.edu.mo for Psychology
- **Key endpoint**: https://fss.um.edu.mo/
- **Failed**: —
- **Last verified**: 2026-06-26

#### Macau University of Science and Technology (MUST)
- **Architecture**: Cloudflare WAF
- **Layer**: L3
- **Access**: BLOCKED all automated attempts. No psychology department exists — psych coursework embedded in FHSS.
- **Key endpoint**: —
- **Failed**: curl → 403 (Cloudflare); browser blocked; Google Scholar shows engineering-only decision-making research; Chinese search yields no psych JDM faculty
- **Last verified**: 2026-06-26

### 🇨🇳 Sino-foreign Joint Programs

#### CUHK Shenzhen
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: hss.cuhk.edu.cn for Applied Psychology
- **Key endpoint**: https://hss.cuhk.edu.cn/en/taxonomy/term/21
- **Failed**: —
- **Last verified**: 2026-06-26

##### CUHK(SZ) 环境/双碳方向补充（2026-08-17 验证）
- 理工学院 SSE `sse.cuhk.edu.cn/faculty/{slug}`、公共政策学院 SPP `spp.cuhk.edu.cn/teacher/{id}`、人文社科学院 HSS `hss.cuhk.edu.cn/teacher/{id}`、数据科学学院 SDS `sds.cuhk.edu.cn/teacher/{id}` 均为可抓取静态页；个人网站走 `myweb.cuhk.edu.cn/{slug}`。
- 环境/能源/双碳/公共政策/空间数据相关院系：SSE（能源经济、智能电网）、SPP（能源政策、可持续转型）、HSS（计算可持续、城市学、地理空间分析）、SDS（时空统计）。
- 研究生院 `gs.cuhk.edu.cn/page/16/`（研究型专业列表）、申请 `pgapply.cuhk.edu.cn`。

#### NYU Shanghai
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: shanghai.nyu.edu for Psychology / Neural Science
- **Key endpoint**: https://shanghai.nyu.edu/academics/graduate/phd-programs
- **Failed**: —
- **Last verified**: 2026-06-26

#### HKUST(GZ)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: Hub structure; Society Hub has 4 thrusts (CNCC, FTEC, IPE, UGOD). No behavioral/cognitive science thrust. No Psychology dept.
- **Key endpoint**: https://soch.hkust-gz.edu.cn/
- **Failed**: No psychology/behavioral science thrust area; no relevant department
- **Last verified**: 2026-06-26

##### HKUST(GZ) IPE 学域补充（2026-08-05 验证）
- **IPE 学域教师列表（WordPress 可抓取）**: https://soch.hkust-gz.edu.cn/academics/ipe/faculty/ — 完整 26 人名单，含姓名/职称/邮箱/SPA 个人页链接
- **官方博士招生手册 PDF**: `soch.hkust-gz.edu.cn/wp-content/uploads/2026/04/PhD-in-Innovation-Policy-and-Entrepreneurship_CN-2026-27-Intake-*.pdf` — 权威在招导师名单，与 faculty 列表有出入，优先以此交叉验证
- **facultyprofiles.hkust-gz.edu.cn 全站 SPA**：`?id=X` 与 `/faculty-personal-page/NAME/slug` 两种格式均返回 1522B Loading 壳，WebFetch/curl 均无法确认内容 → 个人主页必须用替代来源
- **替代主页来源（已验证可抓取）**：
  - 官网人员页：`hkust-gz.edu.cn?p=6493/`（Ye Qi 格式）、`/people/slug/` 只覆盖高级管理人员（如 hui-xiong）
  - 个人网站：luoyec.github.io（Luoye Chen）、qianping-ren.com（Qianping Ren）、seonaparklab.github.io（Seona Park CARE lab）、coreyxu.com（Cloudflare 403 但内容可 WebFetch）、personal.hkust-gz.edu.cn/dxie（Danyang Xie）
  - HKUST 官方页：ppol.hkust.edu.hk/people/detail/（Corey Xu、Xun Wu）、aging.hkust.edu.hk（Corey Xu）
  - 前任机构官方页：dbaswiss.ceibs.edu/he_jinyu（Jinyu He，CEIBS）、sece.xmu.edu.my/（Kok Sin Woon，厦大马校兼职）
- **博士申请信息**: IPE 项目页 `pcc.hkust-gz.edu.cn/postgraduate/program-catalog/innovation-policy-and-entrepreneurship-5` + 申请系统 `fytgs.hkust-gz.edu.cn`（WebFetch 可渲染）
- **Last verified**: 2026-08-05

##### HKUST(GZ) 环境/双碳方向补充（2026-08-17 验证）
- 社会枢纽 CNCC/UGOD 教师列表页（WordPress 可抓取，含姓名/职称/邮箱 + facultyprofiles ?id）：
  - CNCC 碳中和与气候变化 `soch.hkust-gz.edu.cn/academics/cncc/faculty/`
  - UGOD 城市治理与设计 `soch.hkust-gz.edu.cn/academics/ugod/faculty/`
- 功能枢纽 SEE 教师页 `funh.hkust-gz.edu.cn/zh/academics/sustainable-energy-and-environment/faculty-members/` 为 SPA（正文 "Loading"），无法抓取名单；SEE 导师个人页可用 facultyprofiles `?id=X`（如郑君瑜 id=243）。
- **facultyprofiles ?id 交叉核对方法**：直接 WebSearch `"[导师名] facultyprofiles.hkust-gz.edu.cn"` 可拿到含真实姓名/职称/邮箱的搜索结果摘要，比抓 SPA 壳可靠；再与 WordPress 学域列表核对 id。
- 注意 UGOD 有同名双条目（Lingbo LIU id=737 与 id=740，仅 740 带邮箱），写表前核对 email 与 id 匹配。

#### BNBU / UIC (北师香港浸会大学, Zhuhai)
- **Architecture**: Static HTML (general) + Vue SPA (FHSS comm department)
- **Layer**: L1 (general) / L3 (FHSS comm)
- **Access**: 9 PhD programs exist but none in psychology. Applied Psychology is undergraduate-only. FHSS Communication department faculty page is hash-routed SPA.
- **Key endpoint**: https://gs.uic.edu.cn/ (graduate school) / https://fhss.bnbu.edu.cn/comm_en/faculty/faculty.htm (comm faculty SPA)
- **Profile URL**: https://fhss.bnbu.edu.cn/comm_en/faculty/faculty.htm#/{username}/en (hash fragment, SPA-rendered)
- **Failed**: No psychology PhD program; behavioral decision research happens in math/stats depts but not a dedicated track; individual HTML pages don't exist for comm (all SPA hash-routed)
- **⚠️ PhD supervision**: UIC is primarily a teaching institution. MPhil/PhD offered through HKBU co-supervision. Assistant Professors may have limited supervision capacity.
- **Last verified**: 2026-07-01

##### BNBU/UIC 环境/数据方向补充（2026-08-17 验证）
- **研究型硕博专业仅 6 个**：计算机科学、概率论与数理统计、生物学、应用数学、传播学、会计学与企业管理（仅博士）。**无环境科学/公共政策独立专业**，环境方向需挂靠"生物学"（生命科学系），空间/统计方向挂靠"概率论与数理统计"。
- 研究生院导师名录页（静态 HTML，含姓名/职称/研究方向/邮箱，可抓取）：
  - `gs.bnbu.edu.cn/graduate/graduate1/yjxyjskc/Probability_and_Mathematical_Statistics.htm`（统计 PMS）
  - 类似 `.../Biology.htm`、`.../Computer_Science.htm` 等
- 教师个人页多为 SPA：`fst.bnbu.edu.cn/xxx/faculty/faculty.htm#/{username}/en`（hash 锚点，抓取只有导航栏）；`staff.uic.edu.cn/{username}/cn` 为旧域名遗留静态页（仍有效但内容为旧版）。写表时优先用 `gs.bnbu.edu.cn` 导师名录页，或 `staff.uic.edu.cn` 旧页 + 备注标注。
- 申请系统 `rpgadmission.bnbu.edu.cn`。

#### Duke Kunshan University
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: Masters-only institution; 5 Master's programs, zero PhD programs
- **Key endpoint**: https://dukekunshan.edu.cn/en/academics/graduate
- **Failed**: No PhD programs of any kind; Duke Durham has relevant programs but DKU does not
- **Last verified**: 2026-06-26

#### UNNC (Nottingham Ningbo)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: No Psychology dept. Business School (NUBS China) has ICBBR (behavioural business research centre).
- **Key endpoint**: https://www.nottingham.edu.cn/en/business/
- **PhD link**: NUBS China PhD available for behavioural economics/consumer behavior route
- **Failed**: No psychology-specific PhD; business school only
- **Last verified**: 2026-06-26

##### UNNC 环境/地理/ESG 方向补充（2026-08-17 验证）
- 理工科学院 FoSE 个人页格式：`nottingham.edu.cn/en/engineering/staffprofile/{slug}.aspx`、`nottingham.edu.cn/en/people/match.aspx?name={slug}`（均可抓取）。地理科学系、建筑与建筑环境系、化学与环境工程系在 FoSE 下。
- 研究门户（Pure，可抓取）：`research.nottingham.edu.cn/en/persons/{slug}`。
- NUBS China 个人页：`nottingham.edu.cn/en/Business/People/Profile.aspx?id={uuid}`。
- 博士申请：`nottingham.edu.cn/en/study-with-us/postgraduate-research/`；申请系统 `oaas.nottingham.edu.cn`。

##### UNNC 语言学/教育学方向补充（2026-09-01 验证，席天凌案例）
- **人文社科学院 → School of Education and English（教育与英语学院）教师列表**：`nottingham.edu.cn/en/humanities-and-social-sciences/education-and-english/people/listing.aspx`（静态 HTML，L1，可 curl；共 3 页，用 `?STFPageIndex=N` 翻页；第 3 页为 Teaching Fellow 教学岗）。
- **博士项目页**：`nottingham.edu.cn/en/course/PHD-FHSS-EES`（教育学/英语 PhD，研究方向含 Applied linguistics、SLA、Intercultural communication、World Englishes、TESOL、Multilingualism 等）。申请流程：先联系导师获同意再正式申请。
- 关键导师（2026-09 在任）：Anwei Feng（Chair Professor 多语教育，明确欢迎博士申请）、Douglas Bell（Prof ESP/EAP/TESOL）、Robert Weekly（AP World Englishes/语言政策）、Derek Irwin（Prof SFL/跨语言）、Dan Shi（AP SFL 英语教育）。
- **排除案例**：Yu Liu（SLA 但用眼动追踪/心理语言学方法 → 学生排除较强认知分析时不可用）；Curtis Green-Eneix（主页明确 "not accepting any new PhD students"）。

#### XJTLU (Xi'an Jiaotong-Liverpool)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: No Psychology dept in HSS (only China Studies, International Studies, Media, Linguistics). IBSS offers PhD in Business.
- **Key endpoint**: https://www.xjtlu.edu.cn/en/academics/schools/ibss
- **Failed**: No psychology department; IBSS business PhD only
- **Last verified**: 2026-06-26

##### XJTLU 环境/城市规划/ESG 方向补充（2026-08-17 验证）
- **研究门户（Pure，全校教师统一入口，可抓取，含研究方向/邮箱）**：`scholar.xjtlu.edu.cn/en/persons/{slug或uuid}`。这是写 XJTLU 导师主页的首选来源。
- 相关院系：理学院健康与环境科学系 HES（大气/温室气体/全球变化）、设计学院城市规划与设计系 UPD（GIS/可持续城市）、IBSS（ESG/供应链/气候计量经济）、人文社科学院中国研究/国际研究（气候政策）。
- 博士申请：`xjtlu.edu.cn/en/admissions/doctoral/how-to-apply`（全年开放，学费9.9万/年）。博士专业含环境科学、商学、城市规划与设计等。

##### XJTLU 语言学/教育学方向补充（2026-09-01 验证，席天凌案例）
- **应用语言学系（Department of Applied Linguistics）中文教研人员列表**：`xjtlu.edu.cn/zh/study/departments/academic-departments/department-of-applied-linguistics/department-staff/academic-staff`（含姓名/职称/研究方向/邮箱，可直接抓取）。⚠️ 英文版同路径为 SPA 壳（只有 "Academic Staff" 标题），用中文版。
- **Pure slug 大小写敏感**：`scholar.xjtlu.edu.cn/en/persons/RiningWei/`、`/BinZou`、`/HongLiu/`、`/TanjunLiu`、`/stevejeaco`、`/zhoulinruan` 均有效；猜测 `binzou`/`hongliu` 小写会 404。
- **博士项目**：`xjtlu.edu.cn/en/study/doctoral/english-culture-and-communication`（PhD English, Culture and Communication，含 applied linguistics、language pedagogy、TESOL、SLA；学位由 University of Liverpool 授予）；另有 `xjtlu.edu.cn/en/study/doctoral/phd-in-education`（PhD Education，由 Academy of Future Education 提供，偏教育管理/教育技术）。
- 关键导师（2026-09 在任）：Rining Wei（副教授，双语教育/TESOL，明确博导+MA TESOL 主任）、Bin Zou（教授，AI语言教学/CALL）、Zhoulin Ruan（教授，SLA/学术写作，⚠️现任副校长，行政岗风险）、Stephen Jeaco（高级副教授 EAP/TESOL/语料库）、Hong Liu（副教授，双语/语码转换，社会+认知双维度）、Tanjun Liu（副教授，语料库，明确欢迎语料库博士）。
- **排除案例**：Darcy Sperlich（心理语言学/形式语言学，主页明确不指导 general language learning and teaching）；Dawei Wei（语言习得+心理语言学 → 学生排除较强认知分析时不可用）；Esther Pascual（语言与认知）。

### 🇳🇿 New Zealand

#### University of Auckland
- **Architecture**: Adobe AEM (www subdomain) + React SPA (profiles subdomain) + Imperva/Incapsula WAF
- **Layer**: L3→L4 (Mostly blocked; dead end for Communication/Advertising/Brand)
- **Media and Screen Studies**: 9 staff found via contact page, ALL film/TV/media studies focus — NOT communication/advertising/brand. Auckland has NO dedicated Communication/Advertising/Brand programme.
- **Accessible**: calendar.auckland.ac.nz (249KB), researchspace.auckland.ac.nz (203KB), arts about/contact page (290-325KB, accessible via curl but names in SPA)
- **Blocked**: profiles.auckland.ac.nz (JS shell 2122B), unidirectory.auckland.ac.nz (0B/SSL error), business school marketing dept (406/Imperva), most dept pages (403/406), all /our-people/ and /staff/ paths (406)
- **ORCID Discovery Method**: Found 16+ Auckland researchers via ORCID keyword search but employment data incomplete. Cross-reference with Google Scholar for verification.
  - `curl "https://pub.orcid.org/v3.0/search/?q=affiliation-org-name:%22University+of+Auckland%22+AND+(keyword:media+OR+keyword:film+OR+keyword:screen)"`
- **Best method**: None working for staff profiles. ORCID fallback yields names but incomplete data.
- **Manual URL** (last resort): https://www.auckland.ac.nz/en/arts/about-the-faculty/school-of-humanities/our-people/contact-an-academic/contact-an-academic-in-media-and-screen-studies.html
- **Failed**: All curl, browser, and search engine approaches exhausted; individual profile pages (SPA shells); GraphQL API; profiles search API
- **Last verified**: 2026-07-01

#### University of Otago
- **Architecture**: Static HTML behind Cloudflare WAF (curl returns 403)
- **Layer**: L3
- **Access**: In-app browser bypasses Cloudflare. Individual profile URLs follow https://www.otago.ac.nz/{dept}/staff/{name-slug} pattern.
- **Key endpoint**: https://www.otago.ac.nz/education/staff (Education) / https://www.otago.ac.nz/marketing/staff (Business School)
- **Failed**: All curl → Cloudflare 403
- **Last verified**: 2026-06-29

#### Victoria University of Wellington (VUW)
- **Architecture**: Hybrid — Squiz CMS for school pages (sim, sam, fhss) with server-rendered staff listings; Angular SPA for /explore/ and people.wgtn.ac.nz
- **Layer**: L1 (static pages) / L3 (Angular SPA profiles)
- **Best method**: School staff pages (e.g., /sam/about/staff) contain server-rendered staff data with data-cy email attributes. Extract emails via `grep -Eo 'data-cy="[^@]+@vuw\.ac\.nz"' | sort -u`. HTML contains embedded JSON in `<script>` tags (`parsedEmails` key) with firstName, lastName, hrOrgUnitName, hrJobTitle, researchInterests, people.wgtn.ac.nz profile links. Use people.wgtn.ac.nz/{username} for individual profile URLs (JS-rendered, content not accessible via curl).
- **Key endpoint**: `https://www.wgtn.ac.nz/sam/about/staff` (368KB server-rendered page) / `https://www.wgtn.ac.nz/fehps/about/our-people/school-of-education` (embedded JSON)
- **Profile URL**: `https://people.wgtn.ac.nz/{email.username}` (e.g., people.wgtn.ac.nz/geoff.stahl) — SPA shell, 4150 bytes
- **Note**: Communication school is under School of Communication, Journalism and Marketing within Wellington School of Business and Government. SoM staff page only shows management professors. Communication-specific page inaccessible (0 bytes). Wayback Machine: comm staff page not archived (2022-2024).
- **Failed**: people.wgtn.ac.nz profiles all return 4150B JS shells; researchers subdomain 404; seftms 404; /communication-studies returns 404; /explore/ pages are Angular SPA
- **Last verified**: 2026-07-01

#### University of Waikato
- **Architecture**: Static HTML staff list + Symplectic/Elsevier JS SPA for individual profiles
- **Layer**: L1 (staff directory) / L2 (Symplectic SPA for individuals)
- **Access**: Get names from static staff page; open Symplectic profiles in browser to verify research content (JS renders research areas).
- **Key endpoint**: https://www.waikato.ac.nz/about/faculties-schools/education/our-staff/
- **Profile URL**: profiles.waikato.ac.nz/{username} (Symplectic SPA, needs browser)
- **Last verified**: 2026-06-29

#### University of Canterbury
- **Architecture**: Modern SPA with redirects
- **Layer**: L1→L3 (redirects to generic study page)
- **Access**: Navigate from main site https://www.canterbury.ac.nz/ then find Education staff links
- **Failed**: Direct URLs redirect to generic study information pages; academic staff page 404; all staff-related URLs dead
- **Last verified**: 2026-06-29

### 🇪🇺 Europe

#### 🇸🇪 Sweden

##### Linköping University (LiU)
- **Architecture**: Employee ID system; JS-rendered profiles
- **Layer**: L3
- **Access**: https://liu.se/en/employee/{employee-id} (IDs are like danva85)
- **Key endpoint**: https://liu.se/en/employee/danva85 (Daniel Västfjäll)
- **Failed**: Employee search by name via URL doesn't work; ID guessing unreliable
- **Last verified**: 2026-06-26

##### Lund University
- **Architecture**: Research portal (portal.research.lu.se) — 403 to curl
- **Layer**: L3
- **Access**: Browser; https://www.nek.lu.se/en/{name} for economics dept
- **Key endpoint**: https://portal.research.lu.se/en/persons/erik-wengstrom
- **Note**: Erik Wengström moved from QUT → Lund
- **Last verified**: 2026-06-26

#### 🇦🇹 Austria

##### University of Vienna
- **Architecture**: German site (doktorat.univie.ac.at) works well; English redirects often 404. UCRIS Pure portal on separate subdomain (behind Cloudflare). u:find JS SPA at ufind.univie.ac.at.
- **Layer**: L2→L3 (UCRIS Pure Portal + DE site works, EN 404s)
- **Access (PhD info)**: Navigate from https://www.univie.ac.at/studium/ → "PhD / Doktorat" → "Zulassung zu Doktorats- und PhD-Studien" → https://doktorat.univie.ac.at/doktoratunivie/zulassung/
- **Access (individual profiles)**: Search Google for "[Name] University Vienna u:find" → find person ID → use `ufind.univie.ac.at/en/person.html?id=XXXX`. Check "Currently not an active member of staff" status on the profile.
- **Key endpoint**: https://doktorat.univie.ac.at/ (DE version) / https://ufind.univie.ac.at/en/person.html?id={numeric_id}
- **Language requirements**: Deutsch- und/oder Englischkenntnisse auf Niveau C1. "Abschlusszeugnisse und optionaler Sprachnachweis" — language certificate is optional, depends on department. For Bildungswissenschaft (Education), English C1 likely sufficient.
- **Failed**: ufind search.html URLs don't work; need direct person ID; UCRIS blocked by Cloudflare; curl 403, browser also blocked by Cloudflare challenge
- **Last verified**: 2026-06-29

##### University of Innsbruck
- **Architecture**: IEZW site protected by Anubis web firewall (v1.25.0)
- **Layer**: L3 (Anubis anti-bot)
- **Access**: Not accessible via automated tools. Manual search needed.
- **Failed**: curl 404 on team pages; browser blocked by Anubis; FODOK search returns 410
- **Last verified**: 2026-06-29

#### 🇨🇭 Switzerland

##### University of Geneva (FPSE)
- **Architecture**: Static HTML with JS enhancements
- **Layer**: L1 (Static HTML for team pages)
- **Access**: curl the SSED research groups page — contains all research group and professor listings in static HTML. Individual profile URLs need browser (JS-rendered).
- **Key endpoint**: https://www.unige.ch/fapse/recherche/ssed
- **Failed**: EN version URL has redirect loop; personal pages may be JS-rendered
- **Last verified**: 2026-06-29

##### University of Basel
- **Architecture**: Static HTML, well-organized German site. English site sometimes 404. Main site (unibas.ch) works but education-specific subdomains (edu.unibas.ch) fail with SSL.
- **Layer**: L1 (main site) + L3 (edu.unibas.ch SSL fails)
- **Access (PhD info)**: Navigate from https://www.unibas.ch/de/Studium.html → "Anmeldung & Zulassung → Zulassung → Doktorat". Key URL: https://www.unibas.ch/de/Studium/Vor-dem-Studium/Bewerbung-Zulassung/Zulassung/Zulassung-zum-Doktorat.html
- **Language requirements**: "Die hauptsächlichen Unterrichtssprachen sind Deutsch und Englisch. Mindestens Niveau C1 gemäss Europäischem Referenzrahmen erwartet." For doctoral programs, specific requirements in faculty Promotionsordnung.
- **Key endpoint (language)**: https://www.unibas.ch/de/Studium/Vor-dem-Studium/Bewerbung-Zulassung/Zulassung/Sprachkenntnisse.html
- **Failed**: curl SSL error on edu.unibas.ch, browser ERR_CONNECTION_CLOSED
- **Last verified**: 2026-06-29

##### University of Bern
- **Architecture**: Static HTML + JS search interface for staff A-Z. Main site works; erz.unibe.ch blocked by browser policy.
- **Layer**: L1-L2 (edu.unibe.ch works, erz.unibe.ch blocked)
- **Access (PhD info)**: Navigate from https://www.unibe.ch/ → "Studies → Doctorate". Key admission page: https://www.unibe.ch/studies/prospective_students/application_and_admission/application_and_admission_for_doctoral_studies/index_eng.html
- **Access (individual profiles)**: Use main site search (unibe.ch/suche/) to find individual professor pages. edu.unibe.ch/ueber_uns/personen_a___z/ has JS search interface (no static listing). Individual URLs at edu.unibe.ch/ueber_uns/personen_a___z/{dept}/prof_dr_{last}_{first}/
- **Language requirements**: Bachelor requires German C1 certificate. Master programs may require English (if English-taught). For doctoral level, requirements specified in faculty Promotionsordnung. General rule: German and English are main languages.
- **Key endpoint**: https://www.unibe.ch/unibe/portal/content/e1006/e15237/e1466586/Zulassungbedingungen_e_26-27_eng.pdf (admission PDF) / edu.unibe.ch/ueber_uns/personen_a___z/ (staff search)
- **Failed**: erz.unibe.ch blocked by browser policy
- **Last verified**: 2026-06-29

#### 🇩🇪 Germany

##### University of Hamburg
- **Architecture**: Static HTML with complex navigation structure. Education faculty (Fakultät für Erziehungswissenschaft) has restructured website. Most English URLs return 404.
- **Layer**: L3 (multiple 404s, navigation needed)
- **Access**: Start from main site (https://www.uni-hamburg.de/) then navigate to "Forschung → Karrierewege". The "Promovieren" link leads to https://www.uni-hamburg.de/forschung/karrierewege.html. Admission requirements at https://www.uni-hamburg.de/campuscenter/bewerbung/promotion.html. Use university person search (Personensuche) from main site — German URLs work better than English.
- **Key discovery path**: DE version works, EN version returns 404 on most sub-pages.
- **Language requirements**: English B2 required; German C1/C2 only for German-language program.
- **Failed**: /en/personal.html → 404; /personen/ → 404; most EW subpages broken
- **Last verified**: 2026-06-29

##### University of Tübingen
- **Architecture**: WiSo Faculty → IfE → Static HTML for department personal pages
- **Layer**: L1 (static Personal/Team pages)
- **Access**: Navigate from https://uni-tuebingen.de/ → "Fakultäten" → "Wirtschafts- und Sozialwissenschaftliche Fakultät" → "Fachbereich Sozialwissenschaften" → "Erziehungswissenschaft" → "Institut". Key personal pages:
  - Sozialpädagogik: .../abteilungen/sozialpaedagogik/personal/
  - Allgemeine Pädagogik: .../abteilungen/allgemeine-paedagogik/personal/
  - Individual profiles: .../institut/team/{name-slug}/
- **Key discovery**: Old URL de/242 returns 404; new path through WiSo Fakultät navigation works. 15 professors across 4 departments.
- **Failed**: Direct old URLs all 404; site completely restructured in 2025/2026
- **Last verified**: 2026-06-29

##### University of Cologne
- **Architecture**: Static HTML. Individual profile pages use numeric IDs, NOT name slugs.
- **Layer**: L1 (static HTML with numeric page IDs)
- **Access**: Search main site (hf.uni-koeln.de/suche/) for professor name → find numeric page ID (e.g., 33878 for Herzmann, 33835 for Proske). Individual URLs: https://www.hf.uni-koeln.de/{numeric_id}
- **Key discovery**: Name-slug URLs like /personen/petra-herzmann/ all return 404. Numeric IDs are the only working format.
- **Failed**: /personen/ directory browsing; /personen/{name}/ all 404; site search returns no JavaScript results in this environment
- **Last verified**: 2026-06-29

##### University of Freiburg (2026-06-30 update)
- **Architecture**: New uni-freiburg.de site (2025/2026 relaunch); old erzwiss domain returns 000/timeout
- **Layer**: L3→L4 (HISinOne getter-protected, site restructured)
- **Key discovery**: `uni-freiburg.link/personensuche` resolves to HISinOne Personensuche which loads publicly ("ohne Anmeldung am System nur öffentlich sichtbare Personen"). BUT: input fields are getter-protected — `Cannot set property value of [object Object] which has only a getter` — preventing any automated form manipulation. Same protection for Vorlesungsverzeichnis semester selector.
- **Working URLs**: Main page (uni-freiburg.de), Personensuche HISinOne (loads), VVZ (loads), Fakultäten overview page (uni-freiburg.de/universitaet/fakultaeten/)
- **Failed**: Erzwiss domain (timeout), search (0 results), philolfak domain (empty page), all faculty sub-pages (404), all form manipulation (getter-protected)
- **German university pattern confirmed**: Personensuche → HISinOne/QIS system, all protected from external automation
- **Last verified**: 2026-06-30

### 🇺🇸 US/Canada

#### Columbia Business School
- **Architecture**: Cloudflare WAF
- **Layer**: L3
- **Access**: Browser ONLY; business.columbia.edu/faculty/people/{name}
- **Key endpoint**: https://business.columbia.edu/faculty/people/eric-johnson
- **Failed**: curl → Cloudflare block
- **Last verified**: 2026-06-26

#### Princeton University
- **Architecture**: Cloudflare WAF (psych.princeton.edu)
- **Layer**: L3
- **Access**: Browser ONLY
- **Key endpoint**: https://psych.princeton.edu/people/elke-weber
- **Note**: Elke Weber moved from Columbia → Princeton
- **Last verified**: 2026-06-26

#### Harvard University — Psychology
- **Architecture**: Mixed; some profile URLs 404
- **Layer**: L3
- **Access**: Personal sites may be more reliable than dept pages
- **Key endpoint**: https://www.joshua-greene.net/ (personal site; dept URL 404)
- **Last verified**: 2026-06-26

#### Carnegie Mellon University — SDS
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: https://www.cmu.edu/dietrich/sds/people/faculty/{name}.html
- **Key endpoint**: https://www.cmu.edu/dietrich/sds/people/faculty/daniel-oppenheimer.html
- **Note**: Carey Morewedge moved from CMU → Boston University Questrom
- **Last verified**: 2026-06-26

#### Boston University — Questrom
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: https://www.bu.edu/questrom/profile/{name}/
- **Key endpoint**: https://www.bu.edu/questrom/profile/carey-morewedge/
- **Last verified**: 2026-06-26

#### McGill University — Psychology
- **Architecture**: Incapsula WAF (blocks all automated access)
- **Layer**: L3
- **Access**: Browser ONLY; mcgill.ca/psychology/{name}
- **Key endpoint**: https://www.mcgill.ca/psychology/ross-otto
- **Failed**: All curl → 403; search blocked; faculty directory 403
- **Last verified**: 2026-06-26

#### Columbia University — Engineering (APAM / IEOR)
- **Architecture**: Cloudflare challenge ("Just a moment..." JS page) on ALL Columbia web properties except `math.columbia.edu` — includes `apam/ieor.columbia.edu`, `engineering.columbia.edu`, and even `www.columbia.edu/~netid` personal pages
- **Layer**: L3
- **Access**: Browser ONLY; 403 challenge ≠ dead link. Verify live URLs via WebSearch (search engines index full content); confirm exact slug from search result URLs
- **2026-07 consolidation**: Engineering profiles moved from department sites to the central directory `www.engineering.columbia.edu/faculty-staff/directory/{slug}` (alias: `engineering.columbia.edu/faculty/{slug}`). Old `apam.columbia.edu/people/{slug}`, `apam/ieor.columbia.edu/faculty/{slug}` 404 in browser. APAM also has new root-level profiles `apam.columbia.edu/{slug}` (e.g. `/liliana-borcea`); APAM directory: `apam.columbia.edu/directory`. Some IEOR profiles still live at `ieor.columbia.edu/faculty/{slug}` (Sigman, Xunyu Zhou, Dieker) — mixed state, prefer the central engineering directory
- **Last verified**: 2026-07-17

#### Columbia University — Mathematics
- **Architecture**: Static HTML (NO WAF — the only Columbia property directly accessible)
- **Layer**: L1
- **Access**: Profile pattern `https://www.math.columbia.edu/people/faculty-by-rank/name/{slug}/` (trailing slash; verified for Corwin/Dubedat/Knizel/Karatzas/Nutz)
- **Note**: Old `/people/directory/name/{slug}` and `/people/directory/char/F/2` paths are dead/redirected. Faculty list: `/people/faculty-by-rank/`. Personal sites `math.columbia.edu/~{name}/` also work (no WAF)
- **Last verified**: 2026-07-17

#### Cornell University — ORIE (Duffield Engineering)
- **Architecture**: Static HTML, site migrated mid-2026
- **Layer**: L1
- **Access**: `https://www.duffield.cornell.edu/people/{slug}/`
- **Key endpoint**: https://www.duffield.cornell.edu/orie/faculty-staff/
- **Note**: Old `orie.cornell.edu/people/{slug}` URLs all 404; old `/faculty-directory/{slug}` and `engineering.cornell.edu/faculty-directory/{slug}` redirect to duffield. Some slugs include middle name: `andreea-c-minca`, `robert-a-jarrow`, `david-alan-goldberg`. Faculty-staff list page doubles as title reference (Professor/Associate/Assistant).
- **Last verified**: 2026-07-17

#### UT Austin — Mathematics
- **Architecture**: Static HTML, directory migrated
- **Layer**: L1
- **Access**: `https://math.utexas.edu/directory/{firstname-lastname}`
- **Note**: Old `/people/faculty-directory/{slug}` redirects to generic `/directory` (soft-404 for individuals); old `www.ma.utexas.edu/component/cobalt/item/...` URLs redirect correctly but are outdated. Faculty list: `https://math.utexas.edu/directory`.
- **Last verified**: 2026-07-17

#### University of Chicago — Statistics vs Mathematics
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: `https://stat.uchicago.edu/people/profile/{slug}/` for Stats appointments ONLY — Math-only faculty (Lawler, Souganidis) 404 there
- **Note**: Math dept personal pages live at `https://math.uchicago.edu/~{name}/` (small static sites, valid). Joint appointments (Gwynne) have stat profiles. `mathematics.uchicago.edu/people/faculty/` is 404 — do not guess it. CAM program: `cam.uchicago.edu` (occasional SSL flakiness, retry).
- **Last verified**: 2026-07-17

#### Stanford University — Mathematics / ICME / MS&E
- **Architecture**: Static HTML + Stanford Profiles (profiles.stanford.edu)
- **Layer**: L1
- **Access**: Faculty list `https://mathematics.stanford.edu/people/faculty-lecturers` (bare `/people` redirects to department-administration, wrong page)
- **Warning**: `profiles.stanford.edu/{firstname-lastname}` matches SAME-NAME people in other departments — e.g. `profiles.stanford.edu/daniel-spielman` is a Radiology professor, NOT the Yale CS Spielman. Always verify the page's stated department before using.
- **Last verified**: 2026-07-17

#### McGill University — Mathematics & Statistics
- **Architecture**: Static HTML (mathstat site, unlike Psychology's Incapsula)
- **Layer**: L1
- **Access**: `https://www.mcgill.ca/mathstat/{slug}` — slug may include middle initial (e.g. `eric-d-kolaczyk`); bare `firstname-lastname` 404s
- **Last verified**: 2026-07-17

#### UCLA — Mathematics
- **Architecture**: Static HTML, NO WAF
- **Layer**: L1
- **Access**: Personal pages `https://www.math.ucla.edu/~{name}/`
- **Trap**: `www.math.ucla.edu/people/ladder/{slug}` profile pages are **soft-404 empty shells** — all return the same ~12KB generic department template (title "UCLA Department of Mathematics", zero personal content) for every slug, real or not. 200 status means nothing here; check page content. Verified shells: cucuringu, andrea-bertozzi, shlyakhtenko, gangbo, killip. Working personal pages: `~mihai/`, `~bertozzi/`, `~shlyakht/` (Shlyakhtenko), `~wgangbo/` (Gangbo), `~killip/`, `~deanna/` (Needell), `seas.ucla.edu/~vandenbe` (Vandenberghe)
- **Last verified**: 2026-07-17

---

## Know-How: People Who Changed Institutions

Record of faculty moves discovered during verification. Check this before assuming a person is at their "known" institution.

| Name | Was at | Now at | When |
|------|--------|--------|------|
| Bahador Bahrami | UCL | LMU Munich + Royal Holloway | 2019 |
| Carey Morewedge | CMU | Boston University Questrom | ~2023 |
| Elke Weber | Columbia | Princeton | ~2023 |
| Yin WU | (listed as HKU) | PolyU | — |
| Ben Newell | UCL/Carleton(误) | UNSW Sydney | — |
| Erik Wengström | QUT | Lund University | ~2024 |
| Warren Mansell | Manchester | Curtin University | — |
| Neil Stewart | Warwick Psychology | Warwick Business School | — |
| Mihai Cucuringu | Oxford Statistics (Assoc Prof) | UCLA Mathematics (full Professor) | 2025-01 |
| Daniel Spielman (CS) | Yale (Sterling Professor, still there) | NOT at Stanford — Stanford profile with same name is a Radiologist | — |
| Maurice Benayoun (莫奔) | CityU SCM (Professor, PhD coordinator) | Nanjing University (Art School, Professor/博导) | 2024 |

**离任导师验证法（2026-08-04）**：怀疑导师已离任时三步交叉验证——
1. WebFetch 穿透 WAF 打开 scholars 主页，显示 "The page does not exist" → 已失效
2. CityU 学术人员目录标注 Visiting/Adjunct Professor → 通常是离任挂名
3. 系级现任教职员列表（如 scm.cityu.edu.hk/people）各分组均无此人 → 确认离任
搜 `"[导师名] 原校 教授"` 可找到新机构页面（南大案例：官网注明"原香港城市大学创意媒体学院教授（2012年至2024年）"）。

## Know-How: URL Quality Gate

After EVERY batch write to Vika, run this scan:

```python
# Generic URL patterns that indicate a dept page, NOT an individual profile
BAD_PATTERNS = [
    '/faculty-members/', '/faculty.html', '/faculty-directory/',
    '/academic-staff/', '/our-people', '/about/faculty',
    '/people'  # unless followed by /name
]
# If 导师主页 matches any BAD_PATTERN, find the individual URL immediately
# If individual URL is JS-rendered, mark in 备注
```

### URL patterns by university (for quick lookup):

| University | Individual profile pattern |
|-----------|--------------------------|
| CUHK Psych | `psy.cuhk.edu.hk/en/people/faculty-members/{slug}.html` |
| PolyU APSS | `polyu.edu.hk/apss/people/academic-staff/prof-{slug}/` |
| NTU SSS | `dr.ntu.edu.sg/cris/rp/rp{id}` |
| SMU (new) | `faculty.smu.edu.sg/profile/{name}` |
| HKU Psych | `psychology.hku.hk/people/{slug}/` |
| HKU Business | `hkubs.hku.hk/people/{slug}/` |
| CityU | `scholars.cityu.edu.hk/en/persons/{name}({uuid})` — use Scholars Portal search first. ⚠️ 离任教授页面会失效（403 壳穿透后 "The page does not exist"），写入后必须 WebFetch 穿透验证 |
| UCL (new) | `profiles.ucl.ac.uk/{id}-{slug}` |
| UNSW | `unsw.edu.au/staff/{slug}` |
| LiU | `liu.se/en/employee/{employeeId}` (IDs like danva85) |
| Lund | `portal.research.lu.se/en/persons/{slug}` |
| McMaster | `experts.mcmaster.ca/people/{initials}` |
| Carleton | `carleton.ca/psychology/people/{slug}/` |

## PhD Program URL Patterns by University

When filling 博士申请信息, prefer department-level Research Postgraduate programme pages over generic graduate school pages. These have program-specific admission requirements and contact details.

| University | Preferred PhD URL Pattern | Example |
|-----------|--------------------------|---------|
| PolyU | Per-department: /{dept}/study/research-postgraduate-programmes/ | AAE works; ISE SPA -> fallback to /gs/prospective-students/research-postgraduate/ |
| CUHK | Per-department: /research-postgraduate-programme/ | www4.mae.cuhk.edu.hk/research-postgraduate-programme/ |
| HKUST | School-level: /academics/research-postgraduate | seng.hkust.edu.hk/academics/research-postgraduate |
| CityU | Per-department: /academic-programmes/master-philosophy-doctor-philosophy/admissions | cs.cityu.edu.hk/en/academic-programmes/.../admissions |
| NUS | Per-department: /graduate/research-programmes/ | cde.nus.edu.sg/me/graduate/research-programmes/ |
| NTU | General: /admissions/graduate | ntu.edu.sg/admissions/graduate |
| HKU | General: /gradsch.hku.hk/prospective_students | SPA - browser needed |

Rule: Always try /{dept}/study/research-postgraduate-programmes/ (PolyU) or /{dept}/research-postgraduate-programme/ (CUHK) first. If SPA/blocked, fall back to the university graduate school page.

Last verified: 2026-06-30

## ORCID Discovery Pattern (Cross-School)

When all other access methods (curl, browser, search engines) are blocked by WAF:
1. Use ORCID API with affiliation filter: `affiliation-org-name:"[University Name]"`
2. Add keyword filters: `AND+(keyword:media+OR+keyword:communication+OR+keyword:advertising)`
3. Resolve ORCID IDs → researcher names via `/v3.0/{orcid}/person`
4. Cross-reference with external knowledge for department confirmation
5. Note: ORCID employment data requires `/v3.0/{orcid}/employments` (separate endpoint)

**Limitations**:
- ORCID records rely on researchers self-filling data — many have NO employment data
- Department affiliation not always recorded
- Cannot verify research fit without employment context

## HISinOne Tree Bypass Pattern (Freiburg Discovery)

HISinOne tree expand controls are `<input type="image">` elements (not `<button>`). All automated click methods blocked:
- `.click()` → method doesn't exist on input[type="image"]
- `dispatchEvent(new MouseEvent('click'))` → JSF ajax handler not triggered
- `getElementById(id).click()` → IDs regenerate per JSF lifecycle
- Playwright `locator.click()` → selector can't find dynamic tree elements

**Workaround for manual operator:**
1. Navigate to https://uni-freiburg.link/vvz
2. Select semester (e.g., Sommersemester 2026)
3. Expand "1.6 Philosophische Fakultät" by clicking ▶ arrow in browser
4. Browse child departments for Erziehungswissenschaft

This pattern applies to ALL German universities using HISinOne (Freiburg, Göttingen, partially Frankfurt).

## Dead End Diagnosis (exhaustive for Student B, 2026-06)

| School | Last Attempt | Barrier | Manual Bypass |
|--------|-------------|---------|---------------|
| Göttingen | eCampus HISinOne VL catalog | JS-rendered zero-content page; person search needs HRZ login | Google: "Erziehungswissenschaft Professor Uni Göttingen" |
| Frankfurt | QIS/LSF person tab | Needs HRZ login; old site 404 | Google: "Erziehungswissenschaft Professor Goethe Uni Frankfurt" |
| Freiburg | New site search / Fakultäten nav | Full site restructure (all old URLs 404); search returns 0 results; Fakultäten page 404 | Google: "Erziehungswissenschaft Professor Uni Freiburg" |
| Innsbruck | Anubis v1.25.0 anti-bot | Full site WAF; FODOK search returns 410 | Google: "IEZW Innsbruck Professor" |
| Bern | edu.unibe.ch Personen A-Z | JS-only search UI with no accessible API | Google: "Institut für Erziehungswissenschaft Uni Bern Professor" |
| Lausanne | SSP main page | No education-specific prof directory under SSP | Google: "sciences de l'éducation professeur UNIL" |
| Canterbury | Academic staff page | 404; all staff-related URLs dead | Google: "Education lecturer University of Canterbury" |

## Vika School IDs (in dstMNzQU9Aa58DpgW3)

| University | Record ID |
|-----------|----------|
| The University of Melbourne | reco6LXk2RdNg |
| The University of Sydney | recSCi2HYh18f |
| UNSW Sydney | recupYqG8sNJD |
| Australian National University | recd2grjzT9Vf |
| Monash University | recTyuPatx4kC |
| The University of Queensland | recPsoUbww7Zr |
| The University of Western Australia | recr6NH4J8ZxM |
| The University of Adelaide | recMJr4zMuQw8 |
| UTS | recx6JttsSALF |
| RMIT University | rec8y6BX5nvqK |
| Macquarie University | recys0of2k2QN |
| The University of Newcastle | recNh5iNGwa8V |
| Curtin University | recY5NYqlEXX0 |
| Deakin University | recP7hhnKGdHw |

### Melbourne findanexpert URL Pattern Updates (2026-07-01)

**DISCOVERY**: findanexpert.unimelb.edu.au has TWO URL patterns:

| Pattern | Behavior | Status |
|---------|----------|--------|
| `/display/person-{slug}` | Returns 200 SPA shell for **ANY** slug (even non-existent professors) | ❌ BROKEN - cannot verify existence |
| `/profile/{id}/{slug}` | Returns 200 SPA shell for **REAL** profiles only, 404 for fake ones | ✅ CORRECT - has unique profile ID |

**Profile ID discovery**: Each professor has a unique numeric profile ID. The `/profile/{id}/{slug}` URL contains this ID. These IDs can be found by:
- Searching via browser on findanexpert
- Checking Semantic Scholar for profile URLs
- Using the sub-agent approach that worked on 2026-07-01

**Verified profile IDs** (2026-07-01):
- Alan Pert: `/profile/11727/alan-pert`
- Sofia Prado: `/profile/52639/sofia-prado`
- Julie Willis: `/profile/4492/julie-willis`
- Amanda Achmadi: `/profile/48121/amanda-achmadi`
- Sidh Sintusingha: `/profile/66045/sidh-sintusingha`
- Gini Lee: `/profile/66008/gini-lee`
- Margaret Grose: `/profile/14457/margaret-grose`
- Andrew Saniga: `/profile/66248/andrew-saniga`

**David Beynon counter-example**: His `/display/person-david-beynon` returned the same SPA shell, but he's actually at University of Tasmania (UTAS), NOT Melbourne. The `/display/` endpoint accepts any slug and never returns 404 — it's a catch-all route in the React SPA.

**Lesson**: NEVER use the `/display/` endpoint for verification. Always find the `/profile/{id}/` URL. If you can't find the profile ID, mark the record as ⚠️学校归属未验证.

**Cloudflare WAF**: All findanexpert URLs return "Pardon Our Interruption" via curl (6183 bytes). They work correctly in browser. Same situation as UNSW staff pages.

#### Griffith University (2026-07-14)
- **Architecture**: Pure Portal (experts.griffith.edu.au)
- **Layer**: L1 (WebFetch accessible, full HTML content with research interests, supervision records, tags)
- **Best method**: WebSearch "[Name] Griffith University professor" → WebFetch the experts.griffith.edu.au profile page. Teaching tab shows PhD supervision details.
- **Key endpoint**: `https://experts.griffith.edu.au/{id}-{slug}/about` and `/teaching` for supervision records
- **Staff directory**: `https://www.griffith.edu.au/arts-education-law/griffith-law-school/staff`
- **PhD info**: `https://www.griffith.edu.au/apply/research-study`
- **Failed**: —
- **Last verified**: 2026-07-14

#### University of Tasmania (2026-07-14)
- **Architecture**: Pure Portal (discover.utas.edu.au)
- **Layer**: L1→L3 (profile about pages return "Discovery" SPA shell in some cases; teaching tab pages load with full supervision content)
- **Best method**: WebSearch → WebFetch `/teaching` subpage (not `/about`) for supervision records. Alternative: utas.edu.au profiles.
- **Key endpoint**: `https://discover.utas.edu.au/{Name}/teaching` for supervision; `https://discover.utas.edu.au/{Name}/about` may return SPA shell
- **Staff directory**: `https://www.utas.edu.au/law/people`
- **PhD info**: `https://www.utas.edu.au/research/degrees`
- **Note**: Dianne Nicol is Emeritus, not taking new students
- **Failed**: discover.utas.edu.au about pages inconsistent (some SPA shell, some load)
- **Last verified**: 2026-07-14

#### La Trobe University (2026-07-14)
- **Architecture**: Static HTML staff list + scholars.latrobe.edu.au Pure Portal
- **Layer**: L1 (staff listing page) / L3 (scholars portal profiles)
- **Best method**: Use latrobe.edu.au/law/staff for staff list (full HTML). scholars.latrobe.edu.au for individual profiles. LawTech page at latrobe.edu.au/cybersecurity/expertise/lawtech lists key tech-law faculty.
- **Key endpoint**: `https://www.latrobe.edu.au/law/staff` (staff list); `https://scholars.latrobe.edu.au/display/{username}` (individual)
- **PhD info**: `https://www.latrobe.edu.au/research/graduate-research/apply`
- **Failed**: scholars portal individual about pages may return minimal content
- **Last verified**: 2026-07-14

#### Swinburne University of Technology (2026-07-14)
- **Architecture**: Pure Portal (experts.swinburne.edu.au)
- **Layer**: L1 (WebFetch accessible, shows "Available to supervise Doctorate (PhD)" flag clearly)
- **Best method**: WebSearch → WebFetch experts.swinburne.edu.au profile; supervision availability clearly indicated
- **Key endpoint**: `https://experts.swinburne.edu.au/{id}-{slug}/about`
- **Staff directory**: `https://www.swinburne.edu.au/business-law/our-people/`
- **PhD info**: `https://www.swinburne.edu.au/course/research/doctor-of-philosophy-law/`
- **Note**: Dan Hunter (founding dean) has left — now at QUT/King's College London
- **Failed**: —
- **Last verified**: 2026-07-14

#### Western Sydney University (2026-07-14)
- **Architecture**: Pure Portal (researchers.westernsydney.edu.au)
- **Layer**: L1 (WebFetch accessible)
- **Best method**: WebSearch → WebFetch researchers.westernsydney.edu.au profile
- **Key endpoint**: `https://researchers.westernsydney.edu.au/en/persons/{slug}`
- **Staff directory**: `https://www.westernsydney.edu.au/schools/sol/key-people` (research-clusters page returned 406, 2026-07-15)
- **PhD info**: `https://www.westernsydney.edu.au/schools/sol/research/higher_degree_research` (406 on curl, WebFetch OK)
- **Failed**: research-clusters page (406), key-people is the correct staff directory
- **Last verified**: 2026-07-15

#### University of Canberra (2026-07-14)
- **Architecture**: Pure Portal (researchprofiles.canberra.edu.au)
- **Layer**: L1 (WebFetch accessible, shows "Accepting PhD Students" flag)
- **Best method**: WebSearch → WebFetch researchprofiles.canberra.edu.au profile; PhD acceptance status clearly shown
- **Key endpoint**: `https://researchprofiles.canberra.edu.au/en/persons/{slug}`
- **Staff directory**: `https://researchprofiles.canberra.edu.au/en/organisations/school-of-law-and-justice/persons/` (Pure Portal, 403 on curl but accessible via browser)
- **PhD info**: `https://www.canberra.edu.au/future-students/apply-to-uc/research-applications`
- **Note**: UC offers Professional Doctorate in Legal Science (Research) rather than traditional PhD; verify program type with student. Old staff dir `school-of-law-and-justice` returned 404 (2026-07-15).
- **Failed**: Older profile URLs at canberra.edu.au/research/... may 404
- **Last verified**: 2026-07-15

#### Flinders University (2026-07-14)
- **Architecture**: Static HTML + Pure Portal (researchnow.flinders.edu.au)
- **Layer**: L1
- **Best method**: WebSearch → PhD program page lists key supervisors with research areas
- **Key endpoint**: `https://www.flinders.edu.au/study/courses/doctor-philosophy-phd-law/` (lists supervisors)
- **PhD info**: `https://www.flinders.edu.au/study/courses/doctor-philosophy-phd-law/`
- **Note**: Law faculty small; no IP specialist. Vivienne Brand (corp gov + AI) and Marinella Marmo (transnational crime) are listed PhD supervisors. Robert Chalmers (IP + tech law) has personal page but no HDR supervision section — email to confirm PhD supervision eligibility.
- **Failed**: —
- **Last verified**: 2026-07-15

#### Bond University (2026-07-15)
- **Architecture**: SharePoint for staff profiles (bond.edu.au/staff → SharePoint login wall)
- **Layer**: L3 (all individual staff pages behind SharePoint; research.bond.edu.au Pure Portal for profiles)
- **Best method**: WebSearch → research.bond.edu.au profile pages; manual browser for staff directory
- **Key endpoint**: `https://research.bond.edu.au/en/persons/{id-slug}`
- **Staff directory**: `https://bond.edu.au/about-bond/academia/faculty-law/academic-staff/forum` (static HTML, verified)
- **PhD info**: `https://bond.edu.au/researchers/research-degrees/higher-degree-options/how-apply-hdr`
- **Note**: Bond profiles show "Accepting PhD Students" flag on research portal. Staff directory at bond.edu.au/staff just links to SharePoint login.
- **Failed**: bond.edu.au/nz/profile/... returns generic SharePoint directory; bond.edu.au/profile/... returns Access Denied
- **Last verified**: 2026-07-15

#### University of Southern Queensland (UniSQ) (2026-07-15)
- **Architecture**: Static HTML staff profiles + Pure Portal (research.usq.edu.au)
- **Layer**: L2 (staff profiles accessible, research portal has captcha)
- **Best method**: WebSearch → staffprofile.unisq.edu.au profile (bot protection may intermittently block); research.usq.edu.au researcher pages (captcha on automated access)
- **Key endpoint**: `https://staffprofile.unisq.edu.au/Profile/{name}` (bot protection, works in browser)
- **Staff directory**: `https://www.unisq.edu.au/about-unisq/schools/school-of-law-and-justice`
- **PhD info**: `https://www.unisq.edu.au/research/higher-degree-by-research/apply`
- **Note**: Eugenia Georgiades is Associate Professor (IP + privacy + cybersecurity), currently supervising 2 doctoral students. Staff profiles may intermittently block automated access.
- **Failed**: staffprofile.unisq.edu.au/departmentstaff/{id} → 404; research portal has captcha
- **Last verified**: 2026-07-15

#### Victoria University (2026-07-15)
- **Architecture**: Pure Portal (vuir.vu.edu.au) + Drupal CMS
- **Layer**: L1
- **Best method**: WebSearch → vu.edu.au profile pages
- **Key endpoint**: `https://www.vu.edu.au/about-vu/our-people/{slug}`
- **Staff directory**: `https://www.vu.edu.au/node/11362361` (Victoria Law School page, general — not a staff listing)
- **PhD info**: `https://www.vu.edu.au/node/10890586` (vu.edu.au/research/graduate-research returned 404, 2026-07-15)
- **Note**: Two strong IP/AI law supervisors: Christina Tao (IP + AI + legal tech) and Yongqiang Li (IP + disruptive tech, Mandarin speaker). Both have PhD supervision availability.
- **Failed**: vu.edu.au/research/graduate-research → 404; no dedicated law school staff listing page found
- **Last verified**: 2026-07-15

#### Charles Darwin University (2026-07-15)
- **Architecture**: Pure Portal (researchers.cdu.edu.au) + Drupal CMS
- **Layer**: L2 (some researcher pages accessible, others 404)
- **Best method**: WebSearch → cdu.edu.au or researchers.cdu.edu.au pages (unstable, URLs may change)
- **Key endpoint**: `https://researchers.cdu.edu.au/en/persons/{slug}/` (intermittently 404, 2026-07-15)
- **Staff directory**: `https://researchers.cdu.edu.au/en/organisations/law/` (10 staff listed)
- **PhD info**: `https://www.cdu.edu.au/research/research-degrees/how-apply`
- **Note**: Jenny Ng listed as "Registered to supervise postgraduate research" on researchers portal (RD3) but page 404 on RD4 recheck. CDU researchers portal highly unstable. Small law faculty, limited IP/criminal law specialists.
- **Failed**: cdu.edu.au/staff-directory → 404; cdu.edu.au/law → 404; cdu.online subdomain exists but non-standard
- **Last verified**: 2026-07-15

#### CQUniversity (2026-07-15)
- **Architecture**: Acquire repository (acquire.cqu.edu.au) + sportal staff pages
- **Layer**: L2 (acquire portal unstable, sportal requires login)
- **Best method**: WebSearch → acquire.cqu.edu.au author pages (may 404); sportal.cqu.edu.au as fallback
- **Key endpoint**: `https://acquire.cqu.edu.au/authors/{name}/{id}` (intermittently 404)
- **Staff directory**: `https://www.cqu.edu.au/about-us/our-schools/business-law/staff` (formerly `/about-us/school-business-law/staff` → 404 on 2026-07-15)
- **PhD info**: `https://www.cqu.edu.au/research/higher-degree/applying-for-a-hdr`
- **Note**: Amanda-Jane George (Senior Lecturer + Postgraduate Research Coordinator, IP + AI + patent law) has PhD from UQ and thesis cited by Australian High Court, but personal page on acquire.cqu.edu.au returns 404.
- **Failed**: acquire.cqu.edu.au author page → 404; my.cqu.edu.au/login → internal login portal; cqu.edu.au/apply → generic admission (not HDR)
- **Last verified**: 2026-07-15

#### Southern Cross University (SCU) (2026-07-15)
- **Architecture**: Standard university CMS
- **Layer**: L1
- **Best method**: WebSearch → scu.edu.au staff pages
- **Key endpoint**: N/A (only Lecturer-level law staff found)
- **Staff directory**: N/A
- **PhD info**: N/A
- **Note**: Law staff primarily Lecturer level; Brendon Murphy (Professor of Law, 2024) has no personal page URL on SCU site. Not recommended for PhD supervision targets.
- **Failed**: No suitable PhD supervisors found
- **Last verified**: 2026-07-15

#### Edith Cowan University (ECU) (2026-07-15)
- **Architecture**: Standard university CMS
- **Layer**: L1
- **Best method**: WebSearch → ecu.edu.au staff pages
- **Key endpoint**: N/A (only AI regulation / criminology staff found, no IP or criminal law doctrine specialists)
- **Staff directory**: N/A
- **PhD info**: N/A
- **Note**: ECU law school focuses on AI regulation and criminology/policing; Anne Wallace (former professor) has moved to La Trobe as Adjunct. No IP or pure criminal law doctrine supervisors found.
- **Failed**: No suitable PhD supervisors found
- **Last verified**: 2026-07-15

## AU Schools Access Layer Summary (2026-07-01)

| University | Architecture/CMS | Layer | Access Method | Key Endpoint / Profile URL Pattern |
|-----------|-----------------|-------|---------------|-------------------------------------|
| Melbourne | Pure Portal v5.x (React SPA) | L3 | Individual profile pages via findanexpert (browser required; Cloudflare WAF on curl) | findanexpert.unimelb.edu.au/profile/{id}/{slug} |
| Sydney | Symplectic Elements SPA | L3 | profiles.sydney.edu.au/{username} (SPA shell, 2118 bytes) | profiles.sydney.edu.au/{firstname}.{lastname} |
| UNSW | Adobe AEM (staff pages OK) | L2 | unsw.edu.au/staff/{slug} → real HTML content | unsw.edu.au/staff/{slug} |
| ANU | Pure Portal v5.x (React SPA) | L3 | React shell for all pages; individual titles contain researcher name in meta | researchers.anu.edu.au/researchers/{id-slug} |
| Monash | Pure Portal v5.x | L1 | research.monash.edu.au/en/persons/ accessible via web | research.monash.edu.au/en/persons/{name}/ |
| UQ | Drupal/UQ Experts (Numeric ID) | L3 | about.uq.edu.au/experts/{id} → real HTML but no name in URL | about.uq.edu.au/experts/{numeric_id} |
| UWA | Pure Portal (research-repository) | L3 | research-repository.uwa.edu.au/en/persons/{name}/ → SPA | research-repository.uwa.edu.au/en/persons/{name}/ |
| Adelaide | Pure Portal v5.x | L3 | researchers.adelaide.edu.au/profile/{name} → SPA | researchers.adelaide.edu.au/profile/{firstname}.{lastname} |
| UTS | UTS Profiles (SPA) + Cloudflare | L3 | Cloudflare/Imperva blocks all curl; browser required | profiles.uts.edu.au/{Firstname}.{Lastname}/about |
| RMIT | Pure Portal (academics) + Cloudflare | L3 | Cloudflare WAF blocks all curl; browser required | academics.rmit.edu.au/{name-slug} |
| Macquarie | Pure Portal (researchers) | L2 | researchers.mq.edu.au/en/persons/{id} → SPA | researchers.mq.edu.au/en/persons/{id} |
| Curtin | React SPA (staffportal) | L0-SPA | Use personal sites + ResearchGate + research center pages | tamaleaver.net, wishcrys.com, digitalchild.org.au |
| Wollongong | Symplectic Elements | L3 | scholars.uow.edu.au/{name}/about → SPA | scholars.uow.edu.au/{firstname}-{lastname}/about |
| Newcastle | Staff profiles | L2 | Staff profiles may be accessible | newcastle.edu.au/profile/{slug} |
| Deakin | Pure Portal SPA + Cloudflare | L3 | experts.deakin.edu.au/{slug} → SPA; Cloudflare blocks CMS | experts.deakin.edu.au/{slug} |
| Bond | SharePoint staff + Pure Portal research | L3 | research.bond.edu.au profiles accessible; staff pages behind SharePoint login | research.bond.edu.au/en/persons/{id-slug} |
| UniSQ | Static staff profiles + Pure Portal | L2 | staffprofile.unisq.edu.au (bot protection intermittent); research portal has captcha | staffprofile.unisq.edu.au/Profile/{name} |
| Victoria University | Pure Portal + Drupal | L1 | vu.edu.au profile pages accessible; old research/graduate-research URL → 404 | vu.edu.au/node/10890586 |
| CDU | Pure Portal (unstable) + Drupal | L2 | researchers.cdu.edu.au profiles intermittently 404; small law faculty | researchers.cdu.edu.au/en/persons/{slug}/ |
| CQU | Acquire repository + sportal | L2 | acquire.cqu.edu.au pages unstable; sportal requires login | acquire.cqu.edu.au/authors/{name}/{id} |
| SCU | Standard CMS | L1 | Only Lecturer-level law staff; no PhD supervisors found | — |
| ECU | Standard CMS | L1 | AI regulation/criminology focus; no IP or criminal law doctrine supervisors | — |

---

#### University of Missouri
- **Architecture**: Custom CMS (CAFNR WordPress-style personal pages) + static Graduate Studies/Graduate School pages + catalog PDF
- **Layer**: L1/L3
- **Access**: Use `https://gradstudies.missouri.edu/degreecategory/animal-sciences` for current Animal Sciences PhD policy; use `https://gradschool.missouri.edu/funding/assistantships` for school-wide assistantship minimums; find individual CAFNR profiles through the official directory/search, with Amy Petry's verified personal page at `https://cafnr.missouri.edu/?p=84800`; supplement supervision with the official lab graduate-team page and the Animal Sciences catalog PDF's `Doctoral Faculty` marker
- **Key endpoint**: `https://cafnr.missouri.edu/?p=84800`
- **Failed**: `https://cafnr.missouri.edu/?p=80267` for Hong Jo Lee returns Page not found; do not treat an old `?p=` URL as valid without reading page content. School-wide assistantship amounts are minimum standards, not evidence of a specific faculty offer.
- **Last verified**: 2026-08-25

#### Texas Tech University
- **Architecture**: Static HTML department pages with individual faculty pages; catalog pages supplement policy
- **Layer**: L1
- **Access**: Current PhD page and faculty directory are directly readable. Individual faculty pages provide title and research focus. Use the PhD page for deadlines, advisor requirement, concentrations and GRE wording.
- **Key endpoint**: https://www.depts.ttu.edu/afs/programs/phd-animal-science.php
- **Failed**: The current PhD page simultaneously lists a GRE score expectation and a COVID temporary waiver; no current page located here states that the waiver applies to 2027 Fall.
- **Last verified**: 2026-08-25

#### West Virginia University
- **Architecture**: Static catalog plus Davis College CMS; some individual faculty pages are CloudFront-protected
- **Layer**: L1/L3
- **Access**: Use the current catalog page for 2027-28 admissions, GRE and research/funding mechanism. Use Davis College news for current faculty activity and doctoral supervision evidence. Joseph Moritz's individual profile URL is discoverable but WebFetch returned a CloudFront 403.
- **Key endpoint**: http://catalog.wvu.edu/graduate/daviscollegeofagricultureandnaturalresources/afns
- **Failed**: https://www.davis.wvu.edu/faculty-staff/directory/joseph-moritz returned a CloudFront 403; do not treat the 403 alone as proof of a valid page or use it as closed evidence.
- **Last verified**: 2026-08-25

#### University of Nevada, Reno
- **Architecture**: Static PhD page, graduate handbook and mixed static faculty profiles
- **Layer**: L1/L3
- **Access**: Use `https://www.unr.edu/degrees/animal-and-rangeland-science/phd` for the current ARS advisor list, Feb. 1 fall full-consideration deadline and GRE policy; use `https://www.unr.edu/avrs/graduates/handbook-x313496` for advisor-support and assistantship conditions; use NRES/EECB individual profiles for wildlife research. The current ARS advisor list does not include Kelley Stewart.
- **Key endpoint**: https://www.unr.edu/degrees/animal-and-rangeland-science/phd
- **Failed**: Kelley Stewart's official profile and lab evidence cannot substitute for ARS advisor-list membership; Paul Meiman's official profile does not state PhD supervision.
- **Last verified**: 2026-08-25

#### South Dakota State University
- **Architecture**: Static program and directory pages, catalog supplement, official news
- **Layer**: L1
- **Access**: Use `https://www.sdstate.edu/programs/graduate/animal-science-phd` for current program scope and `https://www.sdstate.edu/directory/philip-urso` for the official individual profile. The profile includes research areas, current appointment, graduate-relevant grants and publications. Official bison news confirms a current graduate-student team but not 2027 recruitment.
- **Key endpoint**: https://www.sdstate.edu/directory/philip-urso
- **Failed**: The official catalog page returned an empty 202 response in WebFetch; use the current program page plus the official personal profile instead. No public 2027 Fall recruitment or guaranteed assistantship was found.
- **Last verified**: 2026-08-25

#### Florida State University — Department of Urban & Regional Planning
- **Architecture**: Static HTML / WordPress-style departmental pages; current faculty and program pages are directly readable. Graduate Guide is available as a PDF and search results expose useful text, but direct PDF extraction is less stable than the HTML pages.
- **Layer**: L1, with WebSearch fallback for individual faculty and doctoral-supervision evidence.
- **Access**: Use the current DURP pages at `cosspp.fsu.edu/durp/` for the Doctoral Program, Admissions, FAQ, Financial Aid, and Faculty pages. Use WebSearch to locate individual faculty pages and official student-supervisor pages. The official Graduate School homepage is useful for university-level term availability but explicitly says to confirm open terms and deadlines with the department.
- **Key endpoints**: `https://cosspp.fsu.edu/durp/doctoral-program/`; `https://cosspp.fsu.edu/durp/Admissions/?q=Environmental-Planning`; `https://cosspp.fsu.edu/durp/?p=781`; `https://cosspp.fsu.edu/durp/financial-aid/`; `https://cosspp.fsu.edu/durp/faculty/`; `https://gradschool.fsu.edu/`.
- **Failed / limits**: Do not treat Graduate School Fall 2027 acceptance as proof that DURP has opened a specific Fall 2027 PhD cohort. DURP does not publish a doctoral assistantship dollar amount on the current pages; do not convert the Graduate School minimum GA rate into a program-specific annual stipend. The Graduate Guide PDF may be used as supporting evidence, but current HTML pages take priority when versions conflict.
- **Last verified**: 2026-08-25

#### University of Colorado Boulder — Department of Geography
- **Architecture**: Static HTML / Colorado.edu CMS; faculty profiles and program pages directly readable.
- **Layer**: L1, with WebSearch fallback for doctoral-supervision evidence.
- **Access**: Use `colorado.edu/geography` for program pages and faculty profiles. Graduate admissions page confirms no GRE required since 2021. PhD requires Master's degree. Application requires listing at least one faculty advisor (up to 4); applicants must contact potential advisors before deadline (December 1). Department reviews applications then remaining faculty provide advisor matching input; faculty must agree to serve as advisor before admission is granted.
- **Key endpoints**: `https://colorado.edu/geography/node/2026` (admissions domestic); `https://www.colorado.edu/geography-ma-phd` (degrees overview); `https://colorado.edu/geography/grad-program/graduate-curriculum/graduate-admissions` (admissions criteria); `https://catalog.colorado.edu/graduate/colleges-schools/arts-sciences/programs-study/geography/geography-doctor-philosophy-phd/` (catalog).
- **Faculty profiles**: Emily Yeh (`https://www.colorado.edu/geography/emily-yeh-0`); Mara Goldman (`https://www.colorado.edu/geography/mara-goldman-0`).
- **Failed / limits**: Department does not publish specific doctoral assistantship dollar amount. Funding page references assistantships but no fixed stipend figure. PhD requires 6 semesters residence (4 at CU). Language requirement: one foreign language.
- **Last verified**: 2026-08-26

#### University of Arizona — School of Geography, Development & Environment
- **Architecture**: Static HTML / Drupal CMS; program and faculty pages directly readable. Profiles at `profiles.arizona.edu` and `geography.arizona.edu` both accessible.
- **Layer**: L1, with WebSearch fallback for doctoral-supervision evidence.
- **Access**: Use `geography.arizona.edu` for program and faculty pages. Official admissions page explicitly states "The School does not request scores from the GRE." PhD requires Master's degree. Fall deadline January 5. Assistantship approximately $17,000 for 9 months (two main semesters) plus tuition waiver; typically supported for at least 4 years with 20 hrs/week TA/RA work.
- **Key endpoints**: `https://geography.arizona.edu/node/106` (admissions); `https://geography.arizona.edu/` (home); `https://profiles.arizona.edu/person/agerlak` (Andrea Gerlak); `https://water.cals.arizona.edu/node/105` (Margaret Wilder).
- **Failed / limits**: Diana Liverman retired in May 2022, explicitly not recruiting new students. Do not list as current advisor. No specific dollar amount published beyond the ~$17,000/9-month reference.
- **Last verified**: 2026-08-26

#### Ohio State University — Department of Geography
- **Architecture**: Static HTML / OSU Drupal CMS; faculty profiles and program pages directly readable.
- **Layer**: L1, with WebSearch fallback for doctoral-supervision evidence.
- **Access**: Use `geography.osu.edu` for program and faculty pages. Official FAQ page (`geography.osu.edu/grad/questions`) explicitly states "We do not need to submit your GRE scores. We do not require GRE scores for application to our graduate programs." PhD has direct-to-PhD option (Bachelor's can apply); deadline November 15. Graduate Program page lists relevant faculty (Kendra McSweeney, Harvey Miller, Bryan Mark, Madhumita Dutta) but this list is incomplete for the full human geography faculty. Human Geography cluster covers Political Ecology, Feminist Political Ecology, Human-Environment Geography but specific faculty advisor pages needed.
- **Key endpoints**: `https://geography.osu.edu/grad/questions` (FAQ, GRE); `https://geography.osu.edu/geography-graduate` (program overview); `https://geography.osu.edu/people/wainwright.11` (Joel Wainwright); `https://geography.osu.edu/people/mcsweeney.14` (Kendra McSweeney); `https://sexualitystudies.osu.edu/people/mansfield.32` (Becky Mansfield, Director of Graduate Studies).
- **Failed / limits**: PhD requires Master's degree for direct admission (but Bachelor's can apply via direct-to-PhD track). No specific doctoral assistantship dollar amount published. Relevant Faculty list on grad page only shows 4 faculty, not the full human geography faculty. PhD admission criteria page (`geography.osu.edu/minimum-admission-criteria-phd-geography`) states Master's required for PhD admission — direct-to-PhD may be limited; verify with program. Becky Mansfield's main profile is at `sexualitystudies.osu.edu` (not geography.osu.edu).
- **Last verified**: 2026-08-26

#### University of Georgia — Department of Geography
- **Architecture**: Static HTML / UGA Drupal CMS; faculty directory and program pages directly readable. Student directory pages also directly accessible.
- **Layer**: L1, with WebSearch fallback for doctoral-supervision evidence.
- **Access**: Use `geography.uga.edu` for program and faculty pages. Official prospective students page explicitly states "The Department of Geography is not currently requiring the GRE." GIS applicants are encouraged to add GRE. Fall deadline December 1. ICON PhD requires GRE separately (separate from regular Geography PhD). Department covers climate studies, environmental change, food systems, social movements for climate and racial justice, environmental justice.
- **Key endpoints**: `https://geography.uga.edu/prospective-students` (admissions, GRE policy); `https://www.geography.uga.edu/directory` (full faculty directory); `https://www.geography.uga.edu/directory/people/nik-heynen` (Nik Heynen, Distinguished Research Professor); `https://www.geography.uga.edu/directory/people/steve-holloway` (Steve Holloway); `https://www.geography.uga.edu/directory/people/amy-trauger` (Amy Trauger — verify current status, external info suggests moved to University of Guelph).
- **Failed / limits**: No specific doctoral assistantship dollar amount published. Amy Trauger's external profile suggests she may have moved to University of Guelph as Canada Research Chair; verify before listing as UGA advisor. Marshall Shepherd is primarily atmospheric sciences / meteorology.
- **Last verified**: 2026-08-26

#### University of Washington — Department of Geography
- **Architecture**: Static HTML / UW Drupal CMS; faculty profiles and program pages directly readable. Department ranking US top 10.
- **Layer**: L1, with WebSearch fallback for doctoral-supervision evidence.
- **Access**: Use `geography.washington.edu` for program and faculty pages. Official admissions page and handbook both confirm "GRE no longer required as of autumn 2020." PhD application requires listing at least two faculty members whose work aligns with the applicant's research interests. Deadline December 15 for Autumn Quarter admission. Funding: department awards 15–20 TAships per academic year with tuition waiver. Graduate program covers critical development and poverty studies, racial capitalism, labor geographies, political ecologies, feminist and queer geographies, carceral and abolition geographies, urban/social/political geographies.
- **Key endpoints**: `https://geography.washington.edu/apply-graduate-program` (admissions, GRE policy, deadline); `https://geography.washington.edu/graduate-programs` (program overview, research areas); `https://geography.washington.edu/people` (full faculty directory); `https://geography.washington.edu/people/jen-rose-smith` (Jennifer Rose Smith, environmental justice, Indigenous geographies).
- **Failed / limits**: No specific doctoral assistantship dollar amount published. PhD requires listing multiple faculty mentors — no single-advisor model. PhD applicants should contact potential advisors before December 15 deadline. Department research areas are broad; individual advisor fit must be verified per faculty page.
- **Last verified**: 2026-08-26

#### University of Colorado Denver — College of Architecture and Planning
- **Architecture**: Static HTML / CU Denver Drupal CMS; program and faculty pages directly readable. College of Architecture and Planning pages accessible at `architectureandplanning.ucdenver.edu`; GES faculty pages at `clas.ucdenver.edu/ges/`.
- **Layer**: L1, with WebSearch fallback for doctoral-supervision evidence.
- **Access**: Use `architectureandplanning.ucdenver.edu` for PhD program pages. Official admissions page explicitly states "GRE scores are not required for admission." PhD requires Master's degree. Deadline January 15 (domestic) / December 15 (international). Funding is strong: "nearly all accepted students receive multi-year financial packages that cover some or all tuition and fees and a living stipend." Four Areas of Emphasis: Community Planning & Place, Human-Environment Interactions, Sustainability and Social Justice, Technology Engagement & Design.
- **Key endpoints**: `https://architectureandplanning.ucdenver.edu/admissions/phd` (admissions, GRE policy, funding); `https://architectureandplanning.ucdenver.edu/academics/phd-in-geography-planning-and-design` (program overview); `https://clas.ucdenver.edu/ges/node/223` (Gregory Simon, political ecology, Director of Graduate Studies); `https://news.ucdenver.edu/?p=149731` (PhD achievements, PhD student advisor assignments).
- **Failed / limits**: The PhD is administered by College of Architecture and Planning, not Geography alone — check CAP faculty (not just GES). No specific stipend dollar amount published beyond "living stipend." PhD students draw from 35+ faculty across 11 departments; advisor matching occurs after admission.
- **Last verified**: 2026-08-26

#### University of Missouri Columbia — Department of Geography (NO PhD)
- **Finding**: The Department of Geography at University of Missouri Columbia offers only a M.A. in Geography (and a GIS Graduate Certificate). The Graduate School page for Mizzou Geography confirms "GRE scores optional" but only lists an M.S. program, not a PhD. The PhD in Geosciences at Mizzou Kansas City is a separate institution (UMKC), focused on physical sciences (geophysics, atmospheric science, geochemistry, etc.), not human geography or political ecology.
- **Layer**: L1 confirmed — no PhD in Geography at Mizzou Columbia.
- **Action**: Do not add as a candidate for human geography / political ecology PhD.
- **Last verified**: 2026-08-26

#### University of Kansas — Department of Geography & Atmospheric Science
- **Architecture**: Static HTML / KU Drupal CMS; catalog and department pages directly readable. Note: Graduate application procedure page at `geog.ku.edu/node/238` still lists "Graduate Record Examination (GRE) scores. All students applying for admission must submit official GRE scores" while the academic catalog at `catalog.ku.edu` says "GRE scores are not required." This discrepancy needs clarification — treat as potentially GRE-required until confirmed.
- **Layer**: L1 with discrepancy flag.
- **Access**: Priority deadline January 15 for fall admission with funding; final deadline March 3. Faculty research areas include human geography (cultural-regional geography, political ecology), GIScience, and physical geography. Shannon O'Lear (environmental geopolitics, South Caucasus) is a relevant human geography faculty member. Alexander Diener (Central Asia geopolitics) and Jay T. Johnson (Indigenous geographies, qualitative methods) also relevant.
- **Key endpoints**: `https://catalog.ku.edu/liberal-arts-sciences/geography/phd-geography` (catalog, no GRE); `https://geog.ku.edu/node/238` (application procedure, GRE required); `https://geography.ku.edu/people` (faculty directory); `https://esp.ku.edu/people/shannon-olear` (Shannon O'Lear, environmental geopolitics).
- **Failed / limits**: GRE policy discrepancy between catalog (no GRE) and department application page (GRE required) must be resolved before treating as no-GRE candidate. No specific PhD funding amount published. South Caucasus focus of Shannon O'Lear differs from Southeast Asia preference.
- **Last verified**: 2026-08-26

#### University of Nebraska-Lincoln — Department of Geography (EXCLUDED)
- **Finding**: Petersons clearly lists GRE General Test required for Geography PhD. No alternative UNL PhD program in human geography or environmental studies was found with GRE-optional status.
- **Layer**: L1 confirmed — GRE required is hard exclusion.
- **Action**: Do not add as candidate.
- **Last verified**: 2026-08-26

#### University of Maryland, College Park — Department of Geographical Sciences (EXCLUDED)
- **Architecture**: Static HTML / UMD Drupal CMS; degree-requirements page directly readable.
- **Finding**: Official degree-requirements page at `geog.umd.edu/degree-requirements` explicitly states "GRE verbal score of 160 (600 paper based test) with a good quantitative score of 148 or better (600 paper based test)." Hard GRE requirement; faculty sponsor required for admission. Focus is on Geographical Sciences with Human Dimensions of Global Change, but GRE is a hard block.
- **Layer**: L1 confirmed — GRE required is hard exclusion.
- **Key endpoints**: `https://geog.umd.edu/degree-requirements`
- **Action**: Do not add as candidate.
- **Last verified**: 2026-08-26

#### University of Illinois Chicago — Urban Planning and Policy PhD (EXCLUDED)
- **Architecture**: Static HTML / UIC Drupal CMS.
- **Finding**: ACSP member profile (acsp.org) and Petersons both explicitly state "Doctoral Minimum GRE Score: General required." ACSP page adds "GRE can be substituted with GMAT" — which effectively means GRE is still required. Hard exclusion.
- **Layer**: L1 confirmed — GRE required is hard exclusion.
- **Key endpoints**: `https://www.acsp.org/member/uppatuic`
- **Action**: Do not add as candidate.
- **Last verified**: 2026-08-26

#### University of Texas at Austin — Department of Geography and the Environment (EXCLUDED)
- **Architecture**: Static HTML / UT Austin CMS.
- **Finding**: Petersons and third-party application sources clearly list "GRE General Test" as entrance exam requirement for both MA and PhD (combined verbal+math ≥ 320). Official UT Austin catalog has PhD degree requirements but no published GRE waiver policy. Hard GRE requirement; UT Austin is ranked US News #32 but excluded due to mandatory GRE.
- **Layer**: L1 confirmed — GRE required is hard exclusion.
- **Key endpoints**: `https://liberalarts.utexas.edu/geography/graduate-program/`; `https://catalog.utexas.edu/graduate/areas-of-study/liberal-arts/geography/`
- **Action**: Do not add as candidate.
- **Last verified**: 2026-08-26

#### University of Nebraska-Lincoln — School of Global Integrative Studies PhD (PENDING)
- **Architecture**: Static HTML / UNL Drupal CMS; `graduate.unl.edu` and `globalstudies.unl.edu` both directly readable.
- **Layer**: L1.
- **Access**: Official PhD page at `graduate.unl.edu/academics/programs/GIST-PHD` states "GRE (optional)" — explicitly marked optional. Priority deadline January 1. TA assistantships: $15,000 + tuition remission, competitive basis, up to 3 years. The program is housed in the School of Global Integrative Studies (SGIS), which also houses Anthropology and Global Studies. Geography faculty (Urban and Political Geography, Human-Environment Relations, Cultural Geography) are affiliated with this school after the 2020 reorganization. Faculty listing at `geography.unl.edu` still shows faculty but may not be updated post-SGIS reorganization.
- **Key endpoints**: `https://graduate.unl.edu/academics/programs/GIST-PHD`; `https://globalstudies.unl.edu`; `https://geography.unl.edu`
- **Failed / limits**: Geography faculty specialization in human-environment/political ecology needs individual verification. No specific Fall 2027 admission confirmation published. Advising relationship with Geography faculty needs verification. TA is competitive (not guaranteed), max 3 years.
- **Next step**: Verify whether UNL Geography faculty (particularly those in human-environment/political ecology) are actively supervising GIST PhD students and are accepting new students for Fall 2027.
- **Last verified**: 2026-08-26

#### University of Kansas — Department of Geography PhD (EXCLUDED)
- **Finding**: KU Geography PhD confirmed to exist. Catalog confirms GRE not required (optional). However, PhD focus areas are cultural-regional geography, GIScience, and physical/environmental geography — no political ecology, environmental governance, or environmental policy. No relevant faculty identified.
- **Layer**: L1 confirmed — GRE not required but wrong sub-field concentration.
- **Key endpoints**: `https://geog.ku.edu/geography-phd`; `https://catalog.ku.edu/liberal-arts-sciences/geography/phd-geography/`
- **Action**: Do not add as candidate.
- **Last verified**: 2026-08-26

#### Kansas State University — Department of Geography and Geospatial Sciences PhD (REVIEWED)
- **Architecture**: Static HTML / K-State Drupal CMS; catalog and FAQ both directly readable.
- **Access**: Official FAQ explicitly states GRE not required. Fall 2027 domestic deadline Feb 8; international deadline Jan 2. GTA/GRA competitive, stipend + full tuition waiver, typically 3 years (up to 4).
- **Faculty**: Audrey Joslin (Associate Professor, Graduate Program Director): political ecology + environmental governance + conservation + market-based initiatives + Latin America (Ecuadorian Andes + Great Plains), qualitative and mixed methods. Marcellus Caldas (Professor, Interim Dept Head): environmental economic-geographer, land use science, deforestation, human-environment interactions, teaches GEOG 837 Political Ecology of Land Cover Change — modeling component present. Matt Sanderson: political economy/ecology + development + environment — Sociology primary affiliation.
- **Failed / limits**: Joslin sabbatical Fall 2025; PhD supervision evidence not yet confirmed via personal page (page failed to load full content). Caldas uses quantitative land cover modeling. Sanderson primary affiliation is Sociology.
- **Key endpoints**: `https://www.k-state.edu/geography/academics/graduate/faq.html`; `https://www.k-state.edu/geography/people/faculty`; `https://catalog.k-state.edu/preview_entity.php?catoid=47&ent_oid=5029`
- **Next step**: Verify Joslin PhD supervision evidence and Fall 2027 admission; verify Caldas PhD student supervision history.
- **Last verified**: 2026-08-26

#### University of Kentucky — Department of Geography PhD (REVIEWED)
- **Architecture**: Static HTML / UK Drupal CMS; geography.as.uky.edu faculty directory and graduate-degrees alumni page both directly readable.
- **Access**: Official admissions page explicitly states "GRE scores are NOT required." Deadline January 15. Graduate-degrees alumni page confirms PhD graduates exist.
- **Faculty**: Nari Senanayake (Associate Professor): health-environment geography + political ecology + feminist geographies + agrarian livelihoods + South Asian studies. Alumni page shows 2024 PhD (Nethmi Bathige: Feminist Political Ecology + Climate Resilient Agriculture + Sri Lanka) and 2025 PhD (Aylin Castro: Climate Justice) supervised by Senanayake. 2025 Summer Stipends Award. Active project "Agro-ecological transition at scale and as health?" (OVPR Curate Program). Betsy Beymer-Farris (Assistant Professor, Director of ENS/AES): political ecology + gender + climate change + East Africa (Tanzania). Tad Mutersbaugh (Professor): political ecology + sustainability certifications + agrarian studies + Latin America. Alicia Barceinas Cruz (Assistant Professor): political ecology + borders + migration + transnational livelihoods + environmental justice + Latin America.
- **Failed / limits**: Geography.as.uky.edu faculty pages for most professors returned minimal content. Primary PhD supervision evidence source is graduate-degrees alumni page. Beymer-Farris is Assistant Professor (2020 PhD), PhD supervision evidence weak. Mutersbaugh region focus is Latin America. Nick Lally (digital geographies + policing) excluded.
- **Key endpoints**: `https://geography.as.uky.edu/admissions`; `https://geography.as.uky.edu/graduate-degrees-alumni`; `https://www.as.uky.edu/users/tmute2`; `https://is.as.uky.edu/users/aba568`; `https://research.uky.edu/kentucky-climate-consortium/members/betsy-beymer-farris`
- **Next step**: Verify Nari Senanayake Fall 2027 admission status; verify Beymer-Farris PhD supervision evidence; clarify UK Geography PhD project structure.
- **Last verified**: 2026-08-26

#### University of Iowa — Department of Geography PhD (REVIEWED)
- **Architecture**: Static HTML / Iowa Drupal CMS; sees.uiowa.edu faculty profiles directly readable.
- **Access**: Official grad.admissions.uiowa.edu page explicitly states "GRE scores are not required for this program." Deadline December 31.
- **Faculty**: Silvia Secchi (Associate Professor): climate adaptation + conservation policy + water sustainability + agricultural environmental impacts. PhD supervision alumni confirmed (McClain 2016, Bhattarai 2016, Teshager 2016). Uses integrated modeling methods (modeling component noted — needs tradeoff discussion with student). Heather Sander, Margaret Carrel, Matt Dannenberg, Jessica Meyer, Kate Tierney all excluded (ecosystem science, health disparities, remote sensing, hydrogeology).
- **Failed / limits**: Secchi modeling component may conflict with student's qualitative preference. PhD supervision evidence is historical alumni, not current students. Fall 2027 admission not confirmed.
- **Key endpoints**: `https://sees.uiowa.edu/people/silvia-secchi`; `https://grad.admissions.uiowa.edu/`
- **Next step**: Verify Secchi current PhD student supervision and Fall 2027 admission status.
- **Last verified**: 2026-08-26

#### University of Louisville — Urban and Public Affairs PhD (EXCLUDED)
- **Finding**: Official catalog states "This program is not accepting applications for admission during the 2026-27 academic year." Hard exclusion.
- **Layer**: L1 confirmed — program not open.
- **Action**: Do not add as candidate.
- **Last verified**: 2026-08-26

#### Purdue University — EAPS and ESE PhD Programs (EXCLUDED)
- **Finding**: EAPS PhD requires GRE minimum 300; ESE PhD requires GRE minimum 300 and is engineering/biology-focused; Geography department offers no PhD. Three hard exclusions.
- **Layer**: L1 confirmed — GRE required + wrong sub-field.
- **Action**: Do not add as candidate.
- **Last verified**: 2026-08-26

#### North Carolina State University — Geospatial Analytics PhD (EXCLUDED)
- **Finding**: NCSU Geography dept restructured into Geospatial Analytics PhD. GRE optional. Funding strong ($30,000–$37,500 stipend + tuition waiver + insurance, up to 4 years). But program explicitly requires "Computational/quantitative background, including applied statistics and math, quantitative research methods, computer programming (R and/or Python)". Core courses include GIS 710 Remote Sensing, GIS 712 Geospatial Data Mining. Typical PhD projects involve PNNL flood monitoring + ML time series, NASA/NOAA internships. Data science / computational focus. Incompatible with Guo's preference for qualitative/mixed methods.
- **Layer**: L1 confirmed — wrong sub-field orientation.
- **Action**: Do not add as candidate.

#### Oregon State University — Geography and Environmental Sciences PhD (REVIEWED)
- **Architecture**: CEOAS static HTML; faculty directory at ceoas.oregonstate.edu/directory-units.
- **Access**: CEOAS officially dropped GRE requirement for all graduate programs. Deadline December 15. Assistantships include salary + tuition + health insurance.
- **Faculty**: David Wrathall (Associate Professor): political ecology + climate hazards + climate change adaptation + social vulnerability + migration; **explicitly states "Accepting for advising"** on official directory page; IPCC AR6 WGII Chapter 8 Lead Author. Kelsey Emard (Assistant Professor): political ecology + sustainable rural livelihoods + environmental risk and justice + climate resilience + Central America; teaches GEOG 514 Political Ecology + GEOG 333 Environmental Justice. Hannah Gosnell (Professor): environmental governance + water resource policy/management/law + rural land use change. Demian Hommel (Associate Professor of Teaching): political ecology + climate justice + environmental security.
- **Key endpoints**: `https://ceoas.oregonstate.edu/future-graduate-students`; `https://ceoas.oregonstate.edu/directory-units`; `https://ceoas.oregonstate.edu/directory/david-wrathall`; `https://www.geo.orst.edu/directory/kelsey-emard`
- **Failed / limits**: Wrathall sabbatical/administrative leave status unknown; PhD supervision evidence needs confirmation.

#### Washington State University — School of the Environment PhD in ENRS (REVIEWED)
- **Finding**: PhD in Environmental & Natural Resource Sciences. GRE waived until further notice. Deadline January 10. Must secure faculty advisor's consent before applying.
- **Faculty**: Hannah Hämmerli (Assistant Professor): political ecology + political economy + sustainable development + water governance and policy + institutional change + national and transboundary hydropolitics; co-authored with Andrea Gerlak (UArizona) on "Reimagining Hydropower in the United States" (WIREs Water 2024). Other faculty predominantly biology/ecology/wildlife/geoscience.
- **Key endpoints**: `https://environment.wsu.edu/graduate-studies/phd/`; `https://environment.wsu.edu/people/faculty/`
- **Failed / limits**: Most faculty biology/ecology/wildlife oriented. Hämmerli's PhD supervision evidence not yet confirmed.

#### Northern Arizona University — PhD in Earth Sciences & Environmental Sustainability, Environment & Society emphasis (EXCLUDED)
- **Finding**: PhD program confirmed. Environment & Society emphasis matches Guo's direction (environmental policy, political ecology, water governance, climate change adaptation, environmental sociology). Funding attractive ($20,000–$27,000 stipend + tuition + health insurance). Deadline January 1. But third-party sources (phdportal.com, mastersportal.com) explicitly state "GRE Required". NAU official program page does not clearly state GRE waiver. Hard exclusion rule: GRE required → exclude.
- **Key endpoints**: `https://in.nau.edu/ses/phd-program-in-earth-sciences-environmental-sustainability/`; `https://in.nau.edu/school-earth-sustainability/environment-society`
- **Failed / limits**: GRE required (third-party); could not confirm from official NAU source.

#### University of New Mexico — PhD in Geography (UNM-NMSU Joint) (REVIEWED)
- **Architecture**: UNM Geography static HTML; faculty profiles at geography.unm.edu/people/faculty/faculty-profiles/.
- **Access**: Official page grad.unm.edu/graduate-programs/application-instructions/geography-phd.html and geographyphdnmsu.unm.edu/admissions/admissions.html both confirm "GRE scores are no longer required" / "The Department does not require GRE scores". Deadline January 15. Assistantships include GTA/GRA + tuition waiver + health insurance. Applicants must contact potential advisors first.
- **Faculty**: Benjamin Warner (Associate Professor): development geography + water governance and institutions + Central American development (dry corridor) + agrarian adaptation + vulnerability/risk/adaptation to climate change + political economy of climate adaptation programs + mixed methods. Marygold Walsh-Dilley (Associate Professor): political ecology + food/agricultural systems + rural development + modernity/coloniality + agrarian change + climate vulnerability + qualitative methods + Andes. Both highly relevant to Guo. Chris Lippitt (Professor): remote sensing + GIScience — wrong sub-field.
- **Key endpoints**: `https://geography.unm.edu/`; `https://geography.unm.edu/people/faculty/index.html`; `https://geography.unm.edu/people/faculty/faculty-profiles/benjamin-warner.html`; `https://geography.unm.edu/people/faculty/faculty-profiles/marygold-walsh-dilley.html`; `https://grad.unm.edu/graduate-programs/application-instructions/geography-phd.html`
- **Failed / limits**: Warner and Walsh-Dilley PhD supervision evidence not yet confirmed; Fall 2027 availability unknown.

#### University of Oklahoma — PhD in Geography and Environmental Sustainability (REVIEWED)
- **Architecture**: DGES static HTML at geography.ou.edu; faculty directory at ou.edu/ags/geography/people/faculty.
- **Access**: Official FAQ ou.edu/mcee/geosciences/academics/graduate-programs/graduate-programs-faq.html confirms "No, the GRE is not required". Deadline January 15 (Funding), April 1 (international no funding). GTA/GRA + tuition waiver + health insurance. Must contact advisor before applying. Curriculum includes "Interpreting Society and Environment: Qualitative Research Methods".
- **Faculty**: Lauren Mullenbach (Assistant Professor): urban environmental justice + climate adaptation planning + green space + gentrification + wellbeing. Diana Denham (Assistant Professor): Indigenous geographies + socio-environmental movements. Most other faculty are GIS, hydrology, climatology, ecology — wrong sub-field.
- **Key endpoints**: `https://ou.edu/mcee/geosciences/academics/graduate-programs/graduate-programs-faq.html`; `https://geography.ou.edu/`; `https://ou.edu/ags/geography/research`
- **Failed / limits**: Mullenbach and Denham PhD supervision evidence not yet confirmed; Fall 2027 availability unknown.

#### University of Colorado Colorado Springs — Geography & Environmental Studies (EXCLUDED)
- **Finding**: UCCS GES department offers only MA in Applied Geography and MA in Cultural Heritage and Environmental Resource Management. No PhD program. GRE no longer required for MA. Hard exclusion rule: no PhD → exclude.
- **Key endpoints**: `https://www.uccs.edu/geography/ba-general-information`; `https://ges.uccs.edu/letter-to-prospective-students`
- **Failed / limits**: —
- **Last verified**: 2026-08-26

#### University of Missouri — PhD in Natural Resources (EXCLUDED)
- **Finding**: Department of Geography at MU offers only M.A. (no PhD). PhD in Natural Resources exists with emphasis areas including Human Dimensions of Natural Resources and Water Resources. GRE recommended but not required. Human Dimensions area explicitly requires mixed methods (qualitative + quantitative). Water Resources area is explicitly natural science-oriented (hydrology, water quality, biogeochemistry). MU catalog does not list specific social-environmental faculty names for these emphasis areas. Insufficient evidence of relevant political ecology / environmental governance faculty to justify inclusion.
- **Key endpoints**: `https://catalog.missouri.edu/collegeofagriculturefoodandnaturalresources/naturalresources/phd-natural-resources/`; `https://catalog.missouri.edu/collegeofagriculturefoodandnaturalresources/naturalresources/phd-natural-resources-emphasis-human-dimensions-natural-resources/`; `https://snr.missouri.edu/graduate-studies/`
- **Failed / limits**: No PhD in Geography; relevant social-environmental faculty not identifiable from catalog pages.
- **Last verified**: 2026-08-26

#### University of Nevada Reno — PhD in Geography (REVIEWED)
- **Architecture**: Static HTML; faculty profiles at unr.edu/geography/{name-slug}.
- **Access**: Official page geography.unr.edu confirms "GRE Scores - recommended, not required". Deadline December 15. Master's degree required. Assistantships include GTA/GRA + tuition waiver + health insurance. Applicants must contact potential advisors first.
- **Faculty**: Jessie Clark (Associate Professor, Graduate Program Director): feminist geography + political geography + cultural geography + qualitative methods + Middle East; official page directly states "Please contact me by email if you are interested in advising opportunities". Kate Berry (Professor): water governance + Indigenous geographies + cultural politics of water + environmental justice + legal geographies + geographies of racialization; official page unr.edu/geography/kate-berry confirms research focus; publishes interdisciplinary water governance papers (Wiley WIREs Water). Both highly relevant to Guo.
- **Key endpoints**: `https://geography.unr.edu/`; `https://geography.unm.edu/people/faculty/index.html`; `https://www.unr.edu/people/faculty/berry` (verified working as of 2026-08-26); `https://geography.unr.edu/people/faculty/jessie-clark`; `https://www.unr.edu/geography`
- **Failed / limits**: Clark and Berry PhD supervision evidence not yet confirmed; Fall 2027 availability unknown.

#### University of South Carolina — PhD in Geography (REVIEWED)
- **Architecture**: Static HTML on sc.edu; faculty profiles at sc.edu/study/colleges_schools/artsandsciences/earth_ocean_and_environment/our_people/directory/{name}.php and sc.edu/study/colleges_schools/artsandsciences/geography/our_people/faculty/.
- **Access**: Official application page explicitly states "Please do not submit GRE scores; they will not be reviewed by the admissions committee" (GRE not required). **Fall 2027 is formally open**, Deadline December 1, 2026. Master's degree required. TA/RA limited; PhD stipend $21,000/9 months covers tuition + health insurance.
- **Faculty**: Dean Hardy (Assistant Professor, joint appointment Geography + SEOEO): environmental justice + political ecology + climate change + sea level rise + flood risk + mixed methods (spatial analyses, interviews, participant observation); official sc.edu page confirms research focus. SEOEO additional relevant faculty: David Fuente (water and sanitation policy, East Africa/Middle East/South Asia); Jessica Barnes (sustainable development, Columbia PhD background); Conor Harrison (political economy of energy). Geography department faculty (Kirstin Dow, Meredith DeBoom, Carl Dahlman) research areas not yet fully verified.
- **Key endpoints**: `https://sc.edu/study/colleges_schools/artsandsciences/geography/our_people/`; `https://sc.edu/study/colleges_schools/artsandsciences/earth_ocean_and_environment/our_people/directory/hardy_dean.php` (verified working as of 2026-08-26); `https://sc.edu/study/colleges_schools/artsandsciences/earth_ocean_and_environment/our_people/`
- **Failed / limits**: Hardy PhD supervision evidence not yet confirmed; Fall 2027 availability unknown; SEOEO faculty Geography PhD advisor eligibility unverified.

#### University of Nevada Las Vegas — Geoscience PhD (EXCLUDED)
- **Finding**: catalog.unlv.edu explicitly states "Satisfactory scores on the general Graduate Record Examination (GRE)" — GRE required. Hard exclusion rule: GRE required → exclude.
- **Key endpoints**: `https://catalog.unlv.edu/content.php?catoid=39&catoid=39&coid=162615`
- **Failed / limits**: —
- **Last verified**: 2026-08-26

#### University of Memphis — Earth Sciences PhD (EXCLUDED)
- **Finding**: catalog.memphis.edu explicitly states "The GRE (Graduate Record Exam) is not required" (GRE not required confirmed). Fall Deadline Jan 31; Funding deadline Jan 1; requires 32 credit hours background knowledge in geology, geography, archaeology, or environmental sciences. However, faculty research areas are dominated by physical/earth sciences (hydrogeology, geomorphology, archaeology, seismology, biogeography). No faculty found in political ecology, environmental governance, environmental justice, rural development, or climate adaptation. Hard exclusion rule: no relevant human geography faculty → exclude.
- **Key endpoints**: `https://www.memphis.edu/earthsciences/`; `https://www.memphis.edu/earthsciences/faculty_people/index.php`; `https://catalog.memphis.edu/content.php?catoid=25&coid=14485`
- **Failed / limits**: faculty_people page URL changed (2026-08-26 site redesign); faculty list now at memphis.edu/earthsciences/faculty_people/index.php
- **Last verified**: 2026-08-26

#### University of Arkansas — Geosciences PhD (EXCLUDED)
- **Finding**: catalog.uark.edu explicitly states "GRE (Verbal, Quantitative, and Writing) will be reviewed on a competitive basis" and Graduate School page states "satisfactory scores on the Graduate Record Examination (GRE)" — GRE required. Hard exclusion rule: GRE required → exclude.
- **Key endpoints**: `https://catalog.uark.edu/graduate/catalog/`
- **Failed / limits**: —
- **Last verified**: 2026-08-26

#### University of North Dakota — ESSP PhD (Earth System Science & Policy) (EXCLUDED)
- **Finding**: No Geography PhD at UND; the ESSP PhD (Earth System Science & Policy) is the closest doctoral program. ESSP core courses include ESSP 503 Environmental Policy Science, ESSP 504 The Biosphere, ESSP 505 Energy Issues and Earth Systems, ESSP 506 Atmosphere and Climate Systems, ESSP 507 Earth System Modeling — all science/earth system oriented. No faculty in political ecology, environmental governance, environmental justice, rural development, or qualitative methods. GRE status unclear (Peterson's says required; UND Graduate School official page does not explicitly require GRE), but direction mismatch is sufficient grounds for exclusion regardless of GRE policy.
- **Key endpoints**: UND Graduate School homepage; UND ESSP requirements page (via search)
- **Failed / limits**: GRE policy ambiguous (Peterson's vs official); direction完全不匹配，无需闭合。
- **Last verified**: 2026-08-26

#### University of Nebraska Omaha — M.S. Geography only (EXCLUDED)
- **Finding**: UNO Department of Geography offers only M.S. in Geography (no PhD). Official UNO website confirms no doctoral program in Geography. Hard exclusion rule: no PhD program → exclude.
- **Key endpoints**: `https://www.unomaha.edu/college-of-arts-and-sciences/geography/` (official UNO Geography department)
- **Failed / limits**: —
- **Last verified**: 2026-08-26

#### University of Texas at San Antonio — No Geography PhD (EXCLUDED)
- **Finding**: UTSA itself offers only M.A. in Geography and Environmental Sustainability (no PhD in Geography). The "Geography PhD at Texas State" discovered in search (gradcollege.txst.edu) belongs to Texas State University, not UTSA. UTSA and Texas State are separate institutions. Hard exclusion rule: no PhD program → exclude.
- **Key endpoints**: UTSA official Geography page; Texas State University graduate catalog (separate institution)
- **Failed / limits**: —
- **Last verified**: 2026-08-26

#### University of Wisconsin Milwaukee — Geography PhD (EXCLUDED — RANKING HARD LIMIT)
- **Finding**: UWM Geography PhD exists; official Graduate FAQ explicitly states "GRE scores are waived until further notice" (GRE not required, supersedes Peterson's outdated "required" listing). However, UWM U.S. News National Universities ranking is #301 — far outside the 50-100 target range. Hard exclusion rule: ranking → exclude.
- **Faculty note**: Ryan Holifield (Professor): urban political ecology + environmental justice + environmental governance + qualitative methods (NSF-funded WaterMarks project on Milwaukee water systems); Anne Bonds (Professor): critical geography + racial justice + urban politics; Rina Ghose (Professor): critical GIS + urban geography + political economy. All three align well with the student's research interests, but ranking hard limit overrides.
- **Key endpoints**: `https://uwm.edu/geography/graduate/graduate-faq/` (GRE waived confirmed); `https://uwm.edu/geography/about/directory/?_people_categories_facet=faculty` (faculty directory); `https://usnews.com/best-colleges/wi` (UWM #301 national universities)
- **Failed / limits**: PhD supervision evidence and Fall 2027 availability not investigated due to ranking hard exclusion.
- **Last verified**: 2026-08-26

#### University of Texas Arlington — No Geography PhD (EXCLUDED)
- **Finding**: UTA has History PhD (GRE not required) under the "Department of History and Geography," but no doctoral program in Geography. The department offers only undergraduate Geography courses (GEOG 2301 Physical Geography, GEOG 2302 Human Geography, etc.) and a Geography minor. The 2021-2022 archived catalog confirms "History, M.A." and "History, Ph.D." as the only graduate Geography-related degrees. Hard exclusion rule: no PhD in Geography → exclude.
- **Key endpoints**: `https://catalog.uta.edu/liberalarts/history` (current catalog); `https://www.uta.edu/academics/schools-colleges/liberal-arts/departments/history/study-with-us/graduate/phd/admissions` (History PhD admissions)
- **Failed / limits**: —
- **Last verified**: 2026-08-26

#### Colorado State University — PhD in Anthropology (EXCLUDED — RANKING + DISCIPLINE HARD LIMIT)
- **Finding**: CSU Department of Anthropology and Geography offers a **PhD in Anthropology** (Place, Space & Adaptation), not a Geography PhD. Geography faculty participate by "apply geographic methods to anthropological questions" — the degree conferred is Anthropology. GRE is **OPTIONAL** (official page: "OPTIONAL: GRE General Test scores"; Peterson's "required" is outdated and ignored). U.S. News National Universities ranking is **#151** — far outside the 50-100 target range. Hard exclusion rules: ranking + PhD degree is Anthropology not Geography → exclude.
- **Key endpoints**: `https://www.colostate.edu/programs/anthropology/` (PhD program); Peterson's (outdated GRE required listing — ignore); `https://www.usnews.com/best-colleges/university-of-idaho-1626` (not CSU — use search for "Colorado State University U.S. News national universities ranking 2026")
- **Failed / limits**: Full faculty review not conducted due to hard exclusion.
- **Last verified**: 2026-08-26

#### University of Idaho — Geography PhD (EXCLUDED — RANKING HARD LIMIT + METHODOLOGY)
- **Finding**: University of Idaho offers a PhD in Geography under the College of Science. **GRE is not required** (official program page: "GRE: No"). However, U.S. News National Universities ranking is **#183** — far outside the 50-100 target range. Research content centers on GIS, geospatial technologies, remote sensing, statistical and mathematical modeling, geographic-computational models, carbon flux quantification — core is quantitative/computational geography. Research topics include polar meteorology, regional climate change, forest disturbances, human adaptation in high latitudes — while climate-relevant, methodology is modeling-dominant. No political ecology / human geography / environmental governance faculty identified. Hard exclusion: ranking → exclude.
- **Faculty note**: Faculty research directions (confirmed from hotcourses/idp/third-party listings): spatial statistics and modeling, remote sensing, geographic trade models, climate change, natural resource GIS applications. No qualitative or mixed-methods political ecology tracks found.
- **Key endpoints**: `https://uidaho.edu/academics/degree-finder/geography-phd` (official program page, GRE: No confirmed); `https://www.usnews.com/best-colleges/university-of-idaho-1626` (U.Idaho #183)
- **Failed / limits**: PhD supervision evidence not investigated due to ranking hard exclusion.
- **Last verified**: 2026-08-26

#### University of Montana — PhD in Geosciences (EXCLUDED — RANKING + GRE HARD LIMIT)
- **Finding**: University of Montana Department of Geosciences offers a PhD in Geosciences (Geography content area), not a traditional Geography PhD. **GRE is required** (Peterson's explicitly lists "Doctoral Degree Exam: GRE General Test" and third-party beeinnow.com confirms "GRE scores with a test date that is within the past five years OR verifiable GRE scores"). U.S. News National Universities ranking is **#363** — far outside the 50-100 target range. While the program includes human-environment geography topics (historical/cultural geography, settlement geography, resource geography, economic geography, planning, GIS), the degree is Geosciences/Earth Sciences. Hard exclusion: GRE required + ranking → exclude.
- **Faculty note**: Montana State University (Bozeman, not Missoula) is a separate institution — ranked #318. University of Montana Geography faculty include historical/cultural geography, settlement geography, resource geography (energy and water), economic geography, planning, bioclimatology, GIS, snow science, but under Geosciences department with GRE required.
- **Key endpoints**: `https://catalog.umt.edu/graduate/college-forestry-conservation/phd-programs/geosciences-phd/` (Geosciences PhD catalog); Peterson's (GRE required confirmed); `https://www.usnews.com/best-colleges/university-of-montana-2536` (U.Montana #363)
- **Failed / limits**: Full faculty review not conducted due to hard exclusion.
- **Last verified**: 2026-08-26

#### University of South Florida — PhD in Geography and Environmental Science and Policy (REVIEWED — PROVISIONAL)
- **Finding**: USF School of Geosciences (Tampa) offers a PhD in Geography and Environmental Science and Policy. U.S. News National Universities ranking is **#88** — within target range. **GRE is not required** (official School of Geosciences graduate page explicitly: "The GRE is not required for admission to the graduate programs at the School of Geosciences"; Peterson's listing "GRE General Test" is outdated and overridden by the official page). Fall Deadline: February 15 (Peterson's 2026-27 cycle). Tuition: $15,863/year (international). Requires Master's degree, GPA ≥ 3.20. **Critical rule**: "Ph.D. students are only admitted with a confirmed advisor" and "only faculty members with 'professor' in their title can serve as dissertation advisors" — full professor requirement is a hard constraint. Funding: TA/RA + tuition waiver + health insurance available.
- **Faculty assessment**: Richard Mbatu (Associate Professor, St. Petersburg campus): political ecology + political economy of natural resources + global conservation + sustainable development + climate change + REDD+; publishes extensively; teaches international environmental politics and negotiations; graduate students listed (Jessica Gruber, Aleta Kane) but role as dissertation chair not confirmed from pure.lib.usf.edu records. **Key risk**: Mbatu is Associate Professor — may not satisfy the "professor in title" dissertation advisor requirement; St. Petersburg campus affiliation may not transfer to Tampa PhD program. Fenda Akiwumi (Professor, Tampa): environmental and social geographer + resource development/conservation and policy + environmental justice + Africa + diaspora; direction highly relevant. Kamal Alsharif (Professor, Tampa): water resources management and policy + environmental policy + hydropolitics + International environmental politics; teaches graduate water policy courses. Rebecca Johns (Associate Professor, St. Petersburg): society-nature relationships + environmental citizenship + community-based climate resilience.
- **Key endpoints**: `https://www.usf.edu/arts-sciences/departments/geosciences/graduate` (GRE not required, PhD requirements); `https://www.usf.edu/arts-sciences/departments/geosciences/people` (faculty list); `https://www.usf.edu/arts-sciences/departments/geosciences/people/faculty/richard-mbatu.aspx` (Mbatu profile); `https://catalog.usf.edu/preview_program.php?catoid=24&poid=12488&returnto=4077` (PhD catalog); Peterson's (outdated GRE required — ignore)
- **Failed / limits**: Fall 2027 specific admission open status not confirmed from official pages; Mbatu dissertation chair eligibility and St. Petersburg-to-Tampa transfer not confirmed.
- **Last verified**: 2026-08-26

#### University of Utah — Geography PhD (EXCLUDED — RANKING HARD LIMIT)
- **Finding**: U.S. News National Universities ranking is **#151** — far outside the 50-100 target range. Hard exclusion rule: ranking → exclude.
- **Key endpoints**: Use search for "University of Utah U.S. News national universities ranking 2026"
- **Failed / limits**: Full faculty review not conducted due to hard exclusion.
- **Last verified**: 2026-08-26

#### University of Central Florida — Geography PhD (EXCLUDED — RANKING HARD LIMIT)
- **Finding**: U.S. News National Universities ranking is **#117** — far outside the 50-100 target range. Hard exclusion rule: ranking → exclude.
- **Key endpoints**: Use search for "University of Central Florida U.S. News national universities ranking 2026"
- **Failed / limits**: Full faculty review not conducted due to hard exclusion.
- **Last verified**: 2026-08-26

#### University of Alabama — Geography PhD (EXCLUDED — RANKING HARD LIMIT)
- **Finding**: U.S. News National Universities ranking is **#169** — far outside the 50-100 target range. Hard exclusion rule: ranking → exclude.
- **Key endpoints**: Use search for "University of Alabama U.S. News national universities ranking 2026"
- **Failed / limits**: Full faculty review not conducted due to hard exclusion.
- **Last verified**: 2026-08-26

#### University of Hawaii Manoa — Geography PhD (EXCLUDED — RANKING HARD LIMIT)
- **Finding**: U.S. News National Universities ranking is **#169** — far outside the 50-100 target range. Hard exclusion rule: ranking → exclude.
- **Key endpoints**: Use search for "University of Hawaii Manoa U.S. News national universities ranking 2026"
- **Failed / limits**: Full faculty review not conducted due to hard exclusion.
- **Last verified**: 2026-08-26

## Auto-Update Protocol

After searching EACH school, update this file. Do NOT defer to end of session — update immediately.

### Update Format

```markdown
#### School Name
- **Architecture**: [one of: Pure Portal | Vue SPA | React SPA | Static HTML | Worktribe | Cloudflare WAF | Custom CMS]
- **Layer**: L1
- **Access**: [concise: what worked]
- **Key endpoint**: [URL if API discovered]
- **Failed**: [what you tried that did NOT work]
- **Last verified**: [today's date]
```

### Rules

1. **Always record architecture** — even if you used a fallback. Knowing "Cloudflare WAF" tells the next session to skip curl and go straight to browser.
2. **Record failures** — "Tried API at /api/staff → 404" is AS VALUABLE as a success. It prevents the next session from wasting time on the same dead end.
3. **Update, don't duplicate** — if the school already has an entry, update its fields rather than adding a second entry.
4. **New schools go at the bottom** of their country section.
5. **After updating, save the file**. (Optional: if the skill directory is a git repo and the user consents, commit the changes. Do not auto-commit without confirmation.)

### Why this compounds

| Searches completed | Schools in registry | Hit rate on next search |
|-------------------|-------------------|------------------------|
| 5 | 5 | ~25% |
| 20 | 20 | ~60% |
| 50 | 50 | ~85% |
| 100 | 100 | ~95% |

After 100 schools, almost every new search hits a known architecture. The skill becomes 3-5x faster.

### 🇬🇧 UK — Dance/Performance/Theatre Schools (2026-08-03, 秦嘉琪选导验证)

#### University of York
- **Architecture**: Static HTML (staff profiles)
- **Layer**: L1
- **Best method**: Direct curl/WebFetch — york.ac.uk/sociology/our-staff/academic/{slug} and arts-creative-technologies/people/{slug}
- **Key endpoint**: https://www.york.ac.uk/sociology/our-staff/research/ (staff list)
- **Note**: School of Arts and Creative Technologies (ACT) has theatre faculty; no dedicated dance dept. Sociology has Darren Reed (dance & human sociality)
- **Last verified**: 2026-08-03

#### Cardiff University
- **Architecture**: Static HTML (profiles.cardiff.ac.uk) + Cloudflare on main site
- **Layer**: L1 (profiles subdomain)
- **Best method**: profiles.cardiff.ac.uk/staff/{username} works; main cardiff.ac.uk blocked by Cloudflare; use ORCA author pages as fallback
- **Key endpoint**: https://profiles.cardiff.ac.uk/staff/rowdencs
- **Note**: School of Music, Drama & Performance; no standalone Education school (Cardiff Met is separate)
- **Last verified**: 2026-08-03

#### Newcastle University
- **Architecture**: Static HTML
- **Layer**: L1
- **Best method**: Direct access ncl.ac.uk/sacs/staff/profile/{slug}.html
- **Key endpoint**: https://www.ncl.ac.uk/sacs/people/
- **Note**: School of Arts & Cultures (SACS); no dedicated dance posts; ethnomusicology/performance faculty match
- **Last verified**: 2026-08-03

#### University of East Anglia (UEA)
- **Architecture**: Pure Portal (research-portal.uea.ac.uk)
- **Layer**: L1 (research portal accessible)
- **Best method**: research-portal.uea.ac.uk/en/persons/{slug}; org pages accessible, /persons subpages may trigger bot check
- **Key endpoint**: https://research-portal.uea.ac.uk/en/persons/george-mckay
- **Note**: Drama merged into School of Literature, Drama & Creative Writing; no dance dept
- **Last verified**: 2026-08-03

#### University of Leicester
- **Architecture**: Static HTML (le.ac.uk/people/)
- **Layer**: L1
- **Best method**: le.ac.uk/people/{slug}; School of Media, Communication and Sociology merged into School of Arts (2024)
- **Key endpoint**: https://le.ac.uk/people/melanie-kennedy
- **Last verified**: 2026-08-03

#### Swansea University
- **Architecture**: Static HTML (swansea.ac.uk/staff/)
- **Layer**: L1
- **Best method**: swansea.ac.uk/staff/{initial}.{surname}/
- **Key endpoint**: https://www.swansea.ac.uk/staff/a.rogers/
- **Note**: Amanda Rogers (Geography) researches British Chinese performance + digital dance — top match for Chinese diaspora dance students
- **Last verified**: 2026-08-03

#### University of Reading
- **Architecture**: Static HTML
- **Layer**: L1
- **Best method**: Vicki Harman (Sociology) researches ballroom dancing — biocentre.reading.ac.uk path
- **Key endpoint**: http://www.biocentre.reading.ac.uk/politics-international-relations/staff/professor-vicki-harman
- **Last verified**: 2026-08-03

#### University of Strathclyde
- **Architecture**: Static HTML (strath.ac.uk/staff/)
- **Layer**: L1
- **Best method**: strath.ac.uk/staff/{name}dr/
- **Key endpoint**: https://www.strath.ac.uk/staff/robinsonannadr/ (Anna Robinson — autism + creative arts)
- **Last verified**: 2026-08-03

#### University of Bristol (Theatre)
- **Architecture**: Static HTML + research-information.bris.ac.uk Pure portal
- **Layer**: L1
- **Best method**: research-information.bris.ac.uk/en/persons/{slug} and bristol.ac.uk/person/{uuid-slug}
- **Key endpoint**: https://research-information.bris.ac.uk/en/persons/kirsty-sedgman
- **Note**: Department of Theatre has strong audience/performance faculty (Sedgman, Krebs, Clarke)
- **Last verified**: 2026-08-03

#### University of St Andrews
- **Architecture**: Pure Portal (research-portal.st-andrews.ac.uk)
- **Layer**: L1
- **Best method**: research-portal.st-andrews.ac.uk/en/persons/{slug}
- **Key endpoint**: https://research-portal.st-andrews.ac.uk/en/persons/stavroula-pipyrou
- **Note**: Social Anthropology has Stavroula Pipyrou (performance and dance) — top match for dance anthropology
- **Last verified**: 2026-08-03

#### University of Waikato (NZ)
- **Architecture**: Static HTML staff list + Symplectic SPA profiles
- **Layer**: L1 (staff list) / L2 (profiles.waikato.ac.nz SPA)
- **Best method**: profiles.waikato.ac.nz/{username} via browser; School of Arts has Theatre Studies and Dance
- **Key endpoint**: https://www.waikato.ac.nz/about/faculties-schools/arts/our-people
- **Note**: Laura Haughey (Assoc Prof, Theatre & Dance), Sue Cheesman (dance education)
- **Last verified**: 2026-08-03

#### University of Tasmania
- **Architecture**: Pure Portal (discover.utas.edu.au)
- **Layer**: L1
- **Best method**: discover.utas.edu.au/{Name}/teaching for supervision records; utas.edu.au/profiles/staff/ for theatre
- **Key endpoint**: https://discover.utas.edu.au/MaryAnn.Hunter/teaching
- **Note**: Mary Ann Hunter (arts education, drama AND dance) — strong match for dance education students
- **Last verified**: 2026-08-03

### 🇺🇸 United States — Animal Nutrition / Wildlife Screening (2026-08-25, 邢宝文)

#### University of Illinois Urbana-Champaign
- **Architecture**: Static catalog + WordPress lab/profile pages
- **Layer**: L1
- **Best method**: Use `catalog.illinois.edu` for current Animal Sciences PhD policy, then WebSearch/WebFetch official ACES and lab pages for individual faculty.
- **Key endpoints**: https://catalog.illinois.edu/graduate/aces/animal-sciences-phd/ ; https://publish.illinois.edu/companion-animal-comparative-nutrition/about-us/maria-r-cattai-de-godoy/
- **Note**: 2026-2027 catalog states GRE scores are not required and companion/laboratory animals are available for study. Current public faculty pages do not reliably expose ordinary PhD supervision or 2027 recruitment, so do not infer eligibility from title or graduate-course teaching alone.
- **Last verified**: 2026-08-25

#### University of Minnesota Twin Cities — College of Veterinary Medicine
- **Architecture**: Drupal/static content with profile URL migrations
- **Layer**: L3
- **Best method**: WebSearch current `vetmed.umn.edu` profile URLs, then WebFetch the exact page; do not trust stored bio URLs across sessions.
- **Key endpoint**: https://vetmed.umn.edu/ (department and graduate-program navigation)
- **Note**: Previously stored Julie Churchill profile URL returned 404 on 2026-08-25. Current CVM research-grant pages show graduate research activity but do not establish Churchill as a current ordinary PhD supervisor. Require a newly verified profile plus a current PhD route before reconsidering.
- **Last verified**: 2026-08-25

#### Virginia Tech — School of Animal Sciences
- **Architecture**: Static faculty pages + VT CMS search pages
- **Layer**: L1/L3
- **Best method**: Use the School of Animal Sciences admissions page for deadlines, GRE wording, major-professor assignment, and assistantship enrollment rules; verify each faculty page individually.
- **Key endpoints**: https://dasc.vt.edu/teaching/graduate/admissions-qualifications-requirements.html ; https://sas.vt.edu/people/faculty/persia-mike
- **Note**: Current page lists Fall deadlines as August 1 domestic and April 1 international; GRE is encouraged, not stated as required; students receive a major professor with an active research program. Mike Persia's official page is valid and research-active but focuses on poultry meat/egg production and does not explicitly establish PhD supervision. Some other profiles expose current graduate students, but their research is swine/dairy production-focused.
- **Last verified**: 2026-08-25

#### Virginia Tech — Planning, Governance, and Globalization (PGG)
- **Architecture**: VT Academic Catalog + static SPIA/PGG pages + downloadable handbook
- **Layer**: L1/L3
- **Best method**: Start with the current Graduate Catalog entry at `https://catalog.vt.edu/graduate/degree-programs/planning-governance-globalization-phd/` for the official degree name, tracks, program director, coordinator, and campus locations. Then verify the current PGG page and extract the 2025-26 handbook locally for supervision and curriculum rules. Treat Graduate School deadlines, GRE, and assistantship pages as university-wide policy only unless the PGG page or catalog states a program-specific rule.
- **Key endpoints**: https://catalog.vt.edu/graduate/degree-programs/planning-governance-globalization-phd/ ; https://spia.vt.edu/academics/graduate/pgg.html ; https://spia.vt.edu/graduate/pgg..html ; https://spia.vt.edu/content/spia_vt_edu/en/graduate/pgg/_jcr_content/content/vtmultitab/vt-items_0/download/file.res/PGG_Handbook_2025-26.pdf ; https://graduateschool.vt.edu/admissions/how-to-apply.html ; https://graduateschool.vt.edu/admissions/how-to-apply/testing-requirements.html ; https://graduateschool.vt.edu/funding/assistantships.html
- **Note**: The 2026-27 catalog confirms PGG is an active PhD with Governance and Globalization and Urban and Environmental Design and Planning tracks; it lists Joel Peters as Graduate Program Director and Kelly Crist as Graduate Coordinator. The current PGG page confirms related master's backgrounds, environmental planning and sustainability, international development planning, community and economic development, and full-/part-time study in Blacksburg and the Greater Washington DC area, but does not state Fall 2027, a PGG-specific deadline, project-level GRE, stipend, or multi-year funding guarantee. The 2025-26 handbook states that at least one PGG faculty member must agree to supervise before a formal offer and that advisors are normally full-time, tenured or tenure-track teaching/research faculty. Todd Schenk and Maaz Gardezi have current official personal pages and appear as supporting faculty in the handbook; retain as provisional until 2027 recruitment and supervision willingness are confirmed.
- **Last verified**: 2026-08-26

#### University of Wisconsin-Madison — Animal and Dairy Sciences
- **Architecture**: Static Guide catalog + WordPress department site
- **Layer**: L1
- **Best method**: Read the current Guide PhD page together with `andysci.wisc.edu` research and graduate pages; treat the newer Animal and Dairy Sciences PhD as the active route and do not use the retiring Animal Sciences PhD as the primary 2027 route.
- **Key endpoints**: https://guide.wisc.edu/graduate/animal-dairy-sciences/animal-dairy-sciences-phd/ ; https://andysci.wisc.edu/
- **Note**: The current program covers nutrition, genetics, behavior, health and precision agriculture, but official department framing centers animal agriculture, food systems and precision livestock farming. No verified companion-animal, wildlife or wild-bird PhD supervisor was found in this pass.
- **Last verified**: 2026-08-25

#### University of Georgia — Department of Poultry Science
- **Architecture**: Static official CAES faculty profiles plus legacy/current graduate pages
- **Layer**: L1
- **Best method**: Use the current CAES Poultry Science graduate page for the PhD route, the official assistantship page for funding mechanics, and individual CAES profile pages for faculty. The current personnel directory is useful for active status but is not a substitute for a personal profile.
- **Key endpoints**: https://www.caes.uga.edu/departments/poultry/graduate.html ; https://poultry.caes.uga.edu/graduate/assistantships.html ; https://www.caes.uga.edu/departments/poultry/people/faculty/todd-applegate.html ; https://www.caes.uga.edu/departments/poultry/people/faculty/sammy-aggrey.html
- **Note**: The PhD route covers physiology, genetics, nutrition, products technology, parasitology, toxicology, microbiology and molecular biology. Assistantships are competitive and may be departmental, faculty-grant based, or university-wide; the Presidential Graduate Fellows Program provides five years of support, while departmental assistantships are subject to availability and have stated semester limits. No uniform public stipend or explicit 2027 Fall recruitment statement was found for Applegate or Aggrey; do not infer supervision or recruitment from title alone.
- **Last verified**: 2026-08-26

#### Auburn University — Poultry Science
- **Architecture**: Static College of Agriculture program pages plus directory/profile pages
- **Layer**: L1
- **Best method**: Use the official Poultry Science PhD page for GRE, rolling review, GRA and career information; verify faculty on the individual College of Agriculture profile, not the directory alone.
- **Key endpoints**: https://agriculture.auburn.edu/academic-programs/poultry-science.php ; https://agriculture.auburn.edu/directory/profile.php?id=rochesj ; https://agriculture.auburn.edu/poul/poultry-directory.php
- **Note**: The official PhD page states GRE is not required, review is rolling, and the listed PhD GRA is about $21,000/year with full tuition waiver; amounts may change and availability depends on departmental/faculty resources. Samuel Rochell’s individual profile is valid and shows Associate Professor (Poultry Nutrition), broiler nutrient/energy needs, feed ingredient utilization and stress effects; a third-party-indexed official research record reports graduate supervision history, but current Auburn pages do not state 2027 recruitment or an available assistantship. Do not write without current recruitment/funding closure.
- **Last verified**: 2026-08-26

#### North Carolina State University — Animal Science / Poultry Science
- **Architecture**: Current static CALS pages plus Graduate Catalog
- **Layer**: L1
- **Best method**: Use the current Animal Science Admissions and Deadlines page as the authoritative source for GRE and deadlines; cross-check the Graduate Catalog for degree and assistantship structure, and use current nutrition/physiology faculty pages for research scope.
- **Key endpoints**: https://cals.ncsu.edu/animal-science/students/graduate/admissions-and-deadlines/ ; https://catalog.ncsu.edu/graduate/agriculture-life-sciences/animal-poultry-science/ ; https://cals.ncsu.edu/animal-science/students/graduate/assistantships/ ; https://cals.ncsu.edu/animal-science/group/nutrition/
- **Note**: The current admissions page explicitly says GRE scores are required for all new graduate students, despite the Nutrition catalog PDF listing no entrance exam; for this student’s hard exclusion, use the current Animal Science admissions rule and exclude the Animal Science route. The program covers companion and exotic animals in nutrition and domestic/exotic cats in physiology; assistantships are competitive and the current page lists PhD support of $15,000, or $20,000 including summer supplement, with tuition/health coverage up to five years for direct-BS-to-PhD students and mandatory teaching. The Nutrition PDF should be treated as a conflicting/less-specific source, not as an override.
- **Last verified**: 2026-08-26

#### Purdue University — Animal Sciences
- **Architecture**: Official OGSPS admissions pages plus current College of Agriculture department pages and individual directory profiles
- **Layer**: L1/L3
- **Best method**: Start with the current OGSPS Animal Sciences page for supported degrees, required documents and international deadlines; cross-check the current department graduate pages for entry dates, adviser/support conditions and research areas; verify each faculty member through a unique official profile or official faculty news item. Do not rely on archived catalog pages for current GRE policy.
- **Key endpoints**: https://www.purdue.edu/academics/ogsps/admissions/gradrequirements/westlafayette/animal-sciences/ ; https://ag.purdue.edu/department/ansc/graduate-program/prospective-graduate.html ; https://ag.purdue.edu/department/ansc/faculty-by-area-research.html ; https://ag.purdue.edu/directory/hong566 ; https://ag.purdue.edu/directory/ladeola ; https://ag.purdue.edu/directory/index.html#/ccroney
- **Note**: The current OGSPS page is static and exposes the deadline table in search extraction, but WebFetch renders some headings without the underlying values; use the search extract together with the page. The current OGSPS and department pages list PhD, Nutrition, Genetics and Animal Behavior and Well-being, and state that admission requires a major adviser plus adequate research support and facilities. The current pages do not explicitly say GRE optional or required; an archived 2014-15 catalog says GRE required, but it is not safe to apply that archived rule to 2027 Fall. The department page advises international applicants to apply at least six months before the start date, and current OGSPS deadlines list international Fall April 1, Spring August 1 and Summer January 1. Jinsu Hong, Olayiwola Adeola and Candace Croney have valid official profiles and relevant research/supervision evidence, but 2027 Fall recruitment and individual funding remain unclosed. Victoria Uyanga’s old official CV URL returned a confirmed 404 and is not a valid current profile source.
- **Last verified**: 2026-08-26

#### University of Nebraska-Lincoln — Animal Science
- **Architecture**: Official graduate program page plus static Animal Science faculty profiles, graduate manual and Graduate School funding pages
- **Layer**: L1
- **Best method**: Use the official Animal Science PhD page for GRE, major-advisor acceptance, rolling review and Fall deadline guidance; then verify faculty on individual `animalscience.unl.edu` pages and cross-check assistantship rules in the graduate manual and Graduate School page. Treat general benefits thresholds as eligibility rules, not as guaranteed department stipend offers.
- **Key endpoints**: https://www.unl.edu/gradstudies/academics/programs/ASCI-PHD ; https://animalscience.unl.edu/animal-science-graduate-student-manual/research-assistantships-teaching-assistantships-and-other/ ; https://graduate.unl.edu/funding/assistantships ; https://animalscience.unl.edu/sheila-purdum ; https://animalscience.unl.edu/lisa-karr ; https://animalscience.unl.edu/jessica-l-petersen-phd ; https://cbio.unl.edu/person/tianjing-zhao/
- **Note**: The program page states GRE optional, major advisor acceptance and rolling review, with March 15 recommended for Fall. Department/faculty funding is the key assistantship source; the manual supports a typical three-year PhD assistantship with tuition and eligible health coverage, while the 2025-26 $15,450/year figure is a benefits-eligibility minimum rather than the actual offer. Sheila Purdum is a poultry-nutrition lead but current ordinary PhD supervision and 2027 recruitment are not explicit. Lisa Karr has companion-animal nutrition teaching and PhD supervision history but an extension/administration-centered role. Jessica Petersen has doctoral supervision and USDA research evidence but is mainly focused on cattle/horse genomics. Tianjing Zhao’s official profile is theoretical/computational quantitative genetics and is excluded under the pure-computation rule.
- **Last verified**: 2026-08-26

#### Iowa State University — Animal Science / Poultry Nutrition
- **Architecture**: Official Graduate College program pages plus static Animal Science people pages and faculty-site lab pages
- **Layer**: L1/L3
- **Best method**: Use the Graduate College `animal_science` page as the authoritative source for the PhD, GRE, rolling review and major-professor requirement. Verify faculty through current Animal Science people pages and, where needed, an official faculty-site lab page. Use the Animal Science assistantship page for university-level tuition, health and stipend information, but do not treat it as a PI-specific 2027 Fall offer.
- **Key endpoints**: https://www.grad-college.iastate.edu/programs/animal_science ; https://www.ans.iastate.edu/graduate/scholarships-and-financial-aid ; https://www.ans.iastate.edu/people/elizabeth-bobeck ; https://www.ans.iastate.edu/people/dawn-koltes ; https://faculty.sites.iastate.edu/delkins/ ; https://faculty.sites.iastate.edu/delkins/dawn-koltes-lab-group
- **Note**: The current program page says GRE is not required, there is no fixed deadline and review is rolling; applicants should identify species, a preferred faculty advisor and research interests, and thesis-seeking admission requires a major professor. The assistantship page describes salary, tuition support and health insurance, with PhD tuition support potentially covering 100%; the stipend page title and term labels show a year mismatch, so the public amount should remain a reference rather than a 2027 promise. Elizabeth Bobeck and Dawn Koltes are useful poultry-nutrition leads, but current public pages do not close 2027 Fall recruitment or PI-specific funding.
- **Last verified**: 2026-08-26

#### Colorado State University — Fish, Wildlife and Conservation Biology
- **Architecture**: Warner College program page plus current department directory and dynamic official person pages; lab pages used only as supporting evidence
- **Layer**: L1/L3
- **Best method**: Start with the current FWCB M.S. & Ph.D. Programs page for GRE, degree prerequisites, rolling admissions and faculty-funding conditions. Use the current department directory to discover dynamic `person/?user=...` URLs instead of guessing them, then WebFetch each official personal page. Use lab/student pages only to supplement PhD-supervision evidence. Do not let an old handbook override the current program admissions page.
- **Key endpoints**: https://warnercnr.colostate.edu?p=60536/ ; https://warnercnr.colostate.edu/department-directory/?department=Fish%2C+Wildlife+and+Conservation+Biology&type=Faculty ; https://warnercnr.colostate.edu/person/?user=xaXBeIP6maWZFiC4YlcEIQ%3D%3D ; https://warnercnr.colostate.edu/person/?user=EzpQZpRDt3Pg%2FqhGhen79w%3D%3D ; https://liseaubry.wixsite.com/aubrypopecology/people
- **Note**: The current program page says GRE scores are not required, PhD admission is rolling, a master's degree is normally expected, and applicants must first find a faculty advisor with aligned interests and available funding. Faculty grants are expected to cover tuition and stipend before admission, but this does not establish an individual 2027 Fall opening. Lise Aubry and David Koons are current official faculty with research and doctoral-supervision evidence; Kathryn Stoner appears in older CSU material but not the current FWCB directory, so do not treat her as a current CSU supervisor. An older handbook conflicts with the current GRE-not-required page and should not override it.
- **Last verified**: 2026-08-26

#### Oregon State University — Animal Science / Rangeland Ecology
- **Architecture**: Current static Graduate Education program pages plus current Animal and Rangeland Sciences department pages
- **Layer**: L1/L3
- **Best method**: Use the current Graduate Education program page for the authoritative Required Tests field and deadlines, then cross-check the department's graduate FAQ for GRE and mentor requirements. Do not rely on the older `dev.agsci.oregonstate.edu` fact sheet or archived material when it conflicts with the current Graduate Education page.
- **Key endpoints**: https://graduate.oregonstate.edu/programs/1250/animal-science-phd-ms-minor ; https://anrs.oregonstate.edu/anrs/graduate ; https://anrs.oregonstate.edu/anrs/graduate/thinking-about-graduate-school ; https://gradschool.oregonstate.edu/programs/6220/rangeland-ecology-and-management-phd-ms-minor
- **Note**: The current Animal Science Graduate Education page lists GRE under Required Tests and requires acceptance by a faculty mentor before applying. The department FAQ separately states that a GRE score is required. The current program includes companion-animal behavior, animal nutrition and animal genetics, but the student's GRE hard exclusion closes the route before faculty-level screening. The current Rangeland Ecology and Management program page also lists GRE under Required Tests.
- **Last verified**: 2026-08-26

#### Mississippi State University — Animal and Dairy Sciences
- **Architecture**: Current static department graduate page, with Graduate Handbook linked for supporting detail
- **Layer**: L1
- **Best method**: Use the current department Graduate Studies page as the primary source for the PhD and admissions criteria; treat archived catalog PDFs as historical context only. Search faculty only if the GRE gate is cleared.
- **Key endpoints**: https://ads.msstate.edu/students/grad/index.php ; https://www.ads.msstate.edu/students/docs/ADS_Grad_Handbook.pdf
- **Note**: The current department page confirms the PhD in Agriculture with a concentration in Animal and Dairy Science and explicitly requires a minimum GPA of 3.00 plus GRE scores. The listed research ideas are mainly livestock production, physiology, meat science, genetics and feed-based nutrition. The GRE requirement is sufficient to exclude this route for the student; no faculty-level screening is needed.
- **Last verified**: 2026-08-26

#### Oklahoma State University — Animal and Food Sciences
- **Architecture**: Current static department graduate page plus current Graduate Catalog pages
- **Layer**: L1
- **Best method**: Use the current department graduate page for application materials and advisor-acceptance rules, then cross-check the current Animal Science PhD catalog page for degree requirements. Do not proceed to faculty screening when the GRE hard gate fails.
- **Key endpoints**: https://agriculture.okstate.edu/departments-programs/afs/graduate ; https://catalog.okstate.edu/graduate-college/doctoral/animal-science-phd/
- **Note**: The current department page confirms Animal Science PhD, requires prior advisor acceptance/faculty mentor support, and lists GRE scores among the application materials. This closes the route under the student's GRE-required exclusion before faculty-level screening.
- **Last verified**: 2026-08-26
