# CHANGELOG

All notable changes to **OpenRbac** are documented here.
Version SSOT: `pyproject.toml` + `src/OpenRbac/__init__.__version__`.

## [1.0.5] - 2026-10-14

### Changed

- The product name is OpenRbac. The console script is `open-rbac`. The home folder is `~/.local/OpenRbac`. Environment names start with `OPENRBAC_`. The sqlite file is `openrbac.sqlite3`. The mysql database and account are `openrbac`.
- The front board is 1 rbac, 2 server, 3 system-log, 6 self-management, 7 language, and 9 Exit. Server holds setup 21, audit 22, and serve 23. Rbac children are 11–19 and 110–113. Setup children are 211–218. Audit children are 221–224. Self-management children are 62–67. Language codes are 71–83.
- The README pictures are a new capture of that menu, the sign-in question, and the Exit question.

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
- MariaDB tables shaped for users, roles, menus, departments, posts, parameters, dictionaries, notices, and audit logs.
- Data scope 1–4. Sessions in `sys_session`. Passwords as PBKDF2-HMAC-SHA256.
- Environment names `OPENRBAC_DB_*`, `OPENRBAC_BIND`, `OPENRBAC_PORT`, `OPENRBAC_ALLOW_REMOTE`, `OPENRBAC_LANG`, and `OPENRBAC_HOME`.
- ChronicleLogger constructed in `def main`.

### Changed

- Package name is **OpenRbac**. Console script is `open-rbac`.
- Front row 1 is session. Rows 2, 5, 6, and 7 are access, setup, audit, and serve.
- The about page domain line is `Online RBAC and centralized configuration`.

## Earlier history

This tree was specialized from a HelloTui checkout. Join, file listing, and FFmpeg are not part of OpenRbac.
