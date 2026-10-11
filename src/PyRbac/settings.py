# =============================================================================
# Process settings for PyRbac.
# requirement-environment — names, defaults, and the mode-0600 password file.
# requirement-python-oop — class Settings and SettingsError.
# =============================================================================
from __future__ import annotations

import os


class SettingsError(Exception):
    """A missing or refused setting. The next step is for the operator."""

    def __init__(self, message, nxt, logger=None):
        super().__init__(message)
        self.logger = logger
        self.nxt = nxt
        if logger is not None:
            logger.log_message("instantiated", component="SettingsError")


class Settings:
    """Environment values for the database, the web bind, and the home folder.

    The environment wins. A mode-0600 file supplies a key only when the
    environment value is missing. Defaults never include a password.
    """

    APP_DIR = "PyRbac"
    FILE_NAME = "database"
    DEFAULTS = {
        "PYRBAC_DB_HOST": "127.0.0.1",
        "PYRBAC_DB_PORT": "3306",
        "PYRBAC_DB_USER": "pyrbac",
        "PYRBAC_DB_NAME": "pyrbac",
        "PYRBAC_BIND": "127.0.0.1",
        "PYRBAC_PORT": "8765",
    }
    LOOPBACK = ("127.0.0.1", "localhost", "::1")

    def __init__(self, environ=None, home=None, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Settings")
        if environ is None:
            environ = os.environ
        self.environ = environ
        if home is None:
            home = self.environ.get("HOME", "")
        self.home = home
        self._file_cache = None

    def app_home(self) -> str:
        """General Purpose: The folder that holds the language leaf, the session, and the database file."""
        override = self.environ.get("PYRBAC_HOME", "")
        if override:
            return override
        if not self.home:
            return ""
        return os.path.join(self.home, ".local", self.APP_DIR)

    def database_file(self) -> str:
        folder = self.app_home()
        if not folder:
            return ""
        return os.path.join(folder, self.FILE_NAME)

    def _file_map(self) -> dict:
        if self._file_cache is not None:
            return self._file_cache
        found = {}
        path = self.database_file()
        if path and os.path.isfile(path):
            mode = os.stat(path).st_mode & 0o777
            if mode != 0o600:
                self._file_cache = {}
                return self._file_cache
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    lines = handle.read().splitlines()
            except OSError:
                lines = []
            for line in lines:
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                found[key.strip()] = value
        self._file_cache = found
        return found

    def get(self, name: str) -> str:
        """General Purpose: One setting. Environment, then the 0600 file, then a default."""
        current = self.environ.get(name, "")
        if current != "":
            return current
        filed = self._file_map().get(name, "")
        if filed != "":
            return filed
        return self.DEFAULTS.get(name, "")

    def password(self) -> str:
        """General Purpose: The database password. Empty when neither source has it."""
        return self.get("PYRBAC_DB_PASSWORD")

    def require_password(self) -> str:
        value = self.password()
        if value:
            return value
        raise SettingsError(
            "The database password is not set.",
            "export PYRBAC_DB_PASSWORD and run py-rbac db-init",
            logger=self.logger,
        )

    def database(self) -> dict:
        """General Purpose: The MySQL connection values. The password is required."""
        name = self.get("PYRBAC_DB_NAME")
        if not name or not all(ch.isalnum() or ch == "_" for ch in name):
            raise SettingsError(
                "PYRBAC_DB_NAME must be letters, digits, and underscores.",
                "export PYRBAC_DB_NAME=pyrbac",
                logger=self.logger,
            )
        try:
            port = int(self.get("PYRBAC_DB_PORT"))
        except ValueError:
            port = 0
        if port < 1 or port > 65535:
            raise SettingsError(
                "PYRBAC_DB_PORT must be a port number.",
                "export PYRBAC_DB_PORT=3306",
                logger=self.logger,
            )
        return {
            "host": self.get("PYRBAC_DB_HOST"),
            "port": port,
            "user": self.get("PYRBAC_DB_USER"),
            "password": self.require_password(),
            "database": name,
        }

    def bind(self) -> tuple:
        """General Purpose: Web bind address and port. Non-loopback needs an explicit allow."""
        host = self.get("PYRBAC_BIND")
        try:
            port = int(self.get("PYRBAC_PORT"))
        except ValueError:
            port = -1
        if port < 0 or port > 65535:
            raise SettingsError(
                "PYRBAC_PORT must be a port number. 0 asks the system for a free port.",
                "export PYRBAC_PORT=8765",
                logger=self.logger,
            )
        if host not in self.LOOPBACK and self.environ.get("PYRBAC_ALLOW_REMOTE", "") != "yes":
            raise SettingsError(
                "Refusing to listen on {0}.".format(host),
                "keep PYRBAC_BIND=127.0.0.1, or export PYRBAC_ALLOW_REMOTE=yes",
                logger=self.logger,
            )
        return host, port
