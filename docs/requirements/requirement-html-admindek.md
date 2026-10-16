**file**: docs/requirements/requirement-html-admindek.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-html-admindek`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file records the studied Admindek Analytics page. OpenRbac already stores the name `admindek` as theme choice 2. The listener still sends the Apex shell, `/apex.css`, and `/themes/admindek.css`. This file says which pieces of that studied page stay out of the response.

The eleven names, the shared shell, and the ban on a commercial stylesheet stay on `requirement-html-theme`. The one allowed script stays on `requirement-html-javascript`. The body size stays on `requirement-html-body-font`. The menu row and the verb stay on `requirement-python-tui` and `requirement-python-cli-interface`.

### 1.1 Human-facing

**In one sentence:** Choosing Admindek paints the same OpenRbac pages with the Admindek color sheet. It does not load the Admindek dashboard template.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person who picks theme choice 2 | `open-rbac theme`, then `2` |
| The other role | The page the browser paints | `/apex.css` and `/themes/admindek.css` |
| Not this file | The permission check and the menu groups | `requirement-rbac` |

| Includes | Excludes |
|----------|----------|
| The studied Admindek Analytics shell, and the rule that OpenRbac does not serve it | A second frontend folder or a twelfth theme name |
| The original color sheet `/themes/admindek.css` on the Apex shell | The commercial Admindek stylesheet, its icon fonts, and its scripts |
| The existing OpenRbac menu, forms, and posts | The studied command palette, customizer, notifications, language menu, and demo account |

| Surface | What you open | What for |
|---------|---------------|----------|
| Theme menu | Server row 24, or `open-rbac theme` | Store `admindek` |
| Next page | The listener | Apex markup plus `/themes/admindek.css` |
| Studied page | Admindek Analytics Dashboard | The shell this file records and does not ship |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Pick Admindek | The next HTML page uses the Admindek color sheet on the same shell as Apex. The studied dashboard markup stays off that page. | `open-rbac theme`, then `2` |

## 2. The studied page

The studied document is one HTML page. Its title is `Analytics Dashboard | Admindek Dashboard Template`. The visible footer credit is `OpenRbac (Admindek Theme)`. The main row says `Empty content`. The sidebar list under the caption `Navigation` is empty.

| Piece in the studied document | OpenRbac |
|-------------------------------|----------|
| `title` `Analytics Dashboard \| Admindek Dashboard Template` | Not a product page title. Signed-in pages keep their own titles |
| `theme-color` `#1e293b`, canonical `https://demo.dashboardpack.com/admindek-html/`, author DashboardPack.com | Omitted. The product does not send that head |
| Google font Inter, Phosphor icons, Tabler icons, `style.css`, `style-preset.css`, `jsvectormap.min.css` | Omitted. A page links `/apex.css` and `/themes/admindek.css` only |
| `body` attributes `data-pc-preset="preset-1"`, `data-pc-sidebar-caption="true"`, `data-pc-direction="ltr"`, `data-pc-theme="light"`, `data-pc-sidebar_theme="false"` | Omitted. The body is the Apex document |
| `nav.pc-sidebar`, logo `logo-white.svg`, caption `Navigation`, empty `ul.pc-navbar` | Omitted. The side column stays `aside.main-sidebar`. The menu stays the OpenRbac groups |
| `header.pc-header`: sidebar toggle, mobile collapse, search with `⌘K`, theme Dark / Light / Default, languages English (UK), français, Română, and 中国人, account shortcuts, a notification badge `5`, and the user menu | Omitted. Those controls call `layout_change` or open a menu the product does not serve |
| User menu name `John Doe`, address `john.doe@acmecorp.com`, badge `Pro Plan` | Omitted. The shell shows the signed-in account |
| Notification rows Payment Received, New Team Member, Monthly Report Ready, Security Alert, Feature Update, and the lorem Security row | Omitted. They are demo copy |
| Modal `#commandPalette`, placeholder `Search pages, actions...` | Omitted. The product has no command palette |
| `div.pc-container` > `div.pc-content`, title `Analytics`, breadcrumb Home / Dashboard / Analytics, body `Empty content` | Omitted. There is no `/analytics` route from this file. Page bodies stay the existing templates |
| `footer.pc-footer` text `OpenRbac (Admindek Theme)`, plus Home, Documentation `https://dashboardpack.com/docs/`, and Support `https://dashboardpack.com/support/` | Omitted. The product shell has no `pc-footer`. Those two external links stay out |
| Offcanvas `#offcanvas_pc_layout`, title Theme Customizer: Theme Mode, Layout, Colors, Advanced | Omitted. Theme choice is the stored name, not a page customizer |
| Color swatches preset-1 through preset-8, first swatch Ocean Blue `#4680ff` | Studied only. `/themes/admindek.css` keeps its own colors |
| Chart.js, vector map, world map, device chart, and the KPI script that calls `AdmindekChart` | Omitted |
| Closing calls `layout_change('light')`, `change_box_container('false')`, `layout_caption_change('true')`, `layout_rtl_change('false')`, `preset_change('preset-1')`, `layout_theme_sidebar_change('false')` | Omitted |

The studied accent used by the inline timeline and the chart script is `#4680ff`. The product sheet does not take that value from this page.

## 3. What the name means here

`admindek` remains choice 2. The label remains `Admindek`. Empty and choice 1 remain `apex`. This file does not add a name and does not rename one.

A page whose stored theme is `admindek` links `/apex.css` and `/themes/admindek.css`. The markup is the Apex shell in `requirement-html-theme`: `wrapper`, `main-sidebar`, `content-wrapper`, `main-header`, `content`, `nav-sidebar`, `nav-link active`, `table table-bordered table-striped`, `form-control`, and `btn btn-primary`. The signed-in menu stays Home, Access, Catalog, Audit, and Setup, filtered by permission. Form `method`, `action`, and field `name` values stay on the page that owns them.

`/themes/admindek.css` is `src/OpenRbac/element_plus/themes/admindek.css`. The listener serves it as `text/css`. The file sets shell colors for that name. Its comment states that it is not a commercial template and that layout stays in `/apex.css`. Layout stays in `src/OpenRbac/element_plus/apex.css`.

Brand controls in that layout read this sheet. A search button, an add button, the current organization row, a checked job-title tag, and a menu-type tag use `--primary` and `--primary-foreground`. Search panels, work panels, and date fields use `--panel`, `--border`, `--input`, and `--muted-foreground`. The hex values stay the original indigo set. They are not the studied Ocean Blue.

### 3.1 Implementation notes (this project)

| Item | Value |
|------|--------|
| Product | OpenRbac. Command `open-rbac` |
| Stored theme | `admindek`. Menu label `Admindek`. Choice `2` |
| Layout sheet | `src/OpenRbac/element_plus/apex.css`, URL `/apex.css` |
| Color sheet | `src/OpenRbac/element_plus/themes/admindek.css`, URL `/themes/admindek.css` |
| Shell | The Apex classes in `requirement-html-theme`. Not `pc-sidebar` or `pc-header` |
| Product version | Unchanged by this file |

## 4. Normative rules

1. **Name.** Choice 2 **MUST** stay the stored name `admindek` and the label `Admindek`. This file **MUST NOT** add a theme name and **MUST NOT** remove one.
2. **Shell.** An `admindek` page **MUST** emit the Apex shell in `requirement-html-theme`. It **MUST NOT** emit `pc-sidebar`, `pc-header`, `pc-container`, `pc-footer`, `pc-navbar`, `commandPalette`, `offcanvas_pc_layout`, or `data-pc-preset`.
3. **Stylesheets.** The page **MUST** link `/apex.css` and `/themes/admindek.css` from this host. It **MUST NOT** link `fonts.googleapis.com`, Phosphor icons, Tabler icons, `style.css`, `style-preset.css`, `jsvectormap`, `/element-plus.css`, `/openrbac.css`, or `/adminlte.css`.
4. **Color sheet.** `/themes/admindek.css` **MUST** remain the original OpenRbac color sheet for that name. It **MUST NOT** be replaced by the commercial Admindek stylesheet. The studied `#4680ff` and `#1e293b` **MUST NOT** be copied in as that file.
5. **Script.** The page **MUST NOT** include `layout_change`, `preset_change`, `AdmindekChart`, Chart.js, Bootstrap JavaScript, Popper, SimpleBar, i18next, or a script from another host. A table checkbox still loads `/table-check.js` once, as `requirement-html-javascript` requires. A page with no table checkbox **MUST NOT** include a `<script` tag.
6. **Menu and routes.** The signed-in menu **MUST** stay the OpenRbac groups. The studied caption `Navigation` with an empty list **MUST NOT** replace that menu. This file **MUST NOT** add a route whose path is `/analytics` or `/dashboard/index.html`.
7. **Demo chrome.** The response **MUST NOT** contain `John Doe`, `Empty content`, `Theme Customizer`, `Search pages, actions...`, or a link to `dashboardpack.com`. The studied footer sentence `OpenRbac (Admindek Theme)` **MUST NOT** be added as a product footer by this file.
8. **Same posts.** An `admindek` page **MUST** keep the same form names and permissions as the other ten skins.
9. **Neighbors.** Users, roles, menus, departments, and job titles stay in Access. Parameters, dictionaries, and notices stay in Catalog. The operation log, the login log, and online stay in Audit. The studied header languages, notifications, and lock screen **MUST NOT** become menus.

## 5. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | An `admindek` sign-in page links `/apex.css` and `/themes/admindek.css`, uses `form-control` and `btn btn-primary`, and does not link `/element-plus.css` |
| AC-2 | That page does not contain `pc-sidebar`, `pc-header`, `pc-container`, `commandPalette`, `data-pc-preset`, `fonts.googleapis.com`, `phosphor-icons`, `tabler-icons`, or `style-preset.css` |
| AC-3 | That page does not contain `layout_change`, `AdmindekChart`, `chart.umd`, or `bootstrap.min.js` |
| AC-4 | That page does not contain `John Doe`, `Empty content`, `dashboardpack.com`, or `Analytics Dashboard \| Admindek Dashboard Template` |
| AC-5 | A request for `/themes/admindek.css` returns `text/css`. The file text says it is not a commercial template and does not define `.pc-sidebar` |
| AC-6 | Theme choice 2 is the stored name `admindek`. The product does not register a page at `/analytics` |
| AC-7 | `/themes/admindek.css` sets `--primary: #4f46e5` and does not contain `#4680ff`. `/apex.css` paints `.user-btn` with `var(--primary)` |

## 6. Protection rule

Future editors **MUST NOT**:

- Replace `/themes/admindek.css` with the commercial Admindek stylesheet, or copy its `pc-*` rules into `/apex.css`.
- Add the studied `<script` blocks, the Google font, the Phosphor or Tabler icon fonts, or a script from another host.
- Emit the studied sidebar, header, command palette, customizer, or footer in place of the Apex shell.
- Treat this file as an order to add an Analytics dashboard, a language switcher, or a notification list.
- Bump the product version because this requirement was added.

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Admindek | Theme choice 2. Stored name `admindek`. The OpenRbac color sheet, not the commercial template |
| Studied page | The Admindek Analytics document recorded in section 2 |
| Apex shell | The product markup and `/apex.css`, shared by every skin |

### Project requirements

**Definition:** Project requirements are this workspace’s product law: durable normative documents under `docs/requirements/` that state what this engineering system must or should do. They are finished, project-scoped rules, including the project’s own choices of application type, paths, and who acts. Every requirement file prints a human-facing section with one sentence, three boxes, includes and excludes, surfaces, and a practice line, and does not lead with a privilege code as the only words. They are not reusable blanks, not agent procedures, and not a place to freeze one brand string as if it were the only possible configuration.

**Human daily-life explanation:** Project requirements are this product’s must and should law under `docs/requirements/`. They are finished rules for this product, not blank forms.

**Daily-life example:** “This household must lock the door by 10” is law for this house. A blank curfew form in a stationery shop is not.

### UI constraint theme support

**Definition:** A UI constraint theme support is the rule that says which container fills follow the host theme and which stay a chosen fill. Following the theme means light, dark, or accent can change without a second layout. It is not the size rule, and it is not a toolkit install check. The requirement names which surfaces follow the theme.

**Human daily-life explanation:** A UI constraint theme support is the house rule for paint. Some shelves take the room’s daylight or night paint. One shelf stays white so the photos stay easy to see. The rule is not how wide the shelf grows.

**Daily-life example:** The window frame follows the room’s dark or light theme. The card under the film strip stays a chosen light fill. That split is the UI constraint theme support.

### Registry discipline

**Definition:** Registry discipline is the rule that every authoritative inventory of workspace artifacts matches disk, is scoped to its job, is updated in the same change that creates or removes the thing, and never invents a path that is not there. The product-law inventory is `docs/requirements/index.md`.

**Human daily-life explanation:** Registry discipline means every list of what exists must match the actual files, update in the same change, and never invent a row for something that is not there.

**Daily-life example:** When you add a new mug to the cupboard, you add a line to the mug inventory the same visit. You do not write “golden teapot” when that teapot is not there.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-16 | Active 1.0.0 | The studied Admindek Analytics page is recorded. Choice 2 stays the Apex color skin `admindek` |
| 2026-10-16 | Active 1.0.1 | The original indigo sheet paints brand controls on the Apex shell. The studied ocean blue stays out |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
