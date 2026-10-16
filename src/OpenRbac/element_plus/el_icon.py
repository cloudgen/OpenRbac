# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElIcon.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElIcon:
    """An icon slot."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElIcon")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: An icon slot."""

        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        return '<i class="el-icon"{mark}>{inner}</i>'.format(mark=engine.mark(call), inner=inner)

