**file**: docs/requirements/requirement-html-dictionaries.md
**Status**: Active (Version 1.0.3)
**Area**: python
**Key**: `requirement-html-dictionaries`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the Dictionaries page. The studied document is the RuoYi list titled `字典管理`, with the dialog `修改类型` open over that list. The capture is `Screenshot from 2026-10-14 22-33-44.png`. That document is a search row, a toolbar, a table of dictionary types, a count line, and a dialog that edits one type. OpenRbac serves the list as `GET /dicts`.

The actions, the permission strings, and the text-report columns stay on `requirement-rbac-dictionaries`. The shell, the theme, and the ban on a script stay on `requirement-python-html-template`, `requirement-html-theme`, and `requirement-html-javascript`.

### 1.1 Human-facing

**In one sentence:** Dictionaries is a page with a search row, an add button for a value, a table of dictionary types, and a line that says how many rows are showing.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account opening Dictionaries | `admin` |
| The other role | The sidebar link | Catalog → Dictionaries → `/dicts` |
| Not this file | Who may list or add, and the audit row | `requirement-rbac-dictionaries` |

| Includes | Excludes |
|----------|----------|
| The search row, the add button, the six columns, and the count line | A second page at `/system/dict` or `/system/dict-data` |
| English labels for the studied Chinese labels | The Chinese labels copied onto the page |
| Add a dictionary value when `system:dict:add` is present | The dialog `修改类型`. The record does not edit a type and does not insert a type |
| The three seeded types `sys_user_sex`, `sys_normal_disable`, and `sys_notice_type` | The studied Chinese names, and the extra studied types, as seed data |

| Surface | What you open | What for |
|---------|---------------|----------|
| Sidebar | Catalog, then Dictionaries | `GET /dicts` |
| Page | `templates/dicts.vue` inside the shell | The search, the toolbar, and the table |
| Studied page | `字典管理` | The same list layout, under the OpenRbac path |

## 2. The studied page

| Piece in the studied document | OpenRbac |
|-------------------------------|----------|
| Sidebar item `字典管理`, drawn as the open item | Label `Dictionaries`, href `/dicts`, in the Catalog group. The open page is the active item |
| Tab strip `首页`, `岗位管理`, and `字典管理` | No tab strip. The sidebar is the way back to Home |
| Search `字典名称`, `字典类型`, `字典状态` with `所有`, and `创建时间` with `开始时间` and `结束时间` | `Dictionary name`, `Dictionary type`, `Status`, `Created`. The status choices are `All`, `Normal`, and `Disabled`. `Created` is the date range in `requirement-html-date-range`. The names stay `begin` and `end`. The form is `GET /dicts` |
| `搜索` and `重置` | `Search` submits the form. `Reset` is a link to `/dicts`. Each has an icon |
| Toolbar `新增` | `Add a dictionary value` when `system:dict:add` is allowed. It is a link to `?form=add` and it has an icon. It adds a value under a type that already exists. It does not insert a type |
| Toolbar `修改`, `删除`, `导出`, and `刷新缓存` | Omitted. `requirement-rbac-dictionaries` does not name edit, remove, export, or a cache refresh |
| The four icons at the right of the toolbar | Omitted. They are column and refresh chrome, and they need a script |
| A checkbox on the header and on each row | Omitted. The page does not delete many rows |
| Columns `字典主键`, `字典名称`, `字典类型`, `状态`, `备注`, `创建时间` | `Dictionary id`, `Dictionary name`, `Dictionary type`, `Status`, `Remark`, `Created`, in that order |
| `字典类型` drawn as a link | Text. It is not a link to `/system/dict-data` |
| `状态` shown as a green `正常` | An `el-tag`. Status `0` is `Normal`. Any other status is `Disabled` |
| Rows ordered by the dictionary id | The rows are ordered by `dict_id` |
| Column `操作` with `编辑`, `列表`, and `删除` | Omitted, with the toolbar edit and remove. `列表` does not open a second page. `dict-list` remains the value list |
| `显示第1到第10条记录，总共10条记录` | `Showing {first} to {last} of {total} records` |
| Dialog `修改类型` | Omitted. The record has no type edit |
| Dialog `字典名称`, required, studied value `用户性别` | Omitted with that dialog. `Dictionary name` on the search row is a filter |
| Dialog `字典类型`, required, studied value `sys_user_sex`, with the hint `数据存储中的Key值，如：sys_user_sex` | Omitted with that dialog, including the hint |
| Dialog status radios `正常` and `停用` | Omitted with that dialog. The table uses the tag in section 3 |
| Dialog `备注`, studied text `用户性别列表` | Omitted with that dialog. The column `Remark` shows `sys_dict_type.remark`. The seed leaves that column empty |
| Dialog `确定` and `关闭` | Omitted with that dialog |
| Studied names `用户性别`, `菜单状态`, `系统开关`, `任务状态`, `任务分组`, `系统是否`, `通知类型`, `通知状态`, `操作类型`, and `系统状态` | Not seed data. The seeded names stay `User sex`, `Normal or disabled`, and `Notice type` |

The studied document also loads Bootstrap, jQuery, Font Awesome, and a script block. Those stay out of the response. `Search`, `Reset`, and `Add a dictionary value` use the icon classes already painted for the users page: `user-btn-search`, `user-btn-reset`, and `user-btn-add`. The page does not add a new icon file. The studied groups for monitors, tools, the vendor site, and demos stay out of the menu.

## 3. The dictionaries page

The page is `src/OpenRbac/templates/dicts.vue`, inside the shell. The content root is `dict-page`. Every skin paints the same labels.

The rows come from `Catalog.dict_type_list` (`requirement-rbac-dictionaries`). The verb `dict-list` still returns every dictionary value. The page shows the filtered subset of types.

The search fields are `dict_name`, `dict_type`, `status`, `begin`, and `end`. An empty field does not filter. `dict_name` and `dict_type` keep a row whose stored value contains the trimmed text. The match is case-sensitive. `status` of `0` keeps status `0`. `status` of `1` keeps status `1`. Any other status value, including empty, means `All`. `begin` and `end` are dates `YYYY-MM-DD`. A `begin` of that shape keeps `create_time` on or after that date at `00:00:00`. An `end` of that shape keeps `create_time` on or before that date at `23:59:59`. A `begin` or `end` of any other shape matches no row. `Reset` drops every field. `Created` is the date range in `requirement-html-date-range`. The group word is `Created` followed by one space. The column header `Created` stays the table cell.

The six columns, in order, are `Dictionary id`, `Dictionary name`, `Dictionary type`, `Status`, `Remark`, and `Created`. `Created` is `create_time`. An empty `create_time` is an empty cell. An empty `remark` is an empty cell. `Status` `0` is `<span class="el-tag el-tag--success">Normal</span>`. Any other status is `<span class="el-tag el-tag--info">Disabled</span>`. The status is not an `el-switch`. The users switch stays on the users page. `Dictionary type` is text.

The count line uses the filtered list. When that list is empty, the line is `Showing 0 to 0 of 0 records`. Otherwise `first` is `1` and `last` equals `total`. The page does not add a page-size control.

`Add a dictionary value` is on the toolbar only when `system:dict:add` is allowed. It links to `/dicts?form=add` and keeps the search fields. The add panel is an `el-dialog`, drawn as the Apex card around the same fields. It is shown only when the query is `form=add` and the permission is allowed. The form posts `POST /dicts/add` with `csrf`, `dict_type`, `dict_label`, and `dict_value`. The field labels are `Type`, `Label`, and `Value`. The field rules and the audit row stay on `requirement-rbac-dictionaries`. A query that asks for the form without the permission omits the panel. The panel does not post `dict_name`, `remark`, or a type status.

Every theme links `/apex.css` and `/themes/<name>.css`. The markup is the Apex shell (`requirement-html-theme`).

## 4. Normative rules

1. **Destination.** Dictionaries **MUST** be `GET /dicts`. The template **MUST** be `dicts.vue` inside the shell. The product **MUST NOT** add a dictionary page at `/system/dict` or `/system/dict-data`.
2. **Menu.** An account with `system:dict:list` **MUST** see label `Dictionaries` and href `/dicts` in the Catalog group. The open page **MUST** be the active item in the HTML. An account without that permission **MUST NOT** see that link, and `GET /dicts` **MUST** refuse that account.
3. **Search.** The search form **MUST** be `method="get"` and `action="/dicts"`. It **MUST** include `Dictionary name`, `Dictionary type`, `Status`, `Created`, `Search`, and `Reset`. `Search` **MUST** use `user-btn-search`. `Reset` **MUST** use `user-btn-reset` and **MUST** be a link to `/dicts` with no query. The status control **MUST** offer `All`, `Normal`, and `Disabled`. `Created` **MUST** be the date range in `requirement-html-date-range`. Filtering **MUST** follow section 3. The signed-in `user_name` in the shell **MUST** stay the account name when a search field is filled.
4. **Table.** The table **MUST** show the six labels in section 3, in that order. The rows **MUST** be the filtered list, ordered by `dict_id`. The page **MUST** show the count line in section 3. `Status` **MUST** be the `el-tag` in section 3. It **MUST NOT** be an `el-switch`. `Dictionary type` **MUST** be text.
5. **Toolbar.** `Add a dictionary value` **MUST** be on the toolbar when `system:dict:add` is allowed, and **MUST** be omitted otherwise. It **MUST** use `user-btn-add` and **MUST** link to `form=add`. The add form **MUST** use `method="post"`, `action="/dicts/add"`, and the fields `csrf`, `dict_type`, `dict_label`, and `dict_value`. It **MUST** be omitted unless the query and the permission both allow it. The page **MUST NOT** show Edit, Remove, Export, Refresh cache, a row edit link, a row list link, a row remove link, or a checkbox column. The page **MUST NOT** show the dialog `修改类型`, and the add form **MUST NOT** post `dict_name`, `remark`, or a type status.
6. **Identity.** The shell on this page **MUST** show the signed-in `user_name`. Sign-out **MUST** be a form with `method="post"` and `action="/logout"` and a hidden `csrf` field.
7. **Skin.** The page **MUST** use `Settings.theme()`. Every skin **MUST** show the same search names, the same columns, the same toolbar, and the same form names.
8. **Plain page.** The response **MUST NOT** contain an `<iframe`, a `<script` tag, a `<style` block, `bootstrap.min.css`, `jquery`, or `font-awesome`. It **MUST NOT** contain a tab strip, a lock-screen control, a fullscreen control, or a notice badge filled by a separate request. It **MUST NOT** link to `ruoyi.vip` or `doc.ruoyi.vip`. It **MUST NOT** contain the studied Chinese labels from section 2.
9. **Neighbors.** Users, roles, menus, departments, and job titles **MUST** stay in Access. Parameters, dictionaries, and notices **MUST** stay in Catalog. The operation log, the login log, and online **MUST** stay in Audit. The studied groups for monitors, tools, and demos **MUST NOT** become menus.

## 5. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | An admin `/dicts` page contains `Dictionary name`, `Dictionary type`, `Status`, `Created`, `Search`, `Reset`, `Add a dictionary value`, `user-btn-search`, `user-btn-reset`, `user-btn-add`, and the six column labels in order |
| AC-2 | That page contains `User sex`, `sys_user_sex`, `Normal or disabled`, `sys_normal_disable`, `Notice type`, `sys_notice_type`, `class="el-tag el-tag--success"`, `Normal`, and `Showing 1 to 3 of 3 records`, with `User sex` before `Notice type` |
| AC-3 | That page's shell contains `href="/dicts"` and the signed-in `user_name` |
| AC-4 | `GET /dicts?dict_type=sys_user_sex` contains `User sex` and omits `Notice type`. `GET /dicts?dict_name=Notice` contains `Notice type` and omits `User sex`. `Reset` is a link to `/dicts` |
| AC-5 | `GET /dicts?status=1`, `GET /dicts?begin=2999-01-01`, and `GET /dicts?begin=yesterday` each contain `Showing 0 to 0 of 0 records` |
| AC-6 | `GET /dicts?form=add` for an account with `system:dict:add` contains `Add a dictionary value`, `action="/dicts/add"`, `name="dict_label"`, and `name="dict_value"`. The same page without that query omits `action="/dicts/add"`. The add form omits `name="remark"` |
| AC-7 | The dictionaries HTML contains no `<iframe`, no `<script`, no `bootstrap.min.css`, no `jquery`, no `font-awesome`, no checkbox column, no `修改类型`, and no Edit, Remove, Export, or Refresh cache button |
| AC-8 | Sign-out is `method="post"`, `action="/logout"`, and `name="csrf"` |
| AC-9 | An operator `GET /dicts` is refused with `Missing permission` |
| AC-10 | An Apex `/dicts` page keeps the six column labels and does not link `/element-plus.css` |
| AC-11 | The Created search control is `requirement-html-date-range`: `class="admlte-date-range"`, no `From` or `To` label, `name="begin"` `type="date"`, `name="end"` `type="date"`, and the arrow `→`. The column header stays `>Created<` |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Dictionaries | The OpenRbac page `GET /dicts` |
| Studied page | The RuoYi list whose title is `字典管理`, captured with `修改类型` open |
| Dictionaries link | The sidebar item labeled `Dictionaries` with href `/dicts` |
| Count line | `Showing {first} to {last} of {total} records` under the table |
| Toolbar | `Add a dictionary value` above the table |
| Date range | The Created search control. The markup is `requirement-html-date-range` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Dictionaries page UI. The studied page `字典管理` is `/dicts`. The capture is `Screenshot from 2026-10-14 22-33-44.png` |
| 2026-10-15 | Active 1.0.1 | The Created search is the side-by-side date range in `requirement-html-date-range` |
| 2026-10-15 | Active 1.0.2 | The Created search shows no From or To label |
| 2026-10-16 | Active 1.0.3 | Every skin uses the Apex card for the add panel |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
