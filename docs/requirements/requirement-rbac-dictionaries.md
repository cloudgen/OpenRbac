**file**: docs/requirements/requirement-rbac-dictionaries.md
**Status**: Active (Version 1.1.0)
**Area**: domain
**Key**: `requirement-rbac-dictionaries`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the dictionary record. A dictionary type is a name in `sys_dict_type`. A dictionary value is a label in `sys_dict_data` with the same `dict_type` string. The product can list values and can add a value under a type that already exists. It has no verb that creates a type. The page lists the types. Its layout is `requirement-html-dictionaries`.

### 1.1 Human-facing

**In one sentence:** An administrator can read the labels and can add a label under a dictionary that the seed already created.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account that adds a label | `admin` |
| The other role | The dictionary type | `sys_user_sex` |
| Not this file | The notice type check, which uses the numbers 1 and 2 directly | `requirement-rbac-notices` |

| Includes | Excludes |
|----------|----------|
| The value list, the value add, and the type list on the page | A verb that inserts `sys_dict_type` |
| Add only when the type exists and its status is 0 | Rejecting a second copy of the same label |
| The seeded sex, status, and notice labels | Using the dictionary as the permission check |

| Surface | What you open | What for |
|---------|---------------|----------|
| Text menu | setup rows 214 and 215 | List, then add |
| Typed verb | `open-rbac dict-list` | The list |
| Web page | `/dicts` | The type list, and Add a dictionary value when add is allowed. The layout is `requirement-html-dictionaries` |

## 2. Actions

| Action | Permission | Menu row | Verb | Web |
|--------|------------|----------|------|-----|
| List | `system:dict:list` | 214 `dict-list` | `dict-list` | `GET /dicts` |
| Add a value | `system:dict:add` | 215 `dict-add` | `dict-add` | `POST /dicts/add` |

Common and lead do not receive the dictionary list or dictionary add.

The text-report columns are `dict_type`, `dict_label`, `dict_value`, and `status`. The page columns are `requirement-html-dictionaries`. A successful add prints `Added dictionary value {dict_label}.`

On an empty database the seed inserts these types and values.

| dict_type | dict_name | Labels |
|-----------|-----------|--------|
| `sys_user_sex` | User sex | Male `0` (default), Female `1`, Unknown `2` |
| `sys_normal_disable` | Normal or disabled | Normal `0` (default), Disabled `1` |
| `sys_notice_type` | Notice type | Notice `1` (default), Announcement `2` |

## 3. Normative rules

1. **One path.** List and add **MUST** call `Catalog.dict_list` and `Catalog.dict_add`. A missing permission **MUST** start with `Missing permission`.
2. **List.** `dict-list` **MUST** require `system:dict:list`. It **MUST** return every `sys_dict_data` row, ordered by `dict_type`, `dict_sort`, then `dict_code`.
3. **Type.** `dict-add` **MUST** require `system:dict:add`. The `dict_type` **MUST** match a `sys_dict_type` row whose `status` is 0. Any other type **MUST** say `Unknown dictionary type`. This action **MUST NOT** insert a type.
4. **Label and value.** Both **MUST** be present after trimming. A missing one **MUST** say `dict_label and dict_value are required.` Each **MUST** be stored at 100 characters or fewer. The new row **MUST** set `dict_sort` 0, `is_default` `N`, and `status` 0.
5. **Audit.** A successful add **MUST** write `sys_oper_log` with title `Dictionary`, `business_type` 1, method `dict_add`, and the `dict_type` as the parameter.
6. **Page.** `GET /dicts` **MUST** require `system:dict:list`. The add form **MUST** be omitted when the account lacks `system:dict:add`. The layout of that page is `requirement-html-dictionaries`. The page **MUST** read the optional filters from its query string. The verb `dict-list` **MUST** still return every value.
7. **Type rows.** The page **MUST** call `Catalog.dict_type_list`. That method **MUST** require `system:dict:list`. It **MUST** return every `sys_dict_type` row, ordered by `dict_id`, with `dict_id`, `dict_name`, `dict_type`, `status`, `remark`, and `create_time`. It **MUST NOT** insert a type, and it **MUST NOT** add a verb or a menu row.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | Admin `dict-list` includes Male `0` under `sys_user_sex` and Notice `1` under `sys_notice_type` |
| AC-2 | `dict-add` with an unknown type fails with `Unknown dictionary type` |
| AC-3 | `dict-add` of a label on `sys_notice_type` appears on the next `dict-list` |
| AC-4 | Operator `dict-list` fails with `Missing permission system:dict:list` |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Dictionary type | `sys_dict_type.dict_type`, for example `sys_user_sex` |
| Dictionary value | One `sys_dict_data` row. `dict_type` matches the type string, not `dict_id` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Dictionary value list and add |
| 2026-10-14 | Active 1.1.0 | The dictionaries page layout is `requirement-html-dictionaries` |

---

**Last Updated**: 2026-10-14
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
