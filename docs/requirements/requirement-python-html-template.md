**file**: docs/requirements/requirement-python-html-template.md
**Status**: Active (Version 1.2.0)
**Area**: python
**Key**: `requirement-python-html-template`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the HTML template engine. `WebApp` renders each page through class `HtmlTemplate`. The template syntax is the Vue 3.5 template syntax used by [RuoYi-FastAPI](https://github.com/insistence/RuoYi-FastAPI) `ruoyi-fastapi-frontend/vue3/web` (`vue` 3.5.26 in that project's `package.json`). Python renders the HTML on the server. The browser receives HTML. A document that shows a table checkbox also loads `/table-check.js`. The component tags are `requirement-html-element-plus`.

The reference is the layout of those Vue files. OpenRbac writes its own template files. It does not vendor `ruoyi-fastapi-frontend`. Labels stay in English. A field is shown only when the matching `Access` or `Catalog` method accepts it.

The same process serves the HTML and accepts the form posts. A `frontend/` directory, a `backend/` directory, `package.json`, and `vite.config.js` are not part of this product. Upstream `main.js`, `router/`, `store/`, `api/`, and `permission.js` stay in the reference project.

### 1.1 Human-facing

**In one sentence:** The page is a Vue-shaped template, and Python fills it before the browser sees it.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account opening a page | `admin` on `/users` |
| The other role | The template file | `templates/users.vue` |
| Not this file | The `el-*` markup and the cookie | `requirement-html-element-plus`, `requirement-web-interface` |

| Includes | Excludes |
|----------|----------|
| `{{ }}`, `v-if`, `v-else`, `v-else-if`, `v-show`, `v-for`, `v-bind`, `v-model`, components, and slots | A `<script>` block, a `<style>` block, and a Vue runtime |
| One shell: sidebar, navbar, and the page body | Tags view, a settings drawer, screen full, and header search |
| The pages in section 2 | Code generation, jobs, cache, files, plugins, the mobile app, a `frontend/` folder, and a JSON API for a browser application |

| Surface | What you open | What for |
|---------|---------------|----------|
| Template | `src/OpenRbac/templates/<page>.vue` | The Vue `<template>` for that page |
| Engine | `HtmlTemplate` in `html_template.py` | Render one template to HTML |
| Page | the URL printed by `serve` | That HTML, with the session cookie |

## 2. Pages

The reference column is a path under `ruoyi-fastapi-frontend/vue3/web/src/`. The record column owns the fields and the permission strings.

| Page | OpenRbac path | Reference | Record |
|------|---------------|-----------|--------|
| Sign in | `/login` | `views/login.vue` | `requirement-web-interface` |
| Home | `/` | `layout/index.vue` | signed-in name from `Access.describe` |
| Users | `/users` | `views/system/user/index.vue` | `requirement-rbac-users`. Layout: `requirement-html-user-management` |
| Roles | `/roles` | `views/system/role/index.vue` | `requirement-rbac-roles`. Layout: `requirement-html-role-management` |
| Menus | `/menus` | `views/system/menu/index.vue` | `requirement-rbac-menu`. The tree opens contracted |
| Departments | `/depts` | `views/system/dept/index.vue` | `requirement-rbac-departments`. Layout: `requirement-html-department-management` |
| Job Titles | `/job-titles` | `views/system/post/index.vue` | `requirement-rbac-job-titles`. Layout: `requirement-html-job-titles` |
| Parameters | `/configs` | `views/system/config/index.vue` | `requirement-rbac-parameters`. Layout: `requirement-html-parameter-management` |
| Dictionaries | `/dicts` | `views/system/dict/index.vue` | `requirement-rbac-dictionaries`. Layout: `requirement-html-dictionaries` |
| Notices | `/notices` | `views/system/notice/index.vue` | `requirement-rbac-notices` |
| Operation log | `/oper-log` | `views/monitor/operlog/index.vue` | `Catalog.oper_log`. Layout: `requirement-html-oper-log` |
| Login log | `/login-log` | `views/monitor/logininfor/index.vue` | `Catalog.login_log` (`requirement-rbac`). Layout: `requirement-html-login-log` |
| Online | `/online` | `views/monitor/online/index.vue` | `Catalog.online_list` (`requirement-web-interface`). Layout: `requirement-html-online` |
| Database | `/database` | none in that tree | `requirement-web-interface` |

`vue2/`, `mobile/`, `views/tool/`, `views/system/file/`, `views/system/plugin/`, `views/system/oauth/`, `views/monitor/job/`, `views/monitor/cache/`, and `views/monitor/server/` are not OpenRbac pages.

A list page has a toolbar and an `el-table`. The columns are the columns named by the record file. Add and edit use an `el-dialog` that contains an `el-form`. The form posts the same field names the current page posts. A button is omitted when the account lacks that permission. The sign-in page keeps the sqlite3 and mysql choice. It has no captcha image and no remember-me password cookie. `sys.account.captchaEnabled` and `sys.account.registerUser` stay stored parameters (`requirement-rbac-parameters`).

## 3. Normative rules

1. **Engine.** Class `HtmlTemplate` in `src/OpenRbac/html_template.py` **MUST** be the only renderer for a `WebApp` HTML body. `WebApp` **MUST** pass a dictionary of values. The template **MUST NOT** call `Access` or `Catalog`.
2. **File.** A template **MUST** be a UTF-8 file under `src/OpenRbac/templates/` with one `<template>` root. A `<script>` block and a `<style>` block **MUST** fail the render. The product **MUST NOT** copy a file from `ruoyi-fastapi-frontend` into that directory.
3. **Text.** `{{ name }}` **MUST** insert the value escaped as HTML text. A missing name **MUST** fail the render and the error **MUST** include that name. `v-html` **MUST** fail the render.
4. **Branches.** `v-if`, `v-else-if`, and `v-else` **MUST** choose one branch. `v-show` **MUST** keep the element and set a hidden state when the test is false. The test **MUST** be a name in the value dictionary, or `not` plus a name. Any other expression **MUST** fail the render.
5. **Repeat.** `v-for="row in rows"` and `v-for="(row, index) in rows"` **MUST** repeat the element. `rows` **MUST** be a list in the value dictionary. The names `row` and `index` exist only inside that repeat.
6. **Attributes.** `v-bind:name` and `:name` **MUST** set an attribute from a value. `v-model="field"` on an input, a select, or a textarea **MUST** set `name="field"` and the escaped `value`. The posted name **MUST** stay the name `WebApp` already reads.
7. **Events.** `v-on` and `@` **MUST** be accepted and **MUST NOT** emit a script. A submit control remains a form button. A navigation control remains a link.
8. **Components and slots.** A component tag **MUST** resolve through `requirement-html-element-plus` or through another template. An unknown tag **MUST** fail the render. The default slot and a named slot (`v-slot:name` or `#name`) **MUST** fill that slot.
9. **Shell.** A signed-in page **MUST** render inside the shell: `sidebar`, `navbar`, and `app-main`. The sidebar **MUST** list the destinations the account is allowed to open, using the menu rows from `requirement-rbac`. The sidebar **MUST NOT** wrap that list in `el-scrollbar`. Column height, and the ban on a function that resizes a scroll wrap, are `requirement-html-javascript`. The navbar **MUST** show the signed-in `user_name` and the sign-out control.
10. **Build.** The product **MUST NOT** run Node, Vite, or `vue-router` to produce the page. A template file **MUST NOT** contain a `<script` tag. A component fragment **MUST NOT** contain a `<script` tag. `render_document` **MUST** insert `<script src="/table-check.js"></script>` once, before `</body>`, when the rendered body contains `class="table-check`. Any other `<script` tag **MUST NOT** appear. A document with no table checkbox **MUST NOT** contain a `<script` tag.
11. **Tree.** Folder placement is `requirement-python-project-structure`. The repository **MUST NOT** contain a `frontend/` directory, a `backend/` directory, `package.json`, or `vite.config.js`. The same process **MUST** serve the HTML and accept the form posts. The product **MUST NOT** add a JSON API whose job is to feed a browser application.
12. **Reference files.** Every file under `src/OpenRbac/templates/` **MUST** contain one `<template>` root and **MUST NOT** contain `<script` or `<style`. The product **MUST NOT** copy `main.js`, `router/`, `store/`, `api/`, or `permission.js` from the reference project into this repository.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | `/users` HTML contains `el-table` and the column `user_name` |
| AC-2 | `{{ }}` of `a<b` is escaped, and `v-html` fails the render |
| AC-3 | A template with a `<script>` block fails the render |
| AC-4 | The operator users page omits the add dialog and omits clerk |
| AC-5 | A rendered document contains no `<script` tag, except `<script src="/table-check.js"></script>` once when the body shows a table checkbox. A component fragment contains no `<script` tag |
| AC-6 | `/login` offers sqlite3, the default file, and mysql, and has no captcha image |
| AC-7 | The shell template contains no `el-scrollbar` |
| AC-8 | The repository contains no `frontend/` directory, no `backend/` directory, no `package.json`, and no `vite.config.js` |
| AC-9 | Every file under `src/OpenRbac/templates/` contains `<template>` and contains neither `<script` nor `<style` |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Template | One `<template>` file under `src/OpenRbac/templates/` |
| Shell | Sidebar, navbar, and `app-main` |
| Reference | `ruoyi-fastapi-frontend/vue3/web` in insistence/RuoYi-FastAPI, Vue 3.5.26 |
| Value dictionary | The names `WebApp` passes into `HtmlTemplate` |

### UI infinite reflow

**Definition:** A UI infinite reflow is a layout cycle: the browser measures a box, writes a size that depends on that measurement, and measures again, and the sizes never settle. The usual shape is a cyclic percentage. A scroll wrap is `height: 100%` inside a parent whose height is the wrap’s own content (`min-height` only, or `height: auto`). The same cycle is started by a function that reads `scrollHeight`, `offsetHeight`, `clientHeight`, or `getBoundingClientRect` and writes `height`, `min-height`, or `style` back onto that wrap or its parent. The layout thread keeps re-entering. The page, and often the whole desktop, stops answering. Pain PP-A-31.

**Human daily-life explanation:** A UI infinite reflow is a tailor who measures the cloth, cuts the table to match the cloth, then measures the cloth again because the table changed. The tape never stops. The room fills with the sound of the tape and nobody can open the door.

**Daily-life example:** A side column says “I am as tall as my parent,” and the parent says “I am as tall as the side column.” The painter measures forever. The screen locks.

### UI sidebar

**Definition:** ui-sidebar is the production UI label whose English UI term is Sidebar. The actual UI function is the side column that lists destinations beside the page body. The column’s height is a definite viewport length in the stylesheet (`100vh` or a stated length). Overflow scrolls on that column. The column is not a child whose `height: 100%` is resolved against a parent that sizes itself from the column.

**Human daily-life explanation:** A ui-sidebar is the narrow list on the side of the page that says where you can go. The list has a fixed height, like a door frame. Extra names scroll inside the frame. The frame does not grow because the list grew.

**Daily-life example:** A restaurant menu is clipped to the left of the table. You slide the menu. The table does not get taller each time you slide it.

### UI scrollbar

**Definition:** ui-scrollbar is the production UI label whose English UI term is Scrollbar. The actual UI function is the control that shows more content than fits and lets the reader move through it. The wrap’s size is only in the stylesheet. Changing a scrollable wrap dynamically is forbidden. A function must not read `scrollHeight`, `offsetHeight`, `clientHeight`, or `getBoundingClientRect` and write `height`, `min-height`, or inline style onto that wrap or its parent. That write is a UI infinite reflow.

**Human daily-life explanation:** A ui-scrollbar is the slider that shows there is more to read. The window size is printed on the plan. Nobody comes back with a tape measure and rebuilds the window because the paper was long. Rebuilding the window from the paper is how the room locks.

**Daily-life example:** A long grocery list sits in a fixed window with a slider. A helper who stretches the window to the length of the list, then measures again, never finishes. That helper must not be hired.

### Python web server

**Definition:** A **Python web server** is a **software-development** product whose primary operator surface is a **long-running HTTP process** plus a **browser (or other HTTP) client**. The checkout ship tree uses **`backend/`** for the Python server and **`frontend/`** for the static or client UI. It **MUST NOT** use **`src/`** as the required package root. It is **not** a python-cli and **not** a python-pypi-cli.

**Human daily-life explanation:** A python-web-server is a long-running HTTP program plus a browser client, with `backend/` and `frontend/` trees, not `src/` as the package root. It stays open.

**Daily-life example:** A diner that stays open: kitchen in the back, menu and seating in the front, not a handheld calculator you put away.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Python renderer for the Vue 3.5 template subset |
| 2026-10-14 | Active 1.0.1 | The shell does not wrap the menu in `el-scrollbar` |
| 2026-10-14 | Active 1.1.0 | Pages stay embedded. No frontend tree, no client build files, no copied client runtime |
| 2026-10-14 | Active 1.1.1 | The job title page is `/job-titles` |
| 2026-10-14 | Active 1.1.2 | The users page layout is `requirement-html-user-management` |
| 2026-10-14 | Active 1.1.3 | The job titles page layout is `requirement-html-job-titles` |
| 2026-10-14 | Active 1.1.4 | The departments page layout is `requirement-html-department-management` |
| 2026-10-14 | Active 1.1.5 | The dictionaries page layout is `requirement-html-dictionaries` |
| 2026-10-14 | Active 1.1.7 | The login log page layout is `requirement-html-login-log` |
| 2026-10-14 | Active 1.1.8 | The online page layout is `requirement-html-online` |
| 2026-10-14 | Active 1.1.6 | The roles page layout is `requirement-html-role-management` |
| 2026-10-14 | Active 1.1.6 | The parameters page layout is `requirement-html-parameter-management` |
| 2026-10-15 | Active 1.1.9 | The operation log table layout is `requirement-html-oper-log` |
| 2026-10-16 | Active 1.2.0 | A document with a table checkbox loads `/table-check.js`. A template file still cannot contain a script block |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
