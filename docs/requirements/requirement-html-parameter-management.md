**file**: docs/requirements/requirement-html-parameter-management.md
**Status**: Active (Version 1.0.5)
**Area**: python
**Key**: `requirement-html-parameter-management`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the Parameter Management page. The studied document is the RuoYi list titled `参数设置`, with the dialog `修改参数` open over that list. The capture is `Screenshot from 2026-10-14 22-37-24.png`. That document is a search row, a toolbar, a table of parameters, a count line, and a dialog that changes one parameter. OpenRbac serves the list as `GET /configs`.

The actions, the permission strings, and the text-report columns stay on `requirement-rbac-parameters`. The shell, the theme, and the ban on a script stay on `requirement-python-html-template`, `requirement-html-theme`, and `requirement-html-javascript`.

### 1.1 Human-facing

**In one sentence:** Parameters is a page with a search row, a change button, a table of parameters, and a line that says how many rows are showing.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account opening Parameters | `admin` |
| The other role | The sidebar link | Catalog → Parameters → `/configs` |
| Not this file | Who may list, change, or add, and the audit row | `requirement-rbac-parameters` |

| Includes | Excludes |
|----------|----------|
| The search row, the change button, the eight columns, and the count line | A second page at `/system/config` |
| English labels for the studied Chinese labels | The Chinese labels copied onto the page |
| Change a parameter when `system:config:edit` is present | An add form on this page. Add stays on the verb and on setup row 213 |
| The four seeded keys | The studied Chinese names, the studied remarks, and the extra studied keys, as seed data |

| Surface | What you open | What for |
|---------|---------------|----------|
| Sidebar | Catalog, then Parameters | `GET /configs` |
| Page | `templates/configs.vue` inside the shell | The search, the toolbar, and the table |
| Studied page | `参数设置` | The same list layout, under the OpenRbac path |

## 2. The studied page

| Piece in the studied document | OpenRbac |
|-------------------------------|----------|
| Sidebar item `参数设置`, drawn as the open item | Label `Parameters`, href `/configs`, in the Catalog group. The open page is the active item |
| Tab strip `首页`, `岗位管理`, `字典管理`, and `参数设置` | No tab strip. The sidebar is the way back to Home |
| Search `参数名称`, `参数键名`, `系统内置` with `所有`, and `创建时间` with `开始时间` and `结束时间` | `Parameter name`, `Parameter key`, `Built-in`, `Created`. The built-in choices are `All`, `Yes`, and `No`. `Created` is the date range in `requirement-html-date-range`. The names stay `begin` and `end`. The form is `GET /configs` |
| `搜索` and `重置` | `Search` submits the form. `Reset` is a link to `/configs`. Each has an icon |
| Toolbar `修改` | `Change` when `system:config:edit` is allowed. It submits the chosen parameter and it has an icon |
| Toolbar `新增` | Omitted. This page does not post an add action. Add stays on `config-add` and on setup row 213 |
| Toolbar `删除`, `导出`, and `刷新缓存` | Omitted. `requirement-rbac-parameters` does not name remove, export, or a cache refresh. The product reads `sys_config` when it uses a key |
| The four icons at the right of the toolbar | Omitted. They are column and refresh chrome, and they need a script |
| A checkbox on the header and on each row | When edit is allowed, the header is a checkbox `aria-label="check all"` with no `name`, and each row is a checkbox named `config_id`. The cells use `table-check-col`. `/table-check.js` checks the row boxes in that table. The page does not delete many rows |
| Columns `参数主键`, `参数名称`, `参数键名`, `参数键值`, `系统内置`, `备注`, `创建时间`, `操作` | `Parameter id`, `Parameter name`, `Parameter key`, `Parameter value`, `Built-in`, `Remark`, `Created`, `Action`, in that order |
| `系统内置` shown as a green `是` | An `el-tag`. `Y` is `Yes`. Any other `config_type` is `No` |
| Rows ordered by the parameter id | The rows are ordered by `config_id` |
| Column `操作` with `编辑` and `删除` | `Change` on the row when edit is allowed. `删除` is omitted with the toolbar remove |
| `显示第1到第10条记录，总共11条记录` and `每页显示` | `Showing {first} to {last} of {total} records`. The page does not add a page-size control |
| Dialog `修改参数` | `Change a parameter`, when the query and the permission both allow it |
| Dialog `参数名称`, required, studied value `用户管理-账号初始密码` | Text of the stored `config_name`. It is not an input. Change does not rename the parameter. The seeded name for that key is `Initial password` |
| Dialog `参数键名`, required, studied value `sys.user.initPassword` | Text of the stored `config_key`. The form posts that key in a hidden field. The reader does not replace the key |
| Dialog `参数键值`, required, a textarea, studied value `123456` | A textarea named `config_value`, filled with the stored value |
| Dialog `系统内置` radios `是` and `否`, with `是` selected | Omitted from the dialog. The table uses the tag in section 3. Change does not set `config_type` |
| Dialog `备注`, studied text `初始化密码 123456` | Omitted from the dialog. The column `Remark` shows `remark`. The seed leaves that column empty. Change does not set `remark` |
| Dialog `确定` and `关闭` | `Change` submits the form. `Close` is a link back to the list without `form=edit`, and it keeps the search |
| Studied names `主框架页-默认皮肤样式名称`, `用户管理-账号初始密码`, `主框架页-侧边栏主题`, `账号自助-是否开启用户注册功能`, `用户管理-密码字符范围`, `用户管理-初始密码修改策略`, `用户管理-账号密码更新周期`, `主框架页-菜单导航显示风格`, `主框架页-是否开启页脚`, and `主框架页-是否开启页签` | Not seed data. The seeded names stay `Skin name`, `Initial password`, `Captcha`, and `Registration` |

The studied document also loads Bootstrap, jQuery, Font Awesome, and a script block. Those stay out of the response. `Search`, `Reset`, and `Change` use the icon classes already painted for the users page: `user-btn-search`, `user-btn-reset`, and `user-btn-edit`. The page does not add a new icon file. The studied groups for monitors, tools, the vendor site, and demos stay out of the menu.

## 3. The parameters page

The page is `src/OpenRbac/templates/configs.vue`, inside the shell. The content root is `config-page`. Every skin paints the same labels.

The rows come from `Catalog.config_list` (`requirement-rbac-parameters`). The verb `config-list` still returns every parameter. The page shows the filtered subset.

The search fields are `config_name`, `config_key`, `config_type`, `begin`, and `end`. An empty field does not filter. `config_name` and `config_key` keep a row whose stored value contains the trimmed text. The match is case-sensitive. `config_type` of `Y` keeps `Y`. `config_type` of `N` keeps `N`. Any other built-in value, including empty, means `All`. `Yes` submits `Y`. `No` submits `N`. `begin` and `end` are dates `YYYY-MM-DD`. A `begin` of that shape keeps `create_time` on or after that date at `00:00:00`. An `end` of that shape keeps `create_time` on or before that date at `23:59:59`. A `begin` or `end` of any other shape matches no row. An empty `create_time` matches a date only when both `begin` and `end` are empty. `Reset` drops every field. `Created` is the date range in `requirement-html-date-range`. The group word is `Created` followed by one space. The column header `Created` stays the table cell.

The search form is its own `GET` form. The toolbar and the table are a second `GET` form to `/configs`. Hidden fields on that form keep the search. The edit target is `config_id`, so choosing a row does not replace the search field `config_key`.

The eight columns, in order, are `Parameter id`, `Parameter name`, `Parameter key`, `Parameter value`, `Built-in`, `Remark`, `Created`, and `Action`. The check-all checkbox sits in front of them only when edit is allowed. `Created` is `create_time`. An empty `create_time` is an empty cell. An empty `remark` is an empty cell. `Built-in` `Y` is `<span class="el-tag el-tag--success">Yes</span>`. Any other `config_type` is `<span class="el-tag el-tag--info">No</span>`. Built-in is not an `el-switch`. The users switch stays on the users page. `Parameter value` is the full `config_value`.

The count line uses the filtered list. When that list is empty, the line is `Showing 0 to 0 of 0 records`. Otherwise `first` is `1` and `last` equals `total`. The page does not add a page-size control.

`Change` is on the toolbar only when `system:config:edit` is allowed. It uses `user-btn-edit` and submits `form=edit` with the chosen `config_id`. The row link `Change` uses `user-btn-edit` and links to `form=edit` with that `config_id`, and it keeps the search fields. Submitting change with no chosen id shows `Choose a parameter.` An id outside the account's unfiltered list shows `Unknown parameter`. Either sentence omits the change panel.

The change panel is an `el-dialog`, drawn as the Apex card around the same fields. It is shown only when the query is `form=edit`, the permission is allowed, and that `config_id` is in the unfiltered list. The title is `Change a parameter`. The panel shows the stored `config_name` and `config_key` as text. The form posts `POST /configs/set` with `csrf`, the hidden `config_key` of that row, and `config_value`. `config_value` is a textarea filled with the stored value. `Close` links to `/configs` with the search fields and without `form`. The field rules and the audit row stay on `requirement-rbac-parameters`. A query that asks for the form without the permission omits the panel. The panel does not post `config_name`, `config_type`, or `remark`.

Every theme links `/apex.css` and `/themes/<name>.css`. The markup is the Apex shell (`requirement-html-theme`).

## 4. Normative rules

1. **Destination.** Parameter Management **MUST** be `GET /configs`. The template **MUST** be `configs.vue` inside the shell. The product **MUST NOT** add a parameter page at `/system/config`.
2. **Menu.** An account with `system:config:list` **MUST** see label `Parameters` and href `/configs` in the Catalog group. The open page **MUST** be the active item in the HTML. An account without that permission **MUST NOT** see that link, and `GET /configs` **MUST** refuse that account.
3. **Search.** The search form **MUST** be `method="get"` and `action="/configs"`. It **MUST** include `Parameter name`, `Parameter key`, `Built-in`, `Created`, `Search`, and `Reset`. `Search` **MUST** use `user-btn-search`. `Reset` **MUST** use `user-btn-reset` and **MUST** be a link to `/configs` with no query. The built-in control **MUST** offer `All`, `Yes`, and `No`. `Created` **MUST** be the date range in `requirement-html-date-range`. Filtering **MUST** follow section 3. The signed-in `user_name` in the shell **MUST** stay the account name when a search field is filled.
4. **Table.** The table **MUST** show the eight labels in section 3, in that order. A checkbox with `aria-label="check all"`, class `table-check`, and no `name` **MUST** be the first header when edit is allowed, and **MUST** be omitted otherwise. Each row in that column **MUST** be a checkbox named `config_id`. The header cell and each row cell **MUST** use `table-check-col`. The header **MUST NOT** be the word `Choose`. When the column is shown, the document **MUST** include `<script src="/table-check.js"></script>`, and that file **MUST** check the row boxes in that table. When the column is omitted, the document **MUST NOT** include a script tag. Both stylesheets **MUST** center `.table-check-col`. The rows **MUST** be the filtered list, ordered by `config_id`. The page **MUST** show the count line in section 3. `Built-in` **MUST** be the `el-tag` in section 3. It **MUST NOT** be an `el-switch`.
5. **Toolbar.** `Change` **MUST** be on the toolbar when `system:config:edit` is allowed, and **MUST** be omitted otherwise. It **MUST** use `user-btn-edit` and **MUST** submit the chosen `config_id` with the search fields kept. The row link `Change` **MUST** remain when that permission is allowed. The change form **MUST** use `method="post"`, `action="/configs/set"`, and the fields `csrf`, `config_key`, and `config_value`. `config_value` **MUST** be a textarea. The form **MUST** be omitted unless the query and the permission both allow it, and the `config_id` is in the unfiltered list. The form **MUST NOT** post `config_name`, `config_type`, or `remark`. The page **MUST NOT** post an add action. The page **MUST NOT** show Add, Remove, Delete, Export, Refresh cache, a row remove link, or a control that deletes many rows.
6. **Identity.** The shell on this page **MUST** show the signed-in `user_name`. Sign-out **MUST** be a form with `method="post"` and `action="/logout"` and a hidden `csrf` field.
7. **Skin.** The page **MUST** use `Settings.theme()`. Every skin **MUST** show the same search names, the same columns, the same toolbar, and the same form names.
8. **Plain page.** The response **MUST NOT** contain an `<iframe`, a `<style` block, `bootstrap.min.css`, `jquery`, or `font-awesome`. The only `<script` tag is `<script src="/table-check.js"></script>`, and only when the checkbox column is shown. It **MUST NOT** contain a tab strip, a lock-screen control, a fullscreen control, or a notice badge filled by a separate request. It **MUST NOT** link to `ruoyi.vip` or `doc.ruoyi.vip`. It **MUST NOT** contain the studied Chinese labels from section 2.
9. **Neighbors.** Users, roles, menus, departments, and job titles **MUST** stay in Access. Parameters, dictionaries, and notices **MUST** stay in Catalog. The operation log, the login log, and online **MUST** stay in Audit. The studied groups for monitors, tools, and demos **MUST NOT** become menus.

## 5. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | An admin `/configs` page contains `Parameter name`, `Parameter key`, `Built-in`, `Created`, `Search`, `Reset`, `Change`, `user-btn-search`, `user-btn-reset`, `user-btn-edit`, `aria-label="check all"`, a checkbox named `config_id`, and the eight column labels in order. The header is not the word `Choose` |
| AC-2 | That page contains `Skin name`, `sys.index.skinName`, `skin-blue`, `Initial password`, `sys.user.initPassword`, `123456`, `Captcha`, `Registration`, `class="el-tag el-tag--success"`, `Yes`, and `Showing 1 to 4 of 4 records`, with `sys.index.skinName` before `sys.user.initPassword` |
| AC-3 | That page's shell contains `href="/configs"` and the signed-in `user_name` |
| AC-4 | `GET /configs?config_key=initPassword` contains `sys.user.initPassword` and omits `sys.index.skinName`. `GET /configs?config_name=Captcha` contains `Captcha` and omits `Initial password`. `Reset` is a link to `/configs` |
| AC-5 | `GET /configs?config_type=N`, `GET /configs?begin=2999-01-01`, and `GET /configs?begin=yesterday` each contain `Showing 0 to 0 of 0 records` |
| AC-6 | `GET /configs?form=edit&config_id=2` for an account with `system:config:edit` contains `Change a parameter`, `action="/configs/set"`, `name="config_value"`, a textarea, and `123456`. That form omits `name="config_name"`, `name="config_type"`, and `name="remark"`. The same page without that query omits `action="/configs/set"`. `GET /configs?form=edit` with no `config_id` contains `Choose a parameter` and omits `action="/configs/set"` |
| AC-7 | The parameters HTML contains no `<iframe`, no `bootstrap.min.css`, no `jquery`, no `font-awesome`, no `参数设置`, no `修改参数`, and no Add, Delete, Export, or Refresh cache button. When the checkbox column is shown, the only script is `<script src="/table-check.js"></script>`. When it is omitted, the page contains no `<script` tag. It does not contain `action="/configs/add"`. It does not contain a control that deletes many rows |
| AC-8 | Sign-out is `method="post"`, `action="/logout"`, and `name="csrf"` |
| AC-9 | An operator `/configs` page contains the four seeded keys and omits `Change a parameter`, `user-btn-edit`, `Choose`, `aria-label="check all"`, and `action="/configs/set"`, including when the query is `form=edit`. Lead `GET /configs` is refused with `Missing permission` |
| AC-10 | An Apex `/configs` page keeps the eight column labels and does not link `/element-plus.css`. When the change form is shown it contains `action="/configs/set"` |
| AC-11 | The Created search control is `requirement-html-date-range`: `class="admlte-date-range"`, no `From` or `To` label, `name="begin"` `type="date"`, `name="end"` `type="date"`, and the arrow `→`. The column header stays `>Created<` |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Parameter Management | The OpenRbac page `GET /configs` |
| Studied page | The RuoYi list whose title is `参数设置`, captured with `修改参数` open |
| Parameters link | The sidebar item labeled `Parameters` with href `/configs` |
| Count line | `Showing {first} to {last} of {total} records` under the table |
| Toolbar | `Change` above the table |
| Built-in | `config_type` `Y` shown as `Yes`. Any other type is `No` |
| Date range | The Created search control. The markup is `requirement-html-date-range` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Parameters page UI. The studied page `参数设置` is `/configs`. The capture is `Screenshot from 2026-10-14 22-37-24.png` |
| 2026-10-15 | Active 1.0.1 | The Created search is the side-by-side date range in `requirement-html-date-range` |
| 2026-10-15 | Active 1.0.2 | The Created search shows no From or To label |
| 2026-10-16 | Active 1.0.3 | The parameter table uses a check-all checkbox and a row checkbox named `config_id`. The header is not the word Choose |
| 2026-10-16 | Active 1.0.4 | The checkbox column is centered. `/table-check.js` checks every row box in that table |
| 2026-10-16 | Active 1.0.5 | Every skin uses the Apex card for the change panel |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
