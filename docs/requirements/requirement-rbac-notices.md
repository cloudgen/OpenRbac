**file**: docs/requirements/requirement-rbac-notices.md
**Status**: Active (Version 1.0.0)
**Area**: domain
**Key**: `requirement-rbac-notices`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the notice record. A notice is one row in `sys_notice`. Type `1` is a notice. Type `2` is an announcement. The list shows the title, the type, and the status. The body is stored and is not a list column. List and publish go through `Catalog`.

### 1.1 Human-facing

**In one sentence:** An operator can read notices. An administrator can publish one.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account that publishes | `admin` |
| The other role | The notice type | `2`, an announcement |
| Not this file | The dictionary labels for those type numbers | `requirement-rbac-dictionaries` |

| Includes | Excludes |
|----------|----------|
| Notice list and notice add | Editing or removing a notice |
| Type 1 and type 2 | A type taken from a free-text dictionary at publish time |
| The seeded welcome announcement | The notice body on the list |

| Surface | What you open | What for |
|---------|---------------|----------|
| Text menu | setup rows 216 and 217 | List, then add |
| Typed verb | `open-rbac notice-list` | The list |
| Web page | `/notices` | The list, and Publish a notice when add is allowed |

## 2. Actions

| Action | Permission | Menu row | Verb | Web |
|--------|------------|----------|------|-----|
| List | `system:notice:list` | 216 `notice-list` | `notice-list` | `GET /notices` |
| Publish | `system:notice:add` | 217 `notice-add` | `notice-add` | `POST /notices/add` |

Common receives notice list. It does not receive notice add. Lead receives neither.

The list columns are `notice_id`, `notice_title`, `notice_type`, and `status`. A successful publish prints `Added notice {notice_title}.`

On an empty database the seed inserts notice 1, title `Welcome`, type `2`, content `OpenRbac is ready.`, status `0`.

The typed verb takes `--notice-title`. An omitted `--notice-type` is type `1`. The page posts the title in the field `title`. An empty type on that form is type `1`.

## 3. Normative rules

1. **One path.** List and publish **MUST** call `Catalog.notice_list` and `Catalog.notice_add`. A missing permission **MUST** start with `Missing permission`.
2. **List.** `notice-list` **MUST** require `system:notice:list`. It **MUST** return every notice, ordered by `notice_id`. The list **MUST** include `notice_title`, `notice_type`, and `status`. It **MUST NOT** require `notice_content` as a column.
3. **Title.** The title **MUST** be 1 to 50 characters after trimming. A blank title and a longer title **MUST** say `The notice title is required.`
4. **Type.** `notice_type` **MUST** be `1` or `2`. Any other value **MUST** say `notice_type must be 1 (notice) or 2 (announcement).` An omitted type on the verb, and an empty type on the page, **MUST** be stored as `1`.
5. **New row.** Content **MAY** be empty. The insert **MUST** set `status` 0 and **MUST** store the content that was submitted.
6. **Audit.** A successful publish **MUST** write `sys_oper_log` with title `Notice`, `business_type` 1, method `notice_add`, and the notice title as the parameter.
7. **Page.** `GET /notices` **MUST** require `system:notice:list`. The publish form **MUST** be omitted when the account lacks `system:notice:add`.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | A fresh `notice-list` includes `Welcome` with `notice_type` 2 |
| AC-2 | `notice-add` with type `3` fails |
| AC-3 | `notice-add` with an empty title fails with `The notice title is required.` |
| AC-4 | Operator `notice-list` includes `Welcome` |
| AC-5 | Operator `notice-add` fails with `Missing permission system:notice:add` |
| AC-6 | `notice-add` with no `--notice-type` stores type `1` |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Notice | `notice_type` 1 |
| Announcement | `notice_type` 2 |
| Publish | `notice-add`, which inserts one `sys_notice` row with `status` 0 |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Notice list and publish |

---

**Last Updated**: 2026-10-14
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
