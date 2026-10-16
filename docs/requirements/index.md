# Requirements index

**Product:** OpenRbac (Python CLI — text menu and local web pages for online RBAC)
**Workspace state:** Specialized product law; **software-development** class; **pip/local package** install.
**Product version:** **1.0.5** (`pyproject.toml`, `src/OpenRbac/__init__.py`, root `README.md`)
**Updated:** 2026-10-16

| ID / key | Title | Area | Status | Path | Updated |
|----------|-------|------|--------|------|---------|
| requirement-class-software-dev | Software-development class law + residual stack (Python, setuptools) | class | Active | `requirement-class-software-dev.md` | 2026-10-04 |
| requirement-domain-openrbac | Domain surface: online RBAC and centralized configuration. Sign-in before the menu. No Vue frontend folder | domain | Active | `requirement-domain-openrbac.md` | 2026-10-14 |
| requirement-domain-videojoin | Retired welcome-line domain | domain | Retired | `requirement-domain-videojoin.md` | 2026-10-11 |
| requirement-rbac | RBAC system map, permissions, data scope 1–4, seed on an empty database, protected rows. The operation log table is `requirement-html-oper-log` | domain | Active | `requirement-rbac.md` | 2026-10-15 |
| requirement-rbac-users | User list with optional filters, add, edit, remove, password reset, a status switch, and csv import and export. Edit can replace job titles and roles | domain | Active | `requirement-rbac-users.md` | 2026-10-14 |
| requirement-rbac-roles | Role list, menu grant, and page add, edit, remove, status, and export | domain | Active | `requirement-rbac-roles.md` | 2026-10-14 |
| requirement-rbac-menu | Menu list, add, and page edit, remove, and save sort. Types M, C, and F. The page opens contracted. The check-all checkbox checks the rows in that table | domain | Active | `requirement-rbac-menu.md` | 2026-10-16 |
| requirement-rbac-departments | Department list and add. Ancestors for scope 4 | domain | Active | `requirement-rbac-departments.md` | 2026-10-14 |
| requirement-rbac-job-titles | Job title list and add. A title grants no permission. User edit may replace one user's titles | domain | Active | `requirement-rbac-job-titles.md` | 2026-10-14 |
| requirement-rbac-parameters | Parameter list, change, and add. Initial password key | domain | Active | `requirement-rbac-parameters.md` | 2026-10-14 |
| requirement-rbac-dictionaries | Dictionary values under a seeded type | domain | Active | `requirement-rbac-dictionaries.md` | 2026-10-14 |
| requirement-rbac-notices | Notice list and publish. Types 1 and 2 | domain | Active | `requirement-rbac-notices.md` | 2026-10-14 |
| requirement-database | sqlite3 default file and mysql tables, seed-once, auto-init | domain | Active | `requirement-database.md` | 2026-10-14 |
| requirement-environment | OPENRBAC_* names, mode-0600 file, loopback bind. The default theme is apex | domain | Active | `requirement-environment.md` | 2026-10-16 |
| requirement-local-login | Encrypted local sign-in and the Exit logout question | domain | Active | `requirement-local-login.md` | 2026-10-11 |
| requirement-web-interface | Local HTML site, cookie, CSRF, shared service. Pages are the embedded templates. The stored theme selects the Apex color skin. Sidebar is a 100vh scrollport. An image is a same-origin file unless a requirement specifies an inline image. The image policy allows data:. `script-src` is `'self'` for `/table-check.js`. The document body font size is `requirement-html-body-font` | domain | Active | `requirement-web-interface.md` | 2026-10-16 |
| requirement-python-about | About page: identity, host check, star box. No `--json` | python | Active | `requirement-python-about.md` | 2026-10-14 |
| requirement-video-ffmpeg-pipeline | Retired. No encoder, no concat, no media publish | video | Retired | `requirement-video-ffmpeg-pipeline.md` | 2026-10-11 |
| requirement-python-cli-interface | CLI entry, typed verbs, saved sign-in or question, then menu. `theme` chooses apex or one of ten skins | python | Active | `requirement-python-cli-interface.md` | 2026-10-16 |
| requirement-python-cli-logging | ChronicleLogger construct in `def main`; no passwords in the log | python | Active | `requirement-python-cli-logging.md` | 2026-10-11 |
| requirement-python-tui | Text menu rows 1 rbac, 2 server, 3 system-log, 6 self-management, 7 language, 9 Exit. Server row 24 offers eleven skins. An invalid stored name still lists them | python | Active | `requirement-python-tui.md` | 2026-10-16 |
| requirement-python-cli-language | Menu language: front row 7, codes 71–83, leaf `~/.local/OpenRbac/language` | python | Active | `requirement-python-cli-language.md` | 2026-10-14 |
| requirement-python-oop | Class map, including Desk, Access, WebApp, and HtmlTemplate | python | Active | `requirement-python-oop.md` | 2026-10-14 |
| requirement-python-html-template | Embedded HTML templates for the Vue 3.5 subset. No Vite tree, no frontend folder, no el-scrollbar in the shell. A document with a table checkbox loads `/table-check.js`. The operation log table is `requirement-html-oper-log` | python | Active | `requirement-python-html-template.md` | 2026-10-16 |
| requirement-html-element-plus | HTML components. The tag names stay. They emit Apex shell classes. A RuoYi tree is a nested list with a switch. User status is an on/off switch. Role status is `requirement-html-role-management`. The department page expands and contracts apart from that diagram. The users edit dialog floats over the users page and opens that tree and a job-title dropdown without a script. A checkbox cell uses `table-check-col`. The body size is `requirement-html-body-font` | python | Active | `requirement-html-element-plus.md` | 2026-10-16 |
| requirement-html-theme | Stored theme selects the Apex color skin. Choice 1 is apex. Ten more skins share that shell. Brand controls follow the skin primary. Apex primary is `#1ab394`. Admindek primary is the original indigo `#4f46e5`. The document body font size is `requirement-html-body-font`. A table checkbox loads `/table-check.js`. The operation log table is `requirement-html-oper-log` | python | Active | `requirement-html-theme.md` | 2026-10-16 |
| requirement-html-admindek | Studied Admindek Analytics shell. Choice 2 stays the Apex color skin `admindek`. The original indigo sheet paints brand controls. The studied ocean blue stays out. The commercial page's scripts, fonts, icon fonts, customizer, command palette, and DashboardPack links stay off the product | python | Active | `requirement-html-admindek.md` | 2026-10-16 |
| requirement-html-architectui | Studied ArchitectUI Analytics shell. Choice 3 stays the Apex color skin `architectui`. The commercial page's scripts, Ionicons, icon fonts, layout customizer, drawer, and DashboardPack links stay off the product | python | Active | `requirement-html-architectui.md` | 2026-10-16 |
| requirement-html-adminty | Studied Adminty default shell. Choice 4 stays the Apex color skin `adminty`. The collected Bootstrap, Google Fonts, icon fonts, jQuery, charts, and Adminty scripts stay off the product | python | Active | `requirement-html-adminty.md` | 2026-10-16 |
| requirement-html-body-font | Document body uses the small font size, 13px, in `/apex.css` | python | Active | `requirement-html-body-font.md` | 2026-10-16 |
| requirement-html-date-range | Search date range: two native date inputs on one line, names `begin` and `end`, with an arrow and no From or To label. Users, roles, parameters, and dictionaries title it Created. The login log titles it Login time. The layout is `/apex.css` | python | Active | `requirement-html-date-range.md` | 2026-10-16 |
| requirement-html-javascript | Sidebar scrollport on `.main-sidebar` in `/apex.css`. A function must not resize a scroll wrap. `/table-check.js` checks the row boxes in one table | python | Active | `requirement-html-javascript.md` | 2026-10-16 |
| requirement-html-user-management | Users page: organization tree, search, toolbar of five actions, account table, and an on/off status switch at `/users`. The User cell is a circle of two initials, the account name, and @login. Administrator shows AD. The table does not show a User id column. The first header is a check-all checkbox when edit or remove is allowed, and it checks the rows in that table. The Created search is `requirement-html-date-range`. The edit dialog floats over that page. Edit chooses one department from a floating tree and job titles from a dropdown. A checked job title uses the skin primary | python | Active | `requirement-html-user-management.md` | 2026-10-16 |
| requirement-html-department-management | Departments page: a tree that expands and contracts at `/depts`. Every skin paints it from `/apex.css` | python | Active | `requirement-html-department-management.md` | 2026-10-16 |
| requirement-html-job-titles | Job Titles page: search, add, six-column table, status tag, and count line at `/job-titles` | python | Active | `requirement-html-job-titles.md` | 2026-10-16 |
| requirement-html-parameter-management | Parameters page: search, change of the value, eight-column table, built-in tag, and count line at `/configs`. The first header is a check-all checkbox when edit is allowed, and it checks the rows in that table. The Created search is `requirement-html-date-range`. Add, remove, export, and cache refresh stay off the page | python | Active | `requirement-html-parameter-management.md` | 2026-10-16 |
| requirement-html-dictionaries | Dictionaries page: search, add a value, six-column type table, status tag, and count line at `/dicts`. The Created search is `requirement-html-date-range`. The studied dialog `修改类型` stays off the page | python | Active | `requirement-html-dictionaries.md` | 2026-10-16 |
| requirement-html-oper-log | Operation log table: headers Operation ID, Business Type, and Operation Time at `/oper-log`. The table is the shared Apex table. Stored columns and the text report keep `oper_id`, `business_type`, and `oper_time` | python | Active | `requirement-html-oper-log.md` | 2026-10-16 |
| requirement-html-login-log | Login log page: search, nine-column attempt table, status tag, and count line at `/login-log`. The Login time search is `requirement-html-date-range`. Delete, clear, unlock, and export stay off the page | python | Active | `requirement-html-login-log.md` | 2026-10-16 |
| requirement-html-online | Online page: search, seven-column session table, Online tag, count line, and a row force-logout at `/online`. Department, browser, and a batch logout stay off the page | python | Active | `requirement-html-online.md` | 2026-10-16 |
| requirement-html-role-management | Roles page: search, toolbar of four actions, data-scope tags, and a status switch at `/roles`. The first header is a check-all checkbox when edit or remove is allowed, and it checks the rows in that table. The Created search is `requirement-html-date-range`. On is Enabled and stores 0. Off is Disabled and stores 1 | python | Active | `requirement-html-role-management.md` | 2026-10-16 |
| requirement-python-coding-style | Python style; one class per module; end state is the class map | python | Active | `requirement-python-coding-style.md` | 2026-10-04 |
| requirement-python-packaging | `pyproject.toml` / version / console script `open-rbac` | python | Active | `requirement-python-packaging.md` | 2026-10-14 |
| requirement-python-build-script | Maintainer `./build.sh` commands, including test-install | python | Active | `requirement-python-build-script.md` | 2026-10-14 |
| requirement-python-project-structure | Repository and `src/OpenRbac` layout. Pages are templates. No frontend or backend split | python | Active | `requirement-python-project-structure.md` | 2026-10-14 |
| requirement-python-readme | Root user document: sections, badges, absolute screenshot URLs | python | Active | `requirement-python-readme.md` | 2026-10-14 |
| requirement-python-error-handling | Fail-closed errors; console sentences stay | python | Active | `requirement-python-error-handling.md` | 2026-10-04 |
| requirement-runtime-prerequisites | sqlite3 by default; mysql and PyMySQL when chosen; ChronicleLogger; no root auto-install | runtime | Active | `requirement-runtime-prerequisites.md` | 2026-10-11 |

## Intentionally absent (by design)

| Surface | Status on OpenRbac |
|---------|----------------------|
| Shell online install / `curl\|sh` | **Absent** |
| Type 1 sudoers / root elevation inside the program | **Absent** |
| Code generation, AI, plugins, jobs, Redis, Vue or Vite npm build | **Absent** for 1.0.5 |
| A Vue `frontend/` folder and a JSON API for a browser application | **Absent**. Pages are `src/OpenRbac/templates/`. The reference Vue tree stays in the other project |
| Element Plus JavaScript runtime | **Absent**. HTML components are `requirement-html-element-plus` |
| Second Active `requirement-domain-*` | **Forbidden** while `requirement-domain-openrbac` is Active |
| `hello`, `join`, `list-videos`, FFmpeg | **Absent** |
| `requirement-python-json-output` | **Absent**. No `--json` |

**Install mode:** **pip / local package** (`open-rbac` console script).

**Logger:** required (`ChronicleLogger>=1.3.1`). `def main` in `src/OpenRbac/cli.py` writes `ChronicleLogger(...)`.

**Database:** sqlite3 by default, file `openrbac.sqlite3`. mysql through `PyMySQL>=1.1.0` when `OPENRBAC_DB_ENGINE=mysql`. Product mysql schema `openrbac`. mysql tests use `openrbac_test`.

**Rules for agents:**

1. Treat rows above as the live product-law inventory for OpenRbac.
2. Do not invent additional `requirement-*.md` paths without a registry row in the same change.
3. Product source comments cite only these live requirement files.
4. Keep Status and Path in sync with each file’s header.
5. Exactly one Active `requirement-domain-*` (`requirement-domain-openrbac`).
6. Do not write `ruoyi_db` or `ry`.

When adding a requirement: append a row, create the file under `docs/requirements/`, keep Status in sync with the file header.
