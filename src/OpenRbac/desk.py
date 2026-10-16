# =============================================================================
# Shared command desk for the terminal and the text menu.
# requirement-rbac — one service for both surfaces.
# requirement-python-oop — class Desk.
# =============================================================================
from __future__ import annotations

from .access import Access, AccessError
from .audit_log import AuditLog
from .catalog import Catalog
from .local_login import LocalLogin
from .password_hash import PasswordHash
from .report_text import ReportText
from .schema import Schema
from .session_file import SessionFile
from .settings import Settings, SettingsError
from .store import Store, StoreError
from .web_app import WebApp


class Desk:
    """Database, session file, and the verbs both surfaces call.

    The web listener is created only when serve is chosen. A missing database
    password stays quiet until a verb asks for a connection. A domain verb,
    serve, and the text menu call ensure_database when the tables are missing.
    """

    def __init__(self, logger=None, environ=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Desk")
        self.settings = Settings(environ=environ, logger=logger)
        self.sessions = SessionFile(self.settings, logger=logger)
        self.local_login = LocalLogin(self.settings, logger=logger)
        self.store = Store(self.settings, logger=logger)
        self.audit = AuditLog(self.store, logger=logger)
        self.passwords = PasswordHash(logger=logger)
        self.access = Access(self.store, self.audit, passwords=self.passwords, logger=logger)
        self.catalog = Catalog(self.store, self.access, self.audit, logger=logger)
        self.report = ReportText(logger=logger)
        self.schema = Schema(self.store, passwords=self.passwords, logger=logger)
        self._web = None

    def web(self) -> WebApp:
        """General Purpose: The one web listener for this process."""
        if self._web is None:
            self._web = WebApp(
                self.settings,
                self.access,
                self.catalog,
                self.report,
                logger=self.logger,
                prepare=self.ensure_database,
            )
        return self._web

    def actor(self):
        """General Purpose: The account for the terminal token, or None."""
        token = self.sessions.read()
        if not token:
            return None
        return self.access.actor_from_token(token)

    def require_actor(self):
        """General Purpose: The signed-in account, or a next-step error."""
        actor = self.actor()
        if actor is None:
            raise AccessError(
                "Not signed in.",
                "open-rbac login --user-name NAME",
                logger=self.logger,
            )
        return actor

    def _need(self, options, name, nxt):
        value = getattr(options, name, "")
        if value is None or str(value).strip() == "":
            raise AccessError("{0} is required.".format(name.replace("_", "-")), nxt, logger=self.logger)
        return str(value).strip()

    def _optional(self, options, name):
        value = getattr(options, name, "")
        if value is None:
            return ""
        return str(value).strip()

    def _int(self, value, label):
        try:
            return int(str(value).strip())
        except (TypeError, ValueError):
            raise AccessError(
                "{0} must be a whole number.".format(label),
                "pass a whole number",
                logger=self.logger,
            )

    def _optional_int(self, value, label):
        if value is None or str(value).strip() == "":
            return None
        return self._int(value, label)

    def _ints(self, text, label):
        if text is None or str(text).strip() == "":
            return []
        found = []
        for part in str(text).split(","):
            part = part.strip()
            if part:
                found.append(self._int(part, label))
        return found

    def login(self, user_name, password) -> str:
        """General Purpose: Check the password, store the token, and save the local sign-in."""
        user = self.access.login(user_name, password, ipaddr="127.0.0.1", surface="cli", user_agent="open-rbac")
        self.sessions.write(user["token"])
        self.local_login.save(user["user_name"], password)
        return "Signed in as {0}.".format(user["user_name"])

    def logout(self) -> str:
        """General Purpose: Drop this terminal session and remove the saved sign-in.

        The ciphertext is removed even when the token is already gone. A missing
        token still raises Not signed in.
        """
        try:
            token = self.sessions.read()
            if not token:
                raise AccessError("Not signed in.", "open-rbac login --user-name NAME", logger=self.logger)
            self.access.logout(token)
            self.sessions.clear()
            return "Signed out."
        finally:
            self.local_login.clear()

    def restore_local(self) -> bool:
        """General Purpose: Skip a new question when the previous sign-in still works.

        A live terminal token is enough. Otherwise the saved account and password
        are decoded and tried. A failed try removes the saved sign-in.
        """
        if self.actor() is not None:
            return True
        loaded = self.local_login.load()
        if loaded is None:
            return False
        user_name, password = loaded
        try:
            self.login(user_name, password)
        except Exception:
            self.local_login.clear()
            return False
        return True

    def whoami(self) -> str:
        """General Purpose: Describe the signed-in account. No password and no token."""
        return self.access.describe(self.require_actor())

    def ensure_database(self) -> str:
        """General Purpose: Create missing tables and seed when sys_user is empty.

        A later call returns present and does not add another administrator.
        """
        return self.schema.ensure()

    def db_init(self) -> str:
        """General Purpose: Create tables and seed only when sys_user is empty."""
        state = self.ensure_database()
        return "Database {0}: {1}.".format(self.settings.storage_label(), state)

    def serve_background(self) -> str:
        """General Purpose: Start the site on a background thread and report the URL."""
        self.ensure_database()
        url = self.web().start_background()
        return "Web interface: {0}\nIt stays up while this process is open.".format(url)

    def execute(self, verb, options) -> str:
        """General Purpose: Run one domain verb and return the text to show."""
        if verb == "db-engine":
            return self.settings.apply_choice(self._optional(options, "engine"))
        if verb == "theme":
            return self.settings.apply_theme(self._optional(options, "theme"))
        if verb == "db-init":
            return self.db_init()
        self.ensure_database()
        if verb == "login":
            return self.login(
                self._need(options, "user_name", "open-rbac login --user-name NAME"),
                self._need(options, "password", "open-rbac login --user-name NAME"),
            )
        if verb == "logout":
            return self.logout()
        if verb == "whoami":
            return self.whoami()
        if verb == "serve":
            return self.serve_background()
        actor = self.require_actor()
        if verb == "user-list":
            return self.report.users(self.access.user_list(actor))
        if verb == "user-add":
            row = self.access.user_add(
                actor,
                self._need(options, "user_name", "open-rbac user-add --user-name NAME --nick-name NAME --dept-id N --role-id N"),
                self._need(options, "nick_name", "set --nick-name"),
                self._int(self._need(options, "dept_id", "set --dept-id"), "dept-id"),
                self._int(self._need(options, "role_id", "set --role-id"), "role-id"),
                self._optional(options, "password"),
            )
            return "Added {0}.".format(row["user_name"])
        if verb == "user-edit":
            nick = self._optional(options, "nick_name") or None
            dept = self._optional_int(self._optional(options, "dept_id"), "dept-id")
            status = self._optional(options, "status") or None
            if nick is None and dept is None and status is None:
                raise AccessError(
                    "user-edit needs a name, a department, or a status.",
                    "open-rbac user-edit --user-id N --nick-name NAME",
                    logger=self.logger,
                )
            row = self.access.user_edit(
                actor,
                self._int(self._need(options, "user_id", "set --user-id"), "user-id"),
                nick_name=nick,
                dept_id=dept,
                status=status,
            )
            return "Updated {0}.".format(row["user_name"])
        if verb == "user-remove":
            name = self.access.user_remove(
                actor,
                self._int(self._need(options, "user_id", "set --user-id"), "user-id"),
            )
            return "Removed {0}.".format(name)
        if verb == "user-reset-password":
            name = self.access.user_reset_password(
                actor,
                self._int(self._need(options, "user_id", "set --user-id"), "user-id"),
                self._need(options, "password", "set --password"),
            )
            return "Password updated for {0}.".format(name)
        if verb == "role-list":
            return self.report.roles(self.access.role_list(actor))
        if verb == "role-grant":
            row = self.access.role_grant(
                actor,
                self._int(self._need(options, "role_id", "set --role-id"), "role-id"),
                self._ints(self._need(options, "menu_ids", "set --menu-ids"), "menu-id"),
                data_scope=self._optional(options, "data_scope") or None,
                dept_ids=self._ints(self._optional(options, "dept_ids"), "dept-id"),
            )
            return "Granted role {0} ({1}), data_scope {2}.".format(
                row["role_id"], row["role_key"], row["data_scope"]
            )
        if verb == "menu-list":
            return self.report.menus(self.access.menu_list(actor))
        if verb == "menu-add":
            menu_id = self.access.menu_add(
                actor,
                self._need(options, "menu_name", "set --menu-name"),
                self._int(self._need(options, "parent_id", "set --parent-id"), "parent-id"),
                self._need(options, "menu_type", "set --menu-type M, C, or F"),
                self._optional(options, "perms"),
                self._optional(options, "path"),
            )
            return "Added menu {0}.".format(menu_id)
        if verb == "dept-list":
            return self.report.depts(self.access.dept_list(actor))
        if verb == "dept-add":
            dept_id = self.access.dept_add(
                actor,
                self._need(options, "dept_name", "set --dept-name"),
                self._int(self._need(options, "parent_id", "set --parent-id"), "parent-id"),
            )
            return "Added department {0}.".format(dept_id)
        if verb == "job-title-list":
            return self.report.job_titles(self.access.job_title_list(actor))
        if verb == "job-title-add":
            job_title_id = self.access.job_title_add(
                actor,
                self._need(options, "job_title_code", "set --job-title-code"),
                self._need(options, "job_title", "set --job-title"),
            )
            return "Added job title {0}.".format(job_title_id)
        if verb == "config-list":
            return self.report.configs(self.catalog.config_list(actor))
        if verb == "config-set":
            key = self.catalog.config_set(
                actor,
                self._need(options, "config_key", "set --config-key"),
                self._need(options, "config_value", "set --config-value"),
            )
            return "Set {0}.".format(key)
        if verb == "config-add":
            key = self.catalog.config_add(
                actor,
                self._need(options, "config_key", "set --config-key"),
                self._need(options, "config_name", "set --config-name"),
                self._need(options, "config_value", "set --config-value"),
            )
            return "Added parameter {0}.".format(key)
        if verb == "dict-list":
            return self.report.dicts(self.catalog.dict_list(actor))
        if verb == "dict-add":
            label = self.catalog.dict_add(
                actor,
                self._need(options, "dict_type", "set --dict-type"),
                self._need(options, "dict_label", "set --dict-label"),
                self._need(options, "dict_value", "set --dict-value"),
            )
            return "Added dictionary value {0}.".format(label)
        if verb == "notice-list":
            return self.report.notices(self.catalog.notice_list(actor))
        if verb == "notice-add":
            title = self.catalog.notice_add(
                actor,
                self._need(options, "notice_title", "set --notice-title"),
                self._optional(options, "notice_type") or "1",
                self._optional(options, "content"),
            )
            return "Added notice {0}.".format(title)
        if verb == "oper-log":
            return self.report.oper_log(self.catalog.oper_log(actor))
        if verb == "login-log":
            return self.report.login_log(self.catalog.login_log(actor))
        if verb == "online-list":
            return self.report.online(self.catalog.online_list(actor))
        if verb == "online-logout":
            count = self.catalog.online_logout(
                actor,
                self._need(options, "token", "open-rbac online-list"),
            )
            return "Closed {0} session.".format(count)
        raise AccessError(
            "Unknown verb '{0}'.".format(verb),
            "open-rbac help",
            logger=self.logger,
        )


__all__ = ["Desk", "AccessError", "SettingsError", "StoreError"]
