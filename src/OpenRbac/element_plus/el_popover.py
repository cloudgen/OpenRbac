# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElPopover.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElPopover:
    """A small inline panel."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElPopover")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A small inline panel."""

        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        return '<div class="el-popover"{mark}>{inner}</div>'.format(mark=engine.mark(call), inner=inner)

