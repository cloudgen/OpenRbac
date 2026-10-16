**file**: docs/requirements/requirement-html-architectui.md
**Status**: Active (Version 1.0.0)
**Area**: python
**Key**: `requirement-html-architectui`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file records the studied ArchitectUI Analytics page. OpenRbac already stores the name `architectui` as theme choice 3. The listener still sends the Apex shell, `/apex.css`, and `/themes/architectui.css`. This file says which pieces of that studied page stay out of the response.

The eleven names, the shared shell, and the ban on a commercial stylesheet stay on `requirement-html-theme`. The one allowed script stays on `requirement-html-javascript`. The body size stays on `requirement-html-body-font`. The menu row and the verb stay on `requirement-python-tui` and `requirement-python-cli-interface`. The Admindek study stays on `requirement-html-admindek`.

### 1.1 Human-facing

**In one sentence:** Choosing ArchitectUI paints the same OpenRbac pages with the ArchitectUI color sheet. It does not load the ArchitectUI dashboard template.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person who picks theme choice 3 | `open-rbac theme`, then `3` |
| The other role | The page the browser paints | `/apex.css` and `/themes/architectui.css` |
| Not this file | The permission check and the menu groups | `requirement-rbac` |

| Includes | Excludes |
|----------|----------|
| The studied ArchitectUI Analytics shell, and the rule that OpenRbac does not serve it | A second frontend folder or a twelfth theme name |
| The original color sheet `/themes/architectui.css` on the Apex shell | The commercial ArchitectUI stylesheet, its icon fonts, Ionicons, and its scripts |
| The existing OpenRbac menu, forms, and posts | The studied search, megamenu, language menu, notifications, layout customizer, drawer, and demo account |

| Surface | What you open | What for |
|---------|---------------|----------|
| Theme menu | Server row 24, or `open-rbac theme` | Store `architectui` |
| Next page | The listener | Apex markup plus `/themes/architectui.css` |
| Studied page | ArchitectUI Analytics Dashboard | The shell this file records and does not ship |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Pick ArchitectUI | The next HTML page uses the ArchitectUI color sheet on the same shell as Apex. The studied dashboard markup stays off that page. | `open-rbac theme`, then `3` |

## 2. The studied page

The studied document is one HTML page. `html` has `lang="en"`. Its title is `Analytics Dashboard - This is an example dashboard created using build-in elements and components.` The meta description repeats that sentence, including the word `build-in`. The canonical link is `https://demo.dashboardpack.com/architectui-html-pro/`. The content column `div.app-main__inner` is empty. The sidebar list under the heading `Menu` is Dashboards, and under that one child, Analytics, whose address is `index.html`.

| Piece in the studied document | OpenRbac |
|-------------------------------|----------|
| `title` and description `Analytics Dashboard - This is an example dashboard created using build-in elements and components.` | Not a product page title. Signed-in pages keep their own titles |
| Canonical `https://demo.dashboardpack.com/architectui-html-pro/` | Omitted. The product does not send that head |
| Ionicons v8 module `assets/ionicons/ionicons.esm.js`, and the inline rule that hides `ion-icon` until `.hydrated` | Omitted |
| Inline loader style that forces `.app-container` to opacity 1, and the `DOMContentLoaded` script that adds `app-loaded` on `body` | Omitted. The body is the Apex document |
| Hashed scripts `vendors`, `main`, `demo`, `ladda`, `blockui`, `circle_progress`, `count_up`, `toastr`, `sweet_alerts`, `scrollbar`, `carousel_slider`, `tables`, `charts`, and `sparklines`, each `ccd80cc732201fa31f61.js` | Omitted |
| Hashed sheets `assets/styles/vendors.ccd80cc732201fa31f61.css` and `assets/styles/main.ccd80cc732201fa31f61.css` | Omitted. A page links `/apex.css` and `/themes/architectui.css` only |
| Inline SweetAlert2 `:root` sheet. The confirm button token is `#7066e0` | Omitted. `/themes/architectui.css` keeps its own colors |
| `body.app-loaded` and root `div.app-container.app-theme-white.body-tabs-shadow.fixed-header.fixed-sidebar` | Omitted |
| `div.app-header.header-shadow`: empty `div.logo-src`, hamburger `close-sidebar-btn` with `data-class="closed-sidebar"`, mobile menu, and the header ellipsis | Omitted. The top band stays `main-header` |
| Search input, placeholder `Type to search` | Omitted |
| Header megamenu: Mega Menu, Settings with badge `4`, and Projects. Sample rows include Contacts, Incidents, Companies, Dashboards, Graphic Design, App Development, Icon Design, Miscellaneous, and Frontend Dev | Omitted |
| Header dots: `ion-icon` `apps-sharp` (Grid Dashboard), `notifications-sharp` (`You have 21 unread messages`), language flag `DE` (`Choose Language`, Germany marked), and `analytics-outline` (Users Online, figure `344k`, change `176%`) | Omitted. They are demo chrome |
| Account picture `assets/images/avatars/1.jpg`. Dropdown heading `Alina Mcloughlin` and line `A short profile description`. Visible heading `Alina Mclourd` and line `VP People Manager`. Buttons Logout, Message Inbox, Support Tickets, and Open Messages. Rows Chat `8`, Recover Password, Settings `New`, Messages `512`, and Logs | Omitted. The shell shows the signed-in account |
| Calendar button `show-toastr-example`, and the right-drawer hamburger `open-right-drawer` | Omitted |
| `div.ui-theme-settings`, opener `#TooltipDemo`. Headings Layout Options, Header Options, Sidebar Options, and Main Content Options. Switches Fixed Header, Fixed Sidebar, and Fixed Footer. Two `Choose Color Scheme` swatch rows and `Restore Default`. Sidebar Background Image, Page Title Icon, and Page Title Description | Omitted. Theme choice is the stored name, not a page customizer |
| `div.app-sidebar.sidebar-shadow`, a second `logo-src` and `closed-sidebar` hamburger, `scrollbar-sidebar`, and `ul.vertical-nav-menu.metismenu` | Omitted. The side column stays `aside.main-sidebar`. The menu stays the OpenRbac groups |
| Heading `Menu`. Parent Dashboards with `pe-7s-rocket` and `mm-active`. Child Analytics, `href="index.html"`, also `mm-active` | Omitted. There is no `index.html` route from this file |
| `div.app-main__outer` > `div.app-main__inner`, empty | Omitted. Page bodies stay the existing templates |
| `div.app-wrapper-footer` > `div.app-footer`. Left dots repeat the notification tabs Messages, Events, and System Errors, the line `You have 21 unread messages`, timeline titles including `All Hands Meeting` and `Build the production release`, and the empty-errors pair `All caught up!` / `There are no system errors!` | Omitted |
| Footer right: Footer Menu (Contacts, Incidents `5`, Companies, Dashboards, Queues, Resource Groups, Goal Metrics `3`, Campaigns) and Grid Menu with badge `NEW`, title Two Column Grid, and buttons Automation, Reports, Activity, and Settings | Omitted. The product shell has no `app-footer` |
| `div.app-drawer-wrapper`. Heading Servers Status with Server Load 1 `51%` (`#fd7e14`), Server Load 2 `16%` (`#3ac47d`), and Server Load 3 `51%` (`#ff8130`). Live Statistics, Packages `43`, Dropped `65`, Invalid `18`, Escalate Issue, and Support Center. File Transfers names `TPSReport.docx`, `Latest_photos.zip`, `Annual Revenue.pdf`, and `Analytics_GrowthReport.xls`. Heading Tasks in Progress | Omitted |
| Closing `div.app-drawer-overlay` | Omitted |
| Icon classes `pe-7s-*`, `fa`, `lnr-*`, and `ion-icon` | Omitted. The product does not ship those icon fonts |

The studied confirm color is `#7066e0`. The drawer percents use `#fd7e14`, `#3ac47d`, and `#ff8130`. The product sheet does not take those values from this page. Its sidebar is `#0f2744` and its primary is `#d97706`.

## 3. What the name means here

`architectui` remains choice 3. The label remains `ArchitectUI`. Empty and choice 1 remain `apex`. This file does not add a name and does not rename one.

A page whose stored theme is `architectui` links `/apex.css` and `/themes/architectui.css`. The markup is the Apex shell in `requirement-html-theme`: `wrapper`, `main-sidebar`, `content-wrapper`, `main-header`, `content`, `nav-sidebar`, `nav-link active`, `table table-bordered table-striped`, `form-control`, and `btn btn-primary`. The signed-in menu stays Home, Access, Catalog, Audit, and Setup, filtered by permission. Form `method`, `action`, and field `name` values stay on the page that owns them.

`/themes/architectui.css` is `src/OpenRbac/element_plus/themes/architectui.css`. The listener serves it as `text/css`. The file sets shell colors for that name. Its comment states that it is not a commercial template and that layout stays in `/apex.css`. Layout stays in `src/OpenRbac/element_plus/apex.css`.

### 3.1 Implementation notes (this project)

| Item | Value |
|------|--------|
| Product | OpenRbac. Command `open-rbac` |
| Stored theme | `architectui`. Menu label `ArchitectUI`. Choice `3` |
| Layout sheet | `src/OpenRbac/element_plus/apex.css`, URL `/apex.css` |
| Color sheet | `src/OpenRbac/element_plus/themes/architectui.css`, URL `/themes/architectui.css` |
| Shell | The Apex classes in `requirement-html-theme`. Not `app-container`, `app-sidebar`, or `app-header` |
| Product version | Unchanged by this file |

## 4. Normative rules

1. **Name.** Choice 3 **MUST** stay the stored name `architectui` and the label `ArchitectUI`. This file **MUST NOT** add a theme name and **MUST NOT** remove one.
2. **Shell.** An `architectui` page **MUST** emit the Apex shell in `requirement-html-theme`. It **MUST NOT** emit `app-container`, `app-header`, `app-sidebar`, `vertical-nav-menu`, `metismenu`, `app-main__inner`, `app-footer`, `ui-theme-settings`, `app-drawer-wrapper`, or `app-drawer-overlay`.
3. **Stylesheets.** The page **MUST** link `/apex.css` and `/themes/architectui.css` from this host. It **MUST NOT** link `assets/styles/vendors`, `assets/styles/main`, `ionicons`, `/element-plus.css`, `/openrbac.css`, or `/adminlte.css`.
4. **Color sheet.** `/themes/architectui.css` **MUST** remain the original OpenRbac color sheet for that name. It **MUST NOT** be replaced by the commercial ArchitectUI stylesheet. The studied `#7066e0`, `#fd7e14`, `#3ac47d`, and `#ff8130` **MUST NOT** be copied in as that file. The sheet **MUST NOT** define `.app-sidebar`.
5. **Script.** The page **MUST NOT** include `ionicons.esm.js`, `vendors.*.js`, `ladda`, `blockui`, `circle_progress`, `count_up`, `toastr`, `sweet_alerts`, `scrollbar`, `carousel_slider`, `sparklines`, SweetAlert2, MetisMenu, Perfect Scrollbar, Bootstrap JavaScript, or a script from another host. A table checkbox still loads `/table-check.js` once, as `requirement-html-javascript` requires. A page with no table checkbox **MUST NOT** include a `<script` tag.
6. **Menu and routes.** The signed-in menu **MUST** stay the OpenRbac groups. The studied heading `Menu` with Dashboards and Analytics **MUST NOT** replace that menu. This file **MUST NOT** add a route whose path is `/analytics` or `/index.html`.
7. **Demo chrome.** The response **MUST NOT** contain `Alina Mcloughlin`, `Alina Mclourd`, `VP People Manager`, `Type to search`, `You have 21 unread messages`, `All Hands Meeting`, `All caught up!`, `Layout Options`, `Servers Status`, `TPSReport.docx`, `build-in elements`, or a link to `dashboardpack.com`. The studied title **MUST NOT** become a product page title.
8. **Same posts.** An `architectui` page **MUST** keep the same form names and permissions as the other ten skins.
9. **Neighbors.** Users, roles, menus, departments, and job titles stay in Access. Parameters, dictionaries, and notices stay in Catalog. The operation log, the login log, and online stay in Audit. The studied header languages, notifications, megamenus, and drawer **MUST NOT** become menus.

## 5. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | An `architectui` sign-in page links `/apex.css` and `/themes/architectui.css`, uses `form-control` and `btn btn-primary`, and does not link `/element-plus.css` |
| AC-2 | That page does not contain `app-container`, `app-sidebar`, `app-header`, `vertical-nav-menu`, `metismenu`, `app-main__inner`, `ui-theme-settings`, `app-drawer-wrapper`, or `ion-icon` |
| AC-3 | That page does not contain `ionicons.esm.js`, `sweet_alerts`, `toastr`, `ladda`, `blockui`, or `ccd80cc732201fa31f61` |
| AC-4 | That page does not contain `Alina Mcloughlin`, `Alina Mclourd`, `Type to search`, `All caught up!`, `dashboardpack.com`, or `build-in elements` |
| AC-5 | A request for `/themes/architectui.css` returns `text/css`. The file text says it is not a commercial template and does not define `.app-sidebar` |
| AC-6 | Theme choice 3 is the stored name `architectui`. The product does not register a page at `/analytics` or `/index.html` |

## 6. Protection rule

Future editors **MUST NOT**:

- Replace `/themes/architectui.css` with the commercial ArchitectUI stylesheet, or copy its `app-*` rules into `/apex.css`.
- Add the studied `<script` blocks, Ionicons, the pe-7s, Font Awesome, or Linearicons icon fonts, or a script from another host.
- Emit the studied sidebar, header, footer, layout customizer, or drawer in place of the Apex shell.
- Treat this file as an order to add an Analytics dashboard, a language switcher, a notification list, or a server-status drawer.
- Bump the product version because this requirement was added.

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| ArchitectUI | Theme choice 3. Stored name `architectui`. The OpenRbac color sheet, not the commercial template |
| Studied page | The ArchitectUI Analytics document recorded in section 2 |
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
| 2026-10-16 | Active 1.0.0 | The studied ArchitectUI Analytics page is recorded. Choice 3 stays the Apex color skin `architectui` |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
