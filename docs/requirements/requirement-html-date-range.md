**file**: docs/requirements/requirement-html-date-range.md
**Status**: Active (Version 1.0.2)
**Area**: python
**Key**: `requirement-html-date-range`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the search date range. It is two native date inputs on one line. An arrow sits between them. The inputs have no From label and no To label. The posted names stay `begin` and `end`.

Users, roles, parameters, and dictionaries title the range `Created`. The login log titles it `Login time`. Those pages are `requirement-html-user-management`, `requirement-html-role-management`, `requirement-html-parameter-management`, `requirement-html-dictionaries`, and `requirement-html-login-log`. Which rows a date keeps stays on the page that owns the list. This file owns the control.

The skins are `requirement-html-theme`. A page with no script does not gain one (`requirement-html-javascript`, `requirement-python-html-template`).

### 1.1 Human-facing

**In one sentence:** Two browser date boxes sit on one line, with an arrow between them and no From or To label.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person filtering a list | an admin on Users |
| The other role | The two date boxes | `2026-04-01` then `2026-04-30` |
| Not this file | Which rows the dates keep, and the column that shows a stored time | the page requirement for that list |

| Includes | Excludes |
|----------|----------|
| Side-by-side `input type="date"` named `begin` and `end` | A presets popover, Alpine, or a script |
| The arrow `→` and no From or To label | A label, the word From, or the word To on this control |
| `max` on the start input when `end` is already in the query, and `min` on the end input when `begin` is already in the query | Class `el-date-picker` on this control |

| Surface | What you open | What for |
|---------|---------------|----------|
| `GET /users`, `/roles`, `/configs`, `/dicts` | the search row | the group word `Created` |
| `GET /login-log` | the search row | the group word `Login time` |
| `src/OpenRbac/templates/date-range.vue` | the shared template | the markup |
| `/apex.css` | the layout sheet | `.admlte-date-range` |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Pick a start and an end | Search posts `begin` and `end`. The next page limits the start input by the end date and the end input by the start date. | open the list and submit the search form |

## 2. Core Rules / Requirements (Mandatory)

1. **Template.** The control **MUST** be `src/OpenRbac/templates/date-range.vue`. Users, roles, parameters, dictionaries, and the login log **MUST** include that template in the search form. The group word **MUST** be the slot text. Users, roles, parameters, and dictionaries **MUST** pass `Created` and one trailing space. The login log **MUST** pass `Login time` and one trailing space. That space keeps the search title off the column token `>Created<` or `>Login time<`.
2. **Markup.** The root **MUST** be `div.admlte-date-range`. The title **MUST** be `span.admlte-date-range-title`. The pair **MUST** be `div.admlte-date-range-pair`. Each field **MUST** be `div.admlte-date-range-field`. The start input **MUST** have `id="admlte-date-from"`, `type="date"`, and `name="begin"`. The end input **MUST** have `id="admlte-date-to"`, `type="date"`, and `name="end"`. The control **MUST NOT** render a `label`, the text `From`, or the text `To`. The arrow **MUST** be `span.admlte-date-range-arrow` with `aria-hidden="true"` and the character `→` (U+2192). The title, the two inputs, and the arrow **MUST** sit on one line.
3. **Bounds.** When `query_end` is non-empty, the start input **MUST** set `max` to that string and **MUST** show `query_begin` as `value`. When `query_end` is empty, the start input **MUST** omit `max`. When `query_begin` is non-empty, the end input **MUST** set `min` to that string and **MUST** show `query_end` as `value`. When `query_begin` is empty, the end input **MUST** omit `min`. One search form **MUST** render one of those inputs for `begin` and one for `end`.
4. **Layout.** `/apex.css` **MUST** contain `.admlte-date-range`, `.admlte-date-range-pair`, `.admlte-date-range-field`, `.admlte-date-range-arrow`, and `.admlte-date-range input[type="date"]`. The date input and the arrow **MUST** be 30px tall. The pair **MUST** align the arrow with the inputs on one line.
5. **No script.** The template **MUST NOT** contain a `<script` tag, `x-data`, `x-model`, `:max`, or `:min`. The bounds **MUST** be ordinary `max` and `min` attributes from the query already on the page. The control **MUST NOT** use class `el-date-picker`. A presets popover **MUST NOT** be added to this control.
6. **Neighbors.** Hidden `begin` and `end` fields on a later form **MAY** keep the search. They are not this control. The column that shows a stored time **MUST** stay the column named by the page requirement.

### 2.1 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| Template | `src/OpenRbac/templates/date-range.vue` |
| Callers | `users.vue`, `roles.vue`, `configs.vue`, `dicts.vue`, and `login-log.vue` |
| Empty query | Both inputs render. Neither has `max` or `min` |
| `begin=2026-04-01` and `end=2026-04-30` | The start input has `max="2026-04-30"`. The end input has `min="2026-04-01"` |
| Styles | The same `.admlte-date-range` block is in `apex.css` |

### 2.2 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 1 – Caution:** The two dates stay unlabeled so the pair remains one line.
- **CIAO Principle 2 – Intentional:** The need is a start date and an end date. The purpose is two native date inputs and the arrow between them.
- **CIAO Principle 4 – Over-protect:** The bounds are attributes on the next response. The page does not gain a script to move `max` and `min` while the form is open.
- **CIAO Principle 5 – SSOT:** This file owns the control. Each list page owns which rows the dates keep.

## Under command line for normal user only

This requirement encodes no install, no detect, and no privilege. The control is read in the browser of this login. This file does not wrap `sudo`, `apt`, or a package installer, and it does not create a dedicated system user.

**This requirement:** the search range is two date inputs. Nothing in this file raises privilege.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Treat a hyphen between two dates, and a single `el-date-picker`, as a different control.
- **Intentional:** The two date boxes and the arrow are the visible range. The posted names stay `begin` and `end`.
- **Anti-fragile:** Every skin shares the template and the class names.
- **Over-protect:** Alpine attributes and a presets popover stay out. The query string is the bound.
- **Principle 21:** The portable rule is a start date and an end date side by side. The template path and the class names are Implementation Notes for this product.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Replace the two date inputs with one `el-date-picker`, a presets popover, or a hyphen-only pair.
- Add `x-data`, `x-model`, `:max`, `:min`, or a `<script` tag so the bounds update before the next response.
- Drop the trailing space on `Created` or `Login time`, which would make the search title the column token.
- Put the words From or To back on this control.
- Mint a separate page, file, or term for the arrow.
- Cite an agent procedure file as the behavioral authority in product source. Product source cites this requirement.

## 5. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-html-user-management.md` | Users search, group word `Created` |
| `docs/requirements/requirement-html-role-management.md` | Roles search, group word `Created` |
| `docs/requirements/requirement-html-parameter-management.md` | Parameters search, group word `Created` |
| `docs/requirements/requirement-html-dictionaries.md` | Dictionaries search, group word `Created` |
| `docs/requirements/requirement-html-login-log.md` | Login log search, group word `Login time` |
| `src/OpenRbac/templates/date-range.vue` | The control |
| `src/OpenRbac/element_plus/apex.css` | The date-range layout |

## 6. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | `templates/date-range.vue` is the control. `users.vue`, `roles.vue`, `configs.vue`, and `dicts.vue` include it with the slot text `Created` and a trailing space. `login-log.vue` includes it with `Login time` and a trailing space |
| AC-2 | An empty `query_begin` and `query_end` render `class="admlte-date-range"`, `id="admlte-date-from"` `type="date"` `name="begin"`, `id="admlte-date-to"` `type="date"` `name="end"`, and `class="admlte-date-range-arrow" aria-hidden="true">→<`. That render omits `max=`, `min=`, `>From<`, `>To<`, and a `label` |
| AC-3 | `query_begin` `2026-04-01` and `query_end` `2026-04-30` set `max="2026-04-30"` on the start input and `min="2026-04-01"` on the end input |
| AC-4 | `query_begin` `2026-04-01` with an empty `query_end` sets `min="2026-04-01"` and omits `max=`. An empty `query_begin` with `query_end` `2026-04-30` sets `max="2026-04-30"` and omits `min=` |
| AC-5 | The slot text `Created ` renders `Created ` inside the title and does not render the column token `>Created<` from that title. The slot text `Login time ` does not render `>Login time<` from that title |
| AC-6 | `/apex.css` contains `.admlte-date-range`, `.admlte-date-range-arrow`, and `.admlte-date-range input[type="date"]`, and the date input rule sets `height: 30px` |
| AC-7 | The rendered control contains no `<script`, no `x-data`, no `x-model`, and no `class="el-date-picker"` |

## Terminologies

### Date range

**Definition:** The date range is the search control for a start date and an end date. The start is `input type="date"` named `begin`. The end is `input type="date"` named `end`. The arrow `→` sits between them on the same line. The control shows no From label and no To label. The root class is `admlte-date-range`. A non-empty end date sets `max` on the start input. A non-empty start date sets `min` on the end input. The group word is `Created` or `Login time`, with one trailing space.

**Human daily-life explanation:** A date range is the pair of days a person means, the first day and the last day. Each day has its own box. The boxes sit on one line. An arrow points from the first box to the second.

**Daily-life example:** 1 Apr 2026 and 30 Apr 2026 are one date range. The list keeps rows inside those days. The boxes do not grow a shortcut menu.

## 7. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-15 | Active 1.0.0 | The search date range is side-by-side From and To native date inputs |
| 2026-10-15 | Active 1.0.1 | The two date inputs stay on one line and show no From or To label |
| 2026-10-16 | Active 1.0.2 | The date-range layout lives in `/apex.css` |

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
