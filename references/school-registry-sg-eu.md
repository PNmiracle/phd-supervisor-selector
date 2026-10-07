# Registry: sg-eu

> 本文档由 `school-strategies.md` 于 2026-10-07 拆分而来；入口请见 `school-strategies.md`。

## 🇸🇬 Singapore

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

## 🇪🇺 Europe

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
