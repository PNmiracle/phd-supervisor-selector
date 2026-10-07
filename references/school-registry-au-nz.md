<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：澳洲与新西兰院校逐校情报（各校访问架构、可用通道、已知坑）
> **什么时候读**：目标校在澳/新时，按校名 grep 定位对应条目
> **什么时候不用读**：目标校不在澳新；⚠️ 禁止整读，必须先用校名定位

---

# Registry: au-nz

> 本文档由 `school-strategies.md` 于 2026-10-07 拆分而来；入口请见 `school-strategies.md`。

## 🇦🇺 Australia

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
- **⚠️ 2026-09-20 实测修正**：
  - `findanexpert.unimelb.edu.au/profile/{数字ID}`（**不带 slug 也可以**）**WebFetch 可读**，能拿到姓名/职称/Research Interests 标签；curl 仍被 Cloudflare 拦（返回 6183B "Pardon Our Interruption"，所有 URL 字节数完全相同 → 典型拦截特征，不是死链）
  - `profileprint/{id}` 也被拦（"Pardon Our Interruption"）
  - 院系学术人员列表页 `arts.unimelb.edu.au/school-of-culture-and-communication/our-people/academic-staff` 与 `finearts-music.unimelb.edu.au/about-us/vca/academic-staff`：curl 403 "Just a moment..."，但**WebFetch 可读全文（含每人的电话与邮箱）**——找邮箱首选这两页
  - **VCA 有非标准编目职称**：教学岗在名录上可能写成 `Specialist in Directing` / `Specialist in Movement` 这类（实例 Kat Henry / Colin Sneesby），而校方其他页面（如 study.unimelb 课程页）又称其为 Lecturer。**判职称时两者都要看，并在备注里按页面实际表述写**；这类岗位的 HDR 带博资格通常无公开字段，按「未明确表明监督资格，可以后放～」处理
  - VCA 的 RHD 协调人在名录里写作 `Course Coordinator (Research Higher Degrees)`；影视系的研究生协调人写作 `Course Coordinator (Graduate Research)`

#### University of Sydney
- **Architecture**: Symplectic Elements Discovery portal (profiles.sydney.edu.au). All individual profiles and group pages are pure SPAs (2118 bytes shell). CSS/JS loaded dynamically.
- **Layer**: L3 (Symplectic Elements SPA)
- **Best method**: Main education page (sydney.edu.au/arts/schools/sydney-school-of-education-and-social-work.html) returns 67KB with some profile links embedded. Individual profiles require browser verification.
- **Key endpoint**: profiles.sydney.edu.au/{username} (SPA)
- **Failed**: All API paths (v1/api/individuals, api/rest/v1, etc.), model.json feeds, JSON/RDF format parameters, print view
- **Last verified**: 2026-06-30
- **✅ 2026-09-20 实测修正**：`profiles.sydney.edu.au/{名}.{姓}` 用 curl 只得 **2118B "Discovery" SPA 空壳**，但 **WebFetch 能渲染出完整正文**（含 BIO、研究领域、Availability 段落，如 "Research supervision"）——**这类人必须用 WebFetch，不要因 curl 空壳就判死**
  - 部分教师同时在 `sydney.edu.au/arts/about/our-people/academic-staff/{slug}.html` 有静态页，`sydney.edu.au/arts/staff/profiles/{名}.{姓}.php` 这类旧路径会被 WebFetch 自动跳转并渲染成功
  - **页首常只显示行政职务**（`Chair of Discipline`、`Associate Dean`），**职级（Lecturer / Senior Lecturer / Associate Professor）可能在 `/teaching` 子页或学科页**——不要因页首没写职级就判定信息缺失；判断现任职务时**以个人主页为准**（学科主席这类职务会换人，过去式表述要当心）
  - 学院级页面可 curl：`sydney.edu.au/arts/schools/school-of-art-communication-and-english/{film-studies|theatre-and-performance-studies}.html`、`.../sydney-college-of-the-arts.html`、`.../school-of-languages-and-cultures.html`（均 200/60-110KB）
  - ❌ 不可用：`sydney.edu.au/arts/about/our-people/academic-staff.html`（SPA 空壳）、`.../sydney-college-of-the-arts/academic-staff.html`（SPA 空壳）

#### UNSW Sydney
- **Architecture**: Adobe Experience Manager (AEM) SPA for listing pages. Individual staff profiles at unsw.edu.au/staff/{slug} return real content (100-500KB) with research data embedded in HTML. Research profile pages (research.unsw.edu.au/people/{slug}) also accessible. Main domain may trigger Cloudflare, but staff sub-pages consistently work with curl.
- **Layer**: L2 (Adobe AEM SPA, staff profiles accessible)
- **Best method**: Use known staff names to construct unsw.edu.au/staff/{slug} URLs. Parse HTML for research keywords, publications, grants. School of Education research strengths include "Sociology of education." VERIFIED 2026-07-01 with 6 profiles.
- **Key endpoint**: https://www.unsw.edu.au/staff/{slug}
- **PhD application**: https://www.unsw.edu.au/study/research-degrees
- **Note**: Ben Newell moved from UCL/others → UNSW; not at Carleton
- **Failed**: AEM model.json returns minimal structure only; Our People listing page is SPA; newsroom expert finder API returns HTML only; newsroom.unsw.edu.au/find-an-expert redirects/times out; research.unsw.edu.au/people search returns SPA
- **Last verified**: 2026-07-01
- **✅ 2026-09-20 实测**：个人页两条路径**都能直接 curl**：`www.unsw.edu.au/staff/{slug}`（100-235KB，标题即 "Associate Professor X"）与 `www.arts.unsw.edu.au/our-people/{slug}`。院系统一人员页 `www.arts.unsw.edu.au/our-people/`（269KB）与 SAM 的 `unsw.edu.au/arts-design-architecture/our-schools/arts-media/about-us/meet-our-people`（472KB）均可 curl
  - ❌ `unsw.edu.au/arts-design-architecture/our-schools/humanities-languages/about-us/meet-our-people` 为 404 → School of Humanities & Languages 的人改用 ADA 全院页 `arts.unsw.edu.au/our-people/`
  - ⚠️ 少数人只在 `www.unsw.edu.au/staff/` 有页、在 `arts.unsw.edu.au/our-people/` 没有（如 Miska Mandic）——**两条路径都要试**
  - ⚠️ **2026-09-20 重要发现：不要只扫 School of the Arts and Media，School of Art & Design（Paddington 校区）是独立的另一个学院**（含动画/VFX/沉浸式影像，以及 iCinema 互动电影研究中心），做影视/影像/动画方向时极易整体漏掉
    - 该院人员页：`https://www.unsw.edu.au/arts-design-architecture/our-schools/art-design/about/our-people`（**带 "Available to Supervise" 筛选器**）
    - 该院 HDR 导师登记册 PDF（含全部可带博导师）：`https://www.unsw.edu.au/content/dam/pdfs/ada/art-design/resources/2025-03-research/art-and-design-supervisor-register-november-2025.pdf`
    - 个人页同样走 `www.unsw.edu.au/staff/{slug}`
  - ⚠️ **`profile-available-to-supervise=1`** 是 UNSW 个人页上的带博资格标记，可作判定依据

#### The Australian National University (ANU) (2026-09-20)
- **Architecture**: Pure Portal。`researchers.anu.edu.au/researchers/{slug}` 是 **React SPA 空壳**；**`researchportalplus.anu.edu.au/en/persons/{slug}` 可直接 curl**（100-450KB，标题含姓名）
- **Layer**: L1（用 researchportalplus 域名绕开 SPA）
- **Key endpoint**: `researchportalplus.anu.edu.au/en/persons/{name-slug}`；院系页 `slll.cass.anu.edu.au/people/academics`、`cpas.anu.edu.au/people`（均可 curl）
- **PhD 项目页**: `cass.anu.edu.au/study/higher-degree-research/applications`
- **⚠️ 个人页含 `Registered to supervise` 字段**，是判断带博资格的现成依据
- ❌ `soad.cass.anu.edu.au/people`、`/people/staff`、`/about-us/people` 全部 404 → School of Art & Design 只能用学院首页 `soad.cass.anu.edu.au/` 当院系页
- **Failed**: `researchportalplus.anu.edu.au/en/organisations/*/persons/` 被 Cloudflare 拦（403）；School of Art & Design 无公开人员列表页
- **Last verified**: 2026-09-20

#### Monash University (2026-09-20)
- **Architecture**: Pure Portal。**个人页 `research.monash.edu/en/persons/{slug}` 可直接 curl**（75-130KB，标题含姓名），且页面含 `Accepting PhD Students` 徽标 —— **这是判断招生意愿的现成依据**
- **Layer**: L1
- **Key endpoint**: `research.monash.edu/en/persons/{name-slug}/`
- **PhD 项目页**: `www.monash.edu/arts/research/graduate-research`（curl 403，WebFetch 可读；`/arts/graduate-research` 会重定向到此）
- **⚠️ 戏剧单位已更名**：原 `Centre for Theatre and Performance` 的 Pure 组织页已 302 到 **`research.monash.edu/en/organisations/critical-theatre-performance/`**（旧的 `centre-for-theatre-and-performance/persons/` 显示 0 results）→ 院系/组织页用新 slug；
  - 但个人页上「所属组织」仍可能标注为 `Literary Studies` 或 `School of Languages, Literatures, Cultures and Linguistics` → **写 Department 时以个人页标注为准**
  - 旧路径 `monash.edu/arts/theatre-performance/our-staff` 已跳 Okta 登录页，不可用
- **⚠️ 职称字段值得核对**：页头（Pure 结构化字段）与简介自述可能不一致（实例 Anthony Moore 页头 Professor、简介自称 Associate Professor）→ **以页头字段为准**
- **⚠️ 姓名署名可能简化**：实例 Stacy Holman Jones 在 Pure 页署名为 `Stacy Jones`（邮箱仍为 Stacy.HolmanJones@monash.edu）
- **Failed**: `research.monash.edu/en/organisations/*/persons/` 与 `www.monash.edu/arts/*` curl 403（Cloudflare），但 WebFetch 可读全文
- **Last verified**: 2026-09-20

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

## 🇳🇿 New Zealand

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
