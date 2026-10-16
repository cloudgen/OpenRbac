# =============================================================================
# Text tables shared by the terminal and the text menu.
# requirement-domain-openrbac — the same rows on both surfaces.
# requirement-python-oop — class ReportText.
# =============================================================================
from __future__ import annotations


class ReportText:
    """Plain text tables. The web pages use the same row dictionaries."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ReportText")

    def table(self, columns, rows) -> str:
        """General Purpose: A header and one line per row. Cells are separated by a bar."""
        lines = ["|".join(columns)]
        if not rows:
            lines.append("(none)")
            return "\n".join(lines)
        for row in rows:
            cells = []
            for name in columns:
                value = row.get(name)
                if value is None:
                    value = ""
                cells.append(str(value).replace("|", "/").replace("\n", " "))
            lines.append("|".join(cells))
        return "\n".join(lines)

    def users(self, rows) -> str:
        return self.table(
            ("user_id", "user_name", "nick_name", "dept_id", "dept_name", "status"),
            rows,
        )

    def roles(self, rows) -> str:
        return self.table(
            ("role_id", "role_name", "role_key", "data_scope", "status"),
            rows,
        )

    def menus(self, rows) -> str:
        return self.table(
            ("menu_id", "parent_id", "menu_name", "menu_type", "perms"),
            rows,
        )

    def depts(self, rows) -> str:
        return self.table(
            ("dept_id", "parent_id", "dept_name", "ancestors", "status"),
            rows,
        )

    def job_titles(self, rows) -> str:
        return self.table(
            ("job_title_id", "job_title_code", "job_title", "job_title_sort", "status"),
            rows,
        )

    def configs(self, rows) -> str:
        return self.table(
            ("config_key", "config_name", "config_value", "config_type"),
            rows,
        )

    def dicts(self, rows) -> str:
        return self.table(
            ("dict_type", "dict_label", "dict_value", "status"),
            rows,
        )

    def notices(self, rows) -> str:
        return self.table(
            ("notice_id", "notice_title", "notice_type", "status"),
            rows,
        )

    def login_log(self, rows) -> str:
        return self.table(
            ("info_id", "user_name", "ipaddr", "status", "msg", "login_time"),
            rows,
        )

    def oper_log(self, rows) -> str:
        return self.table(
            ("oper_id", "title", "business_type", "oper_name", "status", "oper_time"),
            rows,
        )

    def online(self, rows) -> str:
        return self.table(
            ("token", "user_name", "ipaddr", "surface", "login_time"),
            rows,
        )
