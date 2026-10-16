**file**: docs/requirements/requirement-html-login-log.md
**Status**: Active (Version 1.0.3)
**Area**: python
**Key**: `requirement-html-login-log`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the Login log page. The studied document is the RuoYi list titled `登录日志`. The capture is `Screenshot from 2026-10-14 22-41-13.png`. That document is a search row, a toolbar, a table of login attempts, and a count line. OpenRbac serves the list as `GET /login-log`.

Who may open the list, and the row a sign-in writes, stay on `requirement-rbac`. The shell, the theme, and the ban on a script stay on `requirement-python-html-template`, `requirement-html-theme`, and `requirement-html-javascript`.

### 1.1 Human-facing

**In one sentence:** Login log is a page with a search row, a table of login attempts, and a line that says how many rows are showing.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account opening Login log | `admin` |
| The other role | The sidebar link | Audit → Login log → `/login-log` |
| Not this file | Who may list, and the row a sign-in writes | `requirement-rbac` |

| Includes | Excludes |
|----------|----------|
| The search row, the nine columns, and the count line | A second page at `/monitor/logininfor` |
| English labels for the studied Chinese labels | The Chinese labels copied onto the page |
| The stored address, place, browser, system, status, and message | A place lookup, and a parse of the browser string into a product name |
| `Search` and `Reset` | Delete, clear, unlock, and export. The record does not name those actions |

| Surface | What you open | What for |
|---------|---------------|----------|
| Sidebar | Audit, then Login log | `GET /login-log` |
| Page | `templates/login-log.vue` inside the shell | The search and the table |
| Studied page | `登录日志` | The same list layout, under the OpenRbac path |

## 2. The studied page

The capture is the studied document. Where `views/monitor/logininfor/index.vue` uses another label or another column order, the capture wins.

| Piece in the studied document | OpenRbac |
|-------------------------------|----------|
| Sidebar item `登录日志`, drawn as the open item under `日志管理` | Label `Login log`, href `/login-log`, in the Audit group. The open page is the active item |
| Tab strip `首页`, `岗位管理`, `字典管理`, `参数设置`, `通知公告`, `操作日志`, and `登录日志` | No tab strip. The sidebar is the way back to Home |
| Search `登录地址`, `登录名称`, `登录状态` with `所有`, and `登录时间` with `开始时间` and `结束时间` | `Login address`, `Login name`, `Login status`, `Login time`. The status choices are `All`, `Success`, and `Failed`. `Login time` is the date range in `requirement-html-date-range`. The names stay `begin` and `end`. The form is `GET /login-log` |
| `搜索` and `重置` | `Search` submits the form. `Reset` is a link to `/login-log`. Each has an icon |
| Toolbar `删除`, `清空`, `解锁`, and `导出` | Omitted. `requirement-rbac` does not name remove, clean, unlock, or export. The product has no locked account to unlock |
| The four icons at the right of the toolbar | Omitted. They are column and refresh chrome, and they need a script |
| A checkbox on the header and on each row | Omitted. The page does not delete many rows |
| Sort marks on `登录名称` and `登录时间` | Omitted. The order is fixed. It is `info_id` descending |
| Columns `访问编号`, `登录名称`, `登录地址`, `登录地点`, `浏览器`, `操作系统`, `登录状态`, `操作信息`, `登录时间` | `Access id`, `Login name`, `Login address`, `Login location`, `Browser`, `Operating system`, `Login status`, `Message`, `Login time`, in that order |
| `登录状态` shown as a green `成功` | An `el-tag`. Status `0` is `Success`. Status `1` is `Failed` |
| Studied row `100`, `admin`, `127.0.0.1`, `内网IP`, `Firefox 156.0`, `Linux`, `成功`, `登录成功` | Not required text. The page shows the stored columns. It does not look up a place name, and it does not parse a browser string into a product name |
| `显示第1到第1条记录，总共1条记录` | `Showing {first} to {last} of {total} records` |

The studied document also loads Bootstrap, jQuery, Font Awesome, and a script block. Those stay out of the response. `Search` and `Reset` use the icon classes already painted for the users page: `user-btn-search` and `user-btn-reset`. The page does not add a new icon file. The studied groups for monitors, tools, the vendor site, and demos stay out of the menu.

## 3. The login log page

The page is `src/OpenRbac/templates/login-log.vue`, inside the shell. The content root is `login-page`. Every skin paints the same labels.

The rows come from `Catalog.login_log`. Each row includes `info_id`, `user_name`, `ipaddr`, `login_location`, `browser`, `os`, `status`, `msg`, and `login_time`. The verb `login-log` still prints `info_id`, `user_name`, `ipaddr`, `status`, `msg`, and `login_time`. The page shows the filtered subset of the list the catalog method returns.

The search fields are `ipaddr`, `user_name`, `status`, `begin`, and `end`. An empty field does not filter. `ipaddr` and `user_name` keep a row whose stored value contains the trimmed text. The match is case-sensitive. `status` of `0` keeps status `0`. `status` of `1` keeps status `1`. Any other status value, including empty, means `All`. `begin` and `end` are dates `YYYY-MM-DD`. A `begin` of that shape keeps `login_time` on or after that date at `00:00:00`. An `end` of that shape keeps `login_time` on or before that date at `23:59:59`. A `begin` or `end` of any other shape matches no row. `Reset` drops every field. `Login time` is the date range in `requirement-html-date-range`. The group word is `Login time` followed by one space. The column header `Login time` stays the table cell.

The nine columns, in order, are `Access id`, `Login name`, `Login address`, `Login location`, `Browser`, `Operating system`, `Login status`, `Message`, and `Login time`. `Access id` is `info_id`. `Login name` is `user_name`. `Login address` is `ipaddr`. `Login location` is `login_location`. `Browser` is `browser`. `Operating system` is `os`. `Message` is `msg`. `Login time` is `login_time`. An empty `login_location`, `browser`, `os`, `msg`, or `login_time` is an empty cell. `Login status` `0` is `<span class="el-tag el-tag--success">Success</span>`. `Login status` `1` is `<span class="el-tag el-tag--danger">Failed</span>`. Any other status is `<span class="el-tag el-tag--danger">Failed</span>`. The status is not an `el-switch`. The users switch stays on the users page.

The rows are ordered by `info_id` descending. The count line uses the filtered list. When that list is empty, the line is `Showing 0 to 0 of 0 records`. Otherwise `first` is `1` and `last` equals `total`. The page does not add a page-size control. The page has no toolbar.

Every theme links `/apex.css` and `/themes/<name>.css`. The markup is the Apex shell (`requirement-html-theme`).

## 4. Normative rules

1. **Destination.** Login log **MUST** be `GET /login-log`. The template **MUST** be `login-log.vue` inside the shell. The product **MUST NOT** add a login-log page at `/monitor/logininfor`.
2. **Menu.** An account with `monitor:logininfor:list` **MUST** see label `Login log` and href `/login-log` in the Audit group. The open page **MUST** be the active item in the HTML. An account without that permission **MUST NOT** see that link, and `GET /login-log` **MUST** refuse that account.
3. **Search.** The search form **MUST** be `method="get"` and `action="/login-log"`. It **MUST** include `Login address`, `Login name`, `Login status`, `Login time`, `Search`, and `Reset`. `Search` **MUST** use `user-btn-search`. `Reset` **MUST** use `user-btn-reset` and **MUST** be a link to `/login-log` with no query. The status control **MUST** offer `All`, `Success`, and `Failed`. `Login time` **MUST** be the date range in `requirement-html-date-range`. Filtering **MUST** follow section 3. The signed-in `user_name` in the shell **MUST** stay the account name when a search field is filled.
4. **Table.** The table **MUST** show the nine labels in section 3, in that order. The rows **MUST** be the filtered list, ordered by `info_id` descending. The page **MUST** show the count line in section 3. `Login status` **MUST** be the `el-tag` in section 3. It **MUST NOT** be an `el-switch`. `Message` **MUST** be the stored `msg`.
5. **Toolbar.** The page **MUST NOT** show Delete, Clear, Unlock, Export, a checkbox column, or a control that sorts a column. The page **MUST NOT** add an icon file. `Search` and `Reset` **MUST** use the icon classes in section 2.
6. **Identity.** The shell on this page **MUST** show the signed-in `user_name`. Sign-out **MUST** be a form with `method="post"` and `action="/logout"` and a hidden `csrf` field.
7. **Skin.** The page **MUST** use `Settings.theme()`. Every skin **MUST** show the same search names and the same columns.
8. **Plain page.** The response **MUST NOT** contain an `<iframe`, a `<script` tag, a `<style` block, `bootstrap.min.css`, `jquery`, or `font-awesome`. It **MUST NOT** contain a tab strip, a lock-screen control, a fullscreen control, or a notice badge filled by a separate request. It **MUST NOT** link to `ruoyi.vip` or `doc.ruoyi.vip`. It **MUST NOT** contain the studied Chinese labels from section 2.
9. **Neighbors.** Users, roles, menus, departments, and job titles **MUST** stay in Access. Parameters, dictionaries, and notices **MUST** stay in Catalog. The operation log, the login log, and online **MUST** stay in Audit. The studied groups for monitors, tools, and demos **MUST NOT** become menus.

## 5. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | An admin `/login-log` page contains `Login address`, `Login name`, `Login status`, `Login time`, `Search`, `Reset`, `user-btn-search`, `user-btn-reset`, and the nine column labels in order |
| AC-2 | That page's shell contains `href="/login-log"` and the signed-in `user_name` |
| AC-3 | A row with status `0` contains `class="el-tag el-tag--success"` and `Success`. A row with status `1` contains `class="el-tag el-tag--danger"` and `Failed`. The status cell is not an `el-switch` |
| AC-4 | `GET /login-log?user_name=admin` keeps a stored `admin` attempt and omits a stored attempt whose name does not contain `admin`. `Reset` is a link to `/login-log` |
| AC-5 | `GET /login-log?begin=2999-01-01` and `GET /login-log?begin=yesterday` each contain `Showing 0 to 0 of 0 records` |
| AC-6 | The login log HTML contains no `<iframe`, no `<script`, no `bootstrap.min.css`, no `jquery`, no `font-awesome`, no checkbox column, and no Delete, Clear, Unlock, or Export button |
| AC-7 | Sign-out is `method="post"`, `action="/logout"`, and `name="csrf"` |
| AC-8 | An operator `GET /login-log` contains `Login address`. A lead `GET /login-log` is refused with `Missing permission` |
| AC-9 | An Apex `/login-log` page keeps the nine column labels and does not link `/element-plus.css` |
| AC-10 | The Login time search control is `requirement-html-date-range`: `class="admlte-date-range"`, no `From` or `To` label, `name="begin"` `type="date"`, `name="end"` `type="date"`, and the arrow `→`. The column header stays `>Login time<`. `GET /login-log?begin=2999-01-01` sets `min="2999-01-01"` on the end input and omits `max` |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Login log | The OpenRbac page `GET /login-log` |
| Studied page | The RuoYi list whose title is `登录日志`, captured in `Screenshot from 2026-10-14 22-41-13.png` |
| Login log link | The sidebar item labeled `Login log` with href `/login-log` |
| Access id | The `info_id` column. It is not the Access menu |
| Count line | `Showing {first} to {last} of {total} records` under the table |
| Message | The stored `msg` for that attempt |
| Date range | The Login time search control. The markup is `requirement-html-date-range` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Login log page UI. The studied page `登录日志` is `/login-log`. The capture is `Screenshot from 2026-10-14 22-41-13.png` |
| 2026-10-15 | Active 1.0.1 | The Login time search is the side-by-side date range in `requirement-html-date-range` |
| 2026-10-15 | Active 1.0.2 | The Login time search shows no From or To label |
| 2026-10-16 | Active 1.0.3 | Every skin shows the same search names and the same columns |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
