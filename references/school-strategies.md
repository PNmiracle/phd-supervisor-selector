# School Strategy Knowledge Base

Living registry of which access layer to use for each university. Discipline-agnostic — works for fashion, engineering, psychology, anything.

---

## Universal Access Framework (L1 → L2 → L3)

Not every school needs a unique trick. Most fall into one of three layers:

| Layer | Name | When to use | Method | Requires |
|:---:|------|-------------|--------|----------|
| **L1** | Direct Access | curl returns full HTML content | `curl` → parse staff list → extract names/links | Nothing |
| **L2** | API Mining | curl returns empty shell (SPA) but API exists | Download JS → grep `api\|baseUrl` → call API with `?size=1000` | JS bundle access |
| **L3** | Search Engine Fallback | curl blocked (403/WAF) OR JS renders but no API | Google `site:{uni} "{name}" professor` → click result in browser | In-app browser |

### Decision Tree

```
curl staff page
├── 200 + HTML table/links → L1: parse directly
├── 200 + empty shell (<5KB) → L2: hunt API in JS bundle
│   ├── API found → L2: call API, filter results
│   └── No API → L3: search engine per name
├── 403/1020/Cloudflare → L3: browser + search engine
└── Timeout/DNS → Try graduate school subdomain or L3 fallback
```

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
| Cloudflare WAF | **L3** | curl blocked → browser + search engine |
| Imperva/Incapsula | **L3** | Browser may also be blocked → manual |
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
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

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
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Edinburgh
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Glasgow
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Brighton
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

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

### 🇦🇺 Australia

#### RMIT University
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Technology Sydney (UTS)
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Melbourne
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

### 🇸🇬 Singapore

#### Nanyang Technological University (NTU)
- **Architecture**: —
- **Layer**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

---


## Auto-Update Protocol (Agent executes during search)

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
5. **After updating, commit**: `git add references/school-strategies.md && git commit -m "learn: {School} → {Architecture}"`

### Why this compounds

| Searches completed | Schools in registry | Hit rate on next search |
|-------------------|-------------------|------------------------|
| 5 | 5 | ~25% |
| 20 | 20 | ~60% |
| 50 | 50 | ~85% |
| 100 | 100 | ~95% |

After 100 schools, almost every new search hits a known architecture. The skill becomes 3-5x faster.



After each search session, fill in the blanks for schools you searched:

```markdown
#### School Name
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: curl → parse staff listing at https://...
- **Key endpoint**: https://www.school.ac.uk/department/staff/
- **Failed**: Tried API at /api/faculty → 404
- **Last verified**: 2026-06-26
```

If a school was NOT in this registry, add it. If you discovered a NEW strategy that worked, mark the old one under **Failed** and update **Access**.

### Batch Update Script

After a search session, run something like:

```python
# Update school-strategies.md with results from this session
for school in searched_schools:
    update_registry(school.name, school.architecture, school.access_method, school.endpoint)
```

The agent should update this file manually as part of the search workflow — after completing a school, add an entry.

#### University of Leeds
- **Architecture**: Static HTML (staff profile pages)
- **Layer**: L1
- **Access**: Direct URL access to staff profiles at ahc.leeds.ac.uk/design/staff/
- **Key endpoint**: https://ahc.leeds.ac.uk/design/staff/
- **Failed**: —
- **Last verified**: 2026-06-26

#### De Montfort University
- **Architecture**: Static HTML (staff profile pages)
- **Layer**: L1
- **Access**: Direct URL access to academic staff pages at dmu.ac.uk/academic-staff/
- **Key endpoint**: https://www.dmu.ac.uk/academic-staff/
- **Failed**: —
- **Last verified**: 2026-06-26

#### University of Brighton
- **Architecture**: Pure Portal (research.brighton.ac.uk)
- **Layer**: L2
- **Access**: Pure Portal JSON API → parse researcher profiles
- **Key endpoint**: https://research.brighton.ac.uk/persons/
- **Failed**: —
- **Last verified**: 2026-06-26

### 🇭🇰 Hong Kong

#### University of Hong Kong (HKU)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: browser → psychology.hku.hk faculty page; business school via hkubs.hku.hk
- **Key endpoint**: https://psychology.hku.hk/faculty-members/
- **Failed**: —
- **Last verified**: 2026-06-26

#### Chinese University of Hong Kong (CUHK)
- **Architecture**: Static HTML (psych) + JS-rendered (business)
- **Layer**: L1
- **Access**: psy.cuhk.edu.hk via browser; bschool.cuhk.edu.hk staff page is JS-rendered
- **Key endpoint**: https://www.psy.cuhk.edu.hk/en/people/faculty.html
- **Failed**: CUHK Psych page partially inaccessible; supplemented via Bing search
- **Last verified**: 2026-06-26

#### HKUST
- **Architecture**: Mixed
- **Layer**: L2→L3
- **Access**: Web accessible; no Psychology dept (only Division of Social Science)
- **Key endpoint**: https://bm.hkust.edu.hk/faculty (Business School)
- **Failed**: No Psychology PhD
- **Last verified**: 2026-06-26

#### City University of Hong Kong (CityU)
- **Architecture**: Static HTML partially accessible
- **Layer**: L1
- **Access**: cityu.edu.hk/ss/ for Social & Behavioural Sciences
- **Key endpoint**: https://www.cityu.edu.hk/ss/
- **Failed**: Full browser verification needed
- **Last verified**: 2026-06-26

#### Hong Kong Polytechnic University (PolyU)
- **Architecture**: JS-rendered
- **Layer**: —
- **Access**: polyu.edu.hk/apss/ for Applied Social Sciences
- **Key endpoint**: https://www.polyu.edu.hk/apss/
- **Failed**: JS-rendered, needs browser
- **Last verified**: 2026-06-26

#### Hong Kong Baptist University (HKBU)
- **Architecture**: Inaccessible
- **Layer**: L3
- **Access**: Browser attempt failed
- **Key endpoint**: https://socsc.hkbu.edu.hk/
- **Failed**: Network restrictions
- **Last verified**: 2026-06-26

#### Lingnan University
- **Architecture**: Static HTML partially accessible
- **Layer**: L1
- **Access**: ln.edu.hk/psy/
- **Key endpoint**: https://www.ln.edu.hk/psy/
- **Failed**: Partial accessibility; applied/counseling focus
- **Last verified**: 2026-06-26

#### Education University of Hong Kong (EdUHK)
- **Architecture**: Inaccessible
- **Layer**: L3
- **Access**: Browser attempt failed
- **Key endpoint**: —
- **Failed**: Network restrictions; educational/developmental focus
- **Last verified**: 2026-06-26

### 🇸🇬 Singapore

#### National University of Singapore (NUS)
- **Architecture**: Static HTML + custom profiles
- **Layer**: L1
- **Access**: fass.nus.edu.sg/psy for Psychology; bschool.nus.edu.sg for Business
- **Key endpoint**: https://fass.nus.edu.sg/psy/people/
- **Failed**: —
- **Last verified**: 2026-06-26

#### Nanyang Technological University (NTU)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: ntu.edu.sg/sss for Psychology; ntu.edu.sg/business for NBS
- **Key endpoint**: https://www.ntu.edu.sg/sss/about-us/our-people
- **Failed**: —
- **Last verified**: 2026-06-26

#### Singapore Management University (SMU)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: socsc.smu.edu.sg for Psychology; business.smu.edu.sg for LKCSB
- **Key endpoint**: https://socsc.smu.edu.sg/about/faculty
- **Failed**: —
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
- **Access**: Browser ONLY (Cloudflare blocks curl)
- **Key endpoint**: —
- **Failed**: curl → 403; all automated access blocked
- **Last verified**: 2026-06-26

### 🇨🇳 Sino-foreign Joint Programs

#### CUHK Shenzhen
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: hss.cuhk.edu.cn for Applied Psychology
- **Key endpoint**: https://hss.cuhk.edu.cn/en/taxonomy/term/21
- **Failed**: —
- **Last verified**: 2026-06-26

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
- **Access**: Hub structure; no Psychology dept
- **Key endpoint**: —
- **Failed**: No relevant department
- **Last verified**: 2026-06-26

#### UIC (BNU-HKBU, Zhuhai)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: Graduate School exists; no Psychology PhD
- **Key endpoint**: —
- **Failed**: No Psychology PhD program
- **Last verified**: 2026-06-26

#### Duke Kunshan University
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: Masters-only; no PhD programs
- **Key endpoint**: —
- **Failed**: No PhD programs, no Psychology dept
- **Last verified**: 2026-06-26

#### UNNC (Nottingham Ningbo)
- **Architecture**: Mixed, not fully accessible
- **Layer**: L2→L3
- **Access**: Browser needed; Psychology PhD unconfirmed
- **Key endpoint**: —
- **Failed**: Automated search inconclusive
- **Last verified**: 2026-06-26

#### XJTLU (Xi'an Jiaotong-Liverpool)
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: No Psychology dept in HSS; Business PhD via IBSS
- **Key endpoint**: —
- **Failed**: No Psychology department
- **Last verified**: 2026-06-26


#### University of Sydney
- **Architecture**: Custom CMS (profiles.sydney.edu.au)
- **Layer**: L1→L3
- **Access**: Direct URL access to staff profiles
- **Key endpoint**: https://profiles.sydney.edu.au/
- **Failed**: —
- **Last verified**: 2026-06-26

#### UNSW
- **Architecture**: React SPA + Cloudflare
- **Layer**: L2
- **Access**: Browser only — find-an-expert page loads but filters are JS-dependent
- **Key endpoint**: https://newsroom.unsw.edu.au/find-an-expert
- **Failed**: Direct API access blocked
- **Last verified**: 2026-06-26

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

#### QUT
- **Architecture**: Cloudflare WAF (全站)
- **Layer**: L3
- **Access**: BLOCKED — needs manual browser from user side
- **Key endpoint**: https://www.qut.edu.au/research/our-people
- **Failed**: curl + browser both blocked
- **Last verified**: 2026-06-26


---

## Auto-Update Protocol

After searching each school, add or update its entry. One sentence per field.

### Required fields

```markdown
#### School Name
- **Layer**: L1 / L2 / L3
- **Architecture**: Static HTML / Pure Portal / Vue SPA / Cloudflare WAF / etc.
- **Best method**: [one sentence — what actually worked]
- **Key URL / endpoint**: [URL]
- **Failed**: [what you tried that did NOT work — as valuable as successes]
- **Last verified**: YYYY-MM-DD
```

### Commit cadence

Every 5 schools: `git add references/school-strategies.md && git commit -m "learn: [School]→L?" && git push`

#### Hong Kong University of Science and Technology (HKUST)
- **Architecture**: Static HTML
- **Access**: No Psychology dept → target Business School Marketing dept
- **Key endpoint**: https://mark.hkust.edu.hk/faculty-and-staff/directory
- **PhD link**: https://prog-crs.ust.hk/pgprog/2022-23/mphil-phd-mark
- **Note**: Also has "Leadership and Behavioral Decision-making" research area via bm.hkust.edu.hk. Management dept may have additional behavioral faculty.
- **Failed**: —
- **Last verified**: 2026-06-26

#### City University of Hong Kong (CityU)
- **Architecture**: Static HTML + Incapsula WAF (partial)
- **Access**: SS pages blocked by WAF → use scholars.cityu.edu.hk or Google cached results. CB pages accessible directly.
- **Key endpoint**: https://scholars.cityu.edu.hk/shanzhen, https://www.cb.cityu.edu.hk/staff/
- **PhD link**: https://www.cb.cityu.edu.hk/pg/ (business), https://www.cityu.edu.hk/pg/programme/ (SS)
- **Failed**: ssweb.cityu.edu.hk blocked by Incapsula
- **Last verified**: 2026-06-26

#### Hong Kong Polytechnic University (PolyU)
- **Architecture**: JS-rendered
- **Access**: polyu.edu.hk/apss/ for Applied Social Sciences; polyu.edu.hk/mm/ for Marketing
- **Key endpoint**: https://www.polyu.edu.hk/apss/people/academic-staff/
- **PhD link**: https://www.polyu.edu.hk/apss/study/research-postgraduate-programme/
- **Note**: Recently posted JDM faculty job on SJDM, confirms active JDM research presence
- **Failed**: JS-rendered needs browser
- **Last verified**: 2026-06-26

#### Hong Kong Baptist University (HKBU)
- **Architecture**: Static HTML (educ.hkbu.edu.hk); socsc.hkbu.edu.hk unreachable
- **Access**: Psychology lives within Dept of Education and Psychology (educ.hkbu.edu.hk), NOT standalone psych dept. Also check Business School at busrpg.hkbu.edu.hk.
- **Key endpoint**: https://educ.hkbu.edu.hk/?page_id=20398
- **PhD link**: https://educ.hkbu.edu.hk/?page_id=20338
- **Failed**: socsc.hkbu.edu.hk → connection refused; browser attempt failed
- **Last verified**: 2026-06-26

#### Lingnan University
- **Architecture**: Static HTML
- **Access**: ln.edu.hk/psy/ fully accessible; browser works
- **Key endpoint**: https://www.ln.edu.hk/psy/about-us/people/academic-staff
- **PhD link**: https://www.ln.edu.hk/rpg/
- **Failed**: —
- **Last verified**: 2026-06-26

#### Education University of Hong Kong (EdUHK)
- **Architecture**: Static HTML
- **Access**: eduhk.hk/ps/en/ for Psychology dept; accessible via browser
- **Key endpoint**: https://www.eduhk.hk/ps/en/aboutus.php?s=our_staff
- **PhD link**: https://www.eduhk.hk/gradsch/
- **Failed**: Previous attempt via network blocked; browser works
- **Last verified**: 2026-06-26

#### Macau University of Science and Technology (MUST)
- **Architecture**: Cloudflare WAF
- **Access**: BLOCKED all automated attempts. No psychology department exists — psych coursework embedded in FHSS.
- **Key endpoint**: —
- **Failed**: curl → 403 (Cloudflare); browser blocked; Google Scholar shows engineering-only decision-making research; Chinese search yields no psych JDM faculty
- **Last verified**: 2026-06-26

#### HKUST(GZ)
- **Architecture**: Static HTML
- **Access**: Hub structure; Society Hub has 4 thrusts (CNCC, FTEC, IPE, UGOD). No behavioral/cognitive science thrust.
- **Key endpoint**: https://soch.hkust-gz.edu.cn/
- **Failed**: No psychology/behavioral science thrust area
- **Last verified**: 2026-06-26

#### BNBU / UIC (北师香港浸会大学, Zhuhai)
- **Architecture**: Static HTML
- **Access**: 9 PhD programs exist but none in psychology. Applied Psychology is undergraduate-only.
- **Key endpoint**: https://gs.uic.edu.cn/ (graduate school)
- **Failed**: No psychology PhD program; behavioral decision research happens in math/stats depts but not a dedicated track
- **Last verified**: 2026-06-26

#### Duke Kunshan University
- **Architecture**: Static HTML
- **Access**: Masters-only institution; 5 Master's programs, zero PhD programs
- **Key endpoint**: https://dukekunshan.edu.cn/en/academics/graduate
- **Failed**: No PhD programs of any kind; Duke Durham has relevant programs but DKU does not
- **Last verified**: 2026-06-26

#### University of Nottingham Ningbo China (UNNC)
- **Architecture**: Static HTML
- **Access**: No Psychology dept. Business School (NUBS China) has ICBBR (behavioural business research centre).
- **Key endpoint**: https://www.nottingham.edu.cn/en/business/
- **PhD link**: NUBS China PhD available for behavioural economics/consumer behavior route
- **Failed**: No psychology-specific PhD; business school only
- **Last verified**: 2026-06-26

#### Xi'an Jiaotong-Liverpool University (XJTLU)
- **Architecture**: Static HTML
- **Access**: No Psychology dept in HSS (only China Studies, International Studies, Media, Linguistics). IBSS offers PhD in Business.
- **Key endpoint**: https://www.xjtlu.edu.cn/en/academics/schools/ibss
- **Failed**: No psychology department; IBSS business PhD only
- **Last verified**: 2026-06-26

### 🇬🇧 United Kingdom (continued)

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

#### University of Edinburgh
- **Architecture**: JS-rendered profile directory (edwebprofiles.ed.ac.uk)
- **Access**: https://www.ed.ac.uk/profile/{name} → redirects to JS profile
- **Key endpoint**: https://www.ed.ac.uk/profile/alison-lenton
- **Failed**: —
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

### 🇺🇸 United States

#### Columbia Business School
- **Architecture**: Cloudflare WAF
- **Access**: Browser ONLY; business.columbia.edu/faculty/people/{name}
- **Key endpoint**: https://business.columbia.edu/faculty/people/eric-johnson
- **Failed**: curl → Cloudflare block
- **Last verified**: 2026-06-26

#### Princeton University
- **Architecture**: Cloudflare WAF (psych.princeton.edu)
- **Access**: Browser ONLY
- **Key endpoint**: https://psych.princeton.edu/people/elke-weber
- **Note**: Elke Weber moved from Columbia → Princeton
- **Last verified**: 2026-06-26

#### Harvard University — Psychology
- **Architecture**: Mixed; some profile URLs 404
- **Access**: Personal sites may be more reliable than dept pages
- **Key endpoint**: https://www.joshua-greene.net/ (personal site; dept URL 404)
- **Last verified**: 2026-06-26

#### Carnegie Mellon University — SDS
- **Architecture**: Static HTML
- **Access**: https://www.cmu.edu/dietrich/sds/people/faculty/{name}.html
- **Key endpoint**: https://www.cmu.edu/dietrich/sds/people/faculty/daniel-oppenheimer.html
- **Note**: Carey Morewedge moved from CMU → Boston University Questrom
- **Last verified**: 2026-06-26

#### Boston University — Questrom
- **Architecture**: Static HTML
- **Access**: https://www.bu.edu/questrom/profile/{name}/
- **Key endpoint**: https://www.bu.edu/questrom/profile/carey-morewedge/
- **Last verified**: 2026-06-26

#### McGill University — Psychology
- **Architecture**: Incapsula WAF (blocks all automated access)
- **Access**: Browser ONLY; mcgill.ca/psychology/{name}
- **Key endpoint**: https://www.mcgill.ca/psychology/ross-otto
- **Failed**: All curl → 403; search blocked; faculty directory 403
- **Last verified**: 2026-06-26

### 🇸🇪 Sweden

#### Linköping University (LiU)
- **Architecture**: Employee ID system; JS-rendered profiles
- **Access**: https://liu.se/en/employee/{employee-id} (IDs are like danva85)
- **Key endpoint**: https://liu.se/en/employee/danva85 (Daniel Västfjäll)
- **Failed**: Employee search by name via URL doesn't work; ID guessing unreliable
- **Last verified**: 2026-06-26

#### Lund University
- **Architecture**: Research portal (portal.research.lu.se) — 403 to curl
- **Access**: Browser; https://www.nek.lu.se/en/{name} for economics dept
- **Key endpoint**: https://portal.research.lu.se/en/persons/erik-wengstrom
- **Note**: Erik Wengström moved from QUT → Lund
- **Last verified**: 2026-06-26

### 🇳🇿 New Zealand

#### University of Otago — Business School
- **Architecture**: Cloudflare WAF (blocks all automated access)
- **Access**: Browser ONLY
- **Key endpoint**: https://www.otago.ac.nz/marketing/staff/professor-maree-thyne
- **Failed**: All curl → Cloudflare 403
- **Last verified**: 2026-06-26

### 🇸🇬 Singapore (updated)

#### Singapore Management University (SMU)
- **Architecture**: SITE RESTRUCTURED 2025-2026; old socsc.smu.edu.sg profiles broken
- **Access**: New platform at https://faculty.smu.edu.sg/ (JS-rendered, search required)
- **Key endpoint**: https://faculty.smu.edu.sg/profile/david-chan (confirmed via Google)
- **Failed**: All socsc.smu.edu.sg individual profile URLs now broken
- **Last verified**: 2026-06-26

### 🇦🇺 Australia (updated)

#### UNSW Sydney
- **Layer**: L1
- **Architecture**: Static HTML staff profiles (unsw.edu.au/staff/) + Adobe AEM (main domain)
- **Access**: curl directly — unsw.edu.au/staff/{slug} returns full HTML with title tag containing professor name. VERIFIED 2026-07-01 with 6 profiles.
- **Key endpoint**: https://www.unsw.edu.au/staff/{slug}
- **PhD application**: https://www.unsw.edu.au/study/research-degrees
- **Note**: Main domain (unsw.edu.au) may trigger Cloudflare, but staff sub-pages consistently work with curl.
- **Failed**: newsroom.unsw.edu.au/find-an-expert redirects/times out
- **Last verified**: 2026-07-01
- **Access**: https://www.unsw.edu.au/staff/{name}
- **Key endpoint**: https://www.unsw.edu.au/staff/ben-newell
- **Note**: Ben Newell moved from UCL/others → UNSW; not at Carleton
- **Last verified**: 2026-06-26

#### Macquarie University
- **Architecture**: Pure research portal (researchers.mq.edu.au)
- **Access**: https://researchers.mq.edu.au/en/persons/{name}/
- **Key endpoint**: https://researchers.mq.edu.au/en/persons/abas-mirzaei/
- **Last verified**: 2026-06-26


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
| CityU | `cb.cityu.edu.hk/people-and-research/people/people-details?eid={id}` |
| UCL (new) | `profiles.ucl.ac.uk/{id}-{slug}` |
| UNSW | `unsw.edu.au/staff/{slug}` |
| LiU | `liu.se/en/employee/{employeeId}` (IDs like danva85) |
| Lund | `portal.research.lu.se/en/persons/{slug}` |
| McMaster | `experts.mcmaster.ca/people/{initials}` |
| Carleton | `carleton.ca/psychology/people/{slug}/` |

#### Victoria University of Wellington
- **Layer**: L1 (static HTML people directory) + L2 (JS-rendered individual profiles)
- **Architecture**: Vue SPA for individual people pages, static HTML for school-of-education page
- **Best method**: Curl the School of Education page (https://www.wgtn.ac.nz/fehps/about/our-people/school-of-education) — embedded JSON has research codes and titles. Use people.wgtn.ac.nz for individual profiles (JS SPA, needs browser).
- **Key endpoint**: https://www.wgtn.ac.nz/fehps/about/our-people/school-of-education
- **Failed**: Direct curl of people.wgtn.ac.nz/{username} returns empty SPA shell
- **Last verified**: 2026-06-29

#### University of Otago
- **Layer**: L3 (Static HTML with Cloudflare WAF)
- **Architecture**: Static HTML behind Cloudflare WAF (curl returns 403)
- **Best method**: In-app browser. Navigate to https://www.otago.ac.nz/education/staff — browser bypasses Cloudflare. Individual profile URLs follow https://www.otago.ac.nz/education/staff/{name-slug} pattern.
- **Key endpoint**: https://www.otago.ac.nz/education/staff
- **Failed**: curl returns 403 (Cloudflare)
- **Last verified**: 2026-06-29

#### University of Geneva (FPSE)
- **Layer**: L1 (Static HTML for team pages)
- **Architecture**: Static HTML with JS enhancements
- **Best method**: curl the SSED research groups page at https://www.unige.ch/fapse/recherche/ssed — contains all research group and professor listings in static HTML. Individual profile URLs need browser (JS-rendered).
- **Key endpoint**: https://www.unige.ch/fapse/recherche/ssed
- **Failed**: EN version URL has redirect loop; personal pages may be JS-rendered
- **Last verified**: 2026-06-29

#### University of Vienna
- **Layer**: L3 (UCRIS Pure portal behind Cloudflare)
- **Architecture**: Pure portal (UCRIS) protected by Cloudflare WAF
- **Best method**: In-app browser — but Cloudflare challenge blocks even the browser. Manual search needed.
- **Failed**: curl 403, browser also blocked by Cloudflare challenge
- **Last verified**: 2026-06-29

#### University of Canterbury
- **Layer**: L1→L3 (redirects to generic study page)
- **Architecture**: Modern SPA with redirects
- **Best method**: Navigate from main site https://www.canterbury.ac.nz/ then find Education staff links
- **Failed**: Direct URLs redirect to generic study information pages
- **Last verified**: 2026-06-29

#### University of Basel
- **Layer**: L3 (SSL issues)
- **Architecture**: edu.unibas.ch subdomain has SSL connection issues
- **Best method**: Try alternative subdomain or manual search
- **Failed**: curl SSL error, browser ERR_CONNECTION_CLOSED
- **Last verified**: 2026-06-29

#### University of Hamburg
- **Layer**: L3 (multiple 404s, navigation needed)
- **Architecture**: Static HTML with complex navigation structure
- **Best method**: Start from main site (https://www.uni-hamburg.de/) then navigate to "Forschung → Karrierewege". The "Promovieren" link leads to https://www.uni-hamburg.de/forschung/karrierewege.html. Admission requirements at https://www.uni-hamburg.de/campuscenter/bewerbung/promotion.html (but refers to faculty-level "Promotionsordnungen").
- **Key discovery path**: DE version works, EN version returns 404 on most sub-pages.
- **Language requirements**: English B2 required; German C1/C2 only for German-language program.
- **Last verified**: 2026-06-29

#### University of Vienna
- **Layer**: L2→L3 (UCRIS Pure Portal + DE site works, EN 404s)
- **Architecture**: German site (doktorat.univie.ac.at) works well; English redirects often 404
- **Best method for PhD info**: Navigate from https://www.univie.ac.at/studium/ → "PhD / Doktorat" → "Zulassung zu Doktorats- und PhD-Studien" → https://doktorat.univie.ac.at/doktoratunivie/zulassung/
- **Language requirements**: Deutsch- und/oder Englischkenntnisse auf Niveau C1. "Abschlusszeugnisse und optionaler Sprachnachweis" — language certificate is optional, depends on department. For Bildungswissenschaft (Education), English C1 likely sufficient.
- **Key endpoint**: https://doktorat.univie.ac.at/ (DE version), https://slw.univie.ac.at/studieren/deutschkenntnisse/ (German requirements)
- **Last verified**: 2026-06-29

#### University of Basel
- **Layer**: L3 (SSL issues on edu subdomain)
- **Architecture**: Main site (unibas.ch) works but education-specific subdomains fail with SSL
- **Best method for PhD info**: Start from main site https://www.unibas.ch/en/ → "Studies" or search "PhD"
- **Last verified**: 2026-06-29

#### University of Basel
- **Layer**: L1 (main site unibas.ch works) + L3 (edu.unibas.ch SSL fails)
- **Architecture**: Static HTML, well-organized German site. English site sometimes 404.
- **Best method for PhD info**: Navigate from https://www.unibas.ch/de/Studium.html → "Anmeldung & Zulassung → Zulassung → Doktorat". Key URL: https://www.unibas.ch/de/Studium/Vor-dem-Studium/Bewerbung-Zulassung/Zulassung/Zulassung-zum-Doktorat.html
- **Language requirements**: "Die hauptsächlichen Unterrichtssprachen sind Deutsch und Englisch. Mindestens Niveau C1 gemäss Europäischem Referenzrahmen erwartet." For doctoral programs, specific requirements in faculty Promotionsordnung. 
- **Key endpoint (language)**: https://www.unibas.ch/de/Studium/Vor-dem-Studium/Bewerbung-Zulassung/Zulassung/Sprachkenntnisse.html
- **Last verified**: 2026-06-29

#### University of Bern
- **Layer**: L1 (main site works) + L3 (erz.unibe.ch SSL fails)
- **Architecture**: Static HTML, well-organized multilingual site. Use English or German paths.
- **Best method for PhD info**: Navigate from https://www.unibe.ch/ → "Studies → Doctorate". Key admission page: https://www.unibe.ch/studies/prospective_students/application_and_admission/application_and_admission_for_doctoral_studies/index_eng.html
- **Language requirements**: Official PDF (Zulassungbedingungen_e_26-27_eng.pdf): Bachelor requires German C1 certificate. Master programs may require English (if English-taught). For doctoral level, requirements specified in faculty Promotionsordnung. General rule: German and English are main languages.
- **Key endpoint**: Admission PDF at https://www.unibe.ch/unibe/portal/content/e1006/e15237/e1466586/Zulassungbedingungen_e_26-27_eng.pdf
- **Last verified**: 2026-06-29

#### University of Bern
- **Layer**: L1-L2 (edu.unibe.ch works, erz.unibe.ch blocked)
- **Architecture**: Static HTML + JS search interface for staff A-Z
- **Best method**: Use main site search (unibe.ch/suche/) to find individual professor pages. edu.unibe.ch/ueber_uns/personen_a___z/ has JS search interface (no static listing). Individual URLs at edu.unibe.ch/ueber_uns/personen_a___z/{dept}/prof_dr_{last}_{first}/
- **Key endpoint**: edu.unibe.ch/ueber_uns/personen_a___z/
- **Failed**: erz.unibe.ch blocked by browser policy
- **Last verified**: 2026-06-29

#### University of Innsbruck
- **Layer**: L3 (Anubis anti-bot)
- **Architecture**: IEZW site protected by Anubis web firewall (v1.25.0)
- **Best method**: Not accessible via automated tools. Manual search needed.
- **Failed**: curl 404 on team pages; browser blocked by Anubis
- **Last verified**: 2026-06-29

#### University of Waikato
- **Layer**: L1 (staff directory static) + L2 (Symplectic SPA for individuals)
- **Architecture**: Static HTML staff list at waikato.ac.nz/about/faculties-schools/education/our-staff/. Individual profiles at profiles.waikato.ac.nz/{username} (Symplectic/Elsevier JS SPA - needs browser).
- **Best method**: Get names from static staff page; open Symplectic profiles in browser to verify research content (JS renders research areas).
- **Key endpoint**: https://www.waikato.ac.nz/about/faculties-schools/education/our-staff/
- **Last verified**: 2026-06-29

#### University of Tübingen
- **Layer**: L1 (static Personal/Team pages)
- **Architecture**: WiSo Faculty → IfE → Static HTML for department personal pages
- **Best method**: Navigate from https://uni-tuebingen.de/ → "Fakultäten" → "Wirtschafts- und Sozialwissenschaftliche Fakultät" → "Fachbereich Sozialwissenschaften" → "Erziehungswissenschaft" → "Institut". Key personal pages:
  - Sozialpädagogik: .../abteilungen/sozialpaedagogik/personal/
  - Allgemeine Pädagogik: .../abteilungen/allgemeine-paedagogik/personal/
  - Individual profiles: .../institut/team/{name-slug}/
- **Key discovery**: Old URL de/242 returns 404; new path through WiSo Fakultät navigation works. 15 professors across 4 departments.
- **Failed**: Direct old URLs all 404; site completely restructured in 2025/2026
- **Last verified**: 2026-06-29

#### University of Vienna (u:find)
- **Layer**: L2 (person.html?id=XXXX for individual profiles)
- **Architecture**: u:find JS SPA at ufind.univie.ac.at. Individual profile URLs use format `person.html?id=XXXX`. UCRIS portal on separate subdomain.
- **Best method**: Search Google for "[Name] University Vienna u:find" → find person ID → use `ufind.univie.ac.at/en/person.html?id=XXXX`. Check "Currently not an active member of staff" status on the profile.
- **Key endpoint**: https://ufind.univie.ac.at/en/person.html?id={numeric_id}
- **Failed**: ufind search.html URLs don't work; need direct person ID; UCRIS blocked by Cloudflare
- **Last verified**: 2026-06-29

#### University of Hamburg
- **Layer**: L3 (site restructured, person search needed)
- **Architecture**: Education faculty (Fakultät für Erziehungswissenschaft) has restructured website. Most English URLs return 404.
- **Best method**: Use university person search (Personensuche) from main site. German URLs work better than English.
- **Failed**: /en/personal.html → 404; /personen/ → 404; most EW subpages broken
- **Last verified**: 2026-06-29

#### University of Cologne
- **Layer**: L1 (static HTML with numeric page IDs)
- **Architecture**: Static HTML. Individual profile pages use numeric IDs, NOT name slugs.
- **Best method**: Search main site (hf.uni-koeln.de/suche/) for professor name → find numeric page ID (e.g., 33878 for Herzmann, 33835 for Proske). Individual URLs: https://www.hf.uni-koeln.de/{numeric_id}
- **Key discovery**: Name-slug URLs like /personen/petra-herzmann/ all return 404. Numeric IDs are the only working format.
- **Failed**: /personen/ directory browsing; /personen/{name}/ all 404; site search returns no JavaScript results in this environment
- **Last verified**: 2026-06-29


### PhD Program URL Patterns by University

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



#### CUHK MAE - Individual Profile URLs
- **Individual profile path**: /peoples/ NOT /people/ (the static HTML listing page uses /people/academic-staff/ but individual profiles use /peoples/{name-slug}/)
- **Slug format**: surname-first (e.g. lau-darwin-tat-ming, liao-wei-hsin, liu-yun-hui, au-kwok-wai-samuel)
- **Best method**: Bing search "[Name] CUHK MAE" to discover the exact slug, then verify with curl
- **Last verified**: 2026-06-30

#### CityU CS - Individual Profile URLs
- **Architecture**: SPA (department site) + Scholars Portal (static)
- **Layer**: L3 for department site, L1 for Scholars Portal
- **Best method**: Use CityU Scholars Portal for individual profiles: https://scholars.cityu.edu.hk/en/persons/{name}({uuid}) - search Bing for "[Name] CityU" to discover UUID
- **Key endpoint**: https://scholars.cityu.edu.hk/ (Pure Portal variant, returns static HTML)
- **Failed**: cs.cityu.edu.hk individual pages are SPA; ee.cityu.edu.hk individual pages also SPA; ~cssamk/ personal pages 404
- **Last verified**: 2026-06-30

#### NUS CDE - Individual Profile URLs
- **Architecture**: Full SPA (all cde.nus.edu.sg pages)
- **Layer**: L3 only
- **Best method**: None via curl - ALL CDE pages return SPA shells (212 chars). Use browser for individual profile verification.
- **Key endpoint**: https://cde.nus.edu.sg/me/people/ (department listing, SPA shell)
- **Failed**: Curl on all CDE subpages returns SPA; Bing search returns encrypted URLs
- **Last verified**: 2026-06-30


#### CityU Sam Kwong - Staff Profile
- **Individual profile**: https://www.cityu.edu.hk/stfprofile/cssamk.htm (static HTML, not SPA)
- **Slug**: cssamk (NOT sam-kwong)
- **Discovery**: DDG HTML search "Sam Kwong CityU"
- **Last verified**: 2026-06-30

#### NUS Wang Hao - Staff Profile  
- **Individual profile**: https://cde.nus.edu.sg/me/staff/wang-hao-victor/ (NOT /people/wang-hao/)
- **Slug**: wang-hao-victor (NOT wang-hao)
- **Discovery**: DDG HTML search "Wang Hao NUS mechanical engineering"
- **Note**: /me/people/ paths are SPA shells; individual staff pages accessible via /me/staff/{slug}/
- **Last verified**: 2026-06-30


#### University of Sydney
- **Layer**: L3 (Symplectic Elements SPA)
- **Architecture**: Symplectic Elements Discovery portal at profiles.sydney.edu.au. All individual profiles and group pages are pure SPAs (2118 bytes shell). CSS/JS loaded dynamically.
- **Best method**: Main education page (sydney.edu.au/arts/schools/sydney-school-of-education-and-social-work.html) returns 67KB with some profile links embedded. Individual profiles require browser verification.
- **Key endpoint**: profiles.sydney.edu.au/{username} (SPA)
- **Failed**: All API paths (v1/api/individuals, api/rest/v1, etc.), model.json feeds, JSON/RDF format parameters, print view
- **Last verified**: 2026-06-30

#### UNSW Sydney
- **Layer**: L2 (Adobe AEM SPA, staff profiles accessible)
- **Architecture**: Adobe Experience Manager (AEM) SPA for listing pages. Individual staff profiles at unsw.edu.au/staff/{slug} return real content (100-500KB) with research data embedded in HTML. Research profile pages (research.unsw.edu.au/people/{slug}) also accessible.
- **Best method**: Use known staff names to construct unsw.edu.au/staff/{slug} URLs. Parse HTML for research keywords, publications, grants. School of Education research strengths include "Sociology of education."
- **Key endpoint**: https://www.unsw.edu.au/staff/{slug}
- **Failed**: AEM model.json returns minimal structure only; Our People listing page is SPA; newsroom expert finder API returns HTML only; research.unsw.edu.au/people search returns SPA
- **Last verified**: 2026-06-30

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

## Australian Universities (2026-06-30)

### Architecture Overview

| University | CMS/Platform | Access Method | Profile URL Pattern |
|-----------|-------------|---------------|---------------------|
| Melbourne | Pure Portal v5.x (React SPA) | findanexpert.unimelb.edu.au → individual profiles by name | findanexpert.unimelb.edu.au/display/{name-slug} |
| Sydney | Symplectic Elements SPA | profiles.sydney.edu.au/{username} (SPA shell, 2118 bytes) | profiles.sydney.edu.au/{firstname}.{lastname} |
| UNSW | Adobe AEM (staff pages OK) | unsw.edu.au/staff/{slug} → real HTML content | unsw.edu.au/staff/{slug} |
| ANU | Pure Portal v5.x (React SPA) | React shell for all pages; individual titles contain researcher name in meta | researchers.anu.edu.au/researchers/{id-slug} |
| Monash | Pure Portal v5.x | research.monash.edu/en/persons/ → accessible via web | research.monash.edu/en/persons/{name}/ |
| UQ | Drupal/UQ Experts (Numeric ID) | about.uq.edu.au/experts/{id} → real HTML but no name in URL | about.uq.edu.au/experts/{numeric_id} |
| UWA | Pure Portal (research-repository) | research-repository.uwa.edu.au/en/persons/{name}/ → SPA | research-repository.uwa.edu.au/en/persons/{name}/ |
| Adelaide | Pure Portal v5.x | researchers.adelaide.edu.au/profile/{name} → SPA | researchers.adelaide.edu.au/profile/{firstname}.{lastname} |
| UTS | UTS Profiles (SPA) | profiles.uts.edu.au/{name}/about → SPA shell | profiles.uts.edu.au/{Firstname}.{Lastname}/about |
| RMIT | Pure Portal (academics) | academics.rmit.edu.au/{name-slug} → SPA | academics.rmit.edu.au/{name-slug} |
| Macquarie | Pure Portal (researchers) | researchers.mq.edu.au/en/persons/{id} → SPA | researchers.mq.edu.au/en/persons/{id} |
| Curtin | Staff Portal (static HTML) | staffportal.curtin.edu.au/staff/profile/view/{id}/ → accessible | staffportal.curtin.edu.au/staff/profile/view/{id}/ |
| Wollongong | Symplectic Elements | scholars.uow.edu.au/{name}/about → SPA | scholars.uow.edu.au/{firstname}-{lastname}/about |
#### Deakin University
- **Layer**: L3
- **Architecture**: Pure Portal SPA (experts.deakin.edu.au) + Cloudflare WAF (deakin.edu.au CMS pages)
- **Access**: experts.deakin.edu.au/{slug} returns "Discovery" SPA shell (~2KB). Individual profiles require browser. deakin.edu.au/about-deakin/people blocked by Cloudflare.
- **Key endpoint**: https://experts.deakin.edu.au/{slug}
- **PhD application**: https://www.deakin.edu.au/study/find-a-course/research-degrees
- **Note**: experts.deakin.edu.au is the consistent URL pattern.
- **Failed**: deakin.edu.au/about-deakin/people/{name} → 403 Cloudflare
- **Last verified**: 2026-07-01


#### University of Freiburg (2026-06-30 update)
- **Layer**: L3-L4 (HISinOne getter-protected, site restructured)
- **Architecture**: New uni-freiburg.de site (2025/2026 relaunch); old erzwiss domain returns 000/timout
- **Key discovery**: `uni-freiburg.link/personensuche` resolves to HISinOne Personensuche which loads publicly ("ohne Anmeldung am System nur öffentlich sichtbare Personen"). BUT: input fields are getter-protected — `Cannot set property value of [object Object] which has only a getter` — preventing any automated form manipulation. Same protection for Vorlesungsverzeichnis semester selector.
- **Working URLs**: Main page (uni-freiburg.de), Personensuche HISinOne (loads), VVZ (loads), Fakultäten overview page (uni-freiburg.de/universitaet/fakultaeten/)
- **Failed**: Erzwiss domain (timeout), search (0 results), philolfak domain (empty page), all faculty sub-pages (404), all form manipulation (getter-protected)
- **German university pattern confirmed**: Personensuche → HISinOne/QIS system, all protected from external automation
- **Last verified**: 2026-06-30

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

### City University of Hong Kong (2026-07-01 update)
- **Architecture**: Incapsula WAF on main domain + various subdomain architectures
- **Layer**: L4 (Fully blocked from curl)
- **Subdomain probe results**:
  - www.cityu.edu.hk/*: Incapsula WAF (212-951 bytes)
  - www6.cityu.edu.hk: Incapsula
  - www2/www3.cityu.edu.hk: SSL EOF
  - com.cityu.edu.hk: 73 bytes (unreachable)
  - moodle.cityu.edu.hk: SSL EOF
  - canvas.cityu.edu.hk: OK 40KB (Canvas LMS, not faculty data)
  - sgs.cityu.edu.hk: SSL EOF
  - scholars.cityu.edu.hk: 404
  - lbms03.cityu.edu.hk: 122 bytes
- **Failed**: 12 subdomains probed, 0 return faculty data
- **Last verified**: 2026-07-01

### Lingnan University, Hong Kong (2026-07-01 update)
- **Architecture**: Unknown — all URLs return 234 bytes
- **Layer**: L4 (Fully blocked)
- **Failed**: ln.edu.hk/daci, ln.edu.hk/visualstudies, main domain
- **Last verified**: 2026-07-01

### University of Auckland (2026-07-01 update)
- **Architecture**: Drupal/JS-rendered profiles + multiple subdomains
- **Layer**: L3-L4 (Mostly blocked)
- **Accessible**: calendar.auckland.ac.nz (249K), researchspace.auckland.ac.nz (203K), arts about page (325K)
- **Blocked**: profiles.auckland.ac.nz (JS shell 2122B), unidirectory.auckland.ac.nz (0B), most dept pages (403/406)
- **Failed**: All staff listing approaches
- **Last verified**: 2026-07-01

### Victoria University of Wellington (2026-07-01 update)
- **Architecture**: Semi-static HTML with embedded JS data
- **Layer**: L2-L3 (Some pages accessible, profiles are JS shells)
- **Accessible pages**: som/about/staff (250KB), fhss/about/staff (191KB), business/about/staff (268KB), explore/subjects (9KB)
- **Key data source**: HTML contains embedded JSON in `<script>` tags (`parsedEmails` key). Staff data includes firstName, lastName, hrOrgUnitName, hrJobTitle, researchInterests, people.wgtn.ac.nz profile links
- **JS shells**: people.wgtn.ac.nz/* (4150 bytes), people.wgtn.ac.nz/json (4150 bytes)
- **Blocked**: wgtn.ac.nz/communication (0 bytes), communication/about/staff (0 bytes)
- **Note**: Communication school is under School of Communication, Journalism and Marketing within Wellington School of Business and Government. SoM staff page only shows management professors. Communication-specific page inaccessible.
- **Workaround**: Extract staff data from embedded JSON in business/som pages; filter by research interests for communication keywords
- **Wayback Machine**: comm staff page not archived (2022-2024)
- **Last verified**: 2026-07-01

### Curtin University (2026-07-01 update)
- **Architecture**: WordPress CMS + SSO-protected staff portal
- **Layer**: L2-L3 (Staff portal accessible, directory requires SSO)  
- **Accessible**: about/our-people (280KB), staffportal profile pages (80KB each), humanities.curtin.edu.au (273KB)
- **Blocked**: staffportal directory (SSO SAML redirect), school-specific staff pages (JS-rendered)
- **Note**: School of Media, Creative Arts and Social Inquiry confirmed to exist in Faculty of Humanities. Staff profiles accessible individually but cannot filter by school from static HTML.
- **Previous L1 status invalidated**: staffportal.curtin.edu.au/staff/directory/ now requires SSO login
- **Last verified**: 2026-07-01

### Hong Kong Baptist University (2026-07-01 update)
- **Architecture**: Adobe AEM (main domain) + Pure Portal SPA (scholars portal) + separate infra for comm subdomain
- **Layer**: L3-L4 (Scholars portal blocked, comm subdomain network-unreachable)
- **Accessible**: gs.hkbu.edu.hk (Grad School), scholars.hkbu.edu.hk (Pure Portal, JS-only for people), hkbu.edu.hk (main domain, Adobe AEM — all guessed URLs return 63KB 404 templates)
- **Blocked**: comm.hkbu.edu.hk (SSL timeout — all protocols), scholars portal API (403)
- **Note**: HKBU has the strongest communication school in HK. Scholars portal UUID-based person pages return 31-byte empty shells. PhD programme URL confirmed: gs.hkbu.edu.hk/programmes/doctor-of-philosophy-master-of-philosophy-school-of-communication
- **Wayback Machine**: scholars organization page archived (235KB) but person data still JS-rendered in archive
- **Last verified**: 2026-07-01

#### Lingnan University
- **Architecture**: Static HTML
- **Layer**: L1
- **Access**: Direct curl → parse profile pages at ln.edu.hk/cultural/people/faculty/{slug}
- **Key endpoint**: https://www.ln.edu.hk/cultural/people/faculty
- **Failed**: uni-directory returns 404; staffdir.htm too thin
- **Last verified**: 2026-07-01

#### Victoria University of Wellington (VUW)
- **Architecture**: Squiz CMS (static pages) + Angular SPA (people profiles)
- **Layer**: L1 (static pages) / L3 (profiles)
- **Access**: Static pages via curl; people.wgtn.ac.nz profiles are SPA shells (4150B) → browser needed
- **Key endpoint**: https://www.wgtn.ac.nz/sam/research/staff-research-interests/media-and-communication
- **Failed**: people.wgtn.ac.nz profiles all return 4150B JS shells; researchers subdomain 404; seftms 404
- **Last verified**: 2026-07-01

#### University of Auckland
- **Architecture**: Imperva/Incapsula WAF
- **Layer**: L3
- **Access**: BLOCKED - 406 on all www subdomains; unidirectory SSL errors; profiles SPA shells; calendar blocked
- **Key endpoint**: None accessible
- **Failed**: All curl, browser, and search engine approaches exhausted
- **Last verified**: 2026-07-01

#### City University of Hong Kong (CityU)
- **Architecture**: Incapsula WAF
- **Layer**: L3
- **Access**: BLOCKED - all www subdomains blocked; canvas.cityu.edu.hk accessible but no staff data
- **Key endpoint**: None accessible
- **Failed**: All curl, browser, and search approaches exhausted
- **Last verified**: 2026-07-01

#### Victoria University of Wellington (VUW)
- **Layer**: L1 (Squiz CMS server-rendered) / L3 (Angular SPA for /explore/ pages)
- **Architecture**: Hybrid - Squiz CMS for school pages (sim, sam, fhss) with server-rendered staff listings; Angular SPA for /explore/ and people.wgtn.ac.nz
- **Best method**: School staff pages (e.g., /sam/about/staff) contain server-rendered staff data with data-cy email attributes. Extract emails via `grep -Eo 'data-cy="[^@]+@vuw\.ac\.nz"' | sort -u`. Use people.wgtn.ac.nz/{username} for individual profile URLs (JS-rendered, content not accessible via curl).
- **Key endpoint**: `https://www.wgtn.ac.nz/sam/about/staff` (368KB server-rendered page)
- **Profile URL**: `https://people.wgtn.ac.nz/{email.username}` (e.g., people.wgtn.ac.nz/geoff.stahl)
- **Failed**: people.wgtn.ac.nz profiles are React SPA - curl returns empty shell; /explore/ pages are Angular SPA; /communication-studies returns 404
- **Last verified**: 2026-07-01

#### Lingnan University
- **Layer**: L1
- **Architecture**: Static HTML (Department of Cultural Studies)
- **Best method**: Direct curl → parse faculty listing at ln.edu.hk/cultural/people/faculty
- **Key endpoint**: `https://www.ln.edu.hk/cultural/people/faculty`
- **Profile URL**: `https://www.ln.edu.hk/cultural/people/faculty/prof-{name-slug}`
- **Failed**: —
- **Last verified**: 2026-07-01

#### City University of Hong Kong (CityU)
- **Layer**: L3 (BLOCKED)
- **Architecture**: Incapsula WAF
- **Best method**: None working. All subdomains blocked (com.cityu.edu.hk, cityu.edu.hk). Incapsula returns 403/captcha for curl, browser, and search engines. Requires manual browser access from user.
- **Key endpoint**: BLOCKED
- **Failed**: All curl attempts → Incapsula 403; in-app browser → Incapsula; DDG/Google search → no usable results
- **Last verified**: 2026-07-01
- **⚠️ Manual access needed**: https://www.cityu.edu.hk/com/

#### University of Auckland
- **Layer**: L3 (BLOCKED)
- **Architecture**: Imperva/Incapsula WAF + SSL errors on unidirectory
- **Best method**: None working. 406 responses + SSL errors. Profiles subdomain returns SPA shell.
- **Key endpoint**: BLOCKED
- **Failed**: All access attempts → 406 or SSL errors; profiles subdomain → SPA shell
- **Last verified**: 2026-07-01
- **⚠️ Manual access needed**: https://www.auckland.ac.nz/en/arts/about-the-faculty/school-of-humanities/our-people/contact-an-academic/contact-an-academic-in-media-and-screen-studies.html

#### BNU-HKBU UIC
- **Layer**: L3
- **Architecture**: Vue SPA (Chinese Visual SiteBuilder CMS) - faculty page is hash-routed SPA
- **Best method**: Google search for individual names. No separate individual profile HTML pages exist - all are served via faculty.htm SPA.
- **Key endpoint**: `https://fhss.bnbu.edu.cn/comm_en/faculty/faculty.htm`
- **Profile URL**: `https://fhss.bnbu.edu.cn/comm_en/faculty/faculty.htm#/{username}/en` (hash fragment, SPA-rendered)
- **Failed**: Individual HTML pages don't exist; all profiles are SPA hash-routed
- **⚠️ PhD supervision**: UIC is primarily a teaching institution. MPhil/PhD offered through HKBU co-supervision. Assistant Professors may have limited supervision capacity.
- **Last verified**: 2026-07-01

### CityU Department of Media and Communication (COM) (2026-07-01 update)

#### Access Overview
- **Layer**: L3 (Search Engine Fallback) — ALL subdomains now blocked
- **Architecture**: Mixed (Pure Portal for scholars.cityu.edu.hk, Custom CMS for com.cityu.edu.hk)
- **Blocked**: scholars.cityu.edu.hk (Cloudflare WAF), www.cityu.edu.hk (Incapsula WAF), www6.cityu.edu.hk (Incapsula), com.cityu.edu.hk (73 bytes), moodle.cityu.edu.hk (SSL EOF), sgs.cityu.edu.hk (SSL EOF)
- **Accessible**: canvas.cityu.edu.hk (Canvas LMS, no faculty data)
- **Best method**: DDG/Bing search "\"{Name}\" \"City University of Hong Kong\" professor" → extract scholars.cityu.edu.hk UUID from search results
- **Profile URL format**: scholars.cityu.edu.hk/en/persons/{name}({uuid}) OR www.cityu.edu.hk/com/people/dr-{name-slug}
- **Failed**: All curl methods (Cloudflare + Incapsula on every subdomain that matters)
- **⚠️**: None of the profile URLs can be verified by curl; all require browser or manual user verification
- **Last verified**: 2026-07-01

### Auckland University Communication/Media (2026-07-01 update)

#### Access Overview
- **Layer**: L3✗ (DEAD END) — No communication programme found, all domains blocked
- **Architecture**: Adobe AEM (www subdomain), React SPA (profiles subdomain)
- **Media and Screen Studies**: 9 staff found via contact page, ALL film/TV/media studies focus — NOT communication/advertising/brand
- **Blocked**: profiles.auckland.ac.nz (JS shell 2122B), unidirectory.auckland.ac.nz (0B), business school marketing dept (406), most dept pages (403/406)
- **Accessible but useless**: calendar.auckland.ac.nz (249K), researchspace.auckland.ac.nz (203K), arts contact page (325K)
- **Best method**: None. The arts about page lists staff names and profile links but all profiles are JS-rendered shells. 
- **Manual URL** (last resort): https://www.auckland.ac.nz/en/arts/about-the-faculty/school-of-humanities/our-people/contact-an-academic/contact-an-academic-in-media-and-screen-studies.html
- **⚠️ Auckland has NO dedicated Communication/Advertising/Brand programme. Media and Screen Studies is purely film/TV/media studies.**
- **Last verified**: 2026-07-01


#### City University of Hong Kong (CityU) - Department of Media and Communication
- **Layer**: L3
- **Architecture**: Incapsula WAF (main site) + Cloudflare WAF (scholars.cityu.edu.hk)
- **Best method**: L3 - DuckDuckGo search for individual professor names. Use queries like "[Name] City University Hong Kong professor communication" to discover profile URLs. All curl/browser access is blocked.
- **Key URL**: scholars.cityu.edu.hk/en/persons/{slug} (Cloudflare), stfprofile also Incapsula-blocked (846 bytes). com.cityu.edu.hk Incapsula (843 bytes).
- **Failed**: All curl approaches (main site, scholars subdomain, stfprofile). All return WAF challenge pages.
- **Last verified**: 2026-07-01

#### University of Auckland - Communication/Advertising/Brand
- **Layer**: L3
- **Architecture**: SPA (profiles.auckland.ac.nz, 2122 bytes), Imperva on Business School (406)
- **Best method**: Staff contact page accessible via curl (290KB HTML) but names in SPA. profiles.auckland.ac.nz/{slug} are JS shells. No communication/advertising/brand department - Media and Screen Studies is cinema/TV/media studies.
- **Key URL**: https://www.auckland.ac.nz/en/arts/about-the-faculty/school-of-humanities/our-people/contact-an-academic/contact-an-academic-in-media-and-screen-studies.html (290KB, accessible)
- **Failed**: Individual profile pages (SPA shells), Business School (406/Imperva), GraphQL API, profiles search API (SPA shell)
- **Last verified**: 2026-07-01
- **Status**: Dead end - no matching department for communication/advertising/brand


#### City University of Hong Kong (CityU) - ORCID Discovery Method (2026-07-01)
- **Architecture**: Incapsula WAF (all subdomains blocked)
- **Layer**: L4 (No direct access) → L3 (ORCID fallback) 
- **New method**: ORCID API keyword search broken through where DDG/Bing/Google all failed
- **Best method**: 1) `curl "https://pub.orcid.org/v3.0/search/?q=affiliation-org-name:%22City+University+of+Hong+Kong%22+AND+keyword:communication"` → get ORCID IDs
  2) `curl "https://pub.orcid.org/v3.0/{orcid}/person"` → get researcher names
  3) Use external knowledge to match ORCID names to COM department
  4) Write to Vika with ⚠️ marker since profile pages unverifiable
- **Key endpoint**: https://pub.orcid.org/v3.0/search/?q=affiliation-org-name:%22City+University+of+Hong+Kong%22+AND+(keyword:media+OR+keyword:communication)
- **Found via ORCID**: Tai-Quan Peng, Dani Madrid-Morales, Hai Liang (COM dept)
- **Failed**: All curl/browser approaches; all Incapsula; scholars blocked (403); www6 blocked (840B); stfprofile dead
- **Last verified**: 2026-07-01

#### University of Auckland - ORCID Discovery Method (2026-07-01)
- **Architecture**: Imperva WAF (staff pages) + Angular SPA (profiles) + static HTML (calendar/researchspace)
- **Layer**: L3-L4 (staff pages blocked, calendar accessible) 
- **ORCID method works**: Found 16+ Auckland researchers via ORCID keyword search but employment data incomplete (ORCID records not filled by researchers)
- **Best method**: ORCID → names → Google Scholar cross-reference → verify affiliation
- **Key endpoint**: https://pub.orcid.org/v3.0/search/?q=affiliation-org-name:%22University+of+Auckland%22+AND+(keyword:media+OR+keyword:film+OR+keyword:screen)
- **Accessible pages**: calendar.auckland.ac.nz (249KB), researchspace.auckland.ac.nz (203KB), arts about page (312KB)
- **Blocked**: All /our-people/ and /staff/ paths (406); profiles subdomain SPA shell (2122B); unidirectory SSL error
- **Last verified**: 2026-07-01

### ORCID Discovery Pattern (Cross-School)

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


## AU Schools Access Layer Summary (2026-07-01)

| University | Architecture | Access Method | Key Endpoint |
|-----------|-------------|---------------|--------------|
| The University of Melbourne | L3 (Incapsula on findanexpert) | Individual profile pages via findanexpert.unimelb.edu.au/profile/{id}-{name} can be accessed via curl (200 OK) | findanexpert.unimelb.edu.au/profile/{id}-{slug} |
| Monash University | L1 (Pure Portal) | Pure portal research.monash.edu.au works; individual persons pages accessible | research.monash.edu.au/en/persons/{slug} |
| UNSW Sydney | L2 | Staff profile pages at unsw.edu.au/staff/{slug} may work; JS-rendered | unsw.edu.au/staff/{slug} |
| The University of Sydney | L3 (JS SPA) | Architecture faculty pages are JS-rendered; individual profiles need browser verification | sydney.edu.au/architecture/about/our-people/academic-staff/{slug}.html |
| RMIT University | L3 (Cloudflare) | Cloudflare WAF blocks all curl access; browser required | rmit.edu.au/contact/staff-contacts/academic-staff/ |
| Deakin University | L3 (Cloudflare) | Cloudflare WAF blocks all curl access; browser required | deakin.edu.au/about-deakin/people/{slug} |
| University of Queensland | L3 (JS SPA) | Researchers portal is JS-rendered; browser required | researchers.uq.edu.au/researcher/{id} |
| Adelaide University | L3 (JS SPA) | Researchers portal is JS-rendered; browser required | researchers.adelaide.edu.au/profile/{slug} |
| UTS | L3 (Cloudflare) | Cloudflare/Imperva blocks all curl access; browser required | profiles.uts.edu.au/{slug} |
| Macquarie University | L2 | Researchers portal may be accessible | researchers.mq.edu.au/en/persons/{slug} |
| Curtin University | L2 | Staff portal may be accessible | staffportal.curtin.edu.au/staff/profile/view/{slug}/ |
| The University of Newcastle | L2 | Staff profiles may be accessible | newcastle.edu.au/profile/{slug} |

### Vika School IDs (in dstMNzQU9Aa58DpgW3)
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

### Melbourne findanexpert URL Pattern Change (2026-07-01)
- **Old pattern**: findanexpert.unimelb.edu.au/profile/{id}-{name-slug} → **BROKEN** (404)
- **New pattern**: findanexpert.unimelb.edu.au/display/person-{name-slug} → Works (6183b SPA shell)
- **Discovery**: The /profile/ path was deprecated. All profiles moved to /display/person-{slug}.
- **Verified**: 2026-07-01

### Melbourne findanexpert — CRITICAL URL Pattern Update (2026-07-01)

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

