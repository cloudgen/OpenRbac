# CHANGELOG

All notable changes to **PyRbac** are documented here.
Version SSOT: `pyproject.toml` + `src/PyRbac/__init__.__version__`.

## [1.0.4] - 2026-10-11

### Added

- A successful terminal sign-in stores the account and password in encrypted files under the home folder. A later start uses them when the login still works and does not ask again. A failed restore removes the saved sign-in. The web sign-in page does not write those files.

### Changed

- Row 9 Exit asks before it leaves. Enter or y logs out and removes the saved sign-in. n leaves and keeps it. Esc stays on the menu. End of input still leaves without the question.
- The sign-in question keeps its instructions, including the sqlite3 file, above the account name and the password.
- The README pictures show the current menu: version 1.0.4, no session row, the sign-in question, and the Exit question.

## [1.0.3] - 2026-10-11

### Changed

- A terminal with no arguments uses sqlite3 and `~/.local/PyRbac/pyrbac.sqlite3`. It asks for the account and the password, and it does not ask for the engine or the file path.
- Enter on `py-rbac db-engine` and on setup row 78 selects sqlite3 and that default file. Choice 2 is still mysql. The web sign-in page has sqlite3 already selected.

## [1.0.2] - 2026-10-11

### Added

- sqlite3 and mysql. The default is the sqlite3 file `~/.local/PyRbac/pyrbac.sqlite3`.
- The terminal, the text menu, and the web sign-in page each offer choice 1 sqlite3 and choice 2 mysql. `py-rbac db-engine` stores the choice and does not open the database. Setup row 78 and the Database page offer the same choice.

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
- Environment names `PYRBAC_DB_*`, `PYRBAC_BIND`, `PYRBAC_PORT`, `PYRBAC_ALLOW_REMOTE`, `PYRBAC_LANG`, and `PYRBAC_HOME`.
- ChronicleLogger constructed in `def main`.

### Changed

- Package name is **PyRbac**. Console script is `py-rbac`.
- Front row 1 is session. Rows 2, 5, 6, and 7 are access, setup, audit, and serve.
- The about page domain line is `Online RBAC and centralized configuration`.

## Earlier history

This tree was specialized from a HelloTui checkout. Join, file listing, and FFmpeg are not part of PyRbac.
