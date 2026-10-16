# Vue-shaped templates and Element Plus HTML components.
# The browser receives HTML. A script block fails the render.
import sys
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from OpenRbac.html_template import HtmlTemplate, HtmlTemplateError

TABLE_CHECK_SCRIPT = '<script src="/table-check.js"></script>'


def assert_only_check_script(test, html):
    """A document with a table checkbox loads only /table-check.js."""
    if 'class="table-check' in html:
        test.assertEqual(html.count(TABLE_CHECK_SCRIPT), 1)
        test.assertNotIn("<script", html.replace(TABLE_CHECK_SCRIPT, "").lower())
    else:
        test.assertNotIn("<script", html.lower())


ROOT_CLASS = {
    "el-button": 'class="btn',
    "el-form": 'class="form-horizontal"',
    "el-form-item": 'class="form-group"',
    "el-input": 'class="form-control"',
    "el-input-number": 'class="form-control"',
    "el-select": 'class="form-control"',
    "el-option": 'class="el-option"',
    "el-radio": 'class="form-check"',
    "el-radio-group": 'class="form-group"',
    "el-checkbox": 'class="form-check"',
    "el-switch": 'class="el-switch"',
    "el-table": 'class="table table-bordered table-striped"',
    "el-table-column": 'class="el-table-column"',
    "el-dialog": 'class="card card-primary card-outline"',
    "el-row": 'class="el-row"',
    "el-col": 'class="el-col',
    "el-tree": 'class="list-unstyled"',
    "el-tree-select": 'class="form-control"',
    "el-tag": 'class="el-tag"',
    "el-tooltip": 'class="el-tooltip"',
    "el-pagination": 'class="text-muted"',
    "el-menu": 'class="nav nav-pills nav-sidebar',
    "el-menu-item": 'class="nav-item"',
    "el-sub-menu": 'class="nav-item',
    "el-breadcrumb": 'class="breadcrumb"',
    "el-breadcrumb-item": 'class="breadcrumb-item"',
    "el-dropdown": 'class="navbar-nav"',
    "el-dropdown-menu": 'class="nav"',
    "el-dropdown-item": 'class="nav-item"',
    "el-scrollbar": 'class="el-scrollbar"',
    "el-icon": 'class="el-icon"',
    "el-popover": 'class="el-popover"',
    "el-date-picker": 'class="el-date-picker"',
}


class TestHtmlTemplate(unittest.TestCase):
    """The renderer escapes text, chooses one branch, and refuses script."""

    def setUp(self):
        self.engine = HtmlTemplate()

    def test_interpolation_escapes_text(self):
        html = self.engine.render_source(
            "<template><p>{{ name }}</p></template>",
            {"name": "a<b"},
        )
        self.assertIn("a&lt;b", html)
        self.assertNotIn("a<b", html)

    def test_missing_name_and_v_html_fail(self):
        with self.assertRaises(HtmlTemplateError) as missing:
            self.engine.render_source("<template><p>{{ absent }}</p></template>", {})
        self.assertIn("absent", str(missing.exception))
        with self.assertRaises(HtmlTemplateError) as raw:
            self.engine.render_source(
                '<template><div v-html="name"></div></template>',
                {"name": "a<b"},
            )
        self.assertIn("v-html", str(raw.exception))

    def test_script_and_style_blocks_fail(self):
        with self.assertRaises(HtmlTemplateError) as script:
            self.engine.render_source("<template><script>alert(1)</script></template>", {})
        self.assertIn("script", str(script.exception).lower())
        with self.assertRaises(HtmlTemplateError) as style:
            self.engine.render_source("<template><style>p{}</style></template>", {})
        self.assertIn("style", str(style.exception).lower())

    def test_branches_and_hidden_state(self):
        source = (
            "<template>"
            '<p v-if="show">yes</p>'
            '<p v-else-if="other">mid</p>'
            "<p v-else>no</p>"
            "</template>"
        )
        self.assertIn("yes", self.engine.render_source(source, {"show": True, "other": True}))
        self.assertNotIn("mid", self.engine.render_source(source, {"show": True, "other": True}))
        mid = self.engine.render_source(source, {"show": False, "other": True})
        self.assertIn("mid", mid)
        self.assertNotIn("yes", mid)
        no = self.engine.render_source(source, {"show": False, "other": False})
        self.assertIn(">no<", no)
        hidden = self.engine.render_source(
            '<template><p v-show="flag">kept</p></template>',
            {"flag": False},
        )
        self.assertIn("kept", hidden)
        self.assertIn("hidden", hidden)
        self.assertIn('style="display:none"', hidden)
        skipped = self.engine.render_source(
            '<template><p v-if="off">{{ missing }}</p><p v-else>ok</p></template>',
            {"off": False},
        )
        self.assertIn("ok", skipped)

    def test_repeat_and_dotted_list(self):
        html = self.engine.render_source(
            '<template><span v-for="(row, index) in rows">{{ index }}:{{ row }}</span></template>',
            {"rows": ["a<b"]},
        )
        self.assertIn("0:", html)
        self.assertIn("a&lt;b", html)
        nested = self.engine.render_source(
            '<template><span v-for="row in group.items">{{ row }}</span></template>',
            {"group": {"items": ["one", "two"]}},
        )
        self.assertIn("one", nested)
        self.assertIn("two", nested)
        with self.assertRaises(HtmlTemplateError) as dotted:
            self.engine.render_source(
                '<template><p v-if="row.ok">x</p></template>',
                {"row": {"ok": True}},
            )
        self.assertIn("row.ok", str(dotted.exception))

    def test_unknown_tag_and_directive_fail(self):
        with self.assertRaises(HtmlTemplateError) as tag:
            self.engine.render_source("<template><foo></foo></template>", {})
        self.assertIn("foo", str(tag.exception))
        with self.assertRaises(HtmlTemplateError) as directive:
            self.engine.render_source('<template><div v-foo="x"></div></template>', {})
        self.assertIn("v-foo", str(directive.exception))

    def test_event_emits_no_script_and_model_sets_the_field(self):
        html = self.engine.render_source(
            '<template><button @click="save">Go</button></template>',
            {},
        )
        self.assertIn("Go", html)
        self.assertNotIn("onclick", html.lower())
        self.assertNotIn("<script", html.lower())
        field = self.engine.render_source(
            '<template><input v-model="name"></template>',
            {"name": 'a<b"c'},
        )
        self.assertIn('name="name"', field)
        self.assertIn("a&lt;b&quot;c", field)
        self.assertNotIn("<script", field.lower())

    def test_each_component_renders_its_root_class(self):
        self.assertEqual(len(ROOT_CLASS), len(self.engine.components))
        for tag, marker in ROOT_CLASS.items():
            html = self.engine.render_source(
                "<template><{0}>Hi</{0}></template>".format(tag),
                {},
            )
            self.assertIn(marker, html, tag)
            self.assertNotIn("<script", html.lower(), tag)

    def test_bind_keeps_name_before_value(self):
        html = self.engine.render_source(
            '<template><input type="hidden" name="csrf" :value="csrf"></template>',
            {"csrf": "token-1"},
        )
        self.assertIn('name="csrf" value="token-1"', html)

    def test_checkbox_tree_posts_menu_id(self):
        html = self.engine.render_source(
            '<template><el-tree :data="menus" show-checkbox name="menu_id" '
            'node-key="menu_id" label-key="menu_name"></el-tree></template>',
            {"menus": [{"menu_id": 100, "menu_name": "User", "perms": "system:user:list"}]},
        )
        self.assertIn('class="list-unstyled"', html)
        self.assertIn('class="form-check"', html)
        self.assertIn('name="menu_id"', html)
        self.assertIn('value="100"', html)
        self.assertNotIn("<script", html.lower())

    def test_check_all_script_is_same_origin(self):
        """The header box checks the row boxes in that table. It does not measure layout."""
        root = Path(__file__).resolve().parents[1]
        script = (root / "src/OpenRbac/element_plus/table-check.js").read_text(encoding="utf-8")
        self.assertIn('tbody input.table-check[type="checkbox"]', script)
        self.assertIn('thead input.table-check[type="checkbox"]', script)
        self.assertIn("list[index].checked = box.checked", script)
        self.assertIn("head.indeterminate", script)
        for banned in (
            "scrollHeight",
            "offsetHeight",
            "clientHeight",
            "getBoundingClientRect",
            ".style",
            "vue",
            "jquery",
            "element-plus",
        ):
            self.assertNotIn(banned, script.lower() if banned in ("vue", "jquery") else script)
        login = self.engine.render_document("login", {
            "title": "Sign in",
            "error": "",
            "engine": "sqlite3",
            "sqlite_label": "sqlite3 file",
            "mysql_label": "mysql openrbac",
        })
        self.assertNotIn("<script", login.lower())
        page = self.engine.render_document("test", {
            "title": "Users",
            "rows": [],
            "can_edit": False,
            "can_remove": False,
            "can_reset": False,
            "csrf": "token",
        })
        self.assertEqual(page.count(TABLE_CHECK_SCRIPT), 1)
        self.assertNotIn("<script", page.replace(TABLE_CHECK_SCRIPT, "").lower())

    def test_sidebar_is_a_definite_scrollport(self):
        root = Path(__file__).resolve().parents[1]
        templates = root / "src/OpenRbac/templates"
        for path in templates.glob("*.vue"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(
                "el-scrollbar",
                text,
                "{0} must not use a percentage-height scroll wrap".format(path.name),
            )
        css = (root / "src/OpenRbac/element_plus/apex.css").read_text(encoding="utf-8")
        sidebar = css.split(".main-sidebar {", 1)[1].split("}", 1)[0]
        self.assertIn("height: 100vh", sidebar)
        self.assertIn("overflow: auto", sidebar)
        banned = ("scrollHeight", "offsetHeight", "clientHeight", "getBoundingClientRect")
        plus = root / "src/OpenRbac/element_plus"
        paths = list(plus.glob("*.py")) + list(plus.glob("*.js"))
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for name in banned:
                self.assertNotIn(name, text, "{0} mentions {1}".format(path.name, name))
        html = self.engine.render(
            "shell",
            {
                "title": "Users",
                "user_name": "admin",
                "csrf": "token",
                "path": "/users",
                "nav_groups": [
                    {"label": "Access", "items": [{"href": "/users", "label": "Users"}]}
                ],
            },
        )
        self.assertIn("main-sidebar", html)
        self.assertIn("nav-sidebar", html)
        self.assertIn('class="nav-link active"', html)
        self.assertNotIn("el-menu", html)
        self.assertNotIn("el-scrollbar", html)
        self.assertIn('aria-current="page"', html)
        self.assertIn('href="/users"', html)
        self.assertNotIn("<script", html.lower())
        themed = self.engine.render(
            "shell",
            {
                "title": "Users",
                "user_name": "admin",
                "csrf": "token",
                "path": "/users",
                "theme": "hospital",
                "nav_groups": [
                    {"label": "Access", "items": [{"href": "/users", "label": "Users"}]}
                ],
            },
        )
        self.assertIn("main-sidebar", themed)
        self.assertIn("nav-sidebar", themed)
        self.assertIn('class="nav-link active"', themed)
        self.assertNotIn("el-menu", themed)
        self.assertNotIn("el-scrollbar", themed)
        self.assertNotIn("<script", themed.lower())
        skin = (root / "src/OpenRbac/element_plus/apex.css").read_text(encoding="utf-8")
        column = skin.split(".main-sidebar {", 1)[1].split("}", 1)[0]
        self.assertIn("height: 100vh", column)
        self.assertIn("overflow: auto", column)

    def test_theme_picks_the_stylesheet_and_the_markup(self):
        login = {
            "title": "Sign in",
            "error": "",
            "engine": "sqlite3",
            "sqlite_label": "sqlite3 file",
            "mysql_label": "mysql openrbac",
        }
        vue = self.engine.render_document("login", login)
        self.assertIn('href="/apex.css"', vue)
        self.assertIn('href="/themes/apex.css"', vue)
        self.assertNotIn("element-plus.css", vue)
        self.assertNotIn("openrbac.css", vue)
        self.assertIn('class="form-horizontal"', vue)
        self.assertIn('class="btn btn-primary btn-lg"', vue)
        admin = dict(login)
        admin["theme"] = "admindek"
        themed = self.engine.render_document("login", admin)
        self.assertIn('href="/apex.css"', themed)
        self.assertIn('href="/themes/admindek.css"', themed)
        self.assertNotIn("element-plus.css", themed)
        self.assertNotIn("openrbac.css", themed)
        self.assertIn('class="form-control"', themed)
        self.assertIn('class="btn btn-primary btn-lg"', themed)
        self.assertIn('class="form-check-input"', themed)
        self.assertNotIn("<script", themed.lower())
        for piece in (
            'method="post"',
            'action="/login"',
            'name="user_name"',
            'name="password"',
            'name="engine"',
        ):
            self.assertIn(piece, vue)
            self.assertIn(piece, themed)
        table = self.engine.render_source(
            "<template><el-table :data=\"rows\">"
            '<el-table-column prop="user_name" label="user_name" />'
            "</el-table></template>",
            {"theme": "apex", "rows": [{"user_name": "admin"}]},
        )
        self.assertIn('class="table table-bordered table-striped"', table)
        self.assertIn("admin", table)
        self.assertNotIn("el-table", table)
        choice = self.engine.render_source(
            "<template><el-select name=\"sex\"><el-option value=\"0\">Male</el-option></el-select></template>",
            {"theme": "apex"},
        )
        self.assertIn('<select class="form-control" name="sex">', choice)
        self.assertNotIn("el-select", choice)
        skin = (Path(__file__).resolve().parents[1] / "src/OpenRbac/element_plus/apex.css").read_text(encoding="utf-8")
        self.assertIn("tailwindcss v4.3.3", skin)
        self.assertIn("--primary:oklch(50% .175 160)", skin)
        self.assertIn("border-radius: var(--radius)", skin)
        self.assertIn("font-size: 13px", skin)
        self.assertNotIn("data:image", skin)
        self.assertIn("background: var(--primary)", skin)
        self.assertNotIn("#1ab394", skin)
        self.assertNotIn(".pc-sidebar", skin)
        themes = Path(__file__).resolve().parents[1] / "src/OpenRbac/element_plus/themes"
        apex_theme = (themes / "apex.css").read_text(encoding="utf-8")
        admindek_theme = (themes / "admindek.css").read_text(encoding="utf-8")
        self.assertIn("--primary: #1ab394", apex_theme)
        self.assertIn("--background: #ffffff", apex_theme)
        self.assertIn("--border: #e7eaec", apex_theme)
        self.assertIn("--primary: #4f46e5", admindek_theme)
        self.assertIn("--sidebar: #1e1b4b", admindek_theme)
        self.assertNotIn("#4680ff", admindek_theme)
        self.assertNotIn("#1e293b", admindek_theme)
        self.assertNotIn(".pc-sidebar", admindek_theme)
        bare = self.engine.render_document("test", {
            "title": "Users",
            "theme": "apex",
            "error": "",
            "csrf": "token",
            "rows": [{
                "user_id": 1,
                "user_name": "admin",
                "nick_name": "Admin",
                "initials": "AD",
                "dept_name": "Group",
                "phone": "",
                "status": "0",
                "status_label": "Enabled",
                "status_form": "user-status-1",
                "status_post": False,
                "status_next": "1",
                "created": "2026-01-01",
                "edit_href": "/users?form=edit&user_id=1",
                "remove_href": "/users?form=remove&user_id=1",
                "reset_href": "/users?form=reset&user_id=1",
            }],
            "can_choose": True,
            "can_edit": True,
            "can_remove": True,
            "can_reset": True,
        })
        self.assertIn('class="table table-bordered table-striped"', bare)
        self.assertIn('aria-label="check all"', bare)
        self.assertIn('aria-label="Select row"', bare)
        self.assertIn(">User<", bare)
        self.assertIn('data-prop="dept_name"', bare)
        self.assertIn('data-prop="created"', bare)
        self.assertIn(">JOINED<", bare)
        self.assertIn('class="min-w-0"', bare)
        self.assertIn(
            'class="font-medium truncate hover:text-primary block"',
            bare,
        )
        self.assertIn('class="text-xs text-muted-foreground truncate"', bare)
        self.assertIn(">Admin<", bare)
        self.assertIn("@admin", bare)
        self.assertIn('class="user-person"', bare)
        self.assertIn('class="user-person-mark"', bare)
        self.assertIn(">AD<", bare)
        self.assertNotIn(">User id<", bare)
        self.assertIn('class="table-check h-4 w-4 rounded border-input"', bare)
        self.assertIn('class="table-check-col"', bare)
        self.assertNotIn("x-model", bare)
        self.assertNotIn("main-sidebar", bare)
        self.assertNotIn("user-page", bare)
        assert_only_check_script(self, bare)

    def test_adminlte_keeps_the_posted_field_names(self):
        """requirement-html-theme — AC-7. The skin changes classes, not the post."""
        values = {
            "title": "Users",
            "error": "",
            "user_name": "admin",
            "csrf": "token",
            "path": "/users",
            "rows": [],
            "total": 0,
            "limit": 10,
            "departments": [],
            "can_depts": False,
            "query_user_name": "",
            "query_phone": "",
            "query_state": "",
            "query_begin": "",
            "query_end": "",
            "query_dept": "",
            "state_all": True,
            "state_on": False,
            "state_off": False,
            "state_all_href": "/users",
            "state_on_href": "/users?state=0",
            "state_off_href": "/users?state=1",
            "note": "",
            "can_add": True,
            "can_edit": False,
            "can_reset": False,
            "can_remove": False,
            "can_import": False,
            "can_export": False,
            "can_choose": False,
            "add_href": "/users?form=add",
            "import_href": "/users?form=import",
            "export_href": "/users/export",
            "show_add": True,
            "show_edit": False,
            "show_reset": False,
            "show_remove": False,
            "show_import": False,
            "nav_groups": [],
        }
        vue = self.engine.render_document("users", values)
        admin = dict(values)
        admin["theme"] = "kero"
        themed = self.engine.render_document("users", admin)
        for piece in (
            'method="post"',
            'action="/users/add"',
            'name="csrf"',
            'name="user_name"',
            'name="nick_name"',
            'name="dept_id"',
            'name="role_id"',
            'name="password"',
        ):
            self.assertIn(piece, vue)
            self.assertIn(piece, themed)
        self.assertIn('class="card card-primary card-outline"', vue)
        self.assertIn('class="card card-primary card-outline"', themed)
        self.assertNotIn("el-dialog", vue)
        self.assertNotIn("el-dialog", themed)
        self.assertNotIn("el-form", themed)
        self.assertNotIn("el-input", themed)
        self.assertNotIn("<script", themed.lower())

    def test_users_page_is_the_user_management_screen(self):
        """requirement-html-user-management — AC-1 through AC-8."""
        from OpenRbac.web_app import WebApp

        class Gate:
            def __init__(self, allowed):
                self.allowed = allowed

            def allows(self, user_id, perm):
                return perm in self.allowed

        full = WebApp(None, Gate({
            "system:user:list",
            "system:role:list",
            "system:menu:list",
            "system:dept:list",
            "system:jobtitle:list",
            "system:config:list",
            "system:dict:list",
            "system:notice:list",
            "monitor:operlog:list",
            "monitor:logininfor:list",
            "monitor:online:list",
            "system:config:edit",
        }), None, None)
        groups = {}
        for group in full._nav({"user_id": 1}):
            groups[group["label"]] = [item["href"] for item in group["items"]]
        self.assertEqual(
            groups["Access"],
            ["/users", "/roles", "/menus", "/depts", "/job-titles"],
        )
        self.assertEqual(groups["Catalog"], ["/configs", "/dicts", "/notices"])
        self.assertEqual(groups["Audit"], ["/oper-log", "/login-log", "/online"])
        self.assertNotIn("/system/user", str(groups))
        listed = WebApp(None, Gate({"system:user:list"}), None, None)
        access = [
            group for group in listed._nav({"user_id": 2}) if group["label"] == "Access"
        ][0]
        self.assertEqual(access["items"], [{"href": "/users", "label": "Users"}])
        self.assertIsNone(listed._route_get("/system/user", {"user_id": 2}, ""))
        self.assertIsNone(listed._route_get("/system/user/profile", {"user_id": 2}, ""))
        values = {
            "title": "Users",
            "error": "",
            "user_name": "admin",
            "csrf": "token",
            "path": "/users",
            "rows": [{
                "user_id": 2,
                "user_name": "clerk",
                "nick_name": "Clerk",
                "initials": "CL",
                "dept_name": "Office",
                "phone": "",
                "status": "0",
                "status_label": "Enabled",
                "status_next": "1",
                "status_form": "user-status-2",
                "status_post": True,
                "created": "2026-10-14 00:00:00",
                "edit_href": "/users?dept=103&form=edit&user_id=2",
                "remove_href": "/users?dept=103&form=remove&user_id=2",
                "reset_href": "/users?dept=103&form=reset&user_id=2",
            }],
            "total": 1,
            "limit": 200,
            "departments": [
                {
                    "dept_name": "Group",
                    "href": "/users?dept=100",
                    "depth_class": "user-depth-0 user-node-branch is-first is-last is-root",
                    "link_class": "user-tree-link",
                    "children": [
                        {
                            "dept_name": "Office",
                            "href": "/users?dept=103",
                            "depth_class": "user-depth-1 user-node-leaf is-first is-last",
                            "link_class": "user-tree-link is-current",
                            "children": [],
                        },
                    ],
                },
            ],
            "can_depts": True,
            "query_user_name": "",
            "query_phone": "",
            "query_state": "",
            "query_begin": "",
            "query_end": "",
            "query_dept": "103",
            "state_all": True,
            "state_on": False,
            "state_off": False,
            "state_all_href": "/users?dept=103",
            "state_on_href": "/users?state=0&dept=103",
            "state_off_href": "/users?state=1&dept=103",
            "note": "",
            "can_add": True,
            "can_edit": True,
            "can_reset": True,
            "can_remove": True,
            "can_import": True,
            "can_export": True,
            "can_choose": True,
            "add_href": "/users?dept=103&form=add",
            "import_href": "/users?dept=103&form=import",
            "export_href": "/users/export?dept=103",
            "show_add": False,
            "show_edit": False,
            "show_reset": False,
            "show_remove": False,
            "show_import": False,
            "nav_groups": full._nav({"user_id": 1}),
        }
        html = self.engine.render_document("users", values)
        self.assertIn('href="/apex.css"', html)
        self.assertIn('href="/themes/apex.css"', html)
        self.assertIn("Organization", html)
        self.assertIn('class="user-page"', html)
        self.assertIn('href="/users?dept=100"', html)
        self.assertIn("user-tree-link is-current", html)
        self.assertIn('class="user-org-manage"', html)
        self.assertIn('href="/depts"', html)
        self.assertIn(">Search<", html)
        self.assertIn(">Reset<", html)
        self.assertIn('class="admlte-date-range"', html)
        self.assertNotIn(">From<", html)
        self.assertNotIn(">To<", html)
        self.assertIn('id="admlte-date-from" type="date" name="begin"', html)
        self.assertIn('id="admlte-date-to" type="date" name="end"', html)
        self.assertIn('class="admlte-date-range-arrow" aria-hidden="true">→<', html)
        self.assertNotIn("max=", html)
        self.assertNotIn("min=", html)
        self.assertIn('class="user-btn user-btn-search"', html)
        self.assertIn('class="user-btn user-btn-reset"', html)
        self.assertIn('class="user-btn user-btn-add"', html)
        self.assertIn('class="user-btn user-btn-edit"', html)
        self.assertIn('class="user-btn user-btn-remove"', html)
        self.assertIn('class="user-btn user-btn-import"', html)
        self.assertIn('class="user-btn user-btn-export"', html)
        self.assertIn('class="user-btn user-btn-resetpwd"', html)
        self.assertIn('class="user-tree"', html)
        self.assertIn("user-node-icon", html)
        self.assertIn("user-switch", html)
        self.assertIn("user-node-branch", html)
        self.assertIn("user-node-leaf", html)
        self.assertLess(html.index(">Group<"), html.index(">Office<"))
        self.assertLess(html.index(">Office<"), html.rindex("</ul>"))
        self.assertIn(">Add<", html)
        self.assertIn(">Edit<", html)
        self.assertIn(">Remove<", html)
        self.assertIn(">Import<", html)
        self.assertIn(">Export<", html)
        self.assertIn('aria-label="check all"', html)
        self.assertIn('class="table-check" type="checkbox" name="user_id"', html)
        self.assertIn('aria-label="Select row"', html)
        self.assertNotIn(">Choose<", html)
        self.assertNotIn('type="radio"', html)
        self.assertLess(html.index('aria-label="check all"'), html.index(">User<"))
        self.assertIn('class="table-check-col"', html)
        self.assertIn('class="table-check-col"', html)
        self.assertIn('class="min-w-0"', html)
        self.assertIn(
            'class="font-medium truncate hover:text-primary block"',
            html,
        )
        self.assertIn('class="text-xs text-muted-foreground truncate"', html)
        self.assertIn(">Clerk<", html)
        self.assertIn("@clerk", html)
        self.assertIn(
            'href="/users?dept=103&amp;form=edit&amp;user_id=2"',
            html,
        )
        self.assertNotIn(">User id<", html)
        self.assertNotIn(">Login name<", html)
        self.assertIn('class="user-person"', html)
        self.assertIn('class="user-person-mark"', html)
        self.assertIn(">CL<", html)
        self.assertEqual(full._user_initials("Administrator", "admin"), "AD")
        self.assertEqual(full._user_initials("Clerk", "clerk"), "CL")
        self.assertEqual(full._user_initials("", "admin"), "AD")
        self.assertIn(">Enabled<", html)
        self.assertIn('class="el-switch is-checked"', html)
        self.assertIn('class="el-switch__core"', html)
        self.assertIn('form="user-status-2"', html)
        self.assertIn('id="user-status-2"', html)
        self.assertIn('action="/users/status"', html)
        self.assertIn('name="status" value="1"', html)
        self.assertIn(">Edit<", html)
        self.assertIn(">Remove<", html)
        self.assertNotIn("Add a user", html)
        self.assertNotIn("user-edit-float", html)
        self.assertNotIn("Choose a department", html)
        self.assertNotIn('action="/users/add"', html)
        labels = (
            "User",
            "Department",
            "Phone",
            "Status",
            "Created",
            "Action",
        )
        positions = []
        for label in labels:
            token = ">{0}<".format(label)
            self.assertIn(token, html)
            positions.append(html.index(token))
        self.assertEqual(positions, sorted(positions))
        self.assertIn('href="/users"', html)
        self.assertIn('aria-current="page"', html)
        self.assertIn(">admin<", html)
        self.assertIn('method="post"', html)
        self.assertIn('action="/logout"', html)
        self.assertIn('name="csrf"', html)
        self.assertIn('method="get"', html)
        self.assertIn('name="user_name"', html)
        self.assertIn('name="phone"', html)
        lowered = html.lower()
        for banned in (
            "<iframe",
            "<style",
            "bootstrap.min.css",
            "jquery",
            "font-awesome",
            "ruoyi.vip",
            "doc.ruoyi.vip",
        ):
            self.assertNotIn(banned, lowered)
        assert_only_check_script(self, html)
        opened = dict(values)
        opened["show_add"] = True
        opened["show_edit"] = True
        opened["show_reset"] = True
        opened["show_remove"] = True
        opened["show_import"] = True
        opened["edit_user_id"] = "2"
        opened["edit_nick"] = "Clerk"
        opened["edit_dept"] = "103"
        opened["edit_status"] = "0"
        opened["edit_phone"] = ""
        opened["edit_email"] = ""
        opened["edit_login"] = "operator"
        opened["edit_remark"] = ""
        opened["edit_dept_name"] = "Operations"
        opened["edit_close_href"] = "/users?dept=103"
        opened["dept_q"] = ""
        opened["picker_dept"] = False
        opened["dept_cleared"] = False
        opened["sex_male"] = False
        opened["sex_female"] = False
        opened["sex_unknown"] = True
        opened["job_titles"] = [
            {"job_title_id": "1", "job_title": "Chief", "checked": True},
            {"job_title_id": "2", "job_title": "Engineer", "checked": False},
        ]
        opened["edit_roles"] = [
            {"role_id": "2", "role_name": "Common", "checked": True, "locked": False},
            {"role_id": "1", "role_name": "Super administrator", "checked": False, "locked": False},
        ]
        opened["edit_departments"] = [{
            "dept_name": "Group",
            "dept_id": "100",
            "checked": True,
            "href": "/users?dept=100",
            "depth_class": "user-depth-0 user-node-branch is-first is-last is-root",
            "link_class": "user-tree-link is-current",
            "children": [],
        }]
        opened["reset_user_id"] = "2"
        opened["remove_user_id"] = "2"
        opened["remove_name"] = "clerk"
        forms = self.engine.render_document("users", opened)
        self.assertIn("Add a user", forms)
        self.assertIn("Edit a user", forms)
        self.assertIn("Reset a password", forms)
        self.assertIn("Remove a user", forms)
        self.assertIn("Import users", forms)
        self.assertIn('action="/users/import"', forms)
        self.assertIn('enctype="multipart/form-data"', forms)
        self.assertIn('name="file"', forms)
        self.assertIn('name="update_support"', forms)
        self.assertIn('class="card card-primary card-outline"', forms)
        self.assertIn('class="form-horizontal"', forms)
        for action in ("/users/add", "/users/edit", "/users/reset", "/users/remove"):
            self.assertIn('action="{0}"'.format(action), forms)
        edit_at = forms.index("Edit a user")
        edit_form = forms[edit_at:]
        self.assertIn('type="checkbox"', edit_form)
        self.assertLess(edit_form.index('value="0"'), edit_form.index('value="1"'))
        self.assertIn('class="el-switch is-checked"', edit_form)
        self.assertIn("user-edit-float", forms)
        assert_only_check_script(self, forms)
        self.assertIn("Account", forms)
        self.assertIn("Choose a department", forms)
        self.assertIn('name="phonenumber"', forms)
        self.assertIn('name="email"', forms)
        self.assertIn('name="sex"', forms)
        self.assertIn('name="job_title_id"', forms)
        self.assertIn('name="role_id"', forms)
        self.assertIn('name="remark"', forms)
        self.assertIn('name="dept_id"', forms)
        self.assertIn("Chief", forms)
        self.assertIn("Male", forms)
        self.assertIn("Female", forms)
        self.assertIn("Unknown", forms)
        self.assertIn(
            '<input class="user-readonly" type="text" readonly="" value="operator">',
            forms,
        )
        self.assertNotIn('checked="False"', forms)
        self.assertNotIn('selected="False"', forms)
        self.assertIn("user-btn-close", forms)
        self.assertLess(edit_form.index(">Save<"), edit_form.index('name="picker"'))
        self.assertIn('formmethod="get"', edit_form)
        add_end = forms.index("Edit a user")
        self.assertNotIn('name="job_title_id"', forms[:add_end])
        close_at = forms.index('<a class="user-btn user-btn-close"')
        close = forms[close_at:forms.index("</a>", close_at)]
        self.assertIn(">Close", close)
        self.assertNotIn("user-btn-remove", close)
        admin_edit = dict(opened)
        admin_edit["theme"] = "kero"
        admin_html = self.engine.render_document("users", admin_edit)
        self.assertIn("user-edit-float", admin_html)
        self.assertIn("Choose a department", admin_html)
        self.assertIn('class="card card-primary card-outline"', admin_html)
        self.assertNotIn("el-dialog", admin_html)
        hidden = dict(values)
        hidden["can_add"] = False
        hidden["can_edit"] = False
        hidden["can_reset"] = False
        hidden["can_remove"] = False
        hidden["can_import"] = False
        hidden["can_export"] = False
        hidden["can_choose"] = False
        hidden["show_import"] = False
        hidden["can_depts"] = False
        hidden["user_name"] = "operator"
        locked = dict(values["rows"][0])
        locked["status_post"] = False
        hidden["rows"] = [locked]
        operator = self.engine.render_document("users", hidden)
        self.assertNotIn("Add a user", operator)
        self.assertNotIn(">Add<", operator)
        self.assertNotIn(">Import<", operator)
        self.assertNotIn(">Export<", operator)
        self.assertNotIn(">Choose<", operator)
        self.assertNotIn('aria-label="check all"', operator)
        self.assertNotIn("user-btn-import", operator)
        self.assertNotIn("user-btn-export", operator)
        self.assertNotIn('action="/users/add"', operator)
        self.assertNotIn('action="/users/import"', operator)
        self.assertNotIn('action="/users/edit"', operator)
        self.assertNotIn('action="/users/reset"', operator)
        self.assertNotIn('action="/users/remove"', operator)
        self.assertNotIn('action="/users/status"', operator)
        self.assertNotIn('form="user-status-2"', operator)
        self.assertIn('class="el-switch is-checked is-disabled"', operator)
        self.assertIn('class="el-switch__core"', operator)
        self.assertNotIn("user-org-manage", operator)
        self.assertIn(">Clerk<", operator)
        self.assertIn("@clerk", operator)
        self.assertIn('class="user-person-mark"', operator)
        self.assertIn(">CL<", operator)
        self.assertIn('class="font-medium truncate block"', operator)
        self.assertNotIn("hover:text-primary", operator)
        self.assertNotIn(">User id<", operator)
        themed_values = dict(values)
        themed_values["theme"] = "kero"
        themed_values["show_add"] = True
        themed = self.engine.render_document("users", themed_values)
        self.assertIn('href="/themes/kero.css"', themed)
        self.assertIn('class="user-person-mark"', themed)
        self.assertIn(">CL<", themed)
        self.assertNotIn("element-plus.css", themed)
        self.assertNotIn("openrbac.css", themed)
        self.assertIn('action="/users/add"', themed)
        self.assertIn('class="nav-link active"', themed)
        self.assertIn('class="card card-primary card-outline"', themed)
        self.assertNotIn("el-dialog", themed)
        themed_at = [themed.index(">{0}<".format(label)) for label in labels]
        self.assertEqual(themed_at, sorted(themed_at))
        self.assertIn('class="table-check-col"', themed)
        assert_only_check_script(self, themed)
        self.assertNotIn("<iframe", themed.lower())
        self.assertNotIn("font-awesome", themed.lower())
        root = Path(__file__).resolve().parents[1]
        for name in ("apex.css",):
            skin = (root / "src" / "OpenRbac" / "element_plus" / name).read_text(encoding="utf-8")
            self.assertIn("user-btn-import::before", skin, name)
            self.assertIn("user-btn-export::before", skin, name)
            self.assertIn("user-btn-add::before", skin, name)
            self.assertIn("user-btn-edit::before", skin, name)
            self.assertIn("user-btn-remove::before", skin, name)
            self.assertIn("user-btn-search::before", skin, name)
            self.assertIn("user-btn-reset::before", skin, name)
            self.assertIn("user-btn-resetpwd::before", skin, name)
            self.assertIn("user-node-branch", skin, name)
            self.assertIn("user-node-leaf", skin, name)
            self.assertIn(".el-switch__core", skin, name)
            self.assertIn(".el-switch__input:checked", skin, name)
            self.assertIn(".table-check", skin, name)
            self.assertIn(".table-check-col", skin, name)
            self.assertIn("text-align: center", skin, name)
            self.assertIn(".user-edit-float", skin, name)
            self.assertIn(".dept-float", skin, name)
            self.assertIn(".job-tag", skin, name)
            self.assertIn(".user-btn-close", skin, name)
            self.assertIn(".user-person-mark", skin, name)
            self.assertIn(".min-w-0", skin, name)
            self.assertIn(".text-muted-foreground", skin, name)
            self.assertIn(".hover\\:text-primary:hover", skin, name)
            self.assertIn("dept-open:checked", skin, name)
            self.assertIn("job-open:checked", skin, name)
            self.assertNotIn(":has(", skin, name)
            self.assertIn('url("/icons/user-upload.svg")', skin, name)
            self.assertIn('url("/icons/user-folder.svg")', skin, name)
            self.assertIn('url("/icons/user-plus.svg")', skin, name)
            self.assertNotIn("data:image", skin, name)
            self.assertNotIn("font-awesome", skin, name)

    def test_roles_page_is_the_role_management_screen(self):
        """requirement-html-role-management — AC-1 through AC-8."""
        from OpenRbac.web_app import WebApp

        class Gate:
            def allows(self, user_id, perm):
                return True

        app = WebApp(None, Gate(), None, None)
        groups = {}
        for group in app._nav({"user_id": 1}):
            groups[group["label"]] = [item["href"] for item in group["items"]]
        self.assertIn("/roles", groups["Access"])
        values = {
            "title": "Roles",
            "error": "",
            "user_name": "admin",
            "csrf": "token",
            "path": "/roles",
            "nav_groups": app._nav({"user_id": 1}),
            "rows": [
                {
                    "role_id": 1,
                    "role_name": "Super administrator",
                    "role_key": "admin",
                    "role_sort": 1,
                    "scope_label": "All data",
                    "scope_type": "success",
                    "status": "0",
                    "status_label": "Enabled",
                    "status_next": "1",
                    "status_form": "role-status-1",
                    "status_post": False,
                    "created": "2026-10-14 00:00:00",
                    "edit_action": False,
                    "remove_action": False,
                    "scope_action": False,
                    "edit_href": "/roles?form=edit&role_id=1",
                    "remove_href": "/roles?form=remove&role_id=1",
                    "scope_href": "/roles?form=scope&role_id=1",
                },
                {
                    "role_id": 2,
                    "role_name": "Common",
                    "role_key": "common",
                    "role_sort": 2,
                    "scope_label": "This department",
                    "scope_type": "warning",
                    "status": "0",
                    "status_label": "Enabled",
                    "status_next": "1",
                    "status_form": "role-status-2",
                    "status_post": True,
                    "created": "2026-10-14 00:00:00",
                    "edit_action": True,
                    "remove_action": True,
                    "scope_action": True,
                    "edit_href": "/roles?form=edit&role_id=2",
                    "remove_href": "/roles?form=remove&role_id=2",
                    "scope_href": "/roles?form=scope&role_id=2",
                },
            ],
            "count_line": "Showing 1 to 2 of 2 records",
            "query_role_name": "",
            "query_role_key": "",
            "query_state": "",
            "query_begin": "",
            "query_end": "",
            "state_all": True,
            "state_on": False,
            "state_off": False,
            "can_add": True,
            "can_edit": True,
            "can_remove": True,
            "can_export": True,
            "can_choose": True,
            "add_href": "/roles?form=add",
            "export_href": "/roles/export",
            "show_add": False,
            "show_edit": False,
            "show_remove": False,
            "show_scope": False,
            "menus": [],
            "scope_menus": [],
            "scope_1": True,
            "scope_2": False,
            "scope_3": False,
            "scope_4": False,
            "edit_role_id": "",
            "edit_name": "",
            "edit_key": "",
            "edit_sort": "",
            "edit_status": "0",
            "edit_remark": "",
            "remove_role_id": "",
            "remove_name": "",
            "scope_role_id": "",
            "scope_name": "",
            "scope_key": "",
            "scope_dept": "",
        }
        html = self.engine.render_document("roles", values)
        self.assertIn('class="admlte-date-range"', html)
        self.assertNotIn(">From<", html)
        self.assertNotIn(">To<", html)
        self.assertIn('type="date" name="begin"', html)
        self.assertIn('type="date" name="end"', html)
        self.assertIn('aria-hidden="true">→<', html)
        self.assertNotIn("max=", html)
        self.assertNotIn("min=", html)
        labels = (
            "Role id",
            "Role name",
            "Permission key",
            "Data scope",
            "Display order",
            "Status",
            "Created",
            "Action",
        )
        spots = [html.index(">{0}<".format(label)) for label in labels]
        self.assertEqual(spots, sorted(spots))
        self.assertIn('aria-label="check all"', html)
        self.assertIn('class="table-check" type="checkbox" name="role_id"', html)
        self.assertNotIn(">Choose<", html)
        self.assertNotIn('type="radio" name="role_id"', html)
        self.assertLess(html.index('aria-label="check all"'), html.index(">Role id<"))
        self.assertIn('class="table-check-col"', html)
        self.assertIn('class="table-check-col"', html)
        table_at = html.index('<table class="table table-bordered table-striped">')
        thead_at = html.index("<thead>", table_at)
        tbody_at = html.index("<tbody>", thead_at)
        self.assertNotIn("<table", html[thead_at:tbody_at])
        self.assertLess(html.index('class="role-work"'), html.index('class="role-count"'))
        self.assertLess(html.index('class="role-count"'), html.index('action="/roles/status"'))
        for piece in (
            "Role name",
            "Permission key",
            "Status",
            "Created",
            ">Search<",
            ">Reset<",
            ">Add<",
            ">Edit<",
            ">Remove<",
            ">Export<",
            ">More<",
            ">Data scope<",
            "All data",
            "This department",
            'class="user-btn user-btn-search"',
            'class="user-btn user-btn-reset"',
            'class="user-btn user-btn-add"',
            'class="user-btn user-btn-edit"',
            'class="user-btn user-btn-remove"',
            'class="user-btn user-btn-export"',
            'class="user-btn user-btn-more"',
            'class="el-tag el-tag--success"',
            'class="el-tag el-tag--warning"',
            'class="el-switch',
            'class="el-switch__core"',
            "Showing 1 to 2 of 2 records",
            'form="role-status-2"',
            'id="role-status-1"',
            'action="/roles/status"',
            'href="/roles"',
            'method="post"',
            'action="/logout"',
            'name="csrf"',
            ">admin<",
            ">common<",
            "Super administrator",
        ):
            self.assertIn(piece, html)
        self.assertNotIn('form="role-status-1"', html)
        self.assertNotIn("form=edit&amp;role_id=1", html)
        self.assertNotIn("menu_id", html)
        self.assertNotIn("Add a role", html)
        self.assertNotIn('action="/roles/add"', html)
        lowered = html.lower()
        for banned in (
            "<iframe",
            "<style",
            "bootstrap.min.css",
            "jquery",
            "font-awesome",
        ):
            self.assertNotIn(banned, lowered)
        assert_only_check_script(self, html)
        opened = dict(values)
        opened["show_add"] = True
        opened["show_edit"] = True
        opened["menus"] = [
            {"menu_id": 100, "menu_name": "User", "perms": "system:user:list", "checked": True},
        ]
        opened["edit_role_id"] = "2"
        opened["edit_name"] = "Common"
        opened["edit_key"] = "common"
        opened["edit_sort"] = "2"
        opened["edit_status"] = "0"
        forms = self.engine.render_document("roles", opened)
        self.assertIn("Add a role", forms)
        self.assertIn('action="/roles/add"', forms)
        self.assertIn("Edit a role", forms)
        self.assertIn('action="/roles/edit"', forms)
        self.assertIn(" checked", forms)
        self.assertIn('class="card card-primary card-outline"', forms)
        scoped = dict(values)
        scoped["show_scope"] = True
        scoped["scope_3"] = True
        scoped["scope_1"] = False
        scoped["scope_menus"] = [{"menu_id": 100}]
        scoped["scope_role_id"] = "2"
        scoped["scope_name"] = "Common"
        scoped["scope_key"] = "common"
        scope_html = self.engine.render_document("roles", scoped)
        self.assertIn("Data scope", scope_html)
        self.assertIn('action="/roles/grant"', scope_html)
        self.assertIn('name="menu_id"', scope_html)
        self.assertNotIn("el-tree", scope_html)
        self.assertNotIn("el-checkbox", scope_html)
        hidden = dict(values)
        hidden["can_add"] = False
        hidden["can_edit"] = False
        hidden["can_remove"] = False
        hidden["can_export"] = False
        hidden["can_choose"] = False
        hidden["show_add"] = False
        hidden["user_name"] = "clerk"
        hidden["rows"] = [dict(values["rows"][1])]
        hidden["rows"][0]["edit_action"] = False
        hidden["rows"][0]["remove_action"] = False
        hidden["rows"][0]["scope_action"] = False
        hidden["rows"][0]["status_post"] = False
        locked = self.engine.render_document("roles", hidden)
        for piece in (
            ">Add<",
            ">Edit<",
            ">Remove<",
            ">Export<",
            ">More<",
            ">Choose<",
            'aria-label="check all"',
            'action="/roles/add"',
            'action="/roles/status"',
        ):
            self.assertNotIn(piece, locked)
        self.assertIn('class="el-switch is-checked is-disabled"', locked)
        themed = dict(opened)
        themed["theme"] = "kero"
        themed_html = self.engine.render_document("roles", themed)
        self.assertIn('href="/themes/kero.css"', themed_html)
        self.assertNotIn("element-plus.css", themed_html)
        self.assertIn('action="/roles/add"', themed_html)
        self.assertIn('class="card card-primary card-outline"', themed_html)
        self.assertNotIn("el-dialog", themed_html)
        themed_at = [themed_html.index(">{0}<".format(label)) for label in labels]
        self.assertEqual(themed_at, sorted(themed_at))
        self.assertIn('class="table-check-col"', themed_html)
        assert_only_check_script(self, themed_html)
        root = Path(__file__).resolve().parents[1]
        icon = (root / "src" / "OpenRbac" / "element_plus" / "icons" / "user-more.svg").read_text(
            encoding="utf-8"
        )
        self.assertIn("<svg", icon)
        self.assertNotIn("<script", icon.lower())
        for name in ("apex.css",):
            skin = (root / "src" / "OpenRbac" / "element_plus" / name).read_text(encoding="utf-8")
            self.assertIn("user-btn-more::before", skin, name)
            self.assertIn('url("/icons/user-more.svg")', skin, name)
            self.assertIn(".role-page", skin, name)
            self.assertNotIn("data:image", skin, name)

    def test_online_page_is_the_online_screen(self):
        """requirement-html-online — AC-1 through AC-7, AC-9, and AC-10."""
        import re
        from OpenRbac.web_app import WebApp

        sessions = [
            {
                "token": "e947a8d6-full-token-value",
                "user_id": 1,
                "user_name": "admin",
                "ipaddr": "127.0.0.1",
                "surface": "web-surface",
                "user_agent": "Firefox 156.0",
                "csrf": "secret-csrf",
                "login_time": "2026-10-14 21:21:38",
                "last_access": "2026-10-14 22:44:11",
            },
            {
                "token": "bbbbbbbb-other-token",
                "user_id": 2,
                "user_name": "operator",
                "ipaddr": "10.0.0.8",
                "surface": "cli-surface",
                "user_agent": "curl",
                "csrf": "other-csrf",
                "login_time": "2026-10-14 20:00:00",
                "last_access": "2026-10-14 21:00:00",
            },
        ]
        labels = [
            "Number",
            "Session",
            "Login name",
            "Host",
            "Session status",
            "Login time",
            "Last access",
        ]
        nav = {
            "system:user:list",
            "system:role:list",
            "system:menu:list",
            "system:dept:list",
            "system:jobtitle:list",
            "system:config:list",
            "system:dict:list",
            "system:notice:list",
            "monitor:operlog:list",
            "monitor:logininfor:list",
            "monitor:online:list",
            "system:config:edit",
        }

        class Theme:
            def __init__(self, name):
                self.name = name

            def theme(self):
                return self.name

        class Gate:
            def __init__(self, allowed):
                self.allowed = allowed

            def allows(self, user_id, perm):
                return perm in self.allowed

        class Sessions:
            def __init__(self, rows):
                self.rows = rows

            def online_list(self, actor):
                return list(self.rows)

        def page(query, allowed, theme="apex", rows=None):
            app = WebApp(Theme(theme), Gate(allowed), Sessions(rows or sessions), None)
            app._request.path = "/online"
            app._request.query = query
            return app.online_page(
                {"user_id": 1, "user_name": "admin", "csrf": "page-csrf"},
                "",
            )

        html = page({}, nav | {"monitor:online:forceLogout"})
        spots = [html.index(">{0}<".format(label)) for label in labels + ["Action"]]
        self.assertEqual(spots, sorted(spots))
        for piece in (
            "Login address",
            "Login name",
            "Search",
            "Reset",
            "user-btn-search",
            "user-btn-reset",
            "Force logout",
            'class="el-tag el-tag--success"',
            ">Online<",
            "Showing 1 to 2 of 2 records",
            'method="get"',
            'action="/online"',
            'method="post"',
            'action="/online/logout"',
            'name="csrf"',
            'name="token"',
            "btn-danger",
            'action="/logout"',
            'class="online-page"',
            'class="nav-link active"',
            'href="/online"',
        ):
            self.assertIn(piece, html)
        self.assertIn(">e947a8d6<", html)
        self.assertIn(">bbbbbbbb<", html)
        self.assertLess(html.index(">e947a8d6<"), html.index(">bbbbbbbb<"))
        self.assertIn("Force logout e947a8d6", html)
        self.assertIn('value="e947a8d6-full-token-value"', html)
        self.assertNotIn(">e947a8d6-full-token-value<", html)
        self.assertNotIn("secret-csrf", html)
        self.assertNotIn("Firefox 156.0", html)
        self.assertNotIn("web-surface", html)
        self.assertNotIn("cli-surface", html)
        self.assertNotIn('type="checkbox"', html)
        self.assertNotIn("el-switch", html)
        self.assertNotIn("<iframe", html.lower())
        self.assertNotIn("<script", html.lower())
        self.assertNotIn("bootstrap.min.css", html)
        self.assertNotIn("jquery", html.lower())
        self.assertNotIn("font-awesome", html)
        for banned in (
            ">Department<",
            "Login location",
            ">Browser<",
            "Operating system",
            ">Surface<",
            "在线用户",
            "强退",
        ):
            self.assertNotIn(banned, html)
        self.assertRegex(
            html,
            r'class="nav-link active" href="/online">Online</a>',
        )
        self.assertIn('class="nav-link">admin<', html)
        named = page({"user_name": ["admin"]}, nav | {"monitor:online:forceLogout"})
        self.assertIn(">e947a8d6<", named)
        self.assertNotIn(">bbbbbbbb<", named)
        self.assertNotIn(">operator<", named)
        self.assertIn("Showing 1 to 1 of 1 records", named)
        self.assertIn('value="admin"', named)
        self.assertIn('class="nav-link">admin<', named)
        self.assertIn('class="user-btn user-btn-reset" href="/online"', named)
        empty = page({"user_name": ["not-a-session"]}, nav | {"monitor:online:forceLogout"})
        self.assertIn("Showing 0 to 0 of 0 records", empty)
        self.assertNotIn("Force logout", empty)
        upper = page({"user_name": ["Admin"]}, nav | {"monitor:online:forceLogout"})
        self.assertIn("Showing 0 to 0 of 0 records", upper)
        host = page({"ipaddr": ["10.0.0"]}, nav | {"monitor:online:forceLogout"})
        self.assertIn(">operator<", host)
        self.assertIn(">bbbbbbbb<", host)
        self.assertNotIn(">e947a8d6<", host)
        self.assertIn("Showing 1 to 1 of 1 records", host)
        self.assertIn('class="nav-link">admin<', host)
        blank = page({}, nav | {"monitor:online:forceLogout"}, rows=[{
            "token": "short",
            "user_name": "admin",
            "ipaddr": None,
            "login_time": None,
            "last_access": None,
        }])
        self.assertIn(">short<", blank)
        self.assertIn("Force logout short", blank)
        self.assertIn('value="short"', blank)
        self.assertNotIn(">None<", blank)
        listed = page({}, {"monitor:online:list"})
        kept = [listed.index(">{0}<".format(label)) for label in labels]
        self.assertEqual(kept, sorted(kept))
        self.assertNotIn('action="/online/logout"', listed)
        self.assertNotIn("Force logout", listed)
        self.assertNotIn(">Action<", listed)
        themed = page({}, nav | {"monitor:online:forceLogout"}, theme="kero")
        themed_spots = [themed.index(">{0}<".format(label)) for label in labels]
        self.assertEqual(themed_spots, sorted(themed_spots))
        self.assertIn("btn-danger", themed)
        self.assertIn('href="/themes/kero.css"', themed)
        self.assertNotIn("/element-plus.css", themed)
        self.assertNotIn("/openrbac.css", themed)
        self.assertIn('class="nav-link active" href="/online"', themed)
        self.assertIsNone(re.search(r"<style", html, re.IGNORECASE))

    def test_pages_are_embedded_html(self):
        """Pages are templates in the package. There is no frontend build.

        requirement-python-html-template — AC-8 and AC-9.
        requirement-python-project-structure — no frontend or backend tree.
        """
        root = Path(__file__).resolve().parents[1]
        banned_dirs = {"frontend", "backend"}
        banned_files = {"package.json", "vite.config.js"}
        for path in root.rglob("*"):
            if path.is_dir() and path.name in banned_dirs:
                self.fail("unexpected directory {0}".format(path))
            if path.is_file() and path.name in banned_files:
                self.fail("unexpected build file {0}".format(path))
        package = root / "src" / "OpenRbac"
        for name in ("main.js", "permission.js", "router", "store", "api"):
            self.assertFalse(
                (package / name).exists(),
                "reference runtime was copied: {0}".format(name),
            )
        pages = {
            "configs.vue",
            "database.vue",
            "dept-choice.vue",
            "depts.vue",
            "dicts.vue",
            "document.vue",
            "home.vue",
            "login-log.vue",
            "login.vue",
            "menus.vue",
            "message.vue",
            "notices.vue",
            "online.vue",
            "oper-log.vue",
            "job-titles.vue",
            "roles.vue",
            "shell.vue",
            "ui-menu.vue",
            "user-node.vue",
            "users.vue",
        }
        templates = package / "templates"
        found = {path.name for path in templates.glob("*.vue")}
        self.assertEqual(pages, found)
        for path in templates.glob("*.vue"):
            text = path.read_text(encoding="utf-8").lower()
            self.assertIn("<template", text, path.name)
            self.assertNotIn("<script", text, path.name)
            self.assertNotIn("<style", text, path.name)
        for path in package.rglob("*.py"):
            for line in path.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if not (
                    stripped.startswith("import ") or stripped.startswith("from ")
                ):
                    continue
                low = stripped.lower()
                for name in ("vue", "pinia", "axios"):
                    self.assertNotIn(
                        name,
                        low,
                        "{0} imports {1}".format(path.name, name),
                    )
        web = (package / "web_app.py").read_text(encoding="utf-8").lower()
        self.assertNotIn("application/json", web)
        self.assertNotIn("json.dumps", web)

    def test_menus_page_is_the_menu_tree(self):
        """The menu page is a search row, a toolbar, and a tree table."""
        from OpenRbac.web_app import WebApp

        sample = [
            {"menu_id": 1, "parent_id": 0, "menu_name": "System", "menu_type": "M",
             "perms": "", "order_num": 1, "path": "system", "visible": "0"},
            {"menu_id": 100, "parent_id": 1, "menu_name": "User", "menu_type": "C",
             "perms": "system:user:list", "order_num": 1, "path": "user", "visible": "0"},
            {"menu_id": 1001, "parent_id": 100, "menu_name": "User query", "menu_type": "F",
             "perms": "system:user:query", "order_num": 1, "path": "", "visible": "0"},
            {"menu_id": 101, "parent_id": 1, "menu_name": "Role", "menu_type": "C",
             "perms": "system:role:list", "order_num": 2, "path": "role", "visible": "1"},
            {"menu_id": 2, "parent_id": 0, "menu_name": "Setup", "menu_type": "M",
             "perms": None, "order_num": 2, "path": "setup", "visible": "0"},
        ]

        class Theme:
            def __init__(self, name):
                self.name = name

            def theme(self):
                return self.name

        class Gate:
            def __init__(self, rows, allowed):
                self.rows = rows
                self.allowed = allowed

            def menu_list(self, actor):
                return self.rows

            def allows(self, user_id, perm):
                return perm in self.allowed

        def page(query, allowed, theme="apex"):
            app = WebApp(Theme(theme), Gate(sample, allowed), None, None)
            app._request.path = "/menus"
            app._request.query = query
            return app.menus_page(
                {"user_id": 1, "user_name": "admin", "csrf": "tok"},
                "",
            )

        labels = ["Menu name", "Sort", "Path", "Type", "Visible", "Permission", "Action"]
        html = page({}, {"system:menu:list", "system:menu:add"})
        spots = [html.index(">{0}<".format(label)) for label in labels]
        self.assertEqual(spots, sorted(spots))
        self.assertIn(">System<", html)
        self.assertIn(">Setup<", html)
        self.assertNotIn(">User<", html)
        self.assertNotIn(">User query<", html)
        self.assertNotIn(">Role<", html)
        self.assertIn("menu-depth-0", html)
        self.assertNotIn("menu-depth-1", html)
        self.assertNotIn("menu-depth-2", html)
        self.assertIn("menu-twist is-shut", html)
        self.assertNotIn("menu-twist is-open", html)
        self.assertIn(">Directory<", html)
        self.assertIn(">Show<", html)
        self.assertIn(">Hide</option>", html)
        self.assertNotIn("menu-tag-hide", html)
        self.assertNotIn(">#<", html)
        self.assertNotIn("system:user:list", html)
        self.assertIn("menu-tag-dir", html)
        self.assertNotIn("menu-tag-button", html)
        self.assertIn("menu-btn-add", html)
        self.assertIn("menu-btn-fold", html)
        self.assertIn(">Expand/Collapse<", html)
        self.assertIn("closed=open", html)
        self.assertIn("closed=100", html)
        self.assertNotIn('name="closed"', html)
        self.assertNotIn('name="keep_closed"', html)
        opened = page({"closed": ["open"]}, {"system:menu:list", "system:menu:add"})
        names = ["System", "User", "User query", "Role", "Setup"]
        order = [opened.index(">{0}<".format(name)) for name in names]
        self.assertEqual(order, sorted(order))
        self.assertIn("menu-depth-0", opened)
        self.assertIn("menu-depth-1", opened)
        self.assertIn("menu-depth-2", opened)
        self.assertIn("menu-twist is-open", opened)
        self.assertNotIn("menu-twist is-shut", opened)
        self.assertIn(">Menu<", opened)
        self.assertIn(">Button<", opened)
        self.assertIn(">Hide<", opened)
        self.assertIn("menu-tag-hide", opened)
        self.assertIn(">#<", opened)
        self.assertIn("system:user:list", opened)
        self.assertIn("menu-tag-button", opened)
        self.assertIn("closed=1%2C100", opened)
        self.assertIn('name="closed" value="open"', opened)
        one = page({"closed": ["100"]}, {"system:menu:list", "system:menu:add"})
        self.assertIn(">System<", one)
        self.assertIn(">User<", one)
        self.assertIn(">Role<", one)
        self.assertNotIn(">User query<", one)
        self.assertIn("menu-twist is-open", one)
        self.assertIn("menu-twist is-shut", one)
        self.assertIn('name="closed" value="100"', one)
        self.assertIn("closed=1%2C100", one)
        self.assertIn('class="menu-sort"', html)
        self.assertIn("readonly", html)
        self.assertNotIn('name="order_num"', html)
        self.assertNotIn(">Choose<", html)
        self.assertNotIn('aria-label="check all"', html)
        self.assertNotIn(">Edit<", html)
        self.assertNotIn(">Save sort<", html)
        self.assertNotIn(">Remove<", html)
        self.assertIn('href="/menus"', html)
        self.assertIn("user-btn-search", html)
        self.assertIn("user-btn-reset", html)
        self.assertNotIn("Add a menu", html)
        self.assertNotIn('action="/menus/add"', html)
        self.assertNotIn("<script", html.lower())
        self.assertNotIn("<iframe", html.lower())
        self.assertNotIn("font-awesome", html.lower())
        folded = page({"closed": ["1"]}, {"system:menu:list", "system:menu:add"})
        self.assertIn("menu-twist is-shut", folded)
        self.assertIn(">System<", folded)
        self.assertIn(">Setup<", folded)
        self.assertNotIn(">User<", folded)
        self.assertNotIn(">Role<", folded)
        found = page({"menu_name": ["Role"]}, {"system:menu:list", "system:menu:add"})
        self.assertIn(">System<", found)
        self.assertIn(">Role<", found)
        self.assertNotIn(">User<", found)
        self.assertNotIn(">Setup<", found)
        hidden = page({"state": ["1"]}, {"system:menu:list", "system:menu:add"})
        self.assertIn(">Role<", hidden)
        self.assertIn(">Hide<", hidden)
        self.assertNotIn(">User<", hidden)
        shown = page({"state": ["0"]}, {"system:menu:list", "system:menu:add"})
        self.assertIn(">User<", shown)
        self.assertNotIn(">Role<", shown)
        adding = page(
            {"form": ["add"], "parent_id": ["100"]},
            {"system:menu:list", "system:menu:add"},
        )
        self.assertIn("Add a menu", adding)
        self.assertIn('action="/menus/add"', adding)
        self.assertIn('value="100" selected', adding)
        self.assertNotIn('value="0" selected', adding)
        self.assertIn('name="csrf"', adding)
        denied = page({"form": ["add"]}, {"system:menu:list"})
        self.assertNotIn(">Add<", denied)
        self.assertNotIn(">Edit<", denied)
        self.assertNotIn(">Save sort<", denied)
        self.assertNotIn(">Remove<", denied)
        self.assertNotIn('action="/menus/add"', denied)
        self.assertNotIn('action="/menus/edit"', denied)
        self.assertNotIn('action="/menus/remove"', denied)
        self.assertNotIn('action="/menus/sort"', denied)
        self.assertIn(">Expand/Collapse<", denied)
        full = {
            "system:menu:list",
            "system:menu:add",
            "system:menu:edit",
            "system:menu:remove",
        }
        managed_labels = [
            "Menu name", "Sort", "Path", "Type", "Visible", "Permission", "Action",
        ]
        managed = page({}, full)
        managed_at = [managed.index(">{0}<".format(label)) for label in managed_labels]
        self.assertEqual(managed_at, sorted(managed_at))
        self.assertIn('aria-label="check all"', managed)
        self.assertIn('class="table-check" type="checkbox" name="menu_id"', managed)
        self.assertNotIn(">Choose<", managed)
        self.assertLess(managed.index('aria-label="check all"'), managed_at[0])
        self.assertIn('class="table-check-col"', managed)
        self.assertIn('class="table-check-col"', managed)
        self.assertIn(">Edit<", managed)
        self.assertIn(">Save sort<", managed)
        self.assertIn(">Remove<", managed)
        self.assertIn("menu-btn-edit", managed)
        self.assertIn("menu-btn-sort", managed)
        self.assertIn("user-btn-edit", managed)
        self.assertIn("user-btn-remove", managed)
        self.assertIn('id="menu-sort"', managed)
        self.assertIn('action="/menus/sort"', managed)
        self.assertIn('form="menu-sort"', managed)
        self.assertIn('name="order_num"', managed)
        self.assertIn('name="menu_id"', managed)
        self.assertNotIn("readonly", managed)
        self.assertNotIn("Edit a menu", managed)
        self.assertNotIn("Remove a menu", managed)
        assert_only_check_script(self, managed)
        editing = page({"form": ["edit"], "menu_id": ["100"]}, full)
        self.assertIn("Edit a menu", editing)
        self.assertIn('action="/menus/edit"', editing)
        self.assertIn('value="User"', editing)
        self.assertIn('value="C" checked', editing)
        self.assertIn('value="0" checked', editing)
        self.assertIn('value="1" selected', editing)
        self.assertNotIn('value="0" selected', editing)
        self.assertIn('value="system:user:list"', editing)
        self.assertIn('value="user"', editing)
        self.assertIn('name="visible"', editing)
        self.assertIn('name="csrf"', editing)
        bare = page({"form": ["edit"]}, full)
        self.assertIn("Choose a menu.", bare)
        self.assertNotIn("Edit a menu", bare)
        self.assertNotIn('action="/menus/edit"', bare)
        missing = page({"form": ["remove"], "menu_id": ["99999"]}, full)
        self.assertIn("That menu is not in this list.", missing)
        self.assertNotIn("Remove a menu", missing)
        removing = page(
            {"form": ["remove"], "menu_id": ["1001"], "menu_name": ["query"]},
            full,
        )
        self.assertIn("Remove a menu", removing)
        self.assertIn('action="/menus/remove"', removing)
        self.assertIn(">User query<", removing)
        self.assertIn("menu_name=query", removing)
        self.assertIn("menu_id=1001", removing)
        locked = page(
            {"form": ["remove"], "menu_id": ["1001"]},
            {"system:menu:list", "system:menu:add"},
        )
        self.assertNotIn("Remove a menu", locked)
        self.assertNotIn('action="/menus/remove"', locked)
        themed = page({}, {"system:menu:list", "system:menu:add"}, theme="kero")
        themed_at = [themed.index(">{0}<".format(label)) for label in labels]
        self.assertEqual(themed_at, sorted(themed_at))
        self.assertIn("main-sidebar", themed)
        self.assertNotIn("/element-plus.css", themed)
        self.assertNotIn("<script", themed.lower())
        themed_full = page({}, full, theme="kero")
        themed_at_full = [themed_full.index(">{0}<".format(label)) for label in managed_labels]
        self.assertEqual(themed_at_full, sorted(themed_at_full))
        self.assertLess(themed_full.index('aria-label="check all"'), themed_at_full[0])
        self.assertIn('class="table-check-col"', themed_full)
        self.assertIn(">Save sort<", themed_full)
        self.assertIn('action="/menus/sort"', themed_full)
        self.assertIn("main-sidebar", themed_full)
        self.assertNotIn("/element-plus.css", themed_full)
        assert_only_check_script(self, themed_full)
        root = Path(__file__).resolve().parents[1]
        for name in ("apex.css",):
            skin = (root / "src" / "OpenRbac" / "element_plus" / name).read_text(encoding="utf-8")
            self.assertIn("menu-tag-dir", skin, name)
            self.assertIn("menu-btn-fold::before", skin, name)
            self.assertIn("menu-btn-edit", skin, name)
            self.assertIn("menu-btn-sort::before", skin, name)
            self.assertIn('url("/icons/menu-fold.svg")', skin, name)
            self.assertIn('url("/icons/menu-page.svg")', skin, name)
            self.assertIn('url("/icons/menu-save.svg")', skin, name)
            self.assertIn('url("/icons/user-folder.svg")', skin, name)
            self.assertNotIn("data:image", skin, name)
        for name in ("menu-fold.svg", "menu-page.svg", "menu-save.svg"):
            icon = (root / "src" / "OpenRbac" / "element_plus" / "icons" / name).read_text(
                encoding="utf-8",
            )
            self.assertIn("<svg", icon)
            self.assertNotIn("<script", icon.lower())

    def test_configs_page_is_parameter_management(self):
        """requirement-html-parameter-management — AC-1 through AC-10."""
        from OpenRbac.access import AccessError
        from OpenRbac.web_app import WebApp

        rows = [
            {"config_id": 1, "config_name": "Skin name", "config_key": "sys.index.skinName",
             "config_value": "skin-blue", "config_type": "Y", "remark": None,
             "create_time": "2026-10-14 12:00:00"},
            {"config_id": 2, "config_name": "Initial password", "config_key": "sys.user.initPassword",
             "config_value": "123456", "config_type": "Y", "remark": "",
             "create_time": "2026-10-14 12:00:00"},
            {"config_id": 3, "config_name": "Captcha", "config_key": "sys.account.captchaEnabled",
             "config_value": "false", "config_type": "Y", "remark": None,
             "create_time": "2026-10-14 12:00:00"},
            {"config_id": 4, "config_name": "Registration", "config_key": "sys.account.registerUser",
             "config_value": "false", "config_type": "Y", "remark": None,
             "create_time": "2026-10-14 12:00:00"},
        ]

        class Theme:
            def __init__(self, name):
                self.name = name

            def theme(self):
                return self.name

        class Gate:
            def __init__(self, allowed):
                self.allowed = allowed
                self.access = self

            def config_list(self, actor):
                if "system:config:list" not in self.allowed:
                    raise AccessError("Missing permission system:config:list.", "ask")
                return rows

            def allows(self, user_id, perm):
                return perm in self.allowed

            def require(self, actor, perm):
                if perm not in self.allowed:
                    raise AccessError("Missing permission {0}.".format(perm), "ask")
                return actor

        def page(query, allowed, theme="apex"):
            gate = Gate(allowed)
            app = WebApp(Theme(theme), gate, gate, None)
            app._request.path = "/configs"
            app._request.query = query
            return app.configs_page(
                {"user_id": 1, "user_name": "admin", "csrf": "tok"},
                "",
            )

        labels = [
            "Parameter id", "Parameter name", "Parameter key", "Parameter value",
            "Built-in", "Remark", "Created", "Action",
        ]
        admin = {"system:config:list", "system:config:edit"}
        html = page({}, admin)
        spots = [html.index(">{0}<".format(label)) for label in labels]
        self.assertEqual(spots, sorted(spots))
        self.assertIn('class="admlte-date-range"', html)
        self.assertNotIn(">From<", html)
        self.assertNotIn(">To<", html)
        self.assertIn('type="date" name="begin"', html)
        self.assertIn('type="date" name="end"', html)
        self.assertIn('aria-hidden="true">→<', html)
        self.assertNotIn("max=", html)
        self.assertNotIn("min=", html)
        self.assertLess(html.index('aria-label="check all"'), spots[0])
        self.assertIn('class="table-check" type="checkbox" name="config_id"', html)
        self.assertIn('class="table-check-col"', html)
        self.assertIn('class="table-check-col"', html)
        self.assertNotIn(">Choose<", html)
        self.assertNotIn('type="radio"', html)
        for piece in (
            "Parameter name", "Parameter key", "Built-in", "Created",
            "Search", "Reset", "Change",
            "user-btn-search", "user-btn-reset", "user-btn-edit",
            "Skin name", "sys.index.skinName", "skin-blue",
            "Initial password", "sys.user.initPassword", "123456",
            "Captcha", "Registration",
            'class="el-tag el-tag--success"', "Yes",
            "Showing 1 to 4 of 4 records",
            'href="/configs"', "admin",
            'method="post"', 'action="/logout"', 'name="csrf"',
        ):
            self.assertIn(piece, html)
        self.assertLess(html.index("sys.index.skinName"), html.index("sys.user.initPassword"))
        self.assertIn("nav-link active", html)
        self.assertNotIn('action="/configs/set"', html)
        self.assertNotIn("Change a parameter", html)
        self.assertNotIn('action="/configs/add"', html)
        self.assertNotIn("el-switch", html)
        assert_only_check_script(self, html)
        self.assertNotIn("<iframe", html.lower())
        self.assertNotIn("<style", html.lower())
        self.assertNotIn("bootstrap.min.css", html.lower())
        self.assertNotIn("jquery", html.lower())
        self.assertNotIn("font-awesome", html.lower())
        self.assertNotIn("参数设置", html)
        self.assertNotIn("修改参数", html)
        self.assertNotIn(">Add<", html)
        self.assertNotIn(">Delete<", html)
        self.assertNotIn(">Export<", html)
        self.assertNotIn(">Refresh cache<", html)
        self.assertIn('class="user-btn user-btn-reset" href="/configs"', html)
        narrowed = page({"config_key": ["initPassword"]}, admin)
        self.assertIn("sys.user.initPassword", narrowed)
        self.assertNotIn("sys.index.skinName", narrowed)
        named = page({"config_name": ["Captcha"]}, admin)
        self.assertIn("Captcha", named)
        self.assertNotIn("Initial password", named)
        self.assertIn(">admin<", named)
        for query in (
            {"config_type": ["N"]},
            {"begin": ["2999-01-01"]},
            {"begin": ["yesterday"]},
        ):
            empty = page(query, admin)
            self.assertIn("Showing 0 to 0 of 0 records", empty)
        kept = page({"begin": ["2020-01-01"]}, admin)
        self.assertIn("Showing 1 to 4 of 4 records", kept)
        editing = page({"form": ["edit"], "config_id": ["2"]}, admin)
        self.assertIn("Change a parameter", editing)
        self.assertIn('action="/configs/set"', editing)
        self.assertIn('name="config_value"', editing)
        self.assertIn("<textarea", editing)
        self.assertIn("123456", editing)
        self.assertIn("Initial password", editing)
        start = editing.index('action="/configs/set"')
        form = editing[editing.rfind("<form", 0, start):editing.index("</form>", start)]
        self.assertNotIn('name="config_name"', form)
        self.assertNotIn('name="config_type"', form)
        self.assertNotIn('name="remark"', form)
        self.assertIn('name="config_key"', form)
        self.assertIn('name="config_value"', form)
        missing = page({"form": ["edit"]}, admin)
        self.assertIn("Choose a parameter.", missing)
        self.assertNotIn('action="/configs/set"', missing)
        unknown = page({"form": ["edit"], "config_id": ["99"]}, admin)
        self.assertIn("Unknown parameter", unknown)
        self.assertNotIn('action="/configs/set"', unknown)
        operator = page({"form": ["edit"], "config_id": ["2"]}, {"system:config:list"})
        for key in (
            "sys.index.skinName", "sys.user.initPassword",
            "sys.account.captchaEnabled", "sys.account.registerUser",
        ):
            self.assertIn(key, operator)
        self.assertNotIn("Change a parameter", operator)
        self.assertNotIn("user-btn-edit", operator)
        self.assertNotIn(">Choose<", operator)
        self.assertNotIn('aria-label="check all"', operator)
        self.assertNotIn('type="checkbox"', operator)
        self.assertNotIn('action="/configs/set"', operator)
        gate = Gate(set())
        app = WebApp(Theme("apex"), gate, gate, None)
        app._request.path = "/configs"
        app._request.query = {}
        with self.assertRaises(AccessError) as refused:
            app._route_get("/configs", {"user_id": 4, "user_name": "lead"}, "")
        self.assertIn("Missing permission", str(refused.exception))
        themed = page({}, admin, theme="kero")
        themed_at = [themed.index(">{0}<".format(label)) for label in labels]
        self.assertEqual(themed_at, sorted(themed_at))
        self.assertNotIn("/element-plus.css", themed)
        themed_edit = page({"form": ["edit"], "config_id": ["2"]}, admin, theme="kero")
        self.assertIn('action="/configs/set"', themed_edit)
        self.assertNotIn("/element-plus.css", themed_edit)

    def test_dicts_page_is_the_type_list(self):
        """The dictionaries page is the type list from the studied screen.

        requirement-html-dictionaries — AC-1 through AC-8 and AC-10.
        """
        from OpenRbac.web_app import WebApp

        types = [
            {"dict_id": 1, "dict_name": "User sex", "dict_type": "sys_user_sex",
             "status": "0", "remark": None, "create_time": "2020-06-01 08:00:00"},
            {"dict_id": 2, "dict_name": "Normal or disabled", "dict_type": "sys_normal_disable",
             "status": "0", "remark": None, "create_time": "2020-06-01 08:00:00"},
            {"dict_id": 3, "dict_name": "Notice type", "dict_type": "sys_notice_type",
             "status": "0", "remark": "", "create_time": "2020-06-01 08:00:00"},
        ]
        admin = {"system:dict:list", "system:dict:add"}
        labels = (
            "Dictionary id",
            "Dictionary name",
            "Dictionary type",
            "Status",
            "Remark",
            "Created",
        )

        class Theme:
            def __init__(self, name):
                self.name = name

            def theme(self):
                return self.name

        class Gate:
            def __init__(self, allowed):
                self.allowed = allowed

            def allows(self, user_id, perm):
                return perm in self.allowed

        class Shelf:
            def __init__(self, rows):
                self.rows = rows

            def dict_type_list(self, actor):
                return self.rows

        def page(query, allowed, theme="apex", rows=None):
            app = WebApp(
                Theme(theme),
                Gate(allowed),
                Shelf(types if rows is None else rows),
                None,
            )
            app._request.path = "/dicts"
            app._request.query = query
            return app.dicts_page(
                {"user_id": 1, "user_name": "admin", "csrf": "tok"},
                "",
            )

        html = page({}, admin)
        spots = [html.index(">{0}<".format(label)) for label in labels]
        self.assertEqual(spots, sorted(spots))
        self.assertIn('class="admlte-date-range"', html)
        self.assertNotIn(">From<", html)
        self.assertNotIn(">To<", html)
        self.assertIn('type="date" name="begin"', html)
        self.assertIn('type="date" name="end"', html)
        self.assertIn('aria-hidden="true">→<', html)
        self.assertNotIn("max=", html)
        self.assertNotIn("min=", html)
        self.assertIn('class="dict-page"', html)
        self.assertIn("Dictionary name", html)
        self.assertIn("Dictionary type", html)
        self.assertIn(">Search<", html)
        self.assertIn(">Reset<", html)
        self.assertIn("Add a dictionary value", html)
        self.assertIn("user-btn-search", html)
        self.assertIn("user-btn-reset", html)
        self.assertIn("user-btn-add", html)
        self.assertIn(">All<", html)
        self.assertIn(">Normal<", html)
        self.assertIn(">Disabled<", html)
        self.assertIn("User sex", html)
        self.assertIn("sys_user_sex", html)
        self.assertIn("Normal or disabled", html)
        self.assertIn("sys_normal_disable", html)
        self.assertIn("Notice type", html)
        self.assertIn("sys_notice_type", html)
        self.assertLess(html.index("User sex"), html.index("Notice type"))
        self.assertIn('class="el-tag el-tag--success"', html)
        self.assertIn("Showing 1 to 3 of 3 records", html)
        self.assertIn('href="/dicts"', html)
        self.assertIn('aria-current="page"', html)
        self.assertIn(">admin<", html)
        self.assertIn('class="user-btn user-btn-reset" href="/dicts"', html)
        self.assertNotIn('action="/dicts/add"', html)
        self.assertNotIn(">sys_user_sex</a>", html)
        self.assertNotIn("/system/dict", html)
        self.assertNotIn("el-switch", html)
        self.assertNotIn('type="checkbox"', html)
        self.assertNotIn("el-checkbox", html)
        for banned in (
            ">Edit<",
            ">Remove<",
            ">Export<",
            "Refresh cache",
            "修改类型",
            "用户性别",
            "菜单状态",
            "系统开关",
            "任务状态",
            "任务分组",
            "系统是否",
            "通知类型",
            "通知状态",
            "操作类型",
            "系统状态",
            "<iframe",
            "<script",
            "<style",
            "bootstrap.min.css",
            "jquery",
            "font-awesome",
        ):
            self.assertNotIn(banned, html)
        self.assertIn('method="post"', html)
        self.assertIn('action="/logout"', html)
        self.assertIn('name="csrf"', html)
        self.assertIn('method="get"', html)
        self.assertIn('action="/dicts"', html)
        narrowed = page({"dict_type": ["sys_user_sex"]}, admin)
        self.assertIn("User sex", narrowed)
        self.assertNotIn("Notice type", narrowed)
        self.assertIn(">admin<", narrowed)
        named = page({"dict_name": ["Notice"]}, admin)
        self.assertIn("Notice type", named)
        self.assertNotIn("User sex", named)
        self.assertIn("dict_name=Notice", named)
        self.assertIn("form=add", named)
        self.assertIn('class="user-btn user-btn-reset" href="/dicts"', named)
        for query in (
            {"status": ["1"]},
            {"begin": ["2999-01-01"]},
            {"begin": ["yesterday"]},
            {"dict_name": ["user"]},
        ):
            empty = page(query, admin)
            self.assertIn("Showing 0 to 0 of 0 records", empty, query)
        adding = page({"form": ["add"]}, admin)
        self.assertIn("Add a dictionary value", adding)
        self.assertIn('action="/dicts/add"', adding)
        self.assertIn('class="card card-primary card-outline"', adding)
        form_at = adding.index('action="/dicts/add"')
        form = adding[form_at:adding.index("</form>", form_at)]
        self.assertIn('name="dict_label"', form)
        self.assertIn('name="dict_value"', form)
        self.assertIn('name="dict_type"', form)
        self.assertIn('name="csrf"', form)
        self.assertNotIn('name="remark"', form)
        self.assertNotIn('name="dict_name"', form)
        plain = page({}, admin)
        self.assertNotIn('action="/dicts/add"', plain)
        locked = page({"form": ["add"]}, {"system:dict:list"})
        self.assertNotIn("Add a dictionary value", locked)
        self.assertNotIn('action="/dicts/add"', locked)
        self.assertNotIn("user-btn-add", locked)
        stopped = page({}, admin, rows=[{
            "dict_id": 9,
            "dict_name": "Paused",
            "dict_type": "sys_paused",
            "status": "1",
            "remark": None,
            "create_time": "2020-06-01 08:00:00",
        }])
        self.assertIn('class="el-tag el-tag--info"', stopped)
        self.assertIn(">Disabled<", stopped)
        self.assertNotIn("el-tag--success", stopped)
        themed = page({}, admin, theme="kero")
        themed_at = [themed.index(">{0}<".format(label)) for label in labels]
        self.assertEqual(themed_at, sorted(themed_at))
        self.assertNotIn("/element-plus.css", themed)
        self.assertIn('href="/themes/kero.css"', themed)
        self.assertIn('class="nav-link active" href="/dicts"', themed)
        themed_add = page({"form": ["add"]}, admin, theme="kero")
        self.assertIn('action="/dicts/add"', themed_add)
        self.assertIn("card-primary", themed_add)
        self.assertNotIn("el-dialog", themed_add)
        self.assertNotIn("<script", themed_add.lower())

    def test_date_range_is_one_line_without_from_or_to(self):
        """requirement-html-date-range — AC-1 through AC-7."""
        root = Path(__file__).resolve().parents[1]
        templates = root / "src" / "OpenRbac" / "templates"
        created = (templates / "date-range.vue").read_text(encoding="utf-8")
        self.assertIn('class="admlte-date-range"', created)
        self.assertNotIn(">From<", created)
        self.assertNotIn(">To<", created)
        self.assertNotIn("<label", created)
        self.assertNotIn("<script", created.lower())
        self.assertNotIn("x-data", created)
        self.assertNotIn("x-model", created)
        for name in ("users.vue", "roles.vue", "configs.vue", "dicts.vue"):
            text = (templates / name).read_text(encoding="utf-8")
            self.assertIn("<date-range>Created </date-range>", text)
        login = (templates / "login-log.vue").read_text(encoding="utf-8")
        self.assertIn("<date-range>Login time </date-range>", login)

        def paint(begin, end):
            return self.engine.render_source(
                "<template><date-range>Created </date-range></template>",
                {"query_begin": begin, "query_end": end},
            )

        empty = paint("", "")
        self.assertIn('class="admlte-date-range"', empty)
        self.assertNotIn(">From<", empty)
        self.assertNotIn(">To<", empty)
        self.assertNotIn("<label", empty)
        self.assertIn('id="admlte-date-from" type="date" name="begin" value=""', empty)
        self.assertIn('id="admlte-date-to" type="date" name="end" value=""', empty)
        self.assertIn('class="admlte-date-range-arrow" aria-hidden="true">→<', empty)
        self.assertNotIn("max=", empty)
        self.assertNotIn("min=", empty)
        self.assertNotIn(">Created<", empty)
        self.assertIn("Created ", empty)
        self.assertNotIn("x-data", empty)
        self.assertNotIn("el-date-picker", empty)
        both = paint("2026-04-01", "2026-04-30")
        self.assertIn('value="2026-04-01" max="2026-04-30"', both)
        self.assertIn('value="2026-04-30" min="2026-04-01"', both)
        start_only = paint("2026-04-01", "")
        self.assertIn('min="2026-04-01"', start_only)
        self.assertNotIn("max=", start_only)
        end_only = paint("", "2026-04-30")
        self.assertIn('max="2026-04-30"', end_only)
        self.assertNotIn("min=", end_only)
        titled = self.engine.render_source(
            "<template><date-range>Login time </date-range></template>",
            {"query_begin": "", "query_end": ""},
        )
        self.assertNotIn(">Login time<", titled)
        self.assertIn("Login time ", titled)
        for sheet in ("apex.css",):
            css = (root / "src" / "OpenRbac" / "element_plus" / sheet).read_text(encoding="utf-8")
            self.assertIn(".admlte-date-range {", css)
            self.assertIn(".admlte-date-range-pair {", css)
            arrow = css.split(".admlte-date-range-arrow {", 1)[1].split("}", 1)[0]
            field = css.split('.admlte-date-range input[type="date"]', 1)[1].split("}", 1)[0]
            self.assertIn("height: 30px", arrow)
            self.assertIn("height: 30px", field)
