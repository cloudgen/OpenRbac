# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElDropdown.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElDropdown:
    """The account menu."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElDropdown")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: The account menu."""

        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        root = "navbar-nav"
        return '<div class="{root}"{mark}>{inner}</div>'.format(
            root=root,
            mark=engine.mark(call),
            inner=inner,
        )

