**file**: docs/requirements/requirement-html-element-plus.md
**Status**: Active (Version 1.0.12)
**Area**: python
**Key**: `requirement-html-element-plus`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the HTML component library. A template tag such as `<el-button>` keeps that name and renders the Apex shell classes for that component. The tag names follow Element Plus 2.14.3, the version pinned by [RuoYi-FastAPI](https://github.com/insistence/RuoYi-FastAPI) `ruoyi-fastapi-frontend/vue3/web/package.json`. The tag is resolved by `requirement-python-html-template`. The library emits HTML. The layout is `/apex.css`. It does not ship the Element Plus JavaScript.

The components below are the ones those Vue pages use for the OpenRbac destinations in the template requirement. A component the record file does not feed stays available and unused.

### 1.1 Human-facing

**In one sentence:** A button, a form, a table, and a dialog on the page use the Apex shell classes. The tag names stay.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The reader of a users page | an `el-table` of accounts |
| The other role | One component class | `ElButton` |
| Not this file | Which rows the table contains | `requirement-rbac-users` |

| Includes | Excludes |
|----------|----------|
| The `el-*` tags listed in section 2 | `element-plus` JavaScript, Vue, Pinia, and Axios |
| The Apex shell classes those tags emit | A stylesheet loaded from a CDN |
| A dialog form that posts the existing field names | A second permission check inside the component |
| A department tree and a job-title dropdown that open without a script | A script that opens them, and a `:has()` rule |

| Surface | What you open | What for |
|---------|---------------|----------|
| Component | `src/OpenRbac/element_plus/el_button.py` | The `el-button` HTML |
| Stylesheet | `/apex.css` and `/themes/<name>.css` | The shell classes and the colors |
| Page | `/users` | Those components filled by the template |

## 2. Components

Each component is one class in `src/OpenRbac/element_plus/`. The module name is the tag with hyphens turned into underscores. The class name is the tag in Pascal case, so `el-button` is class `ElButton` in `el_button.py`.

| Tag | Rendered root class | Used on the reference pages for |
|-----|---------------------|----------------------------------|
| `el-button` | `btn` | toolbar and dialog actions |
| `el-form` | `form-horizontal` | sign-in, query, and dialog forms |
| `el-form-item` | `form-group` | one label and one control |
| `el-input` | `form-control` | text and password fields |
| `el-input-number` | `form-control` | a whole-number field |
| `el-select` | `form-control` | a choice such as status or role |
| `el-option` | `el-option` | one choice inside `el-select` |
| `el-radio` | `form-check` | one radio |
| `el-radio-group` | `form-group` | status, menu type, notice type |
| `el-checkbox` | `form-check` | a menu id on role grant |
| `el-switch` | `el-switch` | an on/off status. On posts `0`. Off posts `1` |
| `el-table` | `table table-bordered table-striped` | every list |
| `el-table-column` | `el-table-column` | one column |
| `el-dialog` | `card card-primary card-outline` | add and edit |
| `el-row` | `el-row` | form grid |
| `el-col` | `el-col` | one grid cell |
| `el-tree` | `list-unstyled` | role menu grant |
| `el-tree-select` | `form-control` | a parent department or parent menu |
| `el-tag` | `el-tag` | a short status label |
| `el-tooltip` | `el-tooltip` | the action title on an icon button |
| `el-pagination` | `text-muted` | the list footer |
| `el-menu` | `nav nav-pills nav-sidebar` | the sidebar |
| `el-menu-item` | `nav-item` | one sidebar destination |
| `el-sub-menu` | `nav-item` | a sidebar group |
| `el-breadcrumb` | `breadcrumb` | the navbar path |
| `el-breadcrumb-item` | `breadcrumb-item` | one path step |
| `el-dropdown` | `navbar-nav` | the account menu |
| `el-dropdown-menu` | `nav` | the account menu list |
| `el-dropdown-item` | `nav-item` | sign out |
| `el-scrollbar` | `el-scrollbar` | a scroll wrap whose size stays in the stylesheet. The signed-in sidebar does not use this tag |
| `el-icon` | `el-icon` | an icon slot |
| `el-popover` | `el-popover` | a small menu-icon chooser |
| `el-date-picker` | `el-date-picker` | a date field when a record action accepts one |

`type="primary"` on `el-button` **MUST** add `btn-primary`. `size="large"` **MUST** add `btn-lg`. A button with no type **MUST** add `btn-default`. `size="small"` **MUST** add `btn-sm`.

The sidebar, navbar, and `app-main` regions are templates in `requirement-python-html-template`. They are composed from the tags above.

## 3. Normative rules

1. **DOM.** A component **MUST** emit the Apex shell classes in `requirement-html-theme`. A button is `btn`. A field is `form-control`. A table is `table`. A dialog is `card`. A menu item is `nav-item`. The tag name stays `el-button` and the other tags in section 2.
2. **Stylesheet.** A page **MUST** link `/apex.css` and the theme sheet in `requirement-html-theme`. It **MUST NOT** link `/element-plus.css` or load a stylesheet from a CDN. The link **MUST** be allowed by the style policy in `requirement-web-interface`.
3. **No runtime.** The library **MUST NOT** import `vue`, `element-plus` JavaScript, `pinia`, `vue-router`, or `axios`. A rendered component **MUST NOT** contain a `<script` tag. The document script `/table-check.js` is `requirement-html-javascript`. It is not a component.
4. **Values.** Text and attribute values **MUST** be escaped before they are placed in the HTML. `v-model` **MUST** become the form `name` and `value` defined by `requirement-python-html-template`.
5. **Dialog form.** An add or edit dialog **MUST** be an `el-dialog` containing an `el-form`. The form **MUST** post to the path the record requirement names, and **MUST** include the hidden `csrf` field from `requirement-web-interface`.
6. **Permission.** A component **MUST** be omitted when `WebApp` does not pass it. The component **MUST NOT** keep its own allow-list.
7. **Pagination.** `el-pagination` **MUST** show the current list bounds. The maximum number of user rows remains the limit in `requirement-rbac-users`.
8. **One class.** Each Python file in `src/OpenRbac/element_plus/` **MUST** define one component class. The package **MUST** export those classes for `HtmlTemplate`. `table-check.js` is the check-all script in `requirement-html-javascript`. It is not a component class. `ElTable` **MUST** add class `table-check-col` on a `th` or `td` whose HTML contains `table-check`. `/apex.css` **MUST** center that column.
9. **Scroll wrap.** `el-scrollbar` **MUST NOT** be the signed-in sidebar. The shell **MUST NOT** place the menu inside this tag. The component **MUST NOT** read `scrollHeight`, `offsetHeight`, `clientHeight`, or `getBoundingClientRect`, and **MUST NOT** write `height`, `min-height`, or an inline style from that read. The sidebar scrollport is `requirement-html-javascript`. Changing a scrollable wrap dynamically is forbidden.
10. **RuoYi tree.** A diagram of parents and children **MUST** use the nested list in section 5. It **MUST NOT** be a flat list indented only by `margin-left`. It **MUST NOT** load a zTree file, jQuery, or a script. The lines **MUST** live in `/apex.css`. An icon **MUST** be a separate file unless a requirement names an inline image. `el-tree` remains the role-grant control in section 2. It is not this diagram. The department list at `GET /depts` is `requirement-html-department-management`. That list expands and contracts. It is not this diagram.
11. **User status switch.** The users `Status` column and the edit-form status field **MUST** be the `el-switch` in section 6. On **MUST** be status `0` and the word `Enabled`. Off **MUST** be status `1` and the word `Disabled`. The control **MUST** be a track and a knob. It **MUST NOT** be a `select` of `0` and `1`, and it **MUST NOT** be only those two words. It **MUST NOT** use a script. A table switch that may post **MUST** be a `button` whose `form` attribute names a form outside the `GET` form that wraps the table. That form **MUST** post to `POST /users/status`. User 1, and an account without `system:user:edit`, **MUST** see the same track and knob and **MUST NOT** submit. The edit field **MUST** be a checkbox of value `0` followed by a hidden input of value `1`. Checked posts `0`. Unchecked posts `1`. The search choices stay the words `All`, `Enabled`, and `Disabled`. `span.user-switch` is the tree in section 5. It is not this control. `/apex.css` **MUST** paint the track and the knob.
12. **Edit choices.** The users edit dialog **MUST** choose one department and any number of job titles without a script. The dialog **MUST** be wrapped in `user-edit-float`. `/apex.css` **MUST** set that class to `position: fixed` so the dialog floats over the users page. The department control **MUST** open a floating panel. That panel **MUST** contain the nested list in section 5, and each row **MUST** be one radio named `dept_id`. The job-title control **MUST** be a dropdown of checkboxes named `job_title_id`. A closed dropdown **MUST** show a tag for each checked title. Opening either control **MUST** use a checkbox that has no `name`, so the open state is not posted. The panel and the dropdown **MUST** use a `:checked` sibling rule. They **MUST NOT** use `:has()`. They **MUST NOT** use a script. The floating panel **MUST** omit expand and collapse, and that panel **MUST** be drawn expanded. The department page at `GET /depts` keeps the expand and collapse in `requirement-html-department-management`. The field names, the validation sentences, and which rows are offered stay on section 6 of `requirement-html-user-management` and on `requirement-rbac-users`. `span.user-switch` stays the organization tree. It is not the department picker.
13. **Body size.** The document `body` size is `requirement-html-body-font`. This file **MUST NOT** set that size.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | The users page contains `class="table table-bordered table-striped"` and `class="btn` for an allowed action |
| AC-2 | When the add form is on the users page, it is `card card-primary card-outline` containing `form-horizontal`, and the account field posts `user_name` |
| AC-3 | The operator users page has no add form |
| AC-4 | The stylesheet response is same-origin and the HTML contains no `cdn` Element Plus URL |
| AC-5 | The rendered components contain no `<script` tag |
| AC-6 | Role grant uses `el-tree` or `el-checkbox` for menu ids and posts `menu_id` |
| AC-7 | The shell template contains no `el-scrollbar` |
| AC-8 | The users organization tree contains `class="user-tree"` and `class="user-switch"`, and Group's row contains Engineering |
| AC-9 | The users page contains `class="el-switch"` and `class="el-switch__core"`. An allowed account's switch posts to `/users/status` |
| AC-10 | When the users edit dialog is shown, the page contains `Choose a department`, `class="user-edit-float"`, `name="dept_id"`, and `name="job_title_id"`. The floating panel's tree uses `user-node-branch` or `user-node-leaf`. The page's only script tag is `<script src="/table-check.js"></script>`. `/apex.css` contains `user-edit-float`, `dept-float`, and `job-tag` |

## 5. RuoYi tree

The studied organization tree is a zTree list: one row is a switch, an icon, and a name, and the children sit in a list inside that row. OpenRbac draws that shape with HTML and `/apex.css`. The users page is the worked example. `templates/users.vue` opens the list. `templates/user-node.vue` draws one department and then its children. The department management list is not this diagram.

| Class | When |
|-------|------|
| `user-node-branch` | The node has a child. The switch is a minus box. The icon is a folder |
| `user-node-leaf` | The node has no child. The switch is an elbow. The icon is a circle |
| `is-first` | The first sibling |
| `is-last` | The last sibling. The vertical line stops at the switch |
| `is-root` | The only node at depth 0. No line comes from above |
| `is-current` | The chosen node. The icon is white |

| Piece | Measurement |
|-------|-------------|
| Switch | 21 by 21 |
| Child list | `padding-left: 18px` |
| Vertical line | 1px wide at `left: 10px`, dotted `#666`, 1px on and 1px off |
| Last sibling | That line is `height: 11px` |
| Several roots | The first root's line starts at `top: 10px` |
| Minus box | 13 by 13 at `left: 4px` and `top: 4px`, a 1px `#333` border, a white fill, and an 8 by 1 bar at `left: 7px` and `top: 10px` |
| Leaf elbow | A dotted line from `left: 10px`, `top: 10px`, 11px wide |
| Icon | A 16 by 16 file |
| Row | `line-height: 21px` and `font-size: 12px` |

An empty child list is still a `ul`. The stylesheet hides `ul:empty`. A `v-if` cannot test a dotted name, so the template does not hide that list with `v-if`.

```html
<ul class="user-tree">
  <li class="user-depth-0 user-node-branch is-first is-last is-root">
    <span class="user-switch"></span>
    <a class="user-tree-link" href="/users?dept=100"><span class="user-node-icon"></span>Group</a>
    <ul>
      <li class="user-depth-1 user-node-branch is-first">
        <span class="user-switch"></span>
        <a class="user-tree-link" href="/users?dept=101"><span class="user-node-icon"></span>Engineering</a>
        <ul>
          <li class="user-depth-2 user-node-leaf is-first is-last">
            <span class="user-switch"></span>
            <a class="user-tree-link" href="/users?dept=103"><span class="user-node-icon"></span>Platform</a>
            <ul></ul>
          </li>
        </ul>
      </li>
      <li class="user-depth-1 user-node-leaf is-last">
        <span class="user-switch"></span>
        <a class="user-tree-link" href="/users?dept=102"><span class="user-node-icon"></span>Operations</a>
        <ul></ul>
      </li>
    </ul>
  </li>
</ul>
```

Group is the root, so it has the box and no line from above. Engineering is not last, so its line runs through Platform. Platform and Operations are last siblings, so each line stops at the elbow.

The users edit dialog places this same list in a floating panel. That panel is section 6 of `requirement-html-user-management`. The dialog that holds the panel uses `user-edit-float` and floats over the users page. The row there is a radio named `dept_id`. The organization row stays a link. The measurements in this section stay the measurements of that panel. The panel does not invent a second geometry. The department page at `GET /depts` keeps its own expand and collapse. That page is `requirement-html-department-management`. It is not this panel.

## 6. User status switch

An account status is a track with a knob. The knob sits on the right when the account is on, and on the left when it is off. The word beside the track is `Enabled` or `Disabled`. The users page is the worked example. `0` is on. `1` is off.

| Piece | Measurement |
|-------|-------------|
| Track | 40 by 20. Off is `#dcdfe6`. On is `#409eff` |
| Knob | 16 by 16, white. `left: 1px` when off. `left: calc(100% - 17px)` when on |
| Locked | Opacity `.6`. The control does not submit |

The table sits inside a `GET` form, so the switch cannot be a nested form. The button names the status form with the `form` attribute. That form follows the `GET` form. Clicking the button posts the other status and keeps the search fields.

```html
<button type="submit" class="el-switch is-checked" form="user-status-2" aria-pressed="true">
  <span class="el-switch__core"><span class="el-switch__action"></span></span>
  <span class="el-switch__label">Enabled</span>
</button>
<form id="user-status-2" method="post" action="/users/status">
  <input type="hidden" name="csrf" value="token">
  <input type="hidden" name="user_id" value="2">
  <input type="hidden" name="status" value="1">
</form>
```

User 1 stays on. An account that cannot edit also sees the track and does not get a button:

```html
<span class="el-switch is-checked is-disabled" aria-disabled="true">
  <span class="el-switch__core"><span class="el-switch__action"></span></span>
  <span class="el-switch__label">Enabled</span>
</span>
```

The edit form uses a checkbox so the knob moves before Save. The checkbox comes first. A checked box posts `0`. An unchecked box posts only the hidden `1`.

```html
<label class="el-switch is-checked">
  <input class="el-switch__input" type="checkbox" name="status" value="0" checked>
  <span class="el-switch__core"><span class="el-switch__action"></span></span>
  <span class="el-switch__label">Enabled</span>
</label>
<input type="hidden" name="status" value="1">
```

The search field stays a choice of `All`, `Enabled`, and `Disabled`. `span.user-switch` on the organization tree is section 5. It is not this control. The roles page uses this same track and knob. Its form, its locked role, and its path are `requirement-html-role-management`. This section stays the users example.

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Component | One `el-*` class that returns HTML |
| Root class | The Element Plus class on the outer element, such as `el-button` |
| Stylesheet | The Element Plus 2.14.3 CSS served by this host |
| RuoYi tree | The nested list in section 5. A switch, an icon, and a dotted line. The department page is not this diagram. The users edit dialog reuses this list as radios |
| User status switch | The `el-switch` in section 6. On is `0`. Off is `1`. It is not `span.user-switch`. The roles switch is `requirement-html-role-management` |

### UI infinite reflow

**Definition:** A UI infinite reflow is a layout cycle: the browser measures a box, writes a size that depends on that measurement, and measures again, and the sizes never settle. The usual shape is a cyclic percentage. A scroll wrap is `height: 100%` inside a parent whose height is the wrap’s own content (`min-height` only, or `height: auto`). The same cycle is started by a function that reads `scrollHeight`, `offsetHeight`, `clientHeight`, or `getBoundingClientRect` and writes `height`, `min-height`, or `style` back onto that wrap or its parent. The layout thread keeps re-entering. The page, and often the whole desktop, stops answering. Pain PP-A-31.

**Human daily-life explanation:** A UI infinite reflow is a tailor who measures the cloth, cuts the table to match the cloth, then measures the cloth again because the table changed. The tape never stops. The room fills with the sound of the tape and nobody can open the door.

**Daily-life example:** A side column says “I am as tall as my parent,” and the parent says “I am as tall as the side column.” The painter measures forever. The screen locks.

### UI sidebar

**Definition:** ui-sidebar is the production UI label whose English UI term is Sidebar. The actual UI function is the side column that lists destinations beside the page body. The column’s height is a definite viewport length in the stylesheet (`100vh` or a stated length). Overflow scrolls on that column. The column is not a child whose `height: 100%` is resolved against a parent that sizes itself from the column.

**Human daily-life explanation:** A ui-sidebar is the narrow list on the side of the page that says where you can go. The list has a fixed height, like a door frame. Extra names scroll inside the frame. The frame does not grow because the list grew.

**Daily-life example:** A restaurant menu is clipped to the left of the table. You slide the menu. The table does not get taller each time you slide it.

### UI scrollbar

**Definition:** ui-scrollbar is the production UI label whose English UI term is Scrollbar. The actual UI function is the control that shows more content than fits and lets the reader move through it. The wrap’s size is only in the stylesheet. Changing a scrollable wrap dynamically is forbidden. A function must not read `scrollHeight`, `offsetHeight`, `clientHeight`, or `getBoundingClientRect` and write `height`, `min-height`, or inline style onto that wrap or its parent. That write is a UI infinite reflow.

**Human daily-life explanation:** A ui-scrollbar is the slider that shows there is more to read. The window size is printed on the plan. Nobody comes back with a tape measure and rebuilds the window because the paper was long. Rebuilding the window from the paper is how the room locks.

**Daily-life example:** A long grocery list sits in a fixed window with a slider. A helper who stretches the window to the length of the list, then measures again, never finishes. That helper must not be hired.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.0.0 | HTML components for the Element Plus tags on the OpenRbac pages |
| 2026-10-14 | Active 1.0.1 | `el-scrollbar` is not the signed-in sidebar. The scrollport is `requirement-html-javascript` |
| 2026-10-14 | Active 1.0.2 | Element Plus classes and `/element-plus.css` are the vue3 theme. adminlte is `requirement-html-theme` |
| 2026-10-14 | Active 1.0.3 | The users add dialog is present when the add form is on the page |
| 2026-10-14 | Active 1.0.4 | A RuoYi tree is the nested list in section 5. The users departments are the example |
| 2026-10-14 | Active 1.0.5 | User status is the on/off switch in section 6. On posts 0. Off posts 1 |
| 2026-10-14 | Active 1.0.6 | The department list expands and contracts. It is not the section 5 diagram |
| 2026-10-14 | Active 1.0.7 | The users edit dialog opens a section 5 tree for one department and a checkbox dropdown for job titles. That panel stays expanded |
| 2026-10-14 | Active 1.0.8 | The roles status switch stays on `requirement-html-role-management`. Section 6 remains the users example |
| 2026-10-14 | Active 1.0.9 | The users edit dialog uses `user-edit-float` and floats over the users page |
| 2026-10-15 | Active 1.0.10 | `--el-font-size-small` stays 13px. The document body size is `requirement-html-body-font` |
| 2026-10-16 | Active 1.0.11 | A checkbox cell uses `table-check-col`. The document may load `/table-check.js`. A component fragment still has no script |
| 2026-10-16 | Active 1.0.12 | The tags emit Apex shell classes. Pages link `/apex.css` and the theme sheet |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
