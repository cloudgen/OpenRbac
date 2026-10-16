**file**: docs/requirements/requirement-rbac-departments.md
**Status**: Active (Version 1.0.1)
**Area**: domain
**Key**: `requirement-rbac-departments`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the department record. Departments form a tree. `ancestors` is the comma-separated path of parent ids. User lists use that path for data scope 4. Which user rows a scope returns stays on `requirement-rbac`. This file is the department list, the add action, and how `ancestors` is written.

### 1.1 Human-facing

**In one sentence:** An administrator sees every department and can add a child under a parent. The page opens as an expanded tree, and a parent can be contracted. The list is the whole tree.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account that adds a department | `admin` |
| The other role | The parent department | Engineering, id 101 |
| Not this file | Which accounts appear in a user list | `requirement-rbac-users` |

| Includes | Excludes |
|----------|----------|
| Department list and department add | Editing or removing a department |
| `ancestors` written from the parent | Data scope applied to this list |
| The seeded Group tree | A permission string stored on the department |

| Surface | What you open | What for |
|---------|---------------|----------|
| Text menu | rbac rows 110 and 111 | List, then add |
| Typed verb | `open-rbac dept-list` | The list |
| Web page | `/depts` | The list, and Add a department when add is allowed. The layout is `requirement-html-department-management` |

## 2. Actions

| Action | Permission | Menu row | Verb | Web |
|--------|------------|----------|------|-----|
| List | `system:dept:list` | 110 `dept-list` | `dept-list` | `GET /depts` |
| Add | `system:dept:add` | 111 `dept-add` | `dept-add` | `POST /depts/add` |

Common and lead do not receive the department list or department add.

The list columns are `dept_id`, `parent_id`, `dept_name`, `ancestors`, and `status`. A successful add prints `Added department {dept_id}.`

On an empty database the seed inserts this tree. A later init does not insert it again.

```text
Group (100)                 ancestors 0
├── Engineering (101)       ancestors 0,100
│   └── Platform (103)      ancestors 0,100,101
└── Operations (102)        ancestors 0,100
```

## 3. Normative rules

1. **One path.** List and add **MUST** call `Access.dept_list` and `Access.dept_add`. A missing permission **MUST** start with `Missing permission`.
2. **List.** `dept-list` **MUST** require `system:dept:list`. It **MUST** return every department with `del_flag` 0, ordered by `parent_id`, `order_num`, then `dept_id`. Data scope **MUST NOT** remove a row from this list.
3. **Name.** `dept_name` **MUST** be 1 to 30 characters after trimming. A blank name and a longer name **MUST** say `dept_name is required.`
4. **Parent and ancestors.** Parent id 0 **MUST** store `ancestors` as `0`. Any other parent **MUST** be a department with `del_flag` 0. An unknown parent **MUST** say `Unknown parent department`. The child's `ancestors` **MUST** be the parent's `ancestors`, a comma, and the parent's `dept_id`.
5. **New row.** The insert **MUST** set `order_num` 0, `status` 0, and `del_flag` 0. Add **MUST NOT** change `sys_role_dept`.
6. **Scope 4.** A user list with scope 4 **MUST** be able to match a child because `ancestors` contains the actor's department id. The match itself stays on `requirement-rbac`.
7. **Audit.** A successful add **MUST** write `sys_oper_log` with title `Department`, `business_type` 1, method `dept_add`, and the department name as the parameter.
8. **Page.** `GET /depts` **MUST** require `system:dept:list`. The add form **MUST** be omitted when the account lacks `system:dept:add`. The layout of that page is `requirement-html-department-management`. The tree **MUST** open expanded, and a parent **MUST** be able to contract.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | Admin `dept-list` includes Group, Engineering, Operations, and Platform |
| AC-2 | `dept-add` under department 101 stores `ancestors` `0,100,101` |
| AC-3 | Admin `dept-list` still includes Operations. The list is the whole tree |
| AC-4 | `dept-add` with parent 999 fails with `Unknown parent department` |
| AC-5 | Operator `dept-list` fails with `Missing permission system:dept:list` |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Root parent | `parent_id` 0. The new row's `ancestors` is `0` |
| Ancestors | The comma-separated parent path stored on the child |
| Whole tree | Every department with `del_flag` 0 |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Department list, add, and ancestors |
| 2026-10-14 | Active 1.0.1 | The page layout is `requirement-html-department-management`. The tree expands and contracts |

---

**Last Updated**: 2026-10-14
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
