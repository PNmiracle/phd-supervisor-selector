# 访问框架与通道路径

> 本文档由 `school-strategies.md` 于 2026-10-07 拆分而来；入口请见 `school-strategies.md`。

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
