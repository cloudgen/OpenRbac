# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElDialog.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElDialog:
    """A dialog panel. The default slot is the body."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElDialog")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A dialog panel. The default slot is the body."""

        title = call["binds"].get("title", call["props"].get("title", ""))
        body = engine.render_nodes(call["slots"].get("default", []), ctx)
        footer_nodes = call["slots"].get("footer", [])
        footer = ""
        if footer_nodes:
            footer = '<div class="card-footer">{0}</div>'.format(
                engine.render_nodes(footer_nodes, ctx)
            )
        return (
            '<div class="card card-primary card-outline"{mark}>'
            '<div class="card-header"><h3 class="card-title">{title}</h3></div>'
            '<div class="card-body">{body}</div>'
            "{footer}</div>"
        ).format(
            mark=engine.mark(call),
            title=engine.escape(title),
            body=body,
            footer=footer,
        )

