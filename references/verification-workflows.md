<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：验证工作流：链接健康审计、链接修复五步、交付前机械复查 SOP（10 项）、申请信息汇编文档批量核查、申请截止日核查、整表验证工作流与问题分级
> **什么时候读**：交付之前；用户报「链接 404 / badcase」时；核查已有表格或申请信息汇编文档时
> **什么时候不用读**：搜索阶段刚开始、还没有可交付内容时；只判断单条导师是否合格（转 selection-rules.md）

---

## 链接健康审计（用户报"链接404/badcase"时，2026-08-04 新增）（自 SKILL.md 迁入 2026-10-07）


先全量审计再针对性修复，不要只修用户点名的几条：

```bash
python3 scripts/link-audit.py [DATASHEET_ID] [VIKA_TOKEN]
```

脚本输出：每个 URL 状态码/字节数/title（独立临时文件避免并发污染）→ 按类型汇总 →
待 WebFetch 穿透验证的存疑项清单（403 / 200 无 title / 疑似 WAF 壳）。

**关键判断规则**：
- `403`（尤其 CityU scholars）：**不能当作 WAF 正常现象直接放过**，必须 WebFetch 穿透看真实内容——
  正常教授页面穿透后可见姓名/职称；离任教授穿透后显示 "The page does not exist" → 删除记录
- `200 + 小字节无 title`：疑似 WAF JS 挑战壳，WebFetch 确认内容

**非 200 结果必须三分流（2026-09-20 沉淀）**：并发探测出的非 200 不可一律判死，按下面三类分开处理：

| 类型 | 判别方法 | 处理 |
|---|---|---|
| **① WAF/反爬拦截** | 同一域名下**所有** URL 都返回同一状态码（403/000），且换 WebFetch/WebSearch 通道能读到正文 | 链接有效，保留；在反馈中标注"站点有反爬，本机 curl 受限" |
| **② 临时网络故障** | 孤立条目，同域名其他 URL 正常；**必须复测一次**（换更长超时 + 完整浏览器 UA） | 复测转 200 即放过；仍失败才进入待重试清单 |
| **③ 真失效** | 换通道后返回真实 404 页（如 "Whoops! You overshot!"、"Access denied"、CloudFront 404），或重定向到**其他机构**的页面 | 必须找到正确 URL 再更正，或删除记录 |

**两条高价值启发式（本轮据此发现 4 个问题）**：
1. **域名一致性**：把「导师主页 URL 的域名」与「所关联学校」逐条比对。不一致的极可能是**已转校**（本轮 VT 的 Saami Yazdani 其 VT 人员页直接跳到 Wake Forest 官方页），也可能是合理的独立实验室站（如 Temple 的 `bellasfatlab.com`）——两种情况都要打开看。
2. **主页正文含姓名**：抓取每个主页正文，检查是否出现该导师的姓或名。可一次性筛出「页面能打开但不属于此人」的情况：SPA 壳（UCR 的 `profiles.ucr.edu/app/home/profile/<用户名>`，curl 取不到正文但抓取通道可读）、跳转页、通用列表页。
3. **URL 命名易错点**：人名类 slug 常与直觉不符，务必从官方目录页取 href 而非手拼。案例：WPI 的 Catherine F. **W**hittington 正确 slug 是 `cfwhittington`（她中间名 Faye），写成 `cwhittington` 会 404。
- 修复流程：搜索替代 URL → 逐条 WebFetch 验证 → `fieldKey="id"` PATCH → 回读验证
- 各校 2026 年 URL 改版格式见「链接修复工作流 → 步骤 2」表格

---


---

## 链接修复工作流（用户说"链接打不开/404"时触发）（自 SKILL.md 迁入 2026-10-07）


当用户反馈已有表格中某学校/学院的导师链接大面积失效时，按以下步骤系统修复：

#### 步骤 0：批量拉取全部 URL（2026-08-04 沉淀）

不要只修用户点名的那几条，先全量审计：

1. GET 全部记录，提取三个 URL 字段（`导师主页` / `博士申请信息` / `其他导师信息`）去重
2. 批量 curl 检查状态码 + 字节数 + title（用**独立临时文件**，不要并发共享同一文件——共享文件会污染 title 读取，但状态码仍可靠）
3. 按学校分组整理结果，区分：真 404 / SPA 壳 / WAF 拦截 / 疑似正常
4. 对存疑的（200 但无 title、403、SPA 壳、标题异常）逐一 WebFetch 穿透验证内容

#### 步骤 1：诊断区分失效类型

用 curl/WebFetch 逐一检查每个链接的状态，区分三类情况：

| 类型 | 症状 | 说明 |
|------|------|------|
| 真 404 | HTTP 404 + 页面标题含"404" | URL 确实失效，需搜索新链接 |
| SPA 壳 | 200 + 所有 URL 返回相同字节数 + 无实际教授信息 | 站点是 JavaScript 渲染，自动化无法判断 |
| WAF/SSL 拦 | 403 / SSL 握手失败 / 超时 | 防护机制干扰，需换工具验证（**注意：403 也可能是离任教授页面已删除，必须 WebFetch 穿透看真实内容，见 CityU 章节**） |

#### 步骤 2：按学校搜索新 URL

不要逐个导师搜，先搜学校的教师目录页找全员新链接格式，再针对性补充搜索：

```python
# 批量搜索语法示例
for name in broken_professors:
    WebSearch(f'"{name}" sds.cuhk.edu.cn teacher OR node')
```

**CUHK(SZ) 搜索技巧**：
- 搜 `"[导师名] sds.cuhk.edu.cn teacher"` 找标准 teacher 页
- 搜 `"[导师名] cuhk.edu.cn"` 发现跨子域名迁移（myweb/gklbdc/sse/mscfe）
- 搜 `"[导师名] sds.cuhk.edu.cn node"` 发现 node 格式页面

**HKUST(GZ) 搜索技巧**：
- 搜 `"dsa.hkust-gz.edu.cn [导师名] faculty blog"` 找 WordPress 格式替代页
- `facultyprofiles.hkust-gz.edu.cn` 是纯 SPA，自动化只能确认 200，无法确认内容
- 若 DSA 博客有个人页则优先使用（可自动化验证内容）

**各校 2026 年改版经验（2026-08-04 沉淀）**：

| 学校 | 变化 | 新旧格式 |
|------|------|---------|
| PolyU Scholars Hub | slug 全面变更，旧 slug 404 | 旧 `persons/christina-wong-wing-yan` → 新 `persons/christina-wong`；`chloe-ki`→`chung-wha-ki`；`magnum-lam`→`man-lok-lam-2`；`minjung-cho`→`min-jung-cho`；`haze-ng`→UUID 格式 `c4fd5adc-...`。**规律：搜 `"[导师名] polyu scholars hub"` 或从 `polyu.edu.hk/sft/people/academic-staff` 列表页抓个人页链接** |
| HKUST HUMA | 路径重组 | 博士申请 `programmes/research-postgraduate` → `teaching/pg/phd`；院系列表 `people` → `about/faculty` |
| HKU Art History | 加 index.php 前缀 | `people/xxx` → `index.php/people/xxx` |
| HKUBS | 人名用英文全名 slug | `people/wan-wen/` → `people/echo-wen-wan/`（万雯的英文名是 Echo Wen Wan） |
| CUHK | 系页面下线后迁移研究门户 | `arch.cuhk.edu.hk/en/people/faculty-members/xxx` → `research.cuhk.edu.hk/en/persons/xxx` |
| 英美欧法学院（2026-08-18 沉淀） | 大面积 404，博士申请/院系列表路径重组 | 博士申请：Kent `courses/postgraduate/237/law`→`courses/postgraduate/340/law-canterbury`；UEA `course/phd/law-phd`→`law/research/research-degrees`；Sheffield `law/postgraduate/research-degrees`→`law/postgraduate/phd/phd-study`；Buffalo `academics/degrees/doctoral.html`→`admissions/apply-to-law-school.jsd.html`；Essex `courses/pgr/phd-law`→`departments/law/research-degrees`；Leeds `law/doc/phd`→`law-research-degrees`；Birmingham `schools/law/courses/postgraduate/research-degrees`→`postgraduate/courses/research/law/law.aspx`。院系列表：UCD `law/about/academicstaff/`→`law/people/`；Vienna `zivilrecht.univie.ac.at/en/team/`→`id.univie.ac.at/en/team/`（创新与数字化系改名）;IVIR `ivir.nl/people/`→`ivir.nl/people/staff/researchers`；LSTS `lsts.research.vub.be/people`→`lsts.research.vub.be/staff-0`；KU `law.ku.edu/people`→`law.ku.edu/faculty`；Tulane `law.tulane.edu/faculty`→`law.tulane.edu/faculty/full-time`；Indiana `law.indiana.edu/about/people/faculty.html`→`law.indiana.edu/about/people/`；Essex `departments/law/people/academic-staff`→`departments/law/people/academic`；Leeds `law/staff`→`law/stafflist`；Birmingham `schools/law/people/index.aspx`→`schools/law/staff/index.aspx`；Temple `contact/`→`directory/faculty/`；UEA `law/people`→`research-portal.uea.ac.uk/en/organisations/school-of-law/persons/`（UEA 主站走 Imperva Human Verification，用研究门户 persons 页兜底） |

#### 步骤 3：写入前逐条 WebFetch 验证

每个候选 URL 必须用 WebFetch 打开，验证能显示：
- ✅ 导师姓名、职称
- ✅ 研究方向
- ✅ 院系归属

出现以下任一情况即判定无效：
- ❌ 404 / 页面未找到
- ❌ 只有导航栏/空壳（SPA）
- ❌ 显示的是其他不相关人员

#### 步骤 4：Vika PATCH 修复

```python
# URL 字段 PATCH 必须 fieldKey="id"
fields = vika("GET", "/fields")
homepage_fid = next(f["id"] for f in fields["data"]["fields"] if '导师主页' in f['name'])

updates = [{"recordId": rid, "fields": {homepage_fid: new_url}} for rid, new_url in fixes.items()]

for i in range(0, len(updates), 10):
    vika("PATCH", "/records", {"records": updates[i:i+10], "fieldKey": "id"})
```

#### 步骤 5：PATCH 后回读验证

```python
# 回读时必须用字段名（不是 field ID）
verified = vika("GET", f"/records?recordIds={','.join(fixed_ids)}")
for r in verified['data']['records']:
    # ✅ 正确：用字段名读取
    url = r['fields'].get('导师主页', '')
    # ❌ 错误：用 field ID 读取 → 永远 None
    # url = r['fields'].get(homepage_fid, '')
```
| CUHK(SZ) teacher ID 跨会话失效 | 上次存的 `/teacher/254` 已变 `/node/59`、`/teacher/273` 变 `/teacher/472` | 每次会话重新 WebSearch 搜索新 ID，不信任旧 ID |
| HKUST(GZ) SPA 全站 1522B 壳 | 新旧 URL 格式均返回相同字节数，自动化无法判定有效性 | 标记为 SPA，提示用户浏览器确认；同步搜索 DSA 博客替代来源 |
| Python SSL 失败当链接失效 | `sds.cuhk.edu.cn` Python urllib 报 handshake failure | 换 WebFetch 验证，不直接判 404 |
| Vika Text 字段 PATCH 用错 fieldKey | Text 字段（如「备注」「你的反馈」）用 `fieldKey="id"` 时 API 返回 code=200 但实际 HTTP 400 "The format of the fields parameter value is wrong"，数据未写入 | Text 字段必须用 `fieldKey="name"`（字段名），不能用 `fieldKey="id"`（字段 ID 留给 URL 字段） |
| PATCH 后回读用错键名 | GET 返回字段名键，但用 field ID 去读永远 None | PATCH 前后各拉一次字段列表，回读用当前字段名 |
| 精确匹配搜不到学校就自建 | 搜 "University of Exeter" 搜不到 "The University of Exeter" → 在主表 POST 创建重复 | 必须用 L1→L2→L3 分层搜索，L2 用不区分大小写子串匹配；搜不到就告诉用户，绝不自建 |
| 对主表执行写入操作 | POST 到主表新建学校、或 PATCH 修改主表记录 | 🚫 主表是只读参考数据源，任何写操作都是禁止的 |

---


---

## ✅ 交付前机械复查 SOP（10 项，全部可脚本化）（自 SKILL.md 迁入 2026-10-07；加第 9 项地区职称门槛闸门、第 10 项项目覆盖完整性）


对抗 auditor 审的是"该不该留"，人工判断之外的**机械一致性**必须再跑一遍。用户说"检查一遍"时直接执行这 10 项。2026-09-14 于洋案例中，这一轮抓出了 auditor 没发现的一处职称错误；2026-09-15 加第 8 项（三硬门槛专项复核）。

| # | 检查项 | 做法 | 通过标准 |
|---|--------|------|---------|
| 1 | 字段完整性 | 遍历本轮记录，查 `导师`/`Department`/`导师主页`/`导师联系方式`/`导师研究领域`/`博士申请信息`/`其他导师信息`/`备注` + 学校关联 | 无空字段；导师名无重复 |
| 2 | 主页命中姓名 | 并发 curl 每个主页，正则取 `<title>` 并检查正文是否含导师姓（last name） | 标题含姓名、无 404/Not Found 字样 |
| 3 | 邮箱域名一致 | 取主页域名根（如 `msu.edu`）与邮箱后缀比对 | 同根（`education.msu.edu` ↔ `msu.edu` 视为一致） |
| 4 | 三列链接可达**且落点正确**（2026-10-07 修正口径） | 去重后并发 curl **三列**（`导师主页` + `博士申请信息` + `其他导师信息`），同时记录状态码与 `-w "%{url_effective}"`；非 200 与疑似壳页换完整浏览器 UA / WebFetch 穿透复测 | 渲染通道下**能打开**；且 **`url_effective` 与原 URL 一致**（未被跳到院系搜索页 / 机构概览页 / 别的项目页）；无 404 / 410 / 域名解析失败。**不以「curl 全 200」为准**——美国校常对 404 返回 200 + "Page Not Found" 内容，反爬站点又常返 403，两个方向的假信号都要靠内容与落点来判 |
| 5 | 学校关联反查 | 拿关联的 recordId 回主表查 `学校`/`排名`，与记录标注的排名比对 | 学校名与排名都对得上 |
| 6 | 备注语言正则扫 | emoji / 方向编号 / 工具名 / 修正语言 / 机器打分 / 元注释 / 误指代「学生」 | 0 命中（注意 `特拉华大学生物力学` 这类「大学生」误报，改写措辞规避） |
| 7 | 职称比对官网 | 逐条抓官网职称文本与备注首词比对 | 一致，且**备注首段必须是真实职称**（不能写成「博士生导师」这类资格描述） |
| 8 | 三硬门槛复核 | 逐校抓项目页，抠 GRE 原文 + 招生年份/截止日 + 是否停招 | ①有对口研究型 PhD ②目标入学年未关闭 ③免 GRE |
| 9 | **地区职称门槛闸门** | 按 `selection-rules.md` / `school-registry-hk-mo-cn.md` 的地区最低职级扫描全表 | 无低于门槛者（HK/MO 为助理教授及以上） |
| 10 | **项目与学校覆盖完整性** | 逐所目标学校打开**该校博士学位课程总目录**，列出全部方向对口的项目；与本轮记录的 `博士申请信息` 去重集合比对 | 每个对口项目都有记录挂靠；无「整所学校 / 整个项目缺席」 |

**第 10 项的坑（必读，2026-10-07 曹琇翕案例，两个真实漏项）**：
- **漏掉整个项目**：本轮「澳门科技大学」的 EdD 被写成「该校无教育博士」。根因是派子代理时**在指令里写死了院系**（人文艺术学院），代理在该范围内如实回报「无」，我把**范围性否定当成了全局否定**。实际该校 EdD 挂在 2025-05 新获批的**国际学院**，不在给定学院内。→ 复核动作：打开 `sgs.must.edu.mo/faculty/id-2894.html`（研究生院博士课程总目录，按院系列出全部博士课程），一眼就能看到「教育博士」「教育学博士」在**国际学院**栏下。
- **导师池过薄 / 总结漏校**：港教大 EdD 只抓到 1 位教育类导师（其余 6 位是艺术类 PhD 方向的院系教师），且**交付报告的 A 线重点人选表完全没有港教大**。根因有二：① 没先抓项目官方的 **Potential Supervisors 名单**（`gs.eduhk.hk/prospective-students/edd/potential-supervisors/`，59 人），而是从院系师资页反推；② 总结表是**手写**的，手写就会静默漏掉整所学校。
- **可脚本化的做法**：`SELECT DISTINCT 博士申请信息 FROM 本轮记录` → 与「逐校总目录里方向对口的项目页 URL 清单」做差集。差集非空即代表某个项目没有挂靠记录，或某所学校整体缺席。**总结表也从这个结果生成，不要手写。**

**第 9 项的坑（必读，2026-10-07 曹琇翕案例）**：
- 门槛原文：`school-registry-hk-mo-cn.md`「HK 地区职称门槛：助理教授（Assistant Professor）及以上；`Lecturer`/`Senior Lecturer`/`Teaching Fellow`/`Instructor`/`Professor of Practice`/`Research Assistant Professor` 一律排除」；`selection-rules.md`「United States, Hong Kong, Macau, and Europe except the UK/Ireland: normally require `Assistant Professor` or above」。
- **用户已裁定按讲师序列一刀切**：`school-registry-hk-mo-cn.md` 原文对「页面明示可带博」留的例外口子**不再自行套用**——实例：EdUHK 甄沛豪（Senior Lecturer I，个人页明写「博士生導師」）仍按讲师序列删除。遇特殊情况先问用户。
- **可脚本化的扫描写法**：取 `备注` 首段（`split("；")[0]`）作为职称位，
  `OK=("教授","副教授","助理教授","讲座教授","特聘教授","杰出教授","高级副教授","首席教授")`、
  `LOW=("讲师","Lecturer","Teaching Fellow","Instructor","Professor of Practice","Research Assistant Professor","研究助理教授","兼职","兼職","Adjunct","Visiting","客座","Emeritus")`。
  既报「不在 OK 内」也报「命中 LOW」——前者能抓出职称位被写成资格描述（本轮 XJTLU 4 人误写「博士生导师」），后者能抓出讲师混入。
- ⚠️ 这一步**必须在写入前也跑一次**（候选生成阶段就过滤），不要只放在交付前；本轮就是因为候选阶段没过滤，先写进去再删。

**第 7 项的坑（必读）**：
- **JS 渲染的院系页 curl 抓不到职称**。Penn State（`hhd.psu.edu/contact/*`）、Marquette、Iowa、Pitt 这几类页面的职称在 curl 结果里是空的，**必须用 WebFetch 读**，否则会误判为"无法核实"。
- **不要采信 auditor 报的职称**。auditor 是人写的简报，可能沿用旧信息。2026-09-14 案例：auditor 把 MSU 的 Rajiv Ranganathan 报成 Associate Professor，官网实为 **Professor**，直接写进备注就是错的。
- **页面自相矛盾时以结构化字段为准**：例如 MSU 页面顶部 title block 写 `Associate Professor`、下方 bio 仍写 `Assistant Professor`（bio 未更新），此时用 title block。

**第 8 项的坑（必读，2026-09-15 于洋案例）**：
- **第三方聚合站（StudyQA / GradCafe / 各类"XX大学博士申请条件"站）会缓存旧版要求**。MSU 的 StudyQA 页仍写「must submit all GRE scores」，而 MSU 院系申请页与学校学术项目目录都已无 GRE。**GRE 与招生年份只采信 `*.edu` 官方页**，冲突时弃用第三方。
- **GRE 在官方页有三种表述，都算"不需要"**：① 明确 not required；② 明确 optional（含"不提交不影响竞争力"）；③ **申请材料清单里根本不列 GRE**。第 ③ 种必须读到完整材料清单才能判定，不能因为页面没出现 "GRE" 字样就下结论。
- **注册处通用条款不是项目要求**。Marquette 研究生院 Bulletin 写「The GRE (if applicable) must have been completed within the previous six years」，这是分数时效规定，不是要求提交；以项目页博士材料清单为准。
- **院系级/实验室级停招要单独查**。CU Boulder 整合生理学系有独立的「Laboratories Not Accepting Graduate Students for Fall 2027」按 PI 姓名列出的名单。**项目整体开放 ≠ 你想投的导师在招**，写入前必须按 PI 姓名逐个比对。
- **年份缺失不等于关闭**。多数美国项目页只写「Fall + 截止日」不写具体年份（年度滚动招生），属正常状态。除明确"暂停/不招生/项目终止"外，一律按"未明确说不开放"通过。
- **可用的正向侧证**：目标申请季内的招生说明会日期（如 2026 年 9-11 月的 info session）、已公布下一学年学费、已列入目标学年目录。
- **先修课与前置条件是独立的第四道关**：Delaware BIOMS 要求 12 学分实验科学 + 微积分 + 解剖/生理（B 以上），且**必须先找到同意资助的导师**；CU Boulder 同样要求先匹配 research mentor。三门槛通过 ≠ 学生实际能申，这些要单独写进交付说明。

---


---

## 申请信息汇编文档的批量核查（2026-09-24 沉淀）（自 SKILL.md 迁入 2026-10-07）


触发：用户给一份 docx/xlsx 汇编（自己或他人整理的院校申请信息，含 N 所学校的截止日期/GRE/材料/资助），说「检查一遍文档里的信息是否正确，需要进官网看」。

#### 分工：按学校切块 + 并行子代理

- 先把文档按**学校标题**切块导出成单独小文件（解析 docx → 按 H5 学校标题分块 → `schools/NN_*.txt`），再让每个子代理读 3-4 个文件。**不要把整篇塞给一个代理，也不要自己逐段读**——32 所学校约 500 段，自己读会吃掉全部上下文。
- 子代理必须收到硬约束：只采信**当场打开的官方页原文**；给英文原句 + 完整 URL；搜不到就写「未能核实」绝不猜；**只报错误/存疑/无法核实，不要逐条复述正确项**（否则回包会爆炸）。
- 子代理回复后，**抽 5-10 条影响最大的结论本人复现原文**，尤其是会改变申请人动作的（截止日、必考项、申请费）。

#### 错误分布规律：查「周边事实」，不要只查 deadline

实测 21 条确定性错误里截止日期只占 3 条，其余全是周边事实：

| 类别 | 实例 |
|---|---|
| 申请费金额 | Penn 数学 75→90（SAS 研究生部统一 $90）、UMD AMSC 75→90、UT Austin 未区分国内 $65/国际 $90 |
| 资助与教学条款 | Penn 数学免教学「第一年」→「至少两年」；UT Austin 把 TA 默认资助误写成首年 fellowship（实为学年末**暑期** fellowship）；GT 数学写着「年限未明确」而官网明写 5 年 |
| GRE 政策 | 文档写「官网未明确」，官网其实写了（Columbia 统计 Subject 明确不需要、Caltech ACM 2026-27 学年不要求） |
| 申请材料 | UCSD 清单里多写「简历」；UIUC 统计先修多写两门（官方只列 MATH 447） |
| 出处张冠李戴 | 引的链接是不承载该信息的页面（分部总览页 vs 项目页），甚至引教员个人主页当官方口径 |

**成因**：截止日期是显眼项、会被反复核对；周边事实往往整段照抄上一版或聚合站。所以核查清单必须显式覆盖「申请费 / 资助年限与形式 / 免教学年限 / 先修课 / 材料清单 / 链接是否承载所引信息」。

#### 三类结论要分开写

1. **确定性错误** —— 有官方原文推翻，必须改，附原文 + URL。
2. **出处/链接问题** —— 信息可能对，但给的 URL 不承载它，或引的是个人页/聚合页。
3. **官网确无此表述** —— 文档写「明确接受/明确要求」但官网查不到 → 建议降级为「官网未明确」，**不要直接当错的删掉**。

另外**单列一节「文档已正确标注的官网滞后」**：汇编作者自己标出的「官网仍写 Fall 2026 / Fall 2025 / Fall 2024」往往是**加分项**，复核属实就保留，别当错误改掉。但要额外挑出**会影响截止日的滞后**（如 UW Seattle 数学页仍写 December 10, 2025，文档时间轴里的「12 月 10 日」其实是推断值）并提醒去信确认。

#### 汇总章节要单独校

汇编末尾常有「时间轴」「硬指标汇总」这类跨校小节，最容易和正文不一致——实测时间轴把 Duke 统计错放进 12 月 1 日（正文写的是 12 月 15 日），「接受 GRE 家考的十所」名单又漏了 Duke（Duke 研究生院 FAQ 明写接受 GRE General Test at Home）。**校完正文后必须拿汇总章节再与正文、与官方值对一遍。**

#### 官方页自相矛盾时怎么写

同一学校内部口径冲突很常见（Penn 数学同页 12/8 与 12/15、MIT 数学系 12/1 vs OGE 项目页 12/15、Cornell ORIE 系页 1/5 vs catalog 1/4）。**报告要写清「矛盾本身」并以最早日期作为准备目标**，不要挑一个当唯一答案。注意有些研究生院页会声明「以本页为准」（Duke 的 `application-deadlines` 页就是这么写的）——这类页面的值优先。

#### 读 docx 的技术注意

`tencent-local-office-edit` 的 `doc_resolve_document_structure` **只返回被截断的 text_preview**（即使 `mode=full` + `text_preview_length=200` 也是摘要），拿不到段落全文。校验类任务读全文用 zipfile 直接解析 `word/document.xml` 取 `w:t`（节点数可与 SDK 的节点数交叉验证），但**改文档**仍走 SDK。

#### 批量写入修正：doc_replace_text 倒序法

用户说「把修正直接写进文档」时用这套流程（实测一次写入 38 处、零损伤）：

1. **改副本，不动原件**。用户给的常是企业微信缓存目录里的文件（`~/Library/Containers/com.tencent.WeWorkMac/.../Caches/Files/...`），会被 WeCom 覆盖。复制到工作区再加 `_已核查修正` 后缀。
2. **定位**：`doc_find` 返回 `{"locations":[{begin,end,related_text}]}`。`related_text` 自带前后约 20 字上下文，**用它做去重**比用段落号可靠。
3. **倒序写入**：把待改项按 `begin` **从大到小**排序，逐条调 `doc_replace_text(ranges=[{begin,end}], text=...)`。替换会改变后面文本的长度，倒序可保证尚未处理的位置始终有效。
4. **`old_text` 不唯一时用「锚点位置法」**：`old_text` 若有 N 处匹配（实测 `GRE 家考：明确接受。` 有 14 处），不要靠 `near` 硬凑上下文——先 `doc_find` 一个**唯一**的相邻锚点串拿到位置 P，再取所有匹配中 `begin > P` 且最小的那个。比猜上下文稳。
5. **必做干运行**：脚本先只 find 不写，确认「可定位 N / N」再 `--apply`。
6. **踩坑**：`open_file` 返回后立刻 find 会报 `document is not open`（文档还在流式打开）。**在 open 之后 sleep 1-2 秒**，并在报错时重试 open。漏掉的那几条写完后再补一轮即可（位置在未处理区间内，不受影响）。
7. **验证**：`save_file` 后用 zipfile 逐段 diff 原稿与修正稿——段数必须一致，变化段数必须等于预期条数。SDK 会把 `w:pStyle` 的数字 styleId 归一化成 8 位十六进制（`4`→`000077`、`5`→`000064`），`styles.xml` 与 `document.xml` 同步改、样式名映射不变，**渲染不受影响，不要误判成格式被破坏**；顺手查一次 `styles.xml` 有无残留旧 ID 引用。

#### 链接全量检查（用户说「确保链接都能打开」）

- 用 zipfile 解析 `document.xml` 取 URL。注意这类汇编文档的链接常是**纯文本**（`w:hyperlink` 数为 0），所以检查对象是文本里的 URL 字符串；XML 里的 `&amp;` 要还原成 `&`。
- 先跑一轮 `curl -L -A <UA> -w "%{http_code}"`。**403 不等于失效**：补 `Accept` / `Accept-Language` / `Sec-Fetch-Mode` / `--compressed` 再试，实测 15 个 403 里全部回 200。仍不通的用 WebFetch（带浏览器内核）逐个确认。只有 404/410/域名解析失败才算坏链。
- **还要看落点**：`-w "%{url_effective}"` 对比原 URL。实测 `oge.mit.edu/?p=589` 仍能打开，但已跳到机构概览页、不再是那个项目页——「能打开」和「还是原来那一页」是两件事，后者要单独提醒。
- 补充链接进文档前，**新链接必须先自己验证可打开**；验证不通的（如超时）宁可不写进去，也不要引入开不了的链接。

---


---

## 申请截止日期核查（2026-09-17 沉淀，CRITICAL）（自 SKILL.md 迁入 2026-10-07）


用户说「检查表内的申请截止日期是否正确」时走这一节。**核查对象是「学校 + PhD 项目」组，不是逐条记录**——同一项目的几十条记录共用一个日期，按组核对即可（先用脚本按 `(学校名字, 导师所在PhD项目, 申请截止)` 分组，再去查官网）。

#### 最高频错误：上一轮的月日被「年份 +1」沿用

实测两个 P0 都是同一成因——填表时打开的是**上一轮**的官方页面，页面里写着带年份的旧日期，于是把年份改成新一轮年份就填进去了：

| 学校 | 官方页面原文（上一轮） | 本轮（Fall 2027）官方值 | 错误填法 |
|------|----------------------|------------------------|----------|
| Boston University | "Fall 2026 Application Deadline: **January 6, 2026**" | January 11 | 2027-01-**06** |
| Duke University | "Applications for **Fall 2026** admission are due by Wednesday, **December 10, 2025**." | December 15（研究生院 fall 2027 汇总页："Mathematics 12/15/2026"） | **2026-12-10** |

**判别方法（三步）**：
1. 打开官方页面，**先找学年标注**（`Fall 2027` / `Autumn 2027` / `for fall 2027`）。标了 → 直接采信。
2. 页面只写月日、不带年份 → 多为长期沿用的固定日期（如 CMU Math 的 `December 20`、Cornell CAM 的 `January 7`、Columbia IEOR 的 `December 15`），可用；但**必须再比一次近一年内的历史快照**（`https://web.archive.org/web/2025<MMDDhhmmss>/<url>`，WebFetch 可穿透，curl 到 archive.org 在本机不通），确认这个月日不是上一轮遗留。
3. 页面上明确出现 `Fall 2026`、`December 10, 2025` 这类**带年份的旧表述** → 该页未更新，**不能作为本轮依据**；去研究生院层面找按学年汇总的截止日期页（Duke 的 `gradschool.duke.edu/admissions/application-deadlines/`、BU 的 `bu.edu/cas/admissions/phd-mfa/apply/` 都属于这类，且会标明 "for fall 2027"）。

#### 搜索引擎摘要 / 缓存快照不可信（必须打开实时页面）

实测两次被索引里的旧值误导，都是先搜到旧数字、打开实时页面才发现已改：

| 学校 | 搜索索引里的值（旧） | 实时页面（新） |
|------|--------------------|---------------|
| NYU GSAS Mathematics | January 4，页脚 "Last updated November 2025" | December 18（建议）/ **January 6**（最终），页脚 "Last updated September 2026" |
| Duke Graduate School | December 10 | **December 15** |

所以：搜索结果里的日期只能当线索，**最终值必须来自当场打开的页面**；`Last updated` 字段要顺手读一眼。

#### 系页面 vs 研究生院页面的口径冲突

两者不一致时，**取更具体、标注学年更明确的那一个**，并把另一个作为备注写进报告，不要静默选一个：

- Cornell ORIE：系页面 `Deadline for fall admission to the Ph.D. program is **January 5**`，研究生院 catalog 写 `January 4` → 以系页面 1/5 为准。
- BU：研究生院 Fall 2027 清单写 **January 11**（数学、统计两个 PhD 都改成了 1/11），系页面仍写 "January 6th for Fall PhD admissions" 且页面明显未更新（正文还引用 Fall 2021 政策）→ 以研究生院标明年份的清单为准，报告里注明"按较早的 1/6 交也不吃亏"。

#### 时间窗口与「待定」

美国项目通常在 9-10 月更新下一轮页面。**核查当天若某项目仍写「往年 12 月初」「待定」这类占位**，要重新打开官网确认是否已公布——实测 UCSD Mathematics 在 2026-09-17 已公布 Fall 2027：`Opens: September 2, 2026 / Closes: December 2, 2026`，占位文字可以直接换成实际日期。

#### 报告与写入

- **只写已核实的值**，每条都要能给出官方原文句子 + 完整 URL；报告按「正确 / 需修正」分组，把差异点写清（差几天、谁和谁冲突）。
- **写入前先查 `选导意向（点击选择）`**：非空的记录已锁定，不能改。实测一批里 BU 的 7 条全部锁定、Duke 9 条中 3 条锁定——报告里要单列「需人工在网页端处理」的记录，不要默默跳过。

---


---

## 表格验证工作流（验证已有表格时触发）（自 SKILL.md 迁入 2026-10-07）


当用户要求"验证表格信息""检查链接""确认 funding 是否属实"时，按以下工作流执行：

#### 验证范围

1. **导师主页链接**：逐条 WebFetch 验证，确认是个人主页而非 404 伪装页/院系列表页/第三方平台
2. **博士申请信息链接**：WebFetch 验证可访问性
3. **其他导师信息链接**：WebFetch 验证可访问性
4. **备注信息**：方向匹配性、格式规范、排除 emoji 和主观判断词
5. **项目综合情况**：PhD 项目名称是否正确、stipend 金额是否与官网一致
6. **funding 预计情况**：NIH grant 类型/金额/时间线是否可验证、是否存在"中心总计"与"个人 funding"混淆

#### 验证执行顺序

```
Step 1: 获取学生方向定义书 + 表格全部记录
    ↓
Step 2: 导师主页链接验证（逐条 WebFetch，禁止仅用 curl）
    ↓
Step 3: 博士申请信息 + 其他导师信息链接验证
    ↓
Step 4: 备注方向匹配性验证（对照方向定义书核心机制）
    ↓
Step 5: Stipend 金额核实（搜索每个学校官网最新数字）
    ↓
Step 6: NIH Grant 核实（NIH Reporter 交叉验证）
    ↓
Step 7: 生成问题清单 → 分级 → 修正 → 二次验证
```

#### 问题分级

| 级别 | 描述 | 示例 |
|------|------|------|
| P0 - 严重 | 404 链接、错误 grant 类型、严重低估 stipend | 必须立即修正 |
| P1 - 重要 | 院系列表页代替个人主页、第三方平台链接 | 需找替代链接 |
| P2 - 轻微 | 备注格式问题、emoji、乱码 | 建议清理 |
| P3 - 提示 | 推测性数据未标注"约"、定性判断 | 建议补充标注 |

---
