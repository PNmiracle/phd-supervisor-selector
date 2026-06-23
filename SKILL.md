---
name: phd-supervisor-selector
description: Research and spreadsheet workflow for PhD supervisor selection. Use when the user asks Codex to search, screen, verify, expand, clean, or fill a supervisor list table for doctoral applications, including tasks mentioning 博士选导, 导师表, Supervisor List, 博导, PhD supervisor, supervisor homepage links, PhD application links, other staff links, remarks/备注, school scope, QS ranking, exclusions, or candidate fit.
---

# PhD Supervisor Selector

## Overview

Build source-backed supervisor lists for doctoral applicants. Search current university pages, judge whether a person is likely to supervise PhD students, fill the spreadsheet columns, and keep unusable or risky candidates out of the main table.

## Core Workflow

1. Parse the student's profile, preferred research directions, hard exclusions, target regions/schools, ranking constraints, and any existing workbook/screenshot columns.
2. Search official university sources first: supervisor profile, department staff list, PhD/research degree page, and supervisor list if available.
3. Verify each supervisor homepage by content: the page must open and visibly match the person's name, role, department, or team identity. Do not accept a plain 200 status, dynamic shell, 404 page, or generic search page.
4. Judge supervision suitability using `references/selection-rules.md`.
5. Fill the spreadsheet using `references/spreadsheet-rules.md`.
6. When a school from the user's list has been searched but no suitable supervisor is found, record the school-level reason in `排除或待确认` / screening sheet.
7. Put uncertain, excluded, weak-fit, stale, or unverified people in a separate `排除或待确认` / screening sheet, not the main table.
8. Before delivery, run compact checks: no empty key links, no broken obvious links, no banned note phrases, no formula errors, and render a preview of every sheet.

## Required Output Columns

Use these columns unless the user explicitly gives a different schema:

`导师`, `Location`, `学校名字`, `QS排名`, `美国USNEWS排名`, `Department`, `导师主页`, `博士申请信息`, `其他导师信息`, `备注`

`其他导师信息` should normally be the same department/school staff list used to find comparable supervisors.

## Search Standards

- Browse current web pages for rankings, application links, staff lists, and profile pages.
- Prefer official university pages. Use Google/search results only to discover a correct profile URL, then verify the official page.
- If the PhD program publishes a specific supervisor list, treat that list as binding eligibility evidence and only select names from it.
- If a common profile URL returns 404 or opens a non-matching page, search the supervisor name plus school again with Google/Bing or another web search, then verify the new official page. Do not keep guessed paths.
- If a site blocks scraping or renders dynamically, use the browser when available and confirm visible page content manually.
- If PhD information is split across several pages, use the most relevant official research degree/program page and explain the merge briefly in the screening notes.
- If eligibility is scattered across a PDF/list and separate staff profiles, use the PDF/list for `博士申请信息` or evidence and the individual profile for `导师主页`.

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
- `排除或待确认`: record why schools or people were not included.
- Optional school screening sheet when the user asks to scan a region or all schools.

Highlight each newly added search round with a distinct pale color and describe the color meaning in the legend.

## References

- Read `references/selection-rules.md` before deciding whether a candidate can enter the main table.
- Read `references/spreadsheet-rules.md` before creating, editing, or validating a supervisor spreadsheet.
