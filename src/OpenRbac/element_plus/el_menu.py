# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElMenu. The active item follows the
# request path. The browser does not run a script to choose it.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElMenu:
    """The sidebar menu. The active item is chosen from the request path."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElMenu")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: The sidebar menu, with the current location already active."""

        previous = ctx.get("_menu")
        ctx["_menu"] = {
            "active": self.active_text(call, ctx),
            "router": self.flag(call, "router"),
            "level": 0,
            "hits": 0,
        }
        try:
            inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        finally:
            if previous is None:
                ctx.pop("_menu", None)
            else:
                ctx["_menu"] = previous
        return (
            '<ul class="nav nav-pills nav-sidebar flex-column" role="menu"{mark}>{inner}</ul>'
        ).format(mark=engine.mark(call), inner=inner)

    def active_text(self, call, ctx) -> str:
        """General Purpose: The location this menu should mark. default-active wins, then path."""

        if "default-active" in call["binds"]:
            value = call["binds"]["default-active"]
            return "" if value is None else str(value)
        if "default-active" in call["props"]:
            return str(call["props"].get("default-active") or "")
        value = ctx.get("path", "")
        return "" if value is None else str(value)

    def flag(self, call, name) -> bool:
        """General Purpose: A Vue boolean attribute. A bare name is true."""

        if name in call["binds"]:
            value = call["binds"][name]
            if isinstance(value, bool):
                return value
            if value is None:
                return False
            return str(value).strip().lower() not in ("false", "0", "none", "")
        if name not in call["props"]:
            return False
        value = call["props"].get(name)
        if value is None:
            return False
        return str(value).strip().lower() not in ("false", "0", "none")

    def mode(self, call) -> str:
        """General Purpose: vertical or horizontal. Anything else stays vertical."""

        if "mode" in call["binds"]:
            value = call["binds"]["mode"]
        else:
            value = call["props"].get("mode", "vertical")
        text = "" if value is None else str(value).strip()
        if text == "horizontal":
            return "horizontal"
        return "vertical"

    def index_of(self, call):
        """General Purpose: The index attribute, from a bind or a literal."""

        if "index" in call["binds"]:
            return call["binds"]["index"]
        if "index" in call["props"]:
            return call["props"].get("index")
        return None

    def current(self, index, ctx) -> bool:
        """General Purpose: Whether this index is the menu's active location."""

        menu = ctx.get("_menu")
        if not isinstance(menu, dict):
            return False
        return self.same(index, menu.get("active"))

    def same(self, index, active) -> bool:
        """General Purpose: Same path, or a longer path under that index. Root matches only itself."""

        left = self.norm(index)
        right = self.norm(active)
        if left == "" or right == "":
            return False
        if left == right:
            return True
        if left != "/" and right.startswith(left + "/"):
            return True
        return False

    def norm(self, value) -> str:
        """General Purpose: A path without a query string or a trailing slash."""

        if value is None:
            return ""
        text = str(value).strip()
        if "?" in text:
            text = text.split("?", 1)[0]
        if text != "/" and text.endswith("/"):
            text = text[:-1]
        return text

    def href_for(self, index) -> str:
        """General Purpose: A same-site path safe to place in an href. Anything else is empty."""

        text = self.norm(index)
        if not text.startswith("/") or text.startswith("//"):
            return ""
        if any(ch in text for ch in (" ", "\t", "\r", "\n", '"', "'", "<", ">", "\\")):
            return ""
        return text

    def use_router(self, ctx) -> bool:
        """General Purpose: Whether items become links. There is no vue-router at run time."""

        menu = ctx.get("_menu")
        return isinstance(menu, dict) and bool(menu.get("router"))

    def note_hit(self, ctx):
        """General Purpose: Count one active descendant so the parent group can open."""

        menu = ctx.get("_menu")
        if isinstance(menu, dict):
            menu["hits"] = int(menu.get("hits") or 0) + 1
