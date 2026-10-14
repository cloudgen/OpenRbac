**file**: docs/requirements/requirement-environment.md
**Status**: Active (Version 1.2.0)
**Area**: domain
**Key**: `requirement-environment`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Process settings come from the environment, then from a mode-0600 file, then from defaults. Defaults never include a database password. The web listener stays on loopback unless the operator sets an explicit allow.

### 1.1 Human-facing

**In one sentence:** The default database is the sqlite3 file. mysql still takes its password from the environment or from a private file, and the web page stays on this computer unless you explicitly allow another address.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The operator | `export OPENRBAC_DB_PASSWORD=…` |
| The other role | The mode-0600 file | `~/.local/OpenRbac/database` |
| Not this file | The menu language leaf | `requirement-python-cli-language` |

| Includes | Excludes |
|----------|----------|
| The names in the table below | A password baked into the package |
| Loopback unless `OPENRBAC_ALLOW_REMOTE=yes` | Listening on every interface by default |

## 2. Names

| Name | Default | Meaning |
|------|---------|---------|
| `OPENRBAC_DB_ENGINE` | `sqlite3` | `sqlite3` or `mysql`. Empty means sqlite3 |
| `OPENRBAC_SQLITE_FILE` | `openrbac.sqlite3` in the home folder | sqlite3 data file. This is not the settings file |
| `OPENRBAC_DB_HOST` | `127.0.0.1` | mysql host |
| `OPENRBAC_DB_PORT` | `3306` | Database port |
| `OPENRBAC_DB_NAME` | `openrbac` | Database name. Letters, digits, and underscore |
| `OPENRBAC_DB_USER` | `openrbac` | Database user |
| `OPENRBAC_DB_PASSWORD` | empty | Required before a mysql connection. Not used by sqlite3. No default |
| `OPENRBAC_BIND` | `127.0.0.1` | Web bind address |
| `OPENRBAC_PORT` | `8765` | Web port. `0` asks for a free port |
| `OPENRBAC_ALLOW_REMOTE` | unset | Must be `yes` before a non-loopback bind |
| `OPENRBAC_LANG` | unset | Menu language. Does not write the language leaf |
| `OPENRBAC_HOME` | unset | When set, replaces `~/.local/OpenRbac` for the session, the database file, and the local sign-in |

## 3. Normative rules

1. **Order.** A non-empty environment value **MUST** win over the file. The file **MUST** win over a default. A password **MUST NOT** have a default. `OPENRBAC_DB_ENGINE` **MUST** follow this order. The default engine **MUST** be `sqlite3`.
2. **File.** The settings file is `${OPENRBAC_HOME:-$HOME/.local/OpenRbac}/database`. The program **MUST** ignore it unless its mode is `0600`. Lines are `KEY=VALUE`. A choice of engine **MUST** write `OPENRBAC_DB_ENGINE` into that file when the environment does not set it, and **MUST** leave the other lines in place. The new file **MUST** be mode `0600` and its folder **MUST** be mode `0700`. A settings file that is not mode `0600` **MUST** be refused rather than rewritten.
3. **sqlite3 file.** The data file **MUST** default to `openrbac.sqlite3` in that same folder. `OPENRBAC_SQLITE_FILE` **MUST** replace it when set. The program **MUST** create the data file as mode `0600`.
4. **Session file.** The terminal token file is `session` in that same directory, mode `0600`, after the directory is mode `0700`. A file that is not mode `0600` **MUST** be treated as signed out. The web cookie is not this file.
5. **Bind.** `127.0.0.1`, `localhost`, and `::1` are loopback. Any other address **MUST** raise a refusal unless `OPENRBAC_ALLOW_REMOTE` is `yes`.
6. **Secrets in docs.** Versioned product documents **MUST NOT** contain a host vault path, a private key name, or a live password. The seeded initial passwords in the user document are the demo values the operator is told to change.
7. **Local sign-in.** The encrypted sign-in files from `requirement-local-login` live in this same home folder. This file does not define a password default for them.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | A mode-0644 database file does not supply the password |
| AC-2 | A mode-0600 file supplies it, and the environment wins |
| AC-3 | Bind `0.0.0.0` without `OPENRBAC_ALLOW_REMOTE=yes` is refused |
| AC-4 | An empty engine is sqlite3 and the default file name is `openrbac.sqlite3` |
| AC-5 | A stored engine choice is mode 0600, and a set environment value wins |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Database file | The mode-0600 `KEY=VALUE` settings file. It is not the sqlite3 data file |
| Default sqlite3 file | `openrbac.sqlite3` in the home folder |
| Loopback | `127.0.0.1`, `localhost`, or `::1` |
| Allow remote | The explicit `OPENRBAC_ALLOW_REMOTE=yes` switch |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-11 | Active 1.0.0 | Environment names, 0600 file, loopback bind |
| 2026-10-11 | Active 1.1.0 | `OPENRBAC_DB_ENGINE` defaults to sqlite3. `OPENRBAC_SQLITE_FILE` names the data file |
| 2026-10-11 | Active 1.2.0 | The home folder also holds the local sign-in files |

---

**Last Updated**: 2026-10-11
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
