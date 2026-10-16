# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElTreeSelect.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElTreeSelect:
    """A parent choice. Root is value 0."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElTreeSelect")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A parent choice. Root is value 0."""

        data = call["binds"].get("data", [])
        if not isinstance(data, (list, tuple)):
            data = []
        key_name = call["props"].get("node-key") or "id"
        label_key = call["props"].get("label-key") or "label"
        name = call["model"] or call["props"].get("name") or ""
        chosen = self._chosen(call)
        known = set()
        self._collect(data, key_name, known)
        if chosen != "0" and chosen not in known:
            chosen = "0"
        root_mark = " selected" if chosen == "0" else ""
        options = [
            '<option value="0"{0}>Root</option>'.format(root_mark)
        ]
        self._options(data, key_name, label_key, options, engine, chosen)
        name_attr = engine.attr("name", name) if name else ""
        return (
            '<select class="form-control"{name}{mark}>{options}</select>'
        ).format(mark=engine.mark(call), name=name_attr, options="".join(options))

    def _chosen(self, call) -> str:
        """General Purpose: The posted parent id, or 0 for the root."""
        if "value" in call["binds"] and call["binds"]["value"] not in (None, ""):
            return str(call["binds"]["value"])
        raw = call["props"].get("value") or ""
        if raw != "":
            return str(raw)
        return "0"

    def _collect(self, items, key_name, known):
        """General Purpose: Every node id, so an unknown value falls back to root."""
        for item in items:
            if not isinstance(item, dict):
                continue
            known.add(str(item.get(key_name, "")))
            children = item.get("children") or []
            if children:
                self._collect(children, key_name, known)

    def _options(self, items, key_name, label_key, options, engine, chosen):
        """General Purpose: Option rows for each node except a second root."""
        for item in items:
            if not isinstance(item, dict):
                continue
            ident = item.get(key_name, "")
            children = item.get("children") or []
            if str(ident) == "0":
                if children:
                    self._options(children, key_name, label_key, options, engine, chosen)
                continue
            label = item.get(label_key, ident)
            selected = " selected" if str(ident) == chosen else ""
            options.append(
                '<option value="{value}"{selected}>{label}</option>'.format(
                    value=engine.escape(ident),
                    selected=selected,
                    label=engine.escape(label),
                )
            )
            if children:
                self._options(children, key_name, label_key, options, engine, chosen)

