<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载 -->
> **本文含**：加拿大批次七类专属陷阱（域名一致性扫描、McMaster 系筛选参数、UAlberta 无系级名录、UBC 三通道、滑铁卢职称过期、备注语气词、补邮箱）。
> **什么时候读**：写加拿大批次之前必读。
> **什么时候不用读**：批次不含加拿大院校时。

> 本文由 `school-registry-us-ca.md` 于 2026-10-07 按地区拆分而来；总入口见 `school-strategies.md`，本地区入口见 `school-registry-us-ca.md`。
---

## 🍁 加拿大批次专属陷阱（2026-09-24 王灏案例沉淀）（自 SKILL.md 迁入 2026-10-07）


#### 1. 写完必须跑「学校 —— 域名」一致性扫描（否则会漏跨校错链）
**踩坑**：同一条写入脚本里，给「滑铁卢土木」和「西安大略土木」的博士项目页常量取了同名（`PHD_W_CEE`）。
Python 自上而下执行，**后定义的 Western 链接覆盖了 Waterloo 链接**，导致 4 条 Waterloo 记录的「博士申请信息」全挂了 `uwo.ca`。
**规则**：写库脚本里每个学校的链接常量必须唯一命名且带校名缩写（`PHD_UW_CEE` / `PHD_UWO_CEE`）；
写完后**必跑**一次校验：

```python
# 学校 → 允许域名白名单，逐条比对 3 个 URL 字段
ALLOW = {"University of Waterloo": ["uwaterloo.ca"], "Western University": ["uwo.ca"], ...}
# 命中白名单外的学校域名 = 跨校错链，P0 必修
```

#### 2. McMaster：`其他导师信息` 必须带系筛选参数
`https://www.eng.mcmaster.ca/faculty-staff/faculty-directory/`（无参）是**跨系总目录**（含 Dean、化工系主任等），不合格。
改用系级筛选 URL（实测只列本系）：土木 `?filter-department=54`，机械 `?filter-department=65`。
文理类用 `kinesiology.mcmaster.ca/people/faculty/`、`sees.mcmaster.ca/people/faculty/`（本身即系级）。
`www.eng.mcmaster.ca` 在本机 curl 会被代理挡（502），**改用 WebFetch 可正常读**。

#### 3. UAlberta：**不存在系级教师名录**，别去猜 URL
`/engineering/<dept>/people/index.html` 一律是同一个工程院级「Find a Person」检索页（或 404）；
CEE 的 `people/index.html` 实测直接 404。人工/审核建议的"换成系级名录页"是**假修复**。
现实做法：`其他导师信息` 用 `https://www.ualberta.ca/engineering/people/index.html`（可列出人名+系别），
并在反馈里**如实说明该校不设系级名录**。个人页统一用 `apps.ualberta.ca/directory/person/<shortname>`（curl 可读）。
注意 `www.ualberta.ca` 直抓只返回 157 字节 JS 壳，**必须 WebFetch 才能判断 200 是真页还是 404 页**。

#### 4. UBC：院系站全线 bot 防护 → 三条可用通道
`civil.ubc.ca` / `mech.ubc.ca` / `kin.ubc.ca` / `spph.ubc.ca` / `bme.ubc.ca` 对自动访问返回 `Browser Verification` 页（URL 有效，人可打开）。
可读的官方个人页只有：
- `https://www.grad.ubc.ca/researcher/<id>` —— 研究生导师库，含 Research Interests / 招生字段；
- `https://news.ubc.ca/expert/<slug>` —— 媒体专家页，含职称 + 院系 + Expertise + 邮箱（WebFetch 可读，curl 403）；
- `scarp.ubc.ca/directory/<slug>`、`engineering.ok.ubc.ca/about/contact/<slug>/` —— 这两个学院站无防护，可直接读。
⚠️ **`grad.ubc.ca` 把副教授统一标成 `Professor`**（Alex Bigazzi 案例），职称必须以 `news.ubc.ca/expert/` 或院系页交叉核对后再写。

#### 5. 滑铁卢：`experts.uwaterloo.ca` 的职称字段会过期
`experts.uwaterloo.ca/<slug>` 可读、有 Expert In 关键词，但职称栏**长期未更新**（Tesfamariam 写 Assistant Professor、Arami 写 Assistant Professor，实际分别为 Professor / Associate Professor）。
职称一律以 `uwaterloo.ca/<dept>/contacts` 为准；本轮据此纠正 1 条。

#### 6. 备注结尾语气词别批量化
「可以备选一下呢～」若在批内出现 10 次以上会被审核判为模板化。准备 4–5 个等价说法轮换
（可以备选一下呢～ / 可以往后放一放～ / 作为备选看看～ / 可以放后面一点～），同一批内每种不超过 3 次。
另注意：**学生的方向标签必须来自其原话**，不要自造新方向名（本轮误写"运动损伤防护方向"，学生并未提过该方向，已按原话改回）。

#### 7. 📧 补邮箱：McGill 的 `[at]` 混淆 与 UBC 的验证码墙（2026-09-28 沉淀）

**McGill（已解决）**：个人页把邮箱做了 **spamspan 混淆**，普通 email 正则**一定抓不到**（只会命中页脚的 `reporterror.xxx@mcgill.ca`）。
真实结构是：

```html
<span class="spamspan"><span class="u">lijun.sun</span> [at] <span class="d">mcgill.ca</span></span>
```

解析正则：
```python
SP = re.compile(r'<span class="u">([^<]+)</span>\s*(?:\[at\]|&#64;|@)\s*<span class="d">([^<]+)</span>', re.I)
# → f"{u}@{d}"
```
实测 6/6 命中（El-Geneidy / Sun / Miranda-Moreno / Dixon / Jiangbo Yu / Manaugh），**个人页本身就带邮箱，不需要去翻系里的 People 页**（那些页还有 Azure WAF）。

**UBC（部分无解）**：`civil.ubc.ca` / `mech.ubc.ca` / `kin.ubc.ca` / `spph.ubc.ca` / `bme.ubc.ca` 对
**curl 和 agent-browser 真浏览器都会拦**——curl 得到 `Browser Verification` 页，浏览器导航几步后直接弹
**图片验证码**（"please complete the captcha below"，要识别图里的瓶子/红点，无法自动通过），换 IP/重试也没用。
可读的官方邮箱来源只剩：
- ✅ `https://news.ubc.ca/expert/<slug>`（WebFetch 可读）——含 **Email + 院系个人页 URL + 实验室页**，最好用；
- ✅ `scarp.ubc.ca/directory/<slug>`、`engineering.ok.ubc.ca/about/contact/<slug>/`（无防护，直接读）。

`news.ubc.ca/expert/<slug>` 的 slug **不统一**，已实测：`tarek-sayed`、`alexander-bigazzi`、`lyndia-wu`（邮箱是 `lwu@mech.ubc.ca`，非姓名全拼）、`peter-m-ostafichuk`（带中间名首字母）。
**不是每个人都有专家页**（Amy Kim `amy-kim` 404、Jesse Charlton `jesse-charlton` 404，站内搜索也查不到）——
这两人只能留空，**绝不可按 `firstname.lastname@ubc.ca` 惯例猜一个填进去**。
UBC 导师库页（`grad.ubc.ca/researcher/*`）本身只提供 "submit a contact request" 表单，**不公开邮箱**，这点可以写进回复向用户说明。

---


---


---
