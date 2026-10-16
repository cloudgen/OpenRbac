**file**: docs/requirements/requirement-rbac-roles.md
**Status**: Active (Version 1.1.0)
**Area**: domain
**Key**: `requirement-rbac-roles`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the role record. A role carries `role_key` and `data_scope`. Its menus are the permission strings an account can use. Grant replaces the menu links for one role. Add, edit, remove, the status switch, and export are the same `Access` methods, called by the roles page. They have no text-menu row and no typed verb. The meaning of scope 1–4, and the rule that role 1 stays as seeded, stay on `requirement-rbac`.

### 1.1 Human-facing

**In one sentence:** An administrator can see every role, add a role, and change any role except the built-in administrator role.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account that grants | `admin` |
| The other role | The role being changed | role 2, `common` |
| Not this file | How scope 4 walks `ancestors` | `requirement-rbac`, `requirement-rbac-departments` |

| Includes | Excludes |
|----------|----------|
| The role list, grant, and the page actions add, edit, remove, status, and export | A typed verb for add, remove, or export |
| Replacing `sys_role_menu` for that role | Editing role 1 |
| Custom departments only when the scope is 2 | A second permission list on the page |

| Surface | What you open | What for |
|---------|---------------|----------|
| Text menu | rbac rows 16 and 17 | List, then grant |
| Typed verb | `open-rbac role-list` | The list |
| Web page | `/roles` | That list, the toolbar, and a form only when the permission is present |

## 2. Actions

| Action | Permission | Menu row | Verb | Web |
|--------|------------|----------|------|-----|
| List | `system:role:list` | 16 `role-list` | `role-list` | `GET /roles` |
| Grant | `system:role:edit` | 17 `role-grant` | `role-grant` | `POST /roles/grant` |
| Add | `system:role:add` | none | none | `POST /roles/add` |
| Edit | `system:role:edit` | none | none | `POST /roles/edit` |
| Remove | `system:role:remove` | none | none | `POST /roles/remove` |
| Change status | `system:role:edit` | none | none | `POST /roles/status` |
| Export | `system:role:export` | none | none | `GET /roles/export` |

The seed also inserts menu 1011, Role query, with `system:role:query`. No verb and no page require that string. The seed inserts menu 1013, Role add, with `system:role:add`, menu 1014, Role remove, with `system:role:remove`, and menu 1015, Role export, with `system:role:export`. The administrator role receives them on a fresh database. `role_key` `admin` passes the check without those rows. A database created before those menus does not gain them. Common and lead do not receive the role list, role edit, role add, role remove, or role export. Rows 16 and 17 stay the two text-menu actions. Add, edit, remove, status, and export call `Access` from the roles page and are not text-menu rows.

The text-report columns are `role_id`, `role_name`, `role_key`, `data_scope`, and `status`. The page columns are `requirement-html-role-management`. A successful grant prints `Granted role {role_id} ({role_key}), data_scope {data_scope}.`

The seeded roles are role 1 `admin` scope 1, role 2 `common` scope 3, and role 3 `lead` scope 4. Which menus each role receives on an empty database stays on `requirement-rbac`.

## 3. Normative rules

1. **One path.** List and grant **MUST** call `Access.role_list` and `Access.role_grant`. Add **MUST** call `Access.role_add`. Edit and the status switch **MUST** call `Access.role_edit`. Remove **MUST** call `Access.role_remove`. Export **MUST** call `Access.role_export`. A missing permission **MUST** start with `Missing permission`.
2. **List.** `role-list` **MUST** require `system:role:list`. It **MUST** return every role with `del_flag` 0, ordered by `role_sort` then `role_id`. Data scope **MUST NOT** drop a role from this list. A call with no filters **MUST** return those rows. Optional filters **MUST** only narrow that set: `role_name` and `role_key` are a contains match after `%`, `_`, and `\` are removed; `status` is `0` or `1`; `begin_time` and `end_time` are `YYYY-MM-DD` or the call fails with `The start date must be YYYY-MM-DD.` or `The end date must be YYYY-MM-DD.` The text report **MUST** keep the five column names above. The list **MAY** also return `role_sort`, `create_time`, and `remark` for the page.
3. **Protected role.** Grant, edit, remove, and a status change on role 1 **MUST** say `The built-in administrator role is not edited here.` They **MUST NOT** change that role's name, key, order, scope, status, menus, or department links.
4. **Scope value.** When grant includes a data scope, the value **MUST** be `1`, `2`, `3`, or `4`. Any other value **MUST** say `data_scope must be 1, 2, 3, or 4.` An omitted scope **MUST** leave the stored scope unchanged.
5. **Menus.** Every submitted menu id **MUST** exist on `sys_menu`. An unknown id **MUST** say `Unknown menu`. The submitted ids **MUST** replace `sys_role_menu` for that role. The typed verb **MUST** require `--menu-ids` as comma-separated ids. A page submit with no menu box **MUST** leave that role with no menu links. `role_edit` **MUST** replace menus when `menu_ids` is passed, and **MUST** leave the menus unchanged when `menu_ids` is omitted. `role_edit` **MUST NOT** change `data_scope` or `sys_role_dept`.
6. **Custom departments.** Grant **MUST** delete `sys_role_dept` for that role. When the scope after the update is `2`, it **MUST** insert the submitted department ids, and each id **MUST** be a department with `del_flag` 0. When the scope is not `2`, it **MUST** leave `sys_role_dept` empty for that role. The typed verb accepts comma-separated `--dept-ids`. The page field `dept_id` is one id.
7. **Audit.** A successful grant **MUST** write `sys_oper_log` with title `Role`, `business_type` 2, method `role_grant`, and the role id as the parameter. Add **MUST** use `business_type` 1 and method `role_add`. Edit, including the status switch, **MUST** use `business_type` 2 and method `role_edit`. Remove **MUST** use `business_type` 3 and method `role_remove`.
8. **Page.** `GET /roles` **MUST** require `system:role:list`. The add, edit, remove, and data-scope forms **MUST** be omitted when the account lacks the matching permission. The export link **MUST** be omitted when `system:role:export` is absent. The layout of that page is `requirement-html-role-management`. The page **MUST** read the optional filters from its query string.
9. **Add.** `role_add` **MUST** require `system:role:add`. `role_name` **MUST** be 1 to 30 characters. `role_key` **MUST** start with a letter and then use only letters, digits, or underscores, at most 100 characters. A miss **MUST** say `role_key must start with a letter and use letters, digits, or underscores.` A key that already exists **MUST** say `That role_key is already in use.` `role_sort` **MUST** be a whole number. A miss **MUST** say `role_sort must be a whole number.` `status` **MUST** be `0` or `1`. An empty status **MUST** store `0`. `remark` **MUST** be at most 500 characters. The row **MUST** start with `data_scope` `1` and `del_flag` `0`. An unknown menu id **MUST** fail before the insert.
10. **Edit.** `role_edit` **MUST** require `system:role:edit` and a listed role. An unknown id **MUST** say `Unknown role`. The call **MUST** refuse when name, key, order, status, remark, and menus are all omitted, with `role-edit needs a name, a key, an order, a status, or a remark.` An omitted field **MUST** leave that column unchanged. `status` **MUST** be `0` or `1`.
11. **Remove.** `role_remove` **MUST** require `system:role:remove`. A listed role **MUST** be updated to `del_flag` `2`. The action **MUST** delete that role's `sys_role_menu`, `sys_role_dept`, and `sys_user_role` rows.
12. **Status switch.** `POST /roles/status` **MUST** call `role_edit` with only `status`. It **MUST** require `system:role:edit`. It **MUST NOT** add a permission, a text-menu row, or a typed verb. `status` **MUST** be `0` or `1`. An id that is not in `role_list` **MUST** say `That role is not in this list.` A successful call **MUST** write the same audit row as edit. The control on the page is `requirement-html-role-management`.
13. **Export.** `role_export` **MUST** require `system:role:export`. It **MUST** use the same optional filters as `role_list`. The csv header **MUST** be `role_id,role_name,role_key,data_scope,role_sort,status,create_time`. `GET /roles/export` **MUST** return that csv as `text/csv` with `Content-Disposition` attachment `roles.csv`.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | Admin `role-list` includes `admin` scope 1, `common` scope 3, and `lead` scope 4 |
| AC-2 | `role-grant` on role 1 fails with the built-in administrator sentence |
| AC-3 | `role-grant` with data scope 5 fails |
| AC-4 | Operator `role-list` fails with `Missing permission system:role:list` |
| AC-5 | Granting menu ids 1 and 100 on role 2 leaves only those two links |
| AC-6 | A filter `role_name=Common` returns `common` and omits `lead`. A bad start date fails with `The start date must be YYYY-MM-DD.` |
| AC-7 | `role_add` stores scope `1`. The same `role_key` again fails with `That role_key is already in use.` Edit, remove, and a status change on role 1 fail with the built-in administrator sentence |
| AC-8 | Export of the filtered list contains the new `role_key` and the header in rule 13. Operator export fails with `Missing permission` |
| AC-9 | The admin roles page includes Add, Edit, Remove, and Export. `POST /roles/status` changes a role other than role 1 |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Grant | Replace the menu links, and the scope-2 department links, for one role |
| Protected role | `role_id` 1, `role_key` `admin` |
| Custom departments | Rows in `sys_role_dept`, read only when `data_scope` is 2 |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Role list and grant |
| 2026-10-14 | Active 1.1.0 | Page add, edit, remove, status, and export. The layout is `requirement-html-role-management` |

---

**Last Updated**: 2026-10-14
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
