# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElSelect.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElSelect:
    """A choice control that posts the selected option."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElSelect")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A choice control that posts the selected option."""

        name = call["model"] or call["props"].get("name") or call["binds"].get("name") or ""
        current = call["model_value"]
        if current is None and "value" in call["binds"]:
            current = call["binds"]["value"]
        elif current is None and "value" in call["props"]:
            current = call["props"]["value"]
        child = dict(ctx)
        child["_select_value"] = current
        inner = engine.render_nodes(call["slots"].get("default", []), child)
        name_attr = engine.attr("name", name) if name else ""
        return (
            '<select class="form-control"{name}{mark}>{inner}</select>'
        ).format(mark=engine.mark(call), name=name_attr, inner=inner)

