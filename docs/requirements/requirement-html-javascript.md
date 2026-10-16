**file**: docs/requirements/requirement-html-javascript.md
**Status**: Active (Version 1.0.3)
**Area**: python
**Key**: `requirement-html-javascript`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the HTML and JavaScript layout law for pages this product serves. A scrollport has a definite height in the stylesheet. A function must not read a box and write that box’s size. That write, and a percentage height whose parent is sized by the same child, is a layout cycle: the browser measures, writes, and measures again, and the page stops answering. Changing a scrollable wrap dynamically is forbidden.

Without this file, a copied scroll component arrives raw: its stylesheet says `height: 100%` and its script sets the wrap height from the wrap’s own content. The signed-in sidebar is the place that copy was used.

### 1.1 Human-facing

**In one sentence:** The side list stays a fixed window, and nothing in the page measures that window and rebuilds it.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person reading the signed-in page | the side list of destinations |
| The other role | The browser layout | a column whose height is `100vh` |
| Not this file | Which destinations the account may open | `requirement-web-interface` |

| Includes | Excludes |
|----------|----------|
| A definite sidebar height and `overflow: auto` in the stylesheet | A wrap whose `height: 100%` depends on its own content |
| The ban on a function that reads layout and writes height | A script added so the menu looks finished |
| `/table-check.js`, which checks the row boxes in one table | An inline script, Vue, Element Plus JavaScript, jQuery, or a CDN script |
| The menu markup already in the HTML | Element Plus JavaScript, Vue, or a CDN script |

| Surface | What you open | What for |
|---------|---------------|----------|
| `open-rbac serve` | the local site | the signed-in pages |
| `src/OpenRbac/templates/shell.vue` | the shell | the side column |
| `src/OpenRbac/element_plus/apex.css` | the layout stylesheet | the sidebar height |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open the site and use the side list | Extra names scroll inside a column that already has a height. The column does not grow because the list grew, and no function comes back to set that height. | `open-rbac serve` |

## 2. Core Rules / Requirements (Mandatory)

1. **Scrollport.** The box that scrolls **MUST** have a definite used height in the stylesheet. A viewport length (`100vh`) or a stated length is definite. `min-height` alone is not.
2. **No cyclic percentage.** A child **MUST NOT** use `height: 100%` when the parent’s used height depends on that child (`height: auto` or `min-height` only).
3. **No measure-then-write.** A function **MUST NOT** read `scrollHeight`, `offsetHeight`, `clientHeight`, or `getBoundingClientRect` and write `height`, `min-height`, or an inline style onto that box or its parent.
4. **No resize loop.** A resize observer, an animation frame, a mutation callback, or a load handler **MUST NOT** assign the wrap’s height from its content.
5. **Dynamic wrap.** Changing a scrollable wrap dynamically is forbidden. The size lives in the stylesheet only.
6. **No script to finish the menu.** The active item **MUST** already be in the HTML. A script **MUST NOT** be added to mark the active item or to size the column.
7. **Side column.** The side column of destinations **MUST** be the scrollport. It **MUST NOT** be wrapped in a second scroll wrap whose height is a percentage of a content-sized parent.
8. **Check all.** A document that contains `class="table-check` **MUST** include `<script src="/table-check.js"></script>` once, immediately before `</body>`. That file **MUST** be `src/OpenRbac/element_plus/table-check.js`. The listener **MUST** serve `/table-check.js` as `text/javascript` from this host, and the package data **MUST** include it. When the header box in `thead` changes, the file **MUST** set every `tbody` checkbox with class `table-check` in that same table to the same checked state. When a row box changes, the header box **MUST** be checked only when every row box is checked, and **MUST** be indeterminate when some are checked. The header box **MUST NOT** have a name. The file **MUST NOT** read `scrollHeight`, `offsetHeight`, `clientHeight`, or `getBoundingClientRect`, and **MUST NOT** write `height`, `min-height`, or an inline style. A document with no table checkbox **MUST NOT** include a `<script` tag. The tag **MUST NOT** be inline. The file **MUST NOT** load Vue, Element Plus JavaScript, jQuery, Bootstrap JavaScript, or a script from another host. Checking the boxes **MUST NOT** delete many rows. Edit, Remove, and Change still use the first posted id.

### 2.1 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| Shell | `src/OpenRbac/templates/shell.vue` |
| Side column | `<aside class="main-sidebar">` on every theme |
| Menu | `<ui-menu>` is a direct child of that column. The shell **MUST NOT** contain `el-scrollbar` |
| Stylesheet | `src/OpenRbac/element_plus/apex.css` |
| Sidebar rule | `height: 100vh; overflow: auto; position: sticky; top: 0` on `.main-sidebar` |
| Component library | `el-scrollbar` may still render its root class for a caller that is not the shell. The shell is not that caller. The class **MUST NOT** read layout |
| Check-all script | `src/OpenRbac/element_plus/table-check.js`, served at `/table-check.js` |
| Script policy | `requirement-web-interface` sends `script-src 'self'` only. This file adds no other script |
| Proof | `tests/test_html_template.py` |

Allowed shape (the product stylesheet):

```css
.main-sidebar {
  height: 100vh;
  overflow: auto;
}
```

Forbidden shape (do not emit this, in a template, in Python, or in a script):

```javascript
function fit(wrap) {
  wrap.style.height = wrap.scrollHeight + "px";
}
```

The same ban covers `offsetHeight`, `clientHeight`, and `getBoundingClientRect`, and a write to `min-height` or to the parent.

### 2.2 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 1 – Caution:** A layout cycle locks the page. The rule fails closed before that function is written.
- **CIAO Principle 2 – Intentional:** The need is a copied scroll component. The purpose is a definite scrollport and a ban on measuring it to set its size.
- **CIAO Principle 4 – Over-protect:** Changing a scrollable wrap dynamically stays forbidden even when the first paint looks stable.
- **CIAO Principle 5 – SSOT:** This file owns the ban. `requirement-html-element-plus` owns the component tags. `requirement-web-interface` owns the headers and the nav permissions. `requirement-python-html-template` owns the template syntax.

## Under command line for normal user only

This requirement encodes no install, no detect, and no privilege. The pages are read in the browser of this login. This file does not wrap `sudo`, `apt`, or a package installer, and it does not create a dedicated system user.

**This requirement:** the side column is a stylesheet scrollport. Nothing in this file raises privilege.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Treat a `height: 100%` scroll wrap inside a content-sized parent as a cycle, even when the author meant only to hide overflow.
- **Intentional:** The sidebar height is written in the stylesheet so a later edit does not invent a fit function.
- **Anti-fragile:** The menu highlight is in the HTML. A missing script runtime does not require a resize function.
- **Over-protect:** The forbidden sample stays in this file so a later edit cannot call the same read-and-write “a small helper.”
- **Principle 21:** Portable bans are the core rules. The shell path and the `100vh` rule are Implementation Notes for this product.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Put the signed-in menu inside `el-scrollbar`, or inside any wrap whose height is a percentage of a content-sized parent.
- Add a function that reads `scrollHeight`, `offsetHeight`, `clientHeight`, or `getBoundingClientRect` and writes `height`, `min-height`, or inline style.
- Change a scrollable wrap’s size from a resize observer, an animation frame, a mutation callback, or a load handler.
- Add a `<script` tag, a broader `script-src`, or a client library so the menu or the column “looks finished.” `/table-check.js` is the one script, and it only checks row boxes.
- Replace `height: 100vh` on `.sidebar` or on `.main-sidebar` with `min-height` only, or with `height: auto`, and then size the column from its content.
- Treat this file’s forbidden sample as code to copy into the product.
- Cite an agent procedure file or a blank checklist as the behavioral authority in product source. Product source cites this requirement.

## 5. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-web-interface.md` | Headers, nav permissions, `script-src 'self'` |
| `docs/requirements/requirement-python-html-template.md` | Shell template and the renderer |
| `docs/requirements/requirement-html-element-plus.md` | `el-*` tags, including `el-scrollbar` when a caller is not the shell |
| `src/OpenRbac/templates/shell.vue` | The side column |
| `src/OpenRbac/element_plus/apex.css` | The `.main-sidebar` height |
| `docs/requirements/requirement-html-theme.md` | Which column the theme uses |
| `tests/test_html_template.py` | The proof |

## 6. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | No file under `src/OpenRbac/templates/` contains `el-scrollbar` |
| AC-2 | The `.main-sidebar` rule in `src/OpenRbac/element_plus/apex.css` sets `height: 100vh` and `overflow: auto` |
| AC-3 | Python and JavaScript under `src/OpenRbac/element_plus/` do not mention `scrollHeight`, `offsetHeight`, `clientHeight`, or `getBoundingClientRect` |
| AC-4 | A rendered shell fragment contains `main-sidebar` and `nav-sidebar`, contains no `el-scrollbar`, and contains no `<script` |
| AC-5 | The rendered menu item for the request path carries `aria-current="page"` |
| AC-6 | A document that shows a table checkbox contains `<script src="/table-check.js"></script>` once. `/table-check.js` sets each row box from the header box. A document with no table checkbox contains no `<script` tag |

## Terminologies

### UI infinite reflow

**Definition:** A UI infinite reflow is a layout cycle: the browser measures a box, writes a size that depends on that measurement, and measures again, and the sizes never settle. The usual shape is a cyclic percentage. A scroll wrap is `height: 100%` inside a parent whose height is the wrap’s own content (`min-height` only, or `height: auto`). The same cycle is started by a function that reads `scrollHeight`, `offsetHeight`, `clientHeight`, or `getBoundingClientRect` and writes `height`, `min-height`, or `style` back onto that wrap or its parent. The layout thread keeps re-entering. The page, and often the whole desktop, stops answering. Pain PP-A-31.

**Human daily-life explanation:** A UI infinite reflow is a tailor who measures the cloth, cuts the table to match the cloth, then measures the cloth again because the table changed. The tape never stops. The room fills with the sound of the tape and nobody can open the door.

**Daily-life example:** A side column says “I am as tall as my parent,” and the parent says “I am as tall as the side column.” The painter measures forever. The screen locks.

### UI sidebar

**Definition:** ui-sidebar is the production UI label whose English UI term is Sidebar. The actual UI function is the side column that lists destinations beside the page body. The column’s height is a definite viewport length in the stylesheet (`100vh` or a stated length). Overflow scrolls on that column. The column is not a child whose `height: 100%` is resolved against a parent that sizes itself from the column. Pain PP-A-31 when an agent wraps this column in a self-sized scroll wrap.

**Human daily-life explanation:** A ui-sidebar is the narrow list on the side of the page that says where you can go. The list has a fixed height, like a door frame. Extra names scroll inside the frame. The frame does not grow because the list grew.

**Daily-life example:** A restaurant menu is clipped to the left of the table. You slide the menu. The table does not get taller each time you slide it.

### UI scrollbar

**Definition:** ui-scrollbar is the production UI label whose English UI term is Scrollbar. The actual UI function is the control that shows more content than fits and lets the reader move through it. The wrap’s size is only in the stylesheet. Changing a scrollable wrap dynamically is forbidden. A function must not read `scrollHeight`, `offsetHeight`, `clientHeight`, or `getBoundingClientRect` and write `height`, `min-height`, or inline style onto that wrap or its parent. That write is a UI infinite reflow (PP-A-31).

**Human daily-life explanation:** A ui-scrollbar is the slider that shows there is more to read. The window size is printed on the plan. Nobody comes back with a tape measure and rebuilds the window because the paper was long. Rebuilding the window from the paper is how the room locks.

**Daily-life example:** A long grocery list sits in a fixed window with a slider. A helper who stretches the window to the length of the list, then measures again, never finishes. That helper must not be hired.

## 7. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-14 | Active 1.0.0 | Definite sidebar scrollport. A function must not resize a scroll wrap. |
| 2026-10-14 | Active 1.0.1 | The adminlte side column is `.main-sidebar` with the same `100vh` rule |
| 2026-10-16 | Active 1.0.2 | `/table-check.js` checks the row boxes in one table. It does not measure layout |
| 2026-10-16 | Active 1.0.3 | The scrollport is `.main-sidebar` in `/apex.css` on every skin |

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
