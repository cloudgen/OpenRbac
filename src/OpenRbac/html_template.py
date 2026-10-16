# =============================================================================
# Vue-shaped HTML templates rendered on the server.
# requirement-python-html-template — class HtmlTemplate. No script block, no style
# block, no copied client runtime, no JSON API for a browser application.
# A document that shows a table checkbox also loads /table-check.js.
# requirement-python-project-structure — templates/ and element_plus/ only.
# requirement-html-element-plus — component tags. The markup is the Apex shell.
# requirement-html-theme — one shell. The stored theme picks the color sheet.
# requirement-python-oop — class HtmlTemplate and HtmlTemplateError.
# =============================================================================
from __future__ import annotations

import html
import re
from pathlib import Path

from .settings import Settings

from .element_plus.el_breadcrumb import ElBreadcrumb
from .element_plus.el_breadcrumb_item import ElBreadcrumbItem
from .element_plus.el_button import ElButton
from .element_plus.el_checkbox import ElCheckbox
from .element_plus.el_col import ElCol
from .element_plus.el_date_picker import ElDatePicker
from .element_plus.el_dialog import ElDialog
from .element_plus.el_dropdown import ElDropdown
from .element_plus.el_dropdown_item import ElDropdownItem
from .element_plus.el_dropdown_menu import ElDropdownMenu
from .element_plus.el_form import ElForm
from .element_plus.el_form_item import ElFormItem
from .element_plus.el_icon import ElIcon
from .element_plus.el_input import ElInput
from .element_plus.el_input_number import ElInputNumber
from .element_plus.el_menu import ElMenu
from .element_plus.el_menu_item import ElMenuItem
from .element_plus.el_option import ElOption
from .element_plus.el_pagination import ElPagination
from .element_plus.el_popover import ElPopover
from .element_plus.el_radio import ElRadio
from .element_plus.el_radio_group import ElRadioGroup
from .element_plus.el_row import ElRow
from .element_plus.el_scrollbar import ElScrollbar
from .element_plus.el_select import ElSelect
from .element_plus.el_sub_menu import ElSubMenu
from .element_plus.el_switch import ElSwitch
from .element_plus.el_table import ElTable
from .element_plus.el_table_column import ElTableColumn
from .element_plus.el_tag import ElTag
from .element_plus.el_tooltip import ElTooltip
from .element_plus.el_tree import ElTree
from .element_plus.el_tree_select import ElTreeSelect


class HtmlTemplateError(Exception):
    """The template cannot be rendered."""

    def __init__(self, message, nxt, logger=None):
        super().__init__(message)
        self.logger = logger
        self.nxt = nxt
        if logger is not None:
            logger.log_message("instantiated", component="HtmlTemplateError")


class HtmlTemplate:
    """Render one Vue 3 template to HTML.

    A template file cannot contain a script block. A document that shows a
    table checkbox loads /table-check.js. A fragment does not.
    """

    _NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    _PATH = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*$")
    _FOR_PAIR = re.compile(
        r"^\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*,\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)\s+in\s+"
        r"([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)\s*$"
    )
    _FOR_ONE = re.compile(
        r"^([A-Za-z_][A-Za-z0-9_]*)\s+in\s+"
        r"([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)\s*$"
    )
    _STRUCTURAL = ("v-if", "v-else-if", "v-else", "v-show", "v-for")
    _BOOLEAN_ATTRS = {"checked", "selected", "disabled", "readonly"}
    _VOID = {
        "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "source", "track", "wbr",
    }
    _HTML = {
        "a", "abbr", "address", "article", "aside", "b", "blockquote", "br",
        "button", "caption", "code", "col", "colgroup", "dd", "div", "dl",
        "dt", "em", "fieldset", "figcaption", "figure", "footer", "form",
        "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hr", "html",
        "i", "img", "input", "label", "legend", "li", "link", "main", "mark",
        "meta", "nav", "ol", "option", "p", "pre", "section", "select",
        "small", "span", "strong", "sub", "sup", "table", "tbody", "td",
        "textarea", "tfoot", "th", "thead", "title", "tr", "ul", "details",
        "summary", "time", "s", "u", "kbd", "body",
    }
    _CHECK_SCRIPT = '<script src="/table-check.js"></script>'

    def __init__(self, logger=None, template_dir=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="HtmlTemplate")
        if template_dir is None:
            self.template_dir = Path(__file__).resolve().parent / "templates"
        else:
            self.template_dir = Path(template_dir)
        self._cache = {}
        self.button = ElButton(logger=logger)
        self.form = ElForm(logger=logger)
        self.form_item = ElFormItem(logger=logger)
        self.input = ElInput(logger=logger)
        self.input_number = ElInputNumber(logger=logger)
        self.select = ElSelect(logger=logger)
        self.option = ElOption(logger=logger)
        self.radio = ElRadio(logger=logger)
        self.radio_group = ElRadioGroup(logger=logger)
        self.checkbox = ElCheckbox(logger=logger)
        self.switch = ElSwitch(logger=logger)
        self.table = ElTable(logger=logger)
        self.table_column = ElTableColumn(logger=logger)
        self.dialog = ElDialog(logger=logger)
        self.row = ElRow(logger=logger)
        self.col = ElCol(logger=logger)
        self.tree = ElTree(logger=logger)
        self.tree_select = ElTreeSelect(logger=logger)
        self.tag = ElTag(logger=logger)
        self.tooltip = ElTooltip(logger=logger)
        self.pagination = ElPagination(logger=logger)
        self.menu = ElMenu(logger=logger)
        self.menu_item = ElMenuItem(logger=logger)
        self.sub_menu = ElSubMenu(logger=logger)
        self.breadcrumb = ElBreadcrumb(logger=logger)
        self.breadcrumb_item = ElBreadcrumbItem(logger=logger)
        self.dropdown = ElDropdown(logger=logger)
        self.dropdown_menu = ElDropdownMenu(logger=logger)
        self.dropdown_item = ElDropdownItem(logger=logger)
        self.scrollbar = ElScrollbar(logger=logger)
        self.icon = ElIcon(logger=logger)
        self.popover = ElPopover(logger=logger)
        self.date_picker = ElDatePicker(logger=logger)
        self.components = {
            "el-button": self.button,
            "el-form": self.form,
            "el-form-item": self.form_item,
            "el-input": self.input,
            "el-input-number": self.input_number,
            "el-select": self.select,
            "el-option": self.option,
            "el-radio": self.radio,
            "el-radio-group": self.radio_group,
            "el-checkbox": self.checkbox,
            "el-switch": self.switch,
            "el-table": self.table,
            "el-table-column": self.table_column,
            "el-dialog": self.dialog,
            "el-row": self.row,
            "el-col": self.col,
            "el-tree": self.tree,
            "el-tree-select": self.tree_select,
            "el-tag": self.tag,
            "el-tooltip": self.tooltip,
            "el-pagination": self.pagination,
            "el-menu": self.menu,
            "el-menu-item": self.menu_item,
            "el-sub-menu": self.sub_menu,
            "el-breadcrumb": self.breadcrumb,
            "el-breadcrumb-item": self.breadcrumb_item,
            "el-dropdown": self.dropdown,
            "el-dropdown-menu": self.dropdown_menu,
            "el-dropdown-item": self.dropdown_item,
            "el-scrollbar": self.scrollbar,
            "el-icon": self.icon,
            "el-popover": self.popover,
            "el-date-picker": self.date_picker,
        }

    def render(self, name, values) -> str:
        """General Purpose: Render one template file to an HTML fragment."""
        return self.render_nodes(self._load(name), self._values(values))

    def render_source(self, source, values) -> str:
        """General Purpose: Render one template string with the same rules as a file."""
        return self.render_nodes(self._parse(source), self._values(values))

    def render_document(self, page, values) -> str:
        """General Purpose: A document whose body is the named page template."""
        ctx = self._values(values)
        ctx["_slots"] = {"default": self._load(page)}
        inner = self.render_nodes(self._load("document"), ctx)
        if 'class="table-check' in inner:
            inner = inner.replace("</body>", self._CHECK_SCRIPT + "</body>", 1)
        return "<!DOCTYPE html>" + inner

    def render_nodes(self, nodes, ctx) -> str:
        """General Purpose: Render a list of template nodes."""
        parts = []
        index = 0
        count = len(nodes)
        while index < count:
            node = nodes[index]
            if node["kind"] != "element":
                parts.append(self.render_one(node, ctx))
                index += 1
                continue
            if self.has_attr(node, "v-if") or self.has_attr(node, "v-else-if") or self.has_attr(node, "v-else"):
                html_text, index = self._branches(nodes, index, ctx)
                parts.append(html_text)
                continue
            parts.append(self.render_one(node, ctx))
            index += 1
        return "".join(parts)

    def render_one(self, node, ctx) -> str:
        """General Purpose: Render one text node, interpolation, or element."""
        if node["kind"] == "text":
            return self.escape(node["text"])
        if node["kind"] == "interp":
            return self.escape(self.lookup(node["expr"], ctx))
        if self.has_attr(node, "v-for"):
            return self._repeat(node, ctx)
        hidden = False
        show = self.read_attr(node, "v-show")
        if show is not None:
            hidden = not self.test_value(show, ctx)
            node = self._strip(node, ("v-show",))
        tag = node["tag"]
        if tag == "template":
            rendered = self.render_nodes(node["children"], ctx)
            if hidden:
                return '<div hidden style="display:none">{0}</div>'.format(rendered)
            return rendered
        if tag == "slot":
            return self._fill_slot(node, ctx)
        if tag in self.components:
            return self.components[tag].render(self.prepare(node, ctx, hidden), ctx, self)
        if self._template_file(tag).is_file():
            return self._render_template(tag, node, ctx, hidden)
        if tag in self._HTML:
            return self._render_html(node, ctx, hidden)
        self._raise(
            "Unknown tag {0}.".format(tag),
            "use an HTML tag or an Element Plus component",
        )

    def prepare(self, node, ctx, hidden) -> dict:
        """General Purpose: Props, binds, v-model, and slots for one component."""
        props = {}
        binds = {}
        model = None
        for key, raw in node["attrs"]:
            if key in self._STRUCTURAL:
                continue
            if key == "v-html":
                self._raise("v-html is not rendered.", "use {{ }} for text")
            if key == "v-model":
                model = (raw or "").strip()
                if not self._NAME.match(model):
                    self._raise("v-model must name one field.", 'use v-model="field"')
                continue
            if key.startswith("v-bind:"):
                binds[key.split(":", 1)[1]] = self.lookup(raw, ctx)
                continue
            if key.startswith(":"):
                binds[key[1:]] = self.lookup(raw, ctx)
                continue
            if key.startswith("v-on:") or key.startswith("@") or key.startswith("v-slot:") or key.startswith("#"):
                continue
            if key in ("v-on", "v-slot"):
                continue
            if key == "v-bind":
                self._raise("v-bind needs an attribute name.", "use :name")
            if key.startswith("v-"):
                self._raise(
                    "Unknown directive {0}.".format(key),
                    "remove {0}".format(key),
                )
            props[key] = raw
        model_value = None
        if model is not None:
            model_value = self.lookup(model, ctx)
        return {
            "props": props,
            "binds": binds,
            "model": model,
            "model_value": model_value,
            "slots": self.slots_of(node),
            "hidden": hidden,
        }

    def slots_of(self, node) -> dict:
        """General Purpose: Default and named slots on one element."""
        slots = {"default": []}
        for child in node["children"]:
            name = self.slot_name(child)
            if name:
                slots.setdefault(name, []).append(child)
            else:
                slots["default"].append(child)
        return slots

    def slot_name(self, node):
        """General Purpose: The slot name on a template tag, or None."""
        if node.get("kind") != "element" or node.get("tag") != "template":
            return None
        for key, _value in node["attrs"]:
            if key == "v-slot":
                return "default"
            if key.startswith("v-slot:"):
                return key.split(":", 1)[1] or "default"
            if key.startswith("#"):
                return key[1:] or "default"
        return None

    def read_attr(self, node, name):
        """General Purpose: The raw attribute value, or None when it is absent."""
        for key, value in node["attrs"]:
            if key == name:
                return value
        return None

    def has_attr(self, node, name) -> bool:
        """General Purpose: Whether the element carries that attribute."""
        return any(key == name for key, _value in node["attrs"])

    def lookup(self, expr, ctx):
        """General Purpose: One name, or a dotted path, from the value dictionary."""
        text = (expr or "").strip()
        if not self._PATH.match(text):
            self._raise(
                "Unknown expression {0}.".format(expr),
                "use a name from the value dictionary",
            )
        parts = text.split(".")
        if parts[0] not in ctx:
            self._raise(
                "Missing value {0}.".format(parts[0]),
                "pass {0} in the value dictionary".format(parts[0]),
            )
        value = ctx[parts[0]]
        walked = parts[0]
        for part in parts[1:]:
            walked = "{0}.{1}".format(walked, part)
            if isinstance(value, dict) and part in value:
                value = value[part]
                continue
            self._raise(
                "Missing value {0}.".format(walked),
                "pass {0} in the value dictionary".format(walked),
            )
        return value

    def skin(self, ctx) -> str:
        """General Purpose: The markup family. Every theme uses the Apex shell."""
        return "apex"

    def test_value(self, expr, ctx) -> bool:
        """General Purpose: A branch test. The test is a name, or not plus a name."""
        text = (expr or "").strip()
        negative = False
        if text.startswith("not "):
            negative = True
            text = text[4:].strip()
        if not self._NAME.match(text):
            self._raise(
                "Unknown expression {0}.".format(expr),
                "use a name or not plus a name",
            )
        if text not in ctx:
            self._raise(
                "Missing value {0}.".format(text),
                "pass {0} in the value dictionary".format(text),
            )
        result = bool(ctx[text])
        if negative:
            return not result
        return result

    def escape(self, value) -> str:
        """General Purpose: Escape text for an HTML text node or attribute."""
        if value is None:
            return ""
        return html.escape(str(value), quote=True)

    def attr(self, name, value) -> str:
        """General Purpose: One escaped HTML attribute, including the leading space."""
        return ' {0}="{1}"'.format(name, self.escape(value))

    def _bound_flag(self, value) -> bool:
        """A bound checked, selected, disabled, or readonly is present only when true."""
        if value is True:
            return True
        if value is False or value is None:
            return False
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return value != 0
        return str(value).strip().lower() not in ("", "0", "false", "none", "no")

    def mark(self, call) -> str:
        """General Purpose: The hidden state for v-show, or an empty string."""
        if call.get("hidden"):
            return ' hidden style="display:none"'
        return ""

    def _values(self, values) -> dict:
        if not isinstance(values, dict):
            self._raise(
                "The template values must be a dictionary.",
                "pass a dictionary of names",
            )
        ctx = dict(values)
        theme = str(ctx.get("theme") or "apex").strip().lower().replace(" ", "-")
        if theme not in Settings.THEMES:
            theme = "apex"
        ctx["theme"] = theme
        ctx["theme_href"] = "/themes/{0}.css".format(theme)
        return ctx

    def _load(self, name):
        if name not in self._cache:
            path = self.template_dir / "{0}.vue".format(name)
            if not path.is_file():
                self._raise(
                    "Missing template {0}.".format(name),
                    "add templates/{0}.vue".format(name),
                )
            self._cache[name] = self._parse(path.read_text(encoding="utf-8"))
        return self._cache[name]

    def _parse(self, source):
        text = source[1:] if source.startswith("\ufeff") else source
        lowered = text.lower()
        if "<script" in lowered:
            self._raise("A script block cannot be rendered.", "remove the script block")
        if "<style" in lowered:
            self._raise("A style block cannot be rendered.", "remove the style block")
        nodes, index = self._parse_nodes(text, 0, None)
        if index < len(text) and text[index:].strip():
            self._fail_at(text, index, "Unexpected text after the template.")
        if len(nodes) != 1 or nodes[0].get("tag") != "template":
            self._raise(
                "A template needs one template root.",
                "wrap the page in one template element",
            )
        inner = nodes[0]["children"]
        self._check_tags(inner)
        return inner

    def _check_tags(self, nodes):
        for node in nodes:
            if node["kind"] != "element":
                continue
            tag = node["tag"]
            known = (
                tag in ("template", "slot")
                or tag in self.components
                or tag in self._HTML
                or self._template_file(tag).is_file()
            )
            if not known:
                self._raise(
                    "Unknown tag {0}.".format(tag),
                    "use an HTML tag or an Element Plus component",
                )
            self._check_directives(node)
            self._check_tags(node["children"])

    def _check_directives(self, node):
        allowed = {"v-if", "v-else-if", "v-else", "v-show", "v-for", "v-model", "v-on", "v-slot", "v-bind"}
        for key, _value in node["attrs"]:
            if key == "v-html":
                self._raise("v-html is not rendered.", "use {{ }} for text")
            if key.startswith("v-"):
                head = key.split(":", 1)[0]
                if head not in allowed:
                    self._raise(
                        "Unknown directive {0}.".format(key),
                        "remove {0}".format(key),
                    )

    def _parse_nodes(self, text, index, stop):
        nodes = []
        length = len(text)
        while index < length:
            if text.startswith("</", index):
                if stop and self._end_is(text, index, stop):
                    return nodes, index
                self._fail_at(text, index, "Unexpected end tag.")
            if text.startswith("<!--", index):
                end = text.find("-->", index + 4)
                if end < 0:
                    self._fail_at(text, index, "An HTML comment is not closed.")
                index = end + 3
                continue
            if text.startswith("{{", index):
                end = text.find("}}", index + 2)
                if end < 0:
                    self._fail_at(text, index, "An interpolation is not closed.")
                nodes.append({"kind": "interp", "expr": text[index + 2:end].strip()})
                index = end + 2
                continue
            if text.startswith("<", index):
                node, index = self._parse_element(text, index)
                nodes.append(node)
                continue
            end = index
            while end < length and not text.startswith("<", end) and not text.startswith("{{", end):
                end += 1
            raw = text[index:end]
            if raw.strip():
                nodes.append({"kind": "text", "text": raw})
            index = end
        if stop:
            self._fail_at(text, index, "Missing end tag {0}.".format(stop))
        return nodes, index

    def _parse_element(self, text, index):
        cursor = index + 1
        if cursor >= len(text) or not text[cursor].isalpha():
            self._fail_at(text, index, "A tag name is missing.")
        start = cursor
        while cursor < len(text) and (text[cursor].isalnum() or text[cursor] in "-_"):
            cursor += 1
        tag = text[start:cursor].lower()
        attrs = []
        while cursor < len(text):
            while cursor < len(text) and text[cursor] in " \t\r\n":
                cursor += 1
            if cursor >= len(text):
                self._fail_at(text, index, "A tag is not closed.")
            if text.startswith("/>", cursor):
                return {"kind": "element", "tag": tag, "attrs": attrs, "children": []}, cursor + 2
            if text[cursor] == ">":
                cursor += 1
                node = {"kind": "element", "tag": tag, "attrs": attrs, "children": []}
                if tag in self._VOID:
                    return node, cursor
                children, cursor = self._parse_nodes(text, cursor, tag)
                cursor = self._consume_end(text, cursor, tag)
                node["children"] = children
                return node, cursor
            name, value, cursor = self._parse_attr(text, cursor)
            attrs.append((name, value))
        self._fail_at(text, index, "A tag is not closed.")

    def _parse_attr(self, text, index):
        start = index
        while index < len(text) and text[index] not in " \t\r\n=/>":
            index += 1
        name = text[start:index]
        if not name:
            self._fail_at(text, index, "An attribute name is missing.")
        while index < len(text) and text[index] in " \t\r\n":
            index += 1
        if index >= len(text) or text[index] != "=":
            return name, "", index
        index += 1
        while index < len(text) and text[index] in " \t\r\n":
            index += 1
        if index >= len(text):
            self._fail_at(text, start, "An attribute value is missing.")
        if text[index] in "\"'":
            quote = text[index]
            index += 1
            end = text.find(quote, index)
            if end < 0:
                self._fail_at(text, start, "An attribute value is not closed.")
            return name, text[index:end], end + 1
        start_value = index
        while index < len(text) and text[index] not in " \t\r\n>":
            index += 1
        return name, text[start_value:index], index

    def _consume_end(self, text, index, tag):
        if not self._end_is(text, index, tag):
            self._fail_at(text, index, "Missing end tag {0}.".format(tag))
        cursor = index + 2
        while cursor < len(text) and text[cursor] in " \t\r\n":
            cursor += 1
        end = cursor
        while end < len(text) and text[end] not in " \t\r\n>":
            end += 1
        cursor = end
        while cursor < len(text) and text[cursor] in " \t\r\n":
            cursor += 1
        if cursor >= len(text) or text[cursor] != ">":
            self._fail_at(text, index, "An end tag is not closed.")
        return cursor + 1

    def _end_is(self, text, index, tag) -> bool:
        if not text.startswith("</", index):
            return False
        cursor = index + 2
        while cursor < len(text) and text[cursor] in " \t\r\n":
            cursor += 1
        end = cursor
        while end < len(text) and text[end] not in " \t\r\n>":
            end += 1
        return text[cursor:end].lower() == tag

    def _branches(self, nodes, index, ctx):
        start = index
        if not self.has_attr(nodes[index], "v-if"):
            self._raise("v-else needs a v-if.", "start the chain with v-if")
        chosen = ""
        taken = False
        while index < len(nodes):
            current = nodes[index]
            if current["kind"] != "element":
                break
            kind = None
            expr = None
            if self.has_attr(current, "v-if") and index == start:
                kind = "if"
                expr = self.read_attr(current, "v-if")
            elif self.has_attr(current, "v-else-if") and index != start:
                kind = "elif"
                expr = self.read_attr(current, "v-else-if")
            elif self.has_attr(current, "v-else") and index != start:
                kind = "else"
            else:
                break
            if not taken:
                take = kind == "else" or self.test_value(expr, ctx)
                if take:
                    chosen = self.render_one(
                        self._strip(current, ("v-if", "v-else-if", "v-else")),
                        ctx,
                    )
                    taken = True
            index += 1
            if kind == "else":
                break
        return chosen, index

    def _repeat(self, node, ctx) -> str:
        expr = self.read_attr(node, "v-for") or ""
        pair = self._FOR_PAIR.match(expr.strip())
        one = self._FOR_ONE.match(expr.strip())
        if pair:
            alias, index_name, list_name = pair.group(1), pair.group(2), pair.group(3)
        elif one:
            alias, index_name, list_name = one.group(1), "index", one.group(2)
        else:
            self._raise(
                "Unknown expression {0}.".format(expr),
                'use v-for="row in rows"',
            )
        data = self.lookup(list_name, ctx)
        if not isinstance(data, (list, tuple)):
            self._raise(
                "{0} must be a list.".format(list_name),
                "pass a list in the value dictionary",
            )
        bare = self._strip(node, ("v-for",))
        parts = []
        for number, item in enumerate(data):
            child = dict(ctx)
            child[alias] = item
            child[index_name] = number
            parts.append(self.render_one(bare, child))
        return "".join(parts)

    def _fill_slot(self, node, ctx) -> str:
        name = "default"
        for key, value in node["attrs"]:
            if key == "name" and value:
                name = value
        slots = ctx.get("_slots") or {}
        return self.render_nodes(slots.get(name, []), ctx)

    def _render_template(self, tag, node, ctx, hidden) -> str:
        child = dict(ctx)
        child["_slots"] = self.slots_of(node)
        rendered = self.render_nodes(self._load(tag), child)
        if hidden:
            return '<div hidden style="display:none">{0}</div>'.format(rendered)
        return rendered

    def _render_html(self, node, ctx, hidden) -> str:
        tag = node["tag"]
        attrs = []
        class_names = []
        model = None
        for key, raw in node["attrs"]:
            if key in self._STRUCTURAL:
                continue
            if key == "v-model":
                model = (raw or "").strip()
                continue
            if key.startswith(("v-on:", "@", "v-slot:", "#")) or key in ("v-on", "v-slot"):
                continue
            if key == "v-bind":
                self._raise("v-bind needs an attribute name.", "use :name")
            if key.startswith("v-bind:") or key.startswith(":"):
                aname = key.split(":", 1)[1] if key.startswith("v-bind:") else key[1:]
                value = self.lookup(raw, ctx)
                if aname == "class":
                    class_names.append("" if value is None else str(value))
                elif aname in self._BOOLEAN_ATTRS:
                    if self._bound_flag(value):
                        attrs.append((aname, None))
                else:
                    attrs.append((aname, value))
                continue
            if key.startswith("v-"):
                self._raise("Unknown directive {0}.".format(key), "remove {0}".format(key))
            if key == "class":
                class_names.append(raw)
                continue
            attrs.append((key, raw))
        if model is not None:
            if not self._NAME.match(model):
                self._raise("v-model must name one field.", 'use v-model="field"')
            model_value = self.lookup(model, ctx)
            names = {key for key, _value in attrs}
            if "name" not in names:
                attrs.append(("name", model))
            if tag == "textarea":
                pass
            elif tag in ("input", "select") and "value" not in names:
                kind = ""
                for key, value in attrs:
                    if key == "type":
                        kind = str(value)
                if kind in ("checkbox", "radio"):
                    current = "on"
                    for key, value in attrs:
                        if key == "value":
                            current = value
                    if str(model_value) == str(current):
                        attrs.append(("checked", None))
                else:
                    attrs.append(("value", "" if model_value is None else model_value))
        if hidden:
            self._hide(attrs)
        if class_names:
            attrs.insert(0, ("class", " ".join(part for part in class_names if part != "")))
        attr_html = "".join(
            " {0}".format(key) if value is None else self.attr(key, value)
            for key, value in attrs
        )
        if tag in self._VOID:
            return "<{0}{1}>".format(tag, attr_html)
        if tag == "textarea" and model is not None:
            inner = self.escape(model_value)
        else:
            inner = self.render_nodes(node["children"], ctx)
        return "<{0}{1}>{2}</{0}>".format(tag, attr_html, inner)

    def _hide(self, attrs):
        attrs.append(("hidden", None))
        for index, (key, value) in enumerate(attrs):
            if key == "style":
                attrs[index] = (key, "{0};display:none".format(value))
                return
        attrs.append(("style", "display:none"))

    def _strip(self, node, names):
        return {
            "kind": "element",
            "tag": node["tag"],
            "attrs": [(key, value) for key, value in node["attrs"] if key not in names],
            "children": node["children"],
        }

    def _template_file(self, tag) -> Path:
        return self.template_dir / "{0}.vue".format(tag)

    def _raise(self, message, nxt):
        raise HtmlTemplateError(message, nxt, logger=self.logger)

    def _fail_at(self, text, index, message):
        snippet = text[max(0, index - 24):index + 24].replace("\n", " ")
        self._raise("{0} Near: {1}".format(message, snippet), "fix the template")
