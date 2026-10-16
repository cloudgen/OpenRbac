# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElTable.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElTable:
    """A list. Each el-table-column is one column."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElTable")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A list. Each el-table-column is one column."""

        data = call["binds"].get("data", [])
        if not isinstance(data, (list, tuple)):
            data = []
        columns = []
        for node in call["slots"].get("default", []):
            if node.get("kind") != "element" or node.get("tag") != "el-table-column":
                continue
            test = engine.read_attr(node, "v-if")
            if test is not None and not engine.test_value(test, ctx):
                continue
            prepared = engine.prepare(node, ctx, False)
            prop = prepared["binds"].get("prop", prepared["props"].get("prop", ""))
            label = prepared["binds"].get("label", prepared["props"].get("label", prop))
            columns.append((
                prop,
                label,
                prepared["slots"].get("default", []),
                prepared["slots"].get("header", []),
            ))
        head_class = ""
        cell_class = ""
        row_class = ""
        heads = []
        for prop, label, _slot, header_nodes in columns:
            prop_attr = engine.attr("data-prop", prop) if prop != "" else ""
            if header_nodes:
                # The header slot is the column title. The check-all box uses it.
                shown = engine.render_nodes(header_nodes, ctx)
            else:
                shown = engine.escape(label)
            heads.append(
                "<th{klass}{prop}>{label}</th>".format(
                    klass=self._cell_class(head_class, shown),
                    prop=prop_attr,
                    label=shown,
                )
            )
        rows = []
        if len(data) == 0:
            span = max(len(columns), 1)
            rows.append(
                "<tr{row}><td{cell} colspan=\"{span}\">(none)</td></tr>".format(
                    row=row_class,
                    cell=cell_class,
                    span=span,
                )
            )
        for index, row in enumerate(data):
            if not isinstance(row, dict):
                row = {}
            child = dict(ctx)
            child["row"] = row
            child["index"] = index
            # A boolean on the row is a v-if name inside that cell.
            # requirement-html-role-management — role 1 omits row actions.
            for key, value in row.items():
                if (
                    type(value) is bool
                    and isinstance(key, str)
                    and key.isidentifier()
                    and key not in child
                ):
                    child[key] = value
            cells = []
            for prop, _label, slot_nodes, _header in columns:
                if slot_nodes:
                    cell = engine.render_nodes(slot_nodes, child)
                else:
                    value = row.get(prop, "") if prop else ""
                    if value is None:
                        value = ""
                    cell = engine.escape(value)
                cells.append(
                    "<td{0}>{1}</td>".format(self._cell_class(cell_class, cell), cell)
                )
            rows.append("<tr{0}>{1}</tr>".format(row_class, "".join(cells)))
        return (
            '<div class="card"{mark}><div class="card-body table-responsive p-0">'
            '<table class="table table-bordered table-striped">'
            "<thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table>"
            "</div></div>"
        ).format(mark=engine.mark(call), heads="".join(heads), rows="".join(rows))

    def _cell_class(self, klass, html):
        """Add table-check-col when the cell holds the checkbox."""
        if "table-check" not in html:
            return klass
        if klass == "":
            return ' class="table-check-col"'
        return klass[:-1] + ' table-check-col"'

