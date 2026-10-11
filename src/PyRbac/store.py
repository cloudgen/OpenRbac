# =============================================================================
# MySQL access for PyRbac.
# requirement-database — one connection per call, parameters only.
# requirement-python-oop — class Store and StoreError.
# =============================================================================
from __future__ import annotations


class StoreError(Exception):
    """The database did not complete the call."""

    def __init__(self, message, nxt, logger=None):
        super().__init__(message)
        self.logger = logger
        self.nxt = nxt
        if logger is not None:
            logger.log_message("instantiated", component="StoreError")


class Store:
    """Short MySQL connections. Callers pass parameters. This class does not build SQL from names."""

    def __init__(self, settings, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Store")
        self.settings = settings

    def connect(self):
        """General Purpose: One new connection. The caller closes it."""
        try:
            import pymysql
            from pymysql.cursors import DictCursor
        except ImportError:
            raise StoreError(
                "PyMySQL is required.",
                'python -m pip install "PyMySQL>=1.1.0"',
                logger=self.logger,
            )
        try:
            cfg = self.settings.database()
        except Exception as exc:
            nxt = getattr(exc, "nxt", "check PYRBAC_DB_PASSWORD")
            raise StoreError(str(exc), nxt, logger=self.logger)
        try:
            return pymysql.connect(
                host=cfg["host"],
                port=cfg["port"],
                user=cfg["user"],
                password=cfg["password"],
                database=cfg["database"],
                charset="utf8mb4",
                cursorclass=DictCursor,
                autocommit=False,
            )
        except Exception as exc:
            if self.logger is not None:
                self.logger.log_message(
                    "database open failed",
                    level="ERROR",
                    component="Store",
                )
            raise StoreError(
                "Cannot open the MySQL database {0}.".format(cfg["database"]),
                "check PYRBAC_DB_HOST, PYRBAC_DB_USER, and PYRBAC_DB_PASSWORD, then py-rbac db-init",
                logger=self.logger,
            ) from exc

    def _run(self, sql, args, fetch):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)
                rows = cursor.fetchall() if fetch else []
                done = {
                    "rows": list(rows),
                    "lastrowid": cursor.lastrowid,
                    "rowcount": cursor.rowcount,
                }
            connection.commit()
            return done
        except StoreError:
            raise
        except Exception as exc:
            try:
                connection.rollback()
            except Exception:
                pass
            if self.logger is not None:
                self.logger.log_message(
                    "database statement failed",
                    level="ERROR",
                    component="Store",
                )
            raise StoreError(
                "The database statement failed.",
                "py-rbac db-init",
                logger=self.logger,
            ) from exc
        finally:
            connection.close()

    def query_all(self, sql, args=()):
        """General Purpose: Every row from one parameterized statement."""
        return self._run(sql, args, True)["rows"]

    def query_one(self, sql, args=()):
        """General Purpose: The first row, or None."""
        rows = self.query_all(sql, args)
        if not rows:
            return None
        return rows[0]

    def execute(self, sql, args=()):
        """General Purpose: One write statement. Returns lastrowid and rowcount."""
        return self._run(sql, args, False)

    def transaction(self, work):
        """General Purpose: Several statements. work(run) sees one connection. Commit is once."""
        connection = self.connect()

        def run(sql, args=()):
            with connection.cursor() as cursor:
                cursor.execute(sql, args)
                return {
                    "rows": list(cursor.fetchall()),
                    "lastrowid": cursor.lastrowid,
                    "rowcount": cursor.rowcount,
                }

        try:
            result = work(run)
            connection.commit()
            return result
        except StoreError:
            try:
                connection.rollback()
            except Exception:
                pass
            raise
        except Exception as exc:
            try:
                connection.rollback()
            except Exception:
                pass
            if self.logger is not None:
                self.logger.log_message(
                    "database transaction failed",
                    level="ERROR",
                    component="Store",
                )
            raise StoreError(
                "The database transaction failed.",
                "py-rbac db-init",
                logger=self.logger,
            ) from exc
        finally:
            connection.close()
