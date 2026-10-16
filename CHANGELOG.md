# CHANGELOG

All notable changes to **OpenRbac** are documented here.
Version SSOT: `pyproject.toml` + `src/OpenRbac/__init__.__version__`.

## [1.0.5] - 2026-10-16

### Added

- Server row 24 is `theme`. `open-rbac theme` offers eleven skins. Choice 1 is Apex. Enter selects Apex. The other choices are Admindek, ArchitectUI, Adminty, Analytic, Cryptocurrency, Directory, Finance SaaS, Fiori, Hospital, and Kero. Every skin uses the Apex shell and `/apex.css`, plus `/themes/<name>.css` for its colors. Those color sheets are original to OpenRbac. `vue3` and `adminlte` are not stored theme names. Empty means Apex. The choice is stored in the mode-0600 settings file and does not open the database. A later write is the skin of the next page.

### Changed

- The users page is an organization tree, a search row, and an account table. The User cell shows a circle of two initials, then the account name and @login. Administrator shows AD. Search filters login name, phone, status, and created dates. The toolbar is Add, Edit, Remove, Import, and Export. Edit and Remove use the chosen account. Import reads a csv of accounts. Export downloads that csv. A folder marks a parent department and a circle marks a leaf. Every button has an icon. Each icon is a file at `/icons/*.svg`. The stylesheets do not embed a data image. The page does not load a script or a Font Awesome file.
- An HTML page allows an image from this host and an inline `data:` image (`img-src 'self' data:`). The policy still has no `script-src`. A product image is a separate file unless a requirement specifies an inline image. The users icons stay files. The Element Plus stylesheet keeps the images already written in that file.
- The organization tree is nested. Each department has a switch in front of its icon. A parent shows a minus box. A leaf shows an elbow. A dotted line joins a node to its parent and stops on the last sibling. That shape is section 5 of `requirement-html-element-plus`, and the project skill `html-tree` follows it.
- User status on the users page is an on/off switch. On is Enabled and stores 0. Off is Disabled and stores 1. The table switch posts the other status. The edit form uses the same switch. User 1 stays enabled. Search still uses the words All, Enabled, and Disabled.
- The users edit dialog floats over the users page. Name, phone, email, sex, remark, roles, and status are on that form. Login name is shown and is not posted. Job title is a dropdown that can hold several titles, shown as tags. Department opens a floating tree and accepts one department. The tree is the same nested list as the organization pane, drawn expanded. The department page keeps its own expand and collapse. The dialog does not use a script. `user-add` still attaches no job title. Changing status does not clear job titles or roles.
- The product name is OpenRbac. The console script is `open-rbac`. The home folder is `~/.local/OpenRbac`. Environment names start with `OPENRBAC_`. The sqlite file is `openrbac.sqlite3`. The mysql database and account are `openrbac`.
- The front board is 1 rbac, 2 server, 3 system-log, 6 self-management, 7 language, and 9 Exit. Server holds setup 21, audit 22, and serve 23. Rbac children are 11–19 and 110–113. Setup children are 211–218. Audit children are 221–224. Self-management children are 62–67. Language codes are 71–83.
- The README pictures are a new capture of that menu, the sign-in question, and the Exit question.
- A job title is `sys_job_title`. The page is `/job-titles`. The verbs are `job-title-list` and `job-title-add`. The list label is Job Titles. The add label is add a job titles.
- Menu Management at `/menus` opens with every branch contracted. `Expand/Collapse` opens every branch. A caret opens that branch only. A name or visibility search with no `closed` value still shows the match.
- Users, roles, menus, and parameters use a centered checkbox column. The header box checks or unchecks every row box in that table. The script is `/table-check.js` from this host. The header box is not posted. Edit, Remove, and Change still open the first checked row. The page does not delete many rows. A page with no checkbox column still has no script. HTML allows `script-src 'self'` and does not allow an inline script or a script from another host.

## [1.0.4] - 2026-10-11

### Added

- A successful terminal sign-in stores the account and password in encrypted files under the home folder. A later start uses them when the login still works and does not ask again. A failed restore removes the saved sign-in. The web sign-in page does not write those files.

### Changed

- Row 9 Exit asks before it leaves. Enter or y logs out and removes the saved sign-in. n leaves and keeps it. Esc stays on the menu. End of input still leaves without the question.
- The sign-in question keeps its instructions, including the sqlite3 file, above the account name and the password.
- The README pictures show the current menu: version 1.0.4, no session row, the sign-in question, and the Exit question.

## [1.0.3] - 2026-10-11

### Changed

- A terminal with no arguments uses sqlite3 and `~/.local/OpenRbac/openrbac.sqlite3`. It asks for the account and the password, and it does not ask for the engine or the file path.
- Enter on `open-rbac db-engine` and on setup row 78 selects sqlite3 and that default file. Choice 2 is still mysql. The web sign-in page has sqlite3 already selected.

## [1.0.2] - 2026-10-11

### Added

- sqlite3 and mysql. The default is the sqlite3 file `~/.local/OpenRbac/openrbac.sqlite3`.
- The terminal, the text menu, and the web sign-in page each offer choice 1 sqlite3 and choice 2 mysql. `open-rbac db-engine` stores the choice and does not open the database. Setup row 78 and the Database page offer the same choice.

## [1.0.1] - 2026-10-11

### Changed

- A terminal with no arguments asks for an account name and a password before the menu. Esc leaves without the menu.
- The front board no longer has a session row. Numbers 2–9 stay. `login`, `logout`, and `whoami` remain typed verbs.
- The menu, `serve`, and every domain verb create missing tables and seed an empty `sys_user` before they continue. A later init still reports `present`.

## [1.0.0] - 2026-10-11

### Added

- Online RBAC and centralized configuration for the text menu, typed verbs, and a local web page.
- MariaDB tables shaped for users, roles, menus, departments, job titles, parameters, dictionaries, notices, and audit logs.
- Data scope 1–4. Sessions in `sys_session`. Passwords as PBKDF2-HMAC-SHA256.
- Environment names `OPENRBAC_DB_*`, `OPENRBAC_BIND`, `OPENRBAC_PORT`, `OPENRBAC_ALLOW_REMOTE`, `OPENRBAC_LANG`, and `OPENRBAC_HOME`.
- ChronicleLogger constructed in `def main`.

### Changed

- Package name is **OpenRbac**. Console script is `open-rbac`.
- Front row 1 is session. Rows 2, 5, 6, and 7 are access, setup, audit, and serve.
- The about page domain line is `Online RBAC and centralized configuration`.

## Earlier history

This tree was specialized from a HelloTui checkout. Join, file listing, and FFmpeg are not part of OpenRbac.
