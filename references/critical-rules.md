

---

## 关键规则（CRITICAL）（自 SKILL.md 迁入 2026-10-07）


#### Stipend 与 Funding 核实规则（验证已有表格时强制执行）

##### Stipend 金额必须逐校核实官网

**禁止未经核实直接填写或接受 stipend 数字。** 表格中常见的 stipend 数据存在系统性偏差，必须搜索每个学校 PhD 项目的官网确认最新数字。

**常见学校官方 stipend 参考（2025-2026 学年）**：

| 学校/项目 | 常见错误数据 | 官方数据 | 偏差 |
|----------|------------|---------|------|
| CWRU BSTP | ~$37K+/yr | **$38,000** | 轻微低估 |
| OSU BSGP | ~$34K/yr | **$33,980** | 基本准确 |
| UB PPBS | ~$32K/yr | **$31,000-$35,000**（来源不一）| 在范围内 |
| TAMU Medical Sciences (Medical Physiology) | ~$32K/yr | **$35,000** | **-$3,000** |
| TAMU Genetics | ~$32K/yr | **$32,000** | 准确 |
| USF Medical Sciences | ~$30K/yr | **$37,000** | **-$7,000（严重）** |
| Rochester GDSC/CMPP | ~$35K/yr | **$35,100** | 基本准确 |
| UW-Madison CMB | $37K+/yr | **$37,000** | 基本准确 |

**关键教训**：
- USF Medical Sciences 的 stipend 被系统性严重低估（$30K vs 实际 $37K）
- TAMU 不同 track（Medical Physiology vs Genetics）stipend 不同，不能统一填写
- 不同来源（学校官网、研究生院、具体项目页面）的 stipend 数字可能不一致，需标注来源

##### NIH Grant 必须通过 NIH Reporter 交叉验证

**对表格中提到的具体 NIH grant，必须到 reporter.nih.gov 核实**：
- Grant 类型（R01 / R35 MIRA / K99/R00 / T32 / K08 等）
- 具体金额和资助周期
- PI 姓名是否与导师一致
- 项目编号是否可查

**常见错误模式**：
- 将 K08 过渡性资助描述为已转为 R01（实际可能未获独立 R01）
- 将合作 grant 误认为个人独立 grant
- 将"中心总计 funding"与"个人 funding"混为一谈
- 将 K99/R00 的资助金额误标为 R01 级别

##### Funding 字段中的推测性数据必须标注

以下数据类型属于**推测性估算**，学校官网通常不公布具体数字，必须标注为"约"或"估算"：
- PhD 录取率（"~15-20%"）
- 国际生比例（"~30%"）
- 未来 funding 预估（"2028 年预计..."）
- startup 金额范围（"$800K-$1.2M"）

**禁止将推测性数据作为事实陈述。**

---

#### SPA 壳返回 200 ≠ 链接有效
200 状态码 + SPA 壳（响应相同内容，所有不同 URL 返回相同字节数）→ **不能确认导师存在**。立即切换到 **L0-SPA 策略**：通过 WebSearch 找替代来源（个人网站、ResearchGate、研究中心页面），不要在 SPA 壳上浪费尝试。详见 `references/search-techniques.md` L0-SPA 节。

**经典案例（2026-07-13）**：CUHK STA 的 `/people/faculty/{name}/` 所有 URL 返回完全相同的 114KB 首页 HTML（SPA 壳），浏览器 JS 加载后才显示个人内容。正确格式是 `/peoples/{slug}/`（静态 HTML，可直接验证研究方向）。详见 `references/school-strategies.md` CUHK 章节。

**经典案例（2026-07-23）**：HKUST(GZ) 的 `facultyprofiles.hkust-gz.edu.cn` 全站 SPA，所有页面返回完全相同的 1522 字节 HTML 壳。URL 格式从 `?name=XXX` 查询参数改为 `/faculty-personal-page/NAME/shortname` 路径格式，但两种格式的 SPA 行为一致。自动化工具无法区分旧 URL 失效和新 URL 有效——200 ≠ 内容正确，必须浏览器人工确认。DSA 学域的替代来源为 `dsa.hkust-gz.edu.cn/blog/YYYY/MM/DD/name-slug`（WordPress 格式，可直接抓取内容）。

#### CUHK(SZ) 特殊规则：教师 URL ID 不稳定（2026-07-23 验证）

CUHK(SZ) 数据科学学院的 `sds.cuhk.edu.cn/teacher/XXX` 的 ID 不是稳定标识符。2026 年 7 月的大规模重组中，同一学院的教授被分散到多个子域名和路径格式：

| 变化类型 | 示例 | 旧 URL | 新 URL |
|----------|------|--------|--------|
| teacher ID 变更 | 李爽 | `/teacher/273` | `/teacher/472` |
| 路径格式切换 | 王子卓 | `/teacher/254` | `/node/59` |
| 跨子域名迁移 | 罗智泉 | `sds.cuhk.edu.cn/teacher/478` | `sse.cuhk.edu.cn/teacher/184` |
| 个人网站 | 丁宏强 | `sds.cuhk.edu.cn/teacher/378` | `myweb.cuhk.edu.cn/chrisding/Home/Index` |

**关键规则**：

1. **每次会话重新搜索**：不信任上次存储的 teacher ID，使用 WebSearch 搜索 `"[导师名] sds.cuhk.edu.cn teacher"` 找新 ID
2. **不能按旧 ID 推断新 ID**：ID 变更无明显规律（不是简单递增/递减）
3. **多种 URL 格式并存**：同一学院同时存在 `/teacher/XXX`、`/node/XXX`、`myweb.cuhk.edu.cn`、`gklbdc.cuhk.edu.cn`、`sse.cuhk.edu.cn`、`mscfe.cuhk.edu.cn` 等多种格式，每种都需独立搜索验证
4. **Python SSL 握手失败 ≠ 链接失效**：`sds.cuhk.edu.cn` 在 Python urllib 中报 `SSLV3_ALERT_HANDSHAKE_FAILURE`，但 WebFetch 和浏览器可以正常访问。先用 WebFetch 测，再判死

#### 导师主页必须是个人 URL

禁止使用通用院系列表页。每位导师必须有自己唯一的个人主页 URL。

**找不到合格个人主页的导师不得写入 Vika 表**（强制规则）：

禁止用以下 URL 代替个人主页：
- 院系师资列表页（如 `psych.zju.edu.cn/27612/list.htm`）
- 实验室成员列表页（如 `www.nakakolab.iis.u-tokyo.ac.jp/member/nakano_e.html`）
- 第三方平台（如 x-mol.com、百度百科、ResearchGate、**ORCID.org**、Google Scholar、aminer.cn）
- 学校/学院首页
- 返回 200 但内容为空或显示"该页面暂未开放"的占位页（如浙大 person.zju.edu.cn 的 577 字节 SPA 壳）

**特别强调**：ORCID（orcid.org）是研究者 ID 注册平台，不是个人主页。即使 ORCID 页面包含研究者的论文列表和简介，也**绝对不能**作为导师主页 URL 使用。ORCID 是学术身份标识系统，不是机构官方个人页面。

**验证标准**：用 WebFetch 或 curl 打开 URL，必须能看到导师的姓名、职称、研究方向等个人信息。如果页面没有导师个人内容，视为无效。

**处理**：找不到合格个人主页 → 不写入 Vika。宁可缺，不可用错误链接凑数。

#### 备注中文章链接：例外允许

**规则：**
- `导师主页` 列必须填学校官网的导师个人 URL（禁止第三方平台）
- 当导师主页信息非常少（没有展现文章、研究内容寥寥）时，在备注中补偿文章链接

**写法**：
- `教授；药物流行病学、比较效果研究；文章看这里 https://scholar.google.com/...`
- `副教授；机器学习临床预测模型；主页信息较少，文章看这里 https://pubmed.ncbi.nlm.nih.gov/...`

**绝对禁止：**
- 将 Google Scholar / ResearchGate / PubMed 链接放在 `导师主页` 列（那是第三方平台）
- 在备注中写"文章看这个链接"以外的引导性语言（如"建议阅读"、"点击查看"）

#### 禁止在备注中出现 AI 痕迹语言（CRITICAL）

**备注是给申请学生看的人工整理信息。以下内容一律禁止——它们不像人说话，不像人操作：**

| 禁止类型 | 错误示例 | 说明 |
|----------|----------|------|
| 机器语气 | `网页被js渲染，需要稍后查看` | 人操作时不会这样说 |
| 警告图标 | `⚠️ 【重大错误：导师已离职】` | 人不会在备注里写警告标签 |
| 操作记录 | `Vika写副教授——实际为正教授` | 人不会把自己的修正过程写进备注 |
| 核实说明 | `✅ 已确认此教授仍在职` | 人不会在备注里写核实状态 |
| 方向编号 | `方向1核心匹配`、`TOP/SECONDARY/TERTIARY方向` | 学生不知道方向书的存在 |
| 工具名称 | `Vika表`、`表格`、`源数据` | 人不会提到自己在用什么工具管理表格 |

**遇到信息与源数据不一致时：**
- 直接写入正确值，不写任何修正说明
- 如果不确定，询问用户下一步操作指示，而不是自己在备注里打标签

**正确做法（遇到导师已离职等重大信息变更时）：**
- ❌ ~~`⚠️【重大错误：导师已离职】`~~
- ❌ ~~`Vika表中该导师状态需更新`~~
- ✅ 不写这条导师记录（如果该导师已不相关）
- ✅ 或写：`教授；心血管病流行病学、营养代谢研究。（已于2025年10月离职Tulane，现为UT Southwestern教授）`（客观注明去向，不写任何修正说明）

#### 禁止在备注中写入方向偏向

不要写 "方向偏X"、"没有非常符合的老师" 等主观评价。

**特别强调：学生不知道方向书的存在。** 任何备注不得引用方向书里的编号或内部术语（如「方向1」「方向2」「TOP方向」「SECONDARY方向」）。有相关性就直接用具体研究方向名称描述。（学生无方向梳理时，备注必须自包含——直接写导师方向+方法，见「备注自包含原则」）

#### 禁止猜测 URL

**永远不要通过命名规则构造 URL。** 大学网站经常重组，URL 路径会变。必须通过以下方式获取 URL：
1. WebSearch 搜索 `"[Name] [University] professor"` 找个人页面
2. WebSearch 搜索 `"[University] [Department] faculty staff listing"` 找系列表页
3. **WebFetch 逐条验证**——200 状态码不代表内容正确（可能是 SPA 壳或 404 软页面）

**「其他导师信息」字段的特殊规则**：这些是系级教职员列表页 URL。每次会话开始、或用户说"检查链接"时，必须对每个 Department 的列表页 URL 逐一 WebFetch 验证。不要依赖 `references/school-strategies.md` 中记录的 URL——它们可能在你上次访问后已经变了。

**教训（2026-07-07）**：12 个「其他导师信息」链接中 4 个已失效（NUS × 2, NTU × 1, CityU × 1），都是因为大学重组了网站结构。

##### 大规模 404 复盘（2026-07-14）

黄肇启选导任务中，60 条记录的 `博士申请信息` 和 `其他导师信息` 出现大面积 404。复盘发现三个根因：

**根因 1：URL 猜测（占 90%+）**

所有出错的 URL 都是在写表时按路径命名规则直接构造的，没有经过 WebSearch 搜索验证。典型的猜测模式 vs 真实路径：

| 字段 | 猜测的路径 | 真实路径 |
|------|-----------|---------|
| HKU SAAS 博士申请 | `/programmes/research-postgraduate` | `/programme/rpg/mphil-phd` |
| HKU Nursing 博士申请 | `/education/postgraduate/` | `/education/doctor-of-philosophy-programme` |
| CUHK SPHPC 博士申请 | `/programmes/` | `/mphil-phd-programme/` |
| HKUST ECE 博士申请 | `/pg/` | `/admissions/postgraduate` |
| HKUST LifeSci 博士申请 | `/programmes/` | 在 `prog-crs.hkust.edu.hk` 子域名 |
| HKU BS 博士申请 | `/programmes/research-postgraduate/` | `phd.hkubs.hku.hk/admissions/...` |
| PolyU Nursing 博士申请 | `/sn/study/` | `/study/pg/rpg/2026/sn` |
| HKU SAAS 院系列表 | `/staff` | `/staff_teaching.php` |
| HKUST CSE 院系列表 | `/people/faculty/` | `/admin/people/faculty/` |
| HKUST LifeSci 院系列表 | `/people/` | `/faculty-members/` |
| HKUST ECE 院系列表 | `/people/` | 无系级列表页，用 `facultyprofiles.hkust.edu.hk` |
| HKUST Math 院系列表 | `/people/faculty/` | 无系级列表页，用 `facultyprofiles.hkust.edu.hk` |

**核心教训**：博士申请信息页和院系列表页的 URL 结构在各校各系之间**没有统一规律**。`/programmes/`、`/people/`、`/staff`、`/pg/`、`/study/` 这些常见路径在大量真实站点上都是 404。**必须先 WebSearch 搜索到真实页面，再把 URL 写进表里，一步都不能省。**

**根因 2：大学网站持续重组**

CUHK SPHPC 的院系列表页从 `/people/` 迁移到了 `/academic-staff/`，原有 URL 直接 404。这类重组是常态，不是偶发事件。

**根因 3：CityU WAF 干扰诊断**

CityU 全站 Incapsula WAF 会使自动化工具看到的返回码异常（403/404/超时/空壳），容易和真正 404 混淆。必须区分"WAF 拦截"和"真 404"——前者是所有 CityU URL 的系统性问题，后者是 URL 本身失效。

**防范措施（写入前强制执行）**：

对于 `博士申请信息` 和 `其他导师信息` 两个字段，**写入每条记录前**必须：
1. 用 WebSearch 搜索 `"[学校] [院系] PhD research postgraduate admission"` 或 `"[学校] [院系] faculty academic staff"`
2. 打开搜索结果中的真实页面
3. 确认 URL 可访问（非 404、非 SPA 壳）
4. 把验证过的 URL 填入字段
5. **批量写入后，对所有非 CityU 的 URL 逐条 curl/WebFetch 验证**

#### 补充「文章链接」「实验室」字段的批量补全方法（2026-09-20 沉淀）

需求量级：101 位导师 × 2 个字段。**不要逐人 WebSearch**（成本极高），用下面的三级流水线。

**字段惯例（照抄表内既有记录）**：
- **文章链接**（Text）：填**作者主页类链接**，优先级 Google Scholar > OpenAlex 作者页 > 实验室 publications 页 > 导师主页。可用 `https://scholar.google.com/citations?user=<ID>&hl=en` 形式。
- **实验室**（Text）：填**中文描述**，格式 `<实验室名或「姓氏 课题组」>；研究方向：<方向；主页：<url>>`。方向直接取自本表「导师研究领域」字段，不要另编。

**三级流水线**：

**L1 从导师主页抓 Google Scholar（零成本，覆盖约 1/3）**
```python
# 抓每个「导师主页」，正则找 scholar 链接
re.findall(r'https?://scholar\.google\.[a-z.]+/citations\?[^"\'\s<>]*', body)
# 同时找实验室站：href 含 lab|group|research，排除 scholar/linkedin/twitter/orcid/researchgate/pubmed
```

**L2 用 OpenAlex API 补作者页（覆盖剩余大部分）**
```
https://api.openalex.org/authors?search=<姓名>&per_page=8
```
- **必须用 `last_known_institutions` 与所关联学校比对**来定候选，不能无脑取第一条（本轮 100 条里有 21 条第一候选是**同名他人**）。
- **学校→机构关键词映射要写对**：Penn State → `pennsylvania state`（不是 `penn state`）、VT → 注意 OpenAlex 常写 `Virginia Tech` 而非 `Virginia Polytechnic Institute`。映射错会把正确候选误判为不匹配。
- 学校名可直接拼进 search query 会**降低**命中率，不要那样做；用姓名搜索 + 机构过滤更准。
- 限流：并发 ≤ 6，条目间 sleep 0.1~0.2s；触发 429 就停。
- **写完后必须逐条回验**：`GET /authors/{id}` 看 `display_name` + `last_known_institutions` + `topics`。**论文数 < 12 的条目基本是名字歧义或合并错误**；topics 与该导师方向明显不符（如做软电子的被判为研究肠道菌群）一律弃用。

**L3 兜底**：L2 判不可靠的，改用该导师的**实验室 publications 页**或**导师主页**（安全优先）。

**收尾**：实验室站 URL 要过滤掉**学校通用页**（`research.mines.edu`、`njit.edu/njitresearch`、`bme.unc.edu/research-areas`、`luddy.iu.edu/research` 等只是学院总览页）和**第三方站**（如 `thriveoncollaboration.org`、`researchstash.com`）。

#### 美国大学站点访问通道与 WAF 绕过（2026-09-20 沉淀）

美国部分大学站点对自动化工具（curl / Python urllib）返回 **403（Cloudflare/WAF）或 000（域名不通）**。遇到时**不要直接判死或跳过**，按 L1→L2→L3 逐级尝试：

**L1 curl/urllib → L2 WebFetch → L3 WebSearch（用站内关键词搜，搜索引擎摘要里就带正文）**

##### 已验证「curl 403，但 WebFetch 可读」

| 站点 | curl | WebFetch | 备注 |
|---|---|---|---|
| `bme.engineering.gwu.edu` / `www.bme.seas.gwu.edu`（GWU BME） | 403（Cloudflare） | ✅ 可读 | `bme.engineering.gwu.edu/faculty-directory` 能读全系名单；个人页偶发被拦，用 WebSearch 兜底 |
| `www.ecs.baylor.edu`（Baylor 工程与计算机学院） | 403 | ✅ 可读 | WebFetch 该页能直接拿到 `ecs.baylor.edu/person/<slug>` 个人页链接 |
| `bme.udel.edu`（Delaware BME） | 403 | ✅ 可读 | 同上 |

##### 已验证「整个域名本机不通（000），须换该校其他域名」

| 学校 | 不通的域名 | 该用的域名 |
|---|---|---|
| Indiana University Bloomington | `ise.iu.edu`、`eng.iu.edu` | **`luddy.iu.edu`**（Luddy 学院站，ISE 系在此，个人页格式 `luddy.iu.edu/people/<姓>-<名>.html`） |
| Howard University | `engineering.howard.edu` | **`profiles.howard.edu`**（个人页 `/<slug>`）、**`cea.howard.edu`**（学院人员列表）、**`gs.howard.edu`**（研究生院项目页） |
| Michigan State University | `engineering.msu.edu`、`egr.msu.edu`（curl 与 WebFetch 均失败） | 只能靠 WebSearch 取线索；若导师有独立实验室站（如 Jinxing Li 的 `labli.net`）可用独立站作「导师主页」，但须在备注与报告中如实说明该 URL 未能在本机验证 |

##### 关键原则

1. **403 ≠ 链接失效，但也 ≠ 链接有效**。必须换通道穿透读正文，确认页面含该导师姓名/职称/方向，才算核验通过。
2. **先读院系名单页、再提取个人页 href**：让 WebFetch 输出每位 faculty 的 href，比猜 URL 后缀可靠得多（Howard 的 `profiles.howard.edu/<slug>`、IU 的 `luddy.iu.edu/people/<姓>-<名>.html` 都是这样拿到的）。
3. **URL 有效但本机不可验证时必须如实标注**（如 MSU 申请页 URL 系按搜索索引推断），不得当作「已验证通过」。
4. **第三方平台的任职信息必须回官网复核**：本轮靠 CV/ORCID 查出 Howard 的 Tao Wei 已转南卡罗来纳大学、MSU 的 Peter Lillehoj 已转 Rice，而 LinkedIn / Aminer / ApplyKite 等仍标原校。凡来源为第三方平台的导师，一律回官方 profile 或官方 CV 交叉确认。
5. **无对口博士项目 ≠ 无对口导师**：核验一所学校前先确认其博士项目是否真存在（如 SMU 只有 M.S. Biomedical Instrumentation，博士仅设机械/电气/运筹；Baylor 的 BME 只是机械系下的方向）。若项目不对口，即使有对口导师也不写入，并在反馈中说明原因。

#### CityU（港城）特殊规则：WAF 防护 + 双域名策略

##### WAF 防护（2026-07-13 验证；2026-08-04 修正）

CityU 全站部署了 **Incapsula WAF**，会拦截所有来自自动化工具（curl、Python urllib、WebFetch）的请求。这不是链接失效，而是反爬机制。

| 域名 | 自动化访问现象 | 浏览器访问 |
|------|-------------|-----------|
| `cityu.edu.hk/stfprofile/` | 200 返回 Incapsula JS 挑战页（200-1000 字节） | ✅ 正常 |
| `scholars.cityu.edu.hk` | **403 Forbidden** | ✅ 正常 |

**关键认知**：
- 自动化审计脚本检测 CityU 链接时，**可能全部报死链**（或 SPA 壳），这是一个已知的系统性问题
- **⚠️ 403 ≠ 必然有效（2026-08-04 修正）**：scholars 返回 403 有两种可能——① 正常教授的页面被 WAF 拦截（有效）；② **离任/已离职教授的页面已删除**（WebFetch 穿透 WAF 后显示 "The page does not exist"）。**必须用 WebFetch 穿透验证**，不能一律当作 WAF 正常现象放过
- 链接有效性必须由人在浏览器中逐条确认，或 WebFetch 穿透 WAF 看真实内容
- 不要因为 WAF 拦截就删除有效的 CityU 导师链接，但也**不要因为 403 就假设链接有效**——交叉验证（见下方「离任导师检测」）

**离任导师检测（2026-08-04 沉淀，Maurice Benayoun 案例）**：

判断 CityU 导师是否已离任，三步交叉验证：

1. **WebFetch 穿透 WAF**：`WebFetch("https://scholars.cityu.edu.hk/en/persons/xxx")` — 若返回 "The page does not exist" / "Page not found"，该学者主页已删除，高度怀疑离任
2. **查 CityU 学术人员目录**：`https://www.cityu.edu.hk/zh-hk/directories/people/academic?page=N` — 若标注 **Visiting Professor** / **Adjunct Professor**，通常是离任后保留的挂名身份
3. **查系级现任教职员列表**：如 `https://www.scm.cityu.edu.hk/people` — 若现任教授/副教授/客座/兼任各分组均无此人，基本确认离任

**辅助手段**：WebSearch 搜 `"[导师名] [原校] 教授"` 看是否已转到其他学校（如南京大学官网注明"原香港城市大学创意媒体学院教授（2012年至2024年）"）。已离任导师**不进入主表**，已写入的需删除。

##### 链接格式策略

CityU 有两种导师主页 URL 格式：

1. **stfprofile 格式**（推荐优先使用）：`https://www.cityu.edu.hk/stfprofile/xxx.htm`
   - 部分旧版教授页面使用此格式
   - 自动化访问返回 Incapsula JS 挑战页（约 200-1000 字节）

2. **scholars 格式**：`https://scholars.cityu.edu.hk/en/persons/xxx/`
   - Pure Portal 全校统一入口，信息更完整
   - 自动化访问返回 403；**离任教授此页面会变成真实 404（穿透 WAF 可见）**

**选择策略**：两种格式都可以用，stfprofile 优先级更高（因为至少不返回 403）。scholars 格式写入后必须 WebFetch 穿透验证内容（能显示教授姓名/职称/院系才算有效）。

##### 写入后复验规则

由于 WAF 的存在，"写入后复验"规则做以下调整：

1. 写入 Vika 后，用 WebFetch 或 urllib 快速检查
2. **预期结果**：stfprofile 返回 200 + 约 200-1000 字节（JS 挑战）；scholars 返回 403
3. 以上两种结果**不能直接判定链接有效**——必须 WebFetch 穿透 WAF 确认页面有该导师姓名/职称/院系内容（穿透后显示 "The page does not exist" 即已失效）
4. **删除记录条件**：Google 搜索找不到该导师、系页面已删除、浏览器确认 404、或**官方目录已无此人（离任）**
5. **交付前**：提示用户在浏览器中抽查 CityU 链接（特别是 scholars 格式的）

#### 🇭🇰🇲🇴 港澳院校博士语言门槛与导师资料入口（2026-09-20 实测沉淀，符日星案例）

港澳任务的**第一决策变量是语言门槛**（大量学生无雅思托福，或只想走中文项目）。下列口径全部来自当场打开的官方页面，写备注时可直接引用。

##### 语言门槛速查（不同学院差别极大，务必逐校核对）

| 学校 | 门槛 | 官方依据要点 |
|---|---|---|
| **香港都会大学 HKMU** | **可绕开** | 「The English language proficiency requirements are **not applicable to** applicants who will work on a Chinese Language education topic, **or whose thesis is to be presented in Chinese**」；另有「waived if the applicant's previous studies at the **Bachelor's degree or above level** adopted English as the medium of instruction」。入口 `hkmu.edu.hk/tc/admissions/research-postgraduate/entry-requirements/` |
| **澳门城市大学 CityU Macao** | **可绕开** | 文化产业研究博士页脚原文「**註：授課語言為中文及英文**」+「**論文可以中文或英文撰寫**」，全页无英语硬门槛。⚠️ **不要写成「中文学制，无需雅思托福」**——官网口径是中英文授课，写「中文学制」属失真 |
| **澳门科技大学 MUST** | **可绕开** | 传播学博士 / 数字媒体博士项目页授课语言栏为「中文/英文」，**未列语言成绩**。入口 `fa.must.edu.mo/programmes/program/view/id-200.html`（传播学）、`id-199`（数字媒体） |
| **北师香港浸会大学 UIC/BNBU（传播学博士）** | 🔴 **严格（易写错）** | **传播学博士全英文授课，只认托福 79 / 雅思 6.5，不接受大学英语六级**。流传很广的「CET-6 500 + CET-SET 口语 B 可替代」**仅适用于理工科技学院开设的专业**，不要套到传播学博士上（2026-09-20 首轮真实写错过）。入口 `gs.bnbu.edu.cn/graduate/graduate1/yjxyjskc/Communication.htm` |
| **港科大 HKUST（清水湾）** | ⚠️ **只认本科学位** | 官方 FAQ `fytgs.hkust.edu.hk/admissions/faq` 的豁免条件**只有「本科学位为英文授课」**；「硕士学位为英文授课能否豁免」在该页**只有提问标题、没有答案**（即官网未确认）。同校社会枢纽页 `soch.hkust-gz.edu.cn/?p=51/` 写「硕士（或以上）英文授课亦可免」，与研究生院口径冲突。**首轮写成「官方 FAQ 明示硕士英文授课亦可免」属过度解读，已更正** |
| **港科大（广州）HKUST(GZ)** | ⚠️ 口径冲突 | 研究生院页 `fytgs.hkust-gz.edu.cn/adm-req` 只写「**bachelor's degree** … medium of instruction was English」；社会枢纽课程页 `soch.hkust-gz.edu.cn/?p=51/` 写「硕士（或以上）英文授课亦可免」。**两处口径不一致：备注里两说并陈并附链接，不要单取一侧** |
| **澳门大学 UM** | ⚠️ 分院系 | 官方 PDF `grs.um.edu.mo/wp-content/uploads/Academic-Units-English-Language-Proficiency-Requirements-for-PhD-Programmes-2526.pdf`：社会科学学院博士「CET 6 score of 500 or above is accepted」，**但「For PhD in Communication, the requirement of IELTS score must be 6.5 or above with no sub-score lower than 5.5」——传播学博士不能用六级替代**。⚠️ 极易写错：不要笼统写「社科学院六级可替代」 |
| **香港中文大学 CUHK（新传博士）** | 严 | 雅思 **7.0** / 托福 **92**（高于研究生院一般标准）。入口 `gs.cuhk.edu.hk/programmes/social-science/phd-communication` |
| 港大 / 港理工 / 港城大 / 港浸会 / 岭南 / 教大 / 港中深 | 常规需雅思托福 | 逐校研究生院页面 |

##### 导师资料入口（实测可用）

- **澳科大 MUST**：博导按方向分组名单页 `fa.must.edu.mo/person/id-744.html`（传播学）、`id-736.html`（数字媒体）、`id-735.html`（电影管理）、`id-732.html`（设计学）。**每位导师的「导师主页」即 `wm-fs2.must.edu.mo/...pdf` 官方简介**，须下载后用 `pypdf` 抽取（WebFetch 读 PDF 返回乱码）。名单页标「教授，兼職博導」者为校外兼任，一律排除。
- **香港都会大学**：RPG 招生页 `admissions.hkmu.edu.hk/rpg/as` **一次给出全院导师姓名 + 职称 + 研究方向关键词**（最省 token）；个人页为 `www.hkmu.edu.hk/as/people/staff-profile/?email=<login>&unit=AS&po=N`。
- **岭南大学 DACI**（数码艺术及创意产业系，2024 年由 Visual Studies 改组）：`ln.edu.hk/daci/staff/faculty`，是港澳「数字文化 + 创意产业」密度最高的一个系。
- **UIC/BNBU 文化与创意学院**：师资页 `scc.bnbu.edu.cn/en/staff/members.htm` 为 JS 渲染；教授个人简介可用 `bnbu.edu.cn/info/<id>.htm` 形式的官方页。

##### 抗抓站点（curl 失败但 WebFetch 可穿透，勿判死链）

`hkmu.edu.hk`（403）、`eduhk.hk`（SSL legacy renegotiation）、`myweb.cuhk.edu.cn` / `hss.cuhk.edu.cn` / `gs.cuhk.edu.cn`（SSL handshake）、`cityu.edu.hk`（WAF 返回 83 字节壳）、`soch.hkust-gz.edu.cn`（经代理偶发 502）。

##### Vika 写入两步法（2026-09-20 确认，可复用）

一次请求**不能混用** `fieldKey="name"` 与 `fieldKey="id"`。新建记录因此分两步：

1. **POST** `/records`，`fieldKey="name"`，只带文本字段 + `OneWayLink`（值必须是数组）→ 拿 `recordId`；MagicLookUp（Location / QS排名）会自动填充。
2. **PATCH** `/records`，`fieldKey="id"`，只带 URL 字段的**字段 ID**（`导师主页` / `博士申请信息` / `其他导师信息`）。
3. 每批 5 条，逐批校验返回条数；任一批返回 0 条立即停。

#### 📌 三类字段一致性硬门（2026-09-21 全表复查沉淀，务必执行）

一次「全表复查」最常见的失分点不是链接失效，而是**字段之间的语义不一致**。交付前必查这三项：

1. **`其他导师信息` 必须是「该导师本人所在系」的师资名单页，不能是学院级/跨系聚合页。**
   典型错误：港大 12 条全部指向 JMSC 名单页，但其中 8 人实际分属社会学系、地理系、SMLC、中文学院、比较文学系、政治与公共行政学系。
   查法：读 `Department` 字段 → 定位该系官方 people/faculty 页 → 逐条替换；再用「页内是否出现该导师姓氏」批量自检（注意繁体页面要做简繁映射）。
   参考：港大社会学 `sociology.hku.hk/people/`、地理 `geog.hku.hk/staff`、SMLC `web.smlc.hku.hk/teachingstaff`、中文 `web.chinese.hku.hk/en/people/academic_staff/`、比较文学 `complit.hku.hk/index.php/faculty/`、政治 `ppaweb.hku.hk/people?people_type=faculty-members`。

1b. **`博士申请信息` 必须是「该项目自己的博士项目页」，不能是全校研究生院统一入口（2026-09-22 用户明确要求）。**
   用户原话：**「博士申请链接需要是各个项目具体的申请链接，不要是全校统一的入口，修复。」**
   典型错误：把 `gs.cuhk.edu.cn/`、`gradsch.hku.hk/prospective_students/programmes`、`fytgs.hkust.edu.hk/prospective-students/admissions`、`www.cityu.edu.hk/en/pg/research-degree-programmes/introduction`、`www.polyu.edu.hk/study/pg/research-postgraduate/`、`www.ln.edu.hk/rpg/admission`、`gs.eduhk.hk/prospective/rpg/`、`fytgs.hkust-gz.edu.cn/adm-req` 这类统一入口写进字段。
   **正确做法**：按 `Department` 找该系/学部/学域自己的 MPhil/PhD 项目页（多数在校系自己域名下）。已核实可用的项目页见下表。
   - 港大：JMSC `jmsc.hku.hk/rpg-programme-overview/`｜中文学院 `chinese.hku.hk/en/postgraduate/programme_information`｜社会学 `sociology.hku.hk/mphil-phd-sociology`｜地理 `geog.hku.hk/mphil-phd`｜SMLC `web.smlc.hku.hk/postgraduate`｜比较文学 `complit.hku.hk/index.php/mphil-phd/`｜政治 `ppa.hku.hk/research-postgraduate/mphil-phd-studies/`
   - 港科大：人文 `huma.hkust.edu.hk/teaching/pg/phd`｜跨学科 `emia.hkust.edu.hk/iip`｜公共政策 `ppol.hkust.edu.hk/mphil-phd-program-overview`｜艺术与机器创意 `amc.hkust.edu.hk/mphil-phd-program-program-objective`
   - 港科广：计算媒体与艺术 `fytgs.hkust-gz.edu.cn/programs/computational-media-and-arts-4`（学域自建站没有项目页，项目页挂在研究生院域的 `/programs/…` 下——注意这仍是**项目页**，不是统一入口）
   - 港中文：`gs.cuhk.edu.hk/programmes/social-science/phd-communication`
   - 港浸会：`gs.hkbu.edu.hk/programmes/doctor-of-philosophy-master-of-philosophy-school-of-communication`
   - 港城大：创意媒体 `scm.cityu.edu.hk/programmes/postgraduate/phd`｜媒体与传播 `cityu.edu.hk/com/Page.aspx?p=PHD_Introduction`
   - 港理工：英文及传意 `polyu.edu.hk/engl/study/research-postgraduate-programme/applying-for-research-study/`｜设计 `polyu.edu.hk/sd/study/rpg/phd/`
   - 岭南：文化研究 `ln.edu.hk/cultural/programmes/mphil-phd`｜数码艺术及创意产业 `ln.edu.hk/daci/programmes/postgraduate/postgraduate`
   - 港中深：人文社科学院项目站 `hsspg.cuhk.edu.cn` 下按项目分：计算社会科学 `mphilphdcss`、城市学 `mphilphdus`、全球研究 `mphilphdgs`（**用「博士生导师」子页核对某人挂哪个项目**，如 `mphilphdus/phdadvisor` 里有王宁馨）
   - 教大：**PhD 是全校统一学位、不按学系分设项目页** → 用学系 RPg 页（LCS `eduhk.hk/lcs/programmes/research-postgraduate`；CCA `eduhk.hk/cca/en/programmes/postgraduate-programmes/research-postgraduate-programmes/`）
   - 都会大学：**无分项目博士页**（PhD 统一授予、按学院开设）→ 用院系官网 RPg 页 `hkmu.edu.hk/as/programmes-courses/rpg/`
   **匹配关键词陷阱**：港中深几位导师记录用的是英文名（`Erika Ningxin Wang`），若匹配键写成中文名（`王宁馨`）会漏改——匹配要同时覆盖中英文名与 `Department`。
   **一次 PATCH 只能放同类字段**：URL 字段（`fldv7ZuB1b06J` / `fldYm8R3l4Bnu` / `fldI3KsjPCYWp`）必须 `fieldKey="id"`，文本字段（如 `Department`）必须 `fieldKey="name"`，混在一起会整体返回 0 条。**

2. **`备注` 里的每一句事实性描述都要能在三个链接中找到出处。**
   高风险表述：主持某实验室/研究中心、兼任某课程主任、曾任系主任、奠基学者、方法以某为主、可作第二导师。
   查法：把该句的关键词（Director / Head / Programme Leader / Centre / Lab）回到 `导师主页` 正文里 grep，命中原文才保留，否则删除或改写成官网原文措辞。
   实例：某导师官方研究方向是「比较文学、性别研究、华语电影」，而备注误写成「数字文化与人文」——原因是**照抄了子代理给出的方向摘要而未回原页核对**。子代理的方向摘要一律视为待核。

3. **职称必须与官网一致，Emeritus / Visiting / Adjunct / 兼职 不得当作正式博导。**（已有规则，此处重申）

#### ✉️ 邮箱抓不到时的两条路（2026-09-21 沉淀）

- **Cloudflare 邮箱混淆解码**：岭南大学等站点的个人页把邮箱写成 `data-cfemail="HEX"` 或 `/cdn-cgi/l/email-protection#HEX`，正则抓不到、WebFetch 才能渲染。可自行解码：**首字节为 XOR 密钥，其后每字节与密钥异或即得明文**。示例（Python）：
  ```python
  def cfdecode(h):
      k = int(h[:2], 16)
      return ''.join(chr(int(h[i:i+2], 16) ^ k) for i in range(2, len(h), 2))
  ```
- **院系名单页往往一次给出全院邮箱**：如 CUHK 新传 `research.cuhk.edu.hk/en/organisations/school-of-journalism-and-communication/persons/`、UM 传播系 `comm.fss.um.edu.mo/people/academic-staff/`、CUHK 中文系 `chi.cuhk.edu.hk/about-us/people`、港大政治 `ppaweb.hku.hk/people`。先抓名单页，比逐人开个人页高效得多。
- 若官网确实未公开邮箱（部分 CityU / 港科广 / UIC 教师），留空即可 —— 海外院校邮箱为选填。

#### ⚠️ Vika 同记录多字段修改：必须合并为一次 PATCH（2026-09-21 实测）

同一 `recordId` 在**同一批 PATCH 请求里出现两次会被去重**，导致只生效一条（表现：一批 5 条只回写 4 条）。对同一记录的多个字段改动，务必合并成一个 `fields` 对象、一次请求提交；跨批处理会丢改动。

#### 港澳／内地合办院校抓取与语言门槛情报（2026-09-21 第二轮沉淀）

**BNBU（北师香港浸会大学，原 UIC）**
- **个人页直接可抓**：`https://staff.bnbu.edu.cn/<username>/cn` 为**服务端渲染**，正文含「姓名 / 职称 / 邮箱 / 办公室 / 主要任职 / 交叉任职 / 研究领域 / 教育背景 / 导师类型」。`<username>` 从 `https://staff.bnbu.edu.cn/unit/SCC/cn.html` 与 `.../unit/FHSS/cn.html` 的成员链接取（这两个 unit 页本身是 AJAX 空壳，抓不到列表，只能从 WebSearch 摘要或个人页 slug 猜测后逐个验证）。
- ⚠️ **约 1/4 的教师个人页没有「研究领域」栏目**（实测 41 人中 11 人缺失：黄煜、许夏营、朱润萍、王元新、欧文杰、胡帆、Anilesh Kumar、董天策、庞胜楠、闫虹、Lin Zhu）。**缺这项就不能录入**——`导师研究领域` 必须来自页面原文，`/en` 英文版同样没有。
- ⚠️ 少数页面「研究领域：」标签会**重复出现两次**，解析时要允许跳过重复标签，否则整段被误判为空（黄小薇就是这种情况）。
- **部分页面带「导师类型：博士」字段**，这是带博资格的正面证据，务必写进备注（实测：Geuntae PARK、周超、计雨含、云启栋、吴晓苹）。
- 🔴 **语言政策极易搞错（2026-09-21 更正）**：BNBU **传播学博士**（人文社科学院，官网 `gs.bnbu.edu.cn/graduate/graduate1/yjxyjskc/Communication.htm`）**所有课程全英文授课，语言要求只有托福 79 或雅思 6.5，不接受大学英语六级**。那个流传很广的「CET-6 500 分 + 口语 B 可替代雅思托福」**仅适用于理工科技学院开设的专业**。**不要再把六级政策套到传播学博士上**（这是首轮真实犯过的 P0）。
- 文化与创意学院（SCC）**自身没有博士项目**；该院教授可进入人文社科学院的传播学博士导师名单（庄以仁、原源均在名单内）。

**香港科技大学（广州）HKUST(GZ)**
- `https://facultyprofiles.hkust-gz.edu.cn/faculty-personal-page?id=xxx` 是**纯前端渲染**（1522 字节壳，WebFetch 也读不到内容）→ **不可作为入库依据**。UGOD / IPE 学域的教师只有枢纽名单页（`soch.hkust-gz.edu.cn/academics/ugod/faculty/`、`.../ipe/faculty/`，可读，含姓名/职称/邮箱，但**无研究方向**）→ 这批人**无法填 `导师研究领域`，不要录入**，写进待补清单。
- ✅ **CMA（计算媒体与艺术）学域例外**：`https://cma.hkust-gz.edu.cn/faculty-regular/<slug>/` 是 WordPress、服务端渲染、可读，含职称/邮箱/Research Areas。slug 列表从 `https://cma.hkust-gz.edu.cn/faculty-regular/` 的**相对 href** 提取（`href="/faculty-regular/xxx/"`）。
- 🔴 **语言口径两处不一致，且真实口径比传言更严（2026-09-21 复核实测）**：港科大官方 FAQ `fytgs.hkust.edu.hk/admissions/faq` 的豁免条件**只有「本科学位为英文授课」**；页面里虽然有一个「硕士学位为英文授课能否豁免」的**提问标题，但没有对应答案**——即**官网并未确认硕士豁免**。社会枢纽页 `soch.hkust-gz.edu.cn/?p=51/` 另写「硕士（或以上）英文授课亦可免」，与研究生院口径冲突。**首轮曾据此写成「官方 FAQ 明示硕士英文授课亦可免」，属过度解读，已更正。** 引用时必须对准导师所属枢纽（CMA 属信息枢纽，只有本科口径适用）。

#### 🔴 备注里的语言说明：只写「不需要语言成绩」的学校（2026-09-21 用户明确要求）

用户原话：**「不需要语言成绩的才做单独备注，需要托福/雅思成绩的不用备注。」**

- **需要雅思/托福的学校一律不要在备注里写语言要求**（港大、港中文、港科大、港科广、港理工、港城大、港浸会、岭南、教大、港中深、北师浸 UIC 等）——几十条重复的语言要求只是噪声，学生只需要一眼看到哪些学校能绕开。
- **只给有「不需要英语成绩」通道的学校写**。符日星这批保留 4 所共 30 条：香港都会大学（选中文论文即不适用英语要求）、澳门城市大学、澳门科技大学（中英文授课、项目页未列语言成绩）、澳门理工大学（报考条件未列英语要求）。
- 删语言说明时，**必须同时删掉只为该说明而加的来源链接**（形如 `可以看这个链接：<语言要求页>`），否则会留下悬空引用；但若该链接同时支撑备注里的其他事实（如院系/研究方向介绍页），则要保留。

**香港中文大学（深圳）CUHK-SZ**
- 域名对 urllib 会 **SSL handshake failure**，**必须用 WebFetch**。
- 个人页两套：`https://myweb.cuhk.edu.cn/<user>`（英文，Name/Title/Research/Email 齐全）与 `https://hss.cuhk.edu.cn/teacher/<id>`（中文，研究领域用分号分隔）。**`hss.cuhk.edu.cn/teacher/<id>` 的 id 不稳定**，每次重新搜。
- HSS 下设「计算社会科学学科部」，是计算传播集群的集中地；跨文化交流学科部的教学序列（Assistant Professor (Teaching)）**不具博导资格**。

**澳门**
- **USJ（圣若瑟大学，澳门）不在统一主表**（主表里的 USJ 是黎巴嫩的 Saint Joseph University of Beirut）→ 按「表格隔离 vs 建校取舍」规则**不写入**，进待补清单。该校 `Doctor of Global Studies` 官网列名 14 位博导，数字媒体艺术方向对口。
- **MPU（澳门理工大学）在主表**（`Macau Polytechnic University`）。该校**没有设计学／视觉艺术博士**；对口的是**文化遗产与人类学博士**（`mpu.edu.mo/eschs/zh/phd_cha.php`，授课语言中文／英文，报考条件页未列英语要求）。艺术及设计学院的教师**个人页只有研究主题标签、没有研究领域表述**（`research.mpu.edu.mo`，对 urllib 返回 403，用 WebFetch），录入前要斟酌。

**抓取通用坑（本轮再次踩到）**
- **别用英文名去匹配中文页面**：BNBU `/cn` 页标题是中文，用 `Mei Wu` 去命中「吴玫」必然假阴性，会误判成「页面无内容」。**正确做法是解析页面自身的字段行**（`English` 之后依次是 姓名 / 职称），而不是拿外部名字去 `in` 判断。
- 校园网个人页的 `len` 判断要看**去标签后的正文长度**，不要只看原始 HTML 大小（BNBU 页 33KB HTML 里正文只有几百字，全被 CSS/JS 占掉）。

#### UQ（The University of Queensland）特殊规则（2026-09-17 沉淀）

UQ 不反爬，**urllib + 普通 UA 即可直接抓取**，但有两个坑：

##### 1. 官方导师主页的两种 URL 与权威判定

| 格式 | 示例 | 特征 | 建议 |
|---|---|---|---|
| **专家库页（权威）** | `https://about.uq.edu.au/experts/{数字ID}` | 含 `Availability` 段落，是判断招生资格的唯一权威来源 | **写入表里的「导师主页」用这个** |
| 院系 profile 页 | `https://business.uq.edu.au/profile/{ID}/{slug}` | 会自动跳转/引用专家库 ID；部分 ID 已失效返回 404 | 仅作为查找入口，不要写进表 |

**`business.uq.edu.au/profile/{ID}` 的 ID 与专家库 ID 不是同一个数字**，不能互推。用 `?search=` 搜到人后再取专家库 ID。

##### 2. 专家搜索的正确参数是 `search`（其他都无效）

```
✅ https://about.uq.edu.au/experts/search?search=Trevor%20Russell   → 命中正确人员
❌ ?name= / ?q= / ?keyword= / ?query=                                 → 一律返回 A 开头的全量字母序列表（假结果，极易误判为"查无此人"）
✅ ?research-field={数字}                                              → 按 UQ 研究领域码筛选（如 4917）
```

**踩坑记录**：`?name=` 会静默返回全量列表而非报错，若不做校验会得出「该导师不存在」的错误结论——**必须校验返回的第一条姓名是否与查询词相关**，不相关就说明参数用错了。

##### 3. 招生资格判定：抓 `Available for supervision`

专家库页固定含以下两句话之一，**这是 UQ 官方的 HDR 招生状态**，直接决定要不要写入：

- `... is: Available for supervision` → 可写入
- `... is: Not available for supervision` → **不写入**（即使方向极对口）

**注意区分**：`Not available for supervision` 不等于离任——很多人是因为**已带满学生**。这类人（如 UQ 的 Clair Sullivan、Morteza Namvar、Katie Williams 等方向极对口者）应记录为「方向对口但暂不带人」，作为次级线索或第二导师候选，**不要当作不合格而丢弃**。

##### 3b. ⚠️「教职员名单里有名字」≠「主页有效」（2026-09-20 踩坑，CRITICAL）

UQ 存在一类**「在册但无已发布主页」**的情况：人名仍出现在院系 `our-people` 教职员列表里，但个人主页已经下线。实例：

| 姓名 | 名单中 | 主页实访结果 |
|---|---|---|
| Peter Liesch（IB 讲席教授、学科召集人，曾任 AIB 主席） | ✅ 仍在 IB 名单 | `business.uq.edu.au/profile/23/peter-liesch` → **"Profile not found"**；`experts/118` → 404 |
| Tapani Rinta-Kahila | ✅ 仍在 IS 名单 | `business.uq.edu.au/profile/7312/...` → **404** |

**规则**：**院系名单只用于发现人名，绝不能用它证明主页有效。** 每个候选人必须实访主页确认三件事：

1. 页面能打开（非 404）
2. 页面出现 `Available for supervision`
3. 页面内容里有该人的姓名/职称/院系

三者缺一 → **不写入表格**。UQ 的 "Profile not found" 页文案是「该地址可能不正确，或此人当前没有已发布的个人主页」，遇到即判定不可写入（可能已退休、转为兼职/名誉、或已离任）。

##### 3c. ⚠️ 同名歧义：按名字检索会命中错误的人

UQ 有同名教职人员。实例：**Anna Jenkins** —— 商学院创业方向副教授 与 医学院精神科医生（Royal Brisbane and Women's Hospital 高级专科医师）同名，`?search=Anna Jenkins` 会命中**医生**那位。

**规则**：命中后必须核对**院系（School）+ 职位类型**是否与目标一致（如目标在商学院，则卡片应显示 `School of Business`）。不一致就换关键词重搜或放弃，**不要凭名字直接采信**。

##### 4. 批量核验脚本模板

```python
import re, urllib.request
def plain(html):
    t = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)
# 专家库页
t = plain(urllib.request.urlopen(f"https://about.uq.edu.au/experts/{rid}").read().decode("utf-8","ignore"))
avail = "NOT" if "Not available for supervision" in t else ("OK" if "Available for supervision" in t else "UNKNOWN")
```

##### 5. 高价值机构入口（找「同一方向还有谁」时优先查这些页，比关键词搜人高效得多）

| 入口 | URL | 说明 |
|---|---|---|
| **Future of Health Research Hub** | `business.uq.edu.au/team/future-health-experts` + `business.uq.edu.au/files/118219/researcher-capability-foh.pdf` | 商学院 20+ 位做医疗的学者全名单，**PDF 内含每人完整研究兴趣，一次抓完最省 token** |
| **Queensland Digital Health Centre (QDHeC)** | 挂靠 `chsr.centre.uq.edu.au`（注意：该域名 2026 年已改版，直接访问会跳转到 HMBS 学院页，需经 WebSearch 找当前路径） | 数字健康中心 |
| **Centre for Online Health** | 医学院侧，远程医疗研究 | 找 telehealth/虚拟医疗导师 |
| **RECOVER 伤害研究中心** | `recover.centre.uq.edu.au` | 内含「Technology-enabled rehabilitation」项目页，**直接列出招生项目和 contact 邮箱** |

**PDF 抓取提示**：UQ 的能力清单 PDF 用 WebFetch 会返回二进制乱码，必须先 `curl -o` 下载再用 `pypdf` 抽取：
```python
from pypdf import PdfReader
text = "\n".join(p.extract_text() or "" for p in PdfReader("foh_capability.pdf").pages)
```

##### 6. 「同一方向还有谁」的学科定位法

不要只按学生方向的关键词搜人。先判断学生的方向**落在哪个培养单位**：
- 医疗**信息化 / 数字化转型 / IS** → UQ Business School 信息系统组（BIS）
- 医疗**服务与患者体验 / 管理控制 / 领导力变革** → Future of Health Hub（营销/会计/管理）
- 医疗**技术干预 / 远程医疗** → 医学院 Centre for Online Health、RECOVER

按单位列全名单后逐个核 `Available for supervision`，比逐校关键词搜索的覆盖率高得多，也更容易解释「为什么这位对口」。

#### 🎓 「排名带内是否有对口博士项目」是独立硬门（2026-09-20 沉淀，美国尤甚）

用户说「先看 USNews 60-100」时，**不要默认这个区间里的学校都有会计博士**。实测一整轮：USNews 2026 排名 60-100 的学校里，逐校实开项目页后**只有 3 所**（Rutgers 75 / Drexel 80 / CU Boulder 97）确有会计博士；同区间被硬门排除 8 所——Delaware、American、Howard、NC State、Marquette（均无商科博士或会计不在其中）、UIC（Accounting 方向官方目录写 `Admission ... is suspended`）、Binghamton（PhD in Management 现行只列 Finance/LOS/Marketing/MIS，**未列 Accounting**）、RPI（会计不在当年招生学科）。

**执行规则**：
1. 先按排名带列候选校，**再逐校打开该校 PhD 项目页**确认「独立 Accounting PhD」或「Business/Management PhD 下明确可选 Accounting」；两者都不成立 → **该校所有导师一律不写入**，在报告里单列排除原因。
2. 「学院有会计系 / 有会计教授」≠「有会计博士项目」。Delaware、American、Howard 都有会计系，但一个会计博士都没有。
3. **项目页写了 ≠ 当前招生**：GWU 有 accountancy 博士项目，但博士页曾出现「no longer accepting admissions for Fall 2026 or Fall 2027」；Fordham 的 PhD 页只举例 finance / management，未显式列 Accounting。这类一律标「存疑」不写入，交用户确认。
4. 项目「存在」之外还要看**方法与范式是否对口**：Minnesota Carlson 有会计博士且师资强，但项目页自述 "#1 in analytical financial accounting"（分析式理论），对排斥纯理论的学生要在备注提示「本项目允许分析式或实证两种研究范式」。
5. 「关键词撞上但方法不对口」最隐蔽，必须落到**个人主页的方法学描述**判断：同一所 UvA，Veenman / Thuerheimer 是归档实证，而 Kroos（管理会计）、Maas（行为会计）、O'Dwyer（质性）即属偏离；UOW 会计组整体偏社会/环境/批判会计；VU 的 Anna Gold 是行为审计（实验+质性）。发现偏离时**保留记录但如实写明方法**并加「可以备选一下呢～」，不要静默放过也不要直接删。

#### 🚧 表格隔离 vs 学校主表建记录的取舍（2026-09-20 定调）

「学校关联字段必填」要求给每条记录设 OneWayLink，但「表格隔离」又禁止操作用户未指定的数据表（含关联的学校主表）。**冲突时的处理**：
1. **主表里已有该校记录** → 正常关联（`fieldKey="name"`，字段值传 `[school_rid]`；Location / QS / USNews 会经 MagicLookUp 自动同步）。
2. **主表里没有该校记录** → **不建校、不写入**，把该学校连同「为什么值得加、对口师资是谁」写进交付报告的待补清单，请用户确认后再做。
3. 理由：主表是全局共享表，一条错误记录会污染其他学生的表；少几所学校只是少几条记录，代价小得多。

#### 排除退休/名誉教授
不添加 Emeritus、退休、约 70 岁以上、或不在当前教职员目录中的导师。

#### 排除顶尖名校（默认规则）

以下学校**默认不纳入搜索范围**，除非用户**明确点名要搜**：

| 地区 | 学校 | 排除原因 |
|------|------|----------|
| 🇬🇧 英国 | University of Oxford、University of Cambridge | 顶尖名校，申请门槛极高 |
| 🇺🇸 美国 | Stanford、MIT、Harvard + **美国 Top 15**（按 US News 排名） | 同上 |

触发条件：用户说「QS 前 xxx」「澳洲和英国 QS 前 xxx」等范围描述时，自动跳过以上学校。仅在用户**单独点名**（如「加上剑桥」）时才纳入。

#### 禁止修改已填写选导意向的记录（见上方「操作权限」）

当 Vika 表中 `选导意向（点击选择）` 非空时，该行即被锁定——不得修改、删除或覆盖。详见「操作权限 → 选导意向保护」。

#### 禁止向 MagicLookUp 或计算字段写入
QS排名、Location、美国USNEWS排名等字段通过 API 只读。

#### 新增记录去重

写入新记录前，检查是否已存在于已有选导意向的记录中。

##### Unicode 规范化去重（2026-08-07 沉淀）

不同来源对名字的拼写可能存在变音符号差异（如 `Jaffre` vs `Jaffré`），简单字符串精确匹配会漏检。**写入前必须使用 Unicode NFKD 规范化去除重音后再比对：**

```python
import unicodedata

def normalize_name(name):
    nfkd = unicodedata.normalize('NFKD', name)
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).lower().strip()
```

**去重流程**：
1. 拉取表中所有已有记录，按 `normalize_name()` 分组
2. 对每个新导师，用 `normalize_name()` 查是否已有同名记录
3. 若已有→**跳过**不写入，或先合并信息到已有记录再删除重复（如果已有记录字段空缺）
4. 删除重复时，优先保留**选导意向非空**（已确认）的记录，删除选导意向为空的记录
5. **DELETE 格式**：`DELETE /records?recordIds=recXXX,recYYY`，不带 Content-Type header

#### 🏫 学校关联字段必填（强制执行 — CRITICAL）

**每条新导师记录写入后，必须立即设置学校关联字段（OneWayLink），让 Location / QS排名 / 美国USNEWS排名 / 国内学校层次 通过 MagicLookUp 自动同步。**

这是最容易遗漏但影响最大的步骤。学校关联字段决定整行的 Location、QS、USNEWS、国内学校层次等信息，不填等于记录残缺。

##### 第一步：识别新学生 / 老学生（强制执行，不可跳过）

每张选导表的 OneWayLink 字段指向的学校主表不同。必须先从字段定义读取 `foreignDatasheetId` 来判断学生类型：

```python
r = vika('GET', f'/datasheets/{datasheet_id}/fields')

link_fields = []
for f in r['data']['fields']:
    if f['type'] == 'OneWayLink':
        link_fields.append({
            'field_id': f['id'],
            'field_name': f['name'],
            'main_table_id': f['property']['foreignDatasheetId'],
        })
```

**根据 `foreignDatasheetId` 的值自动识别**：

| foreignDatasheetId | 学生类型 | 主表模式 |
|---------------------|----------|----------|
| `dstMNzQU9Aa58DpgW3` | **新学生** | 统一主表（一张表管全球） |
| `dstNvlYbmD2BTMCB0r` | **老学生** | QS 主表（非美国学校） |
| `dstd7iuffLGUbSnavd` | **老学生** | US 主表（美国学校） |

新老学生的后续操作流程不同，下面分别说明。

---

##### 第二步-A：新学生模式（统一主表 `dstMNzQU9Aa58DpgW3`）

约 2200 条记录，统一管理全球所有学校。**只有一个 OneWayLink 字段**（如「学校名字」），链接到同一张主表。

字段结构：

| 字段 | 类型 | 说明 |
|------|------|------|
| `学校全称` | Text | 完整英文/中文校名 |
| `学校中文名` | Text | 中文名称 |
| `学校英文缩写` | Text | 如 SYSU、CUC |
| `2026年QS排名` | Number | 2026 QS 综合排名（无排名留空） |
| `2027年QS排名` | Number | 2027 QS 综合排名 |
| `2025年QS排名` | Number | 历史参考 |
| `2025年USNews排名` | Number | 美国学校专用 |
| `国家/地区` | SingleSelect | 含 China (Mainland)、United States 等 |
| `所在大洲` | SingleSelect | Asia、Europe、Americas 等 |
| `国内学校层次` | SingleSelect | 985 / 211 / 双非 / 双一流 / 专业院校 |
| `国内学校所在省份` | SingleSelect | 如广东省、北京市、江苏省 |
| `美国学校所在州` | SingleSelect | 美国学校专用（如 加利福尼亚州） |

**创建学校记录**（新学生）：

```python
# 国内学校示例
data = {'records': [{'fields': {
    '学校全称': '广州大学',
    '学校中文名': '广州大学',
    '学校英文缩写': 'GU',
    '国家/地区': 'China (Mainland)',
    '所在大洲': 'Asia',
    '国内学校层次': '双一流',
    '国内学校所在省份': '广东省',
}}], 'fieldKey': 'name'}
resp = vika('POST', f'/datasheets/{main_table_id}/records', data)
school_rid = resp['data']['records'][0]['recordId']

# 关联
data = {'records': [{
    'recordId': supervisor_rid,
    'fields': {link_field_name: [school_rid]}
}], 'fieldKey': 'name'}
vika('PATCH', f'/datasheets/{datasheet_id}/records', data)
```

SingleSelect 字段直接传字符串值即可，API 自动匹配选项。

---

##### 第二步-B：老学生模式（双主表）

两张独立的学校主表，选导表通常有**两个 OneWayLink 字段**：

| 关联字段 | 链接到 | 适用情况 |
|----------|--------|----------|
| `非美国地区学校` | QS 主表（`dstNvlYbmD2BTMCB0r`，~1651 条） | 非美国学校 |
| `美国地区学校` | US 主表（`dstd7iuffLGUbSnavd`，~439 条） | 美国学校 |

**QS 主表字段**（老学生）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `学校` | Text | 英文校名 |
| `排名` | Number | QS 综合排名 |
| `Location` | SingleSelect | 国家/地区 |
| `地区` | SingleSelect | 大洲 |

**US 主表字段**（老学生）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `学校` | Text | 英文校名 |
| `排名` | Number | US News 排名 |
| `所在州` | SingleSelect | 美国所在州 |

**⚠️ 老学生 US 主表无 Location 字段**：`dstd7iuffLGUbSnavd` 只有 `学校`/`排名`/`所在州`，没有 `Location` 字段。设置 `美国地区学校` 后 MagicLookUp 不会自动填充 Location。

**解决方案（默认不采用，见下方取舍）**：同时设置 `非美国地区学校` 指向一个已有 Location=United States 的学校（如 MIT、Stanford），用作 Location 来源。此时记录会同时有两个链接。

**⚠️ 取舍建议（2026-09-14 实践结论）**：上述绕法会让该行在选导表里**同时显示两所学校名**（真实学校 + MIT/Stanford 这类 Location 垫脚石），学生看表时容易误解成本人有两个目标校。**推荐做法：只设置 `美国地区学校`，Location 留空**，并在交付说明里告知机构"本表 US 主表缺 Location 字段，需要时请在主表侧补字段"。只有在机构明确要求必须显示 Location 时才用绕法，且必须在交付报告中主动说明垫脚石学校的存在与原因。`美国USNEWS排名` 这类 MagicLookUp 不受影响，设好 `美国地区学校` 后照常自动填充。

**✅ 2026-10-06 重要区分 —— "同校双表关联" 不是上面说的绕法，要照做**：

上面反对的是**拿另一所学校（MIT/Stanford）当 Location 垫脚石**。但**美国学校本身往往也在 QS 主表里有一条同名记录**（例：Florida State University 在 US 主表 USNews 54、在 QS 主表 QS 549 / Location=United States）。此时**同时关联两张表的同一所学校**是**正确且必要的**：
- 两个链接指向**同一个校名**，学生不会误读成两所目标校；
- 只有这样才能同时拿到 `Location` + `QS排名`（QS 主表侧）与 `美国USNEWS排名`（US 主表侧）。

实测依据：`dsty9NNxLwQ8vwrlnk` 全表 346 条中，**61 条有 `美国地区学校` 的记录，100% 同时设置了 `非美国地区学校`**，且两处校名一致。**判断规则：先查 QS 主表里有没有同名记录。有 → 两张都设；没有 → 只设 `美国地区学校`，Location 留空（回到上面的推荐做法）。**

（教训：曾把"一条记录同时挂两张主表"当成数据异常上报，实际是本校的普遍约定。**报告异常前先统计该模式在全表的频次**。）

**创建学校记录**（老学生）：

```python
# QS 主表
data = {'records': [{'fields': {
    '学校': 'Ghent University',
    '排名': 159,
    'Location': 'Belgium',
    '地区': 'Europe',
}}], 'fieldKey': 'name'}
vika('POST', f'/datasheets/dstNvlYbmD2BTMCB0r/records', data)

# US 主表
data = {'records': [{'fields': {
    '学校': 'Harvard University',
    '排名': 3,
    '所在州': '马萨诸塞州',
}}], 'fieldKey': 'name'}
vika('POST', f'/datasheets/dstd7iuffLGUbSnavd/records', data)
```

##### 第三步：在主表中查找学校（⚠️ 多层模糊搜索 → 搜不到就停，禁止自建）

> **教训（2026-07-20）**：主表实际有 2200+ 条学校记录，`pageSize=200` 只返回第一页。
> 不翻页会误判学校不存在 → 创建重复 → 后续维护混乱。
> **必须用 `pageNum` 翻页直到 `len(records) >= total`，确认遍历全部记录后再判断。**

> **教训（2026-07-24）**：精确匹配 `"University of Exeter"` 搜不到主表中的 `"The University of Exeter"`（少了 The）。
> 搜索必须分多层：精确 → 模糊 → 缩写 → 多候选确认 → 搜不到就停。
> **绝对禁止在主表 POST 新建学校。** 搜不到就告诉用户去补，等用户补完再继续。

**搜索策略（四层，逐层兜底）：**

| 层 | 策略 | 适用场景 | 搜到多个怎么办 |
|----|------|----------|---------------|
| L1 | 精确匹配 `学校全称` / `学校中文名` | 已知完整名 | 不会多（精确匹配唯一） |
| L2 | 大小写不敏感子串匹配 `lower(学校全称)` in `lower(target)` OR `lower(target)` in `lower(学校全称)` | The/University 等前缀差异 | **列出所有候选让用户选** |
| L3 | 匹配 `学校英文缩写`（如 UW-Madison、Exeter） | 名称差异较大时 | **列出所有候选让用户选** |
| L4 | 搜不到 | 学校确实不在主表 | **停下来告诉用户，绝不 POST** |

> **美国学校特别注意**：L2 子串匹配可能搜出多个同名分校（如 "University of California" 匹配到 UC Berkeley、UC Davis、UCLA 等）。当候选 > 1 时，必须列出全名 + recordId 让用户确认。

```python
def find_school_by_name(main_table_id, school_name, mode='new'):
    """翻页遍历全部主表记录，分层查找学校。搜不到返回None让用户自己补。"""
    name_field = '学校全称' if mode == 'new' else '学校'
    all_records = []
    page = 1
    while True:
        r = vika('GET', f'/datasheets/{main_table_id}/records?pageSize=500&pageNum={page}&cellFormat=string')
        all_records.extend(r['data']['records'])
        total = r['data']['total']
        if len(r['data']['records']) < 500 or page * 500 >= total:
            break
        page += 1
    
    # L1: 精确匹配
    for rec in all_records:
        if rec['fields'].get(name_field) == school_name:
            return [rec['recordId']]  # 返回单个候选的列表
        if mode == 'new' and rec['fields'].get('学校中文名') == school_name:
            return [rec['recordId']]
    
    # L2: 大小写不敏感子串匹配
    target_lower = school_name.lower()
    candidates = []
    for rec in all_records:
        full = (rec['fields'].get(name_field) or '').lower()
        cn = (rec['fields'].get('学校中文名') or '').lower()
        if target_lower in full or full in target_lower or target_lower in cn or cn in target_lower:
            candidates.append(rec)
    
    if candidates:
        # 去重（可能有中文名和英文名指向同一条）
        seen = set()
        unique = []
        for rec in candidates:
            if rec['recordId'] not in seen:
                seen.add(rec['recordId'])
                unique.append(rec)
        if len(unique) == 1:
            return [unique[0]['recordId']]
        else:
            # 多个候选 → 必须让用户选
            return [(r['recordId'], r['fields'].get(name_field, '?')) for r in unique]
    
    # L3: 英文缩写匹配
    candidates = []
    for rec in all_records:
        abbr = (rec['fields'].get('学校英文缩写') or '').lower()
        if abbr and abbr in target_lower:
            candidates.append(rec)
    if candidates:
        return [(r['recordId'], r['fields'].get(name_field, '?')) for r in candidates]
    
    # L4: 搜不到 → 停下来
    return None  # 告诉用户：学校不在主表，请手动添加后再继续
```

**使用方式**：
```python
result = find_school_by_name(main_table_id, "University of Exeter", mode='new')
if result is None:
    # 搜不到 → 告诉用户，停止操作
    print("学校 'University of Exeter' 不在主表中，请先在主表手动添加。")
elif isinstance(result[0], tuple):
    # 多个候选 → 让用户选
    print(f"搜到 {len(result)} 个匹配：")
    for rid, name in result:
        print(f"  {rid}: {name}")
else:
    # 唯一匹配 → 直接用
    school_rid = result[0]
```

##### 第四步：搜不到学校时 — 停下来，不要自建 🚫

第三步搜不到学校时，**绝对不要在主表 POST 新建**。改为：

1. 把导师记录先写入选导表（不含学校关联）
2. 告诉用户："XX 学校不在主表中，请手动添加"
3. 等用户补完学校后，再设置 OneWayLink

**禁止事项（新增）**：
- 🚫 **绝对禁止**对主表执行 POST/PATCH/DELETE 操作（即使 API token 有权限）
- 🚫 **绝对禁止**用 `vika('POST', f'/datasheets/{main_table_id}/...')` 在任何路径下创建学校
- 🚫 **绝对禁止**在搜不到学校时自己去建——正确做法是停下来告诉用户

##### 第五步：设置导师记录的 OneWayLink

```python
data = {'records': [{
    'recordId': supervisor_rid,
    'fields': {link_field_name: [school_rid]}
}], 'fieldKey': 'name'}
vika('PATCH', f'/datasheets/{datasheet_id}/records', data)
```

##### 第六步：验证

Patch 后重新 GET 记录，确认 `Location`、`QS排名`、`国内学校层次` / `美国USNEWS排名` 等已通过 MagicLookUp 自动填充。

**禁止事项**：
- 禁止假设学生类型（必须从 `foreignDatasheetId` 动态识别新/老学生）
- 禁止新老学生混用字段名（新学生用 `学校全称`/`2026年QS排名`，老学生用 `学校`/`排名`）
- 禁止在不创建主表记录的情况下直接设置 OneWayLink（会导致幽灵链接）
- 禁止在未翻页遍历全部主表记录前就判断"学校不存在"并创建
- 禁止 OneWayLink 值写成字符串而非数组
- 🚫 **禁止对主表执行任何写操作**（POST/PATCH/DELETE）。搜不到学校就告诉用户，不自己建

**常见错误**：
- 不识别学生类型 → 用错字段名 → API 报错或写入无效字段
- OneWayLink 值写成字符串而非数组 → API 报错 → 链接未生效
- 翻页不全就判断学校不存在 → 创建重复记录 → 主表数据混乱

#### 国内学校搜索（不使用 Google）
国内（中国大陆）学校的导师搜索**不使用 Google**，改用百度搜索：
- `[导师名] [学校名] 教授`
- `[导师名] [学校名] 博士导师`
- 辅助来源：百度学者、百度百科、知网、万方

所有国内学校导师必须遵守 `references/selection-rules.md` 中的「国内学校选导规则」。

---
