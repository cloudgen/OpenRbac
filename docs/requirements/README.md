# Requirements

Authoritative specialized product law for **OpenRbac** lives here.

| Fact | Value |
|------|-------|
| Product / package | `OpenRbac` |
| Version SSOT | **`1.0.5`** (`pyproject.toml` + `src/OpenRbac/__init__.py`) |
| Console script | `open-rbac` |
| Module | `python -m OpenRbac` |
| Install mode | pip / local package |
| Domain | `requirement-domain-openrbac` — online RBAC and centralized configuration |
| Menu language | `requirement-python-cli-language` — row 7, codes 71–83, leaf `~/.local/OpenRbac/language` |
| Logger | `ChronicleLogger>=1.3.1`, constructed in `def main` |
| Database | sqlite3 file `openrbac.sqlite3` by default; mysql and `PyMySQL>=1.1.0` when chosen; mysql schema `openrbac` |
| Web | `127.0.0.1:8765` unless the environment says otherwise |
| Maintainer tool | `requirement-python-build-script` — `./build.sh` |

The registry is [index.md](index.md).
