# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElRadio.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElRadio:
    """One radio. The value attribute is the posted value."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElRadio")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: One radio. The value attribute is the posted value."""

        if "value" in call["binds"]:
            value = call["binds"]["value"]
        elif "value" in call["props"] and call["props"].get("value") != "":
            value = call["props"]["value"]
        elif "label" in call["binds"]:
            value = call["binds"]["label"]
        elif call["props"].get("label"):
            value = call["props"]["label"]
        else:
            value = ""
        name = call["model"] or call["props"].get("name") or ctx.get("_radio_name") or ""
        checked = ""
        if "_radio_value" in ctx and str(ctx.get("_radio_value")) == str(value):
            checked = " checked"
        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        return (
            '<div class="form-check"{mark}>'
            '<label class="form-check-label">'
            '<input class="form-check-input" type="radio"{name} value="{value}"{checked}>'
            " {inner}</label></div>"
        ).format(
            mark=engine.mark(call),
            name=engine.attr("name", name) if name else "",
            value=engine.escape(value),
            checked=checked,
            inner=inner,
        )

