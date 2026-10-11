# Requirements index

**Product:** PyRbac (Python CLI — text menu and local web pages for online RBAC)
**Workspace state:** Specialized product law; **software-development** class; **pip/local package** install.
**Product version:** **1.0.2** (`pyproject.toml`, `src/PyRbac/__init__.py`, root `README.md`)
**Updated:** 2026-10-11

| ID / key | Title | Area | Status | Path | Updated |
|----------|-------|------|--------|------|---------|
| requirement-class-software-dev | Software-development class law + residual stack (Python, setuptools) | class | Active | `requirement-class-software-dev.md` | 2026-10-04 |
| requirement-domain-pyrbac | Domain surface: online RBAC and centralized configuration. Sign-in before the menu | domain | Active | `requirement-domain-pyrbac.md` | 2026-10-11 |
| requirement-domain-videojoin | Retired welcome-line domain | domain | Retired | `requirement-domain-videojoin.md` | 2026-10-11 |
| requirement-rbac | RBAC system map, permissions, data scope 1–4, seed on an empty database, protected rows | domain | Active | `requirement-rbac.md` | 2026-10-11 |
| requirement-database | sqlite3 default file and mysql tables, seed-once, auto-init | domain | Active | `requirement-database.md` | 2026-10-11 |
| requirement-environment | PYRBAC_* names, mode-0600 file, loopback bind | domain | Active | `requirement-environment.md` | 2026-10-11 |
| requirement-web-interface | Local HTML site, cookie, CSRF, shared service | domain | Active | `requirement-web-interface.md` | 2026-10-11 |
| requirement-python-about | About page: identity, host check, star box. No `--json` | python | Active | `requirement-python-about.md` | 2026-10-11 |
| requirement-video-ffmpeg-pipeline | Retired. No encoder, no concat, no media publish | video | Retired | `requirement-video-ffmpeg-pipeline.md` | 2026-10-11 |
| requirement-python-cli-interface | CLI entry, typed verbs, sign-in then menu on a terminal | python | Active | `requirement-python-cli-interface.md` | 2026-10-11 |
| requirement-python-cli-logging | ChronicleLogger construct in `def main`; no passwords in the log | python | Active | `requirement-python-cli-logging.md` | 2026-10-11 |
| requirement-python-tui | Text menu rows 2–9, sign-in first, path word, display columns | python | Active | `requirement-python-tui.md` | 2026-10-11 |
| requirement-python-cli-language | Menu language: front row 4, codes 41–53, leaf `~/.local/PyRbac/language` | python | Active | `requirement-python-cli-language.md` | 2026-10-11 |
| requirement-python-oop | Class map, including Desk, Access, and WebApp | python | Active | `requirement-python-oop.md` | 2026-10-11 |
| requirement-python-coding-style | Python style; one class per module; end state is the class map | python | Active | `requirement-python-coding-style.md` | 2026-10-04 |
| requirement-python-packaging | `pyproject.toml` / version / console script `py-rbac` | python | Active | `requirement-python-packaging.md` | 2026-10-11 |
| requirement-python-build-script | Maintainer `./build.sh` commands, including test-install | python | Active | `requirement-python-build-script.md` | 2026-10-11 |
| requirement-python-project-structure | Repository and `src/PyRbac` layout | python | Active | `requirement-python-project-structure.md` | 2026-10-11 |
| requirement-python-readme | Root user document: sections, badges, absolute screenshot URLs | python | Active | `requirement-python-readme.md` | 2026-10-11 |
| requirement-python-error-handling | Fail-closed errors; console sentences stay | python | Active | `requirement-python-error-handling.md` | 2026-10-04 |
| requirement-runtime-prerequisites | sqlite3 by default; mysql and PyMySQL when chosen; ChronicleLogger; no root auto-install | runtime | Active | `requirement-runtime-prerequisites.md` | 2026-10-11 |

## Intentionally absent (by design)

| Surface | Status on PyRbac |
|---------|----------------------|
| Shell online install / `curl\|sh` | **Absent** |
| Type 1 sudoers / root elevation inside the program | **Absent** |
| Code generation, AI, plugins, jobs, Redis, Vue bundle | **Absent** for 1.0.2 |
| Second Active `requirement-domain-*` | **Forbidden** while `requirement-domain-pyrbac` is Active |
| `hello`, `join`, `list-videos`, FFmpeg | **Absent** |
| `requirement-python-json-output` | **Absent**. No `--json` |

**Install mode:** **pip / local package** (`py-rbac` console script).

**Logger:** required (`ChronicleLogger>=1.3.1`). `def main` in `src/PyRbac/cli.py` writes `ChronicleLogger(...)`.

**Database:** sqlite3 by default, file `pyrbac.sqlite3`. mysql through `PyMySQL>=1.1.0` when `PYRBAC_DB_ENGINE=mysql`. Product mysql schema `pyrbac`. mysql tests use `pyrbac_test`.

**Rules for agents:**

1. Treat rows above as the live product-law inventory for PyRbac.
2. Do not invent additional `requirement-*.md` paths without a registry row in the same change.
3. Product source comments cite only these live requirement files.
4. Keep Status and Path in sync with each file’s header.
5. Exactly one Active `requirement-domain-*` (`requirement-domain-pyrbac`).
6. Do not write `ruoyi_db` or `ry`.

When adding a requirement: append a row, create the file under `docs/requirements/`, keep Status in sync with the file header.
