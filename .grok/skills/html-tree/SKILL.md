---
name: html-tree
description: "Draw a nested HTML tree in the RuoYi zTree shape: a 21px switch, a minus box on a parent, an elbow on a leaf, and a dotted line that stops on the last sibling. Use when the user asks for the users organization tree, zTree lines, or a RuoYi tree, or when the user runs /html-tree. The department management list is a different control and expands and contracts."
---

# HTML tree

Draw a parent-and-child tree as nested HTML. The law, the measurements, and the worked example are section 5 of `docs/requirements/requirement-html-element-plus.md`. Read that section before writing markup or CSS. Do not invent a second geometry.

## Steps

1. Read section 5 of `docs/requirements/requirement-html-element-plus.md`.
2. Build a nested list. Each node is an `li` inside its parent `ul`. Children go in a `ul` inside that `li`.
3. On every row, emit `span.user-switch`, then the link, then `span.user-node-icon`, then the name.
4. Mark `user-node-branch` when the node has children, otherwise `user-node-leaf`. Mark `is-first` and `is-last` among siblings. Mark `is-root` only when depth 0 has one node.
5. Put the line rules in both `/openrbac.css` and `/adminlte.css`. Copy the measurements from section 5. Do not indent a flat list with `margin-left`.
6. Keep `templates/users.vue` and `templates/user-node.vue` as the shipped example. A new tree uses the same classes.

## Limits

- No `<script>`, no zTree file, no jQuery, and no Font Awesome.
- An icon is a separate same-origin file unless a requirement names an inline image.
- `el-tree` is the role-grant checkbox list. It is not this diagram.
- `v-if` cannot test a dotted path. Emit the child `ul` always. The stylesheet hides an empty `ul`.
- The department management list expands and contracts. Its law is `docs/requirements/requirement-html-department-management.md`. Do not draw that list with `user-switch`.
