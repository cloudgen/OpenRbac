**file**: docs/requirements/requirement-rbac-parameters.md
**Status**: Active (Version 1.1.0)
**Area**: domain
**Key**: `requirement-rbac-parameters`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the parameter record. A parameter is one row in `sys_config`. The product reads `sys.user.initPassword` when a new account omits a password (`requirement-rbac-users`). The other seeded keys are stored and listed. List, change, and add go through `Catalog`. The text menu and the typed verb call that class. The parameters page calls list and change. Its layout is `requirement-html-parameter-management`.

### 1.1 Human-facing

**In one sentence:** An operator can read the parameters. An administrator can change one and can add one.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account that changes a value | `admin` |
| The other role | The parameter key | `sys.user.initPassword` |
| Not this file | The engine choice on the Database page | `requirement-web-interface` |

| Includes | Excludes |
|----------|----------|
| Parameter list, change, and add | Deleting a parameter |
| The initial-password key used by user add | Turning captcha or open registration on from the seeded keys |
| Change on the parameters page | An add form on that page |

| Surface | What you open | What for |
|---------|---------------|----------|
| Text menu | setup rows 211–213 | List, change, and add |
| Typed verb | `open-rbac config-list` | The list |
| Web page | `/configs` | The list, and Change a parameter when edit is allowed. The layout is `requirement-html-parameter-management` |

## 2. Actions

| Action | Permission | Menu row | Verb | Web |
|--------|------------|----------|------|-----|
| List | `system:config:list` | 211 `config-list` | `config-list` | `GET /configs` |
| Change | `system:config:edit` | 212 `config-set` | `config-set` | `POST /configs/set` |
| Add | `system:config:add` | 213 `config-add` | `config-add` | The verb and row 213. The parameters page has no add form |

Common receives parameter list. It does not receive parameter edit or parameter add. Lead receives neither the list nor the edits.

The text-report columns are `config_key`, `config_name`, `config_value`, and `config_type`. The page columns are `requirement-html-parameter-management`. A successful change prints `Set {config_key}.` A successful add prints `Added parameter {config_key}.`

On an empty database the seed inserts these parameters. `config_type` `Y` marks a seeded built-in key. An added key is stored as `N`.

| config_key | config_name | config_value | config_type |
|------------|-------------|--------------|-------------|
| `sys.index.skinName` | Skin name | `skin-blue` | `Y` |
| `sys.user.initPassword` | Initial password | `123456` | `Y` |
| `sys.account.captchaEnabled` | Captcha | `false` | `Y` |
| `sys.account.registerUser` | Registration | `false` | `Y` |

## 3. Normative rules

1. **One path.** List, change, and add **MUST** call `Catalog.config_list`, `Catalog.config_set`, and `Catalog.config_add`. A missing permission **MUST** start with `Missing permission`.
2. **List.** `config-list` **MUST** require `system:config:list`. It **MUST** return every parameter, ordered by `config_id`, with `config_id`, `config_name`, `config_key`, `config_value`, `config_type`, `remark`, and `create_time`. The text report **MUST** keep the four column names above.
3. **Change.** `config-set` **MUST** require `system:config:edit`. An unknown `config_key` **MUST** say `Unknown parameter`. The value **MUST** be 500 characters or fewer. A longer value **MUST** say `config_value must be 500 characters or fewer.` The update **MUST** set `config_value`, `update_by`, and `update_time`.
4. **Add.** `config-add` **MUST** require `system:config:add`. The verb and setup row 213 **MUST** require `config_key`, `config_name`, and `config_value`. An empty field **MUST** fail before the insert. The sentence **MUST** be `config-key is required.`, `config-name is required.`, or `config-value is required.` `config_key` **MUST** be 1 to 100 characters after trimming. A key longer than 100 characters **MUST** say `config_key is required.` A key that already exists **MUST** say `That parameter already exists.` A stored `config_name` **MUST** be at most 100 characters. A stored `config_value` **MUST** be at most 500 characters. `config_type` **MUST** be `N`.
5. **Initial password.** `Access` **MUST** read `sys.user.initPassword` when `user-add` omits a password. Changing that value **MUST** change the password used by the next such add. The product **MUST** store `sys.index.skinName`, `sys.account.captchaEnabled`, and `sys.account.registerUser`. It **MUST NOT** enable a captcha or open registration from those values.
6. **Audit.** Change **MUST** write `sys_oper_log` with title `Parameter`, `business_type` 2, and method `config_set`. Add **MUST** use `business_type` 1 and method `config_add`. The parameter **MUST** be the `config_key`.
7. **Page.** `GET /configs` **MUST** require `system:config:list`. The change form **MUST** be omitted when the account lacks `system:config:edit`. This page **MUST NOT** post to an add action. Add stays on the verb and on setup row 213. The layout of that page is `requirement-html-parameter-management`. The page **MUST** read the optional filters from its query string. The verb `config-list` **MUST** still return every parameter.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | A fresh `config-list` includes `sys.user.initPassword` with value `123456` |
| AC-2 | Operator `config-set` fails with `Missing permission system:config:edit` |
| AC-3 | `config-set` of an unknown key fails with `Unknown parameter` |
| AC-4 | `config-add` of a new key, then `config-set`, stores the new value |
| AC-5 | `config-set` with a value longer than 500 characters is refused |
| AC-6 | Operator `config-list` includes the seeded keys. The parameters page omits Change a parameter |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Parameter | One `sys_config` row, named by `config_key` |
| Built-in key | `config_type` `Y` on a seeded row |
| Initial password | The value of `sys.user.initPassword` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Parameter list, change, and add |
| 2026-10-14 | Active 1.1.0 | The parameters page layout is `requirement-html-parameter-management`. `config-list` also returns id, remark, and create time |

---

**Last Updated**: 2026-10-14
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
