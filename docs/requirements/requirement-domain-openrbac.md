**file**: docs/requirements/requirement-domain-openrbac.md
**Status**: Active (Version 1.2.4)
**Area**: domain
**Key**: `requirement-domain-openrbac`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the domain surface for OpenRbac. The product is online role-based access control and centralized configuration. The same actions are available from the text menu, from typed verbs, and from the local web pages.

OpenRbac owns users, roles, menus, departments, job titles, dictionaries, parameters, notices, and audit records.

This file is the sole Active `requirement-domain-*`.

### 1.1 Human-facing

**In one sentence:** OpenRbac lets an administrator manage accounts and settings from a menu, a command, or a page on this computer, and each surface enforces the same permissions.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The operator | `open-rbac login --user-name admin` |
| The other role | A signed-in account limited by its roles | An operator sees only that operator's department |
| Not this file | The menu frame, the SQL tables, the template syntax, and the `el-*` components | TUI, database, `requirement-python-html-template`, `requirement-html-element-plus` |

| Includes | Excludes |
|----------|----------|
| Access, setup, audit, and serve as one product, after a sign-in | Code generation, AI chat, plugins, file storage, scheduled jobs |
| One service layer for the menu, the verbs, and the pages | A second permission check that the web page skips |
| English seed labels written for this product | Seed text copied from another product |
| Pages rendered inside this package | A separate frontend that calls a JSON API |

| Surface | What you open | What for |
|---------|---------------|----------|
| Text menu | `open-rbac` on a terminal | Sign in, then row 1 rbac and row 2 server |
| Typed verb | `open-rbac user-list` | The same list the menu shows |
| Web page | the URL printed by `serve` | The same list, with a cookie |

## 2. Normative rules

1. **Domain sentence.** The about page **MUST** say `Domain: Online RBAC and centralized configuration`.
2. **Shared service.** Class `Desk` **MUST** be the command path for the terminal and the text menu. Class `WebApp` **MUST** call `Access` and `Catalog` for the same facts.
3. **Non-goals.** The product **MUST NOT** ship code generation, an AI feature, plugins, a file manager, scheduled jobs, a Redis cache, a Vue or Vite npm build, a `frontend/` folder, a `backend/` folder, or transport encryption of the page body. HTML pages **MUST** be the templates rendered by `requirement-python-html-template` and `requirement-html-element-plus`. The reference Vue tree stays in the other project. This product **MUST NOT** add a JSON API whose job is to feed a browser application. It is not a python-web-server. The front board **MUST NOT** include a session row. Folder placement is `requirement-python-project-structure`.
4. **Storage.** Passwords are PBKDF2-HMAC-SHA256, rather than a bcrypt string. Online sessions are rows in `sys_session`, rather than Redis keys. Both facts **MUST** stay visible in the user document.
5. **Sole domain.** `requirement-domain-videojoin` stays Retired.

## 3. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | About text contains the domain sentence in this file |
| AC-2 | `hello`, `join`, and `list-videos` are not product verbs |
| AC-3 | A menu row and the matching verb call the same Desk method |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Online RBAC | Accounts, roles, menus, departments, and job titles checked on each action |
| Centralized configuration | Parameters, dictionary values, and notices in this product's database |
| Surface | The text menu, a typed verb, or the web page |

### Python web server

**Definition:** A **Python web server** is a **software-development** product whose primary operator surface is a **long-running HTTP process** plus a **browser (or other HTTP) client**. The checkout ship tree uses **`backend/`** for the Python server and **`frontend/`** for the static or client UI. It **MUST NOT** use **`src/`** as the required package root. It is **not** a python-cli and **not** a python-pypi-cli.

**Human daily-life explanation:** A python-web-server is a long-running HTTP program plus a browser client, with `backend/` and `frontend/` trees, not `src/` as the package root. It stays open.

**Daily-life example:** A diner that stays open: kitchen in the back, menu and seating in the front, not a handheld calculator you put away.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-11 | Active 1.0.0 | OpenRbac domain. Welcome-line domain retired |
| 2026-10-11 | Active 1.1.0 | Sign-in before the menu. No session row |
| 2026-10-11 | Active 1.2.0 | This product does not depend on another admin framework |
| 2026-10-14 | Active 1.2.1 | The text menu opens rbac on row 1 and server on row 2 |
| 2026-10-14 | Active 1.2.2 | HTML uses the Python Vue-shaped engine. A Vue or Vite npm build stays out |
| 2026-10-14 | Active 1.2.3 | The reference Vue tree stays outside. No frontend folder and no JSON API for a browser application |
| 2026-10-14 | Active 1.2.4 | The domain names job titles |

---

**Last Updated**: 2026-10-14
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
