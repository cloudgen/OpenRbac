# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElSubMenu. The group that contains
# the current path is opened in the HTML.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElSubMenu:
    """A sidebar group. The title slot is the group name."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElSubMenu")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: A sidebar group. The group that holds the current path is active."""

        title = engine.render_nodes(call["slots"].get("title", []), ctx)
        menu = ctx.get("_menu")
        if not isinstance(menu, dict):
            menu = None
        level = 0 if menu is None else int(menu.get("level") or 0)
        before = 0 if menu is None else int(menu.get("hits") or 0)
        if menu is not None:
            menu["level"] = level + 1
        try:
            inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        finally:
            if menu is not None:
                menu["level"] = level
        active = menu is not None and int(menu.get("hits") or 0) > before
        index = engine.menu.index_of(call)
        if engine.menu.current(index, ctx):
            active = True
            engine.menu.note_hit(ctx)
        classes = ["nav-item", "has-treeview", "menu-open"]
        if active:
            classes.append("menu-is-opening")
        return (
            '<li class="{classes}"{mark}>'
            '<p class="nav-link">{title}</p>'
            '<ul class="nav nav-treeview">{inner}</ul>'
            "</li>"
        ).format(
            classes=engine.escape(" ".join(classes)),
            mark=engine.mark(call),
            title=title,
            inner=inner,
        )
