**file**: docs/requirements/requirement-rbac.md
**Status**: Active (Version 1.0.0)
**Area**: domain
**Key**: `requirement-rbac`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the permission and data-scope law. A signed-in account may do an action only when one of its menus carries that permission string, or when a role key is `admin`. A user list shows only the departments the account's roles allow.

The scope numbers follow the studied `sys_role.data_scope` comment: 1 all, 2 custom departments, 3 this department, 4 this department and children. Scope 5 is not granted. An unknown scope contributes no rows.

### 1.1 Human-facing

**In one sentence:** An administrator sees every account, a department operator sees that department, and a lead also sees child departments.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account in the session file or the web cookie | `operator` |
| The other role | A permission string on a menu | `system:user:list` |
| Not this file | How the page is drawn | `requirement-web-interface` |

| Includes | Excludes |
|----------|----------|
| Permission strings and data scope 1–4 | A scope that means "only my own row" |
| Protected administrator user and role | Deleting user 1 or narrowing role 1 |
| Seeded admin, operator, clerk, and lead | A copied upstream password hash |

## 2. Normative rules

1. **Admin bypass.** A role whose `role_key` is `admin` **MUST** pass every permission check and **MUST** see every non-deleted user.
2. **Permission fail closed.** Any other account **MUST** be refused when the permission string is absent. The refusal **MUST** start with `Missing permission`.
3. **Data scope.** User lists **MUST** apply scope 1 as all rows, scope 2 as the role's department list, scope 3 as the actor's department, and scope 4 as that department plus departments whose ancestors contain it. Any other scope **MUST** add no rows. No matching scope **MUST** show no users.
4. **Names.** A new `user_name` **MUST** match `^[A-Za-z][A-Za-z0-9_]{2,29}$`.
5. **Passwords.** Stored passwords **MUST** use `pbkdf2_sha256$iterations$salt$hash` with 260000 iterations. Comparison **MUST** use `hmac.compare_digest`. An unknown account **MUST** still run a dummy verify. The product **MUST NOT** log a password.
6. **Protected rows.** User 1 **MUST NOT** be removed or disabled. Role 1 **MUST NOT** be granted a different scope or menu set through `role-grant`. The signed-in account **MUST NOT** remove itself.
7. **Seed.** When `sys_user` is empty, `db-init` **MUST** create admin (department 101, role admin, password `admin123`), operator (department 102, role common, scope 3, password `operator123`), clerk (department 103, role common, password `clerk123`), and lead (department 101, role lead, scope 4, password `lead123`). Common menus include user list and query, parameter list, notice list, operation log, and login log. They **MUST NOT** include user add, parameter edit, or force logout. Lead menus are system, user list, and user query.
8. **Audit.** A failed and a successful login **MUST** write `sys_logininfor`. A mutation **MUST** write `sys_oper_log`. The operation parameter **MUST NOT** be a password.

## 3. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | Operator user-list returns only `operator` |
| AC-2 | Lead user-list returns `admin`, `clerk`, and `lead` |
| AC-3 | Scope 5 on the common role returns no users |
| AC-4 | Operator user-add and config-set fail with Missing permission |
| AC-5 | user-remove 1, disabling user 1, and role-grant on role 1 fail |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Permission string | A menu `perms` value such as `system:user:add` |
| Data scope | The `data_scope` column: 1, 2, 3, or 4 |
| Protected user | `user_id` 1 |
| Protected role | `role_id` 1, role key `admin` |
| Soft delete | `del_flag` 2. Listed users have `del_flag` 0 |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-11 | Active 1.0.0 | Permissions, scope 1–4, seed, and protected rows |

---

**Last Updated**: 2026-10-11
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
