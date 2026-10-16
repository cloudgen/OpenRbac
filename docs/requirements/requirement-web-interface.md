**file**: docs/requirements/requirement-web-interface.md
**Status**: Active (Version 1.3.10)
**Area**: domain
**Key**: `requirement-web-interface`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

The web interface is a small standard-library HTTP site. Every HTML body is a file under `src/OpenRbac/templates/`, rendered by `requirement-python-html-template` with the components in `requirement-html-element-plus`. The only script is `/table-check.js`, and only on a page that shows a table checkbox. Every list and every form calls the same Access or Catalog method as the text menu. The typed verb `serve` listens in the foreground. Server row 23 starts the listener in the background and prints the URL.

### 1.1 Human-facing

**In one sentence:** Open the printed URL, choose sqlite3 or mysql, sign in, and the pages you see are the actions your role allows.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The browser on this computer | `http://127.0.0.1:8765/` |
| The other role | The cookie `openrbac_session` | HttpOnly, SameSite=Lax |
| Not this file | The permission strings and the Vue template syntax | `requirement-rbac`, `requirement-python-html-template` |

| Includes | Excludes |
|----------|----------|
| Login, the engine choice, users, roles, menus, departments, job titles, parameters, dictionaries, notices, both logs, online users | A Vite build, a `frontend/` folder, or a JSON API clone |
| A hidden CSRF field on POST | Vue, Element Plus JavaScript, jQuery, Bootstrap JavaScript, or a script from another host |
| Forms only when the account has that permission | Showing an Add button the account cannot use |

## 2. Normative rules

1. **Bind.** The listener **MUST** use `requirement-environment`. The default is `127.0.0.1:8765`.
2. **Cookie.** A successful login **MUST** set `openrbac_session` with `HttpOnly`, `SameSite=Lax`, and `Path=/`, then redirect to `/`. The login page **MUST NOT** print the seed passwords.
3. **CSRF.** A POST other than login **MUST** include a hidden `csrf` field equal to the session row. A mismatch **MUST** be status 400.
4. **Auth.** A page other than `/login` without a session **MUST** redirect to `/login`. A missing permission **MUST** be status 403. Another access error **MUST** be status 400.
5. **Headers.** Each HTML response **MUST** send `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, and `Content-Security-Policy: default-src 'none'; style-src 'self' 'unsafe-inline'; script-src 'self'; img-src 'self' data:; form-action 'self'`. The image source **MUST** allow this host and an inline `data:` image. `script-src` **MUST** be `'self'` only. It **MUST NOT** include `unsafe-inline` and it **MUST NOT** name another host.
6. **Images.** An image **MUST** be a separate file on this host. A page or a stylesheet **MUST** reference that file by a same-origin path. An inline `data:` image **MUST NOT** be used unless a requirement explicitly specifies that inline image. A stylesheet that a requirement names as a whole **MAY** keep an image already written inside that file. The image policy allows a `data:` image so a specified inline image is not refused.
7. **Escape.** Text placed in HTML **MUST** be escaped by `HtmlTemplate`. The online page **MUST** show an 8-character token prefix on the button and **MUST** send the full token only as a hidden field. The terminal `online-list` **MUST** show the full token so the operator can pass `--token`. The layout of that page is `requirement-html-online`.
8. **Handler.** `ThreadingHTTPServer` constructs a nested handler inside `WebApp.make_server`. That nested class is the one exception to one-class-per-module. It **MUST** delegate to `WebApp`.
9. **Nav.** The shell sidebar **MUST** omit a destination when the account lacks the matching list permission. The page body **MUST** be the template named for that path in `requirement-python-html-template`. Those files are the pages. A separate frontend and a JSON API for a browser application are out of this product (`requirement-domain-openrbac`, `requirement-python-project-structure`).
10. **Engine choice.** The sign-in page **MUST** offer sqlite3, including the default file path, and mysql. The checked value **MUST** be the current engine. A sign-in from loopback **MAY** store a different engine before the password is checked. A sign-in from any other address **MUST NOT** switch the engine. The Database page **MUST** require `system:config:edit` and the session CSRF field. Saving a different engine there **MUST** clear the session cookie, because the session row remains in the previous database.
11. **Local sign-in.** A web sign-in **MUST NOT** write the terminal session file or the local login files from `requirement-local-login`. It uses the cookie only.
12. **Sidebar scrollport.** The signed-in sidebar **MUST** be a column whose height is `100vh` in the product stylesheet, with `overflow: auto` on that column. The shell **MUST NOT** place the menu inside `el-scrollbar`. A function **MUST NOT** read layout and write that column’s size. The ban is `requirement-html-javascript`. Changing a scrollable wrap dynamically is forbidden.
13. **Theme.** Each HTML page **MUST** use the stored theme from `requirement-html-theme`. Every theme **MUST** link `/apex.css` and `/themes/<name>.css` and **MUST NOT** link `/element-plus.css` or `/openrbac.css`. The listener **MUST** serve those files from this host. An invalid theme **MUST** refuse the page with the settings error. The choice **MUST NOT** add AdminLTE JavaScript, Bootstrap JavaScript, Vue, or a script from another host. A page **MAY** load `/table-check.js` when it shows a table checkbox. The form `method`, `action`, and field `name` values **MUST** stay the same, including `csrf`.
14. **Body font.** The document `body` **MUST** use the small font size in `requirement-html-body-font`. That size **MUST** be 13px. The size **MUST** be in `/apex.css`. It **MUST NOT** be set by a script or by an inline style on `<body>`.

## 3. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | Admin login redirects and the users page includes Add a user |
| AC-2 | A POST with the wrong CSRF token is 400 |
| AC-3 | The operator users page omits Add a user and omits clerk |
| AC-4 | The operator roles page is 403 |
| AC-5 | A users request without a cookie redirects to `/login` |
| AC-6 | The sign-in page offers sqlite3, the default file, and mysql |
| AC-7 | The shell template contains no `el-scrollbar`, and the sidebar rule sets `height: 100vh` and `overflow: auto` |
| AC-8 | A page links `/apex.css` and `/themes/<name>.css` and does not link `/element-plus.css` or `/openrbac.css` |
| AC-9 | An HTML page sends `img-src 'self' data:` and `script-src 'self'`. It does not send `unsafe-inline` on `script-src` and it does not name another script host |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Session cookie | `openrbac_session`, the token stored in `sys_session` |
| CSRF field | The hidden form value that must match the session row |
| Foreground serve | `open-rbac serve`, which blocks until interrupted |
| Background serve | Server row 23, which lives until the process exits |

### UI infinite reflow

**Definition:** A UI infinite reflow is a layout cycle: the browser measures a box, writes a size that depends on that measurement, and measures again, and the sizes never settle. The usual shape is a cyclic percentage. A scroll wrap is `height: 100%` inside a parent whose height is the wrap’s own content (`min-height` only, or `height: auto`). The same cycle is started by a function that reads `scrollHeight`, `offsetHeight`, `clientHeight`, or `getBoundingClientRect` and writes `height`, `min-height`, or `style` back onto that wrap or its parent. The layout thread keeps re-entering. The page, and often the whole desktop, stops answering. Pain PP-A-31.

**Human daily-life explanation:** A UI infinite reflow is a tailor who measures the cloth, cuts the table to match the cloth, then measures the cloth again because the table changed. The tape never stops. The room fills with the sound of the tape and nobody can open the door.

**Daily-life example:** A side column says “I am as tall as my parent,” and the parent says “I am as tall as the side column.” The painter measures forever. The screen locks.

### UI sidebar

**Definition:** ui-sidebar is the production UI label whose English UI term is Sidebar. The actual UI function is the side column that lists destinations beside the page body. The column’s height is a definite viewport length in the stylesheet (`100vh` or a stated length). Overflow scrolls on that column. The column is not a child whose `height: 100%` is resolved against a parent that sizes itself from the column.

**Human daily-life explanation:** A ui-sidebar is the narrow list on the side of the page that says where you can go. The list has a fixed height, like a door frame. Extra names scroll inside the frame. The frame does not grow because the list grew.

**Daily-life example:** A restaurant menu is clipped to the left of the table. You slide the menu. The table does not get taller each time you slide it.

### UI scrollbar

**Definition:** ui-scrollbar is the production UI label whose English UI term is Scrollbar. The actual UI function is the control that shows more content than fits and lets the reader move through it. The wrap’s size is only in the stylesheet. Changing a scrollable wrap dynamically is forbidden. A function must not read `scrollHeight`, `offsetHeight`, `clientHeight`, or `getBoundingClientRect` and write `height`, `min-height`, or inline style onto that wrap or its parent. That write is a UI infinite reflow.

**Human daily-life explanation:** A ui-scrollbar is the slider that shows there is more to read. The window size is printed on the plan. Nobody comes back with a tape measure and rebuilds the window because the paper was long. Rebuilding the window from the paper is how the room locks.

**Daily-life example:** A long grocery list sits in a fixed window with a slider. A helper who stretches the window to the length of the list, then measures again, never finishes. That helper must not be hired.

### Python web server

**Definition:** A **Python web server** is a **software-development** product whose primary operator surface is a **long-running HTTP process** plus a **browser (or other HTTP) client**. The checkout ship tree uses **`backend/`** for the Python server and **`frontend/`** for the static or client UI. It **MUST NOT** use **`src/`** as the required package root. It is **not** a python-cli and **not** a python-pypi-cli.

**Human daily-life explanation:** A python-web-server is a long-running HTTP program plus a browser client, with `backend/` and `frontend/` trees, not `src/` as the package root. It stays open.

**Daily-life example:** A diner that stays open: kitchen in the back, menu and seating in the front, not a handheld calculator you put away.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-11 | Active 1.0.0 | Loopback HTML site, cookie, and CSRF |
| 2026-10-11 | Active 1.1.0 | Sign-in and Database pages choose sqlite3 or mysql |
| 2026-10-11 | Active 1.2.0 | A web sign-in does not write the local login files |
| 2026-10-14 | Active 1.2.1 | Background serve is server row 23 |
| 2026-10-14 | Active 1.3.0 | HTML comes from the Vue-shaped template engine and the Element Plus components |
| 2026-10-14 | Active 1.3.1 | The sidebar is a `100vh` scrollport and is not an `el-scrollbar` |
| 2026-10-14 | Active 1.3.2 | Page files are the embedded templates. No frontend folder and no JSON API for a browser application |
| 2026-10-14 | Active 1.3.3 | The job title page is included with the other record pages |
| 2026-10-14 | Active 1.3.4 | The stored theme selects the stylesheet and the markup |
| 2026-10-14 | Active 1.3.5 | Theme acceptance is AC-8. The sidebar acceptance stays AC-7. adminlte does not link `/openrbac.css` |
| 2026-10-14 | Active 1.3.6 | The image policy allows this host and a data: image. An image is a separate file unless a requirement specifies an inline image |
| 2026-10-14 | Active 1.3.7 | The online page layout is `requirement-html-online` |
| 2026-10-15 | Active 1.3.8 | The document body font size is `requirement-html-body-font` |
| 2026-10-16 | Active 1.3.9 | HTML may load `/table-check.js` from this host. `script-src` is `'self'` only |
| 2026-10-16 | Active 1.3.10 | Every theme links `/apex.css` and one theme color sheet |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
