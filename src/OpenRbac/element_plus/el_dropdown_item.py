# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElDropdownItem.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElDropdownItem:
    """One account menu row."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElDropdownItem")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: One account menu row."""

        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        root = "nav-item"
        return '<li class="{root}"{mark}>{inner}</li>'.format(
            root=root,
            mark=engine.mark(call),
            inner=inner,
        )

