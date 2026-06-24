---
name: phd-supervisor-selector
description: Research and spreadsheet workflow for PhD supervisor selection. Use when the user asks Codex to search, screen, verify, expand, clean, or fill a supervisor list table for doctoral applications, including tasks mentioning 博士选导, 导师表, Supervisor List, 博导, PhD supervisor, supervisor homepage links, PhD application links, other staff links, remarks/备注, school scope, QS ranking, exclusions, or candidate fit.
---

# PhD Supervisor Selector

## Overview

Build source-backed supervisor lists for doctoral applicants. Search current university pages, judge whether a person is likely to supervise PhD students, fill the spreadsheet columns, and keep unusable or risky candidates out of the main table.

## Core Workflow

1. Parse the student's profile, preferred research directions, hard exclusions, target regions/schools, ranking constraints, and any existing workbook/screenshot columns.
2. **Detect the spreadsheet format** (see `references/spreadsheet-rules.md`): if the user provides a template, adopt its column structure. If not, use the default simplified format.
3. Search official university sources first: supervisor profile, department staff list, PhD/research degree page, and supervisor list if available.
4. **For SPA/dynamic sites**: probe the JavaScript bundle for API endpoints before giving up (see `references/search-techniques.md`). Fetch complete datasets in one API call when possible.
5. Verify each supervisor homepage by content: the page must open and visibly match the person's name, role, department, or team identity. Do not accept a plain 200 status, dynamic shell, 404 page, or generic search page.
6. **Use the in-app browser** for content verification when curl is insufficient — especially for SPA personal pages, hidden tab content (Research Interest, Publications), and visual confirmation.
7. Judge supervision suitability using `references/selection-rules.md`.
8. Fill the spreadsheet using `references/spreadsheet-rules.md`.
9. When a school from the user's list has been searched but no suitable supervisor is found, record the school-level reason in `排除或待确认` / screening sheet.
10. Put uncertain, excluded, weak-fit, stale, or unverified people in a separate `排除或待确认` / screening sheet, not the main table.
11. Before delivery, run compact checks: no empty key links, no broken obvious links, no banned note phrases, no formula errors, and render a preview of every sheet.

## Required Output Columns

Two output formats are supported; see `references/spreadsheet-rules.md` for the full decision logic.

### Simplified Format (default, no template provided)

`导师`, `Location`, `学校名字`, `QS排名`, `美国USNEWS排名`, `Department`, `导师主页`, `博士申请信息`, `其他导师信息`, `备注`

- `美国USNEWS排名`: **only include this column when US schools are present in the list.** When the entire list is non-US, omit it entirely.

### Template Format (user provides an `.xlsx` template)

Follow the template's exact column headers. The standard template uses:

`导师`, `Location`, `美国学校`, `非美国学校`, `QS排名`, `美国学校的Usnews排名`, `Department`, `导师主页`, `博士申请信息`, `其他导师信息`, `备注`, `选导反馈`, `学生反馈`

Key rules for template format:
- US schools → fill `美国学校` + `美国学校的Usnews排名`; leave `非美国学校` empty
- Non-US schools → fill `非美国学校` + `QS排名`; leave `美国学校` and `美国学校的Usnews排名` empty
- Both `美国学校` and `非美国学校` can have data in the same spreadsheet but never in the same row

## Search Standards

- Browse current web pages for rankings, application links, staff lists, and profile pages.
- Prefer official university pages. Use Google/search results only to discover a correct profile URL, then verify the official page.
- If the PhD program publishes a specific supervisor list, treat that list as binding eligibility evidence and only select names from it.
- If a common profile URL returns 404 or opens a non-matching page, search the supervisor name plus school again with Google/Bing or another web search, then verify the new official page. Do not keep guessed paths.
- **For SPA or JavaScript-rendered sites**: do not accept a 200-status empty shell. Read `references/search-techniques.md` for API discovery, URL pattern inference, and direct-path vs hash-route strategies.
- **For batch discovery**: use API endpoints to fetch all faculty at once (size=100000), then filter locally. This avoids pagination and page-by-page scraping.
- If a site blocks scraping or renders dynamically, use the browser when available and confirm visible page content manually, including clicking tabs like "Research Interest" to reveal hidden content.
- If PhD information is split across several pages, use the most relevant official research degree/program page and explain the merge briefly in the screening notes.
- If eligibility is scattered across a PDF/list and separate staff profiles, use the PDF/list for `博士申请信息` or evidence and the individual profile for `导师主页`.
- **For PhD program pages on unreachable subdomains**: check the graduate school domain (fytgs.{university}.edu.cn or gs.{university}.edu.cn) — these are often on the main university infrastructure and more accessible.
- **Use parallel sub-agents** (`spawn_agent` with explorer type) for independent checks of different schools or domains. Give each a clear, self-contained task; continue your own verification work while they run.

## Deep Discovery Pipeline

Do not stop at the first batch of results. Use this funnel to maximize coverage:

1. **Full sweep** — fetch all faculty data via API, filter by target department
2. **Filter** — check degree, major, and research keywords of remaining faculty for relevance
3. **Prioritize** — rank by match to student directions; consider adjacent departments (e.g., Intelligent Transportation, Innovation/Policy for urban planning students)
4. **Verify** — open personal pages in browser, click Research Interest tabs for hidden content
5. **Expand** — re-check schools that previously showed 404/unreachable; subdomains may come back online

Also see `references/search-techniques.md` for the full pipeline with code patterns.

## Remarks Style

Default Chinese note format:

`职称；研究关键词；匹配/风险。`

Keep remarks short and specific. Do not use filler such as `主页写明`, `公开资料`, `方向集中在`, `方向一优先`, `方向二备选`, or similar ranking labels. If the user asks for Chinese-only notes, avoid English in the `备注` column.

When a user asks for a friendly evaluation phrase such as `很匹配，这个可以关注下～`, still source the first two parts from the supervisor homepage: `职称；研究方向；简短评价语。` Use the requested phrase for clear matches, but keep concise risk signals for teaching, adjunct, research-only, stale, 404, or supervision-uncertain profiles.

Examples:

- `副教授；博物馆研究、装饰艺术、珍奇柜；高度匹配。`
- `教授；文化遗产、建筑史、遗产保护；建筑遗产偏重。`
- `助理教授（教学）；策展与艺术史、中欧艺术交流；教学岗风险。`

## Workbook Shape

For new or rebuilt lists, include:

- Main sheet named after the student or requested list title.
- `说明与颜色图例`: explain row highlights, source rounds, and note/link rules.
- `排除或待确认`: record why schools or people were not included. Include ⚠️ notes for candidates found but unreachable, with URLs for user-side manual verification.
- Optional school screening sheet when the user asks to scan a region or all schools.

Highlight each newly added search round with a distinct pale color and describe the color meaning in the legend.

## Existing Workbook Handling

When the user drops a template `.xlsx`:

1. Read the template to detect its column structure. Do not overwrite column headers.
2. Fill data into the existing columns, matching by header name.
3. For mixed US/non-US lists, fill school names into the correct column (`美国学校` or `非美国学校`) based on the school's country.
4. Fill US News rankings only for US schools; leave the cell empty for non-US schools.
5. Append new rows for newly discovered supervisors; do not delete or rearrange existing rows.
6. Add new sheets (`说明与颜色图例`, `排除或待确认`) if the template does not already have them.

## References

- Read `references/selection-rules.md` before deciding whether a candidate can enter the main table.
- Read `references/spreadsheet-rules.md` before creating, editing, or validating a supervisor spreadsheet.
- Read `references/search-techniques.md` for SPA/API discovery, URL pattern inference, parallel sub-agent strategies, browser automation, and deep discovery pipelines.
