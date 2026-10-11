**file**: docs/requirements/requirement-runtime-prerequisites.md
**Status**: Active (Version 1.3.0)
**Area**: runtime
**Key**: `requirement-runtime-prerequisites`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

PyRbac needs CPython and ChronicleLogger. sqlite3 comes with CPython and is the default database. mysql also needs PyMySQL and a MariaDB or MySQL server that already has the `pyrbac` schema and account. The program does not install those with root and does not call sudo.

### 1.1 Human-facing

**In one sentence:** Install the Python packages with pip. sqlite3 needs no extra server. mysql still needs MariaDB or MySQL that you provide.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The operator | MariaDB is already running |
| The other role | pip | Installs ChronicleLogger and PyMySQL |
| Not this file | The table list | `requirement-database` |

## 2. Normative rules

1. **Logger.** Missing ChronicleLogger **MUST** exit 1 with the next-step sentence in `requirement-python-cli-logging`.
2. **Driver.** sqlite3 **MUST** use the standard-library module. Missing PyMySQL on a mysql connection **MUST** tell the operator to run `python -m pip install "PyMySQL>=1.1.0"`.
3. **Server.** The program **MUST NOT** install MariaDB or sqlite, create a system user, or call sudo. A connection failure **MUST** name the settings to check and `py-rbac db-init`. sqlite3 **MUST** name the file. mysql **MUST** name the host, user, and password settings.
4. **No encoder.** FFmpeg is not a prerequisite.

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Prerequisite | Something the operator provides before a verb can succeed |
| Next step | The sentence that names the install or the setting to fix |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.1.2 | ChronicleLogger required. FFmpeg was a historical note |
| 2026-10-11 | Active 1.2.0 | MariaDB or MySQL and PyMySQL. No encoder |
| 2026-10-11 | Active 1.3.0 | sqlite3 is the default and needs no separate server |

---

**Last Updated**: 2026-10-11
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
