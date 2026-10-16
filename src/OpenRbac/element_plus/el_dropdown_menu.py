# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElDropdownMenu.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElDropdownMenu:
    """The account menu list."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElDropdownMenu")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: The account menu list."""

        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        root = "nav"
        return '<ul class="{root}"{mark}>{inner}</ul>'.format(
            root=root,
            mark=engine.mark(call),
            inner=inner,
        )

