<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：2026-08 月度区域案例更新日志（英国戏剧/表演类、美国动物营养/野生生物类筛查）
> **什么时候读**：遇到该月同方向或同校的相似场景时，按校名或学生名 grep 定位
> **什么时候不用读**：当前任务与该月案例无关；⚠️ 禁止整读，必须先 grep 定位

---

# 区域案例更新日志 · 2026-08

> 自 `school-updates-log.md` 于 2026-10-07 按月拆分。索引见 `school-updates-log.md`。

## 🇬🇧 UK — Dance/Performance/Theatre Schools (2026-08-03, 秦嘉琪选导验证)

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
