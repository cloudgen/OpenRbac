# =============================================================================
# Password hashes for PyRbac accounts.
# requirement-rbac — stored passwords are PBKDF2, never plaintext.
# requirement-python-oop — class PasswordHash.
# =============================================================================
from __future__ import annotations

import base64
import hashlib
import hmac
import secrets


class PasswordHash:
    """PBKDF2-HMAC-SHA256 passwords. Upstream RuoYi-FastAPI stores bcrypt.

    This class stays on the standard library. A stored value that is not this
    scheme never matches.
    """

    ITERATIONS = 260000
    PREFIX = "pbkdf2_sha256"

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="PasswordHash")

    def hash(self, password: str) -> str:
        """General Purpose: A new stored password. Each call uses a new salt."""
        salt = secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, self.ITERATIONS,
        )
        return "{0}${1}${2}${3}".format(
            self.PREFIX,
            self.ITERATIONS,
            base64.b64encode(salt).decode("ascii"),
            base64.b64encode(digest).decode("ascii"),
        )

    def verify(self, password: str, stored: str) -> bool:
        """General Purpose: True when password matches one stored value from hash()."""
        try:
            prefix, rounds, salt_b64, digest_b64 = str(stored).split("$")
            if prefix != self.PREFIX:
                return False
            salt = base64.b64decode(salt_b64.encode("ascii"))
            expected = base64.b64decode(digest_b64.encode("ascii"))
            got = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt, int(rounds),
            )
            return hmac.compare_digest(got, expected)
        except Exception:
            return False
