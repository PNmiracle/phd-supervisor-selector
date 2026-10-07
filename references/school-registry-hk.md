<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载 -->
> **本文含**：香港各校逐校情报（访问架构、可用通道、已知坑），含港城/港理/浸会三校抓取口径。
> **什么时候读**：目标校在香港时，按校名 grep 定位对应条目。
> **什么时候不用读**：目标校不在香港；⚠️ 禁止整读，必须先用校名定位。

> 本文由 `school-registry-hk-mo-cn.md` 于 2026-10-07 按地区拆分而来；总入口见 `school-strategies.md`，本地区入口见 `school-registry-hk-mo-cn.md`。
---

## 🇭🇰 Hong Kong

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

**⚠️ 新闻与传播学院官网整体下线（2026-09-20 发现，重要）**
- `www.com.cuhk.edu.hk` 与 `pg.com.cuhk.edu.hk` **整站处于 "website is temporarily unavailable" 状态**：根域返回 **167 字节**的占位页（`w_main.jpg` + alt 提示），所有 `/people/*`、`/?p=*` 路径统一 404 或返回同一占位页
- ⚠️ **这是"200 空壳"陷阱**：`pg.com.cuhk.edu.hk/?p=45/` 返回 **HTTP 200**，但正文只有 167 字节 → **按状态码判定链接健康的脚本会漏掉它**。遇到同一学院的链接，必须**同时校验字节数**（<1KB 视为空壳）
- ✅ **有效替代**：
  - 个人页 → `https://research.cuhk.edu.hk/en/persons/{name-slug}`（如 `ying-him-anthony-fung`，含姓名+职称+学院）
  - 学院人员/组织页 → `https://research.cuhk.edu.hk/en/organisations/school-of-journalism-and-communication/`
  - 研究生项目/招生页 → `https://www.gs.cuhk.edu.hk/programmes`（研究生院项目总表；注意 `gs.cuhk.edu.hk/admissions/programme/{dept}`、`/programmes/social-science/mphil-phd-communication` 等具体路径均为 404）
  - 全院教师名录（含职称与邮箱）→ `https://www.cpr.cuhk.edu.hk/tc/news-centre/experts-list/...`
- 已在表中修复的实例：Anthony Y. H. Fung（馮應謙）三个链接全部迁移到上述替代页

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
- **WAF 现状（2026-07-13 验证；2026-08-04 修正）**:
  - CityU 全站 Incapsula WAF，自动化工具（curl、Python urllib、WebFetch）**全部被拦截**
  - stfprofile 页面：200 返回 Incapsula JS 挑战页（约 200-1000 字节），不是真正死链
  - scholars.cityu.edu.hk：**403 Forbidden**（自动化访问），浏览器正常
  - **自动化审计脚本检测 CityU 链接时必然全部报死链/SPA壳，这是已知的系统性问题**
  - 不要因为 WAF 拦截就删除记录；但也**不要因为 403 就假设链接有效**（见下条修正）
- 🔴 **403 有两种可能（2026-08-04 修正，务必区分）**:
  - ① 正常教授页面被 WAF 拦截 → **有效**
  - ② **离任/已离职教授的页面已删除** → **失效**（WebFetch 穿透 WAF 后显示 "The page does not exist"）
  - 因此「403 就放过」是错的：**必须用 WebFetch 穿透看正文**，不能用状态码下结论
- 🔴 **离任导师检测三步（2026-08-04 沉淀，Maurice Benayoun 案例）**:
  1. **WebFetch 穿透 WAF**：`WebFetch("https://scholars.cityu.edu.hk/en/persons/xxx")` — 若返回 "The page does not exist" / "Page not found"，该学者主页已删除，高度怀疑离任
  2. **查 CityU 学术人员目录**：`https://www.cityu.edu.hk/zh-hk/directories/people/academic?page=N` — 若标注 **Visiting Professor** / **Adjunct Professor**，通常是离任后保留的挂名身份
  3. **查系级现任教职员列表**：如 `https://www.scm.cityu.edu.hk/people` — 若现任教授/副教授/客座/兼任各分组均无此人，基本确认离任
  - **辅助手段**：WebSearch `"[导师名] [原校] 教授"` 看是否已转校。**已离任导师不进入主表，已写入的需删除。**
  - 案例经过与旁证见 `cases-rules.md` B3
- **Primary workflow — Scholars Portal (ALL departments, mandatory)**:
  1. 浏览器打开 https://scholars.cityu.edu.hk/en/persons/ — CityU 统一教师数据库
  2. 搜索导师姓名
  3. 打开个人页面，复制 URL（格式: `scholars.cityu.edu.hk/en/persons/{name}({uuid})`）
  4. 写入 Vika 的 `导师主页` 列
  5. **备用格式**: stfprofile 页面 `www.cityu.edu.hk/stfprofile/{slug}.htm`，优先级高于 scholars（因为至少返回 200 而非 403）
  - 两种格式的分工：**scholars** 是 Pure Portal 全校统一入口，信息更完整（评价、论文、任职史齐全），但自动化访问返回 403；**stfprofile** 是旧版院系页，信息较少但至少返回 200
  - 选择策略：两种都能用，写入优先 stfprofile；用 scholars 的必须在写入后 WebFetch 穿透验证内容
- **写入后复验规则（WAF 调整版）**:
  - WebFetch 验证 CityU 链接时，预期返回：stfprofile → 200 + ~200-1000字节（JS挑战）；scholars → 403
  - 以上两种结果**都不是死链信号，但也都不是「有效」的证据** → **必须 WebFetch 穿透 WAF 确认正文含该导师姓名/职称/院系**
  - **删除记录条件**：Google/DDG 搜不到该导师、系页面已移除、浏览器确认 404、**或官方目录已无此人（离任）**
  - 交付前提示用户在浏览器中抽查 CityU 链接（特别是 scholars 格式）
- **自动化审计的 CityU 豁免**：
  - 计算链接通过率时，可将 CityU 记录从分母中扣除
  - 例如：55 条中 15 条 CityU，非 CityU 40 条全通过 → 实际链接率 100%（而非 73%）
  - WAF 拦截 ≠ 链接质量缺陷；但**豁免只针对状态码，不豁免离任检测**
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

#### ⚠️ PolyU 建设及环境学院（FCE）2026-07-01 大重组 —— 旧系名已失效（2026-10-07 实测）

**这是检索港理工建设类方向必须先知道的事**：旧 `polyu.edu.hk/bre/` 与 `polyu.edu.hk/lsgi/` 会 301 跳转，按旧系名/旧路径检索会走空。

| 变更前 | 变更后（2026-07-01 起） | 官网 |
|---|---|---|
| Department of Building and Real Estate (BRE) | **Department of Construction Management and Intelligence (CMI)** 建设管理及智能学系 | `https://www.polyu.edu.hk/cmi/` |
| Department of Land Surveying and Geo-Informatics (LSGI) | **Department of Land Surveying and Geospatial Science (LSGS)** 土地测量及地理空间科学系 | `https://www.polyu.edu.hk/lsgs/` |
| （新设） | **Department of Architecture (ARCH)** | `https://www.polyu.edu.hk/arch/` |
| 不变 | CEE（土木及环境工程）、BEEE（建筑环境及能源工程） | `/cee/`、`/beee/` |

- **公告来源**：`https://www.polyu.edu.hk/fce/news-and-events/news/2026/ebulletin-188-cs/`
- **FCE 师资与博士页通用规律**（2026-10-07 实测，**curl 可直读，无需浏览器**）：
  - 师资：`https://www.polyu.edu.hk/{dept}/people/academic-staff/`（**必须带尾部斜杠**；不带会 301）
  - 个人页：`https://www.polyu.edu.hk/{dept}/people/academic-staff/{slug}/`
  - 博士项目页路径**各系不统一**，实测：
    - CMI：`/cmi/study/research-postgraduate-programme/`（**单数 programme**，复数 404）
    - BEEE：`/beee/study/research-postgraduate-programme/`
    - ARCH：`/arch/study/research-postgraduate-programme/`
    - CEE：**不同路径** → `/cee/prospective-students/research-postgraduate-programme/`
    - LSGS：**不同路径** → `/lsgs/study/rpg-scheme-item---research-postgraduate-programme/`
- **研究领域提取**：CMI/BEEE/LSGS 等系个人页常**没有 Research 板块**，页面正文只有 `Research Overview`（有则优先）或 `Biography`；再没有就取该页链接的 **PolyU Scholars Hub**（`https://research.polyu.edu.hk/en/persons/<uuid>`）的 `Fingerprint` 关键词，并在字段里**注明来源**。⚠️ LSGS 个人页有 `Research Overview` 板块，但**列表页不显示研究领域**，必须逐个进个人页。
- **Research Assistant Professor 要剔除**：PolyU 各系师资页把 RAP 与 Professor/Associate Professor/Assistant Professor 混排（CEE 一个系就有 47 位 RAP），职称字段只写 `Research Assistant Professor`，按规则不进主表。
- **Last verified**: 2026-10-07
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

#### 🇭🇰 香港六校 · 人文/电影方向抓取路径（2026-09-11 验证，姜一丁任务沉淀）

**这六个学校的「电影/影像/文化研究」院系路径与上面记录的心理/商科路径完全不同，按此表走可直接抓到。**

| 学校 | 院系 | 教师列表页 | 个人页格式 | 备注 |
|------|------|-----------|-----------|------|
| HKU | Comparative Literature | `complit.hku.hk/index.php/faculty/` | `complit.hku.hk/index.php/faculty/{slug}/` | 静态页可抓；**`www.complit.hku.hk` 不可达，必须用无 www 域名** |
| HKU | School of Modern Languages (SMLC) | `www.web.smlc.hku.hk/teachingstaff` | `www.web.smlc.hku.hk/teachingstaff/{slug}` | Wix 站，页面约 1MB，正文在 JSON 内嵌结构里，需正则从 `wixui-rich-text` 附近提取 |
| CUHK | Cultural and Religious Studies | `www2.crs.cuhk.edu.hk/tc/faculty-staff/teaching-faculty` | `www2.crs.cuhk.edu.hk/tc/faculty-staff/teaching-faculty/{slug}` | 静态页，研究兴趣在「研究興趣」段 |
| CUHK | Chinese Language and Literature | `www.chi.cuhk.edu.hk/en/people/` | `www.chi.cuhk.edu.hk/profile/prof-{slug}/` | 博士页 `www.chi.cuhk.edu.hk/study/phd-in-chinese-language-and-literature/` |
| CUHK | Journalism and Communication | `www.com.cuhk.edu.hk/en/people/` | `www.com.cuhk.edu.hk/people/{slug}/` | **学院站是 JS 渲染（多个路径返回同一 157KB 壳）**；博士招生页用 `pg.com.cuhk.edu.hk/?p=45/`（`/phd/`、`/rpg/` 均已 404） |
| HKUST | Division of Humanities | `huma.hkust.edu.hk/about/faculty` | `huma.hkust.edu.hk/people/{slug}` | 静态页；博士页 `prog-crs.hkust.edu.hk/pgprog/2026-27/mphil-phd-huma/` |
| HKUST | Division of Arts and Machine Creativity (AMC) | `amc.hkust.edu.hk/faculty` | `facultyprofiles.hkust.edu.hk/profiles.php?profile={slug}` | **facultyprofiles 不是 SPA 空壳，可抓到 Research Interest 与 RPG Supervision**；AMC 博士页只有 `amc.hkust.edu.hk/mphil-phd-program-program-objective`（`/programmes`、`/study`、`/academics` 全 404） |
| PolyU | Chinese History and Culture (CHC) | `www.polyu.edu.hk/chc/people/academic-staff/?sc_lang=en` | `www.polyu.edu.hk/chc/people/academic-staff/dr-{slug}/` | **本次 curl 直接抓到完整内容，非 JS 渲染**；博士页 `www.polyu.edu.hk/study/pg/rpg/2027/chc` |
| PolyU | English and Communication | `www.polyu.edu.hk/engl/people/academic-staff/` | `www.polyu.edu.hk/engl/people/academic-staff/prof-{slug}/` | 博士页 `www.polyu.edu.hk/study/pg/rpg/2027/engl` |
| PolyU | School of Design | `www.polyu.edu.hk/sd/people/academic-staff/` | `www.polyu.edu.hk/sd/people/academic-staff/{slug}/` | 博士页 `www.polyu.edu.hk/sd/study/rpg/phd` |
| CityU | School of Creative Media (SCM) | `www.scm.cityu.edu.hk/people/` | `www.scm.cityu.edu.hk/en/people/{slug}` | **本次 curl 全部返回 200 + 完整内容，未触发 Incapsula WAF**；博士页 `www.scm.cityu.edu.hk/en/programmes/postgraduate/phd`（含潜在导师名单） |
| CityU | Chinese and History (CAH) | `cah.cityu.edu.hk/people/academic-staff` | `scholars.cityu.edu.hk/en/persons/{slug}` | 研究学位页 `cah.cityu.edu.hk/en/programmes-courses/postgraduate/research-degree` |
| CityU | ACIM（跨学科中心） | — | `www.acim.cityu.edu.hk/people/{slug}` | SCM 老教授的页面可能只挂在 ACIM 下 |
| HKBU | Academy of Film | `af.hkbu.edu.hk/en/about-af/people.html` | `af.hkbu.edu.hk/en/about-af/people/{slug}.html` | 有独立研究型 MPhil/PhD（与 MFA 分开）：`gs.hkbu.edu.hk/programmes/doctor-of-philosophy-master-of-philosophy-academy-of-film` |
| HKBU | Humanities and Creative Writing | `hmw.hkbu.edu.hk/people/` | `hmw.hkbu.edu.hk/people/{slug}/` | 博士页 `gs.hkbu.edu.hk/programmes/...department-of-humanities-and-creative-writing` |
| HKBU | 传理学院 / 互动媒体系 | `www.hkbu.edu.hk/content/gda/en/faculty-member/_jcr_content` | `www.hkbu.edu.hk/content/gda/en/faculty-member/{Slug}/_jcr_content` 或 `imd.hkbu.edu.hk/faculty-member/{Slug}.html` | **`comm.hkbu.edu.hk` 会 302，不要用**；邮箱内嵌在 AEM 的 JSON 中需正则提取 |

**跨校通用教训（2026-09-11）**：
1. **个人页存在 ≠ 仍在职**。HKU 比较文学系个人页会残留已离任教师的旧页面（例：Magnan-Park，个人页仍 200，但 2025-26 现任名单已无此人）。**必须把个人页与院系「现任教师名单」交叉验证**，名单里没有的不要写入；已写入的删除。判断现任名单可用：HKU People 页（会标注 "The academic year of 2025-26"）、HKBU `expert.hkbu.edu.hk`、CityU SCM `/people/` 与博士页潜在导师名单。
2. **`www.` 前缀可能是致命差异**：HKU 比较文学系 `www.complit.hku.hk` 全部连接失败，去掉 www 后全部 200。
3. **CUHK 各系 URL 结构毫无统一规律**：Cultural Studies 在 `www2.crs.cuhk.edu.hk`、中文系在 `www.chi.cuhk.edu.hk`、传播学院在 `www.com.cuhk.edu.hk` 且为 JS 渲染。必须逐系从官网首页抓导航链接，不要照搬其他系的格式。
4. **HK 地区职称门槛**：助理教授（Assistant Professor）及以上；`Lecturer`/`Senior Lecturer`/`Teaching Fellow`/`Instructor`/`Professor of Practice`/`Research Assistant Professor`（除非页面明示可带博）一律排除。
5. **⚠️「姓名不在院系列表页」不能直接判定离职（2026-09-11 复核沉淀）**：验证在职状态时，用院系现任名单反查姓名会大量假阴性，常见原因有三类 ——
   - **Wix 站点分块加载**：HKU SMLC `www.web.smlc.hku.hk/teachingstaff` 每次只返回前 10 个 slug（实测 3 次均为 auer-stefan…fichter-james），后面的教师永远抓不到
   - **SPA / JS 渲染**：CUHK 中文系全站、CUHK 新闻与传播学院站、CityU 部分页面，HTML 里根本没有教师姓名文本
   - **列表页只覆盖部分类别**：HKBU 电影学院 people 页不列 Ying Zhu，但 HKBU 官方专家目录列她
   因此判断链应为：**列表页命中 → 在职（可靠）；列表页未命中 → 换第二条通道再判**，第二条通道优先级：① 个人页是否含 2024/2025/2026 年份痕迹、在研项目、当年度课程 ② 学校官方专家目录（如 `expert.hkbu.edu.hk`）③ 官方研究门户的项目/奖项时间线（如 `research.cuhk.edu.hk`）④ 院系 news/活动页近期本人出现记录。**只有四条通道都指向"已离开"时才删记录。**
6. **不要凭终端打印的大段中文多字段输出判断数据错乱**：批量打印「导师/领域/备注」时输出可能错位串行，看起来像字段张冠李戴。必须按 recordId 精确读取（`GET /records?recordIds=recX`）或做程序化 source-vs-table diff 才能确认。本项目曾据此误报一次「备注串行」P0，实际数据完全正确。
7. **邮箱挖掘的三条高效通道（2026-09-14 沉淀，一次任务补齐 13 位邮箱）**：各校官网常把教师邮箱藏起来，按以下顺序找命中率最高 ——
   - **① 学者库/专家名录个人页**（最高命中）：`scholars.hkbu.edu.hk/en/persons/{CODE}/`、`expert.hkbu.edu.hk/en/list/detail/{id}`、`faculty.uci.edu/profile/?facultyId=` 等，这些页面通常直接列 Email，HKBU 学者库还会带 **"Accepting PhD Students"** 徽标（是判断带博资格的一手证据）
   - **② 院系官方教师名录页**（第二命中）：如 `arts.ucdavis.edu/cinema-and-digital-media/faculty`、`cah.cityu.edu.hk/people/academic-staff` 会把全系邮箱列成表；单个人的 profile 页反而可能是 5KB 空壳，此时**要退回到"整系名录页"而不是纠缠个人页**
   - **③ 防爬混淆还原**：HKBU 的 AEM 页面把邮箱写成 `kwaiclo at hkbu.edu.hk`（用 " at " 替代 @），部分站点用 `[at]`/`(at)`/HTML 实体 `&#64;`。抓取脚本必须先做 `.replace(' at ','@')` 之类的还原再匹配，否则会误判"页面没有邮箱"
   - **反面案例**：Sussex 个人页与 vCard 都空（学校未公开）、中戏官网只有学校总邮箱 `zhongxi@zhongxi.cn`（个人邮箱不公开）——这类就不该填，留空并在备注写明可行路径
   - **警惕同名误抓**：抓 US 高校页面时会出现 `or-web-support@`、`rfa@`、`pafs-teach-coord@` 等院系公共地址，必须按"个人职称/姓名 + 域名"筛选，不要把公共地址填成个人邮箱



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
- **PhD link**: https://gs.eduhk.hk/prospective/rpg/ （⚠️ 2026-09-14 更新：旧记录 `eduhk.hk/gradsch/` 已不是招生页；`gs.eduhk.hk` **curl 会 SSL 握手失败，必须用 WebFetch**）
- **Failed**: Previous attempt via network blocked; browser works
- **Last verified**: 2026-06-26

#### 🇭🇰 香港「非前五」院校 · 设计/艺术/文化方向路径（2026-09-14 验证，刘静仪任务沉淀）

**先确认 PhD 开设情况再决定是否搜索（这几所经常白跑）：**

| 学校 | 是否有 PhD/MPhil | 证据 |
|------|-----------------|------|
| HKBU 浸会 | ✅ MPhil/PhD（视觉艺术 / 历史 / 人文创作 / 传理 / 电影各自独立） | `gs.hkbu.edu.hk/programmes/doctor-of-philosophy-master-of-philosophy-{unit-slug}` |
| EdUHK 教大 | ✅ PhD + MPhil（培养领域含 cultural and creative arts） | `gs.eduhk.hk/prospective/rpg/` |
| Lingnan 岭南 | ✅ MPhil/PhD（原视觉研究系已改组为 DACI） | `ln.edu.hk/daci/programmes/postgraduate/postgraduate`；文科入学要求 `ln.edu.hk/rpg/admission/requirement/additional-admission-requirements` |
| HKMU 都大 | ✅ MPhil + PhD（5 学院可招；商学院**不**强制 GMAT/GRE） | `hkmu.edu.hk/admissions/research-postgraduate/`；学院级 RPg 页 `admissions.hkmu.edu.hk/rpg/{as,ba}` |
| HKSYU 树仁 | ✅ MPhil/PhD，但**仅 6 个学科**：Chinese / Economics / English / History / Psychology / Sociology；新闻传播、商科、法律**无**研究型学位；社工与应用数据科学**只能做 Co-supervisor** | `gs.hksyu.edu/en/Programmes/ResearchPostgraduateProgramme`；**权威导师名单**：`gs.hksyu.edu/zh_hk/Thesis%20Supervisor`（写记录前必查） |
| HSUHK 恒生 | ❌ 无 PhD/MPhil。唯一博士层级课程是 Doctor of Decision Analytics（专业博士，要求 3 年工作经验，方向为统计/计算机/供应链） | `gs.hsu.edu.hk/en/programmes-on-offer/` |
| HKAPA 演艺 | ❌ 无 PhD，只有 6 个硕士（MFA/MMus/MA） | `hkapa.edu/sch/postgrad` |
| 圣方济各大学 | ❌ 无研究型学位 | `sfu.edu.hk/tc/admission/programmes-by-qflevel/index.html` |
| 东华学院 TWC | ⚠️ 只有 PhD in Nursing，与人文/设计方向无关 | `twc.edu.hk/en/Programmes/phdn` |

**HKBU 路径（2026-09-14 实测全部 200 且可抓正文）**
- Academy of Visual Arts：列表页 `ava.hkbu.edu.hk/en/academy/people-academic-staff` 是 **SPA 空壳（任意路径都返回同一 7577B）**，但个人页 `ava.hkbu.edu.hk/en/academy/academic-staff/{slug}` 是静态可抓（10–14KB）→ **列表页拿不到就直接搜索定位个人页**
- Academy of Film：列表 `af.hkbu.edu.hk/en/about-af/people.html`；个人 `af.hkbu.edu.hk/en/about-af/people/prof-{slug}.html`；博士页 `af.hkbu.edu.hk/en/programmes/phd-mphil.html`
- Humanities and Creative Writing：列表 `hmw.hkbu.edu.hk/people/staff`；个人 `hmw.hkbu.edu.hk/people/dr-{slug}/`
- Interactive Media：列表 `imd.hkbu.edu.hk/faculty-member.html`；个人 `imd.hkbu.edu.hk/faculty-member/{Slug}.html`
- History：个人 `histweb.hkbu.edu.hk/about-us/people/prof-{slug}.html`；⚠️ 列表页 `histweb.hkbu.edu.hk/about-us/people.html` 是**分 tab 渲染**，WebFetch 常只渲染出 PhD Student 区块而看不到学术职员——**别据此判定它不是教职员列表页**（页面源里有 22 处 Professor）
- 跨学科研究门户（系页找不到某人时的兜底，信息比系页全）：`interdisciplinary-research.hkbu.edu.hk/people/{slug}`
- 专家目录（判断在职状态的第二通道）：`expert.hkbu.edu.hk/en/list/detail/{id}/`
- **补邮箱 + 判断带生意愿最快的通道（2026-09-14 验证）**：`scholars.hkbu.edu.hk/en/persons/{SLUG}/` 含 `Email xxx@hkbu.edu.hk` 与 `Accepting PhD Students` 标记，curl 抓不到（JS 混淆），但用 `WebSearch(query='"{姓名}" HKBU Email', allowed_domains=['scholars.hkbu.edu.hk'])` —— **搜索结果摘要会直接带出邮箱和 Accepting PhD 标记**。AVA 系个人页大多不印邮箱，只有这条路能补全。

**Lingnan 路径**
- ⚠️ **旧记录「ln.edu.hk/daci 返回 234 bytes 不可达」已失效**：2026-09-14 实测 `ln.edu.hk/daci/staff/faculty`（89KB）、`.../faculty/prof-{slug}`、`ln.edu.hk/daci/programmes/postgraduate/postgraduate` 全部正常可抓
- History：列表 `ln.edu.hk/history/people/`；个人 `ln.edu.hk/history/people/{slug}`
- Philosophy：列表 `ln.edu.hk/philoso/people/faculty`；个人 `.../faculty/{slug}`
- Marketing：列表 `ln.edu.hk/mkt/faculty-staff/research-areas`；个人 `.../staff-list/{slug}`

**EdUHK 路径**
- CCA（文化创意艺术）：列表 `eduhk.hk/cca/en/people`；个人 `eduhk.hk/cca/en/people/academic-and-teaching-staff?id={数字}`（**query id 而非 slug，必须搜索获取**）
- Chinese Language Studies：列表 `eduhk.hk/chl/en/people`（`/chl/en/staff`、`/chl/en/people/academic-staff` 均 404）
- Literature and Cultural Studies：列表 `eduhk.hk/lcs/people`
- 个人详情备用通道：`pappl.eduhk.hk/rich/web/person.xhtml?pid={数字}`（校内官方档案系统，含完整发表列表）

**HKMU 路径**
- ⚠️ `hkmu.edu.hk/ca/{slug}` 与 `scholars.hkmu.edu.hk` 对 curl 返回 **403 Cloudflare 挑战页 / 503**，但 **WebFetch 可完整读取**
- 可用模板：`hkmu.edu.hk/staff-profile?email={账号}`（如 `?email=evaman`）——curl 403，**必须用 WebFetch 验证**；能读到姓名+职称+研究兴趣即算有效个人页
- 学院级 RPg 研究兴趣页（判断能否带博 + 快速拿到导师研究方向）：`admissions.hkmu.edu.hk/rpg/as`、`/rpg/ba`

**HKSYU 路径**
- Sociology：列表 `sociology.hksyu.edu/en/Staff`；个人 `sociology.hksyu.edu/en/Staff/detail/{URL-encoded 姓名}`
- History：列表 `history.hksyu.edu/en/teaching%20staff%20new`；个人 `.../detail/{NAME}`
- ⚠️ HKSYU 的艺术史/博物馆/数字媒体师资多挂在 **Sociology 系**（该系同时承载 Arts, Culture and Technology 课程），不要因为「做艺术的人在社会学系」就判为错误
- ⚠️ `Professor of Practice` 通常排除，但若其名字出现在 `gs.hksyu.edu/zh_hk/Thesis%20Supervisor` 官方导师名单上，可保留并如实标注该职称
- ⚠️ 树仁 MPhil/PhD in Sociology 要求「社会学学士（MPhil）/ 社会学或相关领域硕士（PhD）」，设计/时尚背景能否直入需向系方确认

**跨校教训（设计/艺术方向）**
1. **「可持续/环境」≠ 可持续设计**：环境科学（城市气候、空气污染、GIS）与可持续时尚/人本设计只有「可持续」一词重叠，属不同学科。除非方向书明确含 ESG/环境，否则不要收。
2. **传统经学/文献训诂 ≠ 物质文化**：不要因为某学者写过一两篇「传统纹饰」「礼仪动画」的科普短文就归入文化遗产方向；以主页 Research Interests 列表为准。
3. **商科强制 GMAT/GRE 是常见红线**，提交前必须逐校读 RPg 入学要求原文：岭南明写 "The GMAT/GRE test is not mandatory"；HKMU 商学院 RPg 无 GMAT/GRE 要求；HKBU 商学院则**强制**——勿凭印象判断。


## 🇭🇰 港城 / 港理 / 浸会 三校抓取口径（2026-09-24 黄肇启案例沉淀）（自 SKILL.md 迁入 2026-10-07）


#### 港城 CityU
- 商学院各系 people 页路径**不统一**：`/is/people/academic-staff` ✅；`/MKT/about/people/` ✅（注意大写 MKT；`/mkt/people/` 404）；`/mgt/people/`、`/mgt/faculty` 一律 **400**；`/mgt/about-us/faculty-staff` 是 JS 空壳（无姓名）。`www.cb.cityu.edu.hk/sitemap.xml` 只收录 229 个 URL，不含各系 people 页。
- **IS 名单页用 `data-eid` 属性给出 eid** → 个人页 = `https://www.cb.cityu.edu.hk/staff/<eid>/`，curl 可直接读到 `Research Areas` 原文（正文形如 `E-mail: … Research Areas <area1> <area2> … <bio>`）。
- **管理系没有师资名单页** → 用 `https://www.cb.cityu.edu.hk/mgt/research/research-expertise`（含全部 18 位教师姓名 + 研究方向关键词），可作「其他导师信息」并在交付说明里注明。
  - ⚠️ **更正（2026-09-24 复核）**：管理系**有**正式师资名录页 `https://www.cb.cityu.edu.hk/en/mgt/about-us/faculty-staff`（导航 About Us › Faculty & Staff，Drupal view `faculty_staff_listing_new-block_1`）。该页静态 HTML 里结果容器为空、curl 读不到姓名，但**真实浏览器渲染正常**（已用 `agent-browser open` + `snapshot` 确认：完整列出全部教师、职称与研究方向）。**`其他导师信息` 应填这个名录页，不要填 `research-expertise`**——审核会把它判为「研究专长页」不合格。JS 渲染页「curl 读不到」不等于坏链，用 agent-browser 判定，不要因为抓不到就换页。
- 数据科学系 `https://www.ds.cityu.edu.hk/en/people/academic-staff` 只有名单 + `Research Interest:`，**无个人页**（`/people/academic-staff/<slug>` 均返回 Page Not Found）→ 个人页改挂 `scholars.cityu.edu.hk`。
- 🔴 **scholars slug 撞名陷阱**：`scholars.cityu.edu.hk/en/persons/<slug>` 是 **curl 可读**的（只有 `/organisations/...` 与 `?search=` 会被 Cloudflare 403）。但同名者极多——`xinyue-li` 是物理系 PhD 学生，数据科学系副教授实际是 `xinyue-li-2`。**核验时必须断言页面里的院系字段**，只匹配姓名会写错人。
- Incapsula 拦截（200 + ~850B 挑战页，curl 读不到正文）：`www.cityu.edu.hk/stfprofile/<eid>.htm`、`www.cityu.edu.hk/ph/staff/<slug>`、`www.cityu.edu.hk/ph/education/...` → 改用 WebFetch（可读到完整正文）。
- 系级博士项目页（可直接连）：IS `/en/is/postgraduate-degrees/research-degrees/phd`；MGT `/en/mgt/programmes/research-degree`；MKT `/MKT/programmes/ResearchDegree/`；DS `www.ds.cityu.edu.hk/en/programmes/postgraduate-programmes/phd-programme-data-science`；PH `www.cityu.edu.hk/ph/education/research-degree-programme-phd`。
- ⚠️ **IDPH（传染病与公共卫生系）本质是兽医学院下的系**：官方 PhD 项目页写明培养 "specialist skills in the discipline of **veterinary medicine**"，招生研究领域为动物福利 / 水产生产 / 畜禽与水产动物健康 / 保护与野生动物医学。做人类健康或组织数字化的学生慎入，写入前先读项目页的 Research Areas 列表。

#### 港理 PolyU
- `polyu.edu.hk` 各系名单页 curl **带浏览器 UA** 可直读（无 UA 会 403 / 空壳）。
- 个人页正文含 `Research Interests: <原文>`；职称在正文职称行——**导航栏与列表页里出现的 "Professor" 字样不算**，别拿它判职称。
- 系级博士项目页：DSAI `/dsai/study/rpg/phd-and-mphil-in-data-science-and-artificial-intelligence/`；AMA `/ama/study/research-postgraduate-programme/`；HTI `/hti/study/programmes/research-postgraduate-studies/research-postgraduate-programme/`；RS `/rs/study/research-postgraduate-studies/phd-or-mphil/`；**SN 无院级 RPG 页** → 用 `/sn/teaching-and-learning/postgraduate-programmes/`（页内明列 MPhil / Doctor of Philosophy 53601）。
- AMA 的「统计组」几乎全是高维 / 半参 / 统计机器学习**方法论**，其余是优化、PDE、金融数学；真正偏行业应用者极少。若学生明确排除纯方法论，AMA 很可能整系落空——如实报告，不要凑人。

#### 浸会 HKBU
- `scholars.hkbu.edu.hk/en/persons/<ID>` 有 Research Interests，**但页面无邮箱**（`<ID>` 常为人名全大写或缩写，如 `DANIELLAI` / `CHITAT` / `VWPLEE`）。
- **系级名单页信息更全**（含职称 + `Research Focus:`），适合做「其他导师信息」：`sowk.hkbu.edu.hk/en/people/academic-staff.html`、`speh.hkbu.edu.hk/en/people/academic_and_teaching_staff/`、`geog.hkbu.edu.hk/people/academic-and-teaching-staff/`。
- 官方英文名注意：**Department of Sports and Health Sciences**（带 s，该系自身页面英文标题为准）。
- 系级博士页：SHS `/en/programs_and_courses/research_post_graduate_study/`（页标题 "Research Post-Graduate (Ph.D.)"）；Geography `/postgraduate/mphil-phd.html`；SOWK `/en/programmes/doctor-of-philosophy-master-of-philosophy.html`。
- **浸会没有公共卫生学院**：方向3 落地为 SHS（身体活动测量与流行病学、健康行为干预）、地理系（健康地理 · Geo-AI · 社会处方）、社工系（健康老龄化 · 长期照护 · 数字包容 · ICT 干预）。落到这些院系时，**必须在备注与交付报告里如实标注院系**，把边界交给用户裁定，不要假装它们属于公卫学院。

#### 三校博士门槛与招生轮次（2026-09-24 实测，可直接复用）

| 校 / 院 | GRE / GMAT | 招生轮次（原文口径） |
|---|---|---|
| 港城 **商学院** PhD | **无 GMAT/GRE**（`www.cb.cityu.edu.hk/ph/admission/` 全文无这两个词；门槛=硕士或一等荣誉学士 + 托福 85 / 雅思 6.5；录取获校级奖学金约 HKD 19,100/月） | 全年接受申请，每年两轮（January 与 April） |
| 港城 理学院 / 数据科学 / 公卫 | 无 | 同上（校级 RPG 口径） |
| 港理 RPG（含 DSAI / AMA / HTI / SN / RS） | **无 GMAT/GRE**（`www.polyu.edu.hk/study/pg/research-postgraduate/` 全文无这两个词） | 按学年挂出，例：Sept 2027 Entry 截止 30 Apr 2027 |
| 浸会 **商学院** | **必须提交 GMAT 或 GRE** — 官方原句 `School of Business: Please provide GMAT or GRE score upon application.`（`gs.hkbu.edu.hk/admission/research-postgraduate-programmes/application/admission-requirements`） | — |
| 浸会 其他学院（SHS / Geography / SOWK 等） | 无 | 2027/28 学年自 2026-09-01 开放；两轮截止 2026-12-01 与 2027-04-15 |

> 港城商学院 PhD 的 `preferred undergraduate majors` 表中，Information Systems / Management / Marketing 三项均不含 Statistics / Biostatistics（属偏好而非硬门槛，正式资格看硕士学历与英语）——统计背景学生投港城商学院时应在交付说明里提示这一点。

#### 抓取作业注意
- 串行抓 50+ 个页面在前台跑约 2 分钟会被 **SIGKILL（exit 137）** → 用 `run_in_background` 并把 stdout `tee` 到日志文件。
- 读长日志**不要用 `cat`/`tail -n 60`**（会被工具截断，误以为缺行）→ 用 Read 工具按 offset 分段读。

---
