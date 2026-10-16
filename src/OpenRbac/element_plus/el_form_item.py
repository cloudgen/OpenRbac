# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElFormItem.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElFormItem:
    """One label and one control."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElFormItem")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: One label and one control."""

        label = call["binds"].get("label", call["props"].get("label", ""))
        root_class = "form-group"
        label_html = ""
        if label:
            label_html = "<label>{0}</label>".format(engine.escape(label))
        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        content_attr = ""
        return (
            '<div class="{root}"{mark}>{label}<div{content}>{inner}</div></div>'
        ).format(
            root=root_class,
            mark=engine.mark(call),
            label=label_html,
            content=content_attr,
            inner=inner,
        )

