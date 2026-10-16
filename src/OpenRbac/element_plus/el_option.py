# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElOption.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElOption:
    """One choice inside el-select."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElOption")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: One choice inside el-select."""

        if "value" in call["binds"]:
            value = call["binds"]["value"]
        elif "value" in call["props"]:
            value = call["props"]["value"]
        elif "label" in call["binds"]:
            value = call["binds"]["label"]
        else:
            value = call["props"].get("label", "")
        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        if not inner:
            label = call["binds"].get("label", call["props"].get("label", value))
            inner = engine.escape(label)
        selected = ""
        current = ctx.get("_select_value", None)
        if current is not None and str(current) == str(value):
            selected = " selected"
        return '<option class="el-option" value="{value}"{selected}{mark}>{inner}</option>'.format(
            value=engine.escape(value),
            selected=selected,
            mark=engine.mark(call),
            inner=inner,
        )

