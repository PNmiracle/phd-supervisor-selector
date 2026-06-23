# PhD Supervisor Selector

Codex skill for researching and screening PhD supervisors, especially when a student needs a source-backed supervisor spreadsheet.

## What It Does

- Searches official university profiles, staff lists, PhD pages, and supervisor lists.
- Judges whether a person is likely eligible to supervise PhD students.
- Separates strong candidates from uncertain, excluded, or weak-fit candidates.
- Fills supervisor spreadsheets with verified links and concise Chinese remarks.

## Key Rules

- Use official PhD supervisor lists first when they exist.
- Verify that each supervisor homepage visibly matches the person.
- Do not select risky titles such as adjunct, visiting, emeritus, teaching-only, clinical, practice-only, or research-only staff without strong supervision evidence.
- Treat `Lecturer` and `Senior Lecturer` differently by region, especially for the UK, Ireland, Australia, and New Zealand.
- Log searched schools with no suitable supervisor instead of inventing candidates.

## Files

- `SKILL.md`: main skill entry and workflow.
- `references/selection-rules.md`: supervision eligibility, title, region, and fit judgement rules.
- `references/spreadsheet-rules.md`: spreadsheet columns, link rules, remarks style, and quality checks.
- `agents/openai.yaml`: display metadata.
