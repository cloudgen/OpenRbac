**file**: docs/requirements/requirement-python-project-structure.md
**Status**: Active (Version 1.2.0)
**Area**: python
**Key**: `requirement-python-project-structure`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

The installable package is `src/OpenRbac`. Tests live in `tests/`. Product law that is committed lives in `docs/requirements/`. Public reviews live in `reviews/` because the rest of `docs/` is gitignored.

### 1.1 Human-facing

**In one sentence:** The code and the pages are under `src/OpenRbac`, and there is no separate frontend folder.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | A reader of the tree | `src/OpenRbac/cli.py` |
| The other role | gitignore | `docs/**` ignored except `docs/requirements/**` |
| Not this file | The class list | `requirement-python-oop` |

## 2. Normative rules

1. **Package.** Import name `OpenRbac`. There is no `src/HelloTui` and no `src/VideoJoin` in this product.
2. **Tracked docs.** `docs/requirements/**` is tracked. Other `docs/` trees stay local.
3. **Reviews.** A review, checklist, or test plan that must be in the public repository **MUST** live under `reviews/`.
4. **Screenshots.** Running-menu captures live in `screenshots/` and are tracked.
5. **Samples.** This product has no `sample-videos/` tree.
6. **Build script.** `./build.sh` is tracked at the repository root. Its commands are owned by `requirement-python-build-script`.
7. **Pages.** HTML page files **MUST** live under `src/OpenRbac/templates/`. Components and stylesheets **MUST** live under `src/OpenRbac/element_plus/`.
8. **Not a split server.** The repository **MUST NOT** contain a `frontend/` directory or a `backend/` directory. This product is not a python-web-server. A python-web-server keeps `backend/` and `frontend/` and does not use `src/` as the package root. This package root stays `src/OpenRbac`.
9. **No client build.** The repository **MUST NOT** contain `package.json` or `vite.config.js`.

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Package root | `src/OpenRbac` |
| Public review | A Markdown file under `reviews/` |
| Page file | One HTML template under `src/OpenRbac/templates/` |

### Python web server

**Definition:** A **Python web server** is a **software-development** product whose primary operator surface is a **long-running HTTP process** plus a **browser (or other HTTP) client**. The checkout ship tree uses **`backend/`** for the Python server and **`frontend/`** for the static or client UI. It **MUST NOT** use **`src/`** as the required package root. It is **not** a python-cli and **not** a python-pypi-cli.

**Human daily-life explanation:** A python-web-server is a long-running HTTP program plus a browser client, with `backend/` and `frontend/` trees, not `src/` as the package root. It stays open.

**Daily-life example:** A diner that stays open: kitchen in the back, menu and seating in the front, not a handheld calculator you put away.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.0.0 | Earlier package path |
| 2026-10-11 | Active 1.1.0 | `src/OpenRbac` and `reviews/` |
| 2026-10-11 | Active 1.1.1 | `./build.sh` is tracked. Commands live on `requirement-python-build-script` |
| 2026-10-14 | Active 1.2.0 | Pages stay in the package. No `frontend/` or `backend/` split. No client build files |

---

**Last Updated**: 2026-10-14
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
