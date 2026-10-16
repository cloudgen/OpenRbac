**file**: docs/requirements/requirement-rbac-job-titles.md
**Status**: Active (Version 1.2.2)
**Area**: domain
**Key**: `requirement-rbac-job-titles`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the job title record. A job title names a job. It does not grant a permission string and it does not change data scope. `user-add` does not attach a job title. `user-edit` may replace that user's `sys_user_job_title` rows (`requirement-rbac-users`). Removing a user deletes that user's `sys_user_job_title` rows (`requirement-rbac-users`).

### 1.1 Human-facing

**In one sentence:** An administrator can list job titles and add one. Adding a title does not let anyone see more accounts.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account that adds a job title | `admin` |
| The other role | The job code | `se` |
| Not this file | The permission check and data scope | `requirement-rbac` |

| Includes | Excludes |
|----------|----------|
| Job title list and job title add | Editing or removing a job title |
| A unique `job_title_code` | A permission string on the job title |
| The four seeded titles | Assigning the new job title to a user from this action |

| Surface | What you open | What for |
|---------|---------------|----------|
| Text menu | rbac rows 112 and 113 | List, then add |
| Typed verb | `open-rbac job-title-list` | The list |
| Web page | `/job-titles` | The list, and add a job titles when add is allowed. The layout is `requirement-html-job-titles` |

## 2. Actions

| Action | Permission | Menu row | Verb | Web |
|--------|------------|----------|------|-----|
| List | `system:jobtitle:list` | 112 `job-title-list` | `job-title-list` | `GET /job-titles` |
| Add | `system:jobtitle:add` | 113 `job-title-add` | `job-title-add` | `POST /job-titles/add` |

The list label is `Job Titles`. The add label is `add a job titles`. Common and lead do not receive the job title list or job title add.

The text-report columns are `job_title_id`, `job_title_code`, `job_title`, `job_title_sort`, and `status`. The page columns are `requirement-html-job-titles`. A successful add prints `Added job title {job_title_id}.`

On an empty database the seed inserts these titles. `sys_job_title` has no `del_flag`. A database that already has users and an empty `sys_job_title` receives the same rows from `sys_post`. `post_code` is stored as `job_title_code` and `post_name` is stored as `job_title`. That copy is `requirement-database`.

| job_title_id | job_title_code | job_title |
|--------------|----------------|-----------|
| 1 | `ceo` | Chief |
| 2 | `se` | Engineer |
| 3 | `hr` | People |
| 4 | `user` | Staff |

## 3. Normative rules

1. **One path.** List and add **MUST** call `Access.job_title_list` and `Access.job_title_add`. A missing permission **MUST** start with `Missing permission`.
2. **List.** `job-title-list` **MUST** require `system:jobtitle:list`. It **MUST** return every job title, ordered by `job_title_sort` then `job_title_id`.
3. **Add.** `job_title_code` and `job_title` **MUST** both be present after trimming. A missing value **MUST** say `job_title_code and job_title are required.` A `job_title_code` that already exists **MUST** say `That job_title_code is already in use.` The insert **MUST** set `job_title_sort` 0 and `status` 0.
4. **No grant.** Add **MUST NOT** insert `sys_user_job_title`, **MUST NOT** write `sys_menu.perms`, and **MUST NOT** change `sys_role.data_scope`. A later user list **MUST** show the same accounts it showed before the job title was added.
5. **Audit.** A successful add **MUST** write `sys_oper_log` with title `Job Title`, `business_type` 1, method `job_title_add`, and the `job_title_code` as the parameter.
6. **Page.** `GET /job-titles` **MUST** require `system:jobtitle:list`. The add form **MUST** be omitted when the account lacks `system:jobtitle:add`. The layout of that page is `requirement-html-job-titles`. The page **MUST** read the optional filters from its query string. The verb `job-title-list` **MUST** still return every job title.
7. **User edit.** Job title add **MUST NOT** assign the new title to a user. `user-edit` **MAY** replace one user's `sys_user_job_title` rows. That replacement **MUST NOT** grant a permission and **MUST NOT** change data scope.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | Admin `job-title-list` includes `ceo`, `se`, `hr`, and `user` |
| AC-2 | `job-title-add` with `job_title_code` `ceo` fails with the already-in-use sentence |
| AC-3 | After `job-title-add`, operator `user-list` still returns only `operator` |
| AC-4 | Operator `job-title-list` fails with `Missing permission system:jobtitle:list` |

## Terminologies

A job title is a named job in `sys_job_title`. The name says what the job is called. It does not hand over a permission.

| Term | Meaning in this file |
|------|----------------------|
| Job title | A named job in `sys_job_title` |
| jobtitle | The compact token in `system:jobtitle:list` and `system:jobtitle:add` |
| Job Titles | The list label |
| add a job titles | The add label |
| Job title code | The unique `job_title_code` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Post list and add |
| 2026-10-14 | Active 1.1.0 | The record is a job title. Routes, columns, and verbs use that name |
| 2026-10-14 | Active 1.2.0 | The job titles page layout is `requirement-html-job-titles` |
| 2026-10-14 | Active 1.2.1 | Edit a user may replace `sys_user_job_title`. Add still assigns nobody |
| 2026-10-14 | Active 1.2.2 | An empty job-title table is filled from `sys_post` |

---

**Last Updated**: 2026-10-14
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
