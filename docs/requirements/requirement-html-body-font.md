**file**: docs/requirements/requirement-html-body-font.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-html-body-font`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the font size of the document body. The size name is small. The length is 13px. That is the Element Plus small step. Text that does not name its own size inherits 13px. A heading, a tag, or a control that already names a size keeps that size.

The size lives in `/apex.css`. The skins are `requirement-html-theme`. The page template does not carry a style block (`requirement-python-html-template`).

### 1.1 Human-facing

**In one sentence:** Open any page and the ordinary text is the small size, 13px.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person reading a page | the sign-in form, or a list after sign-in |
| The other role | The document body | the `<body>` in `templates/document.vue` |
| Not this file | Which skin is chosen, and which button is shown | `requirement-html-theme`, `requirement-rbac` |

| Includes | Excludes |
|----------|----------|
| `font-size: 13px` on the document `body` in `/apex.css` | A script, an inline style, or a `<style>` block that sets the size |
| The name small for that 13px step | A theme sheet that replaces the body size |
| Inherited text at 13px | Forcing 13px onto a heading or a control that already names its own size |

| Surface | What you open | What for |
|---------|---------------|----------|
| `open-rbac serve` | the local site | every HTML page |
| `src/OpenRbac/element_plus/apex.css` | the layout stylesheet | the `body` rule |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open the site | Ordinary text is 13px. A title that already sets 16px or 18px stays that size. The page does not run a script to shrink the type. | `open-rbac serve` |

## 2. Core Rules / Requirements (Mandatory)

1. **Body.** The document `body` **MUST** set `font-size: 13px`. That declaration **MUST** be in `/apex.css`.
2. **Small.** 13px **MUST** be the small size. The body **MUST NOT** use 14px, 16px, or the browser default in place of 13px.
3. **One sheet.** `/apex.css` **MUST** contain `font-size: 13px` on `body`. A theme sheet under `/themes/` **MUST NOT** replace that size.
4. **Inheritance.** A descendant that does not set `font-size` **MUST** inherit 13px. A rule that already sets `font-size` on a heading, a tag, a table cell, or a control **MUST** stay. This file **MUST NOT** replace those lengths.
5. **No blanket.** The size **MUST NOT** be applied with `!important` on `*`, on `html`, or on every element. The selector for this rule **MUST** be `body`.
6. **No script.** The size **MUST NOT** come from a `<script` tag, an inline `style` attribute on `<body>`, or a `<style>` block in a template. `templates/document.vue` **MUST** keep a plain `<body>`.

### 2.1 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| Document | `src/OpenRbac/templates/document.vue`. The element is `<body>`. It has no `style` attribute |
| Layout sheet | `src/OpenRbac/element_plus/apex.css`. The `body` rule sets `font-size: 13px` |
| Required declaration | `font-size: 13px` inside the `body` rule of `/apex.css` |
| Pages | Sign-in and every signed-in page use that one `<body>` |

Allowed shape, on the existing `body` rule in `/apex.css`:

```css
body {
  font-size: 13px;
}
```

The other properties already on that rule stay.

### 2.2 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 1 – Caution:** A missing body size leaves the page at the browser default. The rule names 13px before a later edit picks another step.
- **CIAO Principle 2 – Intentional:** The need is ordinary text at the small size. The purpose is one `body` declaration of 13px in `/apex.css`.
- **CIAO Principle 4 – Over-protect:** The size stays on `body`. It is not forced onto every element, and it is not set from a script.
- **CIAO Principle 5 – SSOT:** This file owns the document body size. `requirement-html-theme` owns which color sheet loads. `requirement-html-element-plus` owns the component classes.

## Under command line for normal user only

This requirement encodes no install, no detect, and no privilege. The pages are read in the browser of this login. This file does not wrap `sudo`, `apt`, or a package installer, and it does not create a dedicated system user.

**This requirement:** the document body is 13px in the stylesheet. Nothing in this file raises privilege.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Treat a body rule with no `font-size`, and a body rule of 16px, as the wrong size, even when a table cell nearby is already 13px.
- **Intentional:** 13px is written on `body` so a later edit does not inherit the browser default.
- **Anti-fragile:** Every skin inherits the same body length from `/apex.css`.
- **Over-protect:** A universal `* { font-size: 13px !important }` stays forbidden so titles keep the sizes they already name.
- **Principle 21:** The portable rule is a document body at the small size. The stylesheet path is an Implementation Note for this product.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Leave the `body` rule in `/apex.css` without `font-size`, or set that rule to `16px`.
- Set the document `body` to `14px` or to the browser default.
- Let a theme sheet replace the body size.
- Apply `font-size: 13px` with `!important` on `*`, on `html`, or on every element.
- Set the size from a `<script` tag, from an inline style on `<body>`, or from a `<style>` block in a template.
- Cite an agent procedure file as the behavioral authority in product source. Product source cites this requirement.

## 5. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-html-theme.md` | Which stylesheet the page loads |
| `docs/requirements/requirement-html-element-plus.md` | The component classes |
| `docs/requirements/requirement-web-interface.md` | The HTML response and the style policy |
| `docs/requirements/requirement-python-html-template.md` | `templates/document.vue` and the ban on a style block |
| `src/OpenRbac/element_plus/apex.css` | The `body` rule |
| `src/OpenRbac/templates/document.vue` | The `<body>` element |

## 6. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | The `body` rule in `src/OpenRbac/element_plus/apex.css` contains `font-size: 13px` |
| AC-2 | That `body` rule does not contain `font-size: 16px` |
| AC-3 | `src/OpenRbac/templates/document.vue` contains `<body>` and does not set a `style` attribute on that element |
| AC-4 | `/apex.css` does not set `font-size: 13px !important` on `*` |

## Terminologies

### Small font size

**Definition:** The small font size is 13px. The document `body` in `/apex.css` uses that length. Text with no font size of its own inherits it. A heading or a control that names another length keeps that length.

**Human daily-life explanation:** Small font size is the everyday reading size on the page, a little smaller than a book’s normal print. Titles that were printed larger stay larger. The page does not shrink every word to the same size.

**Daily-life example:** A form label and a table cell that do not name a size show at 13px. A page title that already says 18px stays 18px.

## 7. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-15 | Active 1.0.0 | The document body uses the small font size, 13px, on both skins |
| 2026-10-16 | Active 1.0.1 | The 13px body size lives in `/apex.css`. A theme sheet does not replace it |

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
