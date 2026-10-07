

---

## 「博士申请信息」这一列：必须是项目页，不能是全校入口（2026-09-23 实测，125 条）（自 SKILL.md 迁入 2026-10-07）


用户会明确要求「博士申请链接要是各项目具体的申请链接，不要全校统一入口」。这条是硬性质量项，**接手任何表都要主动扫一遍**。

#### 链接层级三分法

| 层级 | 例子 | 处理 |
|---|---|---|
| **校级入口**（要修） | `ethz.ch/en/doctorate.html`、`kit.edu/study/doctorate.php`、`study.unimelb.edu.au/how-to-apply/graduate-research`、`grad.ubc.ca/prospective-students/application-admission`、`study.uq.edu.au/admissions`、`sheffield.ac.uk/postgraduate/phd`、`unsw.edu.au/research/hdr/application`、`queensu.ca/sgs`、`gradsch.hku.hk/.../how_to_apply`、`ucl.ac.uk/prospective-students/...`，以及各校「研究生院 / how to apply」总入口 | **替换**为院系或项目页 |
| **院系/学院级**（通常可接受） | `chemistry.manchester.ac.uk/study/postgraduate-research/`、`mse.ncsu.edu/graduate/`、`chem.ed.ac.uk/studying/postgraduate-research`、`gla.ac.uk/postgraduate/research/chemistry/` | 保留；若该系有更具体的项目页则升级 |
| **项目级**（最佳） | `warwick.ac.uk/study/postgraduate/courses/phd-chemistry`、`gs.cuhk.edu.hk/.../mphil-phd-chemistry`、`polyu.edu.hk/study/pg/rpg/2027/chem`、`grad.berkeley.edu/program/...-phd/`、`admission.umontreal.ca/en/programs/phd-in-chemistry/`、`mse.rutgers.edu/graduate-admissions-and-application-criteria` | 保留 |

**空值也要补齐**（历史批次常见整组为空）。

#### 高效做法（105 组一次搞定）

1. 按 `(学校, Department)` 聚合 → 得到去重后的分组清单（比按记录逐条处理省 10 倍功夫，同院系导师共用一个链接）。
2. 用脚本判定层级（关键词表：`doctorate.php`、`/graduate-studies`、`how-to-apply`、`/admissions`、`js` 等 + "是否只是院系首页"），**产出待修清单**。
3. **派 3–4 路 agent 并行找项目页**（按地区切批），每路要求：先用导师名核实院系 → 判断现有链接是否已是项目页（已是则保留）→ 给替换 URL 并写页面标题 → 反爬站点用 WebFetch 穿透，抓不到标"未核到"、**严禁编造**。
4. 回来自行逐条验证（curl/渲染通道）→ 写 `(学校,院系) → 新URL` 映射 → 批量 PATCH（每批 5 条）。
5. 复查：确认 **空值归零**、不再有校级入口。

#### 两个必须知道的例外与坑

- **有的学校 HDR 申请就是统一入口**（UNSW 无学院级 HDR 页、Macquarie 工学院学院页 404/403）。此时校级入口**就是**实际申请通道，保留并在报告里说明，不要硬凑。
- **院系首页 ≠ 项目页**：`chimie.umontreal.ca/`、`mse.rutgers.edu/`、`ch.nat.tum.de/en/`、`itmc.rwth-aachen.de/` 这类纯首页要换成其 graduate/PhD 页。

#### 写入记录数异常时：用「探针对照实验」自证

批量 PATCH 后若发现表内总数变小，先别慌也别自责——**做一次对照实验**：新建一条 `__探针_请忽略__` 记录 → 用与批量脚本**完全相同**的调用方式 PATCH（只给普通字段、不带主字段、`fieldKey: name`）→ 回读确认仍存在 → 删除探针。实测结论：**按 `recordId` 定位的 PATCH 不会删除记录**（即使 payload 里没有主字段）。若记录数仍减少，则大概率是**人类在表内手工删除**（本例缺失的 3 条正好都是「选导意向」未填的待定行）。此时**不要擅自重建**——先在看板与回复里说明，问用户是否恢复，避免与人工删除意图冲突、也避免与回收站恢复产生重复。

---


---

## 接手别人的表时：先扫一遍历史批次的备注（2026-09-22 实测）（自 SKILL.md 迁入 2026-10-07）


新表常常不是空的——可能是这份列表的**历史副本**（本例新表基线 114 条与旧表完全一致）。历史批次多半是按**更早的格式约定**写的，未必符合当前 skill 规范。**开工前先扫一遍，别只盯自己新写的**，否则用户随手一翻就会问"这几条怎么没按 skill"。

**扫描规则（一次脚本跑完，205 条 5 秒）**：

```text
命中条件 = 备注为空 / 不以标准职称开头 / 备注内含 http 链接 / 含草稿语
草稿语清单：试试、后面再看看、再找找、可以看一下这个链接、失效、论文下滑、主页都是文章、
          scholar.google、researchgate、orcid.org、linkedin
```

实测结果很有代表性：全表 205 条里，**本轮新增 91 条全部合规；历史批次 114 条中有 95 条缺「职称；」前缀**（其中 13 条空备注）。历史备注长这样：

| 问题类型 | 真实样例 |
|---|---|
| 只有方向、无职称 | `光电材料` / `可持续聚合物` / `聚合物化学和功能材料` |
| 备注里夹第三方链接 | `可持续材料，文章https://scholar.google.com/citations?...` |
| 备注里夹 ResearchGate | `可持续材料。可以看一下这个链接https://www.researchgate.net/profile/...` |
| **把核实责任推给学生** | `光电材料。这个链接试试：https://mech.hku.hk/...` |
| 待办式草稿 | `这个老师的学院主页失效了，后面再看看。…` |
| 草稿式评语 | `论文下滑，主页都是文章~生物材料，可持续材料` |

**优先处理哪些**：看 `选导意向（点击选择）` 为空的记录——那些是**尚未定下来的待办行**，属于 agent 的职责范围；已填选导意向的是学生已决定的，改备注前先跟用户确认（大范围改写历史记录属于对既有交付物的变更）。

**修复一个历史备注的标准动作**（本例 5 条）：① 用官方页核实姓名/职称/研究方向（注意历史备注里的方向可能是**错的**，如把"生物材料力学"写成"可持续材料"）；② 备注改写为 `职称；做…。`；③ 顺手补齐 Department、公开邮箱；④ 检查三列链接——历史记录常见「导师主页填了个人域名（非学校官方域）」或「其他导师信息填的是检索落地页」；⑤ 沿时间线反查人物是否还在职（个人页 404 时，用其所在课题组官方页作为替代并注明）。

---


---

## 写入后的「检查一遍」：职称与「其他导师信息」是最容易出错的两处（2026-09-21 实测）（自 SKILL.md 迁入 2026-10-07）


用户说「检查一遍」时，不要只跑字段完整性——要开**独立 auditor 有罪推定逐条核**，并且**职称**和**其他导师信息**这两项几乎每次都出问题。实测 91 条里报出 P0 4 条（全是职称写高）、P1 21 条（15 条是链接质量）。

#### 1. 职称必须取自「官方页面原文」，注意这三类陷阱

| 陷阱 | 实例 | 正确写法 |
|---|---|---|
| **非英语职称直译错误** | EPFL 官方 People 目录写 `Professeur associé`（法/德语区） → 实为 **副教授**，不是教授 | 副教授 |
| **个人页标题 ≠ 正式职称** | UOW 的个人档案页标题写 `Prof Peter Innis`、职位行写 `Professorial Fellow`；但 **IPRI 官方名录页**才写明 `Prof Peter Innis - Professor` | 教授（以**实验室/中心的名录页**为准） |
| **头衔被当成职称** | Liverpool 写 `Chair in Soft Matter`（讲席头衔），正式职称仍是 Professor；KIT 的 `apl. Prof.`（编外教授）也不是正教授 | 教授 / 教授（apl. Prof.） |

**做法**：职称优先查**两级页面**——① 院系或中心的**名录页**（`our-people` / `faculty` / `mitarbeiter`），② 个人的官方 People 目录页（欧洲校常有 `people.<domain>/<name>`）。两者冲突时以名录页为准。审完后用 `PATCH /datasheets/{ds}/records`（`fieldKey: name`，按 `recordId` 批量）修正，一次 5 条。

#### 2. 「其他导师信息」不要填站点根目录 / 搜索落地页

常见错误写法：`https://researchers.adelaide.edu.au/`、`https://researchers.mq.edu.au/`、`https://about.uq.edu.au/experts/search?search=organic`、`cup.uni-muenchen.de/en/`、院系首页。这些虽然能打开，但对学生没有信息量。

**应该填**该导师所在**院系或课题组的教师名录页**，例如：
`.../en/people/`（LMU）、`.../en/people`（Heidelberg PCI）、`www.chemie.rwth-aachen.de/go/id/fspw/`（RWTH ITMC）、`lti.kit.edu/english/mitarbeiter.php`（KIT LTI）、`itcp.kit.edu/english/`（KIT ITCP）、`chemistry.uconn.edu/people/faculty/`、`science.psu.edu/chem/research`、`unsw.edu.au/.../chemistry/our-research`、`smp.uq.edu.au/`、`scmb.uq.edu.au/`、`uwaterloo.ca/chemical-engineering/`、`york.ac.uk/physics-engineering-technology/people/`、`rmit.edu.au/about/schools-colleges/engineering/contact`。

**同时注意跨院系错挂**：填的院系页必须与该导师实际所在系一致（例：化工系的老师别挂到化学系名录；物理工程学院的别挂到化学系）。`博士申请信息` 同理，要挂**他本系**的研究生招生页。

#### 3. 链接全量检查：区分「真 404」与「打不开」

把三列链接去重后整体实测（206 个 URL / 16 并发 / 10s 超时约 1 分钟即可）。**非 200 必须归因**，别直接当成坏链：

- **202 / 403 / 429**：反爬或 JS 挑战（UAlberta、MQ、Monash、Queen's、UniMelb、UMass、St Andrews、Durham）→ 不算问题；
- **301 / 302**：跳转本身不算坏链，但**必须看落到哪**——用 `curl -L -w "%{url_effective}"` 取最终 URL 与原 URL 比对；跳到院系搜索页 / 机构概览页 / 别的项目页，即等于失效；
- **Timeout / URLError**：多为瞬时或 TLS 兼容问题，**复测一次**再判（Adelaide 需 `ssl.OP_LEGACY_SERVER_CONNECT`）；
- 只有**明确的 404** 才算「状态码层面」的坏链，必须替换。

> ⚠️ **能打开 ≠ 合格（用户已明确裁定）**：用户的要求是链接**都能正常打开且落在正确页面**，404 只是举例。状态码正常却仍是坏链的有三类，都要查：
> ① **落点跑偏**——打得开，但已跳到院系搜索页 / 机构概览页 / 别的项目页；
> ② **不是本人的页**——404 伪装成 200（页面正文写 Not Found）、SPA 空壳、跳转页、通用列表页；
> ③ **层级不对**——`博士申请信息` 填了校级入口、`其他导师信息` 填了站点根目录 / 搜索落地页（见上一节）。
>
> **判定以页面内容与最终落点为准，不以状态码为准。** 详见 `verification-workflows.md`「链接健康审计」与「链接全量检查」。

#### 4. 交付前把本地文件改为「以线上表为准」重新生成

审完改完表之后，本地 Excel / HTML 预览就过期了。写一个 `regen_from_live.py`：直接 `GET` 线上表记录 → 生成 Excel 与预览页，保证交付物与线上一致（否则会出现"表里改了、发出去的 Excel 还是旧职称"的尴尬）。顺手在这里处理主表脏数据的影响，例如某校 `国家/地区` 是乱码时，按实际国家归位并单独向用户报告该主表字段需修。

#### 5. 「再次检查备注」时的四项标准动作（2026-09-22 实测，91 条里又查出 6 条）

用户第二次说"检查一遍"时，多半是要求把**备注**这一列挖到底。固定跑这四项：

| 检查 | 做法 | 实测结果 |
|---|---|---|
| **① 职称准确性** | 全量比对官方页面 | 91 条里 6 条疑似不符，人工核清后**全是误报**——见下方"职称比对的两个坑" |
| **② 表述质量** | 逐条读：是不是在讲**研究方向**？ | 查出 5 条：1 条写成了履历（"创办某中心…"）、1 条是口号（"服务能源可持续目标"）、3 条起句不规范（"合成化学家，专长…"／"专长…"） |
| **③ 雷同度** | 跨备注提取 14 字以上重复片段，计数 >1 即雷同 | 0 处（做过"批内零重复"处理的批次，这一步通常干净） |
| **④ 内容可追溯性** | 把备注里的领域关键词（共轭/钙钛矿/热电/自修复…）映射成英文线索，在记录所附链接正文里找 | 查出 **1 条真实缺口**：EPFL 的 `people.epfl.ch/<name>` 这类**人员目录页只有姓名职称、没有研究方向**，研究方向原文在课题组页 → 把「其他导师信息」改挂课题组页即可解决 |

**职称比对的两个坑（必须人工复核，不要脚本一报就改）**：
1. **正则太窄 → 误报**：只写 `professor` 会漏掉页面上常见的 `Prof.` 缩写（德国/瑞士校尤其多），也会漏法语 `Professeur`、德语 `Professor`。实测 Bein / Arne Thomas / Kemerink / Théato 四条的"不符"全是这个原因。
2. **正则太宽 → 也会误报**：法语 `Professeure agrégée` 含 `professeur` 子串，会被判成"教授"，实际是**副教授**（Audrey Laventure 即此例）；同一页面同时出现 `Professor` 与 `Associate Professor`（如多伦多/滑铁卢的院系名录）也会歧义，要认**个人页职称行**而不是名录里的任意一次出现。

**判断"备注写成履历"的简单标准**：把 `职称；` 前缀去掉后，句子应该能回答"这个组做什么"。出现"创办/获得/担任/曾任/推动合作"这类动词，基本就是履历混进来了，需要改写成方向描述。

**不要只信一边**——把「截图勾选集 ∪ 表内勾选字段集 ∪ 截图中有但表内无的行」取并集当作学生的真实意向池，并在报告里注明两处口径差异。

---
