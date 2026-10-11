# =============================================================================
# RBAC commands shared by the terminal, the text menu, and the web interface.
# requirement-rbac — users, roles, menus, departments, posts, data scope.
# requirement-python-oop — class Access and AccessError.
# =============================================================================
from __future__ import annotations

import re
import secrets

from .password_hash import PasswordHash


class AccessError(Exception):
    """The signed-in account cannot complete this RBAC action."""

    def __init__(self, message, nxt, logger=None):
        super().__init__(message)
        self.logger = logger
        self.nxt = nxt
        if logger is not None:
            logger.log_message("instantiated", component="AccessError")


class Access:
    """Users, roles, menus, departments, and posts.

    Data scope is 1 all, 2 custom departments, 3 this department, and 4 this
    department and children. Any other scope contributes no rows. role_key
    admin bypasses permission and scope.
    """

    USER_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]{2,29}$")
    SCOPES = ("1", "2", "3", "4")
    PROTECTED_USER = 1
    PROTECTED_ROLE = 1

    def __init__(self, store, audit, passwords=None, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Access")
        self.store = store
        self.audit = audit
        self.passwords = passwords or PasswordHash(logger=logger)
        self._dummy = self.passwords.hash("not-a-real-password")

    def _fail(self, message, nxt):
        raise AccessError(message, nxt, logger=self.logger)

    def roles_of(self, user_id):
        return self.store.query_all(
            """
            SELECT r.role_id, r.role_key, r.role_name, r.data_scope, r.status
            FROM sys_role r
            JOIN sys_user_role ur ON ur.role_id = r.role_id
            WHERE ur.user_id = %s AND r.del_flag = '0' AND r.status = '0'
            """,
            (user_id,),
        )

    def is_admin(self, user_id) -> bool:
        for role in self.roles_of(user_id):
            if role["role_key"] == "admin":
                return True
        return False

    def perms_of(self, user_id) -> set:
        if self.is_admin(user_id):
            return {"*:*:*"}
        rows = self.store.query_all(
            """
            SELECT DISTINCT m.perms AS perms
            FROM sys_menu m
            JOIN sys_role_menu rm ON rm.menu_id = m.menu_id
            JOIN sys_user_role ur ON ur.role_id = rm.role_id
            JOIN sys_role r ON r.role_id = ur.role_id
            WHERE ur.user_id = %s
              AND r.del_flag = '0' AND r.status = '0'
              AND m.status = '0'
              AND m.perms IS NOT NULL AND m.perms <> ''
            """,
            (user_id,),
        )
        return {row["perms"] for row in rows}

    def allows(self, user_id, perm) -> bool:
        if self.is_admin(user_id):
            return True
        return perm in self.perms_of(user_id)

    def require(self, actor, perm):
        if actor is None:
            self._fail("Sign in first.", "py-rbac login --user-name NAME --password SECRET")
        if not self.allows(actor["user_id"], perm):
            self._fail(
                "Missing permission {0}.".format(perm),
                "ask an administrator to grant {0}".format(perm),
            )
        return actor

    def user_by_id(self, user_id):
        return self.store.query_one(
            """
            SELECT u.user_id, u.user_name, u.nick_name, u.dept_id, u.email,
                   u.phonenumber, u.sex, u.status, u.del_flag, d.dept_name
            FROM sys_user u
            LEFT JOIN sys_dept d ON d.dept_id = u.dept_id AND d.del_flag = '0'
            WHERE u.user_id = %s AND u.del_flag = '0'
            """,
            (user_id,),
        )

    def actor_from_token(self, token):
        row = self.audit.session_row(token)
        if row is None:
            return None
        user = self.user_by_id(row["user_id"])
        if user is None or str(user["status"]) != "0":
            return None
        user["token"] = row["token"]
        user["csrf"] = row["csrf"]
        self.audit.touch(token)
        return user

    def login(self, user_name, password, ipaddr="", surface="cli", user_agent=""):
        """General Purpose: Check the password and open a session. Returns the token."""
        name = (user_name or "").strip()
        row = self.store.query_one(
            """
            SELECT user_id, user_name, nick_name, password, status, del_flag, dept_id
            FROM sys_user
            WHERE user_name = %s AND del_flag = '0'
            """,
            (name,),
        )
        if row is None:
            self.passwords.verify(password or "", self._dummy)
            self.audit.write_login(name, ipaddr, "1", "unknown account")
            self._fail(
                "Unknown account or wrong password.",
                "py-rbac login --user-name NAME --password SECRET",
            )
        if str(row["status"]) != "0":
            self.passwords.verify(password or "", self._dummy)
            self.audit.write_login(name, ipaddr, "1", "disabled")
            self._fail("This account is disabled.", "ask an administrator to enable it")
        if not self.passwords.verify(password or "", row["password"] or ""):
            self.audit.write_login(name, ipaddr, "1", "wrong password")
            self._fail(
                "Unknown account or wrong password.",
                "py-rbac login --user-name NAME --password SECRET",
            )
        token = secrets.token_urlsafe(32)
        csrf = secrets.token_urlsafe(24)
        user = self.user_by_id(row["user_id"])
        self.audit.open_session(token, user, ipaddr, user_agent, csrf, surface)
        self.store.execute(
            """
            UPDATE sys_user
            SET login_ip = %s, login_date = NOW()
            WHERE user_id = %s
            """,
            (ipaddr or "", row["user_id"]),
        )
        self.audit.write_login(name, ipaddr, "0", "success")
        if self.logger is not None:
            self.logger.log_message(
                "login {0} via {1}".format(name, surface),
                component="Access",
            )
        user["token"] = token
        user["csrf"] = csrf
        return user

    def logout(self, token) -> int:
        count = self.audit.drop_session(token or "")
        return count

    def _scope(self, actor):
        if self.is_admin(actor["user_id"]):
            return "1=1", []
        roles = self.roles_of(actor["user_id"])
        if any(str(role["data_scope"]) == "1" for role in roles):
            return "1=1", []
        parts = []
        args = []
        dept_id = actor.get("dept_id")
        for role in roles:
            scope = str(role["data_scope"])
            if scope == "2":
                chosen = self.store.query_all(
                    "SELECT dept_id FROM sys_role_dept WHERE role_id = %s",
                    (role["role_id"],),
                )
                ids = [item["dept_id"] for item in chosen]
                if not ids:
                    continue
                marks = ", ".join(["%s"] * len(ids))
                parts.append("u.dept_id IN ({0})".format(marks))
                args.extend(ids)
            elif scope == "3":
                if dept_id is None:
                    continue
                parts.append("u.dept_id = %s")
                args.append(dept_id)
            elif scope == "4":
                if dept_id is None:
                    continue
                parts.append("(u.dept_id = %s OR FIND_IN_SET(%s, d.ancestors))")
                args.extend([dept_id, str(dept_id)])
        if not parts:
            return "1=0", []
        return "(" + " OR ".join(parts) + ")", args

    def user_list(self, actor):
        self.require(actor, "system:user:list")
        clause, args = self._scope(actor)
        sql = """
            SELECT u.user_id, u.user_name, u.nick_name, u.dept_id,
                   d.dept_name, u.status
            FROM sys_user u
            LEFT JOIN sys_dept d ON d.dept_id = u.dept_id
            WHERE u.del_flag = '0' AND {clause}
            ORDER BY u.user_id
            LIMIT 200
        """.format(clause=clause)
        return self.store.query_all(sql, tuple(args))

    def _check_name(self, user_name):
        if not self.USER_NAME.match(user_name or ""):
            self._fail(
                "user_name must start with a letter and use 3 to 30 letters, digits, or underscores.",
                "pick another user_name",
            )

    def _dept_exists(self, dept_id):
        row = self.store.query_one(
            "SELECT dept_id FROM sys_dept WHERE dept_id = %s AND del_flag = '0'",
            (dept_id,),
        )
        if row is None:
            self._fail("Unknown department {0}.".format(dept_id), "py-rbac dept-list")

    def _role_exists(self, role_id):
        row = self.store.query_one(
            "SELECT role_id FROM sys_role WHERE role_id = %s AND del_flag = '0'",
            (role_id,),
        )
        if row is None:
            self._fail("Unknown role {0}.".format(role_id), "py-rbac role-list")

    def init_password(self) -> str:
        row = self.store.query_one(
            "SELECT config_value FROM sys_config WHERE config_key = %s",
            ("sys.user.initPassword",),
        )
        if row and row["config_value"]:
            return row["config_value"]
        return "123456"

    def user_add(self, actor, user_name, nick_name, dept_id, role_id, password=""):
        self.require(actor, "system:user:add")
        self._check_name(user_name)
        nick = (nick_name or "").strip()
        if not nick or len(nick) > 30:
            self._fail("nick_name is required and must be 30 characters or fewer.", "set --nick-name")
        self._dept_exists(dept_id)
        self._role_exists(role_id)
        existing = self.store.query_one(
            "SELECT user_id FROM sys_user WHERE user_name = %s AND del_flag = '0'",
            (user_name,),
        )
        if existing:
            self._fail("That user_name is already in use.", "pick another user_name")
        secret = password or self.init_password()
        if len(secret) < 5:
            self._fail("The password must be at least 5 characters.", "set --password")
        stored = self.passwords.hash(secret)
        done = self.store.execute(
            """
            INSERT INTO sys_user
              (dept_id, user_name, nick_name, password, status, del_flag,
               create_by, create_time, pwd_update_date)
            VALUES (%s, %s, %s, %s, '0', '0', %s, NOW(), NOW())
            """,
            (dept_id, user_name, nick, stored, actor["user_name"]),
        )
        user_id = done["lastrowid"]
        self.store.execute(
            "INSERT INTO sys_user_role (user_id, role_id) VALUES (%s, %s)",
            (user_id, role_id),
        )
        self.audit.write_oper(actor, "User", 1, "user_add", param=user_name)
        return self.user_by_id(user_id)

    def user_edit(self, actor, user_id, nick_name=None, dept_id=None, status=None):
        self.require(actor, "system:user:edit")
        user = self.user_by_id(user_id)
        if user is None:
            self._fail("Unknown user {0}.".format(user_id), "py-rbac user-list")
        if int(user_id) == self.PROTECTED_USER and status is not None and str(status) != "0":
            self._fail("The built-in administrator stays enabled.", "leave status 0")
        if dept_id is not None:
            self._dept_exists(dept_id)
        if nick_name is not None:
            nick = nick_name.strip()
            if not nick or len(nick) > 30:
                self._fail("nick_name is required and must be 30 characters or fewer.", "set --nick-name")
            self.store.execute(
                "UPDATE sys_user SET nick_name = %s, update_by = %s, update_time = NOW() WHERE user_id = %s",
                (nick, actor["user_name"], user_id),
            )
        if dept_id is not None:
            self.store.execute(
                "UPDATE sys_user SET dept_id = %s, update_by = %s, update_time = NOW() WHERE user_id = %s",
                (dept_id, actor["user_name"], user_id),
            )
        if status is not None:
            if str(status) not in ("0", "1"):
                self._fail("status must be 0 or 1.", "use 0 for normal or 1 for disabled")
            self.store.execute(
                "UPDATE sys_user SET status = %s, update_by = %s, update_time = NOW() WHERE user_id = %s",
                (str(status), actor["user_name"], user_id),
            )
        self.audit.write_oper(actor, "User", 2, "user_edit", param=str(user_id))
        return self.user_by_id(user_id)

    def user_remove(self, actor, user_id):
        self.require(actor, "system:user:remove")
        if int(user_id) == self.PROTECTED_USER:
            self._fail("The built-in administrator cannot be removed.", "disable another account instead")
        if int(user_id) == int(actor["user_id"]):
            self._fail("You cannot remove the account you are using.", "sign in as another administrator")
        user = self.user_by_id(user_id)
        if user is None:
            self._fail("Unknown user {0}.".format(user_id), "py-rbac user-list")
        self.store.execute(
            """
            UPDATE sys_user
            SET del_flag = '2', update_by = %s, update_time = NOW()
            WHERE user_id = %s
            """,
            (actor["user_name"], user_id),
        )
        self.store.execute("DELETE FROM sys_user_role WHERE user_id = %s", (user_id,))
        self.store.execute("DELETE FROM sys_user_post WHERE user_id = %s", (user_id,))
        self.audit.write_oper(actor, "User", 3, "user_remove", param=user["user_name"])
        return user["user_name"]

    def user_reset_password(self, actor, user_id, password):
        self.require(actor, "system:user:resetPwd")
        user = self.user_by_id(user_id)
        if user is None:
            self._fail("Unknown user {0}.".format(user_id), "py-rbac user-list")
        if not password or len(password) < 5:
            self._fail("The password must be at least 5 characters.", "set --password")
        stored = self.passwords.hash(password)
        self.store.execute(
            """
            UPDATE sys_user
            SET password = %s, pwd_update_date = NOW(), update_by = %s, update_time = NOW()
            WHERE user_id = %s
            """,
            (stored, actor["user_name"], user_id),
        )
        self.audit.write_oper(actor, "User", 2, "user_reset_password", param=user["user_name"])
        return user["user_name"]

    def role_list(self, actor):
        self.require(actor, "system:role:list")
        return self.store.query_all(
            """
            SELECT role_id, role_name, role_key, data_scope, status
            FROM sys_role
            WHERE del_flag = '0'
            ORDER BY role_sort, role_id
            """
        )

    def role_grant(self, actor, role_id, menu_ids, data_scope=None, dept_ids=None):
        self.require(actor, "system:role:edit")
        self._role_exists(role_id)
        if int(role_id) == self.PROTECTED_ROLE:
            self._fail(
                "The built-in administrator role is not edited here.",
                "grant menus on another role",
            )
        if data_scope is not None and str(data_scope) not in self.SCOPES:
            self._fail(
                "data_scope must be 1, 2, 3, or 4.",
                "1 all, 2 custom departments, 3 this department, 4 this department and children",
            )
        clean_menus = []
        for item in menu_ids:
            row = self.store.query_one(
                "SELECT menu_id FROM sys_menu WHERE menu_id = %s",
                (int(item),),
            )
            if row is None:
                self._fail("Unknown menu {0}.".format(item), "py-rbac menu-list")
            clean_menus.append(int(item))
        self.store.execute("DELETE FROM sys_role_menu WHERE role_id = %s", (role_id,))
        for menu_id in clean_menus:
            self.store.execute(
                "INSERT INTO sys_role_menu (role_id, menu_id) VALUES (%s, %s)",
                (role_id, menu_id),
            )
        if data_scope is not None:
            self.store.execute(
                """
                UPDATE sys_role
                SET data_scope = %s, update_by = %s, update_time = NOW()
                WHERE role_id = %s
                """,
                (str(data_scope), actor["user_name"], role_id),
            )
        scope_now = str(data_scope) if data_scope is not None else None
        if scope_now is None:
            current = self.store.query_one(
                "SELECT data_scope FROM sys_role WHERE role_id = %s",
                (role_id,),
            )
            scope_now = str(current["data_scope"]) if current else "1"
        self.store.execute("DELETE FROM sys_role_dept WHERE role_id = %s", (role_id,))
        if scope_now == "2":
            for dept_id in dept_ids or []:
                self._dept_exists(int(dept_id))
                self.store.execute(
                    "INSERT INTO sys_role_dept (role_id, dept_id) VALUES (%s, %s)",
                    (role_id, int(dept_id)),
                )
        self.audit.write_oper(actor, "Role", 2, "role_grant", param=str(role_id))
        return self.store.query_one(
            "SELECT role_id, role_name, role_key, data_scope, status FROM sys_role WHERE role_id = %s",
            (role_id,),
        )

    def menu_list(self, actor):
        self.require(actor, "system:menu:list")
        return self.store.query_all(
            """
            SELECT menu_id, parent_id, menu_name, menu_type, perms
            FROM sys_menu
            WHERE status = '0'
            ORDER BY parent_id, order_num, menu_id
            """
        )

    def menu_add(self, actor, menu_name, parent_id, menu_type, perms="", path=""):
        self.require(actor, "system:menu:add")
        name = (menu_name or "").strip()
        if not name or len(name) > 50:
            self._fail("menu_name is required.", "set --menu-name")
        if menu_type not in ("M", "C", "F"):
            self._fail("menu_type must be M, C, or F.", "M directory, C page, F button")
        if int(parent_id) != 0:
            parent = self.store.query_one(
                "SELECT menu_id FROM sys_menu WHERE menu_id = %s",
                (int(parent_id),),
            )
            if parent is None:
                self._fail("Unknown parent menu {0}.".format(parent_id), "py-rbac menu-list")
        done = self.store.execute(
            """
            INSERT INTO sys_menu
              (menu_name, parent_id, order_num, path, menu_type, visible, status,
               perms, create_by, create_time)
            VALUES (%s, %s, 0, %s, %s, '0', '0', %s, %s, NOW())
            """,
            (name, int(parent_id), path or "", menu_type, perms or "", actor["user_name"]),
        )
        self.audit.write_oper(actor, "Menu", 1, "menu_add", param=name)
        return done["lastrowid"]

    def dept_list(self, actor):
        self.require(actor, "system:dept:list")
        return self.store.query_all(
            """
            SELECT dept_id, parent_id, dept_name, ancestors, status
            FROM sys_dept
            WHERE del_flag = '0'
            ORDER BY parent_id, order_num, dept_id
            """
        )

    def dept_add(self, actor, dept_name, parent_id):
        self.require(actor, "system:dept:add")
        name = (dept_name or "").strip()
        if not name or len(name) > 30:
            self._fail("dept_name is required.", "set --dept-name")
        if int(parent_id) == 0:
            ancestors = "0"
        else:
            parent = self.store.query_one(
                """
                SELECT dept_id, ancestors FROM sys_dept
                WHERE dept_id = %s AND del_flag = '0'
                """,
                (int(parent_id),),
            )
            if parent is None:
                self._fail("Unknown parent department {0}.".format(parent_id), "py-rbac dept-list")
            ancestors = "{0},{1}".format(parent["ancestors"], parent["dept_id"])
        done = self.store.execute(
            """
            INSERT INTO sys_dept
              (parent_id, ancestors, dept_name, order_num, status, del_flag,
               create_by, create_time)
            VALUES (%s, %s, %s, 0, '0', '0', %s, NOW())
            """,
            (int(parent_id), ancestors, name, actor["user_name"]),
        )
        self.audit.write_oper(actor, "Department", 1, "dept_add", param=name)
        return done["lastrowid"]

    def post_list(self, actor):
        self.require(actor, "system:post:list")
        return self.store.query_all(
            """
            SELECT post_id, post_code, post_name, post_sort, status
            FROM sys_post
            ORDER BY post_sort, post_id
            """
        )

    def post_add(self, actor, post_code, post_name):
        self.require(actor, "system:post:add")
        code = (post_code or "").strip()
        name = (post_name or "").strip()
        if not code or not name:
            self._fail("post_code and post_name are required.", "set both")
        existing = self.store.query_one(
            "SELECT post_id FROM sys_post WHERE post_code = %s",
            (code,),
        )
        if existing:
            self._fail("That post_code is already in use.", "pick another post_code")
        done = self.store.execute(
            """
            INSERT INTO sys_post
              (post_code, post_name, post_sort, status, create_by, create_time)
            VALUES (%s, %s, 0, '0', %s, NOW())
            """,
            (code, name, actor["user_name"]),
        )
        self.audit.write_oper(actor, "Post", 1, "post_add", param=code)
        return done["lastrowid"]

    def describe(self, actor) -> str:
        """General Purpose: Who is signed in, without a password or a full token."""
        roles = self.roles_of(actor["user_id"])
        names = ", ".join(role["role_key"] for role in roles) or "(none)"
        return (
            "user_name={0}\n"
            "nick_name={1}\n"
            "dept_id={2}\n"
            "roles={3}\n"
            "admin={4}"
        ).format(
            actor["user_name"],
            actor["nick_name"],
            actor.get("dept_id"),
            names,
            "yes" if self.is_admin(actor["user_id"]) else "no",
        )
