<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载 -->
> **本文含**：2026-08 批次补录的美国院校逐校情报（自 au-nz 分册迁回）。
> **什么时候读**：目标校是 2026-08 批次里的美国校时，按校名 grep 定位。
> **什么时候不用读**：目标校不在本册；⚠️ 禁止整读，必须先用校名定位。

> 本文由 `school-registry-us-ca.md` 于 2026-10-07 按批次拆分而来；总入口见 `school-strategies.md`，本地区入口见 `school-registry-us-ca.md`。
---

## 美国院校条目（2026-08 批次，自 au-nz 分册迁回）

> 这批条目原先被误置于 `school-strategies.md` 的「AU Schools Access Layer Summary」标题之下，2026-10-07 按地区分册时纠正归位。

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
