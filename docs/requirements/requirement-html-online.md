**file**: docs/requirements/requirement-html-online.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-html-online`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the Online page. The studied document is the RuoYi list titled `在线用户`. The capture is `Screenshot from 2026-10-14 22-44-54.png`. That document is a search row, a toolbar, a table of signed-in sessions, and a count line. OpenRbac serves the list as `GET /online`.

Who may open the list, who may force a logout, and the 8-character token prefix stay on `Catalog.online_list`, `Catalog.online_logout`, and `requirement-web-interface`. The shell, the theme, and the ban on a script stay on `requirement-python-html-template`, `requirement-html-theme`, and `requirement-html-javascript`.

### 1.1 Human-facing

**In one sentence:** Online is a page with a search row, a table of signed-in sessions, a force-logout button on each row, and a line that says how many rows are showing.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account opening Online | `admin` |
| The other role | The sidebar link | Audit → Online → `/online` |
| Not this file | Who may list or force a logout, and the token prefix rule | `requirement-web-interface` |

| Includes | Excludes |
|----------|----------|
| The search row, the seven columns, the row button, and the count line | A second page at `/monitor/online` |
| English labels for the studied Chinese labels | The Chinese labels copied onto the page |
| The stored login name, host, login time, and last access | A department, a login location, a browser, and an operating system. `sys_session` does not store those |
| `Search`, `Reset`, and `Force logout` on the row | A toolbar button that logs out many sessions. The record does not name that action |

| Surface | What you open | What for |
|---------|---------------|----------|
| Sidebar | Audit, then Online | `GET /online` |
| Page | `templates/online.vue` inside the shell | The search and the table |
| Studied page | `在线用户` | The same list layout, under the OpenRbac path |

## 2. The studied page

The capture is the studied document. Where `views/monitor/online/index.vue` uses another label or another column order, the capture wins. The 8-character token prefix in `requirement-web-interface` still wins over the longer truncation in the capture.

| Piece in the studied document | OpenRbac |
|-------------------------------|----------|
| Sidebar item `在线用户`, drawn as the open item under `系统监控` | Label `Online`, href `/online`, in the Audit group. The open page is the active item |
| Tab strip `首页`, `岗位管理`, `字典管理`, `参数设置`, `通知公告`, `操作日志`, `登录日志`, and `在线用户` | No tab strip. The sidebar is the way back to Home |
| Search `登录地址` and `登录名称` | `Login address` and `Login name`. The form is `GET /online`. There is no status choice |
| `搜索` and `重置` | `Search` submits the form. `Reset` is a link to `/online`. Each has an icon |
| Toolbar `强退` | Omitted. One row has its own `Force logout`. The page does not post many tokens |
| The icons at the right of the toolbar | Omitted. They are column and refresh chrome, and they need a script |
| A checkbox on the header and on each row | Omitted. The page does not choose many rows |
| Sort mark on `最后访问时间` | Omitted as a control. The order is fixed. It is `last_access` descending |
| Column `序号` | `Number`. It is the place of the row in the filtered list, starting at `1` |
| Column `会话编号`, shown truncated | `Session`. The cell is the first 8 characters of `token`. The full token is the hidden field on the row form |
| Columns `登录名称`, `主机`, `会话状态`, `登录时间`, `最后访问时间` | `Login name`, `Host`, `Session status`, `Login time`, `Last access` |
| Columns `部门名称`, `登录地点`, `浏览器`, `操作系统` | Omitted. A session row has no department, login location, browser, or operating system. Those last three belong to the login log |
| `会话状态` shown as a green `在线` | An `el-tag`. Every listed row is `<span class="el-tag el-tag--success">Online</span>` |
| Column `操作` with a red `强退` | `Action`. The button text is `Force logout` and the same 8-character prefix. It is shown when `monitor:online:forceLogout` is allowed |
| Studied row `admin`, `研发部门`, `127.0.0.1`, `内网IP`, `Firefox 156.0`, `Linux` | Not required text. The page shows the stored session columns |
| `显示第 1 到第 1 条记录，总共 1 条记录` | `Showing {first} to {last} of {total} records` |

The studied document also loads Bootstrap, jQuery, Font Awesome, and a script block. Those stay out of the response. `Search` and `Reset` use the icon classes already painted for the users page: `user-btn-search` and `user-btn-reset`. `Force logout` adds no icon file. The studied groups for scheduled jobs, data monitors, service monitors, cache monitors, tools, the vendor site, and demos stay out of the menu. Online stays in Audit.

## 3. The online page

The page is `src/OpenRbac/templates/online.vue`, inside the shell. The content root is `online-page`. Every skin paints the same labels.

The rows come from `Catalog.online_list`. Each row includes `token`, `user_id`, `user_name`, `ipaddr`, `surface`, `login_time`, and `last_access`. The verb `online-list` still prints `token`, `user_name`, `ipaddr`, `surface`, and `login_time`, and the terminal list still prints the full token. The page shows the filtered subset of the list the catalog method returns. The page does not show `surface`, `user_agent`, or `csrf`.

The search fields are `ipaddr` and `user_name`. An empty field does not filter. Each field keeps a row whose stored value contains the trimmed text. The match is case-sensitive. `Reset` drops every field.

The seven columns, in order, are `Number`, `Session`, `Login name`, `Host`, `Session status`, `Login time`, and `Last access`. `Number` is the place in the filtered list, starting at `1`. `Session` is the first 8 characters of `token`. A token shorter than 8 characters shows the whole token. `Login name` is `user_name`. `Host` is `ipaddr`. `Login time` is `login_time`. `Last access` is `last_access`. An empty `ipaddr`, `login_time`, or `last_access` is an empty cell. `Session status` is `<span class="el-tag el-tag--success">Online</span>` on every row. The status is not an `el-switch`. The users switch stays on the users page.

`Action` is the last column when `monitor:online:forceLogout` is allowed, and it is omitted otherwise. The cell is one form. The form posts `POST /online/logout` with hidden `csrf` and hidden `token`. The hidden `token` is the full session token. The button uses `type="danger"`. Its text is `Force logout` and the same prefix the `Session` cell shows. The messages `A session token is required.` and `That session is not online.` stay on `Catalog.online_logout`.

The rows keep the order `online-list` returns: `last_access` descending. The count line uses the filtered list. When that list is empty, the line is `Showing 0 to 0 of 0 records`. Otherwise `first` is `1` and `last` equals `total`. One session is `Showing 1 to 1 of 1 records`. The page does not add a page-size control.

Every theme links `/apex.css` and `/themes/<name>.css`. The markup is the Apex shell (`requirement-html-theme`).

## 4. Normative rules

1. **Destination.** Online **MUST** be `GET /online`. The template **MUST** be `online.vue` inside the shell. The product **MUST NOT** add an online page at `/monitor/online`.
2. **Menu.** An account with `monitor:online:list` **MUST** see label `Online` and href `/online` in the Audit group. The open page **MUST** be the active item in the HTML. An account without that permission **MUST NOT** see that link, and `GET /online` **MUST** refuse that account.
3. **Search.** The search form **MUST** be `method="get"` and `action="/online"`. It **MUST** include `Login address`, `Login name`, `Search`, and `Reset`. `Search` **MUST** use `user-btn-search`. `Reset` **MUST** use `user-btn-reset` and **MUST** be a link to `/online` with no query. Filtering **MUST** follow section 3. The signed-in `user_name` in the shell **MUST** stay the account name when a search field is filled. The verb `online-list` **MUST** still return every session.
4. **Table.** The table **MUST** show the seven labels in section 3, in that order. The rows **MUST** be the filtered list, in the `last_access` descending order from section 3. The page **MUST** show the count line in section 3. `Session` **MUST** be the 8-character prefix. The full token **MUST** appear only as the hidden `token` field. `Session status` **MUST** be the `el-tag` in section 3. It **MUST NOT** be an `el-switch`. The page **MUST NOT** show a department, a login location, a browser, an operating system, `surface`, `user_agent`, or `csrf` as a column.
5. **Row action.** `Force logout` **MUST** be on each row when `monitor:online:forceLogout` is allowed, and **MUST** be omitted otherwise. The form **MUST** use `method="post"`, `action="/online/logout"`, and the hidden fields `csrf` and `token`. The button **MUST** use `type="danger"`. Its text **MUST** be `Force logout` and the prefix from rule 4. The page **MUST NOT** show a toolbar force-logout, a checkbox column, or a control that sorts a column. The page **MUST NOT** add an icon file. `Search` and `Reset` **MUST** use the icon classes in section 2.
6. **Identity.** The shell on this page **MUST** show the signed-in `user_name`. Sign-out **MUST** be a form with `method="post"` and `action="/logout"` and a hidden `csrf` field.
7. **Skin.** The page **MUST** use `Settings.theme()`. Every skin **MUST** show the same search names, the same columns, and the same button text. The button **MUST** be `btn-danger`.
8. **Plain page.** The response **MUST NOT** contain an `<iframe`, a `<script` tag, a `<style` block, `bootstrap.min.css`, `jquery`, or `font-awesome`. It **MUST NOT** contain a tab strip, a lock-screen control, a fullscreen control, or a notice badge filled by a separate request. It **MUST NOT** link to `ruoyi.vip` or `doc.ruoyi.vip`. It **MUST NOT** contain the studied Chinese labels from section 2.
9. **Neighbors.** Users, roles, menus, departments, and job titles **MUST** stay in Access. Parameters, dictionaries, and notices **MUST** stay in Catalog. The operation log, the login log, and online **MUST** stay in Audit. The studied groups for monitors, tools, and demos **MUST NOT** become menus.

## 5. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | An admin `/online` page contains `Login address`, `Login name`, `Search`, `Reset`, `user-btn-search`, `user-btn-reset`, the seven column labels in order, `Action`, and `Force logout` |
| AC-2 | That page contains `class="el-tag el-tag--success"`, `Online`, and `Showing 1 to 1 of 1 records` when the signed-in session is the only row. The `Session` cell and the button show the same 8-character prefix |
| AC-3 | That page's logout form is `method="post"`, `action="/online/logout"`, with hidden `name="csrf"` and hidden `name="token"`. The button includes `el-button--danger` |
| AC-4 | That page's shell contains `href="/online"` and the signed-in `user_name` |
| AC-5 | `GET /online?user_name=not-a-session` contains `Showing 0 to 0 of 0 records`. `Reset` is a link to `/online` |
| AC-6 | The online HTML contains no `<iframe`, no `<script`, no `bootstrap.min.css`, no `jquery`, no `font-awesome`, no checkbox column, and no column label `Department`, `Login location`, `Browser`, `Operating system`, or `Surface` |
| AC-7 | Sign-out is `method="post"`, `action="/logout"`, and `name="csrf"` |
| AC-8 | An operator `GET /online` is refused with `Missing permission` |
| AC-9 | An Apex `/online` page keeps the seven column labels, includes `btn-danger`, and does not link `/element-plus.css` |
| AC-10 | An account with `monitor:online:list` and without `monitor:online:forceLogout` gets the seven column labels and omits `action="/online/logout"` |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Online | The OpenRbac page `GET /online` |
| Studied page | The RuoYi list whose title is `在线用户`, captured in `Screenshot from 2026-10-14 22-44-54.png` |
| Online link | The sidebar item labeled `Online` with href `/online` |
| Session | The first 8 characters of the session `token` |
| Count line | `Showing {first} to {last} of {total} records` under the table |
| Force logout | The row button that posts `POST /online/logout` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Online page UI. The studied page `在线用户` is `/online`. The capture is `Screenshot from 2026-10-14 22-44-54.png` |
| 2026-10-16 | Active 1.0.1 | Every skin shows the same columns. The force-logout button is `btn-danger` |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
