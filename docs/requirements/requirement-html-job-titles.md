**file**: docs/requirements/requirement-html-job-titles.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-html-job-titles`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the Job Titles page. The studied document is the RuoYi list titled `岗位管理`. That document is a search row, a toolbar, a table of job titles, and a count line. OpenRbac serves that page as `GET /job-titles`.

The actions, the permission strings, and the text-report columns stay on `requirement-rbac-job-titles`. The shell, the theme, and the ban on a script stay on `requirement-python-html-template`, `requirement-html-theme`, and `requirement-html-javascript`.

### 1.1 Human-facing

**In one sentence:** Job Titles is a page with a search row, an add button, a table of job titles, and a line that says how many rows are showing.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account opening Job Titles | `admin` |
| The other role | The sidebar link | Access → Job Titles → `/job-titles` |
| Not this file | Who may list or add, and the audit row | `requirement-rbac-job-titles` |

| Includes | Excludes |
|----------|----------|
| The search row, the add button, the six columns, and the count line | A second page at `/system/post` |
| English labels for the studied Chinese labels | The Chinese labels copied onto the page |
| Add when `system:jobtitle:add` is present | Edit, remove, and export. The record file does not name those actions |
| The four seeded codes `ceo`, `se`, `hr`, and `user` | The studied Chinese names as seed data |

| Surface | What you open | What for |
|---------|---------------|----------|
| Sidebar | Access, then Job Titles | `GET /job-titles` |
| Page | `templates/job-titles.vue` inside the shell | The search, the toolbar, and the table |
| Studied page | `岗位管理` | The same layout, under the OpenRbac path |

## 2. The studied page

| Piece in the studied document | OpenRbac |
|-------------------------------|----------|
| Sidebar item `岗位管理`, drawn as the open item | Label `Job Titles`, href `/job-titles`, in the Access group. The open page is the active item |
| Tab strip `首页` and `岗位管理` | No tab strip. The sidebar is the way back to Home |
| Search `岗位编码`, `岗位名称`, `岗位状态` with `所有` | `Job title code`, `Job title`, `Status`. The status choices are `All`, `Normal`, and `Disabled`. The form is `GET /job-titles` |
| `搜索` and `重置` | `Search` submits the form. `Reset` is a link to `/job-titles`. Each has an icon |
| Toolbar `新增` | `add a job titles` when `system:jobtitle:add` is allowed. It is a link to `?form=add` and it has an icon |
| Toolbar `修改`, `删除`, `导出` | Omitted. `requirement-rbac-job-titles` does not name edit, remove, or export |
| The four icons at the right of the toolbar | Omitted. They are column and refresh chrome, and they need a script |
| A checkbox on the header and on each row | Omitted. The page does not delete many rows |
| Columns `岗位编号`, `岗位编码`, `岗位名称`, `显示顺序`, `状态`, `创建时间` | `Job title id`, `Job title code`, `Job title`, `Sort`, `Status`, `Created`, in that order |
| `状态` shown as a green `正常` | An `el-tag`. Status `0` is `Normal`. Any other status is `Disabled` |
| `显示顺序` sorted ascending | The rows are ordered by `job_title_sort`, then `job_title_id` |
| Row `编辑` and `删除` | Omitted, with the toolbar edit and remove |
| `显示第1到第4条记录，总共4条记录` | `Showing {first} to {last} of {total} records` |
| Studied names `董事长`, `项目经理`, `人力资源`, `普通员工` | Not seed data. The seeded names stay `Chief`, `Engineer`, `People`, and `Staff` |

The studied document also loads Bootstrap, jQuery, Font Awesome, and a script block. Those stay out of the response. `Search`, `Reset`, and `add a job titles` use the icon classes already painted for the users page: `user-btn-search`, `user-btn-reset`, and `user-btn-add`. The page does not add a new icon file. The studied groups for monitors, tools, the vendor site, and demos stay out of the menu.

## 3. The job titles page

The page is `src/OpenRbac/templates/job-titles.vue`, inside the shell. The content root is `job-page`. Every skin paints the same labels.

The search fields are `job_title_code`, `job_title`, and `status`. An empty field does not filter. `job_title_code` and `job_title` keep a row whose stored value contains the trimmed text. The match is case-sensitive. `status` of `0` keeps status `0`. `status` of `1` keeps status `1`. Any other status value, including empty, means `All`. `Reset` drops every field. The verb `job-title-list` still returns every job title. The page shows the filtered subset.

The six columns, in order, are `Job title id`, `Job title code`, `Job title`, `Sort`, `Status`, and `Created`. `Created` is `create_time`. An empty `create_time` is an empty cell. `Status` `0` is `<span class="el-tag el-tag--success">Normal</span>`. Any other status is `<span class="el-tag el-tag--info">Disabled</span>`. The status is not an `el-switch`. The users switch stays on the users page.

The count line uses the filtered list. When that list is empty, the line is `Showing 0 to 0 of 0 records`. Otherwise `first` is `1` and `last` equals `total`. The page does not add a page-size control.

`add a job titles` is on the toolbar only when `system:jobtitle:add` is allowed. It links to `/job-titles?form=add` and keeps the search fields. The add panel is an `el-dialog`, drawn as the Apex card around the same fields. It is shown only when the query is `form=add` and the permission is allowed. The form posts `POST /job-titles/add` with `csrf`, `job_title_code`, and `job_title`. The field rules and the audit row stay on `requirement-rbac-job-titles`. A query that asks for the form without the permission omits the panel.

Every theme links `/apex.css` and `/themes/<name>.css`. The markup is the Apex shell (`requirement-html-theme`).

## 4. Normative rules

1. **Destination.** Job Titles **MUST** be `GET /job-titles`. The template **MUST** be `job-titles.vue` inside the shell. The product **MUST NOT** add a job-title page at `/system/post`.
2. **Menu.** An account with `system:jobtitle:list` **MUST** see label `Job Titles` and href `/job-titles` in the Access group. The open page **MUST** be the active item in the HTML. An account without that permission **MUST NOT** see that link, and `GET /job-titles` **MUST** refuse that account.
3. **Search.** The search form **MUST** be `method="get"` and `action="/job-titles"`. It **MUST** include `Job title code`, `Job title`, `Status`, `Search`, and `Reset`. `Search` **MUST** use `user-btn-search`. `Reset` **MUST** use `user-btn-reset` and **MUST** be a link to `/job-titles` with no query. The status control **MUST** offer `All`, `Normal`, and `Disabled`. Filtering **MUST** follow section 3. The signed-in `user_name` in the shell **MUST** stay the account name when a search field is filled.
4. **Table.** The table **MUST** show the six labels in section 3, in that order. The rows **MUST** be the filtered list, ordered by `job_title_sort` then `job_title_id`. The page **MUST** show the count line in section 3. `Status` **MUST** be the `el-tag` in section 3. It **MUST NOT** be an `el-switch`.
5. **Toolbar.** `add a job titles` **MUST** be on the toolbar when `system:jobtitle:add` is allowed, and **MUST** be omitted otherwise. It **MUST** use `user-btn-add` and **MUST** link to `form=add`. The add form **MUST** use `method="post"`, `action="/job-titles/add"`, and the fields `csrf`, `job_title_code`, and `job_title`. It **MUST** be omitted unless the query and the permission both allow it. The page **MUST NOT** show Edit, Remove, Export, a row edit link, a row remove link, or a checkbox column.
6. **Identity.** The shell on this page **MUST** show the signed-in `user_name`. Sign-out **MUST** be a form with `method="post"` and `action="/logout"` and a hidden `csrf` field.
7. **Skin.** The page **MUST** use `Settings.theme()`. Every skin **MUST** show the same search names, the same columns, the same toolbar, and the same form names.
8. **Plain page.** The response **MUST NOT** contain an `<iframe`, a `<script` tag, a `<style` block, `bootstrap.min.css`, `jquery`, or `font-awesome`. It **MUST NOT** contain a tab strip, a lock-screen control, a fullscreen control, or a notice badge filled by a separate request. It **MUST NOT** link to `ruoyi.vip` or `doc.ruoyi.vip`.
9. **Neighbors.** Users, roles, menus, departments, and job titles **MUST** stay in Access. Parameters, dictionaries, and notices **MUST** stay in Catalog. The operation log, the login log, and online **MUST** stay in Audit. The studied groups for monitors, tools, and demos **MUST NOT** become menus.

## 5. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | An admin `/job-titles` page contains `Job title code`, `Job title`, `Status`, `Search`, `Reset`, `add a job titles`, `user-btn-search`, `user-btn-reset`, `user-btn-add`, and the six column labels in order |
| AC-2 | That page contains `ceo`, `se`, `hr`, `user`, `Chief`, `Engineer`, `People`, `Staff`, `class="el-tag el-tag--success"`, `Normal`, and `Showing 1 to 4 of 4 records` |
| AC-3 | That page's shell contains `href="/job-titles"` and the signed-in `user_name` |
| AC-4 | `GET /job-titles?job_title_code=se` contains `Engineer` and omits `Chief`. `Reset` is a link to `/job-titles` |
| AC-5 | `GET /job-titles?form=add` for an account with `system:jobtitle:add` contains `add a job titles` and `action="/job-titles/add"`. The same page without that query omits `action="/job-titles/add"` |
| AC-6 | The job titles HTML contains no `<iframe`, no `<script`, no `bootstrap.min.css`, no `jquery`, no `font-awesome`, no checkbox column, and no Edit, Remove, or Export button |
| AC-7 | Sign-out is `method="post"`, `action="/logout"`, and `name="csrf"` |
| AC-8 | An operator `GET /job-titles` is refused with `Missing permission` |
| AC-9 | An Apex `/job-titles` page keeps the six column labels and does not link `/element-plus.css` |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Job Titles | The OpenRbac page `GET /job-titles` |
| Studied page | The RuoYi list whose title is `岗位管理` |
| Job Titles link | The sidebar item labeled `Job Titles` with href `/job-titles` |
| Count line | `Showing {first} to {last} of {total} records` under the table |
| Toolbar | `add a job titles` above the table |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Job Titles page UI. The studied page `岗位管理` is `/job-titles` |
| 2026-10-16 | Active 1.0.1 | Every skin uses the Apex card for the add panel |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
