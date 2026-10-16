# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElRadioGroup.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElRadioGroup:
    """A group of radios that share one posted name."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElRadioGroup")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A group of radios that share one posted name."""

        name = call["model"] or call["props"].get("name") or call["binds"].get("name") or ""
        current = call["model_value"]
        if current is None and "value" in call["binds"]:
            current = call["binds"]["value"]
        child = dict(ctx)
        child["_radio_name"] = name
        child["_radio_value"] = "" if current is None else current
        inner = engine.render_nodes(call["slots"].get("default", []), child)
        root = "form-group"
        return '<div class="{root}" role="radiogroup"{mark}>{inner}</div>'.format(
            root=root,
            mark=engine.mark(call),
            inner=inner,
        )

