**file**: docs/requirements/requirement-html-department-management.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-html-department-management`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the Department Management page. The studied document is the RuoYi department list, title `部门管理`. That document is a table of departments. A parent row has a caret. The caret expands that parent, and the same caret contracts it. A toolbar control expands every parent or contracts every parent. The list opens with every parent expanded. OpenRbac serves that page as `GET /depts`.

The list rows, the permission strings, the add action, and `ancestors` stay on `requirement-rbac-departments`. The shell, the theme, and the ban on a script stay on `requirement-python-html-template`, `requirement-html-theme`, and `requirement-html-javascript`. The users organization tree stays section 5 of `requirement-html-element-plus`. This page is not that diagram.

### 1.1 Human-facing

**In one sentence:** Departments is a tree table that opens expanded, and a reader can contract one parent or every parent.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The account opening Departments | `admin` |
| The other role | The sidebar link | Access → Departments → `/depts` |
| Not this file | Who may list a department, and how `ancestors` is stored | `requirement-rbac-departments` |

| Includes | Excludes |
|----------|----------|
| A tree of every department, expanded when the page opens | A flat table sorted only by `parent_id` |
| A caret that expands and contracts one parent | A script that toggles the rows |
| One control that expands every parent or contracts every parent | Edit, remove, and save sort |
| The add form when add is allowed | The studied search row |

| Surface | What you open | What for |
|---------|---------------|----------|
| Sidebar | Access, then Departments | `GET /depts` |
| Page | `templates/depts.vue` inside the shell | The tree and the add form |
| Studied page | `部门管理` | The caret and the expand/collapse control, under the OpenRbac path |

## 2. The studied page

| Piece in the studied document | OpenRbac |
|-------------------------------|----------|
| The list opens with every parent expanded | Every branch checkbox is checked. The children are shown |
| A caret on a parent. Down while expanded, and to the right while contracted | `label.dept-caret` for that department. The stylesheet draws the triangle |
| A leaf has no caret | The row carries `dept-leaf`. The stylesheet hides `.dept-leaf .dept-caret` |
| Children sit under the parent, and the name is indented | The child nodes sit in `.dept-children` inside the parent. The name padding follows the depth |
| Toolbar `展开/折叠` | `Expand/Collapse`. It is a label for `dept-fold-all`. The first activation contracts every branch. The next activation expands every branch whose own caret is still open |
| `新增` | The add form from `requirement-rbac-departments`, when `system:dept:add` is allowed |
| `修改`, `保存排序`, row `编辑`, row `删除`, and the name search | Editing, removing, sorting, and searching this list stay out of this file |

The studied document loads a script to toggle the rows. That script stays out of the response. The caret is a CSS triangle. It is not an image file and it is not an inline image.

## 3. The departments page

The page is `src/OpenRbac/templates/depts.vue`, inside the shell. One department is `src/OpenRbac/templates/dept-node.vue`. That component draws the department and then its children. The content root is `dept-page`. Every skin paints that root from `/apex.css`.

The five columns, in order, are `dept_id`, `parent_id`, `dept_name`, `ancestors`, and `status`. They are the list columns from `requirement-rbac-departments`. The header is `div.dept-head`. Each department is `div.dept-row` inside `div.dept-node`. The same five cells repeat on every row. `dept_name` is the cell that holds the caret and the name.

The tree is nested. A parent holds its children in `div.dept-children`. The seed order inside Group is Engineering, then Platform under Engineering, then Operations. That is `dept-fold-100`, then `dept-fold-101`, then `dept-fold-103`, then `dept-fold-102`.

A department with a child has `dept-branch`. A department with no child has `dept-leaf`. The depth class is `dept-depth-0` through `dept-depth-6`. A deeper department uses `dept-depth-6`. The component always emits the checkbox, the caret label, and `.dept-children`. An empty `.dept-children` is still present. `v-if` cannot test a dotted path, so the template does not choose the leaf with `v-if`.

Each department has a checkbox `input.dept-fold` with `id="dept-fold-"` plus that `dept_id`. The checkbox is checked. The caret is `label.dept-caret` and its `for` is that id. The checkbox sits immediately before `div.dept-row`, and `.dept-children` sits immediately after that row.

The toolbar control is `label.dept-btn-fold` with the text `Expand/Collapse`. Its `for` is `dept-fold-all`. The checkbox `input#dept-fold-all.dept-fold-all` is unchecked, and it is the previous sibling of `div.dept-table`. Neither control is a field of the add form.

Contracting a parent hides `.dept-children` of that parent. The children stay in the HTML. Expanding that parent shows them again. `Expand/Collapse` checks `dept-fold-all`, which hides every `.dept-children` and points every caret to the right. Activating it again unchecks `dept-fold-all`. A branch whose own checkbox is still checked shows its children, and its caret points down. A branch the reader already unchecked stays contracted.

The add form stays the form in `requirement-rbac-departments`. This file does not add edit, remove, or save sort.

| Piece | Measurement |
|-------|-------------|
| Row and header | One grid. The five columns share that grid |
| Caret slot | 16 by 16, inline before the name |
| Expanded caret | A downward triangle. Left and right borders are 5px and transparent. The top border is 6px and `#333` |
| Contracted caret | A rightward triangle. Top and bottom borders are 5px and transparent. The left border is 6px and `#333` |
| Name indent | 18px times the depth number in `dept-depth-N` |
| Leaf caret | `display: none` |
| Hidden checkbox | A 1 by 1 box at opacity 0. The label is the control the reader activates |

The sample is the top of the seed tree. Platform follows inside Engineering, and Operations follows Engineering under Group.

```html
<div class="dept-page">
  <label for="dept-fold-all" class="dept-btn-fold">Expand/Collapse</label>
  <input id="dept-fold-all" class="dept-fold-all" type="checkbox">
  <div class="dept-table">
    <div class="dept-head">
      <span>dept_id</span><span>parent_id</span><span>dept_name</span><span>ancestors</span><span>status</span>
    </div>
    <div class="dept-tree">
      <div class="dept-node dept-branch dept-depth-0">
        <input id="dept-fold-100" class="dept-fold" type="checkbox" checked>
        <div class="dept-row">
          <span>100</span><span>0</span>
          <span class="dept-name"><label class="dept-caret" for="dept-fold-100"></label>Group</span>
          <span>0</span><span>0</span>
        </div>
        <div class="dept-children">
          <div class="dept-node dept-branch dept-depth-1">
            <input id="dept-fold-101" class="dept-fold" type="checkbox" checked>
            <div class="dept-row">
              <span>101</span><span>100</span>
              <span class="dept-name"><label class="dept-caret" for="dept-fold-101"></label>Engineering</span>
              <span>0,100</span><span>0</span>
            </div>
            <div class="dept-children"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

Every theme links `/apex.css` and `/themes/<name>.css`. The markup is the Apex shell (`requirement-html-theme`).

## 4. Normative rules

1. **Destination.** Department Management **MUST** be `GET /depts`. The template **MUST** be `depts.vue` inside the shell. `dept-node.vue` **MUST** draw one department and then its children. The product **MUST NOT** add a department-admin page at `/system/dept`.
2. **Menu.** An account with `system:dept:list` **MUST** see label `Departments` and href `/depts` in the Access group. An account without that permission **MUST NOT** receive this page.
3. **Tree.** The page **MUST** show every department from `requirement-rbac-departments` as the nested tree in section 3. The five column labels **MUST** appear in that order. A child **MUST** be inside its parent's `.dept-children`. The seed page **MUST** contain `dept-fold-100`, then `dept-fold-101`, then `dept-fold-103`, then `dept-fold-102`.
4. **One parent.** A branch **MUST** include `input.dept-fold` checked, with `id="dept-fold-"` plus the department id, immediately before `div.dept-row`. `label.dept-caret` **MUST** use that id. `.dept-children` **MUST** follow the row. Unchecking that box **MUST** hide that `.dept-children`. Checking it **MUST** show that `.dept-children` when `dept-fold-all` is unchecked. The caret **MUST** point down while the branch is expanded and to the right while it is contracted.
5. **Every parent.** `label.dept-btn-fold` **MUST** read `Expand/Collapse` and **MUST** target `dept-fold-all`. That checkbox **MUST** start unchecked and **MUST** be the previous sibling of `div.dept-table`. While it is checked, every `.dept-children` **MUST** be hidden and every caret **MUST** point to the right. Unchecking it **MUST** show each branch whose own `dept-fold` is checked.
6. **Leaf.** A department with no child **MUST** carry `dept-leaf`. `.dept-leaf .dept-caret` **MUST** be hidden. The node **MUST** still be in the tree.
7. **Whole list.** Contracting a branch **MUST NOT** remove a department from the HTML. The page **MUST NOT** drop a row because of data scope.
8. **Add.** The add form **MUST** stay the form required by `requirement-rbac-departments`. The fold checkboxes **MUST NOT** be fields of that form. Edit, remove, and save sort **MUST NOT** be added by this file.
9. **Skin.** The page **MUST** use `Settings.theme()`. Every skin **MUST** show the same tree, the same column labels, and the same `Expand/Collapse` control. The rules in section 3 **MUST** live in `/apex.css`. The caret **MUST** be a CSS border. `/apex.css` **MUST NOT** use a `data:` image for it.
10. **Plain page.** The response **MUST NOT** contain an `<iframe`, a `<script` tag, or a `<style` block. It **MUST NOT** load a script to expand or contract the tree. The users organization tree **MUST** stay the diagram in section 5 of `requirement-html-element-plus`.

## 5. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | An admin `/depts` page contains `dept-page`, `dept-table`, `dept-branch`, `dept-leaf`, `dept-caret`, `Expand/Collapse`, `id="dept-fold-all"`, and `id="dept-fold-100"`. `dept-fold-100` precedes `dept-fold-101`, which precedes `dept-fold-103`, which precedes `dept-fold-102`. The checkbox `dept-fold-100` is checked |
| AC-2 | `/apex.css` contains `.dept-fold:not(:checked) + .dept-row + .dept-children`, `.dept-fold-all:checked ~ .dept-table .dept-children`, `.dept-leaf .dept-caret`, and `.dept-depth-2 .dept-name` |
| AC-3 | The departments HTML contains no `<iframe`, no `<script`, and no `<style` |
| AC-4 | The add form is absent when the account lacks `system:dept:add`. `dept-fold-all` is not an input of `action="/depts/add"` |
| AC-5 | An Apex `/depts` page contains `dept-branch`, `Expand/Collapse`, and `dept-fold-103` before `dept-fold-102`, and it does not link `/element-plus.css` |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Department Management | The OpenRbac page `GET /depts` |
| Studied page | The RuoYi department list whose title is `部门管理` |
| Expand | The children of a parent are shown. The caret points down |
| Contract | The children of a parent are hidden. The caret points to the right. The children stay in the HTML |
| Expand/Collapse | The toolbar label for `dept-fold-all`. It expands every open branch, or contracts every branch |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | The department list expands and contracts. The studied control is `展开/折叠` |
| 2026-10-16 | Active 1.0.1 | Every skin paints the department tree from `/apex.css` |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
