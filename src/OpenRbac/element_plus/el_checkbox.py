# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElCheckbox.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElCheckbox:
    """A checkbox. The name and value are the posted field."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElCheckbox")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A checkbox. The name and value are the posted field."""

        name = call["model"] or call["props"].get("name") or call["binds"].get("name") or ""
        if "value" in call["binds"]:
            value = call["binds"]["value"]
        elif "value" in call["props"] and call["props"].get("value") != "":
            value = call["props"]["value"]
        else:
            value = "on"
        checked = ""
        if call["model"] is not None:
            current = call["model_value"]
            if isinstance(current, (list, tuple)):
                if str(value) in [str(item) for item in current]:
                    checked = " checked"
            elif current is True or str(current) == str(value):
                checked = " checked"
        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        return (
            '<div class="form-check"{mark}>'
            '<label class="form-check-label">'
            '<input class="form-check-input" type="checkbox"{name} value="{value}"{checked}>'
            " {inner}</label></div>"
        ).format(
            mark=engine.mark(call),
            name=engine.attr("name", name) if name else "",
            value=engine.escape(value),
            checked=checked,
            inner=inner,
        )

