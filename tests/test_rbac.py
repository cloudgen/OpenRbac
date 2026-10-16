# RBAC, database, environment, web, and ChronicleLogger.
# Uses the openrbac_test schema. Does not write ruoyi_db or ry.
import http.client
import io
import os
import re
import sys
import tempfile
import unittest
import urllib.parse
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from OpenRbac.access import AccessError
from OpenRbac.cli import Cli, main
from OpenRbac.desk import Desk
from OpenRbac.tui import Tui
from OpenRbac.password_hash import PasswordHash
from OpenRbac.schema import Schema
from OpenRbac.settings import Settings, SettingsError
from OpenRbac.web_app import WebApp


TABLE_CHECK_SCRIPT = '<script src="/table-check.js"></script>'
CSP = (
    "default-src 'none'; style-src 'self' 'unsafe-inline'; "
    "script-src 'self'; img-src 'self' data:; form-action 'self'"
)


def assert_only_check_script(test, html):
    """A document with a table checkbox loads only /table-check.js."""
    if 'class="table-check' in html:
        test.assertEqual(html.count(TABLE_CHECK_SCRIPT), 1)
        test.assertNotIn("<script", html.replace(TABLE_CHECK_SCRIPT, "").lower())
    else:
        test.assertNotIn("<script", html.lower())


ROOT = Path(__file__).resolve().parents[1]
TABLES = (
    "sys_user_role",
    "sys_user_job_title",
    "sys_role_menu",
    "sys_role_dept",
    "sys_oper_log",
    "sys_logininfor",
    "sys_session",
    "sys_notice",
    "sys_dict_data",
    "sys_dict_type",
    "sys_config",
    "sys_user",
    "sys_role",
    "sys_menu",
    "sys_dept",
    "sys_job_title",
)


def _password_from_file():
    path = Path.home() / ".local" / "OpenRbac" / "database"
    if not path.is_file():
        raise unittest.SkipTest("database file is absent")
    mode = path.stat().st_mode & 0o777
    if mode != 0o600:
        raise unittest.SkipTest("database file is not mode 0600")
    found = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("OPENRBAC_DB_PASSWORD="):
            found = line.split("=", 1)[1]
    if not found:
        raise unittest.SkipTest("database file has no password")
    return found


def _drop_tables(store):
    for name in TABLES:
        store.execute("DROP TABLE IF EXISTS {0}".format(name))


def _names(text):
    rows = []
    for line in text.splitlines()[1:]:
        if line == "(none)":
            return []
        rows.append(line.split("|")[1])
    return rows


class TestEnvironment(unittest.TestCase):
    """OPENRBAC_* defaults, the 0600 file, and the loopback bind."""

    def test_password_file_mode_and_remote_refusal(self):
        home = tempfile.mkdtemp(prefix="openrbac_env_", dir="/tmp")
        path = Path(home) / "database"
        path.write_text("OPENRBAC_DB_PASSWORD=from-file\n", encoding="utf-8")
        os.chmod(path, 0o644)
        loose = {
            "OPENRBAC_HOME": home,
            "HOME": home,
            "OPENRBAC_DB_PASSWORD": "",
        }
        self.assertEqual(Settings(environ=loose).password(), "")
        os.chmod(path, 0o600)
        self.assertEqual(Settings(environ=loose).password(), "from-file")
        env_wins = dict(loose)
        env_wins["OPENRBAC_DB_PASSWORD"] = "from-env"
        self.assertEqual(Settings(environ=env_wins).password(), "from-env")
        remote = {"OPENRBAC_BIND": "0.0.0.0", "OPENRBAC_PORT": "8765"}
        with self.assertRaises(SettingsError) as caught:
            Settings(environ=remote).bind()
        self.assertIn("Refusing to listen", str(caught.exception))
        remote["OPENRBAC_ALLOW_REMOTE"] = "yes"
        self.assertEqual(Settings(environ=remote).bind()[0], "0.0.0.0")
        self.assertEqual(Settings(environ={}).bind(), ("127.0.0.1", 8765))


class TestPasswordHash(unittest.TestCase):
    def test_pbkdf2_round_trip(self):
        hasher = PasswordHash()
        stored = hasher.hash("admin123")
        self.assertTrue(stored.startswith("pbkdf2_sha256$"))
        self.assertTrue(hasher.verify("admin123", stored))
        self.assertFalse(hasher.verify("admin123", "not-this-scheme"))
        self.assertFalse(hasher.verify("other", stored))


class TestRbacDatabase(unittest.TestCase):
    """Seed, data scope, and permissions on the sqlite3 file."""

    @classmethod
    def setUpClass(cls):
        cls.home = tempfile.mkdtemp(prefix="openrbac_home_", dir="/tmp")
        cls.sqlite_file = os.path.join(cls.home, "openrbac.sqlite3")
        cls._saved = {
            name: os.environ.get(name)
            for name in (
                "OPENRBAC_HOME",
                "OPENRBAC_DB_ENGINE",
                "OPENRBAC_SQLITE_FILE",
                "OPENRBAC_DB_NAME",
                "OPENRBAC_DB_PASSWORD",
                "OPENRBAC_BIND",
                "OPENRBAC_PORT",
                "OPENRBAC_ALLOW_REMOTE",
            )
        }
        os.environ["OPENRBAC_HOME"] = cls.home
        os.environ["OPENRBAC_DB_ENGINE"] = "sqlite3"
        os.environ["OPENRBAC_SQLITE_FILE"] = cls.sqlite_file
        os.environ.pop("OPENRBAC_DB_PASSWORD", None)
        os.environ["OPENRBAC_BIND"] = "127.0.0.1"
        os.environ["OPENRBAC_PORT"] = "0"
        os.environ.pop("OPENRBAC_ALLOW_REMOTE", None)
        cls.desk = Desk()
        _drop_tables(cls.desk.store)
        cls.assert_seed = cls.desk.db_init()

    @classmethod
    def tearDownClass(cls):
        web = cls.desk.web()
        if web.httpd is not None:
            web.stop()
        for name, value in cls._saved.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value

    def setUp(self):
        self.desk.sessions.clear()

    def test_run_initializes_when_tables_are_missing(self):
        def run(argv):
            app = Cli()
            from io import StringIO
            from contextlib import redirect_stderr, redirect_stdout
            out = StringIO()
            err = StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = app.run(argv)
            return code, out.getvalue(), err.getvalue()

        _drop_tables(self.desk.store)
        try:
            code, out, err = run(["user-list"])
            self.assertEqual(code, 1, err)
            self.assertIn("Not signed in", err)
            count = self.desk.store.query_one("SELECT COUNT(*) AS n FROM sys_user")
            self.assertEqual(int(count["n"]), 4)
            admins = self.desk.store.query_one(
                "SELECT COUNT(*) AS n FROM sys_user WHERE user_name = 'admin'"
            )
            self.assertEqual(int(admins["n"]), 1)
            _drop_tables(self.desk.store)
            note = self.desk.serve_background()
            self.assertIn("http://127.0.0.1:", note)
            count = self.desk.store.query_one("SELECT COUNT(*) AS n FROM sys_user")
            self.assertEqual(int(count["n"]), 4)
            code, out, err = run([
                "login", "--user-name", "admin", "--password", Schema.INITIAL_ADMIN_PASSWORD,
            ])
            self.assertEqual(code, 0, err)
            self.assertIn("Signed in as admin", out)
            code, out, err = run(["db-init"])
            self.assertEqual(code, 0, err)
            self.assertIn("present", out)
            self.assertNotIn("seeded", out)
        finally:
            web = self.desk.web()
            if web.httpd is not None:
                web.stop()
            self.desk.db_init()

    def test_seed_once_and_scopes(self):
        self.assertIn("openrbac.sqlite3: seeded", self.assert_seed)
        self.assertNotIn("openrbac_test", self.assert_seed)
        self.assertNotIn("ruoyi_db", self.assert_seed)
        again = self.desk.db_init()
        self.assertIn("present", again)
        def run(argv):
            app = Cli()
            from io import StringIO
            from contextlib import redirect_stderr, redirect_stdout
            out = StringIO()
            err = StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = app.run(argv)
            return code, out.getvalue(), err.getvalue()

        code, out, err = run([
            "login", "--user-name", "admin", "--password", Schema.INITIAL_ADMIN_PASSWORD,
        ])
        self.assertEqual(code, 0, err)
        self.assertIn("Signed in as admin", out)
        code, out, err = run(["whoami"])
        self.assertIn("admin=yes", out)
        code, out, err = run(["user-list"])
        names = _names(out)
        self.assertEqual(names, ["admin", "operator", "clerk", "lead"])
        code, out, err = run([
            "login", "--user-name", "operator", "--password", Schema.INITIAL_OPERATOR_PASSWORD,
        ])
        self.assertEqual(code, 0, err)
        code, out, err = run(["user-list"])
        self.assertEqual(_names(out), ["operator"])
        code, out, err = run([
            "user-add", "--user-name", "extra", "--nick-name", "Extra",
            "--dept-id", "102", "--role-id", "2",
        ])
        self.assertEqual(code, 1)
        self.assertIn("Missing permission", err)
        code, out, err = run(["config-set", "--config-key", "sys.user.initPassword", "--config-value", "nope"])
        self.assertEqual(code, 1)
        self.assertIn("Missing permission", err)
        code, out, err = run([
            "login", "--user-name", "lead", "--password", Schema.INITIAL_LEAD_PASSWORD,
        ])
        self.assertEqual(code, 0, err)
        code, out, err = run(["user-list"])
        self.assertEqual(_names(out), ["admin", "clerk", "lead"])
        code, out, err = run([
            "login", "--user-name", "clerk", "--password", Schema.INITIAL_CLERK_PASSWORD,
        ])
        self.assertEqual(code, 0, err)
        code, out, err = run(["user-list"])
        self.assertEqual(_names(out), ["clerk"])
        self.desk.store.execute("UPDATE sys_role SET data_scope = '5' WHERE role_id = 2")
        try:
            code, out, err = run(["user-list"])
            self.assertEqual(code, 0, err)
            self.assertEqual(_names(out), [])
        finally:
            self.desk.store.execute("UPDATE sys_role SET data_scope = '3' WHERE role_id = 2")
        code, out, err = run([
            "login", "--user-name", "admin", "--password", Schema.INITIAL_ADMIN_PASSWORD,
        ])
        self.assertEqual(code, 0, err)
        code, out, err = run(["user-remove", "--user-id", "1"])
        self.assertEqual(code, 1)
        self.assertIn("cannot be removed", err)
        code, out, err = run(["user-edit", "--user-id", "1", "--status", "1"])
        self.assertEqual(code, 1)
        self.assertIn("stays enabled", err)
        code, out, err = run(["role-grant", "--role-id", "1", "--menu-ids", "1", "--data-scope", "3"])
        self.assertEqual(code, 1)
        self.assertIn("not edited", err)
        code, out, err = run(["logout"])
        self.assertEqual(code, 0, err)
        code, out, err = run([
            "login", "--user-name", "missing", "--password", "admin123",
        ])
        self.assertEqual(code, 1)
        self.assertIn("Unknown account or wrong password", err)
        code, out, err = run(["notice-list"])
        self.assertEqual(code, 1)
        self.assertIn("Not signed in", err)

    def test_present_database_copies_posts_into_job_titles(self):
        """An empty sys_job_title is filled from sys_post. The old names change.

        requirement-database — AC-7.
        """
        store = self.desk.store
        saved = store.query_all(
            """
            SELECT job_title_id, job_title_code, job_title, job_title_sort, status, create_by
            FROM sys_job_title
            """
        )
        saved_links = store.query_all(
            "SELECT user_id, job_title_id FROM sys_user_job_title"
        )
        try:
            store.execute("DROP TABLE IF EXISTS sys_user_post")
            store.execute("DROP TABLE IF EXISTS sys_post")
            store.execute(
                """
                CREATE TABLE sys_post (
                  post_id INTEGER PRIMARY KEY,
                  post_code VARCHAR(64) NOT NULL,
                  post_name VARCHAR(50) NOT NULL,
                  post_sort INT NOT NULL,
                  status CHAR(1) NOT NULL DEFAULT '0',
                  create_by VARCHAR(64) NOT NULL DEFAULT '',
                  create_time DATETIME,
                  update_by VARCHAR(64) NOT NULL DEFAULT '',
                  update_time DATETIME,
                  remark VARCHAR(500)
                )
                """
            )
            store.execute(
                """
                CREATE TABLE sys_user_post (
                  user_id BIGINT NOT NULL,
                  post_id BIGINT NOT NULL,
                  PRIMARY KEY (user_id, post_id)
                )
                """
            )
            store.execute("DELETE FROM sys_user_job_title")
            store.execute("DELETE FROM sys_job_title")
            store.execute(
                """
                INSERT INTO sys_post
                  (post_id, post_code, post_name, post_sort, status, create_by, remark)
                VALUES (1, 'ceo', 'Chief', 1, '0', 'schema', 'from post')
                """
            )
            store.execute(
                """
                INSERT INTO sys_post
                  (post_id, post_code, post_name, post_sort, status, create_by)
                VALUES (2, 'se', 'Engineer', 2, '0', 'schema')
                """
            )
            store.execute(
                "INSERT INTO sys_user_post (user_id, post_id) VALUES (2, 1)"
            )
            note = self.desk.db_init()
            self.assertIn("present", note)
            rows = store.query_all(
                """
                SELECT job_title_id, job_title_code, job_title, job_title_sort, remark
                FROM sys_job_title ORDER BY job_title_id
                """
            )
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["job_title_code"], "ceo")
            self.assertEqual(rows[0]["job_title"], "Chief")
            self.assertEqual(int(rows[0]["job_title_sort"]), 1)
            self.assertEqual(rows[0]["remark"], "from post")
            self.assertEqual(rows[1]["job_title_code"], "se")
            self.assertEqual(rows[1]["job_title"], "Engineer")
            link = store.query_one(
                "SELECT job_title_id FROM sys_user_job_title WHERE user_id = 2"
            )
            self.assertEqual(int(link["job_title_id"]), 1)
            again = self.desk.db_init()
            self.assertIn("present", again)
            count = store.query_one("SELECT COUNT(*) AS n FROM sys_job_title")
            self.assertEqual(int(count["n"]), 2)
        finally:
            store.execute("DROP TABLE IF EXISTS sys_user_post")
            store.execute("DROP TABLE IF EXISTS sys_post")
            store.execute("DELETE FROM sys_user_job_title")
            store.execute("DELETE FROM sys_job_title")
            for row in saved:
                store.execute(
                    """
                    INSERT INTO sys_job_title
                      (job_title_id, job_title_code, job_title, job_title_sort, status,
                       create_by, create_time)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW())
                    """,
                    (
                        row["job_title_id"],
                        row["job_title_code"],
                        row["job_title"],
                        row["job_title_sort"],
                        row["status"],
                        row["create_by"],
                    ),
                )
            for row in saved_links:
                store.execute(
                    "INSERT INTO sys_user_job_title (user_id, job_title_id) VALUES (%s, %s)",
                    (row["user_id"], row["job_title_id"]),
                )

    def test_user_list_filters_and_departments(self):
        """requirement-rbac-users — AC-7 and AC-8. Filters narrow the same list."""
        access = self.desk.access
        admin = access.user_by_id(1)
        self.assertEqual(
            [row["user_name"] for row in access.user_list(admin)],
            ["admin", "operator", "clerk", "lead"],
        )
        self.assertEqual(
            [row["user_name"] for row in access.user_list(admin, {"user_name": "clerk"})],
            ["clerk"],
        )
        self.assertEqual(
            [row["user_name"] for row in access.user_list(admin, {"user_name": "%clerk%"})],
            ["clerk"],
        )
        self.assertEqual(
            [row["user_name"] for row in access.user_list(admin, {"dept_id": 101})],
            ["admin", "clerk", "lead"],
        )
        self.assertEqual(
            [row["user_name"] for row in access.user_list(admin, {"dept_id": 102})],
            ["operator"],
        )
        self.assertEqual(access.user_list(admin, {"phonenumber": "555"}), [])
        self.assertEqual(len(access.user_list(admin, {"status": "0"})), 4)
        self.assertEqual(access.user_list(admin, {"status": "1"}), [])
        with self.assertRaises(AccessError) as caught:
            access.user_list(admin, {"begin_time": "yesterday"})
        self.assertIn("YYYY-MM-DD", str(caught.exception))
        self.assertEqual(
            [row["dept_name"] for row in access.user_departments(admin)],
            ["Group", "Engineering", "Operations", "Platform"],
        )
        operator = access.user_by_id(2)
        self.assertEqual(
            [row["dept_name"] for row in access.user_departments(operator)],
            ["Group", "Operations"],
        )
        lead = access.user_by_id(4)
        self.assertEqual(
            [row["dept_name"] for row in access.user_departments(lead)],
            ["Group", "Engineering", "Platform"],
        )

    def test_user_import_and_export(self):
        """requirement-rbac-users — AC-9. A csv adds an account and the export omits the password."""
        access = self.desk.access
        admin = access.user_by_id(1)
        operator = access.user_by_id(2)

        def drop(user_name):
            row = self.desk.store.query_one(
                "SELECT user_id FROM sys_user WHERE user_name = %s",
                (user_name,),
            )
            if row is None:
                return
            self.desk.store.execute(
                "DELETE FROM sys_user_role WHERE user_id = %s",
                (row["user_id"],),
            )
            self.desk.store.execute(
                "DELETE FROM sys_user WHERE user_id = %s",
                (row["user_id"],),
            )

        try:
            header = "user_name,nick_name,dept_id,role_id,password,phonenumber,status\n"
            result = access.user_import(admin, header + "pat,Pat,102,2,,5550001111,0\n", False)
            self.assertEqual(result, {"added": 1, "updated": 0})
            row = self.desk.store.query_one(
                """
                SELECT user_id, nick_name, phonenumber, password, status
                FROM sys_user WHERE user_name = %s
                """,
                ("pat",),
            )
            self.assertEqual(row["nick_name"], "Pat")
            self.assertEqual(row["phonenumber"], "5550001111")
            self.assertEqual(str(row["status"]), "0")
            self.assertTrue(access.passwords.verify("123456", row["password"]))
            linked = self.desk.store.query_one(
                "SELECT role_id FROM sys_user_role WHERE user_id = %s",
                (row["user_id"],),
            )
            self.assertEqual(int(linked["role_id"]), 2)
            log = self.desk.store.query_one(
                """
                SELECT title, business_type, method, oper_param
                FROM sys_oper_log WHERE method = 'user_import'
                ORDER BY oper_id DESC
                """
            )
            self.assertEqual(log["title"], "User")
            self.assertEqual(int(log["business_type"]), 1)
            self.assertEqual(log["oper_param"], "1 added, 0 updated")
            self.assertNotIn("123456", log["oper_param"])
            mixed = header + "sam,Sam,102,2,,,\npat,Changed,102,2,,,\n"
            with self.assertRaises(AccessError) as caught:
                access.user_import(admin, mixed, False)
            self.assertIn("already in use", str(caught.exception))
            self.assertIsNone(
                self.desk.store.query_one(
                    "SELECT user_id FROM sys_user WHERE user_name = %s AND del_flag = '0'",
                    ("sam",),
                )
            )
            self.assertEqual(
                self.desk.store.query_one(
                    "SELECT nick_name FROM sys_user WHERE user_name = %s",
                    ("pat",),
                )["nick_name"],
                "Pat",
            )
            updated = access.user_import(
                admin,
                "user_name,nick_name,dept_id,role_id\npat,Patrick,101,3\n",
                True,
            )
            self.assertEqual(updated, {"added": 0, "updated": 1})
            renamed = self.desk.store.query_one(
                "SELECT nick_name, dept_id FROM sys_user WHERE user_name = %s",
                ("pat",),
            )
            self.assertEqual(renamed["nick_name"], "Patrick")
            self.assertEqual(int(renamed["dept_id"]), 101)
            with self.assertRaises(AccessError) as blocked:
                access.user_import(
                    admin,
                    "user_name,nick_name,dept_id,role_id,status\nadmin,Root,101,1,1\n",
                    True,
                )
            self.assertIn("stays enabled", str(blocked.exception))
            kept = self.desk.store.query_one(
                "SELECT status, nick_name FROM sys_user WHERE user_id = 1"
            )
            self.assertEqual(str(kept["status"]), "0")
            self.assertEqual(kept["nick_name"], "Administrator")
            exported = access.user_export(admin, {"user_name": "pat"})
            self.assertTrue(
                exported.startswith("user_name,nick_name,dept_id,role_id,phonenumber,status\n")
            )
            self.assertIn("pat,Patrick,101,3", exported)
            self.assertNotIn("pbkdf2", exported)
            self.assertNotIn("123456", exported)
            self.assertNotIn("operator", exported)
            with self.assertRaises(AccessError) as denied:
                access.user_import(operator, header + "pat,Pat,102,2,,,\n", False)
            self.assertTrue(str(denied.exception).startswith("Missing permission"))
            with self.assertRaises(AccessError) as denied_export:
                access.user_export(operator)
            self.assertTrue(str(denied_export.exception).startswith("Missing permission"))
            self.assertEqual(
                self.desk.store.query_one(
                    "SELECT perms FROM sys_menu WHERE menu_id = 1006"
                )["perms"],
                "system:user:import",
            )
            self.assertEqual(
                self.desk.store.query_one(
                    "SELECT perms FROM sys_menu WHERE menu_id = 1007"
                )["perms"],
                "system:user:export",
            )
            self.assertIsNone(
                self.desk.store.query_one(
                    "SELECT menu_id FROM sys_role_menu WHERE role_id = 2 AND menu_id = 1006"
                )
            )
        finally:
            drop("pat")
            drop("sam")

    def test_menu_edit_remove_and_sort(self):
        """requirement-rbac-menu — edit, remove, and save sort stay off the typed verbs."""
        from OpenRbac.cli import Cli
        from OpenRbac.tui import Tui

        access = self.desk.access
        store = self.desk.store
        admin = access.user_by_id(1)
        operator = access.user_by_id(2)
        created = []
        self.assertNotIn("menu-edit", Cli.PRODUCT_VERBS)
        self.assertNotIn("menu-remove", Cli.PRODUCT_VERBS)
        self.assertNotIn("menu-sort", Cli.PRODUCT_VERBS)
        self.assertNotIn("menu-edit", Cli.DOMAIN_VERBS)
        self.assertNotIn("menu-remove", Cli.DOMAIN_VERBS)
        self.assertNotIn("menu-sort", Cli.DOMAIN_VERBS)
        self.assertNotIn("menu-edit", Tui.DOMAIN_KINDS)
        self.assertEqual(
            store.query_one("SELECT perms FROM sys_menu WHERE menu_id = 1022")["perms"],
            "system:menu:edit",
        )
        self.assertEqual(
            store.query_one("SELECT perms FROM sys_menu WHERE menu_id = 1023")["perms"],
            "system:menu:remove",
        )
        self.assertIsNone(
            store.query_one(
                "SELECT menu_id FROM sys_role_menu WHERE role_id = 2 AND menu_id = 1022"
            )
        )
        with self.assertRaises(AccessError) as denied:
            access.menu_edit(operator, 102, "Menu", 1, "C")
        self.assertTrue(str(denied.exception).startswith("Missing permission"))

        def add(name, parent, menu_type):
            menu_id = int(access.menu_add(admin, name, parent, menu_type, "", ""))
            created.append(menu_id)
            return menu_id

        try:
            parent = add("Sort parent", 0, "M")
            child = add("Sort child", parent, "C")
            leaf = add("Sort leaf", parent, "F")
            store.execute(
                "INSERT INTO sys_role_menu (role_id, menu_id) VALUES (2, %s)",
                (leaf,),
            )
            with self.assertRaises(AccessError) as blocked:
                access.menu_remove(admin, parent)
            self.assertEqual(str(blocked.exception), "That menu has children.")
            access.menu_edit(
                admin, child, "Sort renamed", parent, "C",
                "system:menu:renamed", "moved", "1",
            )
            row = store.query_one(
                """
                SELECT menu_name, parent_id, menu_type, perms, path, visible, order_num
                FROM sys_menu WHERE menu_id = %s
                """,
                (child,),
            )
            self.assertEqual(row["menu_name"], "Sort renamed")
            self.assertEqual(int(row["parent_id"]), parent)
            self.assertEqual(row["menu_type"], "C")
            self.assertEqual(row["perms"], "system:menu:renamed")
            self.assertEqual(row["path"], "moved")
            self.assertEqual(str(row["visible"]), "1")
            self.assertEqual(int(row["order_num"]), 0)
            edited = store.query_one(
                """
                SELECT title, business_type, method, oper_param
                FROM sys_oper_log WHERE method = 'menu_edit'
                ORDER BY oper_id DESC
                """
            )
            self.assertEqual(edited["title"], "Menu")
            self.assertEqual(int(edited["business_type"]), 2)
            self.assertEqual(edited["oper_param"], "Sort renamed")
            with self.assertRaises(AccessError) as cycle:
                access.menu_edit(admin, parent, "Sort parent", child, "M")
            self.assertEqual(str(cycle.exception), "A menu cannot sit under itself.")
            with self.assertRaises(AccessError) as itself:
                access.menu_edit(admin, parent, "Sort parent", parent, "M")
            self.assertEqual(str(itself.exception), "A menu cannot sit under itself.")
            with self.assertRaises(AccessError) as missing_parent:
                access.menu_edit(admin, parent, "Sort parent", 99999, "M")
            self.assertIn("Unknown parent menu", str(missing_parent.exception))
            with self.assertRaises(AccessError) as blank_type:
                access.menu_edit(admin, parent, "Sort parent", 0, "")
            self.assertEqual(str(blank_type.exception), "menu_type must be M, C, or F.")
            self.assertEqual(
                store.query_one(
                    "SELECT menu_type FROM sys_menu WHERE menu_id = %s",
                    (parent,),
                )["menu_type"],
                "M",
            )
            with self.assertRaises(AccessError) as bad_name:
                access.menu_edit(admin, parent, "", 0, "M")
            self.assertEqual(str(bad_name.exception), "menu_name is required.")
            with self.assertRaises(AccessError) as bad_visible:
                access.menu_edit(admin, parent, "Sort parent", 0, "M", visible="2")
            self.assertEqual(str(bad_visible.exception), "visible must be 0 or 1.")
            access.menu_edit(admin, leaf, "Sort leaf", parent, "F", visible="")
            self.assertEqual(
                str(store.query_one(
                    "SELECT visible FROM sys_menu WHERE menu_id = %s",
                    (leaf,),
                )["visible"]),
                "0",
            )
            with self.assertRaises(AccessError) as unknown:
                access.menu_edit(admin, 99999, "Missing", 0, "C")
            self.assertIn("Unknown menu", str(unknown.exception))
            store.execute("UPDATE sys_menu SET status = '1' WHERE menu_id = %s", (leaf,))
            with self.assertRaises(AccessError) as disabled:
                access.menu_remove(admin, leaf)
            self.assertIn("Unknown menu", str(disabled.exception))
            listed = [int(item["menu_id"]) for item in access.menu_list(admin)]
            self.assertNotIn(leaf, listed)
            store.execute("UPDATE sys_menu SET status = '0' WHERE menu_id = %s", (leaf,))
            before = int(store.query_one(
                "SELECT order_num FROM sys_menu WHERE menu_id = %s",
                (child,),
            )["order_num"])
            with self.assertRaises(AccessError) as bad_order:
                access.menu_sort(admin, [child], ["nope"])
            self.assertEqual(str(bad_order.exception), "order_num must be a number.")
            with self.assertRaises(AccessError) as too_big:
                access.menu_sort(admin, [child], ["10000"])
            self.assertEqual(str(too_big.exception), "order_num must be a number.")
            with self.assertRaises(AccessError) as mismatch:
                access.menu_sort(admin, [child, leaf], ["3"])
            self.assertEqual(str(mismatch.exception), "Choose a sort for each menu.")
            self.assertEqual(
                int(store.query_one(
                    "SELECT order_num FROM sys_menu WHERE menu_id = %s",
                    (child,),
                )["order_num"]),
                before,
            )
            access.menu_sort(admin, [child, leaf], ["", "4"])
            self.assertEqual(
                int(store.query_one(
                    "SELECT order_num FROM sys_menu WHERE menu_id = %s",
                    (child,),
                )["order_num"]),
                0,
            )
            self.assertEqual(
                int(store.query_one(
                    "SELECT order_num FROM sys_menu WHERE menu_id = %s",
                    (leaf,),
                )["order_num"]),
                4,
            )
            sorted_log = store.query_one(
                """
                SELECT title, business_type, method, oper_param
                FROM sys_oper_log WHERE method = 'menu_sort'
                ORDER BY oper_id DESC
                """
            )
            self.assertEqual(sorted_log["title"], "Menu")
            self.assertEqual(int(sorted_log["business_type"]), 2)
            self.assertEqual(sorted_log["oper_param"], "2")
            access.menu_sort(admin, [child], ["9999"])
            self.assertEqual(
                int(store.query_one(
                    "SELECT order_num FROM sys_menu WHERE menu_id = %s",
                    (child,),
                )["order_num"]),
                9999,
            )
            access.menu_remove(admin, leaf)
            self.assertIsNone(store.query_one(
                "SELECT menu_id FROM sys_menu WHERE menu_id = %s",
                (leaf,),
            ))
            self.assertIsNone(store.query_one(
                "SELECT menu_id FROM sys_role_menu WHERE menu_id = %s",
                (leaf,),
            ))
            removed = store.query_one(
                """
                SELECT title, business_type, method, oper_param
                FROM sys_oper_log WHERE method = 'menu_remove'
                ORDER BY oper_id DESC
                """
            )
            self.assertEqual(removed["title"], "Menu")
            self.assertEqual(int(removed["business_type"]), 3)
            self.assertEqual(removed["oper_param"], "Sort leaf")
            with self.assertRaises(AccessError) as still:
                access.menu_remove(admin, parent)
            self.assertEqual(str(still.exception), "That menu has children.")
            access.menu_remove(admin, child)
            access.menu_remove(admin, parent)
            self.assertIsNone(store.query_one(
                "SELECT menu_id FROM sys_menu WHERE menu_id = %s",
                (parent,),
            ))
        finally:
            for menu_id in created:
                store.execute("DELETE FROM sys_role_menu WHERE menu_id = %s", (menu_id,))
                store.execute("DELETE FROM sys_menu WHERE menu_id = %s", (menu_id,))

    def test_user_role_management_page(self):
        """requirement-rbac-roles 1.1.0 and requirement-html-role-management."""
        access = self.desk.access
        store = self.desk.store
        admin = access.user_by_id(1)
        operator = access.user_by_id(2)
        self.assertEqual(
            [row["role_key"] for row in access.role_list(admin)],
            ["admin", "common", "lead"],
        )
        self.assertEqual(
            [row["role_key"] for row in access.role_list(admin, {"role_name": "Common"})],
            ["common"],
        )
        self.assertEqual(
            [row["role_key"] for row in access.role_list(admin, {"role_key": "lead"})],
            ["lead"],
        )
        with self.assertRaises(AccessError) as caught:
            access.role_list(admin, {"begin_time": "yesterday"})
        self.assertEqual(str(caught.exception), "The start date must be YYYY-MM-DD.")
        with self.assertRaises(AccessError) as caught:
            access.role_list(admin, {"status": "9"})
        self.assertIn("status must be 0 or 1.", str(caught.exception))
        report = self.desk.report.roles(access.role_list(admin))
        self.assertTrue(report.startswith("role_id|role_name|role_key|data_scope|status\n"))
        for call in (
            lambda: access.role_edit(admin, 1, role_name="Nope"),
            lambda: access.role_remove(admin, 1),
            lambda: access.role_edit(admin, 1, status="1"),
        ):
            with self.assertRaises(AccessError) as caught:
                call()
            self.assertIn("not edited", str(caught.exception))
        with self.assertRaises(AccessError) as caught:
            access.role_edit(admin, 2)
        self.assertIn("role-edit needs", str(caught.exception))
        with self.assertRaises(AccessError) as caught:
            access.role_edit(admin, 99999, status="0")
        self.assertIn("Unknown role", str(caught.exception))
        for menu_id, perm in (
            (1013, "system:role:add"),
            (1014, "system:role:remove"),
            (1015, "system:role:export"),
        ):
            self.assertEqual(
                store.query_one("SELECT perms FROM sys_menu WHERE menu_id = %s", (menu_id,))["perms"],
                perm,
            )
            self.assertIsNotNone(
                store.query_one(
                    "SELECT menu_id FROM sys_role_menu WHERE role_id = 1 AND menu_id = %s",
                    (menu_id,),
                )
            )
            self.assertIsNone(
                store.query_one(
                    "SELECT menu_id FROM sys_role_menu WHERE role_id = 2 AND menu_id = %s",
                    (menu_id,),
                )
            )
        with self.assertRaises(AccessError) as caught:
            access.role_add(operator, "Auditor", "auditor", "9")
        self.assertTrue(str(caught.exception).startswith("Missing permission"))
        with self.assertRaises(AccessError) as caught:
            access.role_export(operator)
        self.assertTrue(str(caught.exception).startswith("Missing permission"))
        note = self.desk.serve_background()
        url = note.splitlines()[0].split(": ", 1)[1]
        session = self._sign_in("admin", Schema.INITIAL_ADMIN_PASSWORD, url)
        page = self._open(url + "roles", session)
        self.assertEqual(page.status, 200)
        self.assertIn("Showing 1 to 3 of 3 records", page.body)
        self.assertIn("All data", page.body)
        self.assertIn('class="el-tag el-tag--success"', page.body)
        self.assertIn('class="el-switch', page.body)
        self.assertIn('class="el-switch__core"', page.body)
        self.assertIn('form="role-status-2"', page.body)
        self.assertNotIn('form="role-status-1"', page.body)
        self.assertIn(">admin<", page.body)
        self.assertNotIn("menu_id", page.body)
        self.assertNotIn("Add a role", page.body)
        self.assertNotIn('action="/roles/add"', page.body)
        self.assertNotIn("form=edit&amp;role_id=1", page.body)
        self.assertIn('class="user-btn user-btn-reset" href="/roles"', page.body)
        self.assertIn('method="post"', page.body)
        self.assertIn('action="/logout"', page.body)
        self.assertIn('name="csrf"', page.body)
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
        spots = [page.body.index(">{0}<".format(label)) for label in labels]
        self.assertEqual(spots, sorted(spots))
        narrow = self._open(url + "roles?role_name=Common", session)
        self.assertIn(">common<", narrow.body)
        self.assertNotIn(">lead<", narrow.body)
        self.assertNotIn(">Lead<", narrow.body)
        added = self._open(url + "roles?form=add", session)
        self.assertIn("Add a role", added.body)
        self.assertIn('action="/roles/add"', added.body)
        editing = self._open(url + "roles?form=edit&role_id=2", session)
        self.assertIn("Edit a role", editing.body)
        self.assertIn('action="/roles/edit"', editing.body)
        self.assertIn(" checked", editing.body)
        scope = self._open(url + "roles?form=scope&role_id=2", session)
        self.assertIn("Data scope", scope.body)
        self.assertIn('action="/roles/grant"', scope.body)
        self.assertIn('name="menu_id"', scope.body)
        self.assertNotIn("el-tree", scope.body)
        protected = self._open(url + "roles?form=edit&role_id=1", session)
        self.assertIn("The built-in administrator role is not edited here.", protected.body)
        self.assertNotIn('action="/roles/edit"', protected.body)
        choose = self._open(url + "roles?form=edit", session)
        self.assertIn("Choose a role.", choose.body)
        missing = self._open(url + "roles?form=remove&role_id=99999", session)
        self.assertIn("That role is not in this list.", missing.body)
        dated = self._open(url + "roles?begin=yesterday", session)
        self.assertEqual(dated.status, 400)
        self.assertIn("The start date must be YYYY-MM-DD.", dated.body)
        icon = self._open(url + "icons/user-more.svg", "")
        self.assertEqual(icon.status, 200)
        self.assertIn("image/svg+xml", icon.headers.get("Content-Type", ""))
        self.assertNotIn("<script", icon.body.lower())
        op = self._sign_in("operator", Schema.INITIAL_OPERATOR_PASSWORD, url)
        denied = self._open(url + "roles/export", op)
        self.assertEqual(denied.status, 403)
        self.assertIn("Missing permission", denied.body)
        csrf = re.search(r'name="csrf" value="([^"]+)"', page.body).group(1)
        created_id = None
        try:
            posted = self._post(url + "roles/add", session, {
                "csrf": csrf,
                "role_name": "Auditor",
                "role_key": "auditor",
                "role_sort": "9",
                "status": "0",
                "remark": "audit",
                "menu_id": "100",
            })
            self.assertIn(posted.status, (302, 303), posted.body)
            found = store.query_one(
                "SELECT role_id, data_scope, del_flag FROM sys_role WHERE role_key = %s",
                ("auditor",),
            )
            self.assertEqual(str(found["data_scope"]), "1")
            self.assertEqual(str(found["del_flag"]), "0")
            created_id = int(found["role_id"])
            with self.assertRaises(AccessError) as caught:
                access.role_add(admin, "Auditor", "auditor", "9")
            self.assertIn("That role_key is already in use.", str(caught.exception))
            access.role_grant(admin, created_id, [100], data_scope="2", dept_ids=[101])
            access.role_edit(admin, created_id, remark="kept")
            kept = store.query_one(
                "SELECT data_scope, remark, status FROM sys_role WHERE role_id = %s",
                (created_id,),
            )
            self.assertEqual(str(kept["data_scope"]), "2")
            self.assertEqual(kept["remark"], "kept")
            self.assertEqual(str(kept["status"]), "0")
            self.assertEqual(
                int(store.query_one(
                    "SELECT dept_id FROM sys_role_dept WHERE role_id = %s",
                    (created_id,),
                )["dept_id"]),
                101,
            )
            self.assertIsNotNone(
                store.query_one(
                    "SELECT menu_id FROM sys_role_menu WHERE role_id = %s AND menu_id = 100",
                    (created_id,),
                )
            )
            exported = access.role_export(admin, {"role_key": "auditor"})
            self.assertTrue(
                exported.startswith(
                    "role_id,role_name,role_key,data_scope,role_sort,status,create_time\n"
                )
            )
            self.assertIn("auditor", exported)
            self.assertNotIn("common", exported)
            download = self._open(url + "roles/export?role_key=auditor", session)
            self.assertEqual(download.status, 200)
            self.assertIn("text/csv", download.headers.get("Content-Type", ""))
            self.assertIn("roles.csv", download.headers.get("Content-Disposition", ""))
            self.assertIn("auditor", download.body)
            self.assertNotIn("<html", download.body.lower())
            flipped = self._post(url + "roles/status", session, {
                "csrf": csrf,
                "role_id": str(created_id),
                "status": "1",
                "role_name": "auditor",
            })
            self.assertIn(flipped.status, (302, 303), flipped.body)
            self.assertIn("role_name=auditor", flipped.headers.get("Location", ""))
            disabled = store.query_one(
                "SELECT status, data_scope FROM sys_role WHERE role_id = %s",
                (created_id,),
            )
            self.assertEqual(str(disabled["status"]), "1")
            self.assertEqual(str(disabled["data_scope"]), "2")
            blocked = self._post(url + "roles/status", session, {
                "csrf": csrf,
                "role_id": "1",
                "status": "1",
            })
            self.assertEqual(blocked.status, 400)
            self.assertIn("not edited", blocked.body)
            still = store.query_one("SELECT status FROM sys_role WHERE role_id = 1")
            self.assertEqual(str(still["status"]), "0")
            outside = self._post(url + "roles/status", session, {
                "csrf": csrf,
                "role_id": "99999",
                "status": "1",
            })
            self.assertEqual(outside.status, 400)
            self.assertIn("That role is not in this list.", outside.body)
            removed = self._post(url + "roles/remove", session, {
                "csrf": csrf,
                "role_id": str(created_id),
            })
            self.assertIn(removed.status, (302, 303), removed.body)
            gone = store.query_one(
                "SELECT del_flag FROM sys_role WHERE role_id = %s",
                (created_id,),
            )
            self.assertEqual(str(gone["del_flag"]), "2")
            self.assertIsNone(
                store.query_one(
                    "SELECT menu_id FROM sys_role_menu WHERE role_id = %s",
                    (created_id,),
                )
            )
            self.assertIsNone(
                store.query_one(
                    "SELECT dept_id FROM sys_role_dept WHERE role_id = %s",
                    (created_id,),
                )
            )
        finally:
            if created_id is not None:
                row = store.query_one(
                    "SELECT del_flag FROM sys_role WHERE role_id = %s",
                    (created_id,),
                )
                if row is not None and str(row["del_flag"]) == "0":
                    access.role_remove(admin, created_id)

    def test_web_login_csrf_and_scope(self):
        note = self.desk.serve_background()
        self.assertIn("http://127.0.0.1:", note)
        url = note.splitlines()[0].split(": ", 1)[1]
        admin = self._sign_in("admin", Schema.INITIAL_ADMIN_PASSWORD, url)
        page = self._open(url + "users", admin)
        self.assertEqual(page.status, 200)
        self.assertIn("Organization", page.body)
        self.assertIn("Login name", page.body)
        self.assertIn(">Search<", page.body)
        self.assertIn(">Add<", page.body)
        self.assertIn(">Edit<", page.body)
        self.assertIn(">Remove<", page.body)
        self.assertIn(">Import<", page.body)
        self.assertIn(">Export<", page.body)
        self.assertIn("user-btn-add", page.body)
        self.assertIn("user-btn-edit", page.body)
        self.assertIn("user-btn-remove", page.body)
        self.assertIn("user-btn-import", page.body)
        self.assertIn("user-btn-export", page.body)
        self.assertIn("user-btn-search", page.body)
        self.assertIn('class="user-tree"', page.body)
        self.assertIn("user-node-icon", page.body)
        self.assertIn("user-switch", page.body)
        self.assertIn("user-node-branch", page.body)
        self.assertIn("user-node-leaf", page.body)
        self.assertLess(page.body.index(">Group<"), page.body.index(">Engineering<"))
        self.assertLess(page.body.index(">Engineering<"), page.body.index(">Platform<"))
        self.assertLess(page.body.index(">Platform<"), page.body.index(">Operations<"))
        self.assertIn('aria-label="check all"', page.body)
        self.assertIn('type="checkbox" name="user_id"', page.body)
        self.assertNotIn(">Choose<", page.body)
        self.assertNotIn("font-awesome", page.body.lower())
        self.assertNotIn("Import users", page.body)
        self.assertIn("clerk", page.body)
        self.assertIn('class="user-person-mark"', page.body)
        self.assertIn(">AD<", page.body)
        self.assertIn(">Administrator<", page.body)
        self.assertIn(">Group<", page.body)
        self.assertIn(">Engineering<", page.body)
        self.assertIn('class="table table-bordered table-striped"', page.body)
        self.assertIn('class="btn', page.body)
        self.assertIn('class="el-switch', page.body)
        self.assertIn('class="el-switch__core"', page.body)
        self.assertIn('form="user-status-3"', page.body)
        self.assertNotIn('form="user-status-1"', page.body)
        self.assertIn('action="/users/status"', page.body)
        self.assertIn('name="user_name"', page.body)
        self.assertNotIn("Add a user", page.body)
        self.assertNotIn('action="/users/add"', page.body)
        self.assertIn('href="/apex.css"', page.body)
        self.assertIn('href="/themes/apex.css"', page.body)
        self.assertIn('class="table-check-col"', page.body)
        assert_only_check_script(self, page.body)
        self.assertNotIn("cdn.jsdelivr.net", page.body)
        added = self._open(url + "users?form=add", admin)
        self.assertEqual(added.status, 200)
        self.assertIn("Add a user", added.body)
        self.assertIn('class="card card-primary card-outline"', added.body)
        self.assertIn('class="form-horizontal"', added.body)
        self.assertIn('name="user_name"', added.body)
        self.assertIn('action="/users/add"', added.body)
        narrow = self._open(url + "users?user_name=clerk", admin)
        self.assertIn(">clerk<", narrow.body)
        self.assertNotIn(">operator<", narrow.body)
        self.assertIn(">Group<", narrow.body)
        dept = self._open(url + "users?dept=102", admin)
        self.assertIn(">operator<", dept.body)
        self.assertNotIn(">clerk<", dept.body)
        self.assertIn("is-current", dept.body)
        self.assertIn("Operations", dept.body)
        imported = self._open(url + "users?form=import", admin)
        self.assertEqual(imported.status, 200)
        self.assertIn("Import users", imported.body)
        self.assertIn('action="/users/import"', imported.body)
        self.assertIn('enctype="multipart/form-data"', imported.body)
        self.assertIn('name="file"', imported.body)
        choose = self._open(url + "users?form=edit", admin)
        self.assertIn("Choose an account.", choose.body)
        missing = self._open(url + "users?form=remove&user_id=99999", admin)
        self.assertIn("That account is not in this list.", missing.body)
        exported = self._open(url + "users/export?user_name=clerk", admin)
        self.assertEqual(exported.status, 200)
        self.assertIn("text/csv", exported.headers.get("Content-Type", ""))
        self.assertIn("users.csv", exported.headers.get("Content-Disposition", ""))
        self.assertIn(
            "user_name,nick_name,dept_id,role_id,phonenumber,status",
            exported.body,
        )
        self.assertIn("clerk", exported.body)
        self.assertNotIn("operator", exported.body)
        self.assertNotIn("pbkdf2", exported.body)
        self.assertNotIn("admin123", exported.body)
        self.assertNotIn("<html", exported.body.lower())
        policy = page.headers.get("Content-Security-Policy")
        self.assertEqual(policy, CSP)
        self.assertIn("script-src 'self'", policy)
        self.assertNotIn("script-src 'self' 'unsafe-inline'", policy)
        csrf = re.search(r'name="csrf" value="([^"]+)"', page.body).group(1)
        denied = self._post(url + "users/add", admin, {"user_name": "x", "csrf": "nope"})
        self.assertEqual(denied.status, 400)
        self.assertIn("form token", denied.body)
        flipped = self._post(url + "users/status", admin, {
            "csrf": csrf,
            "user_id": "3",
            "status": "1",
            "user_name": "clerk",
        })
        self.assertIn(flipped.status, (302, 303), flipped.body)
        self.assertIn("user_name=clerk", flipped.headers.get("Location", ""))
        shown = self._open(url + "users?user_name=clerk", admin)
        button = re.search(r'<button[^>]*form="user-status-3"[^>]*>', shown.body)
        self.assertIsNotNone(button)
        self.assertNotIn("is-checked", button.group(0))
        self.assertIn(">Disabled<", shown.body)
        restored = self._post(url + "users/status", admin, {
            "csrf": csrf,
            "user_id": "3",
            "status": "0",
        })
        self.assertIn(restored.status, (302, 303), restored.body)
        back = self._open(url + "users", admin)
        again = re.search(r'<button[^>]*form="user-status-3"[^>]*>', back.body)
        self.assertIsNotNone(again)
        self.assertIn("is-checked", again.group(0))
        kept = self._post(url + "users/status", admin, {
            "csrf": csrf,
            "user_id": "1",
            "status": "1",
        })
        self.assertEqual(kept.status, 400)
        self.assertIn("The built-in administrator stays enabled.", kept.body)
        outside = self._post(url + "users/status", admin, {
            "csrf": csrf,
            "user_id": "99999",
            "status": "1",
        })
        self.assertEqual(outside.status, 400)
        self.assertIn("That account is not in this list.", outside.body)
        edited = self._open(url + "users?form=edit&user_id=2", admin)
        self.assertIn("user-edit-float", edited.body)
        self.assertIn("Edit a user", edited.body)
        self.assertIn("Account", edited.body)
        self.assertIn("Choose a department", edited.body)
        self.assertIn('name="nick_name"', edited.body)
        self.assertIn('name="phonenumber"', edited.body)
        self.assertIn('name="email"', edited.body)
        self.assertIn('name="sex"', edited.body)
        self.assertIn('name="job_title_id"', edited.body)
        self.assertIn('name="role_id"', edited.body)
        self.assertIn('name="remark"', edited.body)
        self.assertIn('name="dept_id"', edited.body)
        self.assertIn("Chief", edited.body)
        self.assertIn("Male", edited.body)
        self.assertIn("Female", edited.body)
        self.assertIn("Unknown", edited.body)
        self.assertIn(
            '<input class="user-readonly" type="text" readonly="" value="operator">',
            edited.body,
        )
        self.assertNotIn('checked="False"', edited.body)
        self.assertNotIn('selected="False"', edited.body)
        assert_only_check_script(self, edited.body)
        edit_at = edited.body.index("Edit a user")
        edit_chunk = edited.body[edit_at:]
        self.assertLess(edit_chunk.index(">Save<"), edit_chunk.index('name="picker"'))
        self.assertIn('formmethod="get"', edit_chunk)
        self.assertNotIn('name="job_title_id"', added.body)
        admin_form = self._open(url + "users?form=edit&user_id=1", admin)
        role_box = re.search(
            r'<input type="checkbox" name="role_id" value="1"([^>]*)>',
            admin_form.body,
        )
        self.assertIsNotNone(role_box)
        self.assertIn("checked", role_box.group(1))
        self.assertIn("disabled", role_box.group(1))
        narrowed = self._open(
            url + "users?form=edit&user_id=3&dept_q=Plat&picker=dept",
            admin,
        )
        self.assertIn(
            'class="dept-open" id="dept-open" type="checkbox" checked',
            narrowed.body,
        )
        for dept_value in ("100", "101", "103"):
            self.assertIn('name="dept_id" value="{0}"'.format(dept_value), narrowed.body)
        self.assertNotIn('name="dept_id" value="102"', narrowed.body)
        kept_ops = self._open(
            url + "users?form=edit&user_id=2&dept_q=Plat&picker=dept",
            admin,
        )
        self.assertIn('name="dept_id" value="102"', kept_ops.body)
        empty_dept = self._post(url + "users/edit", admin, {
            "csrf": csrf,
            "user_id": "2",
            "nick_name": "Operator",
            "dept_id": "",
            "phonenumber": "",
            "email": "",
            "status": "0",
            "sex": "2",
            "job_title_id": "",
            "role_id": "2",
            "remark": "",
        })
        self.assertEqual(empty_dept.status, 400)
        self.assertIn("A department is required.", empty_dept.body)
        empty_roles = self._post(url + "users/edit", admin, {
            "csrf": csrf,
            "user_id": "2",
            "nick_name": "Operator",
            "dept_id": "102",
            "phonenumber": "",
            "email": "",
            "status": "0",
            "sex": "2",
            "job_title_id": "",
            "role_id": "",
            "remark": "",
        })
        self.assertEqual(empty_roles.status, 400)
        self.assertIn("Choose a role.", empty_roles.body)
        bad_mail = self._post(url + "users/edit", admin, {
            "csrf": csrf,
            "user_id": "2",
            "nick_name": "Operator",
            "dept_id": "102",
            "phonenumber": "",
            "email": "nope",
            "status": "0",
            "sex": "2",
            "job_title_id": "",
            "role_id": "2",
            "remark": "",
        })
        self.assertEqual(bad_mail.status, 400)
        self.assertIn("The email must contain @.", bad_mail.body)
        missing_edit = self._post(url + "users/edit", admin, {
            "csrf": csrf,
            "user_id": "99999",
            "nick_name": "Nobody",
            "dept_id": "102",
            "role_id": "2",
        })
        self.assertEqual(missing_edit.status, 400)
        self.assertIn("That account is not in this list.", missing_edit.body)
        kept_admin = self._post(url + "users/edit", admin, {
            "csrf": csrf,
            "user_id": "1",
            "nick_name": "Administrator",
            "dept_id": "101",
            "phonenumber": "",
            "email": "",
            "status": "0",
            "sex": "2",
            "job_title_id": "",
            "role_id": "",
            "remark": "",
        })
        self.assertIn(kept_admin.status, (302, 303), kept_admin.body)
        admin_row = self.desk.store.query_one(
            "SELECT user_name FROM sys_user WHERE user_id = %s",
            (1,),
        )
        self.assertEqual(admin_row["user_name"], "admin")
        admin_roles = self.desk.store.query_all(
            "SELECT role_id FROM sys_user_role WHERE user_id = %s ORDER BY role_id",
            (1,),
        )
        self.assertEqual([int(row["role_id"]) for row in admin_roles], [1])
        try:
            saved = self._post(url + "users/edit", admin, [
                ("csrf", csrf),
                ("user_id", "2"),
                ("nick_name", "Op"),
                ("dept_id", "102"),
                ("phonenumber", "555"),
                ("email", "op@example.com"),
                ("status", "0"),
                ("sex", "1"),
                ("job_title_id", ""),
                ("job_title_id", "1"),
                ("job_title_id", "2"),
                ("role_id", ""),
                ("role_id", "2"),
                ("role_id", "3"),
                ("remark", "desk"),
                ("user_name", "clerk"),
            ])
            self.assertIn(saved.status, (302, 303), saved.body)
            location = saved.headers.get("Location", "")
            self.assertIn("user_name=clerk", location)
            self.assertNotIn("form=", location)
            changed = self.desk.store.query_one(
                """
                SELECT user_name, nick_name, phonenumber, email, sex, remark, dept_id
                FROM sys_user WHERE user_id = %s
                """,
                (2,),
            )
            self.assertEqual(changed["user_name"], "operator")
            self.assertEqual(changed["nick_name"], "Op")
            self.assertEqual(changed["phonenumber"], "555")
            self.assertEqual(changed["email"], "op@example.com")
            self.assertEqual(str(changed["sex"]), "1")
            self.assertEqual(changed["remark"], "desk")
            self.assertEqual(int(changed["dept_id"]), 102)
            title_rows = self.desk.store.query_all(
                """
                SELECT job_title_id FROM sys_user_job_title
                WHERE user_id = %s ORDER BY job_title_id
                """,
                (2,),
            )
            self.assertEqual([int(row["job_title_id"]) for row in title_rows], [1, 2])
            role_rows = self.desk.store.query_all(
                "SELECT role_id FROM sys_user_role WHERE user_id = %s ORDER BY role_id",
                (2,),
            )
            self.assertEqual([int(row["role_id"]) for row in role_rows], [2, 3])
            status_only = self._post(url + "users/status", admin, {
                "csrf": csrf,
                "user_id": "2",
                "status": "1",
            })
            self.assertIn(status_only.status, (302, 303), status_only.body)
            still_titles = self.desk.store.query_all(
                """
                SELECT job_title_id FROM sys_user_job_title
                WHERE user_id = %s ORDER BY job_title_id
                """,
                (2,),
            )
            self.assertEqual([int(row["job_title_id"]) for row in still_titles], [1, 2])
            still_roles = self.desk.store.query_all(
                "SELECT role_id FROM sys_user_role WHERE user_id = %s ORDER BY role_id",
                (2,),
            )
            self.assertEqual([int(row["role_id"]) for row in still_roles], [2, 3])
        finally:
            self.desk.store.execute(
                """
                UPDATE sys_user
                SET nick_name = %s, dept_id = %s, phonenumber = %s, email = %s,
                    sex = %s, remark = %s, status = %s
                WHERE user_id = %s
                """,
                ("Operator", 102, "", "", "2", "", "0", 2),
            )
            self.desk.store.execute(
                "DELETE FROM sys_user_job_title WHERE user_id = %s",
                (2,),
            )
            self.desk.store.execute(
                "DELETE FROM sys_user_role WHERE user_id = %s",
                (2,),
            )
            self.desk.store.execute(
                "INSERT INTO sys_user_role (user_id, role_id) VALUES (%s, %s)",
                (2, 2),
            )
        operator = self._sign_in("operator", Schema.INITIAL_OPERATOR_PASSWORD, url)
        scoped = self._open(url + "users", operator)
        self.assertEqual(scoped.status, 200)
        self.assertNotIn("Add a user", scoped.body)
        self.assertNotIn(">Add<", scoped.body)
        self.assertNotIn(">Import<", scoped.body)
        self.assertNotIn(">Export<", scoped.body)
        self.assertNotIn("user-btn-import", scoped.body)
        self.assertNotIn("/users/export", scoped.body)
        self.assertNotIn('action="/users/add"', scoped.body)
        self.assertNotIn('action="/users/import"', scoped.body)
        self.assertNotIn('action="/users/status"', scoped.body)
        self.assertIn('class="el-switch', scoped.body)
        self.assertIn("is-disabled", scoped.body)
        op_csrf = re.search(r'name="csrf" value="([^"]+)"', scoped.body).group(1)
        blocked_status = self._post(url + "users/status", operator, {
            "csrf": op_csrf,
            "user_id": "2",
            "status": "1",
        })
        self.assertEqual(blocked_status.status, 403)
        self.assertIn("Missing permission", blocked_status.body)
        self.assertIn("operator", scoped.body)
        self.assertIn(">Group<", scoped.body)
        self.assertIn(">Operations<", scoped.body)
        self.assertNotIn(">Engineering<", scoped.body)
        self.assertNotIn(">clerk<", scoped.body)
        self.assertNotIn(">lead<", scoped.body)
        self.assertNotIn("<script", scoped.body.lower())
        forced = self._open(url + "users?form=add", operator)
        self.assertNotIn("Add a user", forced.body)
        self.assertNotIn('action="/users/add"', forced.body)
        forced_import = self._open(url + "users?form=import", operator)
        self.assertNotIn("Import users", forced_import.body)
        self.assertNotIn('action="/users/import"', forced_import.body)
        forced_edit = self._open(url + "users?form=edit&user_id=2", operator)
        self.assertNotIn("Edit a user", forced_edit.body)
        op_export = self._open(url + "users/export", operator)
        self.assertEqual(op_export.status, 403)
        self.assertIn("Missing permission", op_export.body)
        csv_text = "user_name,nick_name,dept_id,role_id\npat,Pat,102,2\n"
        payload, content_type = self._multipart(
            (("csrf", csrf),),
            (("file", "people.csv", csv_text),),
        )
        posted = self._post_bytes(url + "users/import", admin, payload, content_type)
        self.assertIn(posted.status, (302, 303), posted.body)
        self.assertIn("Imported", posted.headers.get("Location", ""))
        listed = self._open(url + "users", admin)
        self.assertIn(">pat<", listed.body)
        bad_payload, bad_type = self._multipart(
            (("csrf", csrf),),
            (("file", "people.txt", csv_text),),
        )
        rejected = self._post_bytes(url + "users/import", admin, bad_payload, bad_type)
        self.assertEqual(rejected.status, 400)
        self.assertIn(".csv", rejected.body)
        blocked = self._open(url + "roles", operator)
        self.assertEqual(blocked.status, 403)
        self.assertIn("Missing permission", blocked.body)
        for path in (
            "/",
            "/users",
            "/roles",
            "/menus",
            "/depts",
            "/job-titles",
            "/configs",
            "/dicts",
            "/notices",
            "/oper-log",
            "/login-log",
            "/online",
            "/database",
        ):
            opened = self._open(url + path.lstrip("/"), admin)
            self.assertEqual(opened.status, 200, opened.body[:500])
            assert_only_check_script(self, opened.body)
            self.assertIn('href="/apex.css"', opened.body)
            self.assertIn('href="/themes/apex.css"', opened.body)
        roles = self._open(url + "roles", admin)
        self.assertIn("Role name", roles.body)
        self.assertIn("Permission key", roles.body)
        self.assertIn("Data scope", roles.body)
        self.assertIn("All data", roles.body)
        self.assertIn('class="el-tag el-tag--success"', roles.body)
        self.assertIn('class="el-switch', roles.body)
        self.assertNotIn("menu_id", roles.body)
        role_edit = self._open(url + "roles?form=edit&role_id=2", admin)
        self.assertIn("el-tree", role_edit.body)
        self.assertIn(" checked", role_edit.body)
        role_scope = self._open(url + "roles?form=scope&role_id=2", admin)
        self.assertIn('name="menu_id"', role_scope.body)
        menus = self._open(url + "menus", admin)
        self.assertEqual(menus.status, 200)
        self.assertIn(">System<", menus.body)
        self.assertNotIn(">User<", menus.body)
        self.assertIn("menu-twist is-shut", menus.body)
        self.assertIn("closed=open", menus.body)
        spread = self._open(url + "menus?closed=open", admin)
        self.assertIn(">User<", spread.body)
        self.assertIn(">User query<", spread.body)
        self.assertIn("menu-twist is-open", spread.body)
        self.assertIn(">Edit<", menus.body)
        self.assertIn(">Save sort<", menus.body)
        self.assertIn('aria-label="check all"', menus.body)
        self.assertIn('type="checkbox" name="menu_id"', menus.body)
        self.assertNotIn(">Choose<", menus.body)
        self.assertIn("menu-btn-edit", menus.body)
        self.assertIn("menu-btn-sort", menus.body)
        self.assertIn('action="/menus/sort"', menus.body)
        self.assertIn('form="menu-sort"', menus.body)
        self.assertIn('name="order_num"', menus.body)
        self.assertIn('class="table-check-col"', menus.body)
        assert_only_check_script(self, menus.body)
        choose_menu = self._open(url + "menus?form=edit", admin)
        self.assertIn("Choose a menu.", choose_menu.body)
        self.assertNotIn("Edit a menu", choose_menu.body)
        editing = self._open(url + "menus?form=edit&menu_id=102", admin)
        self.assertIn("Edit a menu", editing.body)
        self.assertIn('action="/menus/edit"', editing.body)
        self.assertIn('value="Menu"', editing.body)
        self.assertIn('value="C" checked', editing.body)
        assert_only_check_script(self, editing.body)
        login = self._open(url + "login", "")
        self.assertEqual(login.status, 200)
        self.assertIn("sqlite3", login.body)
        self.assertIn("mysql", login.body)
        self.assertIn('name="engine"', login.body)
        self.assertIn('value="sqlite3" checked', login.body)
        self.assertIn("default file", login.body)
        self.assertNotIn("<img", login.body.lower())
        self.assertNotIn("captcha", login.body.lower())
        css = self._open(url + "apex.css", "")
        self.assertEqual(css.status, 200)
        self.assertIn("text/css", css.headers.get("Content-Type", ""))
        self.assertIn(".main-sidebar", css.body)
        theme_css = self._open(url + "themes/hospital.css", "")
        self.assertEqual(theme_css.status, 200)
        self.assertIn("text/css", theme_css.headers.get("Content-Type", ""))
        self.assertIn("--sidebar:", theme_css.body)
        icon = self._open(url + "icons/user-plus.svg", "")
        self.assertEqual(icon.status, 200)
        self.assertIn("image/svg+xml", icon.headers.get("Content-Type", ""))
        self.assertIn("<svg", icon.body)
        self.assertNotIn("<script", icon.body.lower())
        self.assertNotIn("data:image", icon.body)
        missing_icon = self._open(url + "icons/not-an-icon.svg", "")
        self.assertEqual(missing_icon.status, 404)
        slipped = self._open(url + "icons/../openrbac.css", "")
        self.assertNotIn("text/css", slipped.headers.get("Content-Type", ""))
        for path in ("/menus", "/depts", "/job-titles", "/dicts", "/online", "/database"):
            denied_page = self._open(url + path.lstrip("/"), operator)
            self.assertEqual(denied_page.status, 403, path)
            self.assertIn("Missing permission", denied_page.body)
        bare = self._open(url + "users", "")
        self.assertIn(bare.status, (302, 303))
        self.assertEqual(bare.headers.get("Location"), "/login")

    def test_login_log_page_matches_the_studied_list(self):
        """requirement-html-login-log — AC-1 through AC-9."""
        note = self.desk.serve_background()
        url = note.splitlines()[0].split(": ", 1)[1]
        self.desk.audit.write_login(
            "zzlog", "10.9.9.9", "1", "zzlog-marker", "open-rbac", "TestOS",
        )
        admin = self._sign_in("admin", Schema.INITIAL_ADMIN_PASSWORD, url)
        page = self._open(url + "login-log", admin)
        self.assertEqual(page.status, 200, page.body[:500])
        labels = (
            "Access id",
            "Login name",
            "Login address",
            "Login location",
            "Browser",
            "Operating system",
            "Login status",
            "Message",
            "Login time",
        )
        position = -1
        for label in labels:
            found = page.body.find(">{0}<".format(label))
            self.assertGreater(found, position, label)
            position = found
        self.assertIn("Login address", page.body)
        self.assertIn("user-btn-search", page.body)
        self.assertIn("user-btn-reset", page.body)
        self.assertIn('class="user-btn user-btn-reset" href="/login-log"', page.body)
        self.assertIn('class="login-page"', page.body)
        self.assertIn('href="/login-log"', page.body)
        self.assertIn("nav-link active", page.body)
        self.assertIn(">admin<", page.body)
        self.assertIn('class="el-tag el-tag--success"', page.body)
        self.assertIn(">Success<", page.body)
        self.assertIn('class="el-tag el-tag--danger"', page.body)
        self.assertIn(">Failed<", page.body)
        self.assertIn("zzlog-marker", page.body)
        self.assertNotIn("el-switch", page.body)
        self.assertIn('method="post"', page.body)
        self.assertIn('action="/logout"', page.body)
        self.assertIn('name="csrf"', page.body)
        low = page.body.lower()
        self.assertNotIn("<iframe", low)
        self.assertNotIn("<script", low)
        self.assertNotIn("bootstrap.min.css", low)
        self.assertNotIn("jquery", low)
        self.assertNotIn("font-awesome", low)
        self.assertNotIn('type="checkbox"', low)
        for word in ("Delete", "Clear", "Unlock", "Export"):
            self.assertNotIn(">{0}<".format(word), page.body)
        self.assertNotIn("登录", page.body)
        named = self._open(url + "login-log?user_name=admin", admin)
        self.assertIn("zzlog", page.body)
        self.assertNotIn("zzlog", named.body)
        self.assertNotIn("zzlog-marker", named.body)
        missed = self._open(url + "login-log?user_name=ZZLOG", admin)
        self.assertNotIn("zzlog-marker", missed.body)
        failed = self._open(url + "login-log?status=1", admin)
        self.assertIn("zzlog-marker", failed.body)
        self.assertIn('class="el-tag el-tag--danger"', failed.body)
        self.assertNotIn("el-tag--success", failed.body)
        future = self._open(url + "login-log?begin=2999-01-01", admin)
        yesterday = self._open(url + "login-log?begin=yesterday", admin)
        self.assertIn("Showing 0 to 0 of 0 records", future.body)
        self.assertIn("Showing 0 to 0 of 0 records", yesterday.body)
        self.assertIn('class="admlte-date-range"', page.body)
        self.assertNotIn(">From<", page.body)
        self.assertNotIn(">To<", page.body)
        self.assertIn('type="date" name="begin"', page.body)
        self.assertIn('type="date" name="end"', page.body)
        self.assertIn('aria-hidden="true">→<', page.body)
        self.assertIn('min="2999-01-01"', future.body)
        self.assertNotIn("max=", future.body)
        self.assertIn('min="yesterday"', yesterday.body)
        self.assertNotIn("zzlog-marker", future.body)
        report = self.desk.report.login_log(self.desk.catalog.login_log({"user_id": 1}))
        self.assertEqual(
            report.splitlines()[0],
            "info_id|user_name|ipaddr|status|msg|login_time",
        )
        operator = self._sign_in("operator", Schema.INITIAL_OPERATOR_PASSWORD, url)
        allowed = self._open(url + "login-log", operator)
        self.assertEqual(allowed.status, 200, allowed.body[:500])
        self.assertIn("Login address", allowed.body)
        lead = self._sign_in("lead", Schema.INITIAL_LEAD_PASSWORD, url)
        refused = self._open(url + "login-log", lead)
        self.assertEqual(refused.status, 403)
        self.assertIn("Missing permission", refused.body)
        os.environ["OPENRBAC_THEME"] = "hospital"
        try:
            themed = self._open(url + "login-log", admin)
        finally:
            os.environ.pop("OPENRBAC_THEME", None)
        self.assertEqual(themed.status, 200, themed.body[:500])
        position = -1
        for label in labels:
            found = themed.body.find(">{0}<".format(label))
            self.assertGreater(found, position, label)
            position = found
        self.assertNotIn('href="/element-plus.css"', themed.body)
        self.assertIn('href="/apex.css"', themed.body)
        self.assertIn('href="/themes/hospital.css"', themed.body)

    def _multipart(self, fields, files):
        boundary = "----OpenRbacBoundary"
        chunks = []
        for name, value in fields:
            chunks.append(
                '--{0}\r\nContent-Disposition: form-data; name="{1}"\r\n\r\n{2}\r\n'.format(
                    boundary, name, value,
                )
            )
        for name, filename, value in files:
            chunks.append(
                '--{0}\r\nContent-Disposition: form-data; name="{1}"; filename="{2}"\r\n'
                "Content-Type: text/csv\r\n\r\n{3}\r\n".format(
                    boundary, name, filename, value,
                )
            )
        chunks.append("--{0}--\r\n".format(boundary))
        return "".join(chunks).encode("utf-8"), "multipart/form-data; boundary={0}".format(boundary)

    def test_dictionary_page_lists_seeded_types(self):
        """The dictionaries page lists seeded types and still lists values.

        requirement-html-dictionaries — the seeded type table and the filters.
        requirement-rbac-dictionaries — dict_type_list and dict-list.
        """
        admin = {"user_id": 1, "user_name": "admin", "csrf": "tok"}
        kinds = self.desk.catalog.dict_type_list(admin)
        self.assertEqual(
            [row["dict_type"] for row in kinds],
            ["sys_user_sex", "sys_normal_disable", "sys_notice_type"],
        )
        self.assertEqual(kinds[0]["dict_name"], "User sex")
        self.assertIn(kinds[0]["remark"], (None, ""))
        labels = [row["dict_label"] for row in self.desk.catalog.dict_list(admin)]
        self.assertIn("Male", labels)
        self.assertIn("Notice", labels)
        operator = self.desk.store.query_one(
            "SELECT user_id FROM sys_user WHERE user_name = %s",
            ("operator",),
        )
        with self.assertRaises(AccessError) as denied:
            self.desk.catalog.dict_type_list({
                "user_id": operator["user_id"],
                "user_name": "operator",
            })
        self.assertIn("Missing permission", str(denied.exception))
        app = self.desk.web()
        with self.assertRaises(AccessError) as page_denied:
            app._route_get(
                "/dicts",
                {"user_id": operator["user_id"], "user_name": "operator"},
                "",
            )
        self.assertIn("Missing permission", str(page_denied.exception))
        app._request.path = "/dicts"
        app._request.query = {}
        html = app.dicts_page(admin, "")
        self.assertIn("Showing 1 to 3 of 3 records", html)
        self.assertIn("User sex", html)
        self.assertLess(html.index("User sex"), html.index("Notice type"))
        self.assertIn('class="el-tag el-tag--success"', html)
        app._request.query = {"status": ["1"]}
        self.assertIn("Showing 0 to 0 of 0 records", app.dicts_page(admin, ""))
        app._request.query = {"begin": ["2999-01-01"]}
        self.assertIn("Showing 0 to 0 of 0 records", app.dicts_page(admin, ""))
        app._request.query = {"begin": ["yesterday"]}
        self.assertIn("Showing 0 to 0 of 0 records", app.dicts_page(admin, ""))
        app._request.query = {"dict_type": ["sys_user_sex"]}
        one = app.dicts_page(admin, "")
        self.assertIn("User sex", one)
        self.assertNotIn("Notice type", one)
        app._request.query = {"dict_name": ["Notice"]}
        named = app.dicts_page(admin, "")
        self.assertIn("Notice type", named)
        self.assertNotIn("User sex", named)
        app._request.query = {"form": ["add"]}
        self.assertIn('action="/dicts/add"', app.dicts_page(admin, ""))
        app._request.query = {}
        self.assertNotIn('action="/dicts/add"', app.dicts_page(admin, ""))
        app._request.path = ""
        app._request.query = {}

    def _post_bytes(self, url, token, payload, content_type):
        parsed = urllib.parse.urlparse(url)
        connection = self._connection(url)
        connection.request(
            "POST",
            parsed.path or "/",
            payload,
            {
                "Cookie": "openrbac_session={0}".format(token),
                "Content-Type": content_type,
            },
        )
        response = connection.getresponse()
        page = _Page(response.status, response.read().decode("utf-8", "replace"), response.headers)
        connection.close()
        return page

    def _connection(self, url):
        parsed = urllib.parse.urlparse(url)
        return http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=5)

    def _sign_in(self, user_name, password, url):
        body = urllib.parse.urlencode({"user_name": user_name, "password": password})
        connection = self._connection(url)
        connection.request(
            "POST",
            "/login",
            body,
            {"Content-Type": "application/x-www-form-urlencoded"},
        )
        response = connection.getresponse()
        raw = response.read()
        cookie = response.getheader("Set-Cookie") or ""
        connection.close()
        self.assertIn(response.status, (302, 303), raw.decode("utf-8", "replace"))
        self.assertIn("openrbac_session=", cookie)
        token = cookie.split("openrbac_session=", 1)[1].split(";", 1)[0]
        self.assertNotIn(password, cookie)
        return token

    def _open(self, url, token):
        parsed = urllib.parse.urlparse(url)
        connection = self._connection(url)
        headers = {}
        if token:
            headers["Cookie"] = "openrbac_session={0}".format(token)
        target = parsed.path or "/"
        if parsed.query:
            target = "{0}?{1}".format(target, parsed.query)
        connection.request("GET", target, headers=headers)
        response = connection.getresponse()
        page = _Page(response.status, response.read().decode("utf-8"), response.headers)
        connection.close()
        return page

    def _post(self, url, token, fields):
        parsed = urllib.parse.urlparse(url)
        connection = self._connection(url)
        data = urllib.parse.urlencode(fields, doseq=True)
        connection.request(
            "POST",
            parsed.path or "/",
            data,
            {
                "Cookie": "openrbac_session={0}".format(token),
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        response = connection.getresponse()
        page = _Page(response.status, response.read().decode("utf-8"), response.headers)
        connection.close()
        return page


class _Page:
    def __init__(self, status, body, headers):
        self.status = status
        self.body = body
        self.headers = headers


class TestChronicle(unittest.TestCase):
    """def main constructs ChronicleLogger and does not record a password."""

    def test_construct_and_secret_stay_out_of_the_log(self):
        source = (ROOT / "src" / "OpenRbac" / "cli.py").read_text(encoding="utf-8")
        self.assertIn("ChronicleLogger(", source)
        self.assertIn(
            'ChronicleLogger is required. Next step: python -m pip install "ChronicleLogger>=1.3.1"',
            source,
        )
        logdir = tempfile.mkdtemp(prefix="openrbac_log_", dir="/tmp")
        home = tempfile.mkdtemp(prefix="openrbac_loghome_", dir="/tmp")
        saved = {
            name: os.environ.get(name)
            for name in (
                "OPENRBAC_HOME",
                "OPENRBAC_DB_ENGINE",
                "OPENRBAC_SQLITE_FILE",
                "OPENRBAC_DB_NAME",
                "OPENRBAC_DB_PASSWORD",
            )
        }
        os.environ["OPENRBAC_HOME"] = home
        os.environ["OPENRBAC_DB_ENGINE"] = "sqlite3"
        os.environ["OPENRBAC_SQLITE_FILE"] = os.path.join(home, "openrbac.sqlite3")
        os.environ.pop("OPENRBAC_DB_PASSWORD", None)
        secret = "s3cret-value-not-for-logs"
        try:
            Desk().db_init()
            code = main(
                ["login", "--user-name", "admin", "--password", secret],
                logdir=logdir,
            )
            self.assertEqual(code, 1)
            blob = ""
            for path in Path(logdir).rglob("*"):
                if path.is_file():
                    blob += path.read_text(encoding="utf-8", errors="replace")
            self.assertNotIn(secret, blob)
            self.assertIn("ChronicleLogger", source)
        finally:
            for name, value in saved.items():
                if value is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = value


class TestEngineChoice(unittest.TestCase):
    """sqlite3 is the default file. mysql is the other choice. Every interface offers both."""

    def _home(self):
        return tempfile.mkdtemp(prefix="openrbac_engine_", dir="/tmp")

    def _settings(self, home, **extra):
        environ = {"OPENRBAC_HOME": home, "HOME": home}
        environ.update(extra)
        return Settings(environ=environ, home=home)

    def test_default_is_the_sqlite_file(self):
        home = self._home()
        settings = self._settings(home)
        self.assertEqual(settings.engine(), "sqlite3")
        self.assertTrue(settings.sqlite_path().endswith(os.path.join("OpenRbac", "openrbac.sqlite3")) or settings.sqlite_path().endswith("openrbac.sqlite3"))
        self.assertIn("openrbac.sqlite3", settings.sqlite_path())
        lines = settings.choice_lines()
        self.assertIn("Enter uses sqlite3", lines[0])
        self.assertIn("default file", lines[0])
        self.assertIn("1 sqlite3", lines[1])
        self.assertIn("openrbac.sqlite3", lines[1])
        self.assertIn("(default file)", lines[1])
        self.assertIn("2 mysql", lines[2])
        blank = settings.apply_choice("")
        self.assertIn("sqlite3", blank)
        self.assertIn("(default file)", blank)
        self.assertIn("OPENRBAC_DB_ENGINE=sqlite3", (Path(home) / "database").read_text(encoding="utf-8"))
        sentence = settings.apply_choice("1")
        self.assertIn("sqlite3", sentence)
        path = Path(home) / "database"
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertIn("OPENRBAC_DB_ENGINE=sqlite3", path.read_text(encoding="utf-8"))
        self.assertFalse((Path(home) / "openrbac.sqlite3").exists())

    def test_mysql_choice_and_environment_wins(self):
        home = self._home()
        settings = self._settings(home)
        sentence = settings.apply_choice("mysql")
        self.assertIn("mysql", sentence)
        self.assertEqual(settings.engine(), "mysql")
        locked = self._settings(home, OPENRBAC_DB_ENGINE="sqlite3")
        with self.assertRaises(SettingsError) as caught:
            locked.apply_choice("2")
        self.assertIn("environment", str(caught.exception))
        self.assertEqual(locked.apply_choice(""), locked.engine_sentence())
        mysql_env = self._settings(home, OPENRBAC_DB_ENGINE="mysql")
        kept = mysql_env.apply_choice("")
        self.assertIn("mysql", kept)
        self.assertIn("environment", kept)
        self.assertEqual(mysql_env.engine(), "mysql")
        with self.assertRaises(SettingsError):
            settings.apply_choice("postgres")

    def test_cli_prints_both_choices_without_opening_sqlite(self):
        home = self._home()
        saved = {
            name: os.environ.get(name)
            for name in ("OPENRBAC_HOME", "OPENRBAC_DB_ENGINE", "OPENRBAC_SQLITE_FILE", "HOME")
        }
        os.environ["OPENRBAC_HOME"] = home
        os.environ["HOME"] = home
        os.environ.pop("OPENRBAC_DB_ENGINE", None)
        os.environ.pop("OPENRBAC_SQLITE_FILE", None)
        try:
            from io import StringIO
            from contextlib import redirect_stderr, redirect_stdout
            app = Cli()
            out = StringIO()
            err = StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = app.run(["db-engine"])
            self.assertEqual(code, 0, err.getvalue())
            text = out.getvalue()
            self.assertIn("1 sqlite3", text)
            self.assertIn("openrbac.sqlite3", text)
            self.assertIn("2 mysql", text)
            self.assertFalse((Path(home) / "openrbac.sqlite3").exists())
            out = StringIO()
            err = StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = app.run(["db-engine", "--engine", "mysql"])
            self.assertEqual(code, 0, err.getvalue())
            self.assertIn("mysql", out.getvalue())
            stored = (Path(home) / "database").read_text(encoding="utf-8")
            self.assertIn("OPENRBAC_DB_ENGINE=mysql", stored)
            self.assertFalse((Path(home) / "openrbac.sqlite3").exists())
            err = StringIO()
            with redirect_stdout(StringIO()), redirect_stderr(err):
                code = app.run(["db-engine", "--engine", "oracle"])
            self.assertEqual(code, 1)
            self.assertIn("ERROR:", err.getvalue())
            self.assertIn("Next:", err.getvalue())
        finally:
            for name, value in saved.items():
                if value is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = value

    def test_sqlite_seed_file_mode_and_web_choices(self):
        home = self._home()
        data = os.path.join(home, "openrbac.sqlite3")
        desk = Desk(environ={
            "OPENRBAC_HOME": home,
            "HOME": home,
            "OPENRBAC_DB_ENGINE": "sqlite3",
            "OPENRBAC_SQLITE_FILE": data,
            "OPENRBAC_BIND": "127.0.0.1",
            "OPENRBAC_PORT": "0",
        })
        first = desk.db_init()
        self.assertIn("seeded", first)
        self.assertIn(data, first)
        second = desk.db_init()
        self.assertIn("present", second)
        self.assertEqual(os.stat(data).st_mode & 0o777, 0o600)
        page = desk.web().login_page("")
        self.assertIn("sqlite3", page)
        self.assertIn("openrbac.sqlite3", page)
        self.assertIn("mysql", page)
        self.assertIn('name="engine"', page)
        self.assertIn("already selected", page)
        plain = Desk(environ={
            "OPENRBAC_HOME": home,
            "HOME": home,
            "OPENRBAC_BIND": "127.0.0.1",
            "OPENRBAC_PORT": "0",
        })
        plain_page = plain.web().login_page("")
        self.assertIn("(default file)", plain_page)
        self.assertIn("openrbac.sqlite3", plain_page)
        signed = desk.access.login(
            "admin",
            Schema.INITIAL_ADMIN_PASSWORD,
            ipaddr="127.0.0.1",
            surface="web",
            user_agent="test",
        )
        body = desk.web().database_page(signed, "")
        self.assertIn("sqlite3", body)
        self.assertIn("mysql", body)
        self.assertIn("csrf", body)

        class Remote:
            client_address = ("remote.test", 9)

        with self.assertRaises(SettingsError):
            desk.web()._apply_posted_engine(Remote(), {"engine": ["mysql"]})

        class Local:
            client_address = ("127.0.0.1", 9)

        open_choice = Desk(environ={"OPENRBAC_HOME": home, "HOME": home})
        open_choice.web()._apply_posted_engine(Local(), {"engine": ["mysql"]})
        self.assertEqual(open_choice.settings.engine(), "mysql")
        self.assertIn(
            "OPENRBAC_DB_ENGINE=mysql",
            (Path(home) / "database").read_text(encoding="utf-8"),
        )

    def test_menu_row_offers_the_engine(self):
        from OpenRbac.menu_painter import MenuPainter
        rows = MenuPainter().rows_for("setup")
        self.assertIn((218, "db-engine", "sqlite3 file or mysql", "db-engine"), rows)
        self.assertIn("db-engine", Cli.PRODUCT_VERBS)
        self.assertNotIn("db-engine", Cli.DOMAIN_VERBS)

    def test_mysql_seed_when_the_server_is_reachable(self):
        try:
            password = _password_from_file()
        except unittest.SkipTest:
            raise
        home = self._home()
        desk = Desk(environ={
            "OPENRBAC_HOME": home,
            "HOME": home,
            "OPENRBAC_DB_ENGINE": "mysql",
            "OPENRBAC_DB_NAME": "openrbac_test",
            "OPENRBAC_DB_USER": "openrbac",
            "OPENRBAC_DB_HOST": "127.0.0.1",
            "OPENRBAC_DB_PORT": "3306",
            "OPENRBAC_DB_PASSWORD": password,
        })
        try:
            desk.store.query_one("SELECT 1 AS n")
        except Exception:
            raise unittest.SkipTest("mysql is not reachable")
        _drop_tables(desk.store)
        first = desk.db_init()
        self.assertIn("seeded", first)
        self.assertIn("openrbac_test", first)
        second = desk.db_init()
        self.assertIn("present", second)
        self.assertNotIn("ruoyi_db", first)
        self.assertNotIn("ry", first)


class TestThemeChoice(unittest.TestCase):
    """apex is the default theme. Eleven skins share one shell. The verb does not open the database."""

    def _home(self):
        return tempfile.mkdtemp(prefix="openrbac_theme_", dir="/tmp")

    def _settings(self, home, **extra):
        environ = {"OPENRBAC_HOME": home, "HOME": home}
        environ.update(extra)
        return Settings(environ=environ, home=home)

    def test_default_is_apex_and_a_number_stores_that_skin(self):
        home = self._home()
        settings = self._settings(home)
        self.assertEqual(settings.theme(), "apex")
        lines = settings.theme_lines()
        self.assertIn("Enter uses apex", lines[0])
        self.assertEqual(lines[1], "1 apex")
        self.assertEqual(lines[2], "2 admindek")
        self.assertEqual(lines[8], "8 finance-saas")
        self.assertEqual(lines[11], "11 kero")
        self.assertIn("apex", lines[12])
        blank = settings.apply_theme("")
        self.assertEqual(blank, "Theme: apex.")
        path = Path(home) / "database"
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertIn("OPENRBAC_THEME=apex", path.read_text(encoding="utf-8"))
        self.assertFalse((Path(home) / "openrbac.sqlite3").exists())
        sentence = settings.apply_theme("2")
        self.assertEqual(sentence, "Theme: admindek.")
        self.assertIn("OPENRBAC_THEME=admindek", path.read_text(encoding="utf-8"))
        self.assertEqual(settings.apply_theme("8"), "Theme: finance-saas.")
        self.assertEqual(settings.apply_theme("Finance SaaS"), "Theme: finance-saas.")
        self.assertEqual(settings.apply_theme("1"), "Theme: apex.")
        kept = settings.apply_theme("apex")
        self.assertEqual(kept, "Theme: apex.")
        with self.assertRaises(SettingsError):
            settings.apply_theme("12")
        with self.assertRaises(SettingsError):
            settings.apply_theme("vue3")
        with self.assertRaises(SettingsError):
            settings.apply_theme("adminlte")

    def test_an_old_stored_name_still_lists_the_choices(self):
        """Row 24 still offers the eleven skins when the file says adminlte."""
        home = self._home()
        path = Path(home) / "database"
        path.write_text("OPENRBAC_DB_ENGINE=sqlite3\nOPENRBAC_THEME=adminlte\n", encoding="utf-8")
        os.chmod(path, 0o600)
        settings = self._settings(home)
        with self.assertRaises(SettingsError):
            settings.theme()
        lines = settings.theme_lines()
        self.assertEqual(lines[1], "1 apex")
        self.assertEqual(lines[11], "11 kero")
        self.assertIn("adminlte", lines[12])
        self.assertIn("not a theme", lines[12])
        self.assertEqual(settings.apply_theme(""), "Theme: apex.")
        self.assertEqual(settings.theme(), "apex")
        self.assertIn("OPENRBAC_DB_ENGINE=sqlite3", path.read_text(encoding="utf-8"))
        path.write_text("OPENRBAC_THEME=vue3\n", encoding="utf-8")
        os.chmod(path, 0o600)
        self.assertEqual(settings.apply_theme("11"), "Theme: kero.")
        self.assertEqual(settings.theme(), "kero")

    def test_environment_wins_and_engine_line_stays(self):
        home = self._home()
        settings = self._settings(home)
        settings.apply_choice("mysql")
        settings.apply_theme("kero")
        stored = (Path(home) / "database").read_text(encoding="utf-8")
        self.assertIn("OPENRBAC_DB_ENGINE=mysql", stored)
        self.assertIn("OPENRBAC_THEME=kero", stored)
        locked = self._settings(home, OPENRBAC_THEME="apex")
        with self.assertRaises(SettingsError) as caught:
            locked.apply_theme("2")
        self.assertIn("environment", str(caught.exception))
        self.assertEqual(locked.apply_theme(""), locked.theme_sentence())
        admin_env = self._settings(home, OPENRBAC_THEME="kero")
        kept = admin_env.apply_theme("")
        self.assertIn("kero", kept)
        self.assertIn("environment", kept)
        self.assertEqual(admin_env.theme(), "kero")

    def test_cli_prints_both_choices_without_opening_sqlite(self):
        home = self._home()
        saved = {
            name: os.environ.get(name)
            for name in ("OPENRBAC_HOME", "OPENRBAC_THEME", "HOME")
        }
        os.environ["OPENRBAC_HOME"] = home
        os.environ["HOME"] = home
        os.environ.pop("OPENRBAC_THEME", None)
        try:
            from io import StringIO
            from contextlib import redirect_stderr, redirect_stdout
            app = Cli()
            out = StringIO()
            err = StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = app.run(["theme"])
            self.assertEqual(code, 0, err.getvalue())
            text = out.getvalue()
            self.assertIn("1 apex", text)
            self.assertIn("2 admindek", text)
            self.assertIn("11 kero", text)
            self.assertFalse((Path(home) / "openrbac.sqlite3").exists())
            self.assertFalse((Path(home) / "database").exists())
            out = StringIO()
            err = StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = app.run(["theme", "--theme", "2"])
            self.assertEqual(code, 0, err.getvalue())
            self.assertIn("admindek", out.getvalue())
            stored = (Path(home) / "database").read_text(encoding="utf-8")
            self.assertIn("OPENRBAC_THEME=admindek", stored)
            self.assertFalse((Path(home) / "openrbac.sqlite3").exists())
            err = StringIO()
            with redirect_stdout(StringIO()), redirect_stderr(err):
                code = app.run(["theme", "--theme", "oracle"])
            self.assertEqual(code, 1)
            self.assertIn("ERROR:", err.getvalue())
            self.assertIn("Next:", err.getvalue())
        finally:
            for name, value in saved.items():
                if value is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = value

    def test_menu_row_offers_the_theme(self):
        from OpenRbac.menu_painter import MenuPainter
        rows = MenuPainter().rows_for("server")
        self.assertIn((24, "theme", "11 skins, default apex", "theme"), rows)
        self.assertIn("theme", Cli.PRODUCT_VERBS)
        self.assertNotIn("theme", Cli.DOMAIN_VERBS)
        self.assertIn("theme", Tui.DOMAIN_KINDS)

    def test_server_serves_the_stored_theme(self):
        home = self._home()
        vue = WebApp(self._settings(home), None, None, None).login_page("")
        self.assertIn('href="/apex.css"', vue)
        self.assertIn('href="/themes/apex.css"', vue)
        self.assertNotIn("element-plus.css", vue)
        self.assertNotIn("openrbac.css", vue)
        self.assertIn('class="form-control"', vue)
        admin = WebApp(
            self._settings(home, OPENRBAC_THEME="fiori"),
            None,
            None,
            None,
        ).login_page("")
        self.assertIn('href="/apex.css"', admin)
        self.assertIn('href="/themes/fiori.css"', admin)
        self.assertNotIn("element-plus.css", admin)
        self.assertNotIn("openrbac.css", admin)
        self.assertIn('class="form-control"', admin)
        self.assertIn('class="btn btn-primary btn-lg"', admin)
        self.assertNotIn("<script", admin.lower())

    def test_a_running_process_reads_a_later_theme_file(self):
        home = self._home()
        settings = self._settings(home)
        self.assertEqual(settings.theme(), "apex")
        path = Path(home) / "database"
        path.write_text("OPENRBAC_THEME=directory\n", encoding="utf-8")
        os.chmod(path, 0o600)
        self.assertEqual(settings.theme(), "directory")
        page = WebApp(settings, None, None, None).login_page("")
        self.assertIn('href="/themes/directory.css"', page)
        self.assertNotIn("element-plus.css", page)

    def _handler(self, path):
        class Headers:
            def get(self, name, default=""):
                return default

        class Handler:
            def __init__(self):
                self.path = path
                self.headers = Headers()
                self.wfile = io.BytesIO()
                self.status = None
                self.sent = {}

            def send_response(self, code):
                self.status = code

            def send_header(self, key, value):
                self.sent[key] = value

            def end_headers(self):
                return None

        return Handler()

    def test_an_invalid_theme_refuses_the_sign_in_page(self):
        """requirement-html-theme — AC-8. An invalid theme is the settings error."""
        home = self._home()
        app = WebApp(self._settings(home, OPENRBAC_THEME="oracle"), None, None, None)
        handler = self._handler("/login")
        app.get(handler)
        self.assertEqual(handler.status, 400)
        text = handler.wfile.getvalue().decode("utf-8")
        self.assertIn("OPENRBAC_THEME must be one of apex, admindek, architectui, adminty, analytic, cryptocurrency, directory, finance-saas, fiori, hospital, kero.", text)
        self.assertNotIn("element-plus.css", text)
        self.assertNotIn("<html", text.lower())

    def test_listener_serves_apex_css(self):
        """requirement-html-theme — AC-9. The stylesheet is same-origin text/css."""
        home = self._home()
        app = WebApp(self._settings(home), None, None, None)
        handler = self._handler("/apex.css")
        app.get(handler)
        self.assertEqual(handler.status, 200)
        self.assertIn("text/css", handler.sent.get("Content-Type", ""))
        body = handler.wfile.getvalue().decode("utf-8")
        self.assertIn(".main-sidebar", body)
        self.assertIn("height: 100vh", body)
        self.assertNotIn("<script", body.lower())
        script = self._handler("/table-check.js")
        app.get(script)
        self.assertEqual(script.status, 200)
        self.assertIn("text/javascript", script.sent.get("Content-Type", ""))
        source = script.wfile.getvalue().decode("utf-8")
        self.assertIn("list[index].checked = box.checked", source)
        self.assertNotIn("scrollHeight", source)
        login = self._handler("/login")
        app.get(login)
        self.assertEqual(login.status, 200)
        self.assertEqual(login.sent.get("Content-Security-Policy"), CSP)
        self.assertNotIn("<script", login.wfile.getvalue().decode("utf-8").lower())
