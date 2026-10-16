# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElBreadcrumbItem.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElBreadcrumbItem:
    """One step in the navbar path."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElBreadcrumbItem")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: One step in the navbar path."""

        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        return '<li class="breadcrumb-item"{mark}>{inner}</li>'.format(
            mark=engine.mark(call),
            inner=inner,
        )

