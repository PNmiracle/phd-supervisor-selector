<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：香港 / 澳门 / 内地中外合办院校逐校情报，含港城港理浸会三校口径、PolyU 院系重组、合办校导师名单与语言门槛入口
> **什么时候读**：目标校在港澳或中外合办（UNNC / XJTLU / CUHK-SZ / BNBU-UIC / DKU / NYU Shanghai / HKUST-GZ）时，按校名 grep 定位
> **什么时候不用读**：其他地区；⚠️ 本文件 569 行、已超方案 500 行上限，禁止整读，必须先用校名定位

---

# Registry: hk-mo-cn

> 本文档由 `school-strategies.md` 于 2026-10-07 拆分而来；入口请见 `school-strategies.md`。

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

## 🇲🇴 Macau

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

## 🇨🇳 Sino-foreign Joint Programs

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

##### 🎯 HKUST(GZ) 研究方向 JSON 接口——SPA 破解（2026-09-21 验证，优先级最高）
**这是目前拿到港科广研究方向原文最快、最权威的方法，应优先于上文的替代来源与 WebSearch。**

```bash
# slug = faculty-personal-page/<SLUG>/<slug> 的最后一段（如 season / ningningding / shuosun）
curl -s "https://facultyprofiles.hkust-gz.edu.cn/api/itdcms-rpc/profile/primary/<slug>"
# 返回 JSON：data.profile.enName（姓名）+ data.resumes[resumeType=RESEARCH_INTEREST].detail[].content（研究方向原文）
```
- 前端调用方式见 `/js/app.237189e1.js`（`getFacultyByPrimaryKey`）。SPA 空壳页 + 此接口 = 完整个人资料。
- **必须用 `data.profile.enName` 校验身份**：slug 命中失败时接口会返回一个 **150+ 条的聚合兜底列表**（内容是港科广全体研究方向的并集），看起来"有数据"但完全不属于本人。`enName` 为空 = 未命中，该 slug 作废。
- slug 取自 WordPress 学域列表页里的个人页链接末段；DSA 用 `dsa.hkust-gz.edu.cn/faculty/`，社会枢纽 FTEC/IPE/UGOD 用 `soch.hkust-gz.edu.cn/academics/<thrust>/faculty/`（后者的名单是 JS 渲染，抓不到链接，见下）。
- ⚠️ **`RESEARCH_INTEREST` 字段可能是陈旧数据，必须以 `overviews`（Biography）交叉校验**。实例：Sung Hun KIM 的结构化字段存的是"程序员生产力／挖掘软件仓库／静态分析"（他早年的软件工程方向），而同一接口的 Biography 写的是"recommendation systems, neural search (NLP), source code generation"（现任方向）。**两者冲突时以 Biography 为准，且不要只凭结构化字段下结论。**
- 另外可用 `/api/itdcms-rpc/profile/primary/<slug>` 的 `person`/`jobs` 等字段核对职称与所在学域。

##### 🎯 HKUST(GZ) 社会枢纽（FTEC/IPE/UGOD）师资名单 API（2026-09-21 验证）
WordPress 站点，师资名单由 `ThrustFacultyData.js` 动态拉取，页面本身抓不到姓名。直接用其 REST 接口：
```bash
curl -s "https://soch.hkust-gz.edu.cn/wp-json/university/v1/getOfficialThrustList?affiliatedUnits=SOCIHUB&departmentPkCode=<code>"
# FTEC 金融科技        = 10011A10000000000H2S
# IPE  创新创业与公共政策 = 10011A10000000000H2U
# UGOD 城市治理与设计    = 10011A10000000000H2Y
# CNCC 碳中和与气候变化  = 10011A100000000259HQ
```
返回 `CURRENT_FACULTY_ADVISORS`（当届在册师资）+ `ACTING_HEAD`，每条含 `enName`/`name`/`email`/`jobs[0].jobEnName`（职称）/`schoolName`（博士院校）/`majorEnName`（博士专业）/`website`，可据此区分 tenure-track / Adjunct / Professor of Practice。

##### 🇭🇰 七校博士项目 GMAT/GRE 要求（2026-09-22 逐项目官方页面复核，可直接引用）

**判定口径（务必区分）**：
- **免 G** = 官方写 not required / optional；**或材料清单里根本不出现 GMAT/GRE**；**或 GMAT 仅作英语能力可选替代**（TOEFL/IELTS/GMAT 三选一）。
- **要 G** = 官方明确要求提交，或列为必需。
- 「考了加分」≠「必需」；「可用来顶英语成绩」≠「要考」。这两种都判免 G，但要在备注里写清口径。

**逐校结论（本项目实测）**

| 学校 | 校级页（发问时直接给这一页） | 结论 |
|---|---|---|
| HKU | `gradsch.hku.hk/prospective_students/application/admission_requirement` | 免 G，**仅两处例外**：Faculty of Business and Economics 要 GMAT/GRE；Psychology 系非心理学本科者要 GRE Subject Test in Psychology |
| CUHK | `gs.cuhk.edu.hk/admissions/requirements` | 免 G。校级页里 GMAT 只出现在**英语能力测试**列表（`GMAT: Band 21 (Verbal)`），无全校统一 G 要求；商学院为项目专属要求 |
| HKUST | `fytgs.hkust.edu.hk/admissions/Admission-to-Hong-Kong-Campus/submitting-an-application/admission-requirements` | 免 G。官方 RPg 指引原文：`Required only if there is a program-specific requirement on public examination achievements e.g. GMAT, GRE ... In general, only research programs in the School of Business and Management require GMAT/GRE` |
| PolyU | `polyu.edu.hk/study/pg/research-postgraduate/2023/admission-requirements-rpg` | 免 G（统一页只有 General + English 两节）。⚠️ **但统一页不覆盖院系级要求**——理大商科项目页（如 `…/rpg/2027/mm`）硬性写 `Others GMAT Focus Edition/ GMAT/ GRE results are required.` |
| CityU | `cityu.edu.hk/pg/research-degree-programmes/entrance-requirements` | 免 G。**唯一提 G 的地方是 College of Business 条目**：`A high score in GRE or GMAT with supporting proof will be an added advantage though this is not a mandatory requirement. Please note that individual Departments in the College may adopt a higher standard.` ⚠️ 商学院 Management 系页面用词更强（`strongly encouraged to take the GMAT or GRE`），仍非必需 |
| HKUST(GZ) | `fytgs.hkust-gz.edu.cn/admissions/before-submitting-an-application/documents-required/` | 免 G。材料清单第 5 项：`Public Exam Score Reports — Required only if there is a Program-Specific Requirement on public examination achievements, e.g. GMAT, GRE`。四个学域（DSA/FTEC/IPE/UGOD）项目页入学要求都只有 General + English 两项 |
| CUHK(SZ) | `gs.cuhk.edu.cn/en/page/26` | 免 G（GMAT 仅作英语三选一）。**但经管学院例外，见下** |

**⚠️ 最关键的坑：港中大（深圳）经管学院 6 个 MPhil-PhD 里只有 Management 免 G**

用同一个模板，肉眼比对「最低入学要求」末尾有没有这一条：
```
- Taken the GRE General Test or GMAT.
```
以及材料清单里有没有这一项：
```
GRE or GMAT score report
```

| 项目 | page id | 有无 "Taken the GRE General Test or GMAT" + 材料含 G | 判定 |
|---|---|---|---|
| Management | 3255 | ❌ 都没有 | **免 G** |
| Economics | 1957 | ✅ 都有 | 要 G |
| Finance | 1958 | ✅ 都有 | 要 G |
| Accounting | 1959 | ✅ 都有 | 要 G |
| Marketing | 2098 | ✅ 都有 | 要 G |
| Information Management and Business Analytics | 2107 | ✅ 都有 | 要 G |

**新增发现：港中大（深圳）人文社科学院有 5 个 MPhil-PhD 项目，均免 G**
- 项目：Applied Psychology / Global Studies / Urban Studies / Computational Social Science / Sustainable Development（另 Translation Studies 已暂停招生）。
- 官方站是**独立子域** `hsspg.cuhk.edu.cn`（不是 `hss.cuhk.edu.cn`），项目页 URL 规律：`hsspg.cuhk.edu.cn/en/<slug>/{requirements,application,phdadvisor}`，slug 为 `mphilphdap` / `mphilphdgs` / `mphilphdcss` / `mphilphdus` / `mphilphdsd`。
- 入学要求页只有学位门槛 + 英语；英语测试列表含 `GMAT: Band 21 (Verbal)` 但**只作可选项**，全页 `GRE` 出现 0 次。→ 免 G。
- **`phdadvisor` 页是前端渲染**，curl 拿不到导师姓名，需用 WebSearch 或各教师个人页（`myweb.cuhk.edu.cn/<slug>`）反查所属学部。

**⚠️ 港中大（深圳）人文社科学院「学院首页 ≠ 项目页」的坑**：`hss.cuhk.edu.cn/en` 是学院首页，**完全没有入学信息**，也没有指向项目页的导航链接（导航只有 Division 层级）。写表时「博士申请信息」必须用 `hsspg.cuhk.edu.cn` 的项目页，不要用学院首页。

##### 🎯 港中大（深圳）经管学院 SME 师资 JSON:API（2026-09-21 验证，含按学术领域筛选）
SME 的师资检索页是 Drupal + JS 渲染，直接抓页面拿不到姓名，但 **JSON:API 全开**：
```bash
# 全部师资（分页，每页 50）
curl -s 'https://sme.cuhk.edu.cn/jsonapi/node/teacher?page%5Boffset%5D=0&page%5Blimit%5D=50'
# 按学术领域筛选（academic_type 的 drupal_internal__target_id）
curl -s 'https://sme.cuhk.edu.cn/jsonapi/node/teacher?filter%5Bacademic_type.meta.drupal_internal__target_id%5D=31'
```
- **领域 term id**（取自 `/en/teacher-search` 的 Academic Field 下拉）：Accounting=161、**Economics=32**、Finance=33、**Management=31**、Marketing=34、**Information Systems & Operations Management=216**
- 每条 `attributes` 里可直接用：`title`（中文名）、`school_post`（职称/职务）、`research_field`（研究方向原文）、`body.value`（简介）、`email`、`cuhk_website_link.uri`（`myweb.cuhk.edu.cn/<slug>` 个人站）、`path.alias`（`/teacher/<id>`）
- **注意**：`academic_field` / `research_field` 在 `attributes` 里可能为 null，领域归属在 `relationships.academic_type`；`supervisor` 字段指的是**博士后的合作导师**，不是博士指导资格，别误读。
- **教师页 `sme.cuhk.edu.cn/en/teacher/<id>` 是 JS 渲染**（HTML 里读不到研究领域）→ 写表时 `导师主页` 优先挂 `myweb.cuhk.edu.cn/<slug>` 个人站，研究领域在个人站可读可核。

##### 港中大（深圳）经管学院管理学方向的实测结论（2026-09-21）
- MPhil-PhD in **Management** 的 16 位官方师资（学术领域=Management）集中在**组织行为、战略管理、创新创业、人力资源管理**（企业社会责任、非市场化战略、组织吸引力、伦理决策…），与"数据科学/机器学习/数据挖掘/金融量化"几乎无交集；全学院唯一沾边的是做**计算社会科学**的潘歆乐。
- 因此遇到"学生想走港中深管理（因为免 G）"的需求时，**先把这份名单和方向结论给学生看**，再决定是否收录，不要为了填满免 G 口子而把战略/OB 师资整批写入。
- 参考：管理学博士课程为 Microeconomic Theory / Organizational Behavior / Strategic Management / Research Methods in Behavioral Studies & Strategic Management / Econometrics，本质是管理学实证训练。

##### 港中大（深圳）与港城大 研究方向提取要点（2026-09-21 验证）
- **CUHK-SZ SDS 教师页**（`sds.cuhk.edu.cn/en/teacher/<id>`）：结构固定为 `Education Background → Academic Area → Research Field → Personal Website`，**"Research Field" 字段就是研究方向原文**；用"取 Biography 之前一段"的方式提取最稳（先找 `Biography` 位置再回看前 700 字符）。
- **CUHK-SZ HSS 教师页**：用 `Research Fields` 字段；教师个人站 `myweb.cuhk.edu.cn/<slug>`（部分页面 1KB 左右，够读 Education Background 与 Research）。
- **CUHK STA/SOC 教师页**：内容块的字段名是单数 `Research Interest`；页面导航里也有 `Research Areas`，**优先匹配单数形式并取最后一次出现**，否则容易抓到导航菜单。
- **CUHK-SZ 教师中文名不都在官网出现**（如 LI Yujie 页面只有英文名）→ 核不到中文名时用官方英文名，不要自行猜写中文。
- **CityU**：`cb.cityu.edu.hk/dao/.../detail?eid=xxx` 的正文是 `{{{staffResearchAreas}}}` 模板占位符（JS 渲染），抓不到；改用 **CityU Scholars** `scholars.cityu.edu.hk/en/persons/<name-slug>`（含 `Research Interests/Areas` 字段，可 curl），slug 形如 `tze-kin-alan-wan`。营销/传播等系站也常返回 84B WAF 壳，需 WebFetch 穿透。

##### 对抗审核的已知误报模式（2026-09-21 记录）
- **把 WAF/SPA 拦截当死链**：`facultyprofiles.hkust-gz.edu.cn`（SPA 壳）、`web.socialwork.hku.hk` / `datascience.hku.hk` / `research.cuhk.edu.hk`（Cloudflare 403）、`saasweb.hku.hk`（curl 000）、`cityu.edu.hk/stfprofile`（Incapsula 壳）——这些在浏览器里都正常，**审核前必须把这份"已知不可穿透清单"连同穿透方式一起交给审核官**，否则会大量误报。
- **把渲染截断当"页面没有"**：审核官用 WebFetch 读到的 markdown 可能丢掉 JS 标签页里的内容（如港大社会学 ABEL 的 "I am happy to supervise doctoral students…" 实际在页面源码里）。判定"页面无此句"前，必须用 curl + grep 原文复核一次。

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

##### UNNC 商学院 + 理工科人机交互方向补充（2026-09-10 验证，蒋元萍案例 — 创业/AI/幸福感/人机交互方向）
- **NUBS China 全部学术教师一页表格（L1 静态，直接 curl 可解析 name→UUID）**：`nottingham.edu.cn/en/business/people/academic.aspx`（含三个系 EMM / FAE / IBM 的分组姓名+职称）。个人页统一为 `nottingham.edu.cn/en/Business/People/Profile.aspx?id={uuid}&language=en-GB`，curl 即返回 Pure 版完整简介（Research Interests + Personal profile + 邮箱），**无需浏览器**。
- **中文个人页**：把 `/en/` 换成 `/cn/`（`nottingham.edu.cn/cn/People/Profile.aspx?id={uuid}`）→ 拿到中文姓名与中文职称（英文页没有中文名）。
- **邮箱提取**：页面为防爬把 `@` 去掉，形如 `Email Haibo.Zhou nottingham.edu cn` → 正则还原为 `@nottingham.edu.cn`。另有 `/en/people/{slug}` 形式的短链（如 `/en/people/alain-chong`、`/en/people/lin-huang`）。
- **博士申请页（商学院）**：`nottingham.edu.cn/en/business/programmes/phd-programme/phd-programme.aspx`（同目录下另有 `application-details.aspx` / `supervisors.aspx` / `programme-structure.aspx`）。要点：3 年制；**必须先联系导师并取得同意再申请**；IELTS 6.5(min 6.0)、TOEFL 87；中国本科均分 78–83；有全奖（cover 学费+保险+住宿+生活费）；NUBS 要求 9 月入学；入学前有导师+RKE 委员会面试。
- **理工科学院（FoSE）个人页**：`nottingham.edu.cn/en/science-engineering/staffprofile/{slug}.aspx`（如 `xu-sun-.aspx`）或 `nottingham.edu.cn/en/info-hub/staff-profile.aspx?id={uuid}`。院系列表：`.../department/cs/people.aspx`、`.../department/mmme/people.aspx` 等（静态可解析）。
- **UNNC 研究生（PhD）总入口**：`nottingham.edu.cn/en/study-with-us/postgraduate-research/home.aspx`（FoSE 等非商学院导师的「博士申请信息」用它，不要误填成商学院的 PhD 页）。
- **⚠️ research.nottingham.edu.cn（Pure 门户）全站 Cloudflare Turnstile 验证码**，curl/WebFetch 均被拦（返回 ~1.4KB 挑战页）；但上面的 `www.nottingham.edu.cn/.../Profile.aspx?id=` 路径不设验证，可替代使用。
- **⚠️ 职称陷阱**：UNNC 部分教师职称带 `(T&L)`（Teaching & Learning 教学轨，如 Xuan Feng、Feranita）——教学轨科研产出通常很少，**不宜作为博士生第一导师**，写入前须核对主页职称尾部标记。
- **⚠️ 方向陷阱**：`理工科学院 = 只做工程不做行为实验` 是错误概括。FoSE 的计算机系与机械材料制造工程系**设有人机交互团队**（Boon Giin Lee 任 HCI Lab 副主任、主页明示持续招博士生；孙煦 Xu Sun 为拉夫堡大学人机交互博士、正指导 10 位博士生含 9 位第一导师），做 HCI / Human-AI Interaction / 情感与认知计算 / 人因。凡 RP 涉及人机交互、人因、用户实验者，必须扫 FoSE 这两系。
- **Last verified**: 2026-09-10

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
