# Front board and the typed gate.
# Empty argv on a terminal opens the menu. Domain verbs do not.
# The front board starts at access. hello, join, and list-videos are not verbs.
import os
import sys
import tempfile
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from PyRbac.cli import Cli
from PyRbac.menu_model import MenuModel
from PyRbac.menu_painter import MenuPainter
from PyRbac.menu_session import MenuSession
from PyRbac.tui import Tui


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
        home = tempfile.mkdtemp(prefix="pyrbac_menu_", dir="/tmp")
        saved = os.environ.get("PYRBAC_LANG")
        os.environ.pop("PYRBAC_LANG", None)
        try:
            painter = MenuPainter(home=home)
            rows = painter.rows_for("front")
            kinds = [row[3] for row in rows]
            self.assertNotIn("session", kinds)
            self.assertEqual(rows[0], (2, "access", "users, roles, menus, departments, and posts", "access"))
            self.assertEqual(rows[1][3], "system-log")
            self.assertEqual(rows[2][3], "language")
            self.assertEqual(rows[6][3], "self-management")
            self.assertEqual(rows[7], (9, "Exit", "leave", "exit"))
            self.assertEqual([row[0] for row in rows], [2, 3, 4, 5, 6, 7, 8, 9])
            self.assertEqual(painter.rows_for("log")[0][0], 31)
            self.assertEqual(painter.display_rows("lang")[0][0], 41)
            model = MenuModel(painter=painter)
            session = MenuSession(
                "PyRbac",
                "1.0.1",
                on_version=lambda: "PyRbac 1.0.1",
                on_about=lambda: "about",
                painter=painter,
            )
            session.model = model
            self.assertIsNone(session.model.apply_key(ord("1")))
            self.assertIsNone(session.model.apply_key(10))
            self.assertEqual(model.layer, "front")
            self.assertIn("not on this list", model.error)
        finally:
            if saved is None:
                os.environ.pop("PYRBAC_LANG", None)
            else:
                os.environ["PYRBAC_LANG"] = saved

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

        self.assertTrue(tui.login_gate(ask, state="seeded", database_name="pyrbac_test"))
        self.assertIn("Database pyrbac_test: seeded.", seen[0])
        self.assertIn("ERROR: Unknown account or wrong password.", seen[1])
        self.assertEqual(tui.app.desk.calls, [("admin", "nope"), ("admin", "admin123")])
        self.assertFalse(tui.login_gate(lambda lines: None, state="present"))
