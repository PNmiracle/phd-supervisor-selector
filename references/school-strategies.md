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
- **Architecture**: Imperva/Incapsula WAF (findanexpert.unimelb.edu.au) + Cloudflare (finearts-music)
- **Layer**: L3
- **Access**: BLOCKED — needs manual browser from user side
- **Key endpoint**: https://findanexpert.unimelb.edu.au/
- **Failed**: curl + browser both blocked
- **Last verified**: 2026-06-26

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
- **Architecture**: Static HTML staff profiles
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
