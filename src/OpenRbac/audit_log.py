# =============================================================================
# Login log, operation log, and online sessions.
# requirement-rbac — audit rows and online users.
# requirement-python-cli-logging — the status logger is separate from these tables.
# requirement-python-oop — class AuditLog.
# =============================================================================
from __future__ import annotations


class AuditLog:
    """Rows in sys_logininfor, sys_oper_log, and sys_session.

    Passwords are never written into these rows.
    """

    def __init__(self, store, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="AuditLog")
        self.store = store

    def write_login(self, user_name, ipaddr, status, message, browser="open-rbac", os_name=""):
        """General Purpose: One login attempt. status 0 succeeded. status 1 failed."""
        self.store.execute(
            """
            INSERT INTO sys_logininfor
              (user_name, ipaddr, browser, os, status, msg, login_time)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """,
            (user_name or "", ipaddr or "", browser or "", os_name or "", status, message or ""),
        )

    def write_oper(self, actor, title, business_type, method, status=0, error_msg="", param=""):
        """General Purpose: One mutation. business_type 1 add, 2 edit, 3 remove."""
        name = ""
        dept = ""
        if actor:
            name = actor.get("user_name") or ""
            dept = actor.get("dept_name") or ""
        self.store.execute(
            """
            INSERT INTO sys_oper_log
              (title, business_type, method, request_method, operator_type,
               oper_name, dept_name, oper_param, status, error_msg, oper_time)
            VALUES (%s, %s, %s, 'CALL', 1, %s, %s, %s, %s, %s, NOW())
            """,
            (title, int(business_type), method, name, dept, (param or "")[:2000], int(status), (error_msg or "")[:2000]),
        )
        if self.logger is not None:
            self.logger.log_message(
                "{0} {1} by {2}".format(title, method, name or "unknown"),
                component="AuditLog",
            )

    def login_rows(self, limit=100):
        """General Purpose: Newest login rows."""
        return self.store.query_all(
            """
            SELECT info_id, user_name, ipaddr, login_location, browser, os,
                   status, msg, login_time
            FROM sys_logininfor
            ORDER BY info_id DESC
            LIMIT %s
            """,
            (int(limit),),
        )

    def oper_rows(self, limit=100):
        """General Purpose: Newest operation rows."""
        return self.store.query_all(
            """
            SELECT oper_id, title, business_type, method, oper_name, status, oper_time
            FROM sys_oper_log
            ORDER BY oper_id DESC
            LIMIT %s
            """,
            (int(limit),),
        )

    def open_session(self, token, user, ipaddr, user_agent, csrf, surface):
        """General Purpose: Remember one signed-in session."""
        self.store.execute(
            """
            INSERT INTO sys_session
              (token, user_id, user_name, ipaddr, user_agent, csrf, surface,
               login_time, last_access)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """,
            (
                token,
                user["user_id"],
                user["user_name"],
                ipaddr or "",
                (user_agent or "")[:200],
                csrf,
                surface,
            ),
        )

    def touch(self, token):
        """General Purpose: Move last_access forward."""
        self.store.execute(
            "UPDATE sys_session SET last_access = NOW() WHERE token = %s",
            (token,),
        )

    def session_row(self, token):
        """General Purpose: One session, or None."""
        if not token:
            return None
        return self.store.query_one(
            """
            SELECT token, user_id, user_name, ipaddr, user_agent, csrf, surface,
                   login_time, last_access
            FROM sys_session
            WHERE token = %s
            """,
            (token,),
        )

    def online_rows(self):
        """General Purpose: Every current session."""
        return self.store.query_all(
            """
            SELECT token, user_id, user_name, ipaddr, surface, login_time, last_access
            FROM sys_session
            ORDER BY last_access DESC
            """
        )

    def drop_session(self, token):
        """General Purpose: Remove one session. Returns how many rows changed."""
        done = self.store.execute(
            "DELETE FROM sys_session WHERE token = %s",
            (token,),
        )
        return int(done["rowcount"] or 0)
