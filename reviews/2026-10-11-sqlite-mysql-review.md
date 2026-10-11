# PyRbac review — sqlite3 and mysql — 2026-10-11

**Product:** PyRbac 1.0.2
**Scope:** Database engine choice on the command, the text menu, and the local web site. Default data file `pyrbac.sqlite3`. mysql remains available.
**Result:** Pass with the limits below.
**Suite:** `./tests/run.sh` on 2026-10-11 ran 38 tests in 18.687s and finished OK. The mysql seed case connected to `pyrbac_test` and passed.
**Checklists:** `CL-IMPLEMENTATION-CIAO`, `CL-CODE-REVIEW`, and `CL-SECURITY-REVIEW` were filled for this date.

## What was checked

| Check | Result |
|-------|--------|
| Empty `PYRBAC_DB_ENGINE` is sqlite3. The file is `pyrbac.sqlite3` under the app home | Pass. `TestEngineChoice.test_default_is_the_sqlite_file` |
| Choice `1` or `sqlite3` stores `PYRBAC_DB_ENGINE=sqlite3` at mode 0600 and does not create the data file | Pass |
| Choice `2` or `mysql` stores mysql. A set environment value wins. A conflict names `unset PYRBAC_DB_ENGINE to store the choice in the database file` | Pass |
| `py-rbac db-engine` with no `--engine` and no terminal prints both choices, returns 0, and does not create the data file | Pass |
| `--engine oracle` returns 1 with `ERROR:` and `Next:` | Pass |
| First `db-init` on sqlite reports `seeded`. The second reports `present`. The file is mode 0600 | Pass |
| `TestRbacDatabase` uses a temporary sqlite file and does not need `PYRBAC_DB_PASSWORD` | Pass. Seed line contains `pyrbac.sqlite3: seeded` |
| Scope behavior, including department ancestors, passes on sqlite | Pass. `test_seed_once_and_scopes` |
| Login page offers sqlite3 and mysql. `(default file)` appears when `PYRBAC_SQLITE_FILE` is empty | Pass |
| A non-loopback sign-in cannot switch engines | Pass |
| Setup row 78 is `db-engine` / `sqlite3 file or mysql`. Front rows 2–9 are unchanged | Pass |
| `db-engine` is a product verb and is not a domain verb, so the command does not open the database | Pass |
| mysql `pyrbac_test` seeds once and the output does not contain `ruoyi_db` or `ry` | Pass on this host |
| Version string `1.0.2` in the package, the badge, and the docs test | Pass. `tests/test_docs.py` |
| About line names sqlite3 as the default file, or MariaDB or MySQL, and PyMySQL | Pass |

## Requirements

| Requirement | Version | Engine rule |
|-------------|---------|-------------|
| `requirement-database` | 1.3.0 | AC-1 through AC-6. Rules 7 and 8 |
| `requirement-environment` | 1.1.0 | AC-4 and AC-5. Settings file and data file are different files |
| `requirement-python-cli-interface` | 1.3.0 | AC-1 and AC-4. `db-engine` |
| `requirement-python-tui` | 1.3.0 | Engine question, then init, then sign-in. Row 78 |
| `requirement-web-interface` | 1.1.0 | AC-6. Sign-in radios and the Database page |
| `requirement-runtime-prerequisites` | 1.3.0 | sqlite3 from Python. PyMySQL only for mysql |
| `requirement-python-oop` | 1.1.1 | Version `1.0.2`. `Store` remains one class |

`db-engine` is named in the CLI requirement and in the database requirement. Help text is not the second mention.

## How the choice is stored

Resolution stays environment, then the mode-0600 file `database`, then the default. The password still has no default and is required only for mysql. `save_engine` keeps every other line, writes a mode-0600 sibling, and replaces the settings file. `db-engine` does not call `ensure_database`.

The text menu asks inside curses before `ensure_database`. Enter keeps the current engine. Esc returns without creating tables. Setup row 78 uses the same question and does not call `Desk.execute` a second time.

The sign-in page posts the radio with the account form. A different engine from a non-loopback address is refused. The signed-in Database page requires `system:config:edit` and the session CSRF token. A real change clears the cookie because the session row is in the previous database.

## Limits

- The suite does not press curses keys. Row 78, the command, and the web form are what the tests drive.
- sqlite CREATE drops inline non-unique `KEY` indexes. Unique keys remain. The seed and the scope cases passed without those indexes.
- Choosing the other engine does not copy rows. The Database page says the next sign-in uses the saved engine.
- A loopback sign-in that selects an empty database seeds the documented initial accounts. A remote client cannot change the engine from the sign-in form.
- `tests/test_hello.py` still feeds the menu fixture the string `1.0.1`. That fixture is not the package version. The package, the README badge, and `tests/test_docs.py` use `1.0.2`.

## Security

`CL-SECURITY-REVIEW` verdict is clean / low risk. The settings file and the sqlite file are mode 0600. The app directory is mode 0700. Operator errors do not include SQL or the password. Statements stay parameterized on both engines.
