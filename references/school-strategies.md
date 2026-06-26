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
