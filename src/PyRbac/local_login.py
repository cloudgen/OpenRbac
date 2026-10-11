# =============================================================================
# Encrypted local sign-in for the next start.
# requirement-local-login — ciphertext and key, both mode 0600.
# requirement-python-oop — class LocalLogin.
# =============================================================================
from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets
import struct


class LocalLogin:
    """Account and password stored so the next start can try them again.

    The login file is ciphertext. The key is a separate file. Both are mode
    0600. A person who can read only the login file does not see the password.
    A person who can read both files can. The log never receives the password.
    """

    FILE_NAME = "local-login"
    KEY_NAME = "local-login-key"
    MAGIC = "PYRBACLOCAL1"
    KEY_SIZE = 32
    NONCE_SIZE = 16

    def __init__(self, settings, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="LocalLogin")
        self.settings = settings

    def path(self) -> str:
        """General Purpose: The ciphertext file, or empty when there is no home."""
        return self._join(self.FILE_NAME)

    def key_path(self) -> str:
        """General Purpose: The key file, or empty when there is no home."""
        return self._join(self.KEY_NAME)

    def present(self) -> bool:
        """General Purpose: True when a ciphertext file exists, whatever its mode."""
        path = self.path()
        return bool(path) and os.path.isfile(path)

    def load(self):
        """General Purpose: The account and password, or None when unusable.

        A missing file, a file that is not mode 0600, and a bad check all
        return None. This does not delete the file.
        """
        path = self.path()
        key = self._read_key()
        if not path or not key or not self._private(path):
            if path and os.path.isfile(path) and not self._private(path):
                self._rejected()
            return None
        try:
            with open(path, "r", encoding="utf-8") as handle:
                text = handle.read()
        except OSError:
            self._rejected()
            return None
        parts = self._split(text)
        if parts is None:
            self._rejected()
            return None
        nonce, mac, ciphertext = parts
        expect = self._mac(key, nonce, ciphertext)
        if not hmac.compare_digest(mac, expect):
            self._rejected()
            return None
        plain = self._xor(ciphertext, self._keystream(key, nonce, len(ciphertext)))
        loaded = self._unpack(plain)
        if loaded is None:
            self._rejected()
        return loaded

    def save(self, user_name, password) -> None:
        """General Purpose: Replace the ciphertext. The folder is mode 0700."""
        path = self.path()
        if not path:
            raise OSError("no home for the local login")
        key = self._ensure_key()
        plain = self._pack(user_name, password)
        nonce = secrets.token_bytes(self.NONCE_SIZE)
        ciphertext = self._xor(plain, self._keystream(key, nonce, len(plain)))
        mac = self._mac(key, nonce, ciphertext)
        body = "\n".join(
            (
                self.MAGIC,
                base64.b64encode(nonce).decode("ascii"),
                base64.b64encode(mac).decode("ascii"),
                base64.b64encode(ciphertext).decode("ascii"),
                "",
            )
        )
        self._write(path, body.encode("utf-8"))
        if self.logger is not None:
            self.logger.log_message("saved local login", component="LocalLogin")

    def clear(self) -> None:
        """General Purpose: Remove the ciphertext. A missing file is success.

        The key file stays so the next save can use it. A key that is not
        mode 0600 is replaced on that next save.
        """
        path = self.path()
        if not path or not os.path.isfile(path):
            return
        os.remove(path)
        if self.logger is not None:
            self.logger.log_message("cleared local login", component="LocalLogin")

    def _join(self, name: str) -> str:
        folder = self.settings.app_home()
        if not folder:
            return ""
        return os.path.join(folder, name)

    def _rejected(self) -> None:
        if self.logger is not None:
            self.logger.log_message("rejected local login", component="LocalLogin")

    def _private(self, path: str) -> bool:
        if not path or not os.path.isfile(path):
            return False
        return (os.stat(path).st_mode & 0o777) == 0o600

    def _read_key(self) -> bytes:
        path = self.key_path()
        if not self._private(path):
            return b""
        try:
            with open(path, "rb") as handle:
                key = handle.read()
        except OSError:
            return b""
        if len(key) != self.KEY_SIZE:
            return b""
        return key

    def _ensure_key(self) -> bytes:
        key = self._read_key()
        if key:
            return key
        path = self.key_path()
        if not path:
            raise OSError("no home for the local login")
        key = secrets.token_bytes(self.KEY_SIZE)
        self._write(path, key)
        return key

    def _write(self, path: str, data: bytes) -> None:
        folder = os.path.dirname(path)
        os.makedirs(folder, mode=0o700, exist_ok=True)
        os.chmod(folder, 0o700)
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            os.write(descriptor, data)
        finally:
            os.close(descriptor)
        os.chmod(path, 0o600)

    def _pack(self, user_name, password) -> bytes:
        user = str(user_name).encode("utf-8")
        secret = str(password).encode("utf-8")
        if len(user) > 65535 or len(secret) > 65535:
            raise OSError("The account name or the password is too long.")
        return struct.pack(">HH", len(user), len(secret)) + user + secret

    def _unpack(self, blob: bytes):
        if len(blob) < 4:
            return None
        user_len, secret_len = struct.unpack(">HH", blob[:4])
        body = blob[4:]
        if user_len + secret_len != len(body):
            return None
        try:
            user_name = body[:user_len].decode("utf-8")
            password = body[user_len:].decode("utf-8")
        except UnicodeDecodeError:
            return None
        return user_name, password

    def _split(self, text: str):
        lines = [line.strip() for line in text.splitlines() if line.strip() != ""]
        if len(lines) != 4 or lines[0] != self.MAGIC:
            return None
        try:
            nonce = base64.b64decode(lines[1], validate=True)
            mac = base64.b64decode(lines[2], validate=True)
            ciphertext = base64.b64decode(lines[3], validate=True)
        except (ValueError, TypeError):
            return None
        if len(nonce) != self.NONCE_SIZE or len(mac) != 32:
            return None
        return nonce, mac, ciphertext

    def _mac(self, key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
        return hmac.new(
            key,
            b"pyrbac-local-login-mac" + nonce + ciphertext,
            hashlib.sha256,
        ).digest()

    def _keystream(self, key: bytes, nonce: bytes, size: int) -> bytes:
        parts = []
        counter = 0
        filled = 0
        while filled < size:
            block = hmac.new(
                key,
                b"pyrbac-local-login-stream" + nonce + struct.pack(">Q", counter),
                hashlib.sha256,
            ).digest()
            parts.append(block)
            filled += len(block)
            counter += 1
        return b"".join(parts)[:size]

    def _xor(self, left: bytes, right: bytes) -> bytes:
        return bytes(a ^ b for a, b in zip(left, right))
