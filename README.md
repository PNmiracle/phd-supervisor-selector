# PhD Supervisor Selector — 博士选导助手

一个 Codex / ChatGPT / Claude 等 AI coding agent 可用的 skill（技能包），自动帮你搜索、筛选、验证海外/中外合办院校的博士导师，生成结构化的导师遴选表格。

## 小白使用指南（一句话上手）

把你的导师表 + GitHub 链接交给 AI 助手：
```
帮我用这个 skill 找导师：https://github.com/PNmiracle/phd-supervisor-selector
我的方向是城市规划（交通、智慧城市），不喜欢设计建模，偏好分析类
目标学校：西交利物浦、港科广、宁诺、港中深
```

AI 助手会自动执行：搜索学校官网 → 筛选合适导师 → 验证个人主页 → 填写表格。

## 在 Codex 中使用
Codex 原生支持 skill 安装：
- `/skill-installer` → 选择 "从 GitHub 安装" → 输入 `PNmiracle/phd-supervisor-selector`
- 或在对话中直接 `@PNmiracle/phd-supervisor-selector`

## 在 ChatGPT / Claude / 其他 Agent 中使用
直接复制 GitHub 链接并说明需求：
```
https://github.com/PNmiracle/phd-supervisor-selector

按 SKILL.md 的规则，帮我找以下学校的博导：
[你的方向、偏好、学校列表]
```

AI 助手会读取仓库里的 `SKILL.md`，按照其中的规则执行搜索和填表。

## 功能

- 🔍 自动搜索学校官网的师资页面、博士项目页面
- 🧠 判断导师是否具备带博资格（职称、地区规则）
- ✅ 浏览器验证每位导师的个人主页能否打开
- 📊 生成结构化 Excel 表格（导师/学校/QS排名/主页/备注/选导建议）
- ⚠️ 自动筛查教学岗、兼职、方向不匹配的导师
- 🔄 支持多轮"继续找"深度挖掘

## 表格输出示例

| 导师 | 学校 | QS | 导师主页 | 备注 | 选导反馈 |
|------|------|-----|----------|------|----------|
| 乐阳 | 港科广 | 47 | 🔗个人页 | 教授；城市大数据、GeoAI与社会可持续性 | 优先套磁 |
| Hyung-Chul Chung | 西交利物浦 | 176 | 🔗个人页 | 副教授；城市规划与交通融合、AI与机器学习 | 优先套磁 |

## 目录结构

```
SKILL.md                    ← AI 助手的主入口和规则
references/
  selection-rules.md        ← 导师筛选规则（职称、地区、匹配度）
  spreadsheet-rules.md      ← 表格格式、备注规范、质检规则
  search-techniques.md      ← 搜索技术（SPA破解、API发现、URL推断、浏览器自动化、并行子Agent）
README.md                   ← 本文件
```

## 更新日志

- 2025-06-24: 新增 `references/search-techniques.md`，整合 SPA/API 发现、URL 模式推断、并行子 Agent 策略、浏览器自动化等技术。
