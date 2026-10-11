# CHANGELOG

All notable changes to **PyRbac** are documented here.
Version SSOT: `pyproject.toml` + `src/PyRbac/__init__.__version__`.

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
