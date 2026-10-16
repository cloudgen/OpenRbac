# =============================================================================
# RBAC commands shared by the terminal, the text menu, and the web interface.
# requirement-rbac — permission check, data scope, protected rows.
# requirement-rbac-users, requirement-rbac-roles, requirement-rbac-menu,
# requirement-rbac-departments, requirement-rbac-job-titles.
# requirement-python-oop — class Access and AccessError.
# =============================================================================
from __future__ import annotations

import csv
import io
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
    """Users, roles, menus, departments, and job titles.

    Data scope is 1 all, 2 custom departments, 3 this department, and 4 this
    department and children. Any other scope contributes no rows. role_key
    admin bypasses permission and scope.
    """

    USER_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]{2,29}$")
    ROLE_KEY = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,99}$")
    DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
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
            self._fail("Sign in first.", "open-rbac login --user-name NAME --password SECRET")
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
                   u.phonenumber, u.sex, u.remark, u.status, u.del_flag, d.dept_name
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
                "open-rbac login --user-name NAME --password SECRET",
            )
        if str(row["status"]) != "0":
            self.passwords.verify(password or "", self._dummy)
            self.audit.write_login(name, ipaddr, "1", "disabled")
            self._fail("This account is disabled.", "ask an administrator to enable it")
        if not self.passwords.verify(password or "", row["password"] or ""):
            self.audit.write_login(name, ipaddr, "1", "wrong password")
            self._fail(
                "Unknown account or wrong password.",
                "open-rbac login --user-name NAME --password SECRET",
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

    def user_list(self, actor, filters=None):
        """General Purpose: Accounts in scope. Optional filters narrow that list.

        requirement-rbac-users — an omitted filter keeps the unfiltered rows.
        """
        self.require(actor, "system:user:list")
        clause, args = self._scope(actor)
        extra, extra_args = self._user_filters(filters or {})
        sql = """
            SELECT u.user_id, u.user_name, u.nick_name, u.dept_id,
                   d.dept_name, u.phonenumber, u.status, u.create_time
            FROM sys_user u
            LEFT JOIN sys_dept d ON d.dept_id = u.dept_id
            WHERE u.del_flag = '0' AND {clause}{extra}
            ORDER BY u.user_id
            LIMIT 200
        """.format(clause=clause, extra=extra)
        return self.store.query_all(sql, tuple(args) + tuple(extra_args))

    def _user_filters(self, filters):
        """General Purpose: The optional AND clause for one user list."""
        parts = []
        args = []
        name = self._like_piece(filters.get("user_name") or "")
        if name:
            parts.append(" AND u.user_name LIKE %s")
            args.append("%{0}%".format(name))
        phone = self._like_piece(filters.get("phonenumber") or "")
        if phone:
            parts.append(" AND u.phonenumber LIKE %s")
            args.append("%{0}%".format(phone))
        status = filters.get("status")
        if status not in (None, ""):
            if str(status) not in ("0", "1"):
                self._fail("status must be 0 or 1.", "use 0 for normal or 1 for disabled")
            parts.append(" AND u.status = %s")
            args.append(str(status))
        dept_id = filters.get("dept_id")
        if dept_id not in (None, "", 0, "0"):
            parts.append(" AND (u.dept_id = %s OR FIND_IN_SET(%s, d.ancestors))")
            args.extend([dept_id, str(dept_id)])
        begin = filters.get("begin_time") or ""
        if begin:
            if not self.DATE.match(str(begin)):
                self._fail("The start date must be YYYY-MM-DD.", "pick a date")
            parts.append(" AND u.create_time >= %s")
            args.append("{0} 00:00:00".format(begin))
        end = filters.get("end_time") or ""
        if end:
            if not self.DATE.match(str(end)):
                self._fail("The end date must be YYYY-MM-DD.", "pick a date")
            parts.append(" AND u.create_time <= %s")
            args.append("{0} 23:59:59".format(end))
        return "".join(parts), args

    def _like_piece(self, text):
        """General Purpose: User text with the LIKE wildcards removed."""
        return str(text).replace("\\", "").replace("%", "").replace("_", "").strip()

    def user_departments(self, actor):
        """General Purpose: Departments for the users tree, including ancestors.

        requirement-rbac-users — system:user:list. A sibling outside scope stays out.
        """
        self.require(actor, "system:user:list")
        if self.is_admin(actor["user_id"]):
            return self._departments_by_ids(None)
        if any(str(role["data_scope"]) == "1" for role in self.roles_of(actor["user_id"])):
            return self._departments_by_ids(None)
        wanted = set()
        for row in self.user_list(actor):
            dept_id = row.get("dept_id")
            if dept_id is None:
                continue
            wanted.add(int(dept_id))
        if not wanted:
            return []
        for row in self._departments_by_ids(wanted):
            for piece in str(row.get("ancestors") or "").split(","):
                piece = piece.strip()
                if piece.isdigit() and int(piece) != 0:
                    wanted.add(int(piece))
        return self._departments_by_ids(wanted)

    def _departments_by_ids(self, ids):
        """General Purpose: Live departments, or every live department when ids is None."""
        if ids is None:
            return self.store.query_all(
                """
                SELECT dept_id, parent_id, dept_name, ancestors
                FROM sys_dept
                WHERE del_flag = '0'
                ORDER BY parent_id, order_num, dept_id
                """
            )
        ordered = sorted(ids)
        if not ordered:
            return []
        marks = ", ".join(["%s"] * len(ordered))
        return self.store.query_all(
            """
            SELECT dept_id, parent_id, dept_name, ancestors
            FROM sys_dept
            WHERE del_flag = '0' AND dept_id IN ({0})
            ORDER BY parent_id, order_num, dept_id
            """.format(marks),
            tuple(ordered),
        )

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
            self._fail("Unknown department {0}.".format(dept_id), "open-rbac dept-list")

    def _role_exists(self, role_id):
        row = self.store.query_one(
            "SELECT role_id FROM sys_role WHERE role_id = %s AND del_flag = '0'",
            (role_id,),
        )
        if row is None:
            self._fail("Unknown role {0}.".format(role_id), "open-rbac role-list")

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

    def user_edit(
        self,
        actor,
        user_id,
        nick_name=None,
        dept_id=None,
        status=None,
        phonenumber=None,
        email=None,
        sex=None,
        remark=None,
        job_title_ids=None,
        role_ids=None,
    ):
        """General Purpose: Change one listed account. An omitted field stays.

        requirement-rbac-users — the web form posts the fields it shows.
        A list replaces that account's job titles or roles. None leaves the links.
        """
        self.require(actor, "system:user:edit")
        user = self.user_by_id(user_id)
        if user is None:
            self._fail("Unknown user {0}.".format(user_id), "open-rbac user-list")
        nick = None
        if nick_name is not None:
            nick = nick_name.strip()
            if not nick or len(nick) > 30:
                self._fail(
                    "nick_name is required and must be 30 characters or fewer.",
                    "set --nick-name",
                )
        if dept_id is not None:
            self._dept_exists(dept_id)
        phone = None
        if phonenumber is not None:
            phone = phonenumber.strip()
            if len(phone) > 11:
                self._fail(
                    "The phone number must be 11 characters or fewer.",
                    "shorten the phone number",
                )
        mail = None
        if email is not None:
            mail = email.strip()
            if len(mail) > 50:
                self._fail(
                    "The email must be 50 characters or fewer.",
                    "shorten the email",
                )
            if mail and "@" not in mail:
                self._fail("The email must contain @.", "use an email address")
        posted_sex = None
        if sex is not None:
            posted_sex = str(sex).strip()
            if posted_sex not in ("0", "1", "2"):
                self._fail("Sex must be 0, 1, or 2.", "use 0, 1, or 2")
        note = None
        if remark is not None:
            note = remark.strip()
            if len(note) > 500:
                self._fail(
                    "The remark must be 500 characters or fewer.",
                    "shorten the remark",
                )
        posted_status = None
        if status is not None:
            posted_status = str(status).strip()
            if posted_status not in ("0", "1"):
                self._fail("status must be 0 or 1.", "use 0 for normal or 1 for disabled")
            if int(user_id) == self.PROTECTED_USER and posted_status != "0":
                self._fail("The built-in administrator stays enabled.", "leave status 0")
        titles = self._clean_job_titles(job_title_ids)
        roles = self._clean_roles(user_id, role_ids)
        sets = []
        args = []
        if nick is not None:
            sets.append("nick_name = %s")
            args.append(nick)
        if dept_id is not None:
            sets.append("dept_id = %s")
            args.append(dept_id)
        if phone is not None:
            sets.append("phonenumber = %s")
            args.append(phone)
        if mail is not None:
            sets.append("email = %s")
            args.append(mail)
        if posted_sex is not None:
            sets.append("sex = %s")
            args.append(posted_sex)
        if note is not None:
            sets.append("remark = %s")
            args.append(note)
        if posted_status is not None:
            sets.append("status = %s")
            args.append(posted_status)
        if sets or titles is not None or roles is not None:
            sets.append("update_by = %s")
            sets.append("update_time = NOW()")
            args.append(actor["user_name"])
            args.append(user_id)
            self.store.execute(
                "UPDATE sys_user SET {0} WHERE user_id = %s".format(", ".join(sets)),
                tuple(args),
            )
        if titles is not None:
            self.store.execute(
                "DELETE FROM sys_user_job_title WHERE user_id = %s",
                (user_id,),
            )
            for job_id in titles:
                self.store.execute(
                    "INSERT INTO sys_user_job_title (user_id, job_title_id) VALUES (%s, %s)",
                    (user_id, job_id),
                )
        if roles is not None:
            self.store.execute(
                "DELETE FROM sys_user_role WHERE user_id = %s",
                (user_id,),
            )
            for role_id in roles:
                self.store.execute(
                    "INSERT INTO sys_user_role (user_id, role_id) VALUES (%s, %s)",
                    (user_id, role_id),
                )
        self.audit.write_oper(actor, "User", 2, "user_edit", param=str(user_id))
        return self.user_by_id(user_id)

    def edit_job_titles(self, actor):
        """Job titles for the edit form. Requires system:user:edit, not the job-title list."""
        self.require(actor, "system:user:edit")
        return self.store.query_all(
            """
            SELECT job_title_id, job_title
            FROM sys_job_title
            WHERE status = '0'
            ORDER BY job_title_sort, job_title_id
            """
        )

    def edit_roles(self, actor):
        """Live roles for the edit form. Requires system:user:edit, not the role list."""
        self.require(actor, "system:user:edit")
        return self.store.query_all(
            """
            SELECT role_id, role_name
            FROM sys_role
            WHERE del_flag = '0' AND status = '0'
            ORDER BY role_sort, role_id
            """
        )

    def user_job_title_ids(self, user_id):
        rows = self.store.query_all(
            """
            SELECT job_title_id FROM sys_user_job_title
            WHERE user_id = %s ORDER BY job_title_id
            """,
            (user_id,),
        )
        return [int(row["job_title_id"]) for row in rows]

    def user_role_ids(self, user_id):
        rows = self.store.query_all(
            """
            SELECT role_id FROM sys_user_role
            WHERE user_id = %s ORDER BY role_id
            """,
            (user_id,),
        )
        return [int(row["role_id"]) for row in rows]

    def _clean_job_titles(self, job_title_ids):
        if job_title_ids is None:
            return None
        found = []
        seen = set()
        for raw in job_title_ids:
            number = int(raw)
            if number in seen:
                continue
            seen.add(number)
            row = self.store.query_one(
                """
                SELECT job_title_id FROM sys_job_title
                WHERE job_title_id = %s AND status = '0'
                """,
                (number,),
            )
            if row is None:
                self._fail(
                    "Unknown job title {0}.".format(number),
                    "pick a job title",
                )
            found.append(number)
        return found

    def _clean_roles(self, user_id, role_ids):
        if role_ids is None:
            return None
        found = []
        seen = set()
        for raw in role_ids:
            number = int(raw)
            if number in seen:
                continue
            seen.add(number)
            row = self.store.query_one(
                """
                SELECT role_id FROM sys_role
                WHERE role_id = %s AND del_flag = '0' AND status = '0'
                """,
                (number,),
            )
            if row is None:
                self._fail("Unknown role {0}.".format(number), "pick a role")
            found.append(number)
        if int(user_id) == self.PROTECTED_USER and self.PROTECTED_ROLE not in seen:
            found.insert(0, self.PROTECTED_ROLE)
        if not found:
            self._fail("Choose a role.", "pick a role")
        return found

    def user_remove(self, actor, user_id):
        self.require(actor, "system:user:remove")
        if int(user_id) == self.PROTECTED_USER:
            self._fail("The built-in administrator cannot be removed.", "disable another account instead")
        if int(user_id) == int(actor["user_id"]):
            self._fail("You cannot remove the account you are using.", "sign in as another administrator")
        user = self.user_by_id(user_id)
        if user is None:
            self._fail("Unknown user {0}.".format(user_id), "open-rbac user-list")
        self.store.execute(
            """
            UPDATE sys_user
            SET del_flag = '2', update_by = %s, update_time = NOW()
            WHERE user_id = %s
            """,
            (actor["user_name"], user_id),
        )
        self.store.execute("DELETE FROM sys_user_role WHERE user_id = %s", (user_id,))
        self.store.execute("DELETE FROM sys_user_job_title WHERE user_id = %s", (user_id,))
        self.audit.write_oper(actor, "User", 3, "user_remove", param=user["user_name"])
        return user["user_name"]

    def user_reset_password(self, actor, user_id, password):
        self.require(actor, "system:user:resetPwd")
        user = self.user_by_id(user_id)
        if user is None:
            self._fail("Unknown user {0}.".format(user_id), "open-rbac user-list")
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

    def user_import(self, actor, text, update_support=False):
        """General Purpose: Create or update accounts from a csv table.

        requirement-rbac-users — system:user:import. The file is account rows, not a file manager.
        A row that fails a check writes nothing from this file.
        """
        self.require(actor, "system:user:import")
        rows = self._import_rows(text)
        planned = []
        seen = set()
        for item in rows:
            checked = self._import_checked(item)
            name = checked["user_name"]
            existing = self.store.query_one(
                "SELECT user_id FROM sys_user WHERE user_name = %s AND del_flag = '0'",
                (name,),
            )
            exists = existing is not None or name in seen
            if exists and not update_support:
                self._fail(
                    "That user_name is already in use.",
                    "pick another user_name or update existing accounts",
                )
            if existing is not None and int(existing["user_id"]) == self.PROTECTED_USER:
                if checked["status"] not in ("", "0"):
                    self._fail(
                        "The built-in administrator stays enabled.",
                        "leave status 0",
                    )
            if existing is None and not checked["password"]:
                if len(self.init_password()) < 5:
                    self._fail(
                        "The password must be at least 5 characters.",
                        "set password",
                    )
            seen.add(name)
            planned.append(checked)
        added = 0
        updated = 0
        for checked in planned:
            existing = self.store.query_one(
                "SELECT user_id FROM sys_user WHERE user_name = %s AND del_flag = '0'",
                (checked["user_name"],),
            )
            if existing:
                self._import_update(actor, int(existing["user_id"]), checked)
                updated += 1
            else:
                self._import_insert(actor, checked)
                added += 1
        self.audit.write_oper(
            actor,
            "User",
            1,
            "user_import",
            param="{0} added, {1} updated".format(added, updated),
        )
        return {"added": added, "updated": updated}

    def user_export(self, actor, filters=None):
        """General Purpose: A csv table of the accounts this actor can list.

        requirement-rbac-users — system:user:export. The password stays out of the file.
        """
        self.require(actor, "system:user:export")
        rows = self.user_list(actor, filters)
        roles = {}
        ids = [row["user_id"] for row in rows]
        if ids:
            marks = ", ".join(["%s"] * len(ids))
            found = self.store.query_all(
                """
                SELECT user_id, MIN(role_id) AS role_id
                FROM sys_user_role
                WHERE user_id IN ({0})
                GROUP BY user_id
                """.format(marks),
                tuple(ids),
            )
            for item in found:
                roles[int(item["user_id"])] = item["role_id"]
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerow(["user_name", "nick_name", "dept_id", "role_id", "phonenumber", "status"])
        for row in rows:
            writer.writerow([
                row.get("user_name") or "",
                row.get("nick_name") or "",
                "" if row.get("dept_id") is None else row.get("dept_id"),
                roles.get(int(row["user_id"]), ""),
                row.get("phonenumber") or "",
                row.get("status") or "0",
            ])
        return buffer.getvalue()

    def _import_rows(self, text):
        """General Purpose: Account rows from one csv table."""
        raw = "" if text is None else str(text).lstrip("\ufeff")
        if not raw.strip():
            self._fail("The import file has no accounts.", "choose a csv file")
        try:
            reader = csv.DictReader(io.StringIO(raw))
            fieldnames = list(reader.fieldnames or [])
            parsed = list(reader)
        except csv.Error:
            self._fail("The import file is not a csv table.", "use the export columns")
        fields = [str(name or "").strip() for name in fieldnames]
        for name in ("user_name", "nick_name", "dept_id", "role_id"):
            if name not in fields:
                self._fail(
                    "The import file needs the columns user_name, nick_name, dept_id, and role_id.",
                    "download the current list and use those columns",
                )
        rows = []
        for raw_row in parsed:
            if raw_row is None:
                continue
            item = {}
            blank = True
            for name in fields:
                value = str(raw_row.get(name) or "").strip()
                item[name] = value
                if value:
                    blank = False
            if blank:
                continue
            rows.append(item)
            if len(rows) > 200:
                self._fail("An import accepts at most 200 accounts.", "split the file")
        if not rows:
            self._fail("The import file has no accounts.", "choose a csv file")
        return rows

    def _import_checked(self, item):
        """General Purpose: One import row with the same checks as a new account."""
        user_name = item["user_name"]
        self._check_name(user_name)
        nick = item["nick_name"]
        if not nick or len(nick) > 30:
            self._fail("nick_name is required and must be 30 characters or fewer.", "set nick_name")
        dept_id = self._import_int(item["dept_id"], "dept_id")
        role_id = self._import_int(item["role_id"], "role_id")
        self._dept_exists(dept_id)
        self._role_exists(role_id)
        secret = item.get("password") or ""
        if secret and len(secret) < 5:
            self._fail("The password must be at least 5 characters.", "set password")
        status = item.get("status") or ""
        if status not in ("", "0", "1"):
            self._fail("status must be 0 or 1.", "use 0 for normal or 1 for disabled")
        phone = None
        if "phonenumber" in item:
            phone = item.get("phonenumber") or ""
            if len(phone) > 11:
                self._fail("phonenumber must be 11 characters or fewer.", "shorten the phone")
        return {
            "user_name": user_name,
            "nick_name": nick,
            "dept_id": dept_id,
            "role_id": role_id,
            "password": secret,
            "status": status,
            "phone": phone,
        }

    def _import_insert(self, actor, item):
        """General Purpose: One new account from a checked import row."""
        secret = item["password"] or self.init_password()
        if len(secret) < 5:
            self._fail("The password must be at least 5 characters.", "set password")
        status = item["status"] or "0"
        phone = "" if item["phone"] is None else item["phone"]
        stored = self.passwords.hash(secret)
        done = self.store.execute(
            """
            INSERT INTO sys_user
              (dept_id, user_name, nick_name, password, phonenumber, status, del_flag,
               create_by, create_time, pwd_update_date)
            VALUES (%s, %s, %s, %s, %s, %s, '0', %s, NOW(), NOW())
            """,
            (
                item["dept_id"],
                item["user_name"],
                item["nick_name"],
                stored,
                phone,
                status,
                actor["user_name"],
            ),
        )
        self.store.execute(
            "INSERT INTO sys_user_role (user_id, role_id) VALUES (%s, %s)",
            (done["lastrowid"], item["role_id"]),
        )

    def _import_update(self, actor, user_id, item):
        """General Purpose: Update one listed account from a checked import row."""
        self.store.execute(
            """
            UPDATE sys_user
            SET nick_name = %s, dept_id = %s, update_by = %s, update_time = NOW()
            WHERE user_id = %s
            """,
            (item["nick_name"], item["dept_id"], actor["user_name"], user_id),
        )
        if item["status"] != "":
            self.store.execute(
                "UPDATE sys_user SET status = %s, update_by = %s, update_time = NOW() WHERE user_id = %s",
                (item["status"], actor["user_name"], user_id),
            )
        if item["phone"] is not None:
            self.store.execute(
                """
                UPDATE sys_user
                SET phonenumber = %s, update_by = %s, update_time = NOW()
                WHERE user_id = %s
                """,
                (item["phone"], actor["user_name"], user_id),
            )
        if item["password"]:
            self.store.execute(
                """
                UPDATE sys_user
                SET password = %s, pwd_update_date = NOW(), update_by = %s, update_time = NOW()
                WHERE user_id = %s
                """,
                (self.passwords.hash(item["password"]), actor["user_name"], user_id),
            )
        self.store.execute("DELETE FROM sys_user_role WHERE user_id = %s", (user_id,))
        self.store.execute(
            "INSERT INTO sys_user_role (user_id, role_id) VALUES (%s, %s)",
            (user_id, item["role_id"]),
        )

    def _import_int(self, text, label):
        """General Purpose: A whole number from one import cell."""
        if not str(text).isdigit():
            self._fail("{0} must be a number.".format(label), "use an id from the list")
        return int(text)

    def role_list(self, actor, filters=None):
        """General Purpose: Every live role. Optional filters narrow that list.

        requirement-rbac-roles — an omitted filter keeps the unfiltered rows.
        """
        self.require(actor, "system:role:list")
        extra, extra_args = self._role_filters(filters or {})
        sql = """
            SELECT role_id, role_name, role_key, data_scope, role_sort, status,
                   create_time, remark
            FROM sys_role
            WHERE del_flag = '0'{extra}
            ORDER BY role_sort, role_id
        """.format(extra=extra)
        return self.store.query_all(sql, tuple(extra_args))

    def _role_filters(self, filters):
        """General Purpose: The optional AND clause for one role list."""
        parts = []
        args = []
        name = self._like_piece(filters.get("role_name") or "")
        if name:
            parts.append(" AND role_name LIKE %s")
            args.append("%{0}%".format(name))
        key = self._like_piece(filters.get("role_key") or "")
        if key:
            parts.append(" AND role_key LIKE %s")
            args.append("%{0}%".format(key))
        status = filters.get("status")
        if status not in (None, ""):
            if str(status) not in ("0", "1"):
                self._fail("status must be 0 or 1.", "use 0 for normal or 1 for disabled")
            parts.append(" AND status = %s")
            args.append(str(status))
        begin = filters.get("begin_time") or ""
        if begin:
            if not self.DATE.match(str(begin)):
                self._fail("The start date must be YYYY-MM-DD.", "pick a date")
            parts.append(" AND create_time >= %s")
            args.append("{0} 00:00:00".format(begin))
        end = filters.get("end_time") or ""
        if end:
            if not self.DATE.match(str(end)):
                self._fail("The end date must be YYYY-MM-DD.", "pick a date")
            parts.append(" AND create_time <= %s")
            args.append("{0} 23:59:59".format(end))
        return "".join(parts), args

    def _check_menu_ids(self, menu_ids):
        """General Purpose: Menu ids that exist. An empty id is skipped."""
        clean = []
        seen = set()
        for item in menu_ids or []:
            if item is None or str(item).strip() == "":
                continue
            menu_id = int(item)
            if menu_id in seen:
                continue
            row = self.store.query_one(
                "SELECT menu_id FROM sys_menu WHERE menu_id = %s",
                (menu_id,),
            )
            if row is None:
                self._fail("Unknown menu {0}.".format(item), "open-rbac menu-list")
            seen.add(menu_id)
            clean.append(menu_id)
        return clean

    def _write_role_menus(self, role_id, menu_ids):
        """General Purpose: Replace sys_role_menu for one role."""
        self.store.execute("DELETE FROM sys_role_menu WHERE role_id = %s", (role_id,))
        for menu_id in menu_ids:
            self.store.execute(
                "INSERT INTO sys_role_menu (role_id, menu_id) VALUES (%s, %s)",
                (role_id, menu_id),
            )

    def _role_name(self, role_name):
        name = (role_name or "").strip()
        if not name or len(name) > 30:
            self._fail(
                "role_name is required and must be 30 characters or fewer.",
                "set a role name",
            )
        return name

    def _role_key(self, role_key):
        key = (role_key or "").strip()
        if not self.ROLE_KEY.match(key):
            self._fail(
                "role_key must start with a letter and use letters, digits, or underscores.",
                "pick another role_key",
            )
        return key

    def _role_key_free(self, key, role_id=None):
        row = self.store.query_one(
            "SELECT role_id FROM sys_role WHERE role_key = %s",
            (key,),
        )
        if row is None:
            return
        if role_id is not None and int(row["role_id"]) == int(role_id):
            return
        self._fail("That role_key is already in use.", "pick another role_key")

    def _role_sort(self, value):
        text = str(value if value is not None else "").strip()
        if not text.isdigit() or int(text) > 2147483647:
            self._fail("role_sort must be a whole number.", "set a display order")
        return int(text)

    def _role_status(self, value, default=None):
        if value is None or str(value).strip() == "":
            if default is None:
                self._fail("status must be 0 or 1.", "use 0 for normal or 1 for disabled")
            return default
        text = str(value).strip()
        if text not in ("0", "1"):
            self._fail("status must be 0 or 1.", "use 0 for normal or 1 for disabled")
        return text

    def _role_remark(self, value):
        text = "" if value is None else str(value).strip()
        if len(text) > 500:
            self._fail("remark must be 500 characters or fewer.", "shorten the remark")
        return text

    def _role_row(self, role_id):
        return self.store.query_one(
            """
            SELECT role_id, role_name, role_key, role_sort, data_scope, status,
                   create_time, remark
            FROM sys_role
            WHERE role_id = %s
            """,
            (role_id,),
        )

    def role_add(self, actor, role_name, role_key, role_sort, status=None, remark="", menu_ids=None):
        """General Purpose: One new role. Scope starts at 1. No user is attached.

        requirement-rbac-roles — system:role:add. Menus are checked before the insert.
        """
        self.require(actor, "system:role:add")
        name = self._role_name(role_name)
        key = self._role_key(role_key)
        sort = self._role_sort(role_sort)
        stored_status = self._role_status(status, default="0")
        note = self._role_remark(remark)
        self._role_key_free(key)
        clean = self._check_menu_ids(menu_ids) if menu_ids is not None else []
        done = self.store.execute(
            """
            INSERT INTO sys_role
              (role_name, role_key, role_sort, data_scope, status, del_flag,
               create_by, create_time, remark)
            VALUES (%s, %s, %s, '1', %s, '0', %s, NOW(), %s)
            """,
            (name, key, sort, stored_status, actor["user_name"], note),
        )
        role_id = done["lastrowid"]
        if clean:
            self._write_role_menus(role_id, clean)
        self.audit.write_oper(actor, "Role", 1, "role_add", param=str(role_id))
        return self._role_row(role_id)

    def role_edit(
        self,
        actor,
        role_id,
        role_name=None,
        role_key=None,
        role_sort=None,
        status=None,
        remark=None,
        menu_ids=None,
    ):
        """General Purpose: Change one listed role. An omitted field stays.

        requirement-rbac-roles — system:role:edit. Menus change only when menu_ids
        is passed. The status switch calls this with only status. Scope and
        department links stay.
        """
        self.require(actor, "system:role:edit")
        self._role_exists(role_id)
        if int(role_id) == self.PROTECTED_ROLE:
            self._fail(
                "The built-in administrator role is not edited here.",
                "edit another role",
            )
        if (
            role_name is None
            and role_key is None
            and role_sort is None
            and status is None
            and remark is None
            and menu_ids is None
        ):
            self._fail(
                "role-edit needs a name, a key, an order, a status, or a remark.",
                "change one field",
            )
        name = None if role_name is None else self._role_name(role_name)
        key = None if role_key is None else self._role_key(role_key)
        sort = None if role_sort is None else self._role_sort(role_sort)
        stored_status = None if status is None else self._role_status(status)
        note = None if remark is None else self._role_remark(remark)
        if key is not None:
            self._role_key_free(key, role_id)
        clean = None if menu_ids is None else self._check_menu_ids(menu_ids)
        if name is not None:
            self.store.execute(
                """
                UPDATE sys_role
                SET role_name = %s, update_by = %s, update_time = NOW()
                WHERE role_id = %s
                """,
                (name, actor["user_name"], role_id),
            )
        if key is not None:
            self.store.execute(
                """
                UPDATE sys_role
                SET role_key = %s, update_by = %s, update_time = NOW()
                WHERE role_id = %s
                """,
                (key, actor["user_name"], role_id),
            )
        if sort is not None:
            self.store.execute(
                """
                UPDATE sys_role
                SET role_sort = %s, update_by = %s, update_time = NOW()
                WHERE role_id = %s
                """,
                (sort, actor["user_name"], role_id),
            )
        if stored_status is not None:
            self.store.execute(
                """
                UPDATE sys_role
                SET status = %s, update_by = %s, update_time = NOW()
                WHERE role_id = %s
                """,
                (stored_status, actor["user_name"], role_id),
            )
        if note is not None:
            self.store.execute(
                """
                UPDATE sys_role
                SET remark = %s, update_by = %s, update_time = NOW()
                WHERE role_id = %s
                """,
                (note, actor["user_name"], role_id),
            )
        if clean is not None:
            self._write_role_menus(role_id, clean)
        self.audit.write_oper(actor, "Role", 2, "role_edit", param=str(role_id))
        return self._role_row(role_id)

    def role_remove(self, actor, role_id):
        """General Purpose: Hide one role and drop its links.

        requirement-rbac-roles — system:role:remove. del_flag becomes 2.
        """
        self.require(actor, "system:role:remove")
        if int(role_id) == self.PROTECTED_ROLE:
            self._fail(
                "The built-in administrator role is not edited here.",
                "remove another role",
            )
        self._role_exists(role_id)
        current = self._role_row(role_id)
        self.store.execute(
            """
            UPDATE sys_role
            SET del_flag = '2', update_by = %s, update_time = NOW()
            WHERE role_id = %s
            """,
            (actor["user_name"], role_id),
        )
        self.store.execute("DELETE FROM sys_role_menu WHERE role_id = %s", (role_id,))
        self.store.execute("DELETE FROM sys_role_dept WHERE role_id = %s", (role_id,))
        self.store.execute("DELETE FROM sys_user_role WHERE role_id = %s", (role_id,))
        self.audit.write_oper(actor, "Role", 3, "role_remove", param=str(role_id))
        return "" if current is None else current["role_key"]

    def role_export(self, actor, filters=None):
        """General Purpose: A csv table of the roles this actor can list.

        requirement-rbac-roles — system:role:export. The same filters as role_list.
        """
        self.require(actor, "system:role:export")
        rows = self.role_list(actor, filters)
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerow([
            "role_id",
            "role_name",
            "role_key",
            "data_scope",
            "role_sort",
            "status",
            "create_time",
        ])
        for row in rows:
            created = row.get("create_time")
            writer.writerow([
                "" if row.get("role_id") is None else row.get("role_id"),
                row.get("role_name") or "",
                row.get("role_key") or "",
                row.get("data_scope") or "",
                "" if row.get("role_sort") is None else row.get("role_sort"),
                row.get("status") or "0",
                "" if created is None else created,
            ])
        return buffer.getvalue()

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
        clean_menus = self._check_menu_ids(menu_ids)
        self._write_role_menus(role_id, clean_menus)
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
            SELECT menu_id, parent_id, menu_name, menu_type, perms,
                   order_num, path, visible
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
                self._fail("Unknown parent menu {0}.".format(parent_id), "open-rbac menu-list")
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

    def menu_edit(self, actor, menu_id, menu_name, parent_id, menu_type, perms="", path="", visible="0"):
        """General Purpose: Change one listed menu. An empty type is not stored as F."""
        self.require(actor, "system:menu:edit")
        current = self._menu_open(menu_id)
        name = (menu_name or "").strip()
        if not name or len(name) > 50:
            self._fail("menu_name is required.", "set --menu-name")
        if menu_type not in ("M", "C", "F"):
            self._fail("menu_type must be M, C, or F.", "M directory, C page, F button")
        try:
            parent = int(parent_id)
        except (TypeError, ValueError):
            self._fail("Unknown parent menu {0}.".format(parent_id), "open-rbac menu-list")
        if parent != 0:
            found = self.store.query_one(
                "SELECT menu_id FROM sys_menu WHERE menu_id = %s",
                (parent,),
            )
            if found is None:
                self._fail("Unknown parent menu {0}.".format(parent_id), "open-rbac menu-list")
        if self._menu_under(int(current["menu_id"]), parent):
            self._fail("A menu cannot sit under itself.", "choose another parent")
        shown = "" if visible is None else str(visible).strip()
        if shown == "":
            shown = "0"
        if shown not in ("0", "1"):
            self._fail("visible must be 0 or 1.", "0 show, 1 hide")
        self.store.execute(
            """
            UPDATE sys_menu
            SET menu_name = %s, parent_id = %s, menu_type = %s, perms = %s,
                path = %s, visible = %s, update_by = %s, update_time = NOW()
            WHERE menu_id = %s
            """,
            (
                name, parent, menu_type, perms or "", path or "", shown,
                actor["user_name"], int(current["menu_id"]),
            ),
        )
        self.audit.write_oper(actor, "Menu", 2, "menu_edit", param=name)
        return int(current["menu_id"])

    def menu_remove(self, actor, menu_id):
        """General Purpose: Delete one menu that has no listed child, and its role links."""
        self.require(actor, "system:menu:remove")
        current = self._menu_open(menu_id)
        ident = int(current["menu_id"])
        child = self.store.query_one(
            "SELECT menu_id FROM sys_menu WHERE parent_id = %s AND status = '0'",
            (ident,),
        )
        if child is not None:
            self._fail("That menu has children.", "remove the children first")
        self.store.execute("DELETE FROM sys_role_menu WHERE menu_id = %s", (ident,))
        self.store.execute("DELETE FROM sys_menu WHERE menu_id = %s", (ident,))
        self.audit.write_oper(actor, "Menu", 3, "menu_remove", param=current.get("menu_name") or "")
        return ident

    def menu_sort(self, actor, menu_ids, order_nums):
        """General Purpose: Store a whole-number order for each listed menu in the pair."""
        self.require(actor, "system:menu:edit")
        if isinstance(menu_ids, str) or isinstance(order_nums, str):
            self._fail("Choose a sort for each menu.", "send one order for each menu")
        ids = list(menu_ids or [])
        orders = list(order_nums or [])
        if len(ids) != len(orders):
            self._fail("Choose a sort for each menu.", "send one order for each menu")
        pairs = []
        for raw_id, raw_order in zip(ids, orders):
            current = self._menu_open(raw_id)
            pairs.append((self._menu_order(raw_order), int(current["menu_id"])))
        for number, ident in pairs:
            self.store.execute(
                """
                UPDATE sys_menu
                SET order_num = %s, update_by = %s, update_time = NOW()
                WHERE menu_id = %s
                """,
                (number, actor["user_name"], ident),
            )
        self.audit.write_oper(actor, "Menu", 2, "menu_sort", param=str(len(pairs)))
        return len(pairs)

    def _menu_open(self, menu_id):
        """General Purpose: One status-0 menu, or the unknown-menu sentence."""
        text = "" if menu_id is None else str(menu_id).strip()
        if not text.isdigit():
            self._fail("Unknown menu {0}.".format(menu_id), "open-rbac menu-list")
        row = self.store.query_one(
            """
            SELECT menu_id, parent_id, menu_name, menu_type, perms,
                   order_num, path, visible, status
            FROM sys_menu
            WHERE menu_id = %s AND status = '0'
            """,
            (int(text),),
        )
        if row is None:
            self._fail("Unknown menu {0}.".format(menu_id), "open-rbac menu-list")
        return row

    def _menu_under(self, menu_id, parent_id):
        """True when the new parent is this menu or a descendant of it.

        The walk goes up from the proposed parent. A cycle in the stored
        parents stops the walk.
        """
        menu_id = int(menu_id)
        parent_id = int(parent_id)
        if parent_id == 0:
            return False
        if parent_id == menu_id:
            return True
        seen = set()
        current = parent_id
        while current != 0 and current not in seen:
            seen.add(current)
            row = self.store.query_one(
                "SELECT parent_id FROM sys_menu WHERE menu_id = %s",
                (current,),
            )
            if row is None:
                return False
            try:
                current = int(row.get("parent_id") or 0)
            except (TypeError, ValueError):
                return False
            if current == menu_id:
                return True
        return False

    def _menu_order(self, raw):
        """General Purpose: A sort from 0 to 9999. An empty value is 0."""
        text = "" if raw is None else str(raw).strip()
        if text == "":
            return 0
        if not text.isdigit() or int(text) > 9999:
            self._fail(
                "order_num must be a number.",
                "use a whole number from 0 to 9999",
            )
        return int(text)

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
                self._fail("Unknown parent department {0}.".format(parent_id), "open-rbac dept-list")
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

    def job_title_list(self, actor):
        self.require(actor, "system:jobtitle:list")
        return self.store.query_all(
            """
            SELECT job_title_id, job_title_code, job_title, job_title_sort, status
            FROM sys_job_title
            ORDER BY job_title_sort, job_title_id
            """
        )

    def job_title_add(self, actor, job_title_code, job_title):
        self.require(actor, "system:jobtitle:add")
        code = (job_title_code or "").strip()
        name = (job_title or "").strip()
        if not code or not name:
            self._fail("job_title_code and job_title are required.", "set both")
        existing = self.store.query_one(
            "SELECT job_title_id FROM sys_job_title WHERE job_title_code = %s",
            (code,),
        )
        if existing:
            self._fail("That job_title_code is already in use.", "pick another job_title_code")
        done = self.store.execute(
            """
            INSERT INTO sys_job_title
              (job_title_code, job_title, job_title_sort, status, create_by, create_time)
            VALUES (%s, %s, 0, '0', %s, NOW())
            """,
            (code, name, actor["user_name"]),
        )
        self.audit.write_oper(actor, "Job Title", 1, "job_title_add", param=code)
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
