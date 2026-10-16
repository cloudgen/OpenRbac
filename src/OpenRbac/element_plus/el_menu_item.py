# =============================================================================
# Element Plus HTML component.
# requirement-html-element-plus — class ElMenuItem. is-active is rendered
# with the HTML when the index matches the menu location.
# requirement-python-oop — one component class.
# =============================================================================
from __future__ import annotations


class ElMenuItem:
    """One sidebar destination. The current path is active in the HTML."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ElMenuItem")

    def render(self, call, ctx, engine) -> str:
        """General Purpose: One sidebar destination. router draws a link. No script selects it."""

        index = engine.menu.index_of(call)
        active = engine.menu.current(index, ctx)
        if active:
            engine.menu.note_hit(ctx)
        classes = ["nav-item"]
        inner = engine.render_nodes(call["slots"].get("default", []), ctx)
        href = engine.menu.href_for(index) if engine.menu.use_router(ctx) else ""
        if href and "<a" not in inner.lower():
            link_class = "nav-link active" if active else "nav-link"
            inner = '<a class="{0}" href="{1}">{2}</a>'.format(
                link_class,
                engine.escape(href),
                inner,
            )
        current = ' aria-current="page"' if active else ""
        return (
            '<li class="{classes}" role="menuitem"{current}{mark}>{inner}</li>'
        ).format(
            classes=engine.escape(" ".join(classes)),
            current=current,
            mark=engine.mark(call),
            inner=inner,
        )
