<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：常见错误速查表（错误 → 示例 → 正确做法）
> **什么时候读**：交付前的最后一遍扫查；或刚被用户指出一类错误、想快速确认还有没有同类的
> **什么时候不用读**：搜索过程中（此时应看对应阶段的规则）；已跑完交付前机械复查 SOP 且全绿时

---

## 常见错误速查表（自 SKILL.md 迁入 2026-10-07）


| 错误 | 示例 | 正确做法 |
|------|------|---------|
| 猜测 URL | 拼 `/programmes/research-postgraduate`、`/people/faculty/`、`/pg/` 等 | WebSearch 搜索真实页面 URL |
| 批量写入「博士申请信息」时未逐个验证 | 42 条新记录全空，填表时按命名规则拼写 | 每条 URL 写入前必须 WebSearch → 打开验证 → 再填入 |
| 依赖上次会话的院系列表 URL | CUHK SPHPC `/people/` 已变更为 `/academic-staff/` | 每次会话重新 WebFetch 验证 |
| SPA 壳当有效 | 200 响应但无内容（HKUST Math `~macyang` 86B） | 交叉验证姓名和内容，换替代 URL |
| CityU WAF 404 当真实 404 | CityU MKT/EF 系页面返回 404（WAF 拦截） | 浏览器人工确认，区分 WAF 和真 404 |
| 老学生主表有 100 条硬限制（旧表） | 旧 QS/US 主表写入 >100 条时静默丢弃 | 不重新验证 GET；主表只增不删 |
| CDU/CDU 等小型大学研究人员页 404 | RD3 确认有效后 RD4 再查变 404 | 交付前逐条复验所有链接，不信任上一轮验证结果 |
| 备注中 SPA 标注和匹配标识混在同一段 | `Macquarie为SPA系统需浏览器验证；可以备选一下呢～` | SPA 标注放在第二段末尾；备选标识（可以备选一下呢～）仅在方向部分匹配有偏离时使用，且应放在备注最末尾 |
| **监督资格不明/临近退休时写"建议先确认"（2026-09-17 用户明确要求）** | `未出现在创意媒体学院博士导师名单中，套磁前建议先确认带博。`、`建议先邮件确认是否收博士生。`、`这位老师现在约67-68岁了，退休年龄了，申请前建议先邮件确认是否仍收博士生。` | 不要给学生派核实任务。监督资格不明 → 固定写 `未明确表明监督资格，可以后放～`；退休/年龄风险 → 交代事实后写 `……但现在应该到退休年龄了，可以后放～`；行政职务重 → 只客观陈述事实，不写"建议先确认带生意愿"。均用全角～ |
| **引述在研项目/著作时压缩到失真（2026-09-17 用户追问）** | 项目原名 `At the Margins, Across Borders: Translocal Uses of Preexisting Music in Postwar Hong Kong's Cantonese Social Realist and Populist Urban Comedy Films, 1953-1968` 被写成「战后香港粤语喜剧电影音乐的研究项目」——"既有音乐的跨地使用"被压成了泛称"电影音乐"，"社会写实与通俗都市"和年代跨度 1953-1968 都丢了 | 引述在研项目/著作时**必须保留项目本名的关键限定词**（研究对象的确切所指、年代跨度、限定语），宁可多几个字也不要压成近义词泛称；实在不好译就直接给英文原题。备注是给学生判断方向用的，压缩失真会误导方向判断 |
| **备注写了学生点开链接看不到的信息（2026-09-17 用户质询）** | `导师主页` 给的是 HMW 系页，备注却写学者库页上的「接受博士生」和 2027 年在研项目；同类还有 Ying Zhu 的著作、Shin Dong Kim 的"筹建 AI 电影中心"、Anyi Rao 的"AI 电影节"、Charrieras 的"副项目主任" | 备注的任何事实必须能在该记录的 `导师主页`/`博士申请信息`/`其他导师信息` 里看到；来自别的页面时**把来源页链接写进备注**（直接写 `可以看这个链接：<url>`，**不要**写 `（XX页可见：<url>）` 这种来源页批注），或直接不写（见「备注可追溯原则」） |
| **给来源链接时写成"来源页名称（URL）"批注腔（2026-09-17 用户明确要求）** | `……（院系专家名录可见：https://expert.hkbu.edu.hk/en/list/detail/484）`、`这个链接<url>标注其接受博士生`、`页面标注接收博士生`、`学院博士项目页面列其为潜在导师` | 直接说链接、直接说事实：`……。可以看这个链接：<url>`、`欢迎博士生`、`也在学院的博士导师名单里`。不要把"页面/学者库/名录"当成句子的主语（见「备注可追溯原则」的引出语写法表） |
| CUHK(SZ) teacher ID 跨会话失效 | 上次存的 `/teacher/254` 已变 `/node/59`、`/teacher/273`→`/teacher/472` | 每次会话重新 WebSearch 搜新 ID，不信任历史 URL |
| 第三方聚合站当权威源 | MSU 的 StudyQA 页仍写「must submit all GRE scores」，官方页已取消 | GRE / 招生年份只采信 `*.edu` 官方页；第三方页与官方冲突时直接弃用 |
| 页面没出现 "GRE" 就判免 GRE | 未读完整材料清单就下结论 | 必须读到「申请材料清单」全量；清单里不列 GRE 才算免 |
| 注册处通用条款当项目要求 | Marquette Bulletin「The GRE (if applicable)…」被误读为要求 GRE | 该项目页博士材料清单为准；通用条款只约束分数时效 |
| 项目开放即认为导师在招 | CU Boulder 系里单列「Not Accepting Graduate Students for Fall 2027」名单 | 按 PI 姓名逐个比对院系级/实验室级停招名单 |
| 页面无具体年份就当项目关闭 | 美国项目页多只写「Fall + 截止日」，属年度滚动 | 除明确"暂停/不招生"外，一律按"未明确说不开放"通过；可用 info session 日期、下学年学费、目标学年目录侧证 |
| HKUST(GZ) SPA 全站 1522B 壳 | 新旧 URL 格式均返回相同字节数，自动化无法判定有效性 | 标记 SPA，提示浏览器确认；同步搜索 DSA 博客替代来源 |
| Python SSL 失败当 404 | `sds.cuhk.edu.cn` Python urllib 报 handshake failure | 换 WebFetch 验证，不直接判死 |
| Vika Text 字段 PATCH 用错 fieldKey | Text 字段（如「备注」「你的反馈（具体原因）」）用 `fieldKey="id"` 时 API 返回 code=200 但实际 HTTP 400 "The format of the fields parameter value is wrong"，数据未写入 | Text 字段必须用 `fieldKey="name"`（字段名），不能用 `fieldKey="id"`（字段 ID 留给 URL 字段） |
| PATCH 后回读键名错误 | GET 返回字段名键，用 field ID 读永远 None | PATCH 前后各拉字段列表，回读用字段名 |
| CityU scholars 403 一律当有效（2026-08-04） | Maurice Benayoun 案例：scholars 403 是 WAF 壳，穿透后实为 "The page does not exist"（导师已离任） | 403 必须 WebFetch 穿透看真实内容；交叉验证 CityU 学术目录（Visiting/Adjunct 标注）+ 系级教职员列表；已离任导师删除记录 |
| 并发 curl 共享临时文件 | 多个线程写同一 /tmp 文件，title 互相污染（状态码仍可靠） | 每个 URL 用独立临时文件；对 title 异常/200 无 title 的页面用 WebFetch 单独确认 |
| 备注用「学生」称呼申请者 | `明确接受PhD学生` 违反第二人称规则 | 改为 `明确接受PhD申请`，所有备注以「你」称呼申请者 |
| **URL 字段 PATCH 静默丢更新（2026-09-24）** | 用**字段名**（如「其他导师信息」）配 `fieldKey="id"` 提交 → API 返回 `success:true`，但 `data.records` 为空数组、字段完全没变，**没有任何报错** | `fieldKey="id"` 模式下 key 必须是**字段 ID**（`fldI3KsjPCYWp` / `fldv7ZuB1b06J` / `fldYm8R3l4Bnu`）。**每次 PATCH 后必须回读比对**，这是唯一能发现静默失败的手段 |
| **职称脚本比对取到导航/页脚的职称字样（2026-09-24）** | 脚本按「姓名最后一次出现之后最近的职称词」判定 → 导航、页脚里的 "Professor" 被当成该导师职称，10 条全误报 | 职称比对脚本的结论**必须人工复核**；以院系名录页/个人页资料块的职称字段为准。批量比对只用来缩小人工复核范围，不可直接改数据 |
| **curl 200 当链接有效（美国学校 404 伪装页）** | OSU `medicine.osu.edu/find-faculty/...` 返回 200 但内容显示 "Not Found" | **必须 WebFetch 读内容**，状态码 200 ≠ 页面真实存在 |
| **院系列表页当个人主页** | 全院教师列表页只有姓名+职称，无 CV/Publications | 个人主页必须含专属研究内容；列表页不可接受 |
| **第三方平台当个人主页** | DovePress 编辑简介、ORCID、ResearchGate | 禁止用第三方平台代替大学官方个人主页 |
| **Stipend 系统性低估** | USF 写 `$30K/yr` 实际 `$37K`；TAMU Medical Sciences 写 `$32K` 实际 `$35K` | 每条记录写入前搜索学校官网 stipend 页面核实 |
| **K08 误认为 R01** | "NIH K08→R01(2017-2022)" 中 R01 查无实据 | NIH Reporter 交叉验证 grant 类型、金额、时间线 |
| **中心总计与个人 funding 混淆** | "CRM总计>$20M" 被误认为导师个人 funding | 明确区分"中心总计"与"个人独立 grant" |
| **推测性数据未标注** | "录取率~15-20%""2028年预计" 作为事实陈述 | 标注为"估算""约"，说明无官方来源 |
| **选导顾问自审自填（确认偏误）** | 优录-刘同学案例：同一会话反复复查"没问题"，换新对话框 auditor 查出 7 条 P0 | 批次审核必须 spawn 独立 auditor，不复用选导顾问上下文 |
| **长对话疲劳放过** | 几十轮后对"看起来还行"的记录直接放行，`__trashed` 发现了但 WebFetch 能打开就判有效 | 同一会话处理 30+ 条后开新会话；auditor 有罪推定，主动找理由拒绝 |
| **方向定义书转述失真** | 选导顾问把"干细胞+心血管"转述成"干细胞"，auditor 信了转述，iPSC 副业当核心 | auditor 必须亲自读方向定义书原文，不信任任何人的摘要 |
| **硬排除项漏检** | 线虫模型/纯生信/癌症主线一路漏到最终审核才发现，删除 7 条 = 11% 工作量浪费 | 飞行前清单 6b 硬排除检查是写入前硬门，不是写入后审计项 |
| **备注默认学生知道方向定义（2026-09-02 郝悦嘉）** | 写 `和你的国际金融/开放宏观方向能搭上`，但学生没有方向梳理、看不懂"我的方向"指什么 | 写备注前先确认学生是否持有方向梳理；无方向梳理时备注必须自包含：直接写「导师做什么方向+用什么方法+什么通道」（如 `教授；国际金融与开放宏观方向，实证为主（资本流动、汇率与货币政策传导）`）；有方向梳理时才允许"和你的XX方向"关联句式，且须写具体方向名 |
| **Vika 创建记录 payload 少包 `fields` 层（2026-09-14）** | `{'records': [{字段名: 值}], 'fieldKey':'name'}` → HTTP 500 `api_params_instance_fields_error`，看起来像权限/字段名问题，实际是结构错 | 正确结构：`{'records': [{'fields': {字段名: 值}}], 'fieldKey': 'name'}`。报 `api_params_instance_fields_error` 时先怀疑少了 `fields` 包裹层，不要先去怀疑 token 或字段名 |
| **港五方向被写"枯竭"前先穷举院系名单（2026-09-14 万文睿案例）** | "分析化学（质谱/色谱湿实验定量）"在港五：HKU 分析化学组仅 Ivan Chu、HKUST 仅 Simon Wan Chan、CUHK 仅 Chan Tak Wah（2026 已转 Emeritus）、CityU 仅 Ruan Yuefei、PolyU 仅 Yao Zhongping/Zhou Lei/Zhao Qian——全部已被历史轮次收录，本轮 0 新增。说明"院系口径"下确实枯竭 | 结论要落到具体名单证据（逐院系教职员页 + 分析化学组页面），并主动给用户扩展选项：放宽到医学院/生命科学院的临床质谱平台、或扩容到其他地区 |
| **PolyU ABCT 已拆分（2026-07-01）** | 新记录 Department 仍写 "Department of Applied Biology and Chemical Technology" | PolyU ABCT 于 2026-07-01 拆分为 Department of Chemistry 与 Department of Life Sciences；化学师资的新记录应写 `The Hong Kong Polytechnic University - Department of Chemistry`，教职员列表用 `/chem/people/academic-staff/`，博士申请页用 `/study/pg/rpg/2027/chem`（ABCT 旧页 `/study/pg/rpg/20263/abct` 仍可访问） |
| **点名"高分子合成"时的红线边界（2026-09-14）** | 用户说"选材料化学里的高分子和合成制备、不要电化学"，就容易把"挂了 Polymer 关键词"的人都收进来 | 必须看主页**首个 Research Area / 首句 Research Description**：核心若是器件工程（光伏、OLED、OECT 有机电化学晶体管）、能源存储（电池/超级电容/燃料电池膜）、均相催化与配位-金属有机合成，则不算"高分子合成制备"主线，要么不收、要么按部分匹配降级并如实写明偏离（含任何电化学/能源成分，不得在备注中隐去） |
| **只扫化学系就下"已枯竭"结论（2026-09-14 万文睿案例，用户当场追问"材料科学下面呢？"）** | 第一轮只查化学系/化工系，报"港五方向B 无人"，被用户指出漏了材料类院系 | **材料/高分子类方向必须先穷举材料类院系再下结论**：CityU MSE+MNE、HKUST Department of Materials(2026-07 新设，暂无师资页)+CBE+MAE、PolyU SFT(School of Fashion and Textiles，实为纺织化学/高分子复合材料重镇)+PM(Physics and Materials)+ME、HKU ME、CUHK MAE+Physics+MASE(仅挂靠项目)。港五材料类院系的**高分子方向多数已被电池/超电容/燃料电池膜/OECT 占据**，少数真做件的集中在 PolyU SFT（如 FEI Bin 阻燃高分子复合材料、MA Kaikai MOF/纤维复合材料）与 HKUST MAE（杨晶磊 微胶囊/界面聚合复合材料） |
| **纺织/机械等"非化学系"的导师能不能收（2026-09-14）** | 看到 School of Fashion and Textiles / Mechanical Engineering 就直接判断"院系脱节" | 判断标准是**研究对象是不是高分子/多孔材料本体、制备表征方法能否迁移**，而不是院系名字：PolyU SFT 的高分子复合材料与多孔材料（研究对象即材料本体，纺织只是基材）可以收；CityU MNE 的二维材料力学与器件、HKUST MAE 的力学/航空导向则属于偏离，只能标备选并在备注里写明院系与力学/数据驱动成分 |

---
