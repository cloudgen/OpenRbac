# Front board and the typed gate.
# Empty argv on a terminal opens the menu. Domain verbs do not.
# Row 1 is session. hello, join, and list-videos are not verbs.
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
            Cli.stdout_is_tty = previous

    def test_front_rows_and_session_layer(self):
        home = tempfile.mkdtemp(prefix="pyrbac_menu_", dir="/tmp")
        saved = os.environ.get("PYRBAC_LANG")
        os.environ.pop("PYRBAC_LANG", None)
        try:
            painter = MenuPainter(home=home)
            rows = painter.rows_for("front")
            self.assertEqual(rows[0], (1, "session", "sign in, who you are, and sign out", "session"))
            self.assertEqual(rows[2][3], "system-log")
            self.assertEqual(rows[3][3], "language")
            self.assertEqual(rows[7][3], "self-management")
            self.assertEqual(rows[8], (9, "Exit", "leave", "exit"))
            self.assertEqual(painter.rows_for("log")[0][0], 31)
            self.assertEqual(painter.rows_for("session")[0][3], "login")
            self.assertEqual(painter.display_rows("lang")[0][0], 41)
            model = MenuModel(painter=painter)
            session = MenuSession(
                "PyRbac",
                "1.0.0",
                on_version=lambda: "PyRbac 1.0.0",
                on_about=lambda: "about",
                painter=painter,
            )
            session.model = model
            self.assertIsNone(session.model.apply_key(ord("1")))
            self.assertIsNone(session.model.apply_key(10))
            self.assertEqual(model.layer, "session")
            self.assertEqual(session.take_action("login"), "stay")
        finally:
            if saved is None:
                os.environ.pop("PYRBAC_LANG", None)
            else:
                os.environ["PYRBAC_LANG"] = saved
