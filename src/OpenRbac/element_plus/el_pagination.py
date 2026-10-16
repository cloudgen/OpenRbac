# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElPagination.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElPagination:
    """The current list bounds."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElPagination")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: The current list bounds."""

        raw_total = call["binds"].get("total", call["props"].get("total", 0))
        try:
            total = int(raw_total)
        except (TypeError, ValueError):
            total = 0
        if total < 0:
            total = 0
        if total == 0:
            bounds = "Showing 0 of 0"
        else:
            bounds = "Showing 1-{0} of {0}".format(total)
        limit = call["binds"].get("limit", call["props"].get("limit", None))
        limit_html = ""
        if limit not in (None, ""):
            limit_html = " Limit {0}".format(engine.escape(limit))
        return (
            '<p class="text-muted"{mark}>{bounds}{limit}</p>'
        ).format(mark=engine.mark(call), bounds=engine.escape(bounds), limit=limit_html)

