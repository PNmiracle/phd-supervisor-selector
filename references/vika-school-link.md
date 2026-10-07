<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载 -->
> **本文含**：Vika「学校关联字段」（OneWayLink）的完整操作手册——识别新/老学生、创建学校记录、四层搜索、搜不到就停、设置关联、验证，含可直接复用的代码。
> **什么时候读**：给导师记录设置学校关联字段时；需要判断学生是新学生还是老学生时；主表搜不到学校时。
> **什么时候不用读**：搜索/抓取阶段；只改备注、链接、职称等字段时；只需知道「不得对主表写操作」这类硬规则时（看 `rules-write.md` 第 15 节）。

---

# 学校关联字段操作手册（vika-school-link）

> 本文由 `critical-rules.md` 于 2026-10-07 拆出。**五条不可违反的硬门**已在 `rules-write.md` 第 15 节列明，本文只写「怎么做」。Vika 通用 API 细节见 `vika-guide.md`。

**每条新导师记录写入后，必须立即设置学校关联字段（OneWayLink）**，让 Location / QS排名 / 美国USNEWS排名 / 国内学校层次 通过 MagicLookUp 自动同步。

这是最容易遗漏但影响最大的步骤——学校关联字段决定整行的 Location、QS、USNEWS、国内学校层次，不填等于记录残缺。

## 第一步：识别新学生 / 老学生（强制执行，不可跳过）

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

## 第二步-A：新学生模式（统一主表 `dstMNzQU9Aa58DpgW3`）

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

> ⚠️ 上面这段「创建学校记录」只在**主表里确实没有该校、且用户已确认补录之后**才执行。默认路径永远是「先搜，搜不到就停」。

---

## 第二步-B：老学生模式（双主表）

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

## 第三步：在主表中查找学校（⚠️ 多层模糊搜索 → 搜不到就停，禁止自建）

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

## 第四步：搜不到学校时 — 停下来，不要自建 🚫

第三步搜不到学校时，**绝对不要在主表 POST 新建**。改为：

1. 把导师记录先写入选导表（不含学校关联）
2. 告诉用户："XX 学校不在主表中，请手动添加"
3. 等用户补完学校后，再设置 OneWayLink

**禁止事项（新增）**：
- 🚫 **绝对禁止**对主表执行 POST/PATCH/DELETE 操作（即使 API token 有权限）
- 🚫 **绝对禁止**用 `vika('POST', f'/datasheets/{main_table_id}/...')` 在任何路径下创建学校
- 🚫 **绝对禁止**在搜不到学校时自己去建——正确做法是停下来告诉用户

## 第五步：设置导师记录的 OneWayLink

```python
data = {'records': [{
    'recordId': supervisor_rid,
    'fields': {link_field_name: [school_rid]}
}], 'fieldKey': 'name'}
vika('PATCH', f'/datasheets/{datasheet_id}/records', data)
```

## 第六步：验证

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
