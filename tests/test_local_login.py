# Saved sign-in and the Exit question.
# requirement-local-login. Uses a temporary sqlite3 file. Does not write ruoyi_db or ry.
import http.client
import os
import sys
import tempfile
import unittest
import urllib.parse
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from PyRbac.access import AccessError
from PyRbac.desk import Desk
from PyRbac.local_login import LocalLogin
from PyRbac.menu_model import MenuModel
from PyRbac.menu_painter import MenuPainter
from PyRbac.menu_session import MenuSession
from PyRbac.password_hash import PasswordHash
from PyRbac.schema import Schema
from PyRbac.tui import Tui


class Capture:
    def __init__(self):
        self.messages = []

    def log_message(self, message, **kwargs):
        self.messages.append("{0} {1}".format(message, sorted(kwargs.items())))


class Home:
    def __init__(self, folder):
        self.folder = folder

    def app_home(self):
        return self.folder


def _env(home):
    return {
        "PYRBAC_HOME": home,
        "HOME": home,
        "PYRBAC_DB_ENGINE": "sqlite3",
        "PYRBAC_SQLITE_FILE": os.path.join(home, "pyrbac.sqlite3"),
        "PYRBAC_BIND": "127.0.0.1",
        "PYRBAC_PORT": "0",
    }


class TestLocalCipher(unittest.TestCase):
    """The login file is ciphertext. A bad file does not return the password."""

    def test_round_trip_mode_and_tamper(self):
        home = tempfile.mkdtemp(prefix="pyrbac_local_", dir="/tmp")
        logger = Capture()
        local = LocalLogin(Home(home), logger=logger)
        local.save("admin", "admin123")
        login_path = os.path.join(home, "local-login")
        key_path = os.path.join(home, "local-login-key")
        self.assertEqual(os.stat(login_path).st_mode & 0o777, 0o600)
        self.assertEqual(os.stat(key_path).st_mode & 0o777, 0o600)
        self.assertEqual(os.stat(home).st_mode & 0o777, 0o700)
        body = Path(login_path).read_bytes()
        self.assertNotIn(b"admin123", body)
        self.assertTrue(body.startswith(b"PYRBACLOCAL1\n"))
        self.assertEqual(local.load(), ("admin", "admin123"))
        self.assertEqual(len(Path(key_path).read_bytes()), 32)
        joined = "\n".join(logger.messages)
        self.assertIn("saved local login", joined)
        self.assertNotIn("admin123", joined)

        os.chmod(login_path, 0o644)
        self.assertIsNone(local.load())
        os.chmod(login_path, 0o600)
        self.assertEqual(local.load(), ("admin", "admin123"))
        lines = Path(login_path).read_text(encoding="utf-8").splitlines()
        lines[2] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
        Path(login_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
        os.chmod(login_path, 0o600)
        self.assertIsNone(local.load())

        local.save("admin", "admin123")
        os.chmod(key_path, 0o644)
        self.assertIsNone(local.load())
        local.save("admin", "next-secret")
        self.assertEqual(os.stat(key_path).st_mode & 0o777, 0o600)
        self.assertEqual(local.load(), ("admin", "next-secret"))
        local.clear()
        self.assertFalse(os.path.isfile(login_path))
        self.assertTrue(os.path.isfile(key_path))
        self.assertIsNone(local.load())

    def test_empty_home_and_long_password(self):
        local = LocalLogin(Home(""))
        self.assertIsNone(local.load())
        with self.assertRaises(OSError):
            local.save("admin", "admin123")
        home = tempfile.mkdtemp(prefix="pyrbac_local_", dir="/tmp")
        local = LocalLogin(Home(home))
        with self.assertRaises(OSError) as caught:
            local.save("admin", "x" * 65536)
        self.assertIn("too long", str(caught.exception))
        self.assertNotIn("x" * 40, str(caught.exception))


class TestSavedSignIn(unittest.TestCase):
    """Desk stores the sign-in. A later desk can use it. The web page does not."""

    def _desk(self, home, logger=None):
        desk = Desk(logger=logger, environ=_env(home))
        desk.ensure_database()
        return desk

    def test_restore_logout_and_failed_password(self):
        home = tempfile.mkdtemp(prefix="pyrbac_local_", dir="/tmp")
        logger = Capture()
        desk = self._desk(home, logger)
        secret = Schema.INITIAL_ADMIN_PASSWORD
        self.assertIn("admin", desk.login("admin", secret))
        login_path = os.path.join(home, "local-login")
        self.assertNotIn(secret.encode("utf-8"), Path(login_path).read_bytes())
        desk.sessions.clear()
        other = self._desk(home, logger)
        self.assertIsNone(other.actor())
        self.assertTrue(other.restore_local())
        self.assertIn("user_name=admin", other.whoami())

        note = other.logout()
        self.assertEqual(note, "Signed out.")
        self.assertFalse(os.path.isfile(login_path))
        self.assertIsNone(other.actor())

        desk.login("admin", secret)
        self.assertTrue(os.path.isfile(login_path))
        desk.sessions.clear()
        with self.assertRaises(AccessError):
            desk.logout()
        self.assertFalse(os.path.isfile(login_path))

        desk.login("admin", secret)
        desk.store.execute(
            "UPDATE sys_user SET password = %s WHERE user_name = %s",
            (PasswordHash().hash("other-secret-value"), "admin"),
        )
        desk.sessions.clear()
        failed = self._desk(home, logger)
        self.assertFalse(failed.restore_local())
        self.assertFalse(os.path.isfile(login_path))
        joined = "\n".join(logger.messages)
        self.assertNotIn(secret, joined)
        self.assertNotIn("other-secret-value", joined)

    def test_live_token_skips_a_broken_file(self):
        home = tempfile.mkdtemp(prefix="pyrbac_local_", dir="/tmp")
        desk = self._desk(home)
        desk.login("admin", Schema.INITIAL_ADMIN_PASSWORD)
        path = os.path.join(home, "local-login")
        os.chmod(path, 0o600)
        Path(path).write_text("broken\n", encoding="utf-8")
        os.chmod(path, 0o600)
        other = self._desk(home)
        self.assertTrue(other.restore_local())
        self.assertIn("user_name=admin", other.whoami())

    def test_web_sign_in_does_not_write_the_file(self):
        home = tempfile.mkdtemp(prefix="pyrbac_local_", dir="/tmp")
        desk = self._desk(home)
        url = desk.web().start_background()
        try:
            parsed = urllib.parse.urlparse(url)
            body = urllib.parse.urlencode(
                {
                    "user_name": "admin",
                    "password": Schema.INITIAL_ADMIN_PASSWORD,
                }
            )
            connection = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=5)
            connection.request(
                "POST",
                "/login",
                body,
                {"Content-Type": "application/x-www-form-urlencoded"},
            )
            response = connection.getresponse()
            response.read()
            self.assertIn(response.status, (302, 303))
            connection.close()
            self.assertFalse(os.path.isfile(os.path.join(home, "local-login")))
            self.assertFalse(os.path.isfile(os.path.join(home, "session")))
        finally:
            desk.web().stop()


class TestExitQuestion(unittest.TestCase):
    """Row 9 asks. End of input does not."""

    def test_exit_callback_and_end_of_input(self):
        home = tempfile.mkdtemp(prefix="pyrbac_exit_", dir="/tmp")
        painter = MenuPainter(home=home)
        model = MenuModel(painter=painter)
        self.assertEqual(model.apply_key(-1), "exit-now")
        model.layer = "access"
        self.assertIsNone(model.apply_key(-1))
        self.assertEqual(model.layer, "front")
        self.assertEqual(model._activate(9, "exit"), "exit")

        calls = []

        def on_exit():
            calls.append("ask")
            return "stay"

        session = MenuSession(
            "PyRbac",
            "1.0.4",
            on_version=lambda: "PyRbac 1.0.4",
            on_about=lambda: "about",
            painter=painter,
            on_exit=on_exit,
        )
        session.model = model
        self.assertEqual(session.take_action("exit"), "stay")
        self.assertEqual(session.take_action("exit-now"), "exit")
        self.assertEqual(calls, ["ask"])
        session.on_exit = lambda: "leave"
        self.assertEqual(session.take_action("exit"), "exit")

    def test_exit_choice_logout_keep_and_stay(self):
        class Local:
            def __init__(self):
                self.present_file = True

            def present(self):
                return self.present_file

        class DeskBox:
            def __init__(self):
                self.logged_out = 0
                self.local_login = Local()

            def logout(self):
                self.logged_out += 1
                self.local_login.present_file = False
                return "Signed out."

            def restore_local(self):
                return False

        class App:
            def __init__(self):
                self.desk = DeskBox()

        class Box:
            error = ""

        app = App()
        tui = Tui(app=app)
        seen = []

        def read_key(_screen, _model, lines, title="menu"):
            seen.append((title, list(lines)))
            return answers.pop(0)

        tui.read_key = read_key
        answers = [""]
        self.assertEqual(tui._exit_choice(None, Box()), "leave")
        self.assertEqual(app.desk.logged_out, 1)
        self.assertEqual(seen[0][0], "exit")
        self.assertIn("removes the saved sign-in", seen[0][1][1])

        answers = ["y"]
        self.assertEqual(tui._exit_choice(None, Box()), "leave")
        self.assertEqual(app.desk.logged_out, 2)

        answers = ["n"]
        self.assertEqual(tui._exit_choice(None, Box()), "leave")
        self.assertEqual(app.desk.logged_out, 2)

        answers = [None]
        self.assertEqual(tui._exit_choice(None, Box()), "stay")
        self.assertEqual(app.desk.logged_out, 2)

        answers = ["maybe", "yes"]
        self.assertEqual(tui._exit_choice(None, Box()), "leave")
        self.assertEqual(app.desk.logged_out, 3)

        def boom():
            raise RuntimeError("Not signed in.")

        app.desk.logout = boom
        answers = [""]
        self.assertEqual(tui._exit_choice(None, Box()), "leave")

    def test_restore_skips_the_question(self):
        class DeskBox:
            def __init__(self, ok):
                self.ok = ok
                self.local_login = self

            def present(self):
                return not self.ok

            def restore_local(self):
                if self.ok:
                    return True
                raise RuntimeError("disk")

        asked = []

        def ask(lines):
            asked.append(list(lines))
            return None

        tui = Tui(app=type("App", (), {"desk": DeskBox(True)})())
        self.assertTrue(tui.sign_in_or_restore(ask, state="present"))
        self.assertEqual(asked, [])

        tui = Tui(app=type("App", (), {"desk": DeskBox(False)})())
        self.assertFalse(tui.sign_in_or_restore(ask, state="seeded", database_name="pyrbac_test"))
        self.assertIn("The saved sign-in did not match.", asked[0])
        self.assertIn("Database pyrbac_test: seeded.", asked[0])


if __name__ == "__main__":
    unittest.main()
