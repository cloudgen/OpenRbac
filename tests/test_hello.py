# Front board and the typed gate.
# Empty argv on a terminal opens the menu. Domain verbs do not.
# The front board starts at rbac. hello, join, and list-videos are not verbs.
import os
import sys
import tempfile
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from OpenRbac.cli import Cli
from OpenRbac.menu_model import MenuModel
from OpenRbac.menu_painter import MenuPainter
from OpenRbac.menu_session import MenuSession
from OpenRbac.tui import Tui


class TestFrontBoard(unittest.TestCase):
    """The inherited rows stay, and the RBAC rows sit beside them."""

    def test_cli_gate_skips_the_menu_for_domain_verbs(self):
        self.assertIn("login", Cli.PRODUCT_VERBS)
        self.assertIn("serve", Cli.PRODUCT_VERBS)
        self.assertIn("db-init", Cli.PRODUCT_VERBS)
        self.assertNotIn("hello", Cli.PRODUCT_VERBS)
        self.assertNotIn("join", Cli.PRODUCT_VERBS)
        self.assertNotIn("list-videos", Cli.PRODUCT_VERBS)
        self.assertNotIn("language", Cli.PRODUCT_VERBS)
        previous = Cli.stdout_is_tty
        Cli.stdout_is_tty = staticmethod(lambda: True)
        try:
            self.assertTrue(Cli.opens_text_screen([]))
            self.assertTrue(Cli.opens_text_screen(["about"]))
            self.assertFalse(Cli.opens_text_screen(["login"]))
            self.assertFalse(Cli.opens_text_screen(["login", "--user-name", "admin"]))
            self.assertFalse(Cli.opens_text_screen(["serve"]))
            self.assertFalse(Cli.opens_text_screen(["help"]))
            self.assertFalse(Cli.opens_text_screen(["version"]))
            self.assertFalse(Cli.opens_text_screen(["self-update"]))
        finally:
            Cli.stdout_is_tty = staticmethod(previous)

    def test_front_rows_have_no_session(self):
        home = tempfile.mkdtemp(prefix="openrbac_menu_", dir="/tmp")
        saved = os.environ.get("OPENRBAC_LANG")
        os.environ.pop("OPENRBAC_LANG", None)
        try:
            painter = MenuPainter(home=home)
            rows = painter.rows_for("front")
            kinds = [row[3] for row in rows]
            self.assertNotIn("session", kinds)
            self.assertEqual(rows[0], (1, "rbac", "users, roles, menus, departments, and posts", "rbac"))
            self.assertEqual(rows[1], (2, "server", "setup, audit, and the web listener", "server"))
            self.assertEqual(rows[2][3], "system-log")
            self.assertEqual(rows[3], (6, "self-management", "version, about, and pip lifecycle", "self-management"))
            self.assertEqual(rows[4], (7, "language", "display language for this menu", "language"))
            self.assertEqual(rows[5], (9, "Exit", "leave", "exit"))
            self.assertEqual([row[0] for row in rows], [1, 2, 3, 6, 7, 9])
            self.assertEqual(painter.rows_for("rbac")[0][0], 11)
            self.assertEqual(painter.rows_for("rbac")[9][0], 110)
            self.assertEqual([row[0] for row in painter.rows_for("server")], [21, 22, 23, 0])
            self.assertEqual(painter.rows_for("setup")[-2], (218, "db-engine", "sqlite3 file or mysql", "db-engine"))
            self.assertEqual(painter.rows_for("audit")[0][0], 221)
            self.assertEqual(painter.rows_for("self")[0][0], 62)
            self.assertEqual(painter.rows_for("log")[0][0], 31)
            self.assertEqual(painter.display_rows("lang")[0][0], 71)
            model = MenuModel(painter=painter)
            session = MenuSession(
                "OpenRbac",
                "1.0.1",
                on_version=lambda: "OpenRbac 1.0.1",
                on_about=lambda: "about",
                painter=painter,
            )
            session.model = model
            self.assertIsNone(session.model.apply_key(ord("4")))
            self.assertIsNone(session.model.apply_key(10))
            self.assertEqual(model.layer, "front")
            self.assertIn("not on this list", model.error)
            model.error = ""
            self.assertIsNone(session.model.apply_key(ord("2")))
            self.assertIsNone(session.model.apply_key(10))
            self.assertEqual(model.layer, "server")
            self.assertIsNone(session.model.apply_key(ord("2")))
            self.assertIsNone(session.model.apply_key(ord("1")))
            self.assertIsNone(session.model.apply_key(10))
            self.assertEqual(model.layer, "setup")
            self.assertIsNone(session.model.apply_key(ord("0")))
            self.assertIsNone(session.model.apply_key(10))
            self.assertEqual(model.layer, "server")
            self.assertIsNone(session.model.apply_key(ord("0")))
            self.assertIsNone(session.model.apply_key(10))
            self.assertEqual(model.layer, "front")
        finally:
            if saved is None:
                os.environ.pop("OPENRBAC_LANG", None)
            else:
                os.environ["OPENRBAC_LANG"] = saved

    def test_login_gate_asks_before_the_menu(self):
        class Desk:
            def __init__(self):
                self.calls = []

            def login(self, user_name, password):
                self.calls.append((user_name, password))
                if password != "admin123":
                    raise RuntimeError("Unknown account or wrong password.")
                return {"user_name": user_name}

        class App:
            def __init__(self):
                self.desk = Desk()

        tui = Tui(app=App())
        seen = []
        answers = [
            {"user_name": "admin", "password": "nope"},
            {"user_name": "admin", "password": "admin123"},
        ]

        def ask(lines):
            seen.append(list(lines))
            return answers.pop(0)

        self.assertTrue(tui.login_gate(ask, state="seeded", database_name="openrbac_test"))
        self.assertIn("Database openrbac_test: seeded.", seen[0])
        self.assertIn("ERROR: Unknown account or wrong password.", seen[1])
        self.assertEqual(tui.app.desk.calls, [("admin", "nope"), ("admin", "admin123")])
        self.assertFalse(tui.login_gate(lambda lines: None, state="present"))
