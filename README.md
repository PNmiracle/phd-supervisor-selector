# PhD Supervisor Selector · 博士选导助手

让 AI 自动帮你搜索、筛选、验证博士导师，支持 **Vika 表直接操作** 和 **Excel 表格** 两种模式。

---

## 快速开始（选一条路径）

### 🅰️ 路径 A：Vika 模式（推荐 — 零依赖）

> 你给 Vika 链接 + API Token，AI 直接在维格表里增删改查，不碰 Excel。

**前提：** 你有一个 Vika 共享表 + 表的 API Token。

| 步骤 | 你说的 |
|------|--------|
| ① 安装 Skill | `帮我安装这个skill，https://github.com/PNmiracle/phd-supervisor-selector` |
| ② 给 Vika 链接 | `打开这个表 https://vika.cn/share/shrXXX/dstXXX/viwXXX` |
| ③ 给 API Token | `我的 token 是 uskXXX` |
| ④ 直接操作 | `列出所有导师` / `新增一条XXX` / `把Department翻译成中文` / `把这份Excel导入表` / `检查重复` |

**不需要安装任何东西。** 全程用 Python 标准库调用 Vika REST API，零依赖。

> 🔐 **Token 安全注意事项：**

不要把 API Token 贴到聊天框（会被记录到对话历史）。在终端里跑下面**这一行**就行，一劳永逸：

```bash
echo 'export VIKA_TOKEN=你的token' >> ~/.zshrc && source ~/.zshrc
```

> 就是把你的 token 存到 `~/.zshrc`（Mac 每次开机自动加载的环境变量文件），之后所有 Chat 都自动能用。不需要装任何东西，不需要每开一个 Chat 就重复设。

### 🅱️ 路径 B：Excel 模式

> 拖入 Excel，AI 搜索学校官网生成导师表。

| 步骤 | 你说的 |
|------|--------|
| ① 安装 Skill | 同上 |
| ② 说明需求 | `我的方向是城市规划（交通、智慧城市），不喜欢设计建模，偏好分析。目标学校：港科广、西浦、宁诺。` |
| ③ 拖入模板 | 把你的选导 Excel 拖进对话框（可选，没有也行） |
| ④ 追加 | `继续找`（AI 会自动深度挖掘） |

---

## 使用阶段（Phase）

```
Phase 1 ── 新建 / 导入
  │   Vika: 给链接 + Token，AI 列出表结构，自然语言 CRUD
  │   Excel: 说方向+学校，AI 建表并搜索填充
  │
Phase 2 ── 深度搜索
  │   按学校搜索官网师资页、博士项目页
  │   自动并行子 Agent 加速（多学校同时搜）
  │   浏览器验证个人主页是否可访问
  │
Phase 3 ── 清洗 & 补全
  │   Department 翻译成中文
  │   补全缺失的 博士申请信息 / 其他导师信息 链接
  │   去重、标记空行
  │
Phase 4 ── 持续维护
  │   自然语言操作："把XXX的状态改成已套磁"
  │   Excel ↔ Vika 双向导入导出
  │   新增导师、删除放弃的
```

---

## 能力一览

| 能力 | Vika 模式 | Excel 模式 |
|------|-----------|------------|
| 自然语言 CRUD | ✅ "列出所有记录" / "新增一条" | ❌ |
| 批量导入 | ✅ Excel → Vika | N/A |
| 搜索学校官网 | ✅ | ✅ |
| 并行子 Agent | ✅ 多学校同时搜 | ✅ |
| 浏览器验证 | ✅ 打开链接确认 | ✅ |
| Department 翻译 | ✅ 英文 → 中文 | ✅ |
| 去重 & 清洗 | ✅ | ✅ |
| 反爬处理 | ✅ 浏览器→换域名→探 API→⚠️标记 | ✅ |
| 零依赖 | ✅ Python stdlib | 需 openpyxl |

---

## 输出示例

| 导师 | 学校 | QS | 备注 |
|------|------|-----|------|
| 乐阳 | 港科广 | 47 | 教授；城市大数据、GeoAI与社会可持续性；在招博士 |
| David Moreau | 奥克兰大学 | 65 | 副教授；脑动力学、行为神经变异性；心理学院(奥克兰大学) |
| Tianyi LI | 香港大学 | 11 | 助理教授；决策、健康营销、社会认知神经科学；超高产 |

---

## 备注规范

> ⚠️ **禁止使用主观评价**：`高度匹配`、`很匹配`、`完美匹配` 这类词全部禁用。只写事实，不做判断。

| 类型 | 示例 |
|------|------|
| 正常 | `教授；城市大数据、GeoAI；在招博士。` |
| 反爬无法验证 | `⚠️Leeds页面JS动态加载，curl+浏览器均无法自动验证。需手动打开确认。` |
| 仅有个人页 | `仅有个人主页，无官方院系页面。` |

---

## 多人协作 · 共同维护 Skill

如果你和另一位老师一起使用这个 Skill，通过在 GitHub 共享同一仓库来保持 Skill 同步：

### 协作方（第二位老师）设置

**前提：** 仓库拥有者已把你添加为 GitHub 仓库 `PNmiracle/phd-supervisor-selector` 的 Collaborator（Settings → Collaborators）。

```bash
# 如果之前没有安装过这个 skill
git clone git@github.com:PNmiracle/phd-supervisor-selector.git ~/.workbuddy/skills/phd-supervisor-selector/

# 如果之前通过 WorkBuddy 安装过，只需切换到 git 版本
cd ~/.workbuddy/skills/phd-supervisor-selector
git init
git remote add origin git@github.com:PNmiracle/phd-supervisor-selector.git
git fetch origin
git reset --hard origin/main
```

### 日常同步工作流

每次你或另一位老师说 **"结束学生"** 时，AI 会自动：
1. 从这次搜索中提取可沉淀的知识
2. 更新 `SKILL.md` 和 `references/*.md`
3. **先 `git pull --rebase` 拉取对方更新**
4. **再 `git push` 推送你的更新**
5. 如有冲突，AI 会智能合并后重试

### 手动同步（如果需要）

```bash
cd ~/.workbuddy/skills/phd-supervisor-selector
git pull --rebase origin main
```

### 协作规则

- **"结束学生"** 之前，AI 会自动 pull 最新版本，避免覆盖对方的改动
- 如果 git pull 发现冲突，AI 会优先保留双方的增量改动，不做破坏性覆盖
- 推荐每次搜索前先说一次 `git pull` 风格的同步提示给 AI

---

## 目录结构

```
SKILL.md                          ← AI 入口 & 全部规则
references/
  selection-rules.md               ← 导师筛选（职称/地区/匹配度）
  spreadsheet-rules.md             ← 表格格式 & 条件列逻辑
  search-techniques.md             ← 搜索技术（SPA/API/浏览器/子Agent）
  vika-operations-guide.md         ← Vika 表完整操作指南（增删改查/导入/去重/翻译）
  vika-api-patterns.md             ← Vika API 可复用代码模板
README.md                          ← 本文件
```
