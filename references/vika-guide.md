<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：Vika API 操作手册：Setup 与 URL 解析、新建数据表、schema 查看、读记录五种姿势、批量创建（≤10）、各类型字段更新、删除与去重、Excel 导入、批量补链、跨校链接审计、不可写字段绕法、已知 API 问题（POST 超时、DELETE 格式）
> **什么时候读**：任何 Vika 读写操作之前；遇到 309、POST 超时、OneWayLink / MagicLookUp 写入失败时；要批量修订备注时
> **什么时候不用读**：Excel 回退模式；只做页面抓取、不落库时；只判断导师合格性时

---

# Vika Guide — API 代码模板 + 完整操作指南

零依赖。所有操作使用 Python 3 标准库（`urllib` + `json`）——无需 `vika-cli`、npm 或第三方 SDK。仅需 API token 和任意 Python 3 安装。导入 Excel 时额外需要 `openpyxl`。

---

---

# Vika Guide — API 代码模板 + 完整操作指南

已按职能分册（2026-10-07 拆分）。**本册是核心读写（§0–§5），另两册按需打开：**

| 分册 | 内容 | 什么时候打开 |
|---|---|---|
| `vika-batch-ops.md` | 批量补链 / 查空记录 / 跨校链接审计 / 批量补研究领域 / Excel 导入 | 要批量操作时 |
| `vika-troubleshooting.md` | 不可写字段绕法 / 已知 API 问题 / 限流 / 批量修订备注 / 新版表结构 / 309 上限 | 写入失败或踩坑时 |

---

## 0. Setup

> **Token 安全**：不要把 API Token 贴到聊天框。在终端里跑：
> ```bash
> echo 'export VIKA_TOKEN=uskXXXXXX' >> ~/.zshrc && source ~/.zshrc
> ```
> Agent 从 `$VIKA_TOKEN` 环境变量读取，token 只存在你机器上。

### URL 解析

```
https://vika.cn/share/shrXXX/dstXXX/viwXXX
                              ^^^^^^  ^^^^^^
                           datasheetId  viewId
```

### vika() 函数（所有操作的基础）

```python
import os, json, time
from urllib.request import Request, urlopen

TOKEN = os.environ.get("VIKA_TOKEN", "")
DATASHEET = "dstXXX"  # 从 URL 解析
BASE = "https://api.vika.cn/fusion/v1"

def vika(method, path, body=None):
    url = f"{BASE}/datasheets/{DATASHEET}{path}"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

    # DELETE 用 query parameter ?recordIds=recXXX,recYYY（不是 request body）
    if method == "DELETE" and body:
        if isinstance(body, list):
            url += f"?recordIds={','.join(body)}"
            data = None
        elif isinstance(body, dict) and "records" in body:
            url += f"?recordIds={','.join(body['records'])}"
            data = None
        else:
            data = json.dumps(body).encode() if body else None
    else:
        data = json.dumps(body).encode() if body else None

    req = Request(url, data=data, headers=headers, method=method)
    try:
        resp = urlopen(req)
        raw = resp.read()
        return json.loads(raw) if raw else {"code": 0, "message": "OK", "data": {}}
    except Exception as e:
        try:
            if hasattr(e, 'read'):
                raw = e.read()
                body = json.loads(raw) if raw else {}
                raise Exception(f"API {getattr(e,'code','?')}: {body.get('message',str(e))}")
        except Exception:
            pass
        raise
```

---


## 0.5 新建数据表（新学生 vika链接 为空时）

当用户是「任务发布未进行」的新学生、任务记录里 `vika链接` 字段为空时，需要主动建表。

**关键：Fusion API 支持建表（POST，不是 GET）。** `openapi.vika.cn` 域名无法解析，建表一律走 `api.vika.cn/fusion/v1`。

```python
# POST /fusion/v1/spaces/{spaceId}/datasheets
# 字段 type 的 property 规则（与 GET 返回结构一致）：
#   SingleText → property: {}
#   OneWayLink → property: {"foreignDatasheetId": "<主表id>"}
#   Email / Text / URL → 不传 property（传 {} 会报 400 "Invalid value for fields[xxx].property"）
#   SingleSelect → property: {"options": [{"name": "选项1"}, ...]}
fields = [
    {'type':'SingleText','name':'导师','property':{}},
    {'type':'OneWayLink','name':'学校名字','property':{'foreignDatasheetId':'dstMNzQU9Aa58DpgW3'}},
    {'type':'SingleText','name':'Department','property':{}},
    {'type':'Email','name':'导师联系方式'},
    {'type':'Text','name':'导师研究领域'},
    {'type':'URL','name':'导师主页'},
    {'type':'URL','name':'博士申请信息'},
    {'type':'Text','name':'备注'},
    {'type':'URL','name':'其他导师信息'},
    {'type':'SingleSelect','name':'选导意向（点击选择）','property':{'options':[{'name':'优先套磁'},{'name':'第二批套磁'},{'name':'完全不考虑'}]}},
]
data = json.dumps({'name':'XXX-Supervisor List','fields':fields}).encode()
req = Request('https://api.vika.cn/fusion/v1/spaces/{spaceId}/datasheets', data=data, method='POST')
# 返回 data.id 即新表 datasheetId
```

**注意**：
- 建表后会自动附带约 3 条空记录，写入前先 GET 找出 `导师` 为空的行并 DELETE。
- 字段类型名参考：`SingleText`、`Text`、`URL`、`Email`、`SingleSelect`、`OneWayLink`、`Checkbox`、`Attachment`。注意 `SingleText` 和 `Text` 是不同类型。
- 学生类型判断：先读某个同 space 模板表（如「模板⭐️」）的字段，看 `学校名字` OneWayLink 的 `foreignDatasheetId` 指向哪个主表。指向 `dstMNzQU9Aa58DpgW3`（学校主表_2027QS排名）＝新学生统一主表模式。
- **Fusion API 无法生成分享链接**（share 接口 404）。只能回填 `https://vika.cn/workbench/{dstXXX}/{viwXXX}` 格式的 workbench 链接，分享链接需用户在网页端点「分享」手动生成。
- 视图 ID 获取：`GET /datasheets/{dst}/views`。

---


## 1. View Table Schema

```python
result = vika("GET", "/fields")
for f in result["data"]["fields"]:
    print(f"{f['name']:20s} [{f['type']}]")
    if f['type'] == 'SingleSelect':
        opts = [o['name'] for o in f.get('property',{}).get('options',[])]
        print(f"  Options: {opts}")
```

---


## 2. Read Records

### 2.1 All Records

```python
result = vika("GET", "/records?maxRecords=200&pageSize=200")
records = result["data"]["records"]
total = result["data"]["total"]
```

Page size max 200. For >200 records, paginate with `pageNum` or `pageToken` parameter.

### 2.2 Filtered by Formula

```python
from urllib.parse import quote
filter_expr = quote('{状态}="待发邮件"')
result = vika("GET", f"/records?filterByFormula={filter_expr}&maxRecords=200")
```

### 2.3 By Specific View

```python
result = vika("GET", "/records?viewId=viwXXX&maxRecords=200")
```

### 2.4 Only Specific Fields

```python
from urllib.parse import quote
path = f"/records?fields={quote('导师,Department,备注')}&maxRecords=200"
result = vika("GET", path)
```

### 2.5 String Format (避免嵌套对象)

```python
result = vika("GET", "/records?maxRecords=200&pageSize=200&cellFormat=string")
```

使用 `cellFormat=string` 获取纯文本值，避免 URL 字段返回 `{"text":"...","link":"..."}` 嵌套对象。

---


## 3. Create Records (Batch up to 10)

```python
new_records = [
    {"fields": {"导师": "张三", "Department": "心理学院(XX大学)", "备注": "教授；决策研究。", "待确认导师": "新加待check"}},
    {"fields": {"导师": "李四", "Department": "商学院(YY大学)", "备注": "副教授；消费者行为。", "待确认导师": "新加待check"}},
]
result = vika("POST", "/records", {"records": new_records, "fieldKey": "name"})
print(f"Created {len(result['data']['records'])} records")
```

For batch > 10, loop with delay:
```python
for i in range(0, len(all_records), 10):
    batch = all_records[i:i+10]
    vika("POST", "/records", {"records": batch, "fieldKey": "name"})
    time.sleep(0.3)
```

### ⚠️ OneWayLink 字段必须为数组（2026-08-20 实测教训）

**根因**：Fusion API 对 OneWayLink 字段的值类型要求极其严格——传入字符串 `"recordId"` 或 `{"recordId":"..."}` 都报 400，但错误信息没有提示。调试过程浪费了多轮排查。

**正确格式**：OneWayLink 字段的值必须是**只含 recordId 字符串的数组**，不带 `recordId` 键名：

```python
# ✅ 正确：数组，只含 recordId 字符串
{"fields": {"非美国地区学校": ["recKHysoFjpF8"]}}

# ❌ 错误：字符串（400）
{"fields": {"非美国地区学校": "recKHysoFjpF8"}}

# ❌ 错误：对象（400）
{"fields": {"非美国地区学校": {"recordId": "recKHysoFjpF8"}}}

# ❌ 错误：字段ID键名 + 数组（400）
{"fields": {"fldXXX": ["recKHysoFjpF8"]}}
```

**字段键名**：必须用**字段名称**（中文），不能用字段 ID（`fldXXX`）。POST 时 `fieldKey="name"` 是默认值，可省略。

### ⚠️ POST 创建带 OneWayLink 字段时**不能**包含 fieldKey 参数（2026-08-21 实测教训）

**根因**：当请求体中包含 OneWayLink 字段且同时传递 `fieldKey` 参数时，API 会返回 `api_params_instance_fields_error`（HTTP 500），即使空记录也报错。这个错误信息完全没有提示是 `fieldKey` 导致的。

**正确格式**：创建带 OneWayLink 字段的记录时，**不要**在请求体中包含 `fieldKey` 参数：

```python
# ✅ 正确：不带 fieldKey
body = {"records": [{"fields": {"导师": "张三", "非美国地区学校": ["recXXX"]}}]}
result = vika("POST", "/records", body)

# ❌ 错误：带 fieldKey 会导致 500 错误
body = {"records": [{"fields": {"导师": "张三", "非美国地区学校": ["recXXX"]}}], "fieldKey": "name"}
result = vika("POST", "/records", body)  # HTTP 500 api_params_instance_fields_error
```

**注意**：这个限制**仅影响 POST 创建**。PATCH 更新时可以正常使用 `fieldKey="name"`。

**POST 创建时能否同时写 OneWayLink？** 是的，但必须不带 `fieldKey` 参数（如上所示）。

---


## 4. Update Records

### 4.1 Text / SingleSelect / Checkbox Fields

```python
updates = [
    {"recordId": "recXXX", "fields": {"Department": "心理学院(香港大学)", "状态": "待发邮件"}},
    {"recordId": "recYYY", "fields": {"备注": "教授；认知神经科学；在招博士"}},
]
vika("PATCH", "/records", {"records": updates, "fieldKey": "name"})
```

### 4.2 URL Fields (CRITICAL — fieldKey="name" 静默失败)

URL-type fields (导师主页, 博士申请信息, 其他导师信息) do NOT work with `fieldKey="name"`. API returns 200 but silently fails. **Must use field IDs with `fieldKey="id"`.**

```python
# 先获取 field IDs
fields = vika("GET", "/fields")
field_map = {f["name"]: f["id"] for f in fields["data"]["fields"]}

# 用 field ID 做 key，不带 fieldKey
updates = [
    {"recordId": "recXXX", "fields": {
        field_map["导师主页"]: "https://www.university.edu/faculty/prof-name",
        field_map["博士申请信息"]: "https://gradschool.university.edu/phd"
    }}
]
# PATCH with fieldKey="id" (CRITICAL: must include fieldKey="id")
req = Request(
    f"{BASE}/datasheets/{DATASHEET}/records",
    data=json.dumps({"records": updates, "fieldKey": "id"}).encode(),
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
    method='PATCH'
)
urlopen(req)
```

**Note**: This ONLY affects PATCH on URL-type fields. Text/SingleSelect/Checkbox fields work fine with `fieldKey="name"`. Using field IDs without `fieldKey="id"` returns 400 error.

### 4.3 Bulk Department Translation

```python
records = vika("GET", "/records?maxRecords=200&pageSize=200")["data"]["records"]

dept_map = {
    "Department of Psychology": "心理学院",
    "CUHK Business School": "香港中文大学商学院",
}

updates = []
for r in records:
    dept = r["fields"].get("Department", "")
    if dept in dept_map:
        updates.append({"recordId": r["recordId"], "fields": {"Department": dept_map[dept]}})

for i in range(0, len(updates), 10):
    vika("PATCH", "/records", {"records": updates[i:i+10], "fieldKey": "name"})
    time.sleep(0.3)
```

---


## 5. Delete Records

### 5.1 Delete by ID

```python
# vika() 函数自动把 list 转成 ?recordIds=recXXX,recYYY query parameter
vika("DELETE", "/records", ["recXXX", "recYYY"])
# or
vika("DELETE", "/records", {"records": ["recXXX", "recYYY"]})
```

### 5.2 Deduplicate (Keep Most Complete)

```python
from collections import defaultdict

records = vika("GET", "/records?maxRecords=200&pageSize=200")["data"]["records"]

name_map = defaultdict(list)
for r in records:
    name = r["fields"].get("导师", "").strip()
    if name:
        name_map[name].append(r)

to_delete = []
for name, recs in name_map.items():
    if len(recs) > 1:
        recs.sort(key=lambda r: sum(1 for v in r["fields"].values() if v), reverse=True)
        to_delete.extend(r["recordId"] for r in recs[1:])

if to_delete:
    vika("DELETE", "/records", to_delete)
    print(f"Deleted {len(to_delete)} duplicate records")
```

---

---

> 📎 自 SKILL.md 迁入（2026-10-07）。

## Vika 集成

**零依赖。** 所有操作使用 Python 3 标准库（`urllib` + `json`）——无需 `vika-cli`、npm 或第三方 SDK。仅需 API token 和任意 Python 3 安装。导入 Excel 时额外需要 `openpyxl`。

### 设置

1. 从 URL 解析：`datasheetId`（`dstXXX`）、`viewId`（`viwXXX`）
2. **Token 安全**：引导用户设置环境变量（不要在聊天中明文传递）：
   ```bash
   echo 'export VIKA_TOKEN=你的token' >> ~/.zshrc && source ~/.zshrc
   ```
3. Base URL: `https://api.vika.cn/fusion/v1`

> ⚠️ **CRITICAL — 绝不硬编码 token（2026-08-13 复盘）**：每个 Python 脚本里必须用 `os.environ.get("VIKA_TOKEN")` 读取，先 `source ~/.zshrc` 再运行。**绝对不要在脚本里写死 token 字符串**——之前因硬编码了错误的 token 值（只凭 `echo ${VIKA_TOKEN:0:8}` 看到前 8 位就脑补了后面 15 位），导致所有 API 请求返回 401，误判为"权限问题"浪费了多轮排查。诊断 token 是否失效的方法：调用 `GET /spaces`——能返回空间列表说明 token 有效（是表权限问题），返回 401 说明 token 本身失效或写错了。

### 操作前必做：过滤选导意向非空行

**每次执行增删改操作前，必须先获取所有记录并排除 `选导意向（点击选择）` 非空的行：**

```python
# 获取所有记录
result = vika("GET", "/records?maxRecords=200&fieldKey=name")
all_records = result["data"]["records"]

# 仅保留选导意向为空的行（这些是待编辑的行）
editable = [r for r in all_records if not r["fields"].get("选导意向（点击选择）")]

# 选导意向非空的行（这些是受保护的行，只能读取）
locked = [r for r in all_records if r["fields"].get("选导意向（点击选择）")]

# 所有增删改操作只针对 editable 列表中的 recordId
```

### 能力（记录级 CRUD）

| 操作 | 端点 | 备注 |
|------|------|------|
| 列出字段 | `GET /datasheets/{id}/fields` | 发现字段名和类型 |
| 列出记录 | `GET /datasheets/{id}/records?viewId=...&maxRecords=...` | 支持 filterByFormula、sort、分页 |
| 创建记录 | `POST /datasheets/{id}/records` | 每批最多 10 条。**body 必须是 `{'records': [{'fields': {...}}, ...], 'fieldKey': 'name'}`**——每条记录要包一层 `fields` 键；直接传裸字段映射会返回 HTTP 500 `api_params_instance_fields_error`（2026-09-14 实测踩坑） |
| 更新记录 | `PATCH /datasheets/{id}/records` | 发送 `{"records": [{"recordId":"xxx","fields":{...}}], "fieldKey": "name"}` |
| 删除记录 | `DELETE /datasheets/{id}/records?recordIds=recXXX` | recordIds 在 query parameter 中，非 request body |

### 关键限制

- **DELETE 请求格式**：recordIds 必须在 URL query parameter 中（`?recordIds=recXXX,recYYY`），不能在 request body 中。Helper 函数已自动处理此转换。
- MagicLookUp / OneWayLink 字段不可通过 API 写入。
- 每批最多 10 条记录，批次间加 0.3-0.5 秒延迟。

详细的 API 代码模板和操作指南见 `references/vika-guide.md`。

### ⚠️ 写入前必须重新 GET 当前记录（2026-09-15 实测教训，强制执行）

**同一张表可能在两轮之间被别人改过。** 本次实例：第一轮 GET 快照为 **68 条**记录、含「Greg Aldrich（Kansas State）」；几个小时后第二轮 GET 只剩 **65 条**——该记录已被删除，替换为「Julia Guazzelli Pezzali / Chad Paulk」两条，且申请页已改成正确的 Grain Science 链接。用户随后提出的"待修问题"里，K-State 那一项其实**已经不存在了**。

**若直接拿旧快照去 PATCH，会写到已不存在的 recordId，或把别人刚改好的值覆盖回去。**

**执行清单**：
1. **每次 PATCH / POST / DELETE 之前，重新 GET 一次全表**，不复用上一轮落盘的 `records.json`。
2. **前置断言**：用 `recordId` 存在性 + 待改字段的**当前值**做校验（如 `assert cur[rid][字段].startswith(旧首句)`），不匹配立即中止，不要"尽力而为"地写。
3. **先备份**：改前把原值 dump 到 `backup_before.json`，便于回滚。
4. **写完回读**：再 GET 一遍，逐字段比对确认。
5. **先核对再动手**：用户报的"待修项"可能已经被修掉了，逐条核实现状，避免改坏或重复报告。
6. **两类字段分两次请求**：URL 字段（导师主页 / 博士申请信息 / 其他导师信息）必须用**字段 ID + `fieldKey="id"`**；文本字段用**字段名 + `fieldKey="name"`**。两者不可混在同一请求里。

### 自然语言删除流程

当用户说"删除导师XXX"或"删除这条记录"时，按以下步骤操作：

1. **解析请求**：理解要删除什么（按导师名、按学校、按备注内容等）
2. **查找记录**：用 GET + filterByFormula 找到匹配的记录
   ```python
   # 按导师名查找
   filter_expr = urllib.parse.quote('{导师}="张三"')
   result = vika("GET", f"/records?filterByFormula={filter_expr}&maxRecords=200")
   records = result["data"]["records"]
   ```
3. **提取 recordIds**：从响应中提取 `recordId` 字段
4. **确认删除**：向用户展示找到的记录，确认是否删除
5. **执行删除**：使用正确格式调用 DELETE
   ```python
   # ✅ 正确格式
   vika("DELETE", "/records", {"records": [r["recordId"] for r in records]})
   ```
6. **验证结果**：删除后再次 GET 确认记录已移除

⚠️ **DELETE 格式陷阱**：必须发送 `{"records": ["recXXX"]}`，不能发送纯数组 `["recXXX"]`。

#### 🔴 DELETE 单次上限 10 条（2026-09-21 实测）

`DELETE /datasheets/{ds}/records?recordIds=a,b,c,...` **单次最多 10 条**，超过直接报错（**不是**静默失败）：

```
Can't update/delete/create more than $10 records in one single request
```

- 实测 **8 条/批最稳**；批间 `time.sleep(1)`。
- 注意与 POST 的坑**性质不同**：DELETE 是**显式报错**（好排查），而 POST 超 10 条是 **HTTP 201 + success:true 但 `data.records` 返回空数组**（静默失败，回读才发现）。两个都要防。
- **PATCH 单次同样上限 10 条，且是显式报错**（2026-10-16 实测：13 条一次提交报同一条 `Can't update/delete/create more than $10 records`，拆成 7+6 两批即成功）。所以批量改字段时**先按 ≤10 分批**，不要等到报错再返工；同理，批量「补学校关联」这类跨校更新也要分批。
- 删完必须 `GET` 回读，逐个确认 target recordId 已消失，并打印实际删除条数。

#### 🔴 删行前必须 dump 整行 `fields`，不能只看关键字段（2026-09-21 踩坑）

初筛「空行」时若只检查关键字段（导师/学校/备注等），会把**只保留了非关键字段的行**误判为垃圾行。实测：两条记录 8 个关键字段全空，但其中一条有 `确认套磁=True`、`状态=被拒绝`、`等邮件几天=12`、`选导时间`、`From` —— 是一条**真实处理过的套磁记录**（导师名字段丢失的孤儿行），删掉就丢了历史状态。

**规则**：
1. 判定「空行/垃圾行」时，必须 `print(rec["fields"])` 看**整行所有键**，不能只看白名单字段。
2. 只要该行含「选导时间 / 确认套磁 / 状态 / 套磁备注 / 你的反馈 / From / 状态变更日期」中任一字段，就**不是**可删的垃圾行，应报告给用户人工处置。

---
