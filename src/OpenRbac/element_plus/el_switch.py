# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElSwitch.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElSwitch:
    """An on/off status. On is 0. Off is 1."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElSwitch")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A track and a knob. On posts 0. Off posts 1."""

        name = call["model"] or call["props"].get("name") or call["binds"].get("name") or ""
        current = self._current(call)
        on = current == "0"
        label = "Enabled" if on else "Disabled"
        if "label" in call["binds"] and call["binds"]["label"] is not None:
            label = str(call["binds"]["label"])
        classes = ["el-switch"]
        if on:
            classes.append("is-checked")
        mark = engine.mark(call)
        face = (
            '<span class="el-switch__core"><span class="el-switch__action"></span></span>'
            '<span class="el-switch__label">{0}</span>'
        ).format(engine.escape(label))
        class_attr = engine.escape(" ".join(classes))
        if name:
            checked = " checked" if on else ""
            named = engine.attr("name", name)
            return (
                '<label class="{classes}"{mark}>'
                '<input class="el-switch__input" type="checkbox"{named} value="0"{checked}>'
                "{face}</label>"
                '<input type="hidden"{named} value="1">'
            ).format(classes=class_attr, mark=mark, named=named, checked=checked, face=face)
        posting, decided = self._posting(call)
        if decided and posting:
            form_id = call["binds"].get("form", call["props"].get("form", "")) or ""
            form_attr = engine.attr("form", form_id) if str(form_id) != "" else ""
            pressed = "true" if on else "false"
            return (
                '<button type="submit" class="{classes}"{form} aria-pressed="{pressed}"{mark}>'
                "{face}</button>"
            ).format(
                classes=class_attr,
                form=form_attr,
                pressed=pressed,
                mark=mark,
                face=face,
            )
        if decided:
            classes.append("is-disabled")
            class_attr = engine.escape(" ".join(classes))
        return (
            '<span class="{classes}" aria-disabled="true"{mark}>{face}</span>'
        ).format(classes=class_attr, mark=mark, face=face)

    def _current(self, call) -> str:
        if call["model"] is not None and call["model_value"] is not None:
            return str(call["model_value"])
        if "value" in call["binds"] and call["binds"]["value"] is not None:
            return str(call["binds"]["value"])
        raw = call["props"].get("value")
        if raw:
            return str(raw)
        return ""

    def _posting(self, call):
        if "post" in call["binds"]:
            return self._posts(call["binds"]["post"]), True
        raw = call["props"].get("post")
        if raw not in (None, ""):
            return self._posts(raw), True
        return False, False

    def _posts(self, value) -> bool:
        if value is True or value == 1:
            return True
        if value is False or value is None:
            return False
        return str(value).strip() in ("1", "true", "True")
