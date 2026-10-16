# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElTag.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElTag:
    """A short status label."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElTag")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A short status label."""

        classes = ["el-tag"]
        kind = call["binds"].get("type") or call["props"].get("type") or ""
        if kind:
            classes.append("el-tag--" + kind)
        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        return '<span class="{classes}"{mark}>{inner}</span>'.format(
            classes=engine.escape(" ".join(classes)),
            mark=engine.mark(call),
            inner=inner,
        )

