# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElButton.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElButton:
    """A button. type and size add the modifier classes."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElButton")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A button. type and size add the modifier classes."""

        props = call["props"]
        classes = ["btn"]
        kind = props.get("type") or ""
        if kind:
            classes.append("btn-" + kind)
        else:
            classes.append("btn-default")
        size = props.get("size") or ""
        if size == "large":
            classes.append("btn-lg")
        elif size == "small":
            classes.append("btn-sm")
        elif size:
            classes.append("btn-" + size)
        if props.get("class"):
            classes.append(props["class"])
        native = props.get("native-type") or "submit"
        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        return (
            '<button class="{classes}" type="{native}"{mark}><span>{inner}</span></button>'
        ).format(
            classes=engine.escape(" ".join(classes)),
            native=engine.escape(native),
            mark=engine.mark(call),
            inner=inner,
        )

