**file**: docs/requirements/requirement-python-packaging.md
**Status**: Active (Version 1.3.6)
**Area**: python
**Key**: `requirement-python-packaging`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

`pyproject.toml` is the install manifest. The package name is `OpenRbac`, the version is `1.0.5`, and the console script is `open-rbac`.

### 1.1 Human-facing

**In one sentence:** pip installs OpenRbac 1.0.5, the command `open-rbac`, ChronicleLogger, and PyMySQL. sqlite3 comes with Python.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The operator | `python -m pip install -e .` |
| The other role | The manifest | `pyproject.toml` |
| Not this file | MariaDB itself | `requirement-runtime-prerequisites` |

## 2. Normative rules

1. **Name and version.** `name` is `OpenRbac`. `version` is `1.0.5`, the same string as `__version__`.
2. **Script.** `open-rbac = OpenRbac.cli:main`.
3. **Dependencies.** `ChronicleLogger>=1.3.1` and `PyMySQL>=1.1.0` are required. The package **MUST NOT** re-export ChronicleLogger.
4. **Author.** Wong Chun Fai, `cloudgen.wong@gmail.com`. Homepage `https://github.com/cloudgen/OpenRbac`.
5. **Python.** `requires-python` is `>=3.9`.
6. **Secrets.** The manifest **MUST NOT** contain a database password.
7. **Maintainer tool.** Commands of `./build.sh` are owned by `requirement-python-build-script`. This file owns the install manifest.

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Console script | `open-rbac` |
| Floor | The minimum version of a required dependency |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.2.2 | Earlier package identity |
| 2026-10-11 | Active 1.3.0 | OpenRbac 1.0.0, `open-rbac`, PyMySQL |
| 2026-10-11 | Active 1.3.1 | Maintainer commands point at `requirement-python-build-script` |
| 2026-10-11 | Active 1.3.2 | Product version 1.0.1 |
| 2026-10-11 | Active 1.3.3 | Product version 1.0.2 |
| 2026-10-11 | Active 1.3.4 | Product version 1.0.3 |
| 2026-10-11 | Active 1.3.5 | Product version 1.0.4 |
| 2026-10-14 | Active 1.3.6 | Product version 1.0.5 |

---

**Last Updated**: 2026-10-14
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
