**file**: docs/requirements/requirement-html-adminty.md
**Status**: Active (Version 1.0.0)
**Area**: python
**Key**: `requirement-html-adminty`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file records the studied Adminty page and collects every stylesheet and script that page loads. OpenRbac already stores the name `adminty` as theme choice 4. The listener still sends the Apex shell, `/apex.css`, and `/themes/adminty.css`. This file says which pieces of that studied page stay out of the response.

The eleven names, the shared shell, and the ban on a commercial stylesheet stay on `requirement-html-theme`. The one allowed script stays on `requirement-html-javascript`. The body size stays on `requirement-html-body-font`. The menu row and the verb stay on `requirement-python-tui` and `requirement-python-cli-interface`. The Admindek study stays on `requirement-html-admindek`. The ArchitectUI study stays on `requirement-html-architectui`.

### 1.1 Human-facing

**In one sentence:** Choosing Adminty paints the same OpenRbac pages with the Adminty color sheet. It does not load the Adminty dashboard template or the stylesheets and scripts collected below.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person who picks theme choice 4 | `open-rbac theme`, then `4` |
| The other role | The page the browser paints | `/apex.css` and `/themes/adminty.css` |
| Not this file | The permission check and the menu groups | `requirement-rbac` |

| Includes | Excludes |
|----------|----------|
| The studied Adminty shell, and the full list of its stylesheets and scripts | A second frontend folder or a twelfth theme name |
| The original color sheet `/themes/adminty.css` on the Apex shell | Bootstrap, Google Fonts, icon fonts, jQuery, Chart.js, amCharts, and the Adminty scripts |
| The existing OpenRbac menu, forms, and posts | The studied search, notifications, chat, profile menu, and empty Navigation list |

| Surface | What you open | What for |
|---------|---------------|----------|
| Theme menu | Server row 24, or `open-rbac theme` | Store `adminty` |
| Next page | The listener | Apex markup plus `/themes/adminty.css` |
| Studied page | Adminty default dashboard | The shell, stylesheets, and scripts this file records and does not ship |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Pick Adminty | The next HTML page uses the Adminty color sheet on the same shell as Apex. The studied dashboard markup, stylesheets, and scripts stay off that page. | `open-rbac theme`, then `4` |

## 2. The studied page

The studied document is one HTML page. `html` has `lang="en"`. Its title is `Adminty - Premium Admin Template by Colorlib`. The description and the author are both `#`. The keywords name Admin, Responsive, Landing, Bootstrap, App, Template, Mobile, iOS, Android, apple, and creative app. The favicon is `../assets/images/favicon.ico`. `body` has `themebg-pattern="pattern4"`. The content node `div.main-body` is empty. The sidebar caption is `Navigation`. The only menu row is Dashboard, and its only child is Default at `index.html`.

| Piece in the studied document | OpenRbac |
|-------------------------------|----------|
| `title` `Adminty - Premium Admin Template by Colorlib` | Not a product page title. Signed-in pages keep their own titles |
| Favicon `../assets/images/favicon.ico`, description `#`, author `#` | Omitted |
| `body` attribute `themebg-pattern="pattern4"` | Omitted. The body is the Apex document |
| `#pcoded.pcoded.iscollapsed` with `nav-type="st6"`, `theme-layout="vertical"`, `vertical-placement="left"`, `vertical-layout="wide"`, `pcoded-device-type="desktop"`, `vertical-nav-type="expanded"`, `vertical-effect="shrink"`, `vnavigation-view="view1"`, `fream-type="theme1"`, `sidebar-img="false"`, `sidebar-img-type="img1"`, `layout-type="light"` | Omitted |
| `div.pcoded-overlay-box` and `div.pcoded-container.navbar-wrapper` | Omitted |
| `nav.navbar.header-navbar.pcoded-header` with `header-theme="theme1"` and `pcoded-header-position="fixed"` | Omitted. The top band stays `main-header` |
| Logo `../assets/images/logo.png`, alt `Theme-Logo`, address `index.html`. Mobile controls `#mobile-collapse` and `.mobile-options` | Omitted |
| Search input, placeholder `Enter Keyword` | Omitted |
| Full-screen control `onclick="javascript:toggleFullScreen()"` with `feather icon-maximize` | Omitted |
| Notification bell, badge `5`, heading Notifications, badge New. Rows `John Doe`, `Joseph William`, and `Sara Soudein`, each with lorem text and `30 minutes ago` | Omitted. They are demo copy |
| Chat control `displayChatbox`, badge `3` | Omitted |
| Account picture `../assets/images/avatar-4.jpg` and the name `John Doe`. Links Settings, Profile `user-profile.html`, My Messages `email-inbox.html`, Lock Screen `auth-lock-screen.html`, and Logout `auth-normal-sign-in.html` | Omitted. The shell shows the signed-in account |
| `#sidebar.users.p-chat-user.showChat`. Search placeholder `Search Friend`. Names `Josephin Doe`, `Lary Doe`, `Alice`, `Alia`, and `Suzen` | Omitted |
| Inner chat with `Josephin Doe`, the sentence `I'm just looking around. Will you tell me something about yourself?`, time `8:20 a.m.`, and placeholder `Share Your Thoughts` | Omitted |
| Slim-scroll bar painted `rgb(27, 139, 249)` | Studied only. `/themes/adminty.css` keeps its own colors |
| `nav.pcoded-navbar` with `navbar-theme="theme1"`, `active-item-theme="theme1"`, `sub-item-theme="theme2"`, `active-item-style="style0"`, `pcoded-navbar-position="fixed"`, and `mCustomScrollbar` | Omitted. The side column stays `aside.main-sidebar` |
| Caption `Navigation`. Parent Dashboard with `feather icon-home`. Child Default, `href="index.html"`, class `active`. Comment groups Layouts, Widgets, UI Components, Forms, Tables, Charts & Maps, Pages, Applications, Extensions, Other, and Support are empty | Omitted. The menu stays the OpenRbac groups |
| `div.pcoded-content` > `div.pcoded-inner-content` > `div.main-body`, empty. The container uses an inline `margin-top: 58px` | Omitted. Page bodies stay the existing templates |
| Icon classes `feather`, `icofont`, `themify`, and Font Awesome | Omitted. The product does not ship those icon fonts |

### 2.1 Stylesheets collected from the studied page

The studied head loads these sheets, in this order. An `adminty` OpenRbac page loads none of them.

| Order | Studied stylesheet |
|------:|--------------------|
| 1 | `https://fonts.googleapis.com` preconnect, and `https://fonts.gstatic.com` preconnect |
| 2 | `https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;800&display=swap` |
| 3 | `../plugins/bootstrap/dist/css/bootstrap.min.css` |
| 4 | `../assets/icon/themify-icons/themify-icons.css` |
| 5 | `../assets/icon/icofont/css/icofont.css` |
| 6 | `../assets/icon/feather/css/feather.css` |
| 7 | `../plugins/@fortawesome/fontawesome-free/css/all.min.css` |
| 8 | `../assets/css/theme/style.min.css` |
| 9 | `../assets/css/jquery.mCustomScrollbar.css` |

The product page links `/apex.css` and `/themes/adminty.css` only.

### 2.2 Scripts collected from the studied page

The studied body ends with these scripts, in this order. An `adminty` OpenRbac page loads none of them. The inline call `toggleFullScreen()` is in the same set.

| Order | Studied script |
|------:|----------------|
| 1 | `../plugins/jquery/dist/jquery.min.js` |
| 2 | `../plugins/jquery-ui/dist/jquery-ui.min.js` |
| 3 | `../plugins/@popperjs/core/dist/umd/popper.min.js` |
| 4 | `../plugins/bootstrap/dist/js/bootstrap.min.js` |
| 5 | `../plugins/jquery-slimscroll/jquery.slimscroll.js` |
| 6 | `../plugins/chart.js/dist/chart.umd.js` |
| 7 | `../assets/pages/widget/amchart/amcharts.js` |
| 8 | `../assets/pages/widget/amchart/serial.js` |
| 9 | `../assets/pages/widget/amchart/light.js` |
| 10 | `../assets/js/pcoded.min.js` |
| 11 | `../assets/js/theme-persistence.js` |
| 12 | `../assets/js/vartical-layout.min.js` |
| 13 | `../assets/js/jquery.mCustomScrollbar.concat.min.js` |
| 14 | `../assets/js/script.js` |
| 15 | `../assets/js/SmoothScroll.js` |
| 16 | `../assets/pages/dashboard/custom-dashboard.js` |
| 17 | Inline `toggleFullScreen()` on the maximize control |

A table checkbox still loads `/table-check.js` once. A page with no table checkbox has no `<script` tag.

The studied slim-scroll color is `#1b8bf9`. The product sheet does not take that value from this page. Its sidebar is `#0f3d3e` and its primary is `#0f766e`.

## 3. What the name means here

`adminty` remains choice 4. The label remains `Adminty`. Empty and choice 1 remain `apex`. This file does not add a name and does not rename one.

A page whose stored theme is `adminty` links `/apex.css` and `/themes/adminty.css`. The markup is the Apex shell in `requirement-html-theme`: `wrapper`, `main-sidebar`, `content-wrapper`, `main-header`, `content`, `nav-sidebar`, `nav-link active`, `table table-bordered table-striped`, `form-control`, and `btn btn-primary`. The signed-in menu stays Home, Access, Catalog, Audit, and Setup, filtered by permission. Form `method`, `action`, and field `name` values stay on the page that owns them.

`/themes/adminty.css` is `src/OpenRbac/element_plus/themes/adminty.css`. The listener serves it as `text/css`. The file sets shell colors for that name. Its comment states that it is not a commercial template and that layout stays in `/apex.css`. Layout stays in `src/OpenRbac/element_plus/apex.css`.

### 3.1 Implementation notes (this project)

| Item | Value |
|------|--------|
| Product | OpenRbac. Command `open-rbac` |
| Stored theme | `adminty`. Menu label `Adminty`. Choice `4` |
| Layout sheet | `src/OpenRbac/element_plus/apex.css`, URL `/apex.css` |
| Color sheet | `src/OpenRbac/element_plus/themes/adminty.css`, URL `/themes/adminty.css` |
| Shell | The Apex classes in `requirement-html-theme`. Not `pcoded`, `pcoded-header`, or `pcoded-navbar` |
| Collected stylesheets | The nine rows in section 2.1. None is a product URL |
| Collected scripts | The seventeen rows in section 2.2. None is a product URL |
| Product version | Unchanged by this file |

## 4. Normative rules

1. **Name.** Choice 4 **MUST** stay the stored name `adminty` and the label `Adminty`. This file **MUST NOT** add a theme name and **MUST NOT** remove one.
2. **Shell.** An `adminty` page **MUST** emit the Apex shell in `requirement-html-theme`. It **MUST NOT** emit `pcoded`, `pcoded-header`, `pcoded-navbar`, `pcoded-container`, `pcoded-content`, `main-body`, `showChat`, `themebg-pattern`, or `header-theme`.
3. **Stylesheets.** The page **MUST** link `/apex.css` and `/themes/adminty.css` from this host. It **MUST NOT** link any stylesheet in section 2.1, including `fonts.googleapis.com`, `fonts.gstatic.com`, `bootstrap.min.css`, `themify-icons.css`, `icofont.css`, `feather.css`, `fontawesome-free`, `style.min.css`, or `jquery.mCustomScrollbar.css`. It **MUST NOT** link `/element-plus.css`, `/openrbac.css`, or `/adminlte.css`.
4. **Color sheet.** `/themes/adminty.css` **MUST** remain the original OpenRbac color sheet for that name. It **MUST NOT** be replaced by `style.min.css` or by Bootstrap. The studied `#1b8bf9` **MUST NOT** be copied in as that file. The sheet **MUST NOT** define `.pcoded`.
5. **Script.** The page **MUST NOT** include any script in section 2.2, including jQuery, jQuery UI, Popper, Bootstrap JavaScript, slimScroll, Chart.js, amCharts, `pcoded.min.js`, `theme-persistence.js`, `vartical-layout.min.js`, `script.js`, `SmoothScroll.js`, `custom-dashboard.js`, or `toggleFullScreen`. A table checkbox still loads `/table-check.js` once, as `requirement-html-javascript` requires. A page with no table checkbox **MUST NOT** include a `<script` tag.
6. **Menu and routes.** The signed-in menu **MUST** stay the OpenRbac groups. The studied caption `Navigation` with Dashboard and Default **MUST NOT** replace that menu. This file **MUST NOT** add a route whose path is `/index.html`, `/user-profile.html`, `/email-inbox.html`, `/auth-lock-screen.html`, or `/auth-normal-sign-in.html`.
7. **Demo chrome.** The response **MUST NOT** contain `John Doe`, `Joseph William`, `Sara Soudein`, `Josephin Doe`, `Lary Doe`, `Enter Keyword`, `Search Friend`, `Share Your Thoughts`, `Premium Admin Template by Colorlib`, or `I'm just looking around`.
8. **Same posts.** An `adminty` page **MUST** keep the same form names and permissions as the other ten skins.
9. **Neighbors.** Users, roles, menus, departments, and job titles stay in Access. Parameters, dictionaries, and notices stay in Catalog. The operation log, the login log, and online stay in Audit. The studied notifications, chat, lock screen, and profile menu **MUST NOT** become menus.

## 5. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | An `adminty` sign-in page links `/apex.css` and `/themes/adminty.css`, uses `form-control` and `btn btn-primary`, and does not link `/element-plus.css` |
| AC-2 | That page does not contain `pcoded`, `pcoded-navbar`, `pcoded-header`, `main-body`, `showChat`, or `themebg-pattern` |
| AC-3 | That page does not contain `jquery.min.js`, `bootstrap.min.css`, `bootstrap.min.js`, `style.min.css`, `pcoded.min.js`, `theme-persistence.js`, `fonts.googleapis.com`, `themify-icons`, `icofont`, or `feather.css` |
| AC-4 | That page does not contain `John Doe`, `Josephin Doe`, `Enter Keyword`, `Search Friend`, or `Premium Admin Template by Colorlib` |
| AC-5 | A request for `/themes/adminty.css` returns `text/css`. The file text says it is not a commercial template and does not define `.pcoded` |
| AC-6 | Theme choice 4 is the stored name `adminty`. The product does not register a page at `/index.html` |

## 6. Protection rule

Future editors **MUST NOT**:

- Replace `/themes/adminty.css` with the commercial Adminty stylesheet, or copy its `pcoded` rules into `/apex.css`.
- Add any stylesheet from section 2.1 or any script from section 2.2, including the Google font, Bootstrap, jQuery, Chart.js, amCharts, or the icon fonts.
- Emit the studied header, sidebar, chat, or empty `main-body` in place of the Apex shell.
- Treat this file as an order to add a Default dashboard, a friend chat, a notification list, or a lock screen.
- Bump the product version because this requirement was added.

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Adminty | Theme choice 4. Stored name `adminty`. The OpenRbac color sheet, not the commercial template |
| Studied page | The Adminty document recorded in section 2 |
| Collected stylesheet | One row of section 2.1. It is recorded here and is not a product URL |
| Collected script | One row of section 2.2. It is recorded here and is not a product URL |
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
| 2026-10-16 | Active 1.0.0 | The studied Adminty page is recorded. Its nine stylesheets and seventeen scripts are collected here. Choice 4 stays the Apex color skin `adminty` |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
