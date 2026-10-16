# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElTooltip.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElTooltip:
    """A title on the wrapped control."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElTooltip")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A title on the wrapped control."""

        title = call["binds"].get("content", call["props"].get("content", ""))
        if title == "":
            title = call["binds"].get("title", call["props"].get("title", ""))
        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        return '<span class="el-tooltip"{title}{mark}>{inner}</span>'.format(
            title=engine.attr("title", title) if title != "" else "",
            mark=engine.mark(call),
            inner=inner,
        )

