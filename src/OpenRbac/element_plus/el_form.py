# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElForm.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElForm:
    """A form. method and action are the posted form."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElForm")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A form. method and action are the posted form."""

        props = call["props"]
        method = props.get("method") or "post"
        action = props.get("action") or ""
        enctype = props.get("enctype") or ""
        enctype_attr = engine.attr("enctype", enctype) if enctype else ""
        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        form_class = "form-horizontal"
        return (
            '<form class="{form_class}" method="{method}" action="{action}"{enctype}{mark}>{inner}</form>'
        ).format(
            form_class=form_class,
            method=engine.escape(method),
            action=engine.escape(action),
            enctype=enctype_attr,
            mark=engine.mark(call),
            inner=inner,
        )

