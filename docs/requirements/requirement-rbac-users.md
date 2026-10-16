**file**: docs/requirements/requirement-rbac-users.md
**Status**: Active (Version 1.0.6)
**Area**: domain
**Key**: `requirement-rbac-users`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the user record. A signed-in account lists, adds, edits, removes, or resets a password only through `Access`. The text menu, the typed verb, and the web page call that same method. Import and export are the same `Access` methods, called by the users page. They have no text-menu row and no typed verb. Who passes the permission check, and which departments a list may include, stay on `requirement-rbac`. The columns stay on `requirement-database`.

### 1.1 Human-facing

**In one sentence:** An administrator can add, import, and export accounts. A department operator can list the accounts in that department and cannot add, import, or export one.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account that runs the action | `admin` |
| The other role | The permission string on a menu | `system:user:add` |
| Not this file | Data scope numbers and the password hash | `requirement-rbac` |

| Includes | Excludes |
|----------|----------|
| List, add, edit, remove, password reset, csv import, and csv export | A separate query verb for `system:user:query` |
| One role on a new account. On edit, the posted roles and job titles replace that account's links | Assigning a job title from `user-add`, and changing `user_name` |
| Soft delete of a listed account | Removing user 1 or the signed-in account |
| A csv of account rows | A file manager, and an xls or xlsx workbook |

| Surface | What you open | What for |
|---------|---------------|----------|
| Text menu | rbac rows 11–15 | List, add, edit, remove, and password reset |
| Typed verb | `open-rbac user-list` | That list without the menu |
| Web page | `/users` | That list, the five toolbar actions, and a form only when the permission is present |

## 2. Actions

| Action | Permission | Menu row | Verb | Web |
|--------|------------|----------|------|-----|
| List | `system:user:list` | 11 `user-list` | `user-list` | `GET /users` |
| Add | `system:user:add` | 12 `user-add` | `user-add` | `POST /users/add` |
| Edit | `system:user:edit` | 13 `user-edit` | `user-edit` | `POST /users/edit` |
| Remove | `system:user:remove` | 14 `user-remove` | `user-remove` | `POST /users/remove` |
| Reset password | `system:user:resetPwd` | 15 `user-reset-password` | `user-reset-password` | `POST /users/reset` |
| Import | `system:user:import` | none | none | `POST /users/import` |
| Export | `system:user:export` | none | none | `GET /users/export` |
| Change status | `system:user:edit` | none | none | `POST /users/status` |

The seed also inserts menu 1001, User query, with `system:user:query`. No verb and no page require that string. The seed inserts menu 1006, User import, with `system:user:import`, and menu 1007, User export, with `system:user:export`. The administrator role receives both on a fresh database. `role_key` `admin` passes the check without those rows. Common and lead receive list and query. They do not receive add, edit, remove, reset password, import, or export. Rows 11–15 stay the five text-menu actions. Import and export call `Access` from the users page and are not text-menu rows.

The text-report columns are `user_id`, `user_name`, `nick_name`, `dept_id`, `dept_name`, and `status`. The page columns are `requirement-html-user-management`. A successful add prints `Added {user_name}.` A successful edit prints `Updated {user_name}.` A successful remove prints `Removed {user_name}.` A successful reset prints `Password updated for {user_name}.`

## 3. Normative rules

1. **One path.** Each action **MUST** call the matching `Access` method. A missing permission **MUST** start with `Missing permission`. `role_key` `admin` follows the bypass on `requirement-rbac`.
2. **List.** `user-list` **MUST** require `system:user:list`. It **MUST** return accounts with `del_flag` 0 that pass data scope, ordered by `user_id`, at most 200 rows. Scope 1–4 and an empty result for any other scope stay on `requirement-rbac`. A call with no filters **MUST** return those rows. Optional filters **MUST** only narrow that set: `user_name` and `phonenumber` are a contains match after `%`, `_`, and `\` are removed; `status` is `0` or `1`; `dept_id` includes that department and departments whose `ancestors` contain it; `begin_time` and `end_time` are `YYYY-MM-DD` or the call fails with `The start date must be YYYY-MM-DD.` or `The end date must be YYYY-MM-DD.` The text report **MUST** keep the six column names above.
3. **Name.** A new `user_name` **MUST** match `^[A-Za-z][A-Za-z0-9_]{2,29}$`. A miss **MUST** say `user_name must start with a letter and use 3 to 30 letters, digits, or underscores.` A listed account that already has that name **MUST** say `That user_name is already in use.` The column stays unique for every row, including a removed account (`requirement-database`).
4. **Add.** `user-add` **MUST** require `system:user:add`, a `nick_name` of 1 to 30 characters, a department with `del_flag` 0, and a role with `del_flag` 0. An unknown department **MUST** say `Unknown department`. An unknown role **MUST** say `Unknown role`. The row **MUST** start with `status` 0 and `del_flag` 0, and **MUST** insert one `sys_user_role` row. It **MUST NOT** insert `sys_user_job_title`.
5. **Password on add.** An empty password **MUST** use `sys_config.config_value` for `sys.user.initPassword`. When that value is missing, the password **MUST** be `123456`. A password shorter than 5 characters **MUST** say `The password must be at least 5 characters.` Storage **MUST** follow `requirement-rbac`. The operation parameter **MUST** be the `user_name`, and **MUST NOT** be the password.
6. **Edit.** `user-edit` **MUST** require `system:user:edit` and a listed user. An unknown id **MUST** say `Unknown user`. The verb **MUST** refuse when name, department, and status are all empty, with `user-edit needs a name, a department, or a status.` The menu uses that verb. On the verb, an omitted field **MUST** leave that column unchanged, and an omitted job-title list or role list **MUST** leave those links unchanged. `status` **MUST** be `0` or `1`. Setting user 1 to any status other than `0` **MUST** say `The built-in administrator stays enabled.` The action **MUST NOT** change `user_name`. `POST /users/edit` **MUST** refuse an id that is not in that account's `user_list` with `That account is not in this list.` The web form posts every field it shows. A posted `nick_name` **MUST** be 1 to 30 characters or the call says `nick_name is required and must be 30 characters or fewer.` A posted empty `dept_id` **MUST** say `A department is required.` An unknown department **MUST** say `Unknown department`. `phonenumber` **MUST** be at most 11 characters or the call says `The phone number must be 11 characters or fewer.` A posted empty phone stores an empty string. `email` **MUST** be at most 50 characters. A posted empty email stores an empty string. A non-empty email that does not contain `@` **MUST** say `The email must contain @.` A longer email **MUST** say `The email must be 50 characters or fewer.` `sex` **MUST** be `0`, `1`, or `2`, or the call says `Sex must be 0, 1, or 2.` `remark` **MUST** be at most 500 characters or the call says `The remark must be 500 characters or fewer.` A posted empty remark stores an empty string. A posted job-title list **MUST** replace that user's `sys_user_job_title` rows with the distinct posted ids. Each id **MUST** be a job title with `status` `0`, or the call says `Unknown job title`. A posted role list **MUST** replace that user's `sys_user_role` rows with the distinct posted ids. Each id **MUST** be a role with `del_flag` 0, or the call says `Unknown role`. An empty role list **MUST** say `Choose a role.` User 1 **MUST** keep role 1. The checks **MUST** finish before any write. A refusal **MUST** leave the columns and the link rows unchanged. One successful edit **MUST** write one `user_edit` audit row. The layout is section 6 of `requirement-html-user-management`.
7. **Remove.** `user-remove` **MUST** require `system:user:remove`. User 1 **MUST** say `The built-in administrator cannot be removed.` The signed-in account **MUST** say `You cannot remove the account you are using.` A listed account **MUST** be updated to `del_flag` 2. The action **MUST** delete that account's `sys_user_role` and `sys_user_job_title` rows.
8. **Reset.** `user-reset-password` **MUST** require `system:user:resetPwd`, a listed user, and a password of at least 5 characters. It **MUST** store a new hash and set `pwd_update_date`. The operation parameter **MUST** be the `user_name`.
9. **Audit.** Add **MUST** write `sys_oper_log` with title `User`, `business_type` 1, and method `user_add`. Edit and reset **MUST** use `business_type` 2. Remove **MUST** use `business_type` 3.
10. **Page.** `GET /users` **MUST** require `system:user:list`. The add, edit, reset, remove, and import forms **MUST** be omitted when the account lacks the matching permission. The export link **MUST** be omitted when `system:user:export` is absent. The layout of that page is `requirement-html-user-management`. The page **MUST** read the optional filters from its query string.
11. **Departments on the page.** `user_departments` **MUST** require `system:user:list`. An administrator, or a role with data scope 1, **MUST** receive every department with `del_flag` 0. Any other account **MUST** receive the departments of the unfiltered user list plus their ancestor departments, and **MUST NOT** receive a sibling department outside that set. The tree **MUST** stay the unfiltered set when the table is filtered.
12. **Import.** `user_import` **MUST** require `system:user:import` and **MUST NOT** also require `system:user:add`. The text is utf-8 csv. The header **MUST** include `user_name`, `nick_name`, `dept_id`, and `role_id`. `password`, `phonenumber`, and `status` are optional. A missing required column **MUST** say `The import file needs the columns user_name, nick_name, dept_id, and role_id.` An empty file **MUST** say `The import file has no accounts.` More than 200 accounts **MUST** say `An import accepts at most 200 accounts.` A new row **MUST** use the name, nick, department, role, and password rules of add. An empty password **MUST** use the initial password. `status` **MUST** be `0` or `1`, and an empty status **MUST** store `0`. `phonenumber` **MUST** be at most 11 characters. A listed `user_name` **MUST** say `That user_name is already in use.` unless `update_support` is set. With `update_support`, that account **MUST** update nick, department, role, status when the cell is present, phone when the column is present, and password when the cell is non-empty. It **MUST NOT** change `user_name`. Setting user 1 to any status other than `0` **MUST** say `The built-in administrator stays enabled.` A failing row **MUST** write no account from that file. One `sys_oper_log` row **MUST** use title `User`, `business_type` 1, and method `user_import`. The operation parameter **MUST** be the added and updated counts, and **MUST NOT** be a password.
13. **Export.** `user_export` **MUST** require `system:user:export`. It **MUST** use the same optional filters as `user_list`. The csv header **MUST** be `user_name,nick_name,dept_id,role_id,phonenumber,status`. `role_id` **MUST** be the minimum `role_id` on `sys_user_role` for that account. The file **MUST NOT** contain a password. The text-report columns stay the six names in section 2. `GET /users/export` **MUST** return that csv as `text/csv` with `Content-Disposition` attachment `users.csv`.
14. **Status switch.** `POST /users/status` **MUST** call `user_edit` with only `status`. It **MUST** require `system:user:edit`. It **MUST NOT** add a permission, a text-menu row, or a typed verb. `status` **MUST** be `0` or `1`. Setting user 1 to any status other than `0` **MUST** say `The built-in administrator stays enabled.` An id that is not in that account's `user_list` **MUST** say `That account is not in this list.` A successful call **MUST** write the same audit row as edit. The call **MUST NOT** replace `sys_user_job_title` or `sys_user_role`. The control on the page is section 6 of `requirement-html-element-plus`.
15. **Edit choices.** The job titles and the roles on the edit form **MUST** be readable by an account with `system:user:edit`. That read **MUST NOT** require `system:jobtitle:list` or `system:role:list`, and **MUST NOT** add a permission. The job titles **MUST** be the rows with `status` 0. The roles **MUST** be the rows with `del_flag` 0 and `status` 0. `user-add` **MUST NOT** insert `sys_user_job_title`. The layout is section 6 of `requirement-html-user-management`.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | Operator `user-list` returns only `operator` |
| AC-2 | Lead `user-list` returns `admin`, `clerk`, and `lead` |
| AC-3 | `user-add` with `user_name` `1bad` fails the name rule |
| AC-4 | `user-remove` of user 1 fails with the built-in administrator sentence |
| AC-5 | `user-add` with an empty password stores a hash of the initial-password parameter |
| AC-6 | The admin users page includes Add, Import, and Export. The operator users page omits Add, Import, Export, and `action="/users/add"` |
| AC-7 | An admin filter `user_name=clerk` returns `clerk`. Department 101 returns `admin`, `clerk`, and `lead`. Department 102 returns `operator` |
| AC-8 | Operator departments are Group and Operations. Lead departments are Group, Engineering, and Platform |
| AC-9 | A csv row for a new account adds that account and stores a hash of the initial password when the password cell is empty. The same name again fails with `That user_name is already in use.` and writes nothing from that file. `update_support` changes the nick. Status `1` for user 1 fails and user 1 stays enabled. Export of the filtered list contains the new `user_name` and does not contain `pbkdf2_sha256` or the password. Operator import and export fail with `Missing permission` |
| AC-10 | `POST /users/status` for an account in the list changes that status and keeps the search fields. User 1 stays enabled. An id outside the list is refused with `That account is not in this list.` An account without `system:user:edit` is refused with `Missing permission` |
| AC-11 | Editing a listed account can store a phone, an email, a sex, a remark, one department, a set of job titles, and a set of roles, and leaves `user_name` unchanged. An empty department fails with `A department is required.` An empty role set fails with `Choose a role.` User 1 keeps role 1 and stays enabled. A job title on that account does not change which accounts `user-list` returns. `POST /users/status` does not clear the job titles or the roles. An id outside the list fails with `That account is not in this list.` |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Listed account | `sys_user` with `del_flag` 0 |
| Initial password | `sys.user.initPassword`, or `123456` when that parameter is missing |
| Protected user | `user_id` 1. Remove and disable are refused |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | User list, add, edit, remove, and password reset |
| 2026-10-14 | Active 1.0.1 | The account link is `sys_user_job_title` |
| 2026-10-14 | Active 1.0.2 | The users page layout is `requirement-html-user-management` |
| 2026-10-14 | Active 1.0.3 | Optional list filters. The users tree uses `system:user:list` |
| 2026-10-14 | Active 1.0.4 | Csv import and export. Menus 1006 and 1007. No text-menu row and no typed verb |
| 2026-10-14 | Active 1.0.5 | POST /users/status calls user_edit with only status. The id must be in the actor's list |
| 2026-10-14 | Active 1.0.6 | Edit can replace phone, email, sex, remark, job titles, and roles. It does not change user_name. user-add still inserts no job title |

---

**Last Updated**: 2026-10-14
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
