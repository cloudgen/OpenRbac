**file**: docs/requirements/requirement-html-user-management.md
**Status**: Active (Version 1.3.5)
**Area**: python
**Key**: `requirement-html-user-management`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the User Management page. The studied document is the RuoYi user list, title `用户列表`. That document is a left organization tree, a search row, a toolbar, and an account table. OpenRbac serves that page as `GET /users`.

The actions, the permission strings, the list filters, and the text-report columns stay on `requirement-rbac-users`. The shell, the theme, and the ban on a script stay on `requirement-python-html-template`, `requirement-html-theme`, and `requirement-html-javascript`.

### 1.1 Human-facing

**In one sentence:** Users is a gray page with an organization tree on the left, a search row, a toolbar of Add, Edit, Remove, Import, and Export, and an account table.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account opening Users | `admin` |
| The other role | The sidebar link | Access → Users → `/users` |
| Not this file | Who may see a row, and the password hash | `requirement-rbac-users`, `requirement-rbac` |

| Includes | Excludes |
|----------|----------|
| The organization tree, the search row, the toolbar, and the account table | A second page at `/system/user` |
| English labels for the studied Chinese labels | The Chinese labels copied onto the page |
| Add, edit, remove, import, and export when that permission is present | A file manager, an xlsx file, and a checkbox that deletes many rows |
| The edit dialog in section 6: one department from a floating tree, and any number of job titles from a dropdown | A second user page, a script, and an expand or collapse control |

| Surface | What you open | What for |
|---------|---------------|----------|
| Sidebar | Access, then Users | `GET /users` |
| Page | `templates/users.vue` inside the shell | The tree, the search, and the table |
| Studied page | `用户列表` | The same layout, under the OpenRbac path |

## 2. The studied page

| Piece in the studied document | OpenRbac |
|-------------------------------|----------|
| Left title `组织机构` and the department tree | Title `Organization`. A tree of the departments the account can see. A folder marks a parent. A circle marks a leaf. `GET /users?dept=ID` keeps that department and its children |
| `登录名称`, `手机号码`, `用户状态`, `创建时间` | `Login name`, `Phone`, `Status`, `Created`. `Created` is the date range in `requirement-html-date-range`. The form is `GET /users` |
| `搜索` and `重置` | `Search` submits the form. `Reset` is a link to `/users`. Each has an icon |
| Toolbar `新增`, `修改`, `删除`, `导入`, `导出` | `Add`, `Edit`, `Remove`, `Import`, and `Export`. Each is a working action when that permission is allowed, and each has an icon |
| Columns `用户ID`, `登录名称`, `用户名称`, `部门`, `手机`, `用户状态`, `创建时间`, `操作` | `User`, `Department`, `Phone`, `Status`, `Created`, and `Action`. `User` is a circle of two initials, the account name, and `@` plus the login name. The table does not show `User id`. A check-all checkbox is added in front when edit or remove is allowed. Each row is a checkbox named `user_id` |
| Row `编辑`, `删除`, `重置密码` | Links `Edit`, `Remove`, `Reset` when that permission is allowed. Each has an icon |
| `分配角色` | Roles are checkboxes on the edit dialog in section 6. The role record stays the role page. `Status` is an `el-switch` that posts the other status |
| Studied edit form `基本信息`, and the window `选择部门` over a dimmed form | Section 6. English labels. One department. Several job titles. The sample names on those screens are not seed data |
| `部门管理` | Link `Departments` to `/depts` when `system:dept:list` is allowed. It has a pencil icon |

The studied document also loads Bootstrap, jQuery, Font Awesome, zTree, bootstrap-table, and a script block. Those stay out of the response. Each icon is a file at `/icons/<name>.svg`, served by this host as `image/svg+xml`. The stylesheets point at those files. This page specifies a separate file for each icon, so the icon is not an inline image. The shapes are a tree, a plus, a pencil, a trash can, an upload, a download, a magnifier, a circular arrow, and a key. The page does not load a Font Awesome file. The studied company names are not seed data. The tree uses `sys_dept`.

## 3. The users page

The page is `src/OpenRbac/templates/users.vue`, inside the shell. The content root is `user-page`. Every skin paints that root from `/apex.css`.

The search fields are `user_name`, `phone`, `state`, `begin`, and `end`. A chosen department is `dept`. `Reset` drops every field. The status choices are `All`, `Enabled`, and `Disabled`. `Created` is the date range in `requirement-html-date-range`. The group word is `Created` followed by one space. The column header `Created` stays the table cell.

The toolbar and the table are one `GET` form to `/users`. Hidden fields keep the search. When edit or remove is allowed, the first header is a checkbox with `aria-label="check all"` and no `name`, and each row has one checkbox named `user_id`. The header cell and each row cell use `table-check-col`. The header is not the word `Choose`. `/table-check.js` checks or unchecks every row box in that table. The header box is not posted. Edit and Remove still use the first posted id. The page does not delete many rows. `Edit` submits `form=edit`. `Remove` submits `form=remove`. `Add` is a link to `?form=add`. `Import` is a link to `?form=import`. `Export` is a link to `GET /users/export` with the same filters. Submitting edit or remove with no chosen account shows `Choose an account.` An id outside the account's unfiltered list shows `That account is not in this list.`

The six data columns, in order, are `User`, `Department`, `Phone`, `Status`, `Created`, and `Action`. The check-all checkbox sits in front of them only when edit or remove is allowed. The table does not show a `User id` column. `user_id` stays the row checkbox name, the query on the edit link, and a hidden field on the status, edit, reset, and remove forms.

The `User` cell shows a circle of two initials, the account name, and the login name. The account name is `nick_name`. The login name is `@` plus `user_name`. The initials come from the account name. A name of two or more words uses the first letter of the first word and the first letter of the second word. A name of one word uses its first two letters. An empty name uses `user_name` the same way. The letters are uppercase. `Administrator` shows `AD`. A name with no letter or digit shows `?`. The circle stays when edit is not allowed. The account name is a link to the edit form when edit is allowed. When edit is not allowed, the account name is text and is not a link. The cell is:

```html
<div class="user-person"><span class="user-person-mark">AD</span><div class="min-w-0"><a class="font-medium truncate hover:text-primary block" href="/users?form=edit&amp;user_id=1">Administrator</a><div class="text-xs text-muted-foreground truncate">@admin</div></div></div>
```

`Status` is an `el-switch`, as section 6 of `requirement-html-element-plus`. On shows `Enabled` and stores `0`. Off shows `Disabled` and stores `1`. A click posts `POST /users/status` when `system:user:edit` is allowed and the account is not user 1. User 1, and an account without that permission, show the switch and do not submit. The edit form uses the same switch for `status`. The other edit fields are section 6. The search choices stay the words `All`, `Enabled`, and `Disabled`. The search label `Login name` stays on the search form. The edit dialog still shows `Name` and `Login name` as separate fields. The row links `Edit`, `Remove`, and `Reset` stay.

| Form | Shown when | Post |
|------|------------|------|
| Add a user | `?form=add` and `system:user:add` | `POST /users/add` with `csrf`, `user_name`, `nick_name`, `dept_id`, `role_id`, `password` |
| Edit a user | `?form=edit&user_id=` and `system:user:edit`, and that id is in the account's unfiltered list | `POST /users/edit` with `csrf`, `user_id`, `nick_name`, `dept_id`, `phonenumber`, `email`, `status`, `sex`, `job_title_id`, `role_id`, and `remark`. The dialog is section 6. `user_name` is shown and is not posted |
| Reset a password | `?form=reset&user_id=` and `system:user:resetPwd`, and that id is in the account's unfiltered list | `POST /users/reset` with `csrf`, `user_id`, `password` |
| Remove a user | `?form=remove&user_id=` and `system:user:remove`, and that id is in the account's unfiltered list | `POST /users/remove` with `csrf`, `user_id` |
| Import users | `?form=import` and `system:user:import` | `POST /users/import` with `enctype="multipart/form-data"`, `csrf`, `file`, and optional `update_support` value `1` |

A form that the account cannot use is absent, including when the query asks for it. Each panel is an `el-dialog`, drawn as the Apex card around the same fields. The dialog buttons use the same icon classes as the toolbar. `Close` on the edit dialog is section 6. It does not use `user-btn-remove`.

`GET /users/export` is not an HTML page. It returns `text/csv` and `Content-Disposition: attachment; filename="users.csv"`. The columns and the permission are `requirement-rbac-users`. The file is a csv of accounts. It is not a file manager, and it is not an xls or xlsx workbook. A file whose name does not end in `.csv` is refused.

Every button carries `user-btn` and one action class: `user-btn-search`, `user-btn-reset`, `user-btn-add`, `user-btn-edit`, `user-btn-remove`, `user-btn-import`, `user-btn-export`, `user-btn-resetpwd` for the row password action, or `user-btn-close` for Close. Both stylesheets paint a `::before` icon for each class from `/icons/`. `user-btn-close::before` sets `content: none`.

The tree is nested. `user-node.vue` draws one department and then its children. Each row has a 21px `span.user-switch` and then `span.user-node-icon`. A department with a child has `user-node-branch`, a folder icon, and a small minus box. A department with no child has `user-node-leaf`, a circle icon, and an elbow. A dotted line joins the switch to its parent and runs on to the next sibling. The last sibling stops that line. The single root has the box and no line from above. The chosen department keeps `is-current`, and its icon is white. The lines are drawn in the stylesheet. They are not a zTree file and they are not a script. The switch size, the elbow, and the dotted line are section 5 of `requirement-html-element-plus`.

Every theme links `/apex.css` and `/themes/<name>.css`. The markup is the Apex shell (`requirement-html-theme`).

## 4. Normative rules

1. **Destination.** User Management **MUST** be `GET /users`. The template **MUST** be `users.vue` inside the shell. The product **MUST NOT** add a user-admin page at `/system/user` or `/system/user/profile`.
2. **Menu.** An account with `system:user:list` **MUST** see label `Users` and href `/users` in the Access group. The open page **MUST** be the active item in the HTML. An account without that permission **MUST NOT** see that link.
3. **Organization.** The page **MUST** list the departments from `requirement-rbac-users` under the title `Organization`, as the tree in section 3. Each name **MUST** be a link to `/users` with `dept` set to that id and the other search fields kept. The chosen department **MUST** carry the class `is-current`. A link labeled `Departments` to `/depts` **MUST** appear only when `system:dept:list` is allowed.
4. **Search.** The search form **MUST** be `method="get"` and `action="/users"`. It **MUST** include `Login name`, `Phone`, `Status`, `Created`, `Search`, and `Reset`. `Search` **MUST** use `user-btn-search`. `Reset` **MUST** use `user-btn-reset` and **MUST** be a link to `/users` with no query. `Created` **MUST** be the date range in `requirement-html-date-range`. The signed-in `user_name` in the shell **MUST** stay the account name when the search field is filled.
5. **Table.** The table **MUST** show the six data labels in section 3, in that order. A checkbox with `aria-label="check all"`, class `table-check`, and no `name` **MUST** be the first header when edit or remove is allowed, and **MUST** be omitted otherwise. Each row in that column **MUST** be a checkbox named `user_id` with `aria-label="Select row"`. The header cell and each row cell **MUST** use `table-check-col`. The header **MUST NOT** be the word `Choose`. When the column is shown, the document **MUST** include `<script src="/table-check.js"></script>`, and that file **MUST** check the row boxes in that table. When the column is omitted, the document **MUST NOT** include a script tag. Both stylesheets **MUST** paint `.table-check` and `.table-check-col`, and **MUST** center that column. The `User` cell **MUST** show the circle, `nick_name`, and `@` plus `user_name` in the markup in section 3. The circle **MUST** use `user-person-mark` and **MUST** show the two initials from section 3. `Administrator` **MUST** show `AD`. The account name **MUST** be a link to the edit form when edit is allowed, and **MUST** be text when edit is not allowed. The circle **MUST** stay in both cases. The table **MUST NOT** show a column labeled `User id`. The rows **MUST** be the filtered list from `requirement-rbac-users`. The page **MUST** show how many rows are on the list. The `Status` column **MUST** be the switch in section 6 of `requirement-html-element-plus`. It **MUST NOT** be only the words `Enabled` and `Disabled`. Both stylesheets **MUST** paint `.user-person`, `.user-person-mark`, `.min-w-0`, `.truncate`, `.font-medium`, `.text-xs`, `.text-muted-foreground`, and `.hover\:text-primary:hover`. The mark **MUST** be a circle.
6. **Toolbar.** `Add`, `Edit`, `Remove`, `Import`, and `Export` **MUST** be on the toolbar when `system:user:add`, `system:user:edit`, `system:user:remove`, `system:user:import`, and `system:user:export` are allowed, and **MUST** be omitted otherwise. They **MUST** use `user-btn-add`, `user-btn-edit`, `user-btn-remove`, `user-btn-import`, and `user-btn-export`. `Edit` and `Remove` **MUST** submit the chosen `user_id` with the search fields kept. `Add` and `Import` **MUST** be links to `form=add` and `form=import`. `Export` **MUST** be a link to `/users/export` with those filters. The row links `Edit`, `Remove`, and `Reset` **MUST** remain when the matching permission is allowed. `Reset` on a row **MUST** use `user-btn-resetpwd`. Each form in section 3 **MUST** use that method, action, and field `name`, including `csrf`, and **MUST** be omitted unless the query and the permission both allow it. The field rules and the audit row stay on `requirement-rbac-users`. Import and export are page actions. They are not text-menu rows and they are not typed verbs.
7. **Identity.** The shell on this page **MUST** show the signed-in `user_name`. Sign-out **MUST** be a form with `method="post"` and `action="/logout"` and a hidden `csrf` field.
8. **Skin.** The page **MUST** use `Settings.theme()`. Every skin **MUST** show the same tree, the same search names, the same columns, the same toolbar, and the same form names. The `user-page` rules **MUST** live in `/apex.css`. Each icon **MUST** be a file under `/icons/` with a lowercase name ending in `.svg`. The listener **MUST** serve that file as `image/svg+xml`. `/apex.css` **MUST** reference those files and **MUST NOT** use a `data:` image. This requirement specifies those files. `requirement-web-interface` allows a `data:` image only when a requirement names that inline image.
9. **Plain page.** The response **MUST NOT** contain an `<iframe`, a `<style` block, `bootstrap.min.css`, `jquery`, or `font-awesome`. The only `<script` tag is `<script src="/table-check.js"></script>`, and only when the checkbox column is shown. It **MUST NOT** contain a tab strip, a lock-screen control, a fullscreen control, a theme-switch dialog, a horizontal-menu control, or a notice badge filled by a separate request. It **MUST NOT** link to `ruoyi.vip` or `doc.ruoyi.vip`. An icon file **MUST NOT** contain a `<script` tag.
10. **Neighbors.** Roles, menus, departments, and job titles **MUST** stay in Access. Parameters, dictionaries, and notices **MUST** stay in Catalog. The operation log, the login log, and online **MUST** stay in Audit. The studied groups for monitors, tools, and demos **MUST NOT** become menus.
11. **Edit dialog.** The edit form **MUST** be the dialog in section 6. It **MUST** post `nick_name`, `dept_id`, `phonenumber`, `email`, `status`, `sex`, `job_title_id`, `role_id`, and `remark`. It **MUST** show `user_name` and **MUST NOT** post it. The department control **MUST** be the floating tree in section 6. The job-title control **MUST** be the dropdown in section 6. The add form **MUST** stay the fields in section 3 and **MUST NOT** post `job_title_id`. `Close` **MUST** be a link that keeps the search and **MUST NOT** use `user-btn-remove`. The dialog **MUST** be a floating window: a `div` with class `user-edit-float` and `position: fixed`, over a dimmed users page. A query `picker=dept` **MUST** leave the department panel open. The department picker and the job-title dropdown **MUST NOT** use a script. The document's only script tag is `<script src="/table-check.js"></script>` when the checkbox column is shown. The page **MUST NOT** contain an expand or collapse control.

## 5. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | An admin `/users` page contains `Organization`, `Login name`, `Search`, `Reset`, `Add`, `Edit`, `Remove`, `Import`, `Export`, the classes `user-btn-add`, `user-btn-edit`, `user-btn-remove`, `user-btn-import`, `user-btn-export`, `user-btn-search`, and `user-btn-reset`, `user-node-icon`, and the six column labels in order. The first header is a checkbox `aria-label="check all"` with no `name`. Each row has a checkbox named `user_id`. The column is not labeled `Choose`. The `User` cell contains `user-person-mark`, the two initials, the account name, and `@` plus the login name. `Administrator` shows `AD`. The page does not contain `>User id<` |
| AC-2 | That page's shell contains `href="/users"` and the signed-in `user_name` |
| AC-3 | An operator `/users` page omits `Add`, `Import`, `Export`, `action="/users/add"`, and `action="/users/import"`, including when the query is `form=add` or `form=import`. An account that cannot edit or remove also omits `aria-label="check all"` |
| AC-4 | The users HTML contains no `<iframe`, no `bootstrap.min.css`, no `jquery`, and no `font-awesome`. When the checkbox column is shown, the only script is `<script src="/table-check.js"></script>`. When it is omitted, the page contains no `<script` tag |
| AC-5 | Sign-out is `method="post"`, `action="/logout"`, and `name="csrf"` |
| AC-6 | An Apex `/users` page keeps the six column labels and the same `User` cell, including `user-person-mark`, does not link `/element-plus.css`, and includes `action="/users/add"` when the add form is shown |
| AC-7 | `GET /users?form=add` for an account with `system:user:add` contains `Add a user` and `action="/users/add"`. The same page without that query omits both. `GET /users?form=import` with `system:user:import` contains `Import users`, `action="/users/import"`, and `enctype="multipart/form-data"` |
| AC-8 | A department link is `/users?dept=` plus that id. The admin list filtered by department 102 contains `operator` and omits `clerk`. The tree contains `user-switch`, `user-node-branch`, and `user-node-leaf`, with Group before Engineering, Engineering before Platform, and Platform before Operations |
| AC-9 | `/apex.css` contains `user-btn-import::before`, `user-node-branch`, and `url("/icons/user-upload.svg")`, and it does not contain `data:image`. `GET /icons/user-plus.svg` is `image/svg+xml` and contains no `<script`. `GET /users/export` for an allowed account is `text/csv` and is not an HTML page |
| AC-10 | An admin `/users` page contains `class="el-switch"` and `class="el-switch__core"`, and a switch for an account other than user 1 posts to `/users/status`. An operator `/users` page contains `class="el-switch"` and does not contain `action="/users/status"` |
| AC-11 | An admin page `?form=edit&user_id=2` contains `Edit a user`, `Account`, `Choose a department`, `class="user-edit-float"`, `name="nick_name"`, `name="phonenumber"`, `name="email"`, `name="sex"`, `name="job_title_id"`, `name="role_id"`, `name="remark"`, `name="dept_id"`, `Chief`, `Male`, `Female`, `Unknown`, and `action="/users/edit"`. The login name control has `readonly` and no `name`. `Close` does not use `user-btn-remove`. An operator page omits `Edit a user`. `?form=add` does not contain `name="job_title_id"`. `/apex.css` contains `user-edit-float`, `dept-float`, `job-tag`, and `user-btn-close`. The only script tag is `<script src="/table-check.js"></script>` |
| AC-12 | The Created search control is `requirement-html-date-range`: `class="admlte-date-range"`, no `From` or `To` label, `name="begin"` `type="date"`, `name="end"` `type="date"`, and the arrow `→`. The column header stays `>Created<` |

## 6. Edit a user

The studied edit screen is the RuoYi account form whose heading is `基本信息`. The studied department screen is the window `选择部门` floating over that dimmed form. OpenRbac serves both as the edit dialog on `GET /users?form=edit&user_id=`. The labels are English. The names printed on those two screens are not seed data. Seed departments are Group, Engineering, Platform, and Operations. Seed job titles are Chief, Engineer, People, and Staff. Seed roles are Super administrator, Common, and Lead.

The edit dialog is a floating window on the users page. A `div` with class `user-edit-float` wraps the dialog. That wrap is `position: fixed` and covers the users page. The page behind it is dimmed. Add, reset, remove, and import stay in the page flow. They do not use `user-edit-float`.

The dialog title is `Edit a user`. The heading is `Account`. The fields sit in two columns on `user-edit-grid`. `Remark` uses `user-edit-wide` and spans both columns. The field rules and the audit row stay on `requirement-rbac-users`.

| Studied label | OpenRbac | Field |
|---------------|----------|-------|
| `用户名称` | `Name` | `nick_name`. Required. 1 to 30 characters |
| `归属部门` | `Department` | One `dept_id`, chosen in the floating tree. The closed field shows the department name |
| `手机号码` | `Phone` | `phonenumber`. At most 11 characters. A posted empty value stores an empty string |
| `邮箱` | `Email` | `email`. At most 50 characters. Empty is allowed. A non-empty value contains `@` |
| `登录账号` | `Login name` | The stored `user_name`, on a gray `user-readonly` control. The control has `readonly` and no `name` |
| `用户状态` | `Status` | The `el-switch` in section 6 of `requirement-html-element-plus` |
| `岗位` | `Job title` | Any number of `job_title_id` values. The closed control shows one green tag for each checked title |
| `用户性别` | `Sex` | `sex`. `Male` is `0`, `Female` is `1`, `Unknown` is `2` (`requirement-rbac-dictionaries`) |
| `角色` | `Role` | Any number of `role_id` values. Each offered role is a checkbox |
| `备注` | `Remark` | `remark`. At most 500 characters. A posted empty value stores an empty string |
| `保存` | `Save` | Submits `POST /users/edit`. Class `user-btn user-btn-edit`. It is the first submit button in the form |
| `关闭` | `Close` | A link to `/users` that keeps `user_name`, `phone`, `state`, `begin`, `end`, and `dept`, and drops `form`. Class `user-btn user-btn-close` |

`user-btn::before` draws an icon box on `user-btn`. `user-btn-close::before` **MUST** set `content: none`. The link is a red outline. It **MUST NOT** use `user-btn-remove`. The add dialog stays the fields in section 3. It does not offer a job title.

An unselected sex option, department, job title, or role **MUST NOT** carry `checked` or `selected`. A selected one carries the bare attribute. On user 1, the role 1 checkbox is `checked` and `disabled`.

### 6.1 Job titles

The control is a dropdown of checkboxes. A checkbox with class `job-open` and no `name` opens it. The open state is not posted. Each title is a checkbox `name="job_title_id"` inside `job-menu`. A hidden `job_title_id` with an empty value is always present, so a search with every title unchecked is an empty set. The titles are the status `0` rows from `requirement-rbac-users`. A checked title is a `job-tag`. The tag uses the skin primary. On Apex that primary is `#1ab394`. The closed control shows a tag only for a checked title. The open control shows every offered title. A `:checked` sibling rule does that. A wrapper may use `display: contents` so the sibling can see the tag. The control **MUST NOT** use `:has()`. Both `/apex.css` paint the tag.

### 6.2 Department

The closed field shows the department name and a magnifier. The magnifier uses `user-btn-search` and is a label for a checkbox with class `dept-open`. That checkbox has no `name`. When it is checked, a panel with class `dept-float` covers the form. The panel is `position: fixed`. The form behind it is dimmed. The panel title is `Choose a department`.

`Keyword` is `name="dept_q"`. `Search` is a submit button with class `user-btn user-btn-search`, `name="picker"`, `value="dept"`, `formmethod="get"`, and `formaction="/users"`. It comes after `Save`, so Enter saves the account. That button sends the edit fields with the dialog still open. When the query contains `picker=dept`, the server renders `dept-open` checked, so the panel stays open. `dept_q` filters this panel only. The organization tree on the left, and the account table, stay on their own filters.

The list inside the panel is the nested tree in section 5 of `requirement-html-element-plus`. `templates/dept-choice.vue` draws one department and then its children. Each row is a radio `name="dept_id"`. One department is the whole choice. The chosen row has `is-current`. The organization tree stays `user-node.vue` and stays a link. A keyword keeps a match, the ancestors of a match, and the chosen department with its ancestors, so the checked radio stays on the page. The list is drawn expanded. The panel has no expand control and no collapse control. Expand and collapse on `/depts` stay `requirement-html-department-management`.

`Confirm` and the panel `Close` are labels that clear `dept-open`. They do not submit the form. `Clear` is a radio `name="dept_id"` with an empty value. `Clear` **MUST NOT** use `user-btn-reset`. A saved empty department is refused by `requirement-rbac-users`.

`dept-open` and `dept-float` are siblings, so `.dept-open:checked ~ .dept-float` shows the panel. `Save` comes before that panel in the document. The panel does not need a rule for each department id. Both stylesheets paint `dept-float`.

### 6.3 Roles and the round trip

Each offered role is a checkbox `name="role_id"`. A hidden `role_id` with an empty value is always present. The offered roles are the live roles from `requirement-rbac-users`. User 1's role 1 is checked and disabled, so the browser does not post it. The server keeps role 1 on user 1.

The hidden search fields are `user_name`, `phone`, `state`, `begin`, `end`, and `dept`. A hidden `form` value `edit` keeps the dialog open on the department search. `Save` redirects without `form`. The account phone is `phonenumber`. The search phone is `phone`. The organization filter is `dept`. The account department is `dept_id`.

When `job_title_id` is absent from the query, the checkboxes show the stored titles. When the key is present, the checkboxes show the posted digits and skip the empty value. `role_id` follows the same rule. The other posted edit fields follow the query when the key is present, and the stored account when it is absent.

`Save` is the first submit button. The department search is a later submit. The panel is fixed, so it can follow `Save` in the document and still cover the form. The fragment shows that shape. The departments are the account's tree. The measurements stay in section 5 of `requirement-html-element-plus`.

```html
<button type="submit" class="user-btn user-btn-edit">Save</button>
<a class="user-btn user-btn-close" href="/users">Close</a>
<input class="dept-open" type="checkbox">
<div class="dept-float">
  <p>Choose a department</p>
  <label>Keyword <input name="dept_q"></label>
  <button type="submit" class="user-btn user-btn-search" name="picker" value="dept" formmethod="get" formaction="/users">Search</button>
  <ul class="user-tree">
    <li class="user-depth-0 user-node-branch is-first is-last is-root">
      <span class="user-switch"></span>
      <label class="user-tree-link is-current"><input type="radio" name="dept_id" value="100" checked>Group</label>
      <ul></ul>
    </li>
  </ul>
  <label class="user-btn">Confirm</label>
  <label><input type="radio" name="dept_id" value="">Clear</label>
  <label>Close</label>
</div>
```

The job-title control uses the same kind of nameless checkbox:

```html
<div class="job-select">
  <input type="hidden" name="job_title_id" value="">
  <input class="job-open" type="checkbox">
  <div class="job-menu">
    <label class="job-tag"><input class="job-check" type="checkbox" name="job_title_id" value="1" checked>Chief</label>
  </div>
</div>
```

A checked box shows its tag when the menu is closed. The open checkbox shows every tag. Neither control contains a `<script` tag.

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| User Management | The OpenRbac page `GET /users` |
| User cell | A circle of two initials (`user-person-mark`), the account name (`nick_name`), and `@` plus the login name (`user_name`) in the `User` column. `Administrator` shows `AD` |
| Studied page | The RuoYi user list whose title is `用户列表`, and the edit form studied in section 6 |
| Users link | The sidebar item labeled `Users` with href `/users` |
| Organization | The department tree on the left of the users page |
| Toolbar | Add, Edit, Remove, Import, and Export above the account table |
| Edit dialog | The account form in section 6 |
| Department picker | The floating tree titled `Choose a department` |
| Job title dropdown | The checkbox menu whose checked rows use the skin primary |
| Date range | The Created search control. The markup is `requirement-html-date-range` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Users page UI. The studied menu `用户管理` is `/users` |
| 2026-10-14 | Active 1.1.0 | The users page follows the studied user list: organization, search, and the eight columns |
| 2026-10-14 | Active 1.2.0 | Toolbar Add, Edit, Remove, Import, and Export. Tree icons and a button icon on every action |
| 2026-10-14 | Active 1.2.1 | Icons are `/icons/*.svg`. A data: image is refused by img-src 'self' |
| 2026-10-14 | Active 1.2.2 | These icons stay separate files because this page specifies files |
| 2026-10-14 | Active 1.2.3 | The organization tree is nested. Each row has a switch, and the dotted line stops on the last sibling |
| 2026-10-14 | Active 1.2.4 | The switch, the elbow, and the dotted line are section 5 of requirement-html-element-plus |
| 2026-10-14 | Active 1.2.5 | Status is an el-switch. On is Enabled. Off is Disabled. Search stays those words |
| 2026-10-14 | Active 1.2.6 | The edit dialog chooses one department from a floating tree and any number of job titles from a dropdown |
| 2026-10-14 | Active 1.2.7 | The edit dialog floats over the users page as `user-edit-float`. `picker=dept` leaves the department panel open |
| 2026-10-15 | Active 1.2.8 | The Created search is the side-by-side date range in `requirement-html-date-range` |
| 2026-10-15 | Active 1.2.9 | The Created search shows no From or To label |
| 2026-10-16 | Active 1.3.0 | The account table shows User as the name and @login. It does not show a User id column |
| 2026-10-16 | Active 1.3.1 | The User cell shows the initials circle again. Administrator shows AD |
| 2026-10-16 | Active 1.3.2 | The account table uses a check-all checkbox and a row checkbox named `user_id`. The header is not the word Choose |
| 2026-10-16 | Active 1.3.3 | The checkbox column is centered. `/table-check.js` checks every row box in that table |
| 2026-10-16 | Active 1.3.4 | Every skin uses the Apex card for an add or edit panel. The rules live in `/apex.css` |
| 2026-10-16 | Active 1.3.5 | A checked job-title tag uses the skin primary. On Apex that primary is `#1ab394` |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
