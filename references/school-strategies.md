<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：学校策略库入口与总则：L0-SPA → L4 访问框架、架构→层映射、院校条目更新协议、院系名录页索引与覆盖度台账、已停止追踪的人
> **什么时候读**：开始一个搜索任务、需要确定该用哪条访问通道时；要新增或更新院校情报时；要查院系名录页入口时
> **什么时候不用读**：已有明确目标校且地区分册里能找到条目时——直接看分册；只做字段格式或备注写作时

---

## School Strategy Knowledge Base

Living registry of which access layer to use for each university. Discipline-agnostic — works for fashion, engineering, psychology, anything.

---

## 📂 本知识库已按地区/职能分册（2026-10-07 拆分）

本文件是**入口与索引**。各校的访问层、URL 模式与踩坑记录已拆分到下列分册——**先按目标校所在地区打开对应分册，再用关键词定位，不要整读**。

| 分册 | 覆盖范围 | 何时读 |
|---|---|---|
| `school-registry-uk.md` | 英国院校注册表 | 目标校在英国 |
| `school-registry-au-nz.md` | 澳大利亚 + 新西兰注册表，含 AU 访问层总表 | 目标校在澳 / 新 |
| `school-registry-hk-mo-cn.md` | **入口页** → 指向下面两册 | 先定位再进分册 |
| `school-registry-hk.md` | 中国香港（含港城 / 港理 / 浸会三校口径、PolyU 院系重组） | 目标校在中国香港 |
| `school-registry-mo-cn.md` | 中国澳门 + 内地中外合办（UNNC / XJTLU / CUHK-SZ / BNBU-UIC / DKU / NYU Shanghai / HKUST-GZ） | 目标校在中国澳门或合办项目 |
| `school-registry-sg-eu.md` | 新加坡 + 欧洲院校注册表 | 目标校在新 / 欧 |
| `school-registry-us-ca.md` | **入口页** → 指向下面三册 | 先定位再进分册 |
| `school-registry-us.md` | 美国：博士项目筛选体系与口径总则 + 主要美国校 | 目标校在美国 |
| `school-registry-ca.md` | 加拿大：批次专属陷阱七条 | 写加拿大批次前 |
| `school-registry-us-backlog.md` | 美国：2026-08 批次补录 | 目标校属该批次 |
| `access-framework.md` | 跨校通用：L0–L4 通道路径、PhD 项目 URL 模式速查、ORCID / HISinOne 模式、Dead-end 诊断、Vika 学校 ID | 找访问通道、判 URL 质量时 |
| `school-updates-log.md` | **日志索引**（2026-10-07 起按月分册） | 先看索引再进对应月份 |
| `school-updates-2026-08.md` / `-09.md` / `-10.md` | 各月的区域案例更新 | 排查「以前是否遇到过同类问题」 |

> ⚠️ 拆分后本文件名**不变**，仍是唯一入口——`search-orchestrator.md`、`rules-write.md`、`search-techniques.md`、`SKILL.md` 中对 `school-strategies.md` 的引用依然有效。
> 同理，`school-registry-hk-mo-cn.md` 与 `school-registry-us-ca.md` 拆成多册后**仍保留为入口页**，全仓既有引用无需改动。
> 新增学校时：按地区写入对应注册表分册；跨地区的通用教训写入 `access-framework.md`；带日期的案例复盘追加到 `school-updates-log.md`（本文件只保留访问框架与协议）。
> **查某校情报优先用脚本**：`python3 scripts/school-info.py <校名>` 直接返回单条（含来源文件与行号），不必手工 grep。

## Universal Access Framework (L0-SPA → L1 → L2 → L3 → L4)

Not every school needs a unique trick. Most fall into one of five layers:

| Layer | Name | When to use | Method | Requires |
|:---:|------|-------------|--------|----------|
| **L0-SPA** | Alternative Source Workaround | SPA returns empty shell, no accessible API, but scholars have personal sites/ResearchGate/etc. | WebSearch → find alternative domains → WebFetch personal sites/ResearchGate/research center pages | Nothing |
| **L1** | Direct Access | curl returns full HTML content | `curl` → parse staff list → extract names/links | Nothing |
| **L2** | API Mining | curl returns empty shell (SPA) but API exists | Download JS → grep `api\|baseUrl` → call API with `?size=1000` | JS bundle access |
| **L3** | Search Engine Fallback | curl blocked (403/WAF) OR JS renders but no API | Google `site:{uni} "{name}" professor` → click result in browser | In-app browser |
| **L4** | Tavily Extract/Crawl | L3 fails (WAF blocks even search, encrypted URLs, DDG empty) | `tavily-search-pro extract/crawl/search/research` → bypass client-side WAF via server-side fetch | `TAVILY_API_KEY` env var |

### Decision Tree

```
For each professor, identify the school →
Check school-strategies.md for that school's known layer

├── L0-SPA: Skip staff portal → WebSearch for alternative sources
│   ├── Found personal website → WebFetch (rich HTML, full content)
│   ├── Found ResearchGate → WebFetch (publications + research areas)
│   ├── Found research center page → WebFetch (role + projects)
│   └── Combine all sources → verified research profile
│
├── L1: curl → 200 + HTML table/links → parse directly
│
├── L2: curl → 200 + empty shell (<5KB) → hunt API in JS bundle
│   ├── API found → call API, filter results
│   └── No API → escalate to L3
│
├── L3: curl blocked (403/WAF) → search engine per name
│   ├── Search results found → verify in browser
│   └── Search blocked/encrypted → L4
│
└── L4: Tavily fallback for WAF/blocked pages
```

### L0-SPA — Alternative Source Strategy (NEW)

When a university's staff profile portal is pure SPA (returns <5KB empty HTML shell, status 200 but no content):

**Why SPA portals fail**: React/Vue/Angular render content client-side. WebFetch, curl, and even Tavily extract only receive the JS shell. The actual professor data never reaches the server response.

**Key insight**: Scholars maintain academic identities on MULTIPLE platforms — most are server-rendered and accessible:

| Source | Reliability | Access | Typical Content |
|--------|-------------|--------|-----------------|
| Personal academic website | **High** | WebFetch | Research areas, projects, CV, PhD students, teaching |
| Research center/lab page | **High** | WebFetch | Role description, funded projects, collaborators |
| ResearchGate | **Med-High** | WebFetch | All publications, research areas/tags, citation stats, co-authors |
| ORCID | **Medium** | WebFetch | Structured profile, affiliations, limited publication list |
| Google Scholar (snippet) | **Medium** | WebSearch | Citation count, research field tags (from search result snippet) |

**Discovery workflow**:
1. WebSearch `"[Name] [University] professor research"`
2. Scan results for non-staffportal domains (wordpress.com, .net, researchgate.net, .org.au, ORCID)
3. WebFetch 2-3 alternative sources for each professor
4. Cross-reference: research areas from personal site + publications from ResearchGate + citations from Scholar

**Reliability rule**: A research direction confirmed by 2+ independent alternative sources = verified. Single-source data = noted with source.

### L4 — Tavily Search-Pro Integration

When all L1-L3 methods fail (WAF blocks curl+browser+search, DDG returns empty, Google encrypts URLs), use tavily-search-pro as a server-side proxy that bypasses client-side anti-crawl protections.

**Command location**: `$HOME/.workbuddy/skills/tavily-search-pro/lib/tavily_search.py`
**Python runtime**: `$HOME/.workbuddy/binaries/python/envs/default/bin/python3`
**Required**: `TAVILY_API_KEY` environment variable set
**Note**: 如果 `tavily-search-pro` skill 未安装，L4 层不可用。通过 WorkBuddy 推荐市场安装，或跳过 L4 直接用 L3 搜索引擎兜底。

| Tavily Mode | When to Use | Example |
|-------------|-------------|---------|
| **extract** | WebFetch/curl blocked by WAF (403, Cloudflare, Incapsula) | Extract a professor's profile page content when direct access is blocked |
| **search** | Search engines return encrypted URLs or no results; DDG HTML empty | Search `"John Smith NUS professor"` when Google/DDG fail |
| **crawl** | Need to discover all faculty pages on a university site | Crawl a department's website to find all professor profile URLs |
| **map** | Need a sitemap of faculty-related URLs | Map `nus.edu.sg` to discover all staff directory paths |
| **research** | Deep analysis of a department's faculty composition | Research `"NUS Psychology department PhD supervisors"` for comprehensive results |

**L4 Command Syntax**:
```bash
TAVILY_API_KEY="$TAVILY_API_KEY" "$HOME/.workbuddy/binaries/python/envs/default/bin/python3" "$HOME/.workbuddy/skills/tavily-search-pro/lib/tavily_search.py" <mode> "query" [options]
```

**L4 Escalation Rule**: Only escalate to L4 after L3 has been attempted and confirmed to fail. L4 consumes credits (1-2 per call), so reserve it for genuine blockers.

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
| Cloudflare WAF | **L3→L4** | curl blocked → browser + search engine → Tavily extract/crawl |
| Imperva/Incapsula | **L3→L4** | Browser may also be blocked → Tavily extract fallback |
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

## Auto-Update Protocol

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
5. **After updating, save the file**. (Optional: if the skill directory is a git repo and the user consents, commit the changes. Do not auto-commit without confirmation.)

### Why this compounds

| Searches completed | Schools in registry | Hit rate on next search |
|-------------------|-------------------|------------------------|
| 5 | 5 | ~25% |
| 20 | 20 | ~60% |
| 50 | 50 | ~85% |
| 100 | 100 | ~95% |

After 100 schools, almost every new search hits a known architecture. The skill becomes 3-5x faster.

## 🗺️ 院系名录页索引 + 覆盖度台账（2026-09-29 实测）（自 SKILL.md 迁入 2026-10-07）


做完任务后**必须回答「学校是不是都找完了」**。这张表就是答案的基础——每扫完一个系就补一行，含名录页 URL、人数、实际核查数与有无对口。下次同类方向可**直接从中断处续跑**，不用重扫。

#### 港澳

| 学校 | 院系 | 名录页 | 规模 | 结论 |
|---|---|---|---|---|
| HKU | 机械工程 | `mech.hku.hk/academic-staff/` | 25 | 无对口（除已收 Shin Dong-Myeong） |
| HKU | 电子与计算机（原 EEE） | `ece.hku.hk/people/` | 65 | 无新增 |
| HKU | 生物医学工程 SBME（2025 新设） | `sbme.hku.hk/people` | 40（joint 16 / courtesy 19 / honorary 3 / teaching 2） | 无新增；**注意 SBME 是 joint appointment 入口，可反查到机械系的 TENG 人** |
| CUHK | 机械与自动化 | `www4.mae.cuhk.edu.hk/people/academic-staff/` | 45 | 已收 4 人 |
| CUHK | 电子工程 | `explore.ee.cuhk.edu.hk/en-gb/people/academic-staff`（**urllib 失败，用 WebFetch**） | 39 | 新增 Ren Hongliang |
| CUHK | 生物医学工程 | `www.bme.cuhk.edu.hk/new/core-faculty.php` | 22 | 无新增 |
| CUHK-SZ | 理工（SSE） | `sse.cuhk.edu.cn/en/teacher-search`（分页 `?page=N`，每页 10） | 130 | 全量核完，无强对口 |
| HKUST | 机械与航空航天 | `mae.hkust.edu.hk/en/people/faculty/primary-faculty` | 31 | 已收 3 人 |
| HKUST | 电子与计算机 | `www.ece.ust.hk/research/areas`（**系级名录页全 404，只能按研究方向页扫**） | BME 向 9 + 控制向 7 | 无新增 |
| HKUST | BME 分部 | ⚠️ `bme.hkust.edu.hk` **全站 403**；**该分部 2017-07-01 已并入 CBE** | bioeng 向 15 | 无对口 |
| HKUST | `researchportal.hkust.edu.hk` | ⚠️ Cloudflare 403 | — | 不可用；改用 `facultyprofiles.hkust.edu.hk` |
| CityU | 机械工程 | `cityu.edu.hk/en/mne/people/academic-staff`（**WebFetch 可读，urllib 只回 212 字节壳**） | 全量 | 已收 3 人 |
| CityU | 生物医学工程 | ⚠️ **系级名录页不存在**；用 `cityu.edu.hk/cra/core_members.htm`（机器人与自动化中心） | 26 | 无确认对口 |
| PolyU | 机械工程 | `polyu.edu.hk/me/people/academic-teaching-staff/?sc_lang=en` | 全量 | 已收 5 人 |
| PolyU | 生物医学工程 | `polyu.edu.hk/bme/people/academic-and-teaching-staff/?sc_lang=en` | 全量 | 已收 2 人 |
| PolyU | 电子与电气 | `polyu.edu.hk/eee/people/academic-staff-and-teaching-staff` | 85 | 无新增（能量采集侧 Xu Wanghuai 已在上一轮） |
| PolyU | 工业与系统工程 | `polyu.edu.hk/ise/people/academic-staff/` | 47 | 无对口 |
| PolyU | 康复治疗科学 | `polyu.edu.hk/rs/people/academic-staff/` | 74 | ⚠️ **名录页只给姓名/职称/邮箱，不列研究方向**，需逐个开个人页；对口仅 Kenneth FONG |
| PolyU | 物理与材料（原 AP） | `polyu.edu.hk/pm/people/academic-staff/` | 32 | 无对口（凝聚态/钙钛矿/二维材料） |
| HKBU | **全校五大系** | 见下方专条 | 154 | **确认无对口** |

#### 澳洲 / 新西兰（QS 前 200 共 15 所）

| 学校 | QS26 | 名录页 | 覆盖度 | 结论 |
|---|---|---|---|---|
| Melbourne | 19 | `mechanical.eng.unimelb.edu.au/people/academic-staff` | 44 全核 | 无对口；无人做能量采集 |
| UNSW | 20 | ⚠️ **无公开完整名录页**（`.../our-people` 404）；`research.unsw.edu.au/researcher?for2020=…` 可拼合 | ≈35 | 仅 Liya Zhao 沾边但**官方页需登录** |
| Sydney | 25 | AMME/ECE：`profiles.sydney.edu.au/groups/177740/experts`（疑分页截断）；⚠️ BME 专属名录页 404 | 部分 | 有对口（算法侧强） |
| ANU | 32 | `eng.anu.edu.au/people`（6 页×50）；`cs.anu.edu.au/research/clusters/intelligent-systems/` | 机电 8 + CS ≈30 | 控制理论强，**硬件内核为零** |
| Monash | 36 | `research.monash.edu/en/organisations/mechanical-aerospace-engineering/persons/`（⚠️ 官网页有 Cloudflare，用 research.monash.edu） | 42 | 有对口（外骨骼） |
| UQ | 42 | 机械与采矿 `mechmining.uq.edu.au/our-people`（44 全核，**零 exoskeleton/rehabilitation/vibration**）；EECS `eecs.uq.edu.au` | 44 + EECS | 强对口不在工学院，在 **School of Biomedical Sciences** |
| Auckland | 65 | `auckland.ac.nz/en/engineering/about-the-faculty/engineering/mechanical-engineering/contacts.html`；权威名录是 2026 Calendar Staff List PDF（⚠️ **自定义字体编码，解析不出**） | ≈25 | 已收 3 人 |
| UWA | 77 | `research-repository.uwa.edu.au/en/organisations/school-of-engineering/persons/`（**260 人，逐页抓**） | ≈120（46%） | 未穷尽；只有计算生物力学 ISML |
| Adelaide | 82 | `adelaide.edu.au/about/school/<school-slug>/our-people/` | 已收 2 人 | 学院页只列领导层 |
| UTS | 96 | SEMBE：`profiles.uts.edu.au/groups/124/experts`（A–Z 分页，**未翻完**） | 部分 | 无在校强对口；**Liya Zhao 已转 UNSW、Aguirre-Ollinger 已离职** |
| RMIT | 125 | 四个方向 contact 页：`rmit.edu.au/about/schools-colleges/engineering/contact/<方向>` | ≈130 全核 | 能量采集命中质量最高 |
| Macquarie | 138 | `researchers.mq.edu.au/en/organisations/school-engineering/persons/`（111–113） | 部分 | 交集少 |
| Curtin | 183 | ⚠️ `our-people` 是 **JS 空壳**，改用 `profiles.curtin.edu.au/<编号>-<slug>` 逐人页 | 62 | 有强对口（下肢矫形器） |
| Wollongong | 184 | `uow.edu.au/engineering-information-sciences/school-of-engineering/our-people/` | 全量 | 已收 4 人 |
| Otago | 197 | `otago.ac.nz/sopeses/staff/academic-staff` | 19 + 生工 6 | **无对口** |

#### HKBU 专条：为什么「没有」

**HKBU 没有工学院**——这是结论的根因，不是检索不充分。五个系全为理科与计算：

| 系 | 名录页 | 人数 |
|---|---|---|
| Physics | `physics.hkbu.edu.hk/people/faculty-members` | 13 在编（+RAP 2 / 讲师 4 / visiting 1 / honorary 1 / emeritus 4） |
| Chemistry | `chem.hkbu.edu.hk/people/faculty` | 27 |
| Biology | `biol.hkbu.edu.hk/people/academic_staff/` | 33 |
| Mathematics | `www.math.hkbu.edu.hk/people/faculty/` | 37 |
| Computer Science | `www.comp.hkbu.edu.hk/v1/?page=faculty`（⚠️ **urllib 报 URLError，用 WebFetch**） | 44 |

物理系方向全为凝聚态/光子/材料/声学超材料；化学系纯化学；生物系动植物与环境；数学系纯数学；计算机系软件与 AI。
**唯一沾边**：可穿戴康复项目 *Aspire Motion®*（平衡/肌力评估 + 个性化训练），由**已退休**的物理系教授牵头，以校办公司 Surge Motion Inc 运营 → **不构成博士招生路径**，不得作为导师收录。

> 同类「看似有缺口、实则结构性没有」的情况：某校若无工学院/机械系，就不要在报告里写「未能找到」，而应写「**该校无工学院，五大系均为理科与计算，逐系核过 N 人，无对口**」并附名录页 URL——用户要的是可复核的结论，不是「找不到」。

#### 已停止追踪的人（状态陷阱，避免重复劳动）

| 姓名 | 原单位 | 现状 |
|---|---|---|
| **Liya ZHAO** | UTS → **UNSW**（2022） | 仍在做压电/摩擦电俘能与超材料减振；但 UNSW 官方页需登录 |
| Tomislav BACEK | Melbourne | 已转 Honorary Fellow（ORCID 显示赴瑞士 Lake Lucerne Institute） |
| Minas LIAROKAPIS | Auckland | 已转 Honorary Academic（2025 起任 NTUA + Acumino CEO）→ 不再招生 |
| Gabriel AGUIRRE-OLLINGER | UTS | 已离职，现于新加坡 Articares 任研发经理 |
| Antonio PADILHA LANARI BO | UQ | Honorary Research Fellow，官方页明确 **Not available for supervision** |
| Robert MCLAUGHLIN | UWA | Adjunct Professor，实际已任 Adelaide 生物光子学讲席（2016 起） |
| Jeffery CHEUNG | HKBU Physics | **已退休**，其可穿戴康复项目以校办公司运营 |

---
