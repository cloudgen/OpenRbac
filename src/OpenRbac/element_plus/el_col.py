# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElCol.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElCol:
    """One grid cell. span sets the column width class."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElCol")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: One grid cell. span sets the column width class."""

        span = call["binds"].get("span", call["props"].get("span", "24"))
        classes = "el-col el-col-{0}".format(span)
        if call["props"].get("class"):
            classes = classes + " " + call["props"]["class"]
        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        return '<div class="{classes}"{mark}>{inner}</div>'.format(
            classes=engine.escape(classes),
            mark=engine.mark(call),
            inner=inner,
        )

