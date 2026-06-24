# PhD Supervisor Selector · 博士选导助手

让 AI 自动帮你搜索、筛选、验证博士导师，生成带个人主页链接和匹配分析的选导表格。

---

## 一句话上手

复制下面这句话，发给 Codex / ChatGPT / Claude：

> 帮我安装这个 skill，https://github.com/PNmiracle/phd-supervisor-selector，并教我怎么使用

AI 会自己读 `SKILL.md`，装好之后你直接说：

> 我的方向是城市规划（交通、智慧城市），不喜欢设计建模，偏好分析类。
> 目标学校：港科广、西交利物浦、宁诺。

然后把你的导师表模板拖进去（如果有的话），AI 就会自动干活了。

---

## 怎么用（30 秒版）

| 步骤 | 你说的话 |
|------|----------|
| ① 安装 | `帮我安装这个skill，https://github.com/PNmiracle/phd-supervisor-selector` |
| ② 说明需求 | `我的方向是___，不喜欢___，目标学校___` |
| ③ 拖入模板 | 把你的选导 Excel 拖进对话框（可选） |
| ④ 追加 | `继续找`（AI 会自动深度挖掘） |

---

## 功能

- 🔍 自动搜索学校官网师资页、博士项目页
- 🧠 判断导师是否具备带博资格（职称/地区规则，自动排除 Adjunct/Clinical/Teaching 等）
- ✅ 浏览器验证个人主页能否打开，点击 Research Interest 获取隐藏方向
- 📊 生成结构化表格（导师/学校/QS排名/主页/备注/选导建议）
- ⚠️ 自动筛查教学岗、兼职、方向不匹配的导师 → 放入排除表
- 🇺🇸 支持美国 + 非美国学校混合列表，自动判断是否加 US News 列

---

## 输出示例

| 导师 | 学校 | QS | 备注 | 选导反馈 |
|------|------|-----|------|----------|
| 乐阳 | 港科广 | 47 | 教授；城市大数据、GeoAI与社会可持续性 | 优先套磁 |
| Hyung-Chul Chung | 西交利物浦 | 176 | 副教授；城市规划与交通融合、AI与机器学习 | 优先套磁 |
| Jing Bie | 宁诺 | 108 | 助理教授；交通工程 | 优先套磁 |

---

## 目录结构

```
SKILL.md                          ← AI 入口 & 规则
references/
  selection-rules.md               ← 导师筛选（职称/地区/匹配度）
  spreadsheet-rules.md             ← 表格格式 & 条件列逻辑
  search-techniques.md             ← 搜索技术（SPA破解/API/浏览器/子Agent）
README.md                          ← 本文件
```
