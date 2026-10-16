**file**: docs/requirements/requirement-html-theme.md
**Status**: Active (Version 1.0.6)
**Area**: python
**Key**: `requirement-html-theme`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

The stored theme is the color skin the listener serves. Choice 1 is apex. The same templates, the same form names, and the same permissions stay. The shell markup stays. The color sheet changes with the choice.

The menu row and the verb are `requirement-python-tui` and `requirement-python-cli-interface`. The stored name is `requirement-environment`. This file is what the browser receives after `serve`.

### 1.1 Human-facing

**In one sentence:** Enter keeps Apex. Pick another number and the next page uses that skin's colors on the same shell.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person who chose a theme | server row 24, then row 23 |
| The other role | The page the browser paints | `/apex.css` and `/themes/hospital.css` |
| Not this file | The permission check | `requirement-rbac` |

| Includes | Excludes |
|----------|----------|
| Eleven skins from the same templates | A second frontend folder |
| A same-origin stylesheet for the chosen skin | AdminLTE JavaScript, Bootstrap JavaScript, Vue, or a script from another host |
| Original OpenRbac colors for each name | A copy of a commercial dashboard stylesheet |

## 2. Skins

| Choice | Stored name | Label |
|--------|-------------|--------|
| 1 | `apex` | Apex. Enter selects this name. Empty means this name |
| 2 | `admindek` | Admindek |
| 3 | `architectui` | ArchitectUI |
| 4 | `adminty` | Adminty |
| 5 | `analytic` | Analytic |
| 6 | `cryptocurrency` | Cryptocurrency |
| 7 | `directory` | Directory |
| 8 | `finance-saas` | Finance SaaS |
| 9 | `fiori` | Fiori |
| 10 | `hospital` | Hospital |
| 11 | `kero` | Kero |

Every theme emits one shell. The shell is `wrapper`, `main-sidebar`, `content-wrapper`, `main-header`, and `content`. The menu is `nav-sidebar`. A current link is `nav-link active`. A table is `table table-bordered table-striped` inside a `card`, including the operation log. That page's headers are `requirement-html-oper-log`. A field is `form-control`. A primary button is `btn btn-primary`. A dialog is a `card`.

Every page links `/apex.css` and `/themes/<name>.css`. `/apex.css` is the layout. The theme file sets the shell colors. `vue3` and `adminlte` are not theme names.

Choice 1 `apex` and choice 2 `admindek` each set the full token set: sidebar, header, canvas, panel, primary, background, foreground, card, muted, border, input, and ring. The Apex primary is the product green `#1ab394`. The Admindek primary is the original indigo `#4f46e5`. Brand controls in the layout use `var(--primary)`. Those controls are the search button, the add button, the current organization row, the checked job-title tag, and the menu-type tag. Export, edit, remove, reset, and the status switch keep their own action colors. Search panels and date fields use the panel, border, and input tokens.

`/apex.css` is the product skin. It uses those class names. It is not a copy of the AdminLTE distribution. The page does not load that distribution and does not load Bootstrap. A theme file is not a commercial template. The name is the OpenRbac skin.

## 3. Normative rules

1. **Choice.** The listener **MUST** render each HTML page with `Settings.theme()`. Empty **MUST** be `apex`. The only values **MUST** be the eleven names in section 2. An invalid value **MUST** refuse the page with the settings error.
2. **Fresh read.** `Settings.theme()` **MUST** read the settings file again on each call. A choice stored after the listener started **MUST** be the skin of the next HTML page in that process. An environment value **MUST** still win over the file.
3. **One shell.** Every theme **MUST** emit the classes in section 2. The side column **MUST** be `aside.main-sidebar`. The page **MUST NOT** emit an Element Plus menu, table, dialog, or form class for those controls.
4. **Stylesheets.** A page **MUST** link `/apex.css` and `/themes/<name>.css` from this host. It **MUST NOT** link `/element-plus.css`, `/openrbac.css`, or `/adminlte.css`. It **MUST NOT** load a skin from a CDN. The listener **MUST** serve `/apex.css` from `src/OpenRbac/element_plus/apex.css` and each theme file from `src/OpenRbac/element_plus/themes/<name>.css`. The package data **MUST** include those files. A theme path **MUST** be one of the eleven names.
5. **Same posts.** Every theme **MUST** keep the same form `method`, `action`, and field `name` values, including `csrf`.
6. **No skin script.** A theme **MUST NOT** add AdminLTE JavaScript, Bootstrap JavaScript, Vue, or a script from another host. The active menu item **MUST** already be in the HTML. A page that shows a table checkbox **MUST** include `<script src="/table-check.js"></script>` once, as `requirement-html-javascript` requires. A page with no table checkbox **MUST NOT** include a `<script` tag.
7. **Scrollport.** `.main-sidebar` in `/apex.css` **MUST** set `height: 100vh` and `overflow: auto`. The shell **MUST NOT** put that column inside `el-scrollbar`. The ban on measuring a wrap and writing its height is `requirement-html-javascript`.
8. **Colors.** `/themes/<name>.css` **MUST** set the shell colors for that name, including `--primary`, `--primary-foreground`, `--background`, `--foreground`, `--card`, `--muted`, `--muted-foreground`, `--border`, `--input`, and `--ring`, and the sidebar, header, canvas, and panel tokens. Those colors are original to this product. The file **MUST NOT** be a commercial dashboard stylesheet. A brand control in `/apex.css` **MUST** use `var(--primary)`. The Apex sheet **MUST** set `--primary` to `#1ab394`. The Admindek sheet **MUST** set `--primary` to `#4f46e5` and **MUST NOT** contain `#4680ff` or `#1e293b`. Export, edit, remove, reset, and the status switch **MUST** keep their own action colors.
9. **Body font.** The document `body` font size **MUST** be `requirement-html-body-font`. `/apex.css` **MUST** set `font-size: 13px` on `body`. A heading or a control that already names its own size **MUST** keep that size.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | An empty theme sign-in page links `/apex.css` and `/themes/apex.css` and does not link `/element-plus.css` |
| AC-2 | An `admindek` sign-in page links `/apex.css` and `/themes/admindek.css`, uses `form-control` and `btn btn-primary`, and does not link `/element-plus.css` |
| AC-3 | A shell uses `main-sidebar` and `nav-link active`, and does not emit an Element Plus menu class |
| AC-4 | `.main-sidebar` is `height: 100vh` and `overflow: auto`. The shell templates contain no `el-scrollbar` |
| AC-5 | A settings file written after the first read is the theme of the next page |
| AC-6 | A page with no table checkbox contains no `<script` tag. A page that shows a table checkbox contains only `<script src="/table-check.js"></script>` |
| AC-7 | A users page keeps `method="post"`, `action="/users/add"`, and the names `csrf`, `user_name`, `nick_name`, `dept_id`, `role_id`, and `password` |
| AC-8 | `OPENRBAC_THEME` set to a value other than the eleven names refuses the sign-in response with the settings error |
| AC-9 | A request for `/apex.css` returns that file as `text/css`. A request for `/themes/hospital.css` returns that file as `text/css` |
| AC-10 | `themes/apex.css` sets `--primary: #1ab394`. `themes/admindek.css` sets `--primary: #4f46e5` and does not contain `#4680ff`. `/apex.css` still contains `--primary:oklch(50% .175 160)` and paints `.user-btn` with `var(--primary)` |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Theme | One stored name from section 2 |
| Skin | The color sheet for that name, on the shared Apex shell |
| Apex shell | The product markup and `/apex.css`. It is not the upstream AdminLTE file |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | The stored theme selects the markup and the stylesheet `serve` sends |
| 2026-10-14 | Active 1.0.1 | Acceptance checks cover the same form names, a refused invalid theme, and the stylesheet response |
| 2026-10-15 | Active 1.0.2 | The document body font size is `requirement-html-body-font` |
| 2026-10-15 | Active 1.0.3 | The operation log table is the Data grid in `requirement-html-oper-log` |
| 2026-10-16 | Active 1.0.4 | A table checkbox loads `/table-check.js`. Neither skin loads AdminLTE or Bootstrap JavaScript |
| 2026-10-16 | Active 1.0.5 | The Vue theme is gone. AdminLTE is renamed Apex. Ten more skins share that shell |
| 2026-10-16 | Active 1.0.6 | Apex and Admindek set the full token set. Brand controls follow `--primary`. The studied Admindek ocean blue stays out |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
