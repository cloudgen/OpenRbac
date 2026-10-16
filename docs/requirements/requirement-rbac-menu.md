**file**: docs/requirements/requirement-rbac-menu.md
**Status**: Active (Version 1.2.2)
**Area**: domain
**Key**: `requirement-rbac-menu`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the menu record. A menu row is a directory, a page, or a button. The permission string is `perms`. An account reaches a string through `sys_role_menu`, as `requirement-rbac` describes. This file is the list, the add action, and the page actions edit, remove, and save sort. The text-menu row numbers are `requirement-python-tui`.

### 1.1 Human-facing

**In one sentence:** An administrator can read the menu tree, add a directory, a page, or a button, and change or remove a menu. The page opens with every branch contracted.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account that adds a button | `admin` |
| The other role | The new permission string | `system:user:export` |
| Not this file | Which role receives the seeded menus | `requirement-rbac` |

| Includes | Excludes |
|----------|----------|
| Menu list, menu add, and the page actions edit, remove, and save sort | A typed verb for edit, remove, or save sort |
| Types `M`, `C`, and `F` | A second allow-list beside `perms` |
| Parent id 0 as the root | Hiding a disabled menu by deleting the row |
| The page opens contracted. `Expand/Collapse` and a caret open branches | A script that expands the tree |

| Surface | What you open | What for |
|---------|---------------|----------|
| Text menu | rbac rows 18 and 19 | List, then add |
| Typed verb | `open-rbac menu-list` | The list |
| Web page | `/menus` | That list, the toolbar, and a form only when the permission is present |

## 2. Actions

| Action | Permission | Menu row | Verb | Web |
|--------|------------|----------|------|-----|
| List | `system:menu:list` | 18 `menu-list` | `menu-list` | `GET /menus` |
| Add | `system:menu:add` | 19 `menu-add` | `menu-add` | `POST /menus/add` |
| Edit | `system:menu:edit` | none | none | `POST /menus/edit` |
| Remove | `system:menu:remove` | none | none | `POST /menus/remove` |
| Save sort | `system:menu:edit` | none | none | `POST /menus/sort` |

Common and lead do not receive the menu list, menu add, menu edit, or menu remove.

The text-report columns are `menu_id`, `parent_id`, `menu_name`, `menu_type`, and `perms`. A successful add prints `Added menu {menu_id}.`

`menu_type` `M` is a directory, `C` is a page, and `F` is a button. The seed uses those letters. The seeded ids and permission strings are `Schema.MENUS` in `schema.py`. An empty `sys_user` inserts that set once (`requirement-rbac`).

The seed inserts menu 1022, Menu edit, with `system:menu:edit`, and menu 1023, Menu remove, with `system:menu:remove`. The administrator role receives them on a fresh database. `role_key` `admin` passes the check without those rows. A database created before those menus does not gain them. Rows 18 and 19 stay the two text-menu actions. Edit, remove, and save sort call `Access` from the menus page and are not text-menu rows.

## 3. Normative rules

1. **One path.** List and add **MUST** call `Access.menu_list` and `Access.menu_add`. Edit **MUST** call `Access.menu_edit`. Remove **MUST** call `Access.menu_remove`. Save sort **MUST** call `Access.menu_sort`. A missing permission **MUST** start with `Missing permission`. Edit, remove, and save sort **MUST NOT** add a text-menu row or a typed verb.
2. **List.** `menu-list` **MUST** require `system:menu:list`. It **MUST** return rows with `status` 0, ordered by `parent_id`, `order_num`, then `menu_id`. A row with `status` other than 0 **MUST** stay off the list. `sys_menu` has no `del_flag`. The text report **MUST** keep the five column names above. The list **MAY** also return `order_num`, `path`, and `visible` for the page.
3. **Name and type.** `menu_name` **MUST** be 1 to 50 characters after trimming. A blank name and a longer name **MUST** say `menu_name is required.` `menu_type` **MUST** be `M`, `C`, or `F`. Any other type **MUST** say `menu_type must be M, C, or F.` The typed verb **MUST** require the type. An empty type on `POST /menus/add` **MUST** be stored as `F`. An empty type on edit **MUST** use that same sentence and **MUST NOT** be stored as `F`.
4. **Parent.** Parent id 0 **MUST** be accepted as the root. Any other parent **MUST** exist on `sys_menu`. An unknown parent **MUST** say `Unknown parent menu`.
5. **New row.** The insert **MUST** set `order_num` 0, `visible` 0, and `status` 0. An omitted permission string or path **MUST** be stored as an empty string. Add **MUST NOT** attach the new id to a role. A role sees the new string only after grant (`requirement-rbac-roles`).
6. **Audit.** A successful add **MUST** write `sys_oper_log` with title `Menu`, `business_type` 1, method `menu_add`, and the menu name as the parameter. Edit and save sort **MUST** use `business_type` 2 and methods `menu_edit` and `menu_sort`. Remove **MUST** use `business_type` 3 and method `menu_remove`.
7. **Page.** `GET /menus` **MUST** require `system:menu:list`. The add form **MUST** be omitted when the account lacks `system:menu:add`. The edit form and Save sort **MUST** be omitted when the account lacks `system:menu:edit`. The remove form **MUST** be omitted when the account lacks `system:menu:remove`. Edit or remove with no menu id **MUST** say `Choose a menu.` An id that is not in `menu_list` **MUST** say `That menu is not in this list.` Either sentence **MUST** omit the form. When edit is allowed, the first header is a checkbox with `aria-label="check all"` and no `name`, and each row is a checkbox named `menu_id`. The header cell and each row cell use `table-check-col`. The header is not the word `Choose`. `/table-check.js` checks or unchecks every row box in that table. The header box is not posted. Edit and Remove still use the first posted id. The page does not delete many rows. The column is omitted when edit is not allowed, and then the page has no script tag. A row shows Edit when edit is allowed, Add when add is allowed, and Remove when remove is allowed. Save sort posts one `menu_id` and one `order_num` for each visible row. A successful add, edit, remove, or save sort **MUST** return to `/menus` and keep the posted menu name, visibility, and closed branches.
8. **Edit.** `menu_edit` **MUST** require `system:menu:edit` and a row with `status` 0. An unknown id **MUST** say `Unknown menu`. It **MUST** store the posted name, parent, type, permission, path, and visible. It **MUST NOT** change `order_num`. A parent equal to the menu, or a descendant of the menu, **MUST** say `A menu cannot sit under itself.` An empty visible **MUST** store `0`. Any other visible **MUST** say `visible must be 0 or 1.`
9. **Remove.** `menu_remove` **MUST** require `system:menu:remove` and a row with `status` 0. An unknown id **MUST** say `Unknown menu`. A `status` 0 child **MUST** say `That menu has children.` and **MUST** leave the row in place. Otherwise the action **MUST** delete that id from `sys_role_menu` and **MUST** delete the `sys_menu` row. The audit parameter **MUST** be the menu name.
10. **Save sort.** `menu_sort` **MUST** require `system:menu:edit`. The two lists **MUST** have the same length, or the call says `Choose a sort for each menu.` Each id **MUST** be a `status` 0 row, or the call says `Unknown menu`. Each order **MUST** be a whole number from 0 to 9999, or the call says `order_num must be a number.` An empty order **MUST** store 0. A failed check **MUST NOT** change a stored order. The audit parameter **MUST** be the count of updated rows.
11. **Contracted start.** `GET /menus` with no `closed` value and no menu-name or visibility filter **MUST** show the roots and **MUST** hide every child. Every branch caret **MUST** be `menu-twist is-shut`. `Expand/Collapse` **MUST** be a link. On that page its target **MUST** include `closed=open`, and that address **MUST** show every kept row with each branch caret `menu-twist is-open`. On any page that is not fully contracted, `Expand/Collapse` **MUST** list every branch id in `closed`, and that address **MUST** show only the roots. A caret **MUST** change that branch only. Opening a branch **MUST** leave a still-contracted descendant contracted. `closed=open` **MUST** mean every branch is open. A comma-separated list of ids **MUST** mean those branches are contracted and the other branches are open. A name or visibility filter with no `closed` value **MUST** show the match and the ancestors that connect it. The page **MUST NOT** use a script to expand or contract.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | Admin `menu-list` includes User, type `C`, perms `system:user:list` |
| AC-2 | `menu-add` with type `X` fails |
| AC-3 | `menu-add` with parent 0 and type `F` appears on the next `menu-list` |
| AC-4 | Operator `menu-list` fails with `Missing permission system:menu:list` |
| AC-5 | A new menu id is absent from `sys_role_menu` until a grant includes it |
| AC-6 | Edit stores the new name, parent, type, permission, path, and visible, and leaves `order_num` unchanged. A menu under itself or under its child fails with `A menu cannot sit under itself.` An unknown parent fails with `Unknown parent menu`. An empty type fails with `menu_type must be M, C, or F.` and stays unchanged |
| AC-7 | Remove of a menu that has a `status` 0 child fails with `That menu has children.` Remove of a child deletes the row and its `sys_role_menu` links. A `status` other than 0 fails with `Unknown menu` |
| AC-8 | Save sort stores an empty order as 0 and stores 9999. `nope` and `10000` fail with `order_num must be a number.` A shorter order list fails with `Choose a sort for each menu.` The stored orders stay unchanged after a failed call |
| AC-9 | The admin menus page includes Add, Edit, Save sort, a checkbox `aria-label="check all"`, a checkbox named `menu_id`, class `table-check-col`, and Remove. The only script is `<script src="/table-check.js"></script>`. The header is not the word `Choose`. `?form=edit` with no id says `Choose a menu.` and omits the edit form. An account without `system:menu:edit` omits Edit, Save sort, `aria-label="check all"`, and `action="/menus/sort"`, and contains no `<script` tag. Operator edit fails with `Missing permission` |
| AC-10 | `GET /menus` with no query shows `System`, hides `User`, and includes `menu-twist is-shut` and `closed=open`. `GET /menus?closed=open` shows `User` and `User query`. `GET /menus?closed=1` shows `System` and hides `User` |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Directory | `menu_type` `M` |
| Page | `menu_type` `C` |
| Button | `menu_type` `F` |
| Permission string | `sys_menu.perms` |
| Save sort | Replace `order_num` for each posted menu id |
| Contracted | A branch whose children are hidden. The caret is `menu-twist is-shut` |
| `closed=open` | Every branch is open. It is not a menu id |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | Menu list and add |
| 2026-10-14 | Active 1.1.0 | Page edit, remove, and save sort. No typed verb and no text-menu row |
| 2026-10-15 | Active 1.2.0 | The menu page opens contracted. `Expand/Collapse` opens every branch |
| 2026-10-16 | Active 1.2.1 | The menu table uses a check-all checkbox and a row checkbox named `menu_id`. The header is not the word Choose |
| 2026-10-16 | Active 1.2.2 | The checkbox column is centered. `/table-check.js` checks every row box in that table |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
