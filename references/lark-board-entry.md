<!-- 头部由 2026-10-07 瘦身改造统一添加：三行说明用于阻止无谓加载，正文未改动 -->
> **本文含**：飞书「选导任务管理看板」记录入口与三类任务判别（①搜索+写表 ②审核已有表 ③分析类），以及结论回写看板的要求
> **什么时候读**：用户直接甩一条飞书 record 链接说「做这个」时；需要判断该条记录属于哪类任务时
> **什么时候不用读**：任务由用户直接口述、不经看板下发时；已经在按看板提示词执行中时

---

## 任务入口：飞书「选导任务管理看板」（2026-09-14 沉淀）（自 SKILL.md 迁入 2026-10-07）


用户直接甩一条 `https://my.feishu.cn/record/XXXX` 链接说「做这个」时，该记录属于飞书选导任务看板，**不一定**是"搜索导师"任务——先读「提示词」字段判断任务类型，常见三类：① 搜索+写表；② 审核已有表；③ **分析类**（如"从 CV + 最终名单反推学生偏好的方向"）。分析类任务同样要把结论回写到看板。

**标准流程（lark-cli）**：

```bash
# 1. 解析记录坐标
lark-cli base +url-resolve --url 'https://my.feishu.cn/record/XXXX' --as user
# → base_token / table_id / record_id

# 2. 读记录（看「提示词」「检查重点」「附件」）
lark-cli base +record-get --base-token <bt> --table-id <tbl> --record-id <rec> --as user

# 3. 下载附件（CV / 截图 / RP）——⚠️ 必须用当前工作目录下的相对路径
lark-cli base +record-download-attachment --base-token <bt> --table-id <tbl> \
  --record-id <rec> --output ./<目录> --as user

# 4. 分析完成后回写结论到「AI 反馈」字段（该字段= agent 汇报位，看板其余记录皆如此）
lark-cli base +record-batch-update --base-token <bt> --table-id <tbl> \
  --json @./<目录>/payload.json --as user
# payload: {"update_records": {"<record_id>": {"AI 反馈": "……"}}}
```

**lark-cli 路径陷阱（2026-09-14 实测）**：`--output` 与 `--json @file` 都**只接受当前工作目录内的相对路径**（`./xxx`）。传 `/tmp/xxx` 或绝对路径会报 `unsafe output path` / `invalid JSON file path`。`/tmp` 也被拒。做法：先把中间文件写到工作目录下的子目录，用完再删。

**⚠️ 前置门槛：读看板记录必须先用「用户身份」授权（2026-10-06 实测，最容易卡住第一步）**

- `+url-resolve` 用**应用（bot）身份**就能成功（返回 base_token / table_id / record_id）；
- 但 `+record-get` 用 bot 会报 `app_scope_not_applied`（缺 `base:record:read`）——**bot 读不了用户的多维表格**，此处**不要**去开发者后台给 bot 加 scope，直接走用户授权；
- 正确做法：`lark-cli auth login --domain base,drive --no-wait --json` → 用 `lark-cli auth qrcode <verification_url> --output ./xxx.png` 生码 → **本轮把 URL（先）+ 二维码图片（后）发给用户，然后结束本轮** → 用户回复"已授权"后由 agent 自己执行 `lark-cli auth login --device-code <device_code>`；
- `--device-code` 会**阻塞轮询**，前台调用常被工具超时打断（实测 exit 137、无输出）→ **放后台任务跑**，再 `auth status --json` 复核 `identities.user.status == "ready"`；
- device code **有效 10 分钟**，过期就重新签发，不要复用旧链接；范围给 `base`（读写记录）+ `drive`（下载附件）即可，不必 `--domain all`。

**⚠️ Fusion API 单次批量写入上限（2026-09-20 实测，必须遵守）**：`POST /datasheets/{ds}/records` 一次提交**超过 10 条会静默失败**——HTTP 仍返回 **201**、`success: true`，但 `data.records` 是**空数组**。若脚本用 `r.get("data",{}).get("records",[])` 取 ID，会拿到空列表却不报错，**记录实际没写进去**（本次 21 条批量提交即中招，回读才发现全表查无此人）。

对策：
1. **每批最多 5 条**提交，批间 `time.sleep(1)`；
2. 逐批收集返回的 `recordId`，**任一批返回 0 个 ID 就立即停并报错**，不要继续往下跑；
3. **写完必须回读校验**：重新 `GET` 全表，按「导师」字段精确比对名字，确认条数、学校关联、US/QS 排名都对；
4. 批量更新（PATCH）同理建议分批；测试用临时记录（如 `__测试_请忽略__`）测完要 `DELETE /datasheets/{ds}/records?recordIds=<id>` 清掉。

**看板字段语义**：`AI 反馈`=agent 汇报（回写位）；`检查反馈`=审核官报错；`置信度`=通过/不通过；`处理节点`/`开始时间`/`锁定时间`=调度系统占用标记。同名学生可能有多条记录（带「-周X需交付」后缀的是排期副本），看清是哪一个。

---
