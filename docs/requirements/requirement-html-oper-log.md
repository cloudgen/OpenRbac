**file**: docs/requirements/requirement-html-oper-log.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-html-oper-log`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the Operation log table. OpenRbac serves the list as `GET /oper-log`. The visible headers use well-known names. The table is the shared Apex table.

Who may open the list stays on `Catalog.oper_log`. The stored columns stay on `requirement-database`. The shell, the theme, and the ban on a script stay on `requirement-python-html-template`, `requirement-html-theme`, and `requirement-html-javascript`.

### 1.1 Human-facing

**In one sentence:** Operation log is a table whose headers say Operation ID, Business Type, and Operation Time.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account opening Operation log | `admin` |
| The other role | The sidebar link | Audit → Operation log → `/oper-log` |
| Not this file | Who may list, and the row a mutation writes | `Catalog.oper_log`, `requirement-database` |

| Includes | Excludes |
|----------|----------|
| The six headers, with Operation ID, Business Type, and Operation Time | A header that reads `oper_id`, `opera_id`, `business_type`, or `oper_time` |
| The shared Apex table: `table table-bordered table-striped` inside a `card`, with no `data-slot` | A separate Data grid, and a `data-slot` on that table |
| The stored cell values | A rename of `sys_oper_log` columns, and a rename of the `oper-log` text report |

| Surface | What you open | What for |
|---------|---------------|----------|
| Sidebar | Audit, then Operation log | `GET /oper-log` |
| Page | `templates/oper-log.vue` inside the shell | The table |
| Text report | `open-rbac oper-log` | The stored column names |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open Operation log | The table headers use the well-known names. The text report still prints the stored names. | open Audit, then Operation log |

## 2. Headers

The six headers, in order, are `Operation ID`, `title`, `Business Type`, `oper_name`, `status`, and `Operation Time`.

| Header | Stored field |
|--------|----------------|
| `Operation ID` | `oper_id` |
| `title` | `title` |
| `Business Type` | `business_type` |
| `oper_name` | `oper_name` |
| `status` | `status` |
| `Operation Time` | `oper_time` |

`Operation ID` is the header for `oper_id`. The header text is `Operation ID`. `opera_id` is not a column. `Business Type` is the header for `business_type`. `Operation Time` is the header for `oper_time`. The other three headers stay `title`, `oper_name`, and `status`.

Each cell shows the stored value. `business_type` stays the integer from `requirement-database`: `1` is add, `2` is edit, and `3` is remove. This file does not replace those integers with other words. An empty `oper_time` is an empty cell.

The `oper-log` text report stays `oper_id`, `title`, `business_type`, `oper_name`, `status`, and `oper_time`. `requirement-database` keeps those column names on `sys_oper_log`.

## 3. Shared table

The operation log table is the shared Apex table in `requirement-html-theme`. The element is one `table` with class `table table-bordered table-striped`, inside a `card`. The header is a `thead`. The body is a `tbody`. The `table`, the `thead`, each `tr`, each `th`, the `tbody`, and each `td` have no `data-slot`.

The header words are the six words in section 2. The sample column words Reference, Customer, Region, Channel, Status, Units, Amount, and Date stay sample words. They are not these headers.

The page links `/apex.css` and the theme sheet. It does not link `/element-plus.css` or `/openrbac.css`.

The page has a toolbar whose text is `Operation log`. The page keeps `el-pagination`. The rows are the list `Catalog.oper_log` returns, newest `oper_id` first.

Sample classes `w-full`, `table-fixed`, `caption-bottom`, and `text-sm` stay sample. A sticky header class stays sample. This page does not require them. The sample caption `10,000 rows, scrollable. Only the rows near the viewport are rendered.` stays sample text. This page does not use that sentence. Sort buttons, an up-down icon, a hidden spacer row, and sample status pills stay off this page. A sort button would need a script.

The page does not load the AdminLTE distribution, Bootstrap, jQuery, or Font Awesome.

## 4. Normative rules

1. **Destination.** Operation log **MUST** be `GET /oper-log`. The template **MUST** be `oper-log.vue` inside the shell. The product **MUST NOT** add an operation-log page at `/monitor/operlog`.
2. **Headers.** The table **MUST** show the six headers in section 2, in that order, on every skin. The header text **MUST** be `Operation ID` for `oper_id`, `Business Type` for `business_type`, and `Operation Time` for `oper_time`. The header text **MUST NOT** be `oper_id`, `opera_id`, `business_type`, or `oper_time`.
3. **Values.** A cell **MUST** show the stored field named in section 2. `business_type` **MUST** stay the stored integer. The `oper-log` text report **MUST** keep the names in section 2. `sys_oper_log` column names **MUST** stay the names in `requirement-database`.
4. **Shared table.** The operation log table **MUST** be one `table` with a `thead` and a `tbody`. That `table`, its `thead`, its `tr`, its `th`, its `tbody`, and its `td` **MUST NOT** carry a `data-slot`. That table **MUST** use `table table-bordered table-striped` inside a `card`, as `requirement-html-theme` requires. The header words **MUST** be the six words in section 2.
5. **Stylesheet.** The page **MUST** link `/apex.css` and `/themes/<name>.css`. It **MUST NOT** link `/element-plus.css` or `/openrbac.css`.
6. **Plain page.** The response **MUST NOT** contain a `<script` tag or a `<style` block. It **MUST NOT** contain `bootstrap.min.css`, `jquery`, or `font-awesome`. It **MUST NOT** add a sort button. It **MUST NOT** use the sample caption sentence in section 3.

## 5. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | An admin `/oper-log` page contains the six headers in section 2, in that order, including `>Operation ID<`, `>Business Type<`, and `>Operation Time<` |
| AC-2 | That page's headers do not contain `>oper_id<`, `>opera_id<`, `>business_type<`, or `>oper_time<` |
| AC-3 | An `/oper-log` page contains `<table`, `<thead`, and `<tbody`, and the operation log table has no `data-slot` |
| AC-4 | That table uses `table table-bordered table-striped` inside a `card` |
| AC-5 | The page links `/apex.css` and does not link `/element-plus.css`. It keeps the six headers |
| AC-6 | The operation log HTML contains no `<script` tag, no sort button, and no sample caption `10,000 rows, scrollable` |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Operation log | The OpenRbac page `GET /oper-log` |
| Operation ID | The header for the stored `oper_id`. The spelling `opera_id` is not a column |
| Business Type | The header for the stored `business_type` |
| Operation Time | The header for the stored `oper_time` |
| Data grid | The studied sample grid in the terminology below. This page uses the shared Apex table |

### Data grid

**Definition:** **admlte-component-data-grid** is the grid named **Data grid**. In the sample the element is a `table`. It has no `data-slot`. Sample classes include `w-full`, `table-fixed`, `caption-bottom`, and `text-sm`. A `caption` with class `sr-only` reads `10,000 rows, scrollable. Only the rows near the viewport are rendered.` The header is a `thead`. In the sample its classes include `sticky` and `top-0`. The body is a `tbody`. Heads, rows, and cells have no `data-slot="table-header"`, `data-slot="table-row"`, `data-slot="table-head"`, `data-slot="table-body"`, or `data-slot="table-cell"`. The sample column words are Reference, Customer, Region, Channel, Status, Units, Amount, and Date. Each head has `aria-sort="none"` and a button. The sample accessible names say the column is not sorted and that activating the button sorts ascending. Those buttons have `type="button"` and no `data-slot="button"`. The sample draws 27 data rows. Each has `data-index` from `0` through `26`. The first row shows REF-000001, Edsger Allen, APAC, Reseller, the word fulfilled, the units 11, the amount $752.94, and the date Jun 14, 2026. Five drawn rows read processing: REF-000002 Shafi Perlman, REF-000012 Jean Bartik, REF-000013 Anita Hopper, REF-000018 Anita Turing, and REF-000023 Margaret Torvalds. One drawn row reads backordered: REF-000010 Tim Berners-Lee, United Kingdom, Self-serve, 9 units, $319.64, Jan 12, 2026. The other drawn rows read fulfilled. Their sample names, in order, are Edsger Allen, Tim Berners-Lee, Radia Hopper, Shafi Bartik, Radia Perlman, Alan Torvalds, Leslie Johnson, Alan Johnson, Barbara Hopper, Margaret Allen, Alan Borg, Radia Liskov, Frances Lovelace, Margaret Perlman, Jean Dijkstra, Edsger Lamport, Barbara Allen, Margaret Borg, Leslie Knuth, Radia Hopper, and Barbara Knuth. A further row has `aria-hidden="true"` and one empty cell with `colspan="8"`. The sample style on that cell sets a height. Names, references, regions, channels, status words, units, amounts, dates, the caption sentence, the sort buttons, and the up-down icons are sample contents. They are not separate terms. The sample does not say that a status word sets the amount. The sample does not say that a row click does anything.

**Human daily-life explanation:** An **admlte-component-data-grid** is one wide grid of lines. The sample caption says there are ten thousand rows, and that only the lines near the window are drawn. The markup shows those nearby lines, then one tall blank line that is hidden from assistive tools. The orders grid is a different word.

**Daily-life example:** A grid whose first row shows “REF-000001” and “Edsger Allen” is the **admlte-component-data-grid**. The reference and the name are only the sample.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-15 | Active 1.0.0 | Operation log table. Headers `Operation ID`, `Business Type`, and `Operation Time`. The adminlte table is a Data grid |
| 2026-10-16 | Active 1.0.1 | The operation log uses the shared Apex table. The page links `/apex.css` and the theme sheet |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
