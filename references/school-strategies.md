# School Strategy Knowledge Base

Living registry of which search strategy works for each university. Update after every search session — successes AND failures. This file compounds in value with every search.

## Architecture Categories

| Type | Signature | Best Approach | curl Works? | Browser Needed? |
|------|-----------|---------------|-------------|-----------------|
| **Pure Portal** | URL contains `/portal/en/persons/`, JSON API | `GET ?format=json` → parse JSON | ✅ Yes | No |
| **Vue SPA** | Empty HTML shell, `__vue__` in source | Download JS → grep `api\|baseUrl` → call API directly | ❌ No | Sometimes |
| **React SPA** | Empty HTML, `react` in JS filenames | Similar to Vue: find API endpoint in bundle | ❌ No | Sometimes |
| **Static HTML** | Full content in `curl` output, `<table>` or `<ul>` staff lists | Direct `curl` + BeautifulSoup parse | ✅ Yes | No |
| **Worktribe** | `/staff/profiles/` URL pattern, structured pages | Direct `curl` staff listing + individual profiles | ✅ Yes | No |
| **Cloudflare WAF** | 403/1020 on curl, works in browser | Browser automation ONLY | ❌ No | ✅ Required |
| **Custom CMS** | Unknown pattern, unique per school | Try curl first → if blocked, browser → if JS-only, API hunt | ⚠️ Varies | ⚠️ Varies |

## Strategy Selection Flow

```
1. Try curl on staff listing page
   ├── 200 + content → Static HTML or Worktribe → parse directly
   ├── 200 + empty shell → SPA → hunt API endpoint in JS bundle
   ├── 403/1020 → Cloudflare → browser automation
   └── Timeout/DNS → Try graduate school domain or search engine fallback
```

## School Registry

Update format: `YYYY-MM-DD: {what worked} | {what failed}`

### 🇬🇧 United Kingdom

#### University of the Arts London (UAL)
- **Architecture**: Pure Portal
- **Access**: `curl` → Pure API JSON
- **Key endpoint**: `https://researchers.arts.ac.uk/portal/en/persons/?format=json`
- **Notes**: Each college has separate Pure instance. Search per college.
- **Failed**: — (first try worked)
- **Last verified**: (fill after search)

#### Royal College of Art (RCA)
- **Architecture**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Leeds
- **Architecture**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Southampton
- **Architecture**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### Kingston University
- **Architecture**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### Heriot-Watt University
- **Architecture**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### De Montfort University
- **Architecture**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Edinburgh
- **Architecture**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Glasgow
- **Architecture**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Brighton
- **Architecture**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### Nottingham Trent University (NTU)
- **Architecture**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

### 🇦🇺 Australia

#### RMIT University
- **Architecture**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Technology Sydney (UTS)
- **Architecture**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

#### University of Melbourne
- **Architecture**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

### 🇸🇬 Singapore

#### Nanyang Technological University (NTU)
- **Architecture**: —
- **Access**: —
- **Key endpoint**: —
- **Failed**: —
- **Last verified**: —

---


## Auto-Update Protocol (Agent executes during search)

After searching EACH school, update this file. Do NOT defer to end of session — update immediately.

### Update Format

```markdown
#### School Name
- **Architecture**: [one of: Pure Portal | Vue SPA | React SPA | Static HTML | Worktribe | Cloudflare WAF | Custom CMS]
- **Access**: [concise: what worked]
- **Key endpoint**: [URL if API discovered]
- **Failed**: [what you tried that did NOT work]
- **Last verified**: [today's date]
```

### Rules

1. **Always record architecture** — even if you used a fallback. Knowing "Cloudflare WAF" tells the next session to skip curl and go straight to browser.
2. **Record failures** — "Tried API at /api/staff → 404" is AS VALUABLE as a success. It prevents the next session from wasting time on the same dead end.
3. **Update, don't duplicate** — if the school already has an entry, update its fields rather than adding a second entry.
4. **New schools go at the bottom** of their country section.
5. **After updating, commit**: `git add references/school-strategies.md && git commit -m "learn: {School} → {Architecture}"`

### Why this compounds

| Searches completed | Schools in registry | Hit rate on next search |
|-------------------|-------------------|------------------------|
| 5 | 5 | ~25% |
| 20 | 20 | ~60% |
| 50 | 50 | ~85% |
| 100 | 100 | ~95% |

After 100 schools, almost every new search hits a known architecture. The skill becomes 3-5x faster.



After each search session, fill in the blanks for schools you searched:

```markdown
#### School Name
- **Architecture**: Static HTML
- **Access**: curl → parse staff listing at https://...
- **Key endpoint**: https://www.school.ac.uk/department/staff/
- **Failed**: Tried API at /api/faculty → 404
- **Last verified**: 2026-06-26
```

If a school was NOT in this registry, add it. If you discovered a NEW strategy that worked, mark the old one under **Failed** and update **Access**.

### Batch Update Script

After a search session, run something like:

```python
# Update school-strategies.md with results from this session
for school in searched_schools:
    update_registry(school.name, school.architecture, school.access_method, school.endpoint)
```

The agent should update this file manually as part of the search workflow — after completing a school, add an entry.

#### University of Leeds
- **Architecture**: Static HTML (staff profile pages)
- **Access**: Direct URL access to staff profiles at ahc.leeds.ac.uk/design/staff/
- **Key endpoint**: https://ahc.leeds.ac.uk/design/staff/
- **Failed**: —
- **Last verified**: 2026-06-26

#### De Montfort University
- **Architecture**: Static HTML (staff profile pages)
- **Access**: Direct URL access to academic staff pages at dmu.ac.uk/academic-staff/
- **Key endpoint**: https://www.dmu.ac.uk/academic-staff/
- **Failed**: —
- **Last verified**: 2026-06-26

#### University of Brighton
- **Architecture**: Pure Portal (research.brighton.ac.uk)
- **Access**: Pure Portal JSON API → parse researcher profiles
- **Key endpoint**: https://research.brighton.ac.uk/persons/
- **Failed**: —
- **Last verified**: 2026-06-26
