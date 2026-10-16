# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElBreadcrumb.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElBreadcrumb:
    """The navbar path."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElBreadcrumb")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: The navbar path."""

        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        return '<ol class="breadcrumb" aria-label="Breadcrumb"{mark}>{inner}</ol>'.format(
            mark=engine.mark(call),
            inner=inner,
        )

