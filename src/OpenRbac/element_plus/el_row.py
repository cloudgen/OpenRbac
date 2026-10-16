# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElRow.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElRow:
    """A form grid row."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElRow")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A form grid row."""

        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        return '<div class="el-row"{mark}>{inner}</div>'.format(mark=engine.mark(call), inner=inner)

