**file**: docs/requirements/requirement-html-role-management.md
**Status**: Active (Version 1.0.6)
**Area**: python
**Key**: `requirement-html-role-management`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the Role Management page. The studied document is the RuoYi list titled `角色管理`. That document is a search row, a toolbar, a role table, and a count line. OpenRbac serves that page as `GET /roles`.

The actions, the permission strings, the list filters, and the text-report columns stay on `requirement-rbac-roles`. The shell, the theme, and the ban on a script stay on `requirement-python-html-template`, `requirement-html-theme`, and `requirement-html-javascript`.

### 1.1 Human-facing

**In one sentence:** Roles is a page with a search row, a toolbar of Add, Edit, Remove, and Export, and a role table whose data scope is a colored tag and whose status is an on/off switch.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account opening Roles | `admin` |
| The other role | The sidebar link | Access → Roles → `/roles` |
| Not this file | Who may grant, and the protected role | `requirement-rbac-roles`, `requirement-rbac` |

| Includes | Excludes |
|----------|----------|
| The search row, the toolbar, the role table, and the count line | A second page at `/system/role` |
| English labels for the studied Chinese labels | The Chinese labels copied onto the page |
| Add, edit, remove, export, the status switch, and Data scope when that permission is present | Assign users. The studied More menu names it. This page does not open a user list |
| A check-all checkbox and a row checkbox named `role_id` when edit or remove is allowed | A checkbox that deletes many rows |

| Surface | What you open | What for |
|---------|---------------|----------|
| Sidebar | Access, then Roles | `GET /roles` |
| Page | `templates/roles.vue` inside the shell | The search, the toolbar, and the table |
| Studied page | `角色管理` | The same layout, under the OpenRbac path |

## 2. The studied page

| Piece in the studied document | OpenRbac |
|-------------------------------|----------|
| Sidebar item `角色管理`, drawn as the open item | Label `Roles`, href `/roles`, in the Access group. The open page is the active item |
| Tab strip `首页` and `角色管理` | No tab strip. The sidebar is the way back to Home |
| Search `角色名称`, `权限字符`, `角色状态` with `所有`, `创建时间` with a start and an end | `Role name`, `Permission key`, `Status`, `Created`. `Created` is the date range in `requirement-html-date-range`. The status choices are `All`, `Enabled`, and `Disabled`. The form is `GET /roles` |
| `搜索` and `重置` | `Search` submits the form. `Reset` is a link to `/roles`. Each has an icon |
| Toolbar `新增`, `修改`, `删除`, `导出` | `Add`, `Edit`, `Remove`, and `Export`. Each is a working action when that permission is allowed, and each has an icon |
| The four icons at the right of the toolbar | Omitted. They are column and refresh chrome, and they need a script |
| A checkbox on the header and on each row | The header is a checkbox `aria-label="check all"` with no `name`. Each row is a checkbox named `role_id`. The cells use `table-check-col`. `/table-check.js` checks the row boxes in that table. The page does not delete many rows |
| Columns `角色编号`, `角色名称`, `权限字符`, `数据权限`, `显示顺序`, `角色状态`, `创建时间`, `操作` | `Role id`, `Role name`, `Permission key`, `Data scope`, `Display order`, `Status`, `Created`, `Action`, in that order |
| `数据权限` as a green `全部数据权限` or a blue `自定义数据权限` | An `el-tag`. Scope `1` is `All data` and `el-tag--success`. Scope `2` is `Custom data` and `el-tag--primary`. Scope `3` is `This department` and `el-tag--warning`. Scope `4` is `Department and children` and `el-tag--info` |
| `角色状态` as an on/off switch | An `el-switch` in section 6. On is `Enabled` and stores `0`. Off is `Disabled` and stores `1`. The track and the knob use the measurements in that section |
| Row `编辑`, `删除`, and `更多操作` on every role except the first | `Edit`, `Remove`, and `More` when that permission is allowed and the role is not role 1. `More` contains `Data scope` |
| `显示第 1 到第 N 条记录，总共 N 条记录` | `Showing 1 to N of N records` |
| Studied names `超级管理员` and `普通角色` | Not seed data. The seeded names stay on `requirement-rbac-roles` |

The studied document also loads Bootstrap, jQuery, Font Awesome, and a script block. Those stay out of the response. The buttons use the icon classes already painted for the users page: `user-btn-search`, `user-btn-reset`, `user-btn-add`, `user-btn-edit`, `user-btn-remove`, and `user-btn-export`. `More` uses `user-btn-more`. That icon is `/icons/user-more.svg`. The page does not load a Font Awesome file.

## 3. The roles page

The page is `src/OpenRbac/templates/roles.vue`, inside the shell. The content root is `role-page`. Every skin paints that root from `/apex.css`.

The search fields are `role_name`, `role_key`, `state`, `begin`, and `end`. An empty field does not filter. `Reset` drops every field. The status choices are `All`, `Enabled`, and `Disabled`. `state` of `0` keeps status `0`. `state` of `1` keeps status `1`. `Created` is the date range in `requirement-html-date-range`. The group word is `Created` followed by one space. The column header `Created` stays the table cell.

The toolbar and the table are one `GET` form to `/roles`. Hidden fields keep the search. When edit or remove is allowed, the first header is a checkbox with `aria-label="check all"` and no `name`, and each row has one checkbox named `role_id`. The header cell and each row cell use `table-check-col`. The header is not the word `Choose`. `/table-check.js` checks or unchecks every row box in that table. The header box is not posted. Edit and Remove still use the first posted id. The page does not delete many rows. `Edit` submits `form=edit`. `Remove` submits `form=remove`. `Add` is a link to `form=add`. `Export` is a link to `GET /roles/export` with the same filters. Submitting edit, remove, or Data scope with no chosen role shows `Choose a role.` An id outside the unfiltered list shows `That role is not in this list.` Role 1 shows `The built-in administrator role is not edited here.` and does not open the form.

The eight data columns, in order, are `Role id`, `Role name`, `Permission key`, `Data scope`, `Display order`, `Status`, `Created`, and `Action`. The check-all checkbox sits in front of them only when edit or remove is allowed. `Display order` is `role_sort`. `Created` is `create_time`, cut to 19 characters. An empty time is an empty cell. `Data scope` is the tag in section 2. `Status` is the switch in section 6. On shows `Enabled` and stores `0`. Off shows `Disabled` and stores `1`. A click posts `POST /roles/status` when `system:role:edit` is allowed and the role is not role 1. Role 1, and an account without that permission, show the switch and do not submit. `Role name` is a link to the edit form when edit is allowed and the role is not role 1.

The count line uses the filtered list. When that list is empty, the line is `Showing 0 to 0 of 0 records`. Otherwise it is `Showing 1 to N of N records`. The page does not add a page-size control.

| Form | Shown when | Post |
|------|------------|------|
| Add a role | `?form=add` and `system:role:add` | `POST /roles/add` with `csrf`, `role_name`, `role_key`, `role_sort`, `status`, `remark`, and `menu_id` |
| Edit a role | `?form=edit&role_id=` and `system:role:edit`, and that id is in the unfiltered list and is not role 1 | `POST /roles/edit` with `csrf`, `role_id`, `role_name`, `role_key`, `role_sort`, `status`, `remark`, and `menu_id` |
| Remove a role | `?form=remove&role_id=` and `system:role:remove`, and that id is in the unfiltered list and is not role 1 | `POST /roles/remove` with `csrf` and `role_id` |
| Data scope | `?form=scope&role_id=` and `system:role:edit`, and that id is in the unfiltered list and is not role 1 | `POST /roles/grant` with `csrf`, `role_id`, `data_scope`, `dept_id`, and the role's current `menu_id` values as hidden fields |

A form that the account cannot use is absent, including when the query asks for it. Each panel is an `el-dialog`, drawn as the Apex card around the same fields. The edit form and the add form draw the menu boxes with `el-tree`. A menu the role already has starts checked. The data scope form does not draw that tree. It posts the current menu ids so the grant keeps them. The status field on add and edit is the switch in section 6. A checked switch posts `0`. An unchecked switch posts `1`. The search choices stay the words `All`, `Enabled`, and `Disabled`.

`GET /roles/export` is not an HTML page. It returns `text/csv` and `Content-Disposition: attachment; filename="roles.csv"`. The columns and the permission are `requirement-rbac-roles`.

The row links `Edit`, `Remove`, and `More` stay when the matching permission is allowed and the role is not role 1. `More` is a `details` element. Its summary is `More`. The link inside it is `Data scope`.

Every theme links `/apex.css` and `/themes/<name>.css`. The markup is the Apex shell (`requirement-html-theme`).

## 4. Normative rules

1. **Destination.** Role Management **MUST** be `GET /roles`. The template **MUST** be `roles.vue` inside the shell. The product **MUST NOT** add a role-admin page at `/system/role`.
2. **Menu.** An account with `system:role:list` **MUST** see label `Roles` and href `/roles` in the Access group. The open page **MUST** be the active item in the HTML. An account without that permission **MUST NOT** see that link.
3. **Search.** The search form **MUST** be `method="get"` and `action="/roles"`. It **MUST** include `Role name`, `Permission key`, `Status`, `Created`, `Search`, and `Reset`. `Search` **MUST** use `user-btn-search`. `Reset` **MUST** use `user-btn-reset` and **MUST** be a link to `/roles` with no query. The status control **MUST** offer `All`, `Enabled`, and `Disabled`. `Created` **MUST** be the date range in `requirement-html-date-range`. The signed-in `user_name` in the shell **MUST** stay the account name when a search field is filled.
4. **Table.** The table **MUST** show the eight data labels in section 3, in that order. A checkbox with `aria-label="check all"`, class `table-check`, and no `name` **MUST** be the first header when edit or remove is allowed, and **MUST** be omitted otherwise. Each row in that column **MUST** be a checkbox named `role_id`. The header cell and each row cell **MUST** use `table-check-col`. The header **MUST NOT** be the word `Choose`. When the column is shown, the document **MUST** include `<script src="/table-check.js"></script>`, and that file **MUST** check the row boxes in that table. When the column is omitted, the document **MUST NOT** include a script tag. Both stylesheets **MUST** center `.table-check-col`. The rows **MUST** be the filtered list from `requirement-rbac-roles`. The page **MUST** show the count line in section 3. `Data scope` **MUST** be the tag in section 2. `Status` **MUST** be the switch in section 6 and in rule 10. It **MUST NOT** be only the words `Enabled` and `Disabled`.
5. **Toolbar.** `Add`, `Edit`, `Remove`, and `Export` **MUST** be on the toolbar when `system:role:add`, `system:role:edit`, `system:role:remove`, and `system:role:export` are allowed, and **MUST** be omitted otherwise. They **MUST** use `user-btn-add`, `user-btn-edit`, `user-btn-remove`, and `user-btn-export`. `Edit` and `Remove` **MUST** submit the chosen `role_id` with the search fields kept. `Add` **MUST** be a link to `form=add`. `Export` **MUST** be a link to `/roles/export` with those filters. The row links `Edit`, `Remove`, and `More` **MUST** remain when the matching permission is allowed and the role is not role 1. `More` **MUST** use `user-btn-more` and **MUST** contain `Data scope`. Role 1 **MUST NOT** show those row links. Each form in section 3 **MUST** use that method, action, and field `name`, including `csrf`, and **MUST** be omitted unless the query and the permission both allow it. The field rules and the audit row stay on `requirement-rbac-roles`.
6. **Identity.** The shell on this page **MUST** show the signed-in `user_name`. Sign-out **MUST** be a form with `method="post"` and `action="/logout"` and a hidden `csrf` field.
7. **Skin.** The page **MUST** use `Settings.theme()`. Every skin **MUST** show the same search names, the same columns, the same toolbar, and the same form names. The `role-page` rules **MUST** live in `/apex.css`. `More` **MUST** use `/icons/user-more.svg`. The listener **MUST** serve that file as `image/svg+xml`. `/apex.css` **MUST** reference that file and **MUST NOT** use a `data:` image.
8. **Plain page.** The response **MUST NOT** contain an `<iframe`, a `<style` block, `bootstrap.min.css`, `jquery`, or `font-awesome`. The only `<script` tag is `<script src="/table-check.js"></script>`, and only when the checkbox column is shown. It **MUST NOT** contain a tab strip, a lock-screen control, a fullscreen control, a theme-switch dialog, or a notice badge filled by a separate request. It **MUST NOT** link to `ruoyi.vip` or `doc.ruoyi.vip`.
9. **Neighbors.** Users, roles, menus, departments, and job titles **MUST** stay in Access. Parameters, dictionaries, and notices **MUST** stay in Catalog. The operation log, the login log, and online **MUST** stay in Audit. The studied groups for monitors, tools, and demos **MUST NOT** become menus.
10. **Status switch.** `Status` **MUST** be the switch in section 6. On **MUST** be status `0` and the word `Enabled`. Off **MUST** be status `1` and the word `Disabled`. The control **MUST** be a track and a knob. It **MUST NOT** be a `select` of `0` and `1`, and it **MUST NOT** be only those two words. It **MUST NOT** use a script. A table switch that may post **MUST** be a `button` whose `form` attribute names a form outside the `GET` form that wraps the table. That form **MUST** use `method="post"` and `action="/roles/status"`, and **MUST** send `csrf`, `role_id`, and the other `status`. Role 1, and an account without `system:role:edit`, **MUST** be a `span` with `is-disabled` and **MUST NOT** submit. The add field and the edit field **MUST** be a checkbox of value `0` followed by a hidden input of value `1`. Checked posts `0`. Unchecked posts `1`. The search choices stay the words `All`, `Enabled`, and `Disabled`. The track **MUST** be 40 by 20. Off **MUST** be `#dcdfe6`. On **MUST** be `#409eff`. The knob **MUST** be 16 by 16 and white. Both `/apex.css` **MUST** paint that track and that knob. Job titles, dictionaries, the login log, online, and parameters **MUST** keep the status tags named by their own requirements.

## 5. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | An admin `/roles` page contains `Role name`, `Permission key`, `Status`, `Created`, `Search`, `Reset`, `Add`, `Edit`, `Remove`, `Export`, the classes `user-btn-add`, `user-btn-edit`, `user-btn-remove`, `user-btn-export`, `user-btn-search`, and `user-btn-reset`, and the eight column labels in order |
| AC-2 | That page contains `All data`, `class="el-tag el-tag--success"`, `class="el-switch"`, `class="el-switch__core"`, `class="el-switch__action"`, `Showing 1 to 3 of 3 records`, and the signed-in `user_name`. Role 2 is a `button` with `form="role-status-2"`, `el-switch__label` `Enabled`, and a form `id="role-status-2"` `method="post"` `action="/roles/status"` whose hidden `status` is `1`. Role 1 is `class="el-switch is-checked is-disabled"` and the page omits `form="role-status-1"` |
| AC-3 | An account with only `system:role:list` omits `Add`, `Edit`, `Remove`, `Export`, `More`, `action="/roles/add"`, `action="/roles/status"`, and `aria-label="check all"`, including when the query is `form=add` |
| AC-4 | The roles HTML contains no `<iframe`, no `bootstrap.min.css`, no `jquery`, and no `font-awesome`. When the checkbox column is shown, the only script is `<script src="/table-check.js"></script>`. When it is omitted, the page contains no `<script` tag |
| AC-5 | Sign-out is `method="post"`, `action="/logout"`, and `name="csrf"` |
| AC-6 | An Apex `/roles` page keeps the eight column labels, does not link `/element-plus.css`, and includes `action="/roles/add"` when the add form is shown |
| AC-7 | `GET /roles?form=add` for an account with `system:role:add` contains `Add a role`, `action="/roles/add"`, `class="el-switch__input"`, `name="status"` `value="0"`, and a following hidden `name="status"` `value="1"`. The same page without that query omits `Add a role` and `action="/roles/add"`. `GET /roles?form=edit&role_id=2` contains `Edit a role`, `action="/roles/edit"`, a checked menu box, and that same status pair. `GET /roles?form=scope&role_id=2` contains `Data scope` and `action="/roles/grant"` |
| AC-8 | `GET /roles?role_name=Common` contains `common` and omits `lead`. `Reset` is a link to `/roles`. Role 1 has no `form=edit&role_id=1` link |
| AC-9 | `/apex.css` contains `user-btn-more::before` and `url("/icons/user-more.svg")`, and it does not contain `data:image`. `GET /icons/user-more.svg` is `image/svg+xml` and contains no `<script`. `GET /roles/export` for an allowed account is `text/csv` and is not an HTML page |
| AC-10 | `POST /roles/status` for a role other than role 1 changes that status and keeps the search fields. Role 1 stays enabled. An id outside the list is refused with `That role is not in this list.` |
| AC-11 | The Created search control is `requirement-html-date-range`: `class="admlte-date-range"`, no `From` or `To` label, `name="begin"` `type="date"`, `name="end"` `type="date"`, and the arrow `→`. The column header stays `>Created<` |

## 6. Role status switch

A role status is a track with a knob. The knob sits on the right when the role is on, and on the left when the role is off. The word beside the track is `Enabled` when the role is on, and `Disabled` when the role is off. `0` is on. `1` is off.

| Piece | Measurement |
|-------|-------------|
| Track | 40 by 20. Off is `#dcdfe6`. On is `#409eff` |
| Knob | 16 by 16, white. `left: 1px` when off. `left: calc(100% - 17px)` when on |
| Locked | Opacity `.6`. The control does not submit |

The table sits inside a `GET` form, so the switch uses the `form` attribute. The status form follows that `GET` form. Clicking the button posts the other status and keeps the search fields.

On, for a role other than role 1, when `system:role:edit` is allowed:

```html
<button type="submit" class="el-switch is-checked" form="role-status-2" aria-pressed="true">
  <span class="el-switch__core"><span class="el-switch__action"></span></span>
  <span class="el-switch__label">Enabled</span>
</button>
<form id="role-status-2" method="post" action="/roles/status">
  <input type="hidden" name="csrf" value="token">
  <input type="hidden" name="role_id" value="2">
  <input type="hidden" name="status" value="1">
</form>
```

Off uses `class="el-switch"` without `is-checked`. The label is `Disabled`. `aria-pressed` is `false`. The hidden `status` is `0`, which turns the role on:

```html
<button type="submit" class="el-switch" form="role-status-2" aria-pressed="false">
  <span class="el-switch__core"><span class="el-switch__action"></span></span>
  <span class="el-switch__label">Disabled</span>
</button>
<form id="role-status-2" method="post" action="/roles/status">
  <input type="hidden" name="csrf" value="token">
  <input type="hidden" name="role_id" value="2">
  <input type="hidden" name="status" value="0">
</form>
```

Role 1 stays on. An account without `system:role:edit` also sees the track and gets a `span`:

```html
<span class="el-switch is-checked is-disabled" aria-disabled="true">
  <span class="el-switch__core"><span class="el-switch__action"></span></span>
  <span class="el-switch__label">Enabled</span>
</span>
```

The add form and the edit form use a checkbox so the knob moves before Save. The checkbox comes first. A checked box posts `0`. An unchecked box posts the hidden `1`.

On:

```html
<label class="el-switch is-checked">
  <input class="el-switch__input" type="checkbox" name="status" value="0" checked>
  <span class="el-switch__core"><span class="el-switch__action"></span></span>
  <span class="el-switch__label">Enabled</span>
</label>
<input type="hidden" name="status" value="1">
```

Off:

```html
<label class="el-switch">
  <input class="el-switch__input" type="checkbox" name="status" value="0">
  <span class="el-switch__core"><span class="el-switch__action"></span></span>
  <span class="el-switch__label">Disabled</span>
</label>
<input type="hidden" name="status" value="1">
```

The search field stays a choice of `All`, `Enabled`, and `Disabled`. Both `/apex.css` paint this track and this knob. The page uses no script.

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Role Management | The OpenRbac page `GET /roles` |
| Studied page | The RuoYi role list whose title is `角色管理` |
| Roles link | The sidebar item labeled `Roles` with href `/roles` |
| Data scope | The colored tag in the role table. The words are section 2 |
| More | The row control that opens Data scope. It is not a script menu |
| Toolbar | Add, Edit, Remove, and Export above the role table |
| Role status switch | The `el-switch` in section 6. On is `Enabled` and stores `0`. Off is `Disabled` and stores `1` |
| Date range | The Created search control. The markup is `requirement-html-date-range` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Roles page UI. The studied page `角色管理` is `/roles` |
| 2026-10-14 | Active 1.0.1 | Role status is the on/off switch in section 6. On is Enabled and stores 0. Off is Disabled and stores 1 |
| 2026-10-15 | Active 1.0.2 | The Created search is the side-by-side date range in `requirement-html-date-range` |
| 2026-10-15 | Active 1.0.3 | The Created search shows no From or To label |
| 2026-10-16 | Active 1.0.4 | The role table uses a check-all checkbox and a row checkbox named `role_id`. The header is not the word Choose |
| 2026-10-16 | Active 1.0.5 | The checkbox column is centered. `/table-check.js` checks every row box in that table |
| 2026-10-16 | Active 1.0.6 | Every skin uses the Apex card for an add or edit panel. The rules live in `/apex.css` |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
