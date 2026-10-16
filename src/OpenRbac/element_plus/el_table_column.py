# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElTableColumn.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElTableColumn:
    """One column. el-table reads it as a child."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElTableColumn")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: One column. el-table reads it as a child."""

        prop = call["binds"].get("prop", call["props"].get("prop", ""))
        label = call["binds"].get("label", call["props"].get("label", prop))
        header_nodes = call["slots"].get("header", [])
        if header_nodes:
            shown = engine.render_nodes(header_nodes, ctx)
        else:
            shown = engine.escape(label)
        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        prop_attr = engine.attr("data-prop", prop) if prop != "" else ""
        return '<div class="el-table-column"{prop}{mark}>{label}{inner}</div>'.format(
            prop=prop_attr,
            mark=engine.mark(call),
            label=shown,
            inner=inner,
        )

