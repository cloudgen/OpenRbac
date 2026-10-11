# Requirements

Authoritative specialized product law for **PyRbac** lives here.

| Fact | Value |
|------|-------|
| Product / package | `PyRbac` |
| Version SSOT | **`1.0.4`** (`pyproject.toml` + `src/PyRbac/__init__.py`) |
| Console script | `py-rbac` |
| Module | `python -m PyRbac` |
| Install mode | pip / local package |
| Domain | `requirement-domain-pyrbac` — online RBAC and centralized configuration |
| Menu language | `requirement-python-cli-language` — row 4, codes 41–53, leaf `~/.local/PyRbac/language` |
| Logger | `ChronicleLogger>=1.3.1`, constructed in `def main` |
| Database | sqlite3 file `pyrbac.sqlite3` by default; mysql and `PyMySQL>=1.1.0` when chosen; mysql schema `pyrbac` |
| Web | `127.0.0.1:8765` unless the environment says otherwise |
| Maintainer tool | `requirement-python-build-script` — `./build.sh` |

The registry is [index.md](index.md).
