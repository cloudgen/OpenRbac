# PyRbac

![Version 1.0.0](https://img.shields.io/badge/version-1.0.0-blue)
![License MIT](https://img.shields.io/badge/license-MIT-green)
[![CIAO](https://img.shields.io/badge/CIAO-cloudgen-black)](https://github.com/cloudgen/ciao)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)

PyRbac is online role-based access control and centralized configuration. The text menu, the typed commands, and the local web pages call the same service.

It is specialized from the HelloTui menu and studied from [RuoYi-FastAPI](https://github.com/insistence/RuoYi-FastAPI). The web pages are plain HTML. There is no JavaScript bundle.

**Domain:** Online RBAC and centralized configuration.

## Features

- Front board rows: session, access, system-log, language, setup, audit, serve, self-management, and Exit.
- The same user, role, menu, department, post, parameter, dictionary, notice, and audit actions on the menu, on the command line, and on the web page.
- Data scope 1 all, 2 custom departments, 3 this department, 4 this department and children. Any other scope shows no rows.
- MariaDB or MySQL. The product database is `pyrbac`.
- ChronicleLogger for the status file. Passwords are not written there.
- The site listens on `127.0.0.1` unless you set `PYRBAC_ALLOW_REMOTE=yes`.

## Advantages

- One permission check for every surface. A button that your role cannot use is not shown.
- The menu keeps the path line, the local clock, and the rounded input box.
- Menu language is row 4, codes 41–53. `PYRBAC_LANG` overrides it and does not write the language file.
- `py-rbac` with no arguments on a terminal opens the menu and does not run pip.

## Quick Installation

You provide MariaDB or MySQL. pip installs this package, ChronicleLogger, and PyMySQL. pip does not install the database server, and this program does not call sudo.

```bash
python -m pip install PyRbac
```

From a checkout:

```bash
python -m pip install -e .
```

Create the tables once. The database password comes from the environment or from `~/.local/PyRbac/database` when that file is mode `0600`.

```bash
export PYRBAC_DB_PASSWORD='the-password-you-chose'
py-rbac db-init
```

The first run prints `Database pyrbac: seeded.` A later run prints `present` and does not add another administrator.

## Usage

On a terminal, `py-rbac` opens the menu. `py-rbac help` lists the verbs. `py-rbac serve` prints a URL and listens until you interrupt it. Menu row 7 starts that site in the background for as long as the process stays open.

`--password` is visible in the process list. The menu asks for the password in a masked field.

### Seeded accounts

Change these after the first sign-in.

| Account | Password | What this account can see |
|---------|----------|---------------------------|
| admin | admin123 | Every account and every action. Department Engineering. |
| operator | operator123 | Only the Operations department. List and query. No add, no parameter edit, no force logout. |
| clerk | clerk123 | Only the Platform department. Same common role as operator. |
| lead | lead123 | Engineering and its child department Platform. Not Operations. User list and query only. |

A suggested password for a new account is the parameter `sys.user.initPassword`, seeded as `123456`.

### How this differs from RuoYi-FastAPI

- Passwords are stored as PBKDF2-HMAC-SHA256 (`pbkdf2_sha256$…`). Upstream stores bcrypt.
- Signed-in sessions are rows in `sys_session`. Upstream keeps them in Redis.
- Data scope uses 1, 2, 3, and 4, which matches the studied role-column comment. Scope 5 is not granted.
- Captcha, export, import, scheduled jobs, code generation, and the Vue applications are not in this version.

### Environment

| Name | Default |
|------|---------|
| `PYRBAC_DB_HOST` | `127.0.0.1` |
| `PYRBAC_DB_PORT` | `3306` |
| `PYRBAC_DB_NAME` | `pyrbac` |
| `PYRBAC_DB_USER` | `pyrbac` |
| `PYRBAC_DB_PASSWORD` | none |
| `PYRBAC_BIND` | `127.0.0.1` |
| `PYRBAC_PORT` | `8765` |
| `PYRBAC_ALLOW_REMOTE` | unset. Set `yes` before binding a non-loopback address |
| `PYRBAC_LANG` | unset. One of the thirteen menu codes. It does not write the language file |

## Screenshots

These are captures of the running text menu.

![Front board](https://raw.githubusercontent.com/cloudgen/PyRbac/main/screenshots/main-menu-en.png)

*Front board. Row 1 is session. Row 4 is language. Row 9 is Exit.*

![Session](https://raw.githubusercontent.com/cloudgen/PyRbac/main/screenshots/session-menu.png)

*Session: login, whoami, and logout.*

![Login prompt](https://raw.githubusercontent.com/cloudgen/PyRbac/main/screenshots/login-prompt.png)

*The login question. The password field is masked.*

![Access](https://raw.githubusercontent.com/cloudgen/PyRbac/main/screenshots/access-menu.png)

*Users, roles, menus, departments, and posts.*

![Setup](https://raw.githubusercontent.com/cloudgen/PyRbac/main/screenshots/setup-menu.png)

*Parameters, dictionaries, and notices.*

![Audit](https://raw.githubusercontent.com/cloudgen/PyRbac/main/screenshots/audit-menu.png)

*Operation log, login log, and online users.*

![System log](https://raw.githubusercontent.com/cloudgen/PyRbac/main/screenshots/system-log.png)

*System log: view, clear, and the log folder.*

![Language](https://raw.githubusercontent.com/cloudgen/PyRbac/main/screenshots/language-menu.png)

*Language codes 41–53.*

![Self-management](https://raw.githubusercontent.com/cloudgen/PyRbac/main/screenshots/self-management.png)

*Version, about, and the pip verbs.*

![Traditional Chinese](https://raw.githubusercontent.com/cloudgen/PyRbac/main/screenshots/main-menu-zh-hant.png)

*The same front board after Traditional Chinese is selected. The path label is 路徑.*

![Simplified Chinese](https://raw.githubusercontent.com/cloudgen/PyRbac/main/screenshots/main-menu-zh-hans.png)

*Simplified Chinese.*

![Japanese](https://raw.githubusercontent.com/cloudgen/PyRbac/main/screenshots/main-menu-ja.png)

*Japanese.*

## Examples

```bash
py-rbac db-init
py-rbac login --user-name admin
py-rbac user-list
py-rbac whoami
py-rbac logout
py-rbac serve
```

On a terminal, the same `user-list` is row 2, then row 21.

## Platform Compatibility

Linux is the primary host. The menu needs a terminal. The database client is PyMySQL talking to MariaDB or MySQL. The web pages need a browser on this computer.

## Related Projects

- https://github.com/cloudgen/PyRbac
- https://pypi.org/project/PyRbac/
- https://github.com/insistence/RuoYi-FastAPI
- https://github.com/Wilgat/ChronicleLogger
- https://github.com/cloudgen/ciao
- https://github.com/cloudgen/ciao-lite
- https://github.com/cloudgen/safe-rm

## Contributing

Open an issue or a pull request on https://github.com/cloudgen/PyRbac/issues. Do not send a database password or a session token in a public issue.

## License

MIT. Copyright (c) 2026 Wong Chun Fai, aka: Cloudgen (cloudgen.wong@gmail.com). See [LICENSE.md](LICENSE.md).

## Last Update

2026-10-11
