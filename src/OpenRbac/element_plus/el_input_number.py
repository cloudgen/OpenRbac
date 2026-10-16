# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElInputNumber.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElInputNumber:
    """A whole-number field."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElInputNumber")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A whole-number field."""

        props = call["props"]
        binds = call["binds"]
        name = call["model"] or binds.get("name") or props.get("name") or ""
        if call["model"] is not None:
            value = call["model_value"]
        elif "value" in binds:
            value = binds["value"]
        else:
            value = props.get("value", "")
        if value is None:
            value = ""
        field_type = binds.get("type") or props.get("type") or "number"
        extra = ""
        placeholder = binds.get("placeholder", props.get("placeholder", ""))
        autocomplete = binds.get("autocomplete", props.get("autocomplete", ""))
        if placeholder:
            extra += engine.attr("placeholder", placeholder)
        if autocomplete:
            extra += engine.attr("autocomplete", autocomplete)
        name_attr = engine.attr("name", name) if name else ""
        return (
            '<input class="form-control" type="{typ}"{name} value="{val}"{extra}{mark}>'
        ).format(
            mark=engine.mark(call),
            typ=engine.escape(field_type),
            name=name_attr,
            val=engine.escape(value),
            extra=extra,
        )

