**file**: docs/requirements/requirement-environment.md
**Status**: Active (Version 1.0.0)
**Area**: domain
**Key**: `requirement-environment`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Process settings come from the environment, then from a mode-0600 file, then from defaults. Defaults never include a database password. The web listener stays on loopback unless the operator sets an explicit allow.

### 1.1 Human-facing

**In one sentence:** Put the database password in the environment or in a private file, and the web page stays on this computer unless you explicitly allow another address.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The operator | `export PYRBAC_DB_PASSWORD=…` |
| The other role | The mode-0600 file | `~/.local/PyRbac/database` |
| Not this file | The menu language leaf | `requirement-python-cli-language` |

| Includes | Excludes |
|----------|----------|
| The names in the table below | A password baked into the package |
| Loopback unless `PYRBAC_ALLOW_REMOTE=yes` | Listening on every interface by default |

## 2. Names

| Name | Default | Meaning |
|------|---------|---------|
| `PYRBAC_DB_HOST` | `127.0.0.1` | Database host |
| `PYRBAC_DB_PORT` | `3306` | Database port |
| `PYRBAC_DB_NAME` | `pyrbac` | Database name. Letters, digits, and underscore |
| `PYRBAC_DB_USER` | `pyrbac` | Database user |
| `PYRBAC_DB_PASSWORD` | empty | Required before a connection. No default |
| `PYRBAC_BIND` | `127.0.0.1` | Web bind address |
| `PYRBAC_PORT` | `8765` | Web port. `0` asks for a free port |
| `PYRBAC_ALLOW_REMOTE` | unset | Must be `yes` before a non-loopback bind |
| `PYRBAC_LANG` | unset | Menu language. Does not write the language leaf |
| `PYRBAC_HOME` | unset | When set, replaces `~/.local/PyRbac` for the session and the database file |

## 3. Normative rules

1. **Order.** A non-empty environment value **MUST** win over the file. The file **MUST** win over a default. A password **MUST NOT** have a default.
2. **File.** The database file is `${PYRBAC_HOME:-$HOME/.local/PyRbac}/database`. The program **MUST** ignore it unless its mode is `0600`. Lines are `KEY=VALUE`.
3. **Session file.** The terminal token file is `session` in that same directory, mode `0600`, after the directory is mode `0700`. A file that is not mode `0600` **MUST** be treated as signed out. The web cookie is not this file.
4. **Bind.** `127.0.0.1`, `localhost`, and `::1` are loopback. Any other address **MUST** raise a refusal unless `PYRBAC_ALLOW_REMOTE` is `yes`.
5. **Secrets in docs.** Versioned product documents **MUST NOT** contain a host vault path, a private key name, or a live password. The seeded initial passwords in the user document are the demo values the operator is told to change.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | A mode-0644 database file does not supply the password |
| AC-2 | A mode-0600 file supplies it, and the environment wins |
| AC-3 | Bind `0.0.0.0` without `PYRBAC_ALLOW_REMOTE=yes` is refused |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Database file | The mode-0600 `KEY=VALUE` file for connection settings |
| Loopback | `127.0.0.1`, `localhost`, or `::1` |
| Allow remote | The explicit `PYRBAC_ALLOW_REMOTE=yes` switch |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-11 | Active 1.0.0 | Environment names, 0600 file, loopback bind |

---

**Last Updated**: 2026-10-11
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
