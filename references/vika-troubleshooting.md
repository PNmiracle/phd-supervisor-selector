<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载 -->
> **本文含**：Vika 疑难与限制——不可写字段绕法、已知 API 问题（POST 超时 / DELETE 格式 / fieldKey 坑）、限流与最佳实践、待确认导师自查、批量修订备注、新版学生表结构、维格行数上限 309。
> **什么时候读**：写入失败（309 / POST 超时 / 返回 0 条 / 写不进字段）时；要批量修订备注时。
> **什么时候不用读**：一切正常、只做常规读写时。

> 本文由 `vika-guide.md` 于 2026-10-07 按职能拆分而来；入口与核心读写见 `vika-guide.md`。
---

## 11. Non-Writable Fields

These fields **cannot** be written via Fusion API — they are computed or linked:

| Field Type | Examples | Why |
|-----------|----------|-----|
| MagicLookUp | Location, QS排名, USNEWS排名 | Computed from linked records |
| OneWayLink | 学校名字, Location | Link to another datasheet |
| Formula | 等邮件几天 | Auto-calculated |
| LastModifiedTime | 状态变更日期 | Auto-generated |
| CreatedBy / CreatedTime | From, 选导时间 | Auto-generated |

### OneWayLink / MagicLookUp Write Workaround (verified 2026-07-03)

**Problem**: Vika API rejects OneWayLink/MagicLookUp fields with "Lookup field can't be edited" when using `fieldKey=name`.

**Solution**: Use **field NAMES** as keys, with a **list of record ID strings** as the value. Works with or without `fieldKey` in body.

```python
# Works — field name key + list of record ID strings
body = {
    "records": [
        {"recordId": "recXXX", "fields": {"学校名字": ["recSchoolId123"]}}
    ]
    # fieldKey can be "name" or omitted (defaults to name mode)
}

# Fails (400) — field ID key without fieldKey="id"
body = {
    "records": [
        {"recordId": "recXXX", "fields": {"fldFfXtdDSST1": ["recSchoolId123"]}}
    ]
}
```

**Workaround for creating records with linked fields**:
1. POST record WITHOUT `学校名字` and `Location` fields (use `fieldKey=name` for regular fields)
2. PATCH the record WITHOUT `fieldKey` to set `学校名字: [school_record_id]`
3. `Location` and `QS排名` will auto-fill after school link is set

**POST 创建时也可以写 OneWayLink**（2026-08-20 实测）：字段名做 key + 数组值 + **不带 fieldKey 参数**即可成功，无需分两步。

⚠️ **关键提醒**（2026-08-21 实测）：POST 创建带 OneWayLink 字段时，**绝对不能**在请求体中包含 `fieldKey` 参数，否则会返回 `api_params_instance_fields_error`（HTTP 500），即使空记录也报错。这个错误信息完全没有提示是 `fieldKey` 导致的。

---


## 12. Known API Issues

### POST Requests Timeout — GET Works, POST Fails (2026-08-26 confirmed)

**现象**：所有 POST 请求（创建/更新记录）持续超时，GET 正常。
- Python `urlopen`: `TimeoutError: The read operation timed out`
- curl: exit 28 (timeout) 或 exit 137 (SIGKILL)
- httpx/requests: `ReadTimeout`
- 所有库、所有 timeout 值（10s/60s/90s/150s）一致失败
- **GET 完全正常**（1-2s 内返回 200）
- 不受代理设置影响（`unset HTTP_PROXY` 也失败）

**影响**：无法创建学校记录、导师记录，无法 PATCH 更新。

**根因**：Vika 服务器对 POST 请求不返回任何响应（连接建立成功，body 发送成功，但服务器 0 字节响应后挂起）。可能是服务端维护、地区屏蔽或速率限制。

**临时方案**：
- 等待 Vika 服务恢复后重试
- 可设置循环重试脚本（间隔 5-10 分钟）
- 如需紧急写入，考虑网页端手动录入

**验证脚本**：
```python
import json, ssl
from urllib.request import Request, urlopen

with open('env.json') as f:
    token = json.load(f)['VIKA_TOKEN']

ctx = ssl.create_default_context()
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

url = 'https://api.vika.cn/fusion/v1/datasheets/dstMNzQU9Aa58DpgW3/records'
data = json.dumps({'fields': {'学校全称': 'Test'}}).encode()
req = Request(url, data=data, headers=headers, method='POST')
try:
    with urlopen(req, timeout=15, context=ctx) as r:
        print('SUCCESS:', r.status)
except Exception as e:
    print('POST FAILED:', type(e).__name__, str(e)[:100])
```

### DELETE Format (Critical)

Vika DELETE API uses query parameter, NOT request body. The `vika()` function handles this automatically.

### 临时脚本 PATCH/POST 必须带完整路径（2026-09-14 实测坑）

写一次性脚本改动记录时，容易把路径写成 `"/records"`。返回 **404 `{"success":false,"code":404,"message":"The API does not exist"}`**，而且不会提示是路径问题，极易被误读成"权限不足"或"字段不可写"。

```python
# ✅ 正确：路径必须含 datasheets/{dst}
req("PATCH", f"/datasheets/{DATASET}/records", {"records": [...], "fieldKey": "name"})
req("POST",  f"/datasheets/{DATASET}/records", {"records": [...]})

# ❌ 错误：404 The API does not exist（无任何有用提示）
req("PATCH", "/records", {...})
```

判断依据：如果封装过的 `vika()` helper（内部已拼 `f"/datasheets/{DATASET}{path}"`）能成功、而临时脚本失败，几乎一定是路径少了前缀。**写入后一定要 GET 回读确认**，不要只看脚本打印的 "ok"。

### ⚠️ 返回体判定键是 `success`，不是 `ok`（2026-09-16 实测坑）

自写执行脚本时容易用 `r.get("ok")` 判定成功与否。Fusion API 的返回体形如
`{"code": 200, "success": true, "data": {"records": [...]}}` —— **没有 `ok` 字段**。
用 `r.get("ok")` 会把成功误判为失败，进而重复写入或错误回滚。

```python
# ✅ 正确
if r.get("success"):
    created.extend(r["data"]["records"])

# ❌ 错误：永远取到 None，成功也走失败分支
if r.get("ok"):
```

注意：`lark-cli` 的返回体才用 `"ok": true`（飞书 CLI），两套 API 判定键不同，别混用。
**批量写入后务必 GET 回读，用 total 条数与记录内容核对**，这是唯一可靠的成功判据。

### ⚠️ 写表前必须重新拉取最新快照（2026-09-18 实测坑）

线上表**可能正被人并行 curation**。用几小时前导出的快照里的 recordId 去 PATCH，会报
`{"success":false,"code":400,"message":"The record specified by the recordId does not exist"}`
—— 记录已被人工删除，**错误信息不提示"记录已消失"，极易误判成字段/权限问题**。

实测案例：一次批量改链接时，AUT 记录集已从 24 条变成 18 条（人工删了 7 条、新增 1 条，表总数 351→345），旧快照的所有 recordId 全部失效。

```python
# ✅ 正确：动手前先 dump 最新快照
dump(ds, "now.json"); recs = json.load(open("now.json"))
# ❌ 错误：复用几小时前的快照，recordId 可能已失效
recs = json.load(open("final_aut.json"))
```

**配套规则**：
1. 每次增删改前重新 dump，不复用上一轮导出的快照。
2. 条数或记录集与预期不符时**先停手比对差异**（按 `导师` 名比对新旧快照的增删），确认人工改了什么再决定动作。
3. **人工删除的记录不要自行恢复** —— 那是刻意的 curation 决定。人工新增的记录若属同一批量任务范围（如同一列链接统一修正），可一并处理，但要在汇报里说明。
4. 批量 PATCH 失败时按单条重试并打印每条返回，可立刻定位是"个别 recordId 失效"还是"整批语法错误"。

### GET Cache Staleness

After DELETE or PATCH, subsequent GET requests may return stale data from an API cache. The Vika UI typically reflects changes faster than the API. Always verify in the UI after making changes.

### URL Field PATCH with fieldKey="name" Returns 200 but Silently Fails

See section 4.2 above. URL-type fields require field IDs without `fieldKey` parameter.

### 回读验证的两个陷阱（2026-07-17 实战教训）

1. **GET 回读必须用字段名，不能用 field ID**。PATCH 用 `fieldKey="id"` 写入后，GET（不带 fieldKey 参数）返回的 fields 字典是**字段名键**。用 `fields.get("fldXXX")` 读取永远是 None，会误判写入失败。
2. **用户可能在两次会话之间改了字段名**（例如 `导师主页` → `导师主页（⭐️看这里）`）。字段 ID 不变，写入照常成功，但按旧字段名回读会得到 None，造成"写入没生效"的假象。**批量写入前后都应重新拉一次 `GET /fields` 确认当前字段名**，回读以字段名为准。判读写入是否成功的可靠依据：PATCH 响应体回显的字段值 + 按当前字段名 GET 的值一致。

---


## 13. Rate Limits & Best Practices

- **10 records max** per POST/PATCH/DELETE request
- **0.3-0.5s delay** between batches
- 175 records = 15 batches = 15-20 seconds total
- Use `fieldKey: "name"` for Chinese field names (except for URL field PATCH)
- Always `strip()` names before comparison
- URL fields accept plain strings (API wraps them)

### 长文本批量 PATCH 连接重置（2026-08-25 实战教训）

**现象**：一次 PATCH 10 条备注（每条 50-150 字长文本）时，`Connection reset by peer`（Errno 54），整批失败、0 条生效。同样的请求内容改小批次后成功。

**原因**：请求体过大 + 网络不稳定，Vika API 或中间链路断开连接。**返回 200 不一定成功，连接重置则一定失败**——PATCH 后必须 GET 回读确认。

**正确做法**：
1. **每批 5 条**（备注长文本场景，不要用满 10 条上限）
2. 请求加 `timeout=30`
3. 加重试循环（3 次，间隔 1.5s）
4. PATCH 后 GET 回读全部记录，确认每条都是新内容
5. 批量修复前先做全量备份（`GET /records` 全量存 JSON 到本地），删除/修改不可逆时尤其重要

---

### 写入后必做的「空值扫描 + 通用链接扫描」（2026-09-22 实战教训）

**教训**：某轮批量写入 126 条后，自查脚本只校验了 `导师` / `Department` / `导师主页` / `博士申请信息` / `其他导师信息` / `备注` / `学校名字` / `Location` 八个字段，**漏掉了 `导师研究领域`**——结果 16 条港中深 SDS + 4 条港中深 HSS 记录的该字段静默留空，直到下一轮复核才被发现。原因是提取脚本只认 `Research Field` 标签，而 HSS 页面用的是 `Research`。

**因此写入后必须跑这两个扫描，缺一不可**：

```python
# ① 空值扫描：覆盖所有应当有值的列（不要手写字段清单，直接从 GET /fields 拉全部字段名）
EMPTY = [r["fields"].get("导师") for r in mine
         if not (r["fields"].get("导师研究领域") or "").strip()]

# ② 通用链接扫描：统计 (学校, 博士申请信息) 的重复度
#    同一 URL 在「同一院系」内共用 → 正常
#    同一 URL 跨院系/跨学院大量共用 → 误填了全校入口，必须逐条改
```

**高频漏填/误填字段清单**（按踩坑频率）：
1. `导师研究领域` —— 提取脚本字段标签不匹配时整批静默跳过
2. `博士申请信息` —— 抓不到项目页时退回填学院首页或全校入口
3. `其他导师信息` —— 有时填了个人主页而非院系师资名单页

写入流程的收尾动作固定为：**空值扫描 → 通用链接扫描 → 随机抽样打开链接确认页面主体是该导师/该项目 → 交给独立审核官**。前两步是机械的，能在 30 秒内跑完，不要省。

---


## 14. 待确认导师自查流程

当用户说"检查新加导师"时，获取所有 `待确认导师` = `新加待check` 的记录进行自查：

```python
from urllib.parse import quote

# 获取所有待确认导师=新加待check 的记录
filter_expr = quote('{待确认导师}="新加待check"')
result = vika("GET", f"/records?filterByFormula={filter_expr}&maxRecords=200&cellFormat=string")
pending = result["data"]["records"]

print(f"待检查记录: {len(pending)} 条")
for r in pending:
    f = r["fields"]
    print(f"  [{r['recordId']}] {f.get('导师','?')} | {f.get('备注','?')[:60]}")
```

自查项目（逐条执行，不自动放行）：
1. 导师主页 URL 可访问且为个人页面
2. 姓名/职称/院系与主页一致
3. 研究方向匹配度合理
4. 备注格式三段式
5. 备注无禁止内容
6. 博士申请信息 & 其他导师信息 URL 有效
7. 无遗漏风险标注
8. 非 Emeritus/退休/Visiting
9. 无重复（与选导意向非空记录比对）

检查完毕输出通过/修正/建议删除三类清单。**不自动清空 `待确认导师`**，提醒用户人工抽检后手动清空。


---


## 🔁 批量修订已有记录的备注（2026-09-29 实操，可直接复用）（自 SKILL.md 迁入 2026-10-07）


写完之后才发现备注要改，是常见场景（措辞返工、后缀重复超限、补偏离说明）。流程与陷阱如下。

#### 接口
```python
# 单字段批量更新（不动其他字段，尤其不要碰人工填写的「选导意向」）
PATCH /datasheets/{DS}/records
body = {"records": [{"recordId": "recXXX", "fields": {"备注": "<新文本>"}}]}
```
- **每批 5 条**（与 POST 同量级，别一次塞 10 条以上）。
- **写入前先把旧值 dump 成 `notes_backup.json`**，便于回滚和事后 diff。
- PATCH 是**整字段替换**，不是 append——新文本必须自带完整内容。

#### ⚠️ 陷阱：用关键词筛「带后缀的记录」会漏

想筛出「所有带备选/后放后缀的记录」时，**不要**写 `if "备选" in note or "后放" in note`：
- `可以往后放一放～` 含「后放」✓ 能命中
- `可以放后面一点～` / `可以往XX方向靠～` **两个字都不含，全部漏掉** ❌

实测：16 条带后缀记录，关键词法只命中 12 条，**静默漏 4 条**。
**正确做法：用完整后缀列表匹配。**

```python
ALIASES = ["可以备选一下呢～", "可以往后放一放～", "作为备选看看～",
           "可以放后面一点～", "可以往XX方向靠～", "可以后放～"]
targets = {r["name"]: r["note"] for r in RECORDS if any(k in r["note"] for k in ALIASES)}
```

#### 匹配与校验三步
1. **归一化姓名匹配，并要求唯一命中**（`len(hits) != 1` 就中止，不要取第一条）。
2. 写入后**逐条回读比对**（新值 == 线上值才算成功）。
3. 再查三件事：记录总数**未变**、原有记录的**人工字段未变**（逐条比对 `选导意向`）、三个 URL 字段仍是**链接对象**。

> 同名教师重名风险虽低，但「姓氏相同、名字缩写相同」的两人（如多个 `J. WANG`）在归一化后可能撞车，务必唯一命中才写。


---


## 🆕 2026-09 新版学生表结构（统一学校主表）· 2026-09-29 实测（自 SKILL.md 迁入 2026-10-07）


机构已把学生表迁移到新版结构，**字段与关联方式都变了**。拿到新分享链接时先跑一遍字段读取，不要套用旧表参数。

| | 旧版 | **新版** |
|---|---|---|
| 学生表 | `dst0ND4xFmVYCEhp9W` | 由分享链接现取（如 `dst1uE8b1LcYULFCEu`） |
| 学校关联 | **两个** OneWayLink：`美国学校` + `非美国地区学校` | **一个** OneWayLink：**`学校`**（`fldLcSSXtr0B7`） |
| 学校主表 | 两张：`dstHnRL5BSi3F9MiiW`（US）/ `dstlDbcfonUfUcWwRG`（非美） | **一张统一表**（如 `dstMNzQU9Aa58DpgW3`，2208 行） |
| QS 口径 | 2026 | **2027**（MagicLookUp 自动带出，Excel 镜像要对齐同一口径，否则与线上不一致） |

**统一学校主表字段**：`学校全称`、`学校中文名`、`学校英文缩写`、`2027年QS排名`、`2026年QS排名`、`2025年QS排名`、`2026年USNews排名`、`国家/地区`、`所在大洲`、`美国学校所在州`、`国内学校层次`、`国内学校所在省份`。

**新旧切换要点**：
1. 字段名从「非美国地区学校」变成「学校」，**写 `fieldKey=name` 的 POST 里必须同步改**，否则链接静默丢失。
2. `导师主页`/`博士申请信息`/`其他导师信息` 三个 URL 字段 **ID 未变**（`fldv7ZuB1b06J` / `fldYm8R3l4Bnu` / `fldI3KsjPCYWp`），两段式写入的第二段可原样复用。
3. **新的统一主表没有 1000 行分页上限**（旧的非美主表有），`pageSize=500` 可一次翻完 2208 行，建索引比逐校 `recordIds` 查询更省事——但两种都可行。
4. 校名匹配要**归一化后精确比对**（新主表里写的是 `The University of Hong Kong`，旧表写的是 `The University of Hong Kong（HKU）`；`City University of Hong Kong` vs `香港城市大学` 中文名字段另存）。用 `NFKC + 去括号/空格/标点 + lower` 再比，9 所目标校全部唯一命中。
5. **迁移后的新表通常已含旧表全部记录**，人工字段（`选导意向` 等）会原样带过来。写入前必须做同名去重，写入后必须**逐一比对原记录的 `选导意向` 是否被动过**——这是「保护已锁定记录」的硬要求。
6. 写后必查三件事：① 三个 URL 字段是否为**正式链接对象**（不带 `cellFormat=string` 时返回 `{title,text,favicon}`，而不是纯字符串）；② `学校` 是否返回 `["recXXX"]` 数组；③ `Location`／`QS排名` 等 MagicLookUp 是否已被主表带出。

#### 归一化校名比对模板

```python
import re, unicodedata
def norm(s):
    s = unicodedata.normalize("NFKC", s or "").lower()
    return re.sub(r"[（()）\s,.\-–—&']", "", s)
# 先精确等值，未命中再放宽为子串双向包含；放宽后若命中 >1 条，必须人工裁决，不要取第一条
hits = [x for x in idx if norm(x.name) == norm(target)] or \
       [x for x in idx if norm(target) in norm(x.name) or norm(x.name) in norm(target)]
```

---


---


## 🔴 维格空间行数上限：写入会被 309 拒绝（2026-09-20 实测，必须前置检查）（自 SKILL.md 迁入 2026-10-07）


**症状**：`POST /datasheets/{ds}/records` 返回

```json
{"success": false, "code": 309,
 "message": "{\"key\":\"max_rows_in_space\",\"specification\":20000,\"usage\":37427}"}
```

**这是账号级配额**，不是表权限、不是 token、不是 payload 结构问题。表现特征：

- **单条也写不进去**（先测 1 条即可确诊，不要浪费 99 条去试）；**连试 5–6 次结果完全一致 → 可排除间歇性拦截**，不要在这上面反复重试；
- 同一账号下**所有** datasheet 的新建都被拒；
- `GET` 读取、`PATCH` 更新既有记录不受影响（行数没增加），所以**链接修复类任务照常可做**；
- `usage` 可能已经**大于** `specification`（套餐被降级的情形），此时无论如何都建不了新行。

**怎么确认到底是"这个空间满了"还是"整个账号满了"**（只读，一分钟搞定，别急着下结论）：

```text
GET /spaces                                  → 列出账号下全部空间
GET /spaces/{spaceId}/nodes?type=Datasheet   → 列出该空间所有数据表（pageSize 给 1000）
GET /datasheets/{ds}/records?pageSize=1      → 响应里 data.total 就是该表行数（不用真拉数据）
```

把每个空间的行数加总：**若单个空间未超上限、但合计超了，就是账号级配额**。2026-09-21 实测案例：目标表所在空间只有 11,987 行（远低于 2 万），但账号下 6 个空间合计约 4.45 万行，维格自报用量 37,427 —— 单看那个空间会误判成"表没问题，是不是权限问题"，白查半天。统计时 8 并发跑 600+ 张表约 45 秒。

**报告给用户时要给可操作的解封路径**：列出各空间的行数分布，指出最大的几个占用方（多数是历史年度库），并给出"升级套餐"与"归档历史库把总量压到上限以下"两条路线。

**正确的处理顺序**：

1. 任务一开始（拿到 Vika 链接后）**先做一次单条 POST 探针**，确认能写，再投入搜索。**不要搜完 100 条才发现写不进去。**
2. 若被拒：
   - 立刻停止写入尝试，**不要**用"删旧记录腾地方"的办法绕（删他人记录属高危且被明令禁止）；
   - 走**Excel 回退模式**交付：列结构与表一致（导师 / 学校 / Ranking / Location / Department / 导师联系方式 / 导师主页 / 博士申请信息 / 其他导师信息 / 备注），并保留一份 JSON payload，配额解除后可一次性批量导入；
   - **把导入做成一条命令**（`import_to_vika.py`）：内置 `--dry-run` 演练、断点续跑（表内已有的同名导师自动跳过）、每批 5 条、失败即停、写后回读校验。交付前必须跑一次 `--dry-run`，确认「链接格式 + 学校关联可解析 + 与表内零重名」三项全过，这样配额一解除就能直接跑，不必重新搜索或核验；
   - 若用户需要先看结果，额外生成一个**离线 HTML 预览**（按地区筛选 + 关键词搜索），零风险、不污染对方生产表格；
   - 回写飞书看板 `AI 反馈`，写明配额数值（上限 / 当前用量）、接口返回码 309、各空间行数分布、以及需人工升级套餐或归档历史库；
   - 在最终回复里如实告知用户"写入被阻断"，不要静默降级成"已完成"。

---

## 🔴 DELETE 的返回体没有 `data` 键；批量删除会静默失败（2026-10-12 实测）

**现象**：`DELETE /datasheets/{ds}/records?recordIds=a,b,c,...`（8 条）返回
`{"code":200,"success":true,"message":"SUCCESS"}` 或 `{"success":false,"code":400,"message":"..."}`，
**都没有 `data` 键**。用 `res["data"]["records"]` 取值会直接 `KeyError: 'data'`；
更糟的是一种「返回不报错、但记录还在」的情况——脚本若只 `print` 不读 `success`
就会误判为删除成功。实测 8 条一批的删除**没有生效**（回读发现导师名仍在表内）。

**可靠做法**：
1. **逐条删除**（一次一个 recordId），删完立刻读返回体的 `success` 字段，不要读 `data`；
   ```python
   url = f"{BASE}/datasheets/{DS}/records?recordIds={rid}"
   req = Request(url, headers={"Authorization": f"Bearer {TOKEN}"}, method="DELETE")  # 不带 Content-Type
   body = json.loads(urlopen(req).read())
   ok = body.get("success") is True
   ```
2. 批间 `time.sleep(1.0)`；
3. 全部删完后**重新 GET 全表**，逐个确认目标 recordId/导师名已消失——这是唯一可靠的确认方式。

## 混合通道核验链接：curl 打头，Chrome 无头兜底（2026-10-12 实测）

本轮 70 位候选人 × 3 个 URL 的核验流程（可复用）：

1. 先 `curl -sL --max-time 30 -A "<完整浏览器 UA>" --compressed`。**`timeout` 命令在 macOS 不存在**，别用它包命令。
2. curl 返回 200 但 `size < 2000`、或（对个人页）正文不含该导师姓名时，再上
   `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --headless=new --disable-gpu --no-sandbox
   --user-data-dir=<临时目录> --no-first-run --virtual-time-budget=10000 --dump-dom "<url>"`。
3. ⚠️ **Chrome 子进程必须加 `subprocess.run(..., timeout=25)`，并在 `finally` 里
   `shutil.rmtree(临时 profile 目录)` + `pkill -f <profile 前缀>`**。否则 Chrome 不会干净退出，
   实测会堆积 30+ 个进程和十几份残留 profile，把整轮核验拖到几十分钟甚至卡死。
4. **结果增量落盘**（每处理完一个人就 `json.dump` 一次），不要等全部跑完再写文件——进程被工具超时杀掉时不会全丢。
5. 403 / 429 / 202 不等于失效：换个通道（WebFetch 或 Chrome）再看；若替换 URL 是子代理实际打开并核对过内容的，
   可按「反爬（子代理已打开核验）」放行，但**必须在交付报告里单列说明**，不要当成直接 200 核验。

## 🔴 批量 POST 可能「部分成功却整体报 500」（2026-10-13 实测，必读）

**现象**：97 条记录按 5 条一批 POST（共 20 批），前 17 批成功、第 18 批抛 `HTTPError: HTTP Error 500`，
脚本直接 `SystemExit` → **看起来全军覆没，实际已有 85 条落库**。
随后我用一个不带判重的调试脚本「测试」前 12 条 → **重复写入 12 条**，只能逐条 DELETE 清理。

**强制做法**：
1. 写入前**先拉全表**，建「已存在导师名」集合；逐条写入时先判重再 POST；
   批量 POST 失败时**不要假设全部失败**，必须回读确认。
2. 写入后按 `recordId`（POST 返回值）逐个回读校验，再比对「导师名 → recordId」是否命中。
3. **任何调试/补写脚本都必须带判重**，否则一次误跑就制造重复记录。
4. 重复记录的清理：按导师名分组 → 每组保留字段最全的一条 → 其余逐条 DELETE → 再回读确认。
5. 逐条 POST 比批量稳（本次 97 条逐条 + `sleep(0.6)` 全部成功，约 70 秒），数据量大时优先逐条。

## ⚠️ `cellFormat=string` 会改变「学校名字」关联字段的返回形态（2026-10-13 实测）

- **不带** `cellFormat=string`：`fields["学校名字"] == ["recEfSjrZePcd"]`（关联记录的 recordId 数组）→ 可用来做关联。
- **带** `cellFormat=string`：同一字段返回的是**学校名字符串**（不是 recordId 数组），
  同名记录无法消歧，且对「说明行」（导师列为空）可能显示为空 → 用 `not fields.get("学校名字")`
  判断「是否已设学校关联」会**误判为未设关联**。

**结论**：需要读/写关联 recordId 时，拉记录**不要带** `cellFormat=string`；只读文本展示时才带。

## 说明行（学校说明）与导师行的字段差异

- 说明行只有 `学校名字` + `备注` 两个字段，其余 7 列按设计为空 →
  字段完整性检查会对说明行报大量 FAIL，属误报，需在检查里按「导师列为空」跳过。
- 同理，说明行的 `备注` 是学校情况说明，**没有职称首段**，职称检查也必须跳过。

## 🔴 准入口径收紧后批量删除：两处致命坑（2026-10-15 实测，必读）

场景：用户把准入口径从「有对口导师即可」收紧为「QS 综合前 100 **或** 专业排名前 20」，
要求把不达标学校整所删干净。76 所 / 141 条 → 删 33 条。过程中踩到两个坑：

### 坑 1：删除名单必须用明确的 DROP 集合，绝不能用「补集」逻辑

**错误写法**：构造 `KEEP = 满足条件的 QS>100 学校`，然后 `if 学校名 not in KEEP: 待删`。
结果把 **31 所 QS≤100 的学校也全部算进待删**（一次性选出 154 条待删，正确应为 37 条）。

原因：QS≤100 的学校根本不在 KEEP 集合里——它们满足的是**另一个**准入条件（综合排名），
而不是被 KEEP 覆盖的那一条。两个准入条件是「或」关系，不能用单集合取补。

**正确做法**：
- **先构造明确的 `DROP` 集合**（例如直接列出「C 档学校名」列表），
  再 `if 学校名 in DROP: 待删`。
- 写完后必须打印 `待删学校数 / 待删条数` 并与预期数字核对，不符就停。

### 坑 2：「确认套磁」字段几乎全是 `0`，**不能**当作学生已填写的判据

全表 100+ 条记录的「确认套磁」都是 `'0'`——这是**复选框控件的默认值**，不代表任何决策。

**真正的填写判据**是这 6 个字段是否非空：
`选导意向（点击选择）` / `你的反馈（具体原因）` / `套磁备注` / `状态` / `后续安排` / `导师回复`

本次正是靠这 6 个字段捞出 Southampton 的 2 条：
Kai Yang（选导意向=优先套磁）、Stephen Beeby（选导意向=优先套磁，导师已有 9.3 邮件回复）。

### 强制流程（收紧口径类删除任务）

1. **先备份**：全表 `GET /records?cellFormat=string` 导出 JSON 落盘（本次 182 行 → `backup_full_*.json`），
   确认行数正确再动删除。
2. **扫敏感字段**：对待删记录检查上述 6 个字段，**任何一条命中就整所学校暂缓**，
   交付给用户定夺，不擅自删（见 SOUL.md「不得删除已选导师记录」边界）。
3. **整所暂缓而非只留命中的几条**：同一所学校只删一半会让学生看到残缺记录；
   本次把 Southampton 4 条全部暂缓。
4. **dry-run 模式**：脚本接受 `dry` / `run` 参数，先跑 dry 打印计划删除与暂缓清单，确认后再 run。
5. **逐条 DELETE + 读 `success`**：批量 DELETE 曾静默失败；逐条删并累加成功/失败计数。
6. **回读验证**：
   - 残留检查：`if 学校名 in DROP` 应只剩暂缓的那些；
   - **残缺检查**：按学校聚合，找出「有说明行但导师记录为 0」的学校——若某保留学校被删空，
     说明误删了本应保留的学校，应立即停工并向用户报告。

### 「专业排名」该用哪张榜

- 服装 / 时尚 / 纺织设计方向 → **QS by Subject: Art & Design**。
- 但该榜**不覆盖**纺织工程、服装人体工学、时尚供应链管理——而这些常是学生的真实方向。
  只用它判定会把 NC State（Wilson College of Textiles，北美纺织第一）、
  Iowa State（AESHM）、TMU（School of Fashion，加拿大第一）、Heriot-Watt（英国纺织教育发源地）
  全部误杀。
- **因此必须给用户三选一**，不要替他决定：
  ① 只用 QS 学科榜前 20（最严）② 学科榜前 100 ③ 学科榜前 20 + 专业领域公认强院（本次用户选此）。
- 2026 版 QS Art & Design 前 150 完整名单可从
  `betteredu.net/universityranking/491.html` 的 `?page=2`（51-100）与 `?page=3`（101-150）抓取。
