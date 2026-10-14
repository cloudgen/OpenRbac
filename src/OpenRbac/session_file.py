# =============================================================================
# Terminal session token file.
# requirement-environment — ~/.local/OpenRbac/session mode 0600.
# requirement-rbac — the token matches a sys_session row.
# requirement-python-oop — class SessionFile.
# =============================================================================
from __future__ import annotations

import os


class SessionFile:
    """The token for this terminal. The web interface uses a cookie instead."""

    NAME = "session"

    def __init__(self, settings, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="SessionFile")
        self.settings = settings

    def path(self) -> str:
        folder = self.settings.app_home()
        if not folder:
            return ""
        return os.path.join(folder, self.NAME)

    def read(self) -> str:
        """General Purpose: The token, or empty when the file is missing or not mode 0600."""
        path = self.path()
        if not path or not os.path.isfile(path):
            return ""
        mode = os.stat(path).st_mode & 0o777
        if mode != 0o600:
            return ""
        try:
            with open(path, "r", encoding="utf-8") as handle:
                return handle.read().strip()
        except OSError:
            return ""

    def write(self, token: str) -> None:
        """General Purpose: Replace the token file. The directory is mode 0700."""
        path = self.path()
        if not path:
            raise OSError("no home for the session file")
        folder = os.path.dirname(path)
        os.makedirs(folder, mode=0o700, exist_ok=True)
        os.chmod(folder, 0o700)
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            os.write(descriptor, (token + "\n").encode("utf-8"))
        finally:
            os.close(descriptor)
        os.chmod(path, 0o600)

    def clear(self) -> None:
        """General Purpose: Remove the token file. A missing file is success."""
        path = self.path()
        if path and os.path.isfile(path):
            os.remove(path)
