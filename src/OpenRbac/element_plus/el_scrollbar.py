# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElScrollbar.
# requirement-html-javascript — the signed-in sidebar does not use this wrap.
# requirement-python-oop — one component class.
# This class does not read layout and does not write a height.
# =============================================================================
from __future__ import annotations


class ElScrollbar:
    """A scroll wrap. The signed-in sidebar does not use this class."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElScrollbar")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A scroll wrap. Size stays in the stylesheet."""

        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        return (
            '<div class="el-scrollbar"{mark}>'
            '<div class="el-scrollbar__wrap"><div class="el-scrollbar__view">{inner}</div></div>'
            "</div>"
        ).format(mark=engine.mark(call), inner=inner)

