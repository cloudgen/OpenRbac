# PyRbac

![Version 1.0.2](https://img.shields.io/badge/version-1.0.2-blue)
![License MIT](https://img.shields.io/badge/license-MIT-green)
[![CIAO](https://img.shields.io/badge/CIAO-cloudgen-black)](https://github.com/cloudgen/ciao)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)

PyRbac is online role-based access control and centralized configuration. The text menu, the typed commands, and the local web pages call the same service.

It is specialized from the HelloTui menu. The web pages are plain HTML. There is no JavaScript bundle.

**Domain:** Online RBAC and centralized configuration.

## Features

- A terminal with no arguments asks for the database engine, then an account and a password, then opens the menu.
- Front board rows: access, system-log, language, setup, audit, serve, self-management, and Exit. There is no session row.
- The same user, role, menu, department, post, parameter, dictionary, notice, and audit actions on the menu, on the command line, and on the web page.
- Data scope 1 all, 2 custom departments, 3 this department, 4 this department and children. Any other scope shows no rows.
- sqlite3 or MariaDB or MySQL. The default is the sqlite3 file `~/.local/PyRbac/pyrbac.sqlite3`. mysql uses the database `pyrbac`.
- ChronicleLogger for the status file. Passwords are not written there.
- The site listens on `127.0.0.1` unless you set `PYRBAC_ALLOW_REMOTE=yes`.

## Advantages

- One permission check for every surface. A button that your role cannot use is not shown.
- The menu keeps the path line, the local clock, and the rounded input box.
- Menu language is row 4, codes 41–53. `PYRBAC_LANG` overrides it and does not write the language file.
- `py-rbac` with no arguments on a terminal signs in, then opens the menu, and does not run pip. A missing database is created before that question.

## Quick Installation

The default database is a sqlite3 file. You do not install a database server for that choice. mysql is optional: you provide MariaDB or MySQL yourself. pip installs this package, ChronicleLogger, and PyMySQL. pip does not install a database server, and this program does not call sudo.

```bash
python -m pip install PyRbac
```

From a checkout:

```bash
python -m pip install -e .
```

The default engine is sqlite3. `py-rbac db-init` creates `~/.local/PyRbac/pyrbac.sqlite3` when that file is missing. A password is not required for sqlite3.

```bash
py-rbac db-init
```

The first init prints `seeded`. A later init prints `present` and does not add another administrator.

Choose the engine from the terminal, from the text menu, or from the web sign-in page. Choice 1 is the sqlite3 file. Choice 2 is mysql. Enter keeps the current engine. `py-rbac db-engine` does not open the database.

```bash
py-rbac db-engine --engine sqlite3
py-rbac db-engine --engine mysql
```

mysql reads the password from the environment or from `~/.local/PyRbac/database` when that file is mode `0600`. The sqlite3 data file is also mode `0600`. The product mysql database is `pyrbac`.

```bash
export PYRBAC_DB_PASSWORD='the-password-you-chose'
py-rbac db-engine --engine mysql
py-rbac db-init
```

## Usage

On a terminal, `py-rbac` asks for the database engine, then asks for the account name, then the password. A menu, `serve`, or any domain verb creates the tables when they are missing. After a match it opens the menu. Esc on the engine question or the sign-in question leaves without the menu. Setup row 78 asks for the same engine choice. `py-rbac help` lists the verbs. `py-rbac serve` prints a URL and listens until you interrupt it. Menu row 7 starts that site in the background for as long as the process stays open. The web sign-in page has the same two engine choices. A signed-in administrator can also open Database.

`login`, `logout`, and `whoami` are typed verbs. They are not rows on the menu.

`--password` is visible in the process list. The sign-in question and the menu mask the password field.

### Seeded accounts

Change these after the first sign-in.

| Account | Password | What this account can see |
|---------|----------|---------------------------|
| admin | admin123 | Every account and every action. Department Engineering. |
| operator | operator123 | Only the Operations department. List and query. No add, no parameter edit, no force logout. |
| clerk | clerk123 | Only the Platform department. Same common role as operator. |
| lead | lead123 | Engineering and its child department Platform. Not Operations. User list and query only. |

A suggested password for a new account is the parameter `sys.user.initPassword`, seeded as `123456`.

### Passwords and sessions

- Passwords are stored as PBKDF2-HMAC-SHA256 (`pbkdf2_sha256$…`), rather than bcrypt.
- Signed-in sessions are rows in `sys_session`, rather than Redis.
- Data scope uses 1, 2, 3, and 4. Scope 5 is not granted.
- Captcha, export, import, scheduled jobs, code generation, and a Vue application are not in this version.

### Environment

| Name | Default |
|------|---------|
| `PYRBAC_DB_ENGINE` | `sqlite3`. The other value is `mysql` |
| `PYRBAC_SQLITE_FILE` | `~/.local/PyRbac/pyrbac.sqlite3` |
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

*Front board after sign-in. Row 2 is access. Row 4 is language. Row 9 is Exit. This capture still shows the earlier session row.*

![Login prompt](https://raw.githubusercontent.com/cloudgen/PyRbac/main/screenshots/login-prompt.png)

*The sign-in question that opens before the menu. The password field is masked.*

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
py-rbac
py-rbac db-init
py-rbac login --user-name admin
py-rbac user-list
py-rbac whoami
py-rbac logout
py-rbac serve
```

On a terminal, after sign-in, the same `user-list` is row 2, then row 21.

## Platform Compatibility

Linux is the primary host. The menu needs a terminal. The database client is PyMySQL talking to MariaDB or MySQL. The web pages need a browser on this computer.

## Related Projects

- https://github.com/cloudgen/PyRbac
- https://pypi.org/project/PyRbac/
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
