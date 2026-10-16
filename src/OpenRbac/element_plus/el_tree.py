# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElTree.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElTree:
    """A tree. show-checkbox posts each node key."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElTree")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A tree. show-checkbox posts each node key."""

        data = call["binds"].get("data", [])
        if not isinstance(data, (list, tuple)):
            data = []
        key_name = call["props"].get("node-key") or "id"
        label_key = call["props"].get("label-key") or "label"
        post_name = call["props"].get("name") or call["model"] or ""
        show = "show-checkbox" in call["props"] and str(call["props"].get("show-checkbox")).lower() != "false"
        inner = self._nodes(data, key_name, label_key, post_name, show, ctx, engine)
        root = "list-unstyled"
        return '<div class="{root}" role="tree"{mark}>{inner}</div>'.format(
            root=root,
            mark=engine.mark(call),
            inner=inner,
        )

    def _nodes(self, items, key_name, label_key, post_name, show, ctx, engine) -> str:
        """General Purpose: One level of tree nodes, including nested children."""
        parts = []
        checkbox = engine.components["el-checkbox"]
        for item in items:
            if not isinstance(item, dict):
                continue
            ident = item.get(key_name, "")
            label = item.get(label_key, "")
            perms = item.get("perms") or ""
            text = str(label)
            if perms:
                text = "{0} {1}".format(text, perms)
            if show and post_name:
                box = {
                    "props": {"name": post_name},
                    "binds": {"value": ident},
                    "model": None,
                    "model_value": None,
                    "slots": {"default": [{"kind": "text", "text": text}]},
                    "hidden": False,
                }
                if item.get("checked"):
                    box["model"] = post_name
                    box["model_value"] = [ident]
                control = checkbox.render(box, ctx, engine)
            else:
                label_class = "form-check-label"
                control = '<span class="{0}">{1}</span>'.format(label_class, engine.escape(text))
            children = item.get("children") or []
            nested = ""
            if children:
                child_class = "ml-3"
                nested = '<div class="{0}">{1}</div>'.format(
                    child_class,
                    self._nodes(children, key_name, label_key, post_name, show, ctx, engine),
                )
            node_class = "mb-1"
            parts.append(
                '<div class="{0}" role="treeitem">{1}{2}</div>'.format(node_class, control, nested)
            )
        return "".join(parts)

