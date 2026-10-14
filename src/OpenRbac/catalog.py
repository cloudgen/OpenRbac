# =============================================================================
# Centralized parameters, dictionaries, and notices.
# requirement-domain-openrbac — setup surface.
# requirement-python-oop — class Catalog.
# =============================================================================
from __future__ import annotations

from .access import AccessError


class Catalog:
    """sys_config, sys_dict_type, sys_dict_data, and sys_notice.

    The same methods serve the terminal, the text menu, and the web pages.
    """

    def __init__(self, store, access, audit, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Catalog")
        self.store = store
        self.access = access
        self.audit = audit

    def _fail(self, message, nxt):
        raise AccessError(message, nxt, logger=self.logger)

    def config_list(self, actor):
        self.access.require(actor, "system:config:list")
        return self.store.query_all(
            """
            SELECT config_key, config_name, config_value, config_type
            FROM sys_config
            ORDER BY config_id
            """
        )

    def config_set(self, actor, config_key, config_value):
        self.access.require(actor, "system:config:edit")
        row = self.store.query_one(
            "SELECT config_id, config_key FROM sys_config WHERE config_key = %s",
            (config_key,),
        )
        if row is None:
            self._fail("Unknown parameter {0}.".format(config_key), "open-rbac config-list")
        value = "" if config_value is None else str(config_value)
        if len(value) > 500:
            self._fail("config_value must be 500 characters or fewer.", "shorten the value")
        self.store.execute(
            """
            UPDATE sys_config
            SET config_value = %s, update_by = %s, update_time = NOW()
            WHERE config_key = %s
            """,
            (value, actor["user_name"], config_key),
        )
        self.audit.write_oper(actor, "Parameter", 2, "config_set", param=config_key)
        return config_key

    def config_add(self, actor, config_key, config_name, config_value):
        self.access.require(actor, "system:config:add")
        key = (config_key or "").strip()
        if not key or len(key) > 100:
            self._fail("config_key is required.", "set --config-key")
        existing = self.store.query_one(
            "SELECT config_id FROM sys_config WHERE config_key = %s",
            (key,),
        )
        if existing:
            self._fail("That parameter already exists.", "open-rbac config-set --config-key {0}".format(key))
        self.store.execute(
            """
            INSERT INTO sys_config
              (config_name, config_key, config_value, config_type, create_by, create_time)
            VALUES (%s, %s, %s, 'N', %s, NOW())
            """,
            ((config_name or key)[:100], key, (config_value or "")[:500], actor["user_name"]),
        )
        self.audit.write_oper(actor, "Parameter", 1, "config_add", param=key)
        return key

    def dict_list(self, actor):
        self.access.require(actor, "system:dict:list")
        return self.store.query_all(
            """
            SELECT d.dict_type, d.dict_label, d.dict_value, d.status
            FROM sys_dict_data d
            ORDER BY d.dict_type, d.dict_sort, d.dict_code
            """
        )

    def dict_add(self, actor, dict_type, dict_label, dict_value):
        self.access.require(actor, "system:dict:add")
        kind = self.store.query_one(
            "SELECT dict_type FROM sys_dict_type WHERE dict_type = %s AND status = '0'",
            (dict_type,),
        )
        if kind is None:
            self._fail("Unknown dictionary type {0}.".format(dict_type), "open-rbac dict-list")
        label = (dict_label or "").strip()
        value = (dict_value or "").strip()
        if not label or not value:
            self._fail("dict_label and dict_value are required.", "set both")
        self.store.execute(
            """
            INSERT INTO sys_dict_data
              (dict_sort, dict_label, dict_value, dict_type, is_default, status,
               create_by, create_time)
            VALUES (0, %s, %s, %s, 'N', '0', %s, NOW())
            """,
            (label[:100], value[:100], dict_type, actor["user_name"]),
        )
        self.audit.write_oper(actor, "Dictionary", 1, "dict_add", param=dict_type)
        return label

    def notice_list(self, actor):
        self.access.require(actor, "system:notice:list")
        return self.store.query_all(
            """
            SELECT notice_id, notice_title, notice_type, status
            FROM sys_notice
            ORDER BY notice_id
            """
        )

    def notice_add(self, actor, title, notice_type, content):
        self.access.require(actor, "system:notice:add")
        name = (title or "").strip()
        if not name or len(name) > 50:
            self._fail("The notice title is required.", "set --title")
        if str(notice_type) not in ("1", "2"):
            self._fail("notice_type must be 1 (notice) or 2 (announcement).", "set --notice-type 1")
        self.store.execute(
            """
            INSERT INTO sys_notice
              (notice_title, notice_type, notice_content, status, create_by, create_time)
            VALUES (%s, %s, %s, '0', %s, NOW())
            """,
            (name, str(notice_type), content or "", actor["user_name"]),
        )
        self.audit.write_oper(actor, "Notice", 1, "notice_add", param=name)
        return name

    def oper_log(self, actor):
        self.access.require(actor, "monitor:operlog:list")
        return self.audit.oper_rows()

    def login_log(self, actor):
        self.access.require(actor, "monitor:logininfor:list")
        return self.audit.login_rows()

    def online_list(self, actor):
        self.access.require(actor, "monitor:online:list")
        return self.audit.online_rows()

    def online_logout(self, actor, token):
        self.access.require(actor, "monitor:online:forceLogout")
        if not token:
            self._fail("A session token is required.", "open-rbac online-list")
        count = self.audit.drop_session(token)
        if count == 0:
            self._fail("That session is not online.", "open-rbac online-list")
        self.audit.write_oper(actor, "Online", 3, "online_logout", param=token[:8])
        return count
