# =============================================================================
# Web interface for the same RBAC actions as the text menu.
# requirement-web-interface — loopback pages, cookie session, permission checks.
# requirement-python-html-template — HtmlTemplate renders each HTML body.
# requirement-python-project-structure — pages stay under templates/. No frontend tree.
# requirement-html-element-plus — the page tags. They emit the Apex shell classes.
# requirement-html-theme — the stored theme picks the color sheet. The shell stays.
# requirement-html-user-management — GET /users is the User Management page.
# requirement-html-role-management — GET /roles is the Role Management page.
# requirement-html-dictionaries — GET /dicts is the dictionary type list.
# requirement-html-login-log — GET /login-log is the Login log page.
# requirement-html-parameter-management — GET /configs is the Parameter Management page.
# requirement-html-online — GET /online is the Online page.
# requirement-python-oop — class WebApp. The standard-library handler is created
# inside make_server because that library constructs the handler itself.
# =============================================================================
from __future__ import annotations

import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

from .html_template import HtmlTemplate
from .settings import Settings, SettingsError


class WebApp:
    """Small HTTP site. Every HTML body comes from HtmlTemplate."""

    COOKIE = "openrbac_session"
    VENDOR = Path(__file__).resolve().parent / "element_plus"
    ROLE_SCOPES = {
        "1": ("All data", "success"),
        "2": ("Custom data", "primary"),
        "3": ("This department", "warning"),
        "4": ("Department and children", "info"),
    }
    _DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    def __init__(self, settings, access, catalog, report, logger=None, prepare=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="WebApp")
        self.settings = settings
        self.access = access
        self.catalog = catalog
        self.report = report
        self.prepare = prepare
        self.templates = HtmlTemplate(logger=logger)
        self.httpd = None
        self.thread = None
        self._request = threading.local()

    def url(self) -> str:
        if self.httpd is None:
            host, port = self.settings.bind()
        else:
            host, port = self.httpd.server_address[0], self.httpd.server_address[1]
        return "http://{0}:{1}/".format(host, port)

    def make_server(self):
        """General Purpose: A loopback server unless remote bind was explicitly allowed."""
        host, port = self.settings.bind()
        outer = self

        class Handler(BaseHTTPRequestHandler):
            """Constructed by ThreadingHTTPServer. WebApp owns the actions."""

            def do_GET(self):
                outer.get(self)

            def do_POST(self):
                outer.post(self)

            def log_message(self, fmt, *args):
                if outer.logger is not None:
                    outer.logger.log_message(
                        "http {0}".format(fmt % args),
                        component="WebApp",
                    )

        self.httpd = ThreadingHTTPServer((host, port), Handler)
        return self.httpd

    def serve_foreground(self):
        """General Purpose: Serve until the process is interrupted."""
        server = self.make_server()
        if self.logger is not None:
            self.logger.log_message(
                "listening {0}".format(self.url()),
                component="WebApp",
            )
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def start_background(self) -> str:
        """General Purpose: Serve on a daemon thread and return the URL."""
        if self.thread is not None and self.thread.is_alive():
            return self.url()
        self.make_server()
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        if self.logger is not None:
            self.logger.log_message(
                "listening {0}".format(self.url()),
                component="WebApp",
            )
        return self.url()

    def stop(self):
        """General Purpose: Stop the server if this object started one."""
        server = self.httpd
        if server is not None:
            try:
                server.shutdown()
            except Exception:
                pass
            try:
                server.server_close()
            except Exception:
                pass
        self.httpd = None
        self.thread = None

    def get(self, handler):
        path = urlparse(handler.path).path or "/"
        self._request.path = self._clean_path(path)
        try:
            if path == "/apex.css":
                self._send_static(handler, "apex.css", "text/css; charset=utf-8")
                return
            theme_css = self._theme_css(path)
            if theme_css:
                self._send_static(handler, theme_css, "text/css; charset=utf-8")
                return
            if path == "/element-plus.LICENSE":
                self._send_static(handler, "LICENSE", "text/plain; charset=utf-8")
                return
            if path == "/table-check.js":
                self._send_static(handler, "table-check.js", "text/javascript; charset=utf-8")
                return
            icon = self._icon_file(path)
            if icon:
                self._send_static(handler, icon, "image/svg+xml")
                return
            user = self._user(handler)
            if path == "/login":
                self._send(handler, 200, self.login_page(""))
                return
            if user is None:
                self._redirect(handler, "/login")
                return
            query = parse_qs(urlparse(handler.path).query, keep_blank_values=True)
            self._request.query = query
            if path == "/users/export":
                self._export_users(handler, user)
                return
            if path == "/roles/export":
                self._export_roles(handler, user)
                return
            error = self._first(query, "error")
            body = self._route_get(path, user, error)
            if body is None:
                self._send(handler, 404, self._message(user, "Not found", "That page is not on this site."))
                return
            self._send(handler, 200, body)
        except Exception as exc:
            self._fail(handler, exc)
        finally:
            self._request.path = ""
            self._request.query = {}

    def post(self, handler):
        path = urlparse(handler.path).path or "/"
        self._request.path = self._clean_path(path)
        try:
            form = self._form(handler)
            if path == "/login":
                self._post_login(handler, form)
                return
            user = self._user(handler)
            if user is None:
                self._redirect(handler, "/login")
                return
            if not self._csrf_ok(user, form):
                self._send(
                    handler,
                    400,
                    self._message(user, "Rejected", "The form token did not match this session."),
                )
                return
            self._route_post(handler, path, user, form)
        except Exception as exc:
            self._fail(handler, exc)
        finally:
            self._request.path = ""

    def _route_get(self, path, user, error):
        if path == "/":
            return self.home_page(user, error)
        if path == "/users":
            self.access.require(user, "system:user:list")
            return self.users_page(user, error)
        if path == "/test":
            self.access.require(user, "system:user:list")
            return self.test_page(user, error)
        if path == "/roles":
            self.access.require(user, "system:role:list")
            return self.roles_page(user, error)
        if path == "/menus":
            self.access.require(user, "system:menu:list")
            return self.menus_page(user, error)
        if path == "/depts":
            self.access.require(user, "system:dept:list")
            return self.depts_page(user, error)
        if path == "/job-titles":
            self.access.require(user, "system:jobtitle:list")
            return self.job_titles_page(user, error)
        if path == "/configs":
            self.catalog.access.require(user, "system:config:list")
            return self.configs_page(user, error)
        if path == "/dicts":
            self.catalog.access.require(user, "system:dict:list")
            return self.dicts_page(user, error)
        if path == "/notices":
            self.catalog.access.require(user, "system:notice:list")
            return self.notices_page(user, error)
        if path == "/oper-log":
            self.catalog.access.require(user, "monitor:operlog:list")
            return self.oper_log_page(user, error)
        if path == "/login-log":
            self.catalog.access.require(user, "monitor:logininfor:list")
            return self.login_log_page(user, error)
        if path == "/online":
            self.catalog.access.require(user, "monitor:online:list")
            return self.online_page(user, error)
        if path == "/database":
            self.access.require(user, "system:config:edit")
            return self.database_page(user, error)
        return None

    def _route_post(self, handler, path, user, form):
        if path == "/logout":
            self.access.logout(user.get("token"))
            self._redirect(handler, "/login", clear=True)
            return
        if path == "/users/add":
            self.access.user_add(
                user,
                self._first(form, "user_name"),
                self._first(form, "nick_name"),
                int(self._first(form, "dept_id") or "0"),
                int(self._first(form, "role_id") or "0"),
                self._first(form, "password"),
            )
            self._redirect(handler, "/users")
            return
        if path == "/users/edit":
            user_id = int(self._first(form, "user_id") or "0")
            visible = False
            for row in self.access.user_list(user):
                if int(row["user_id"]) == user_id:
                    visible = True
                    break
            if not visible:
                raise ValueError("That account is not in this list.")
            dept_id = None
            if "dept_id" in form:
                raw_dept = self._first(form, "dept_id").strip()
                if not raw_dept.isdigit() or int(raw_dept) <= 0:
                    raise ValueError("A department is required.")
                dept_id = int(raw_dept)
            self.access.user_edit(
                user,
                user_id,
                nick_name=self._posted(form, "nick_name"),
                dept_id=dept_id,
                status=self._posted(form, "status"),
                phonenumber=self._posted(form, "phonenumber"),
                email=self._posted(form, "email"),
                sex=self._posted(form, "sex"),
                remark=self._posted(form, "remark"),
                job_title_ids=self._posted_ids(form, "job_title_id"),
                role_ids=self._posted_ids(form, "role_id"),
            )
            self._redirect(handler, self._users_href({
                "user_name": self._first(form, "user_name"),
                "phone": self._first(form, "phone"),
                "state": self._first(form, "state"),
                "begin": self._first(form, "begin"),
                "end": self._first(form, "end"),
                "dept": self._first(form, "dept"),
            }))
            return
        if path == "/users/status":
            user_id = int(self._first(form, "user_id") or "0")
            visible = False
            for row in self.access.user_list(user):
                if int(row["user_id"]) == user_id:
                    visible = True
                    break
            if not visible:
                raise ValueError("That account is not in this list.")
            self.access.user_edit(user, user_id, status=self._first(form, "status"))
            self._redirect(handler, self._users_href({
                "user_name": self._first(form, "user_name"),
                "phone": self._first(form, "phone"),
                "state": self._first(form, "state"),
                "begin": self._first(form, "begin"),
                "end": self._first(form, "end"),
                "dept": self._first(form, "dept"),
            }))
            return
        if path == "/users/remove":
            self.access.user_remove(user, int(self._first(form, "user_id") or "0"))
            self._redirect(handler, "/users")
            return
        if path == "/users/reset":
            self.access.user_reset_password(
                user,
                int(self._first(form, "user_id") or "0"),
                self._first(form, "password"),
            )
            self._redirect(handler, "/users")
            return
        if path == "/users/import":
            filename = self._first(form, "file_filename")
            if filename and not filename.lower().endswith(".csv"):
                raise ValueError("Import accepts a .csv file.")
            result = self.access.user_import(
                user,
                self._first(form, "file"),
                self._first(form, "update_support") in ("1", "on", "true"),
            )
            self._redirect(
                handler,
                "/users?" + urlencode({
                    "note": "Imported {0}. Updated {1}.".format(result["added"], result["updated"]),
                }),
            )
            return
        if path == "/roles/add":
            self.access.role_add(
                user,
                self._first(form, "role_name"),
                self._first(form, "role_key"),
                self._first(form, "role_sort"),
                status=self._first(form, "status") or None,
                remark=self._first(form, "remark"),
                menu_ids=self._posted_ints(form, "menu_id"),
            )
            self._redirect(handler, "/roles")
            return
        if path == "/roles/edit":
            role_id = int(self._first(form, "role_id") or "0")
            if not self._role_listed(user, role_id):
                raise ValueError("That role is not in this list.")
            self.access.role_edit(
                user,
                role_id,
                role_name=self._first(form, "role_name"),
                role_key=self._first(form, "role_key"),
                role_sort=self._first(form, "role_sort"),
                status=self._first(form, "status") or None,
                remark=self._first(form, "remark"),
                menu_ids=self._posted_ints(form, "menu_id"),
            )
            self._redirect(handler, "/roles")
            return
        if path == "/roles/remove":
            role_id = int(self._first(form, "role_id") or "0")
            if not self._role_listed(user, role_id):
                raise ValueError("That role is not in this list.")
            self.access.role_remove(user, role_id)
            self._redirect(handler, "/roles")
            return
        if path == "/roles/status":
            role_id = int(self._first(form, "role_id") or "0")
            if not self._role_listed(user, role_id):
                raise ValueError("That role is not in this list.")
            self.access.role_edit(user, role_id, status=self._first(form, "status"))
            self._redirect(handler, self._roles_href({
                "role_name": self._first(form, "role_name"),
                "role_key": self._first(form, "role_key"),
                "state": self._first(form, "state"),
                "begin": self._first(form, "begin"),
                "end": self._first(form, "end"),
            }))
            return
        if path == "/roles/grant":
            menus = self._posted_ints(form, "menu_id")
            depts = self._posted_ints(form, "dept_id")
            scope = self._first(form, "data_scope") or None
            self.access.role_grant(
                user,
                int(self._first(form, "role_id") or "0"),
                menus,
                data_scope=scope,
                dept_ids=depts,
            )
            self._redirect(handler, "/roles")
            return
        if path == "/menus/add":
            self.access.menu_add(
                user,
                self._first(form, "menu_name"),
                int(self._first(form, "parent_id") or "0"),
                self._first(form, "menu_type") or "F",
                self._first(form, "perms"),
                self._first(form, "path"),
            )
            self._redirect(handler, self._menu_back(form))
            return
        if path == "/menus/edit":
            self.access.menu_edit(
                user,
                self._first(form, "menu_id") or "0",
                self._first(form, "menu_name"),
                int(self._first(form, "parent_id") or "0"),
                self._first(form, "menu_type"),
                self._first(form, "perms"),
                self._first(form, "path"),
                self._first(form, "visible"),
            )
            self._redirect(handler, self._menu_back(form))
            return
        if path == "/menus/remove":
            self.access.menu_remove(user, self._first(form, "menu_id") or "0")
            self._redirect(handler, self._menu_back(form))
            return
        if path == "/menus/sort":
            self.access.menu_sort(
                user,
                form.get("menu_id") or [],
                form.get("order_num") or [],
            )
            self._redirect(handler, self._menu_back(form))
            return
        if path == "/depts/add":
            self.access.dept_add(
                user,
                self._first(form, "dept_name"),
                int(self._first(form, "parent_id") or "0"),
            )
            self._redirect(handler, "/depts")
            return
        if path == "/job-titles/add":
            self.access.job_title_add(
                user,
                self._first(form, "job_title_code"),
                self._first(form, "job_title"),
            )
            self._redirect(handler, "/job-titles")
            return
        if path == "/configs/set":
            self.catalog.config_set(
                user,
                self._first(form, "config_key"),
                self._first(form, "config_value"),
            )
            self._redirect(handler, "/configs")
            return
        if path == "/dicts/add":
            self.catalog.dict_add(
                user,
                self._first(form, "dict_type"),
                self._first(form, "dict_label"),
                self._first(form, "dict_value"),
            )
            self._redirect(handler, "/dicts")
            return
        if path == "/notices/add":
            self.catalog.notice_add(
                user,
                self._first(form, "title"),
                self._first(form, "notice_type") or "1",
                self._first(form, "content"),
            )
            self._redirect(handler, "/notices")
            return
        if path == "/online/logout":
            self.catalog.online_logout(user, self._first(form, "token"))
            self._redirect(handler, "/online")
            return
        if path == "/database":
            self.access.require(user, "system:config:edit")
            before = self.settings.engine()
            self._apply_posted_engine(handler, form, allow_remote=True)
            if self.settings.engine() != before:
                self._redirect(handler, "/login", clear=True)
                return
            self._redirect(handler, "/database")
            return
        self._send(handler, 404, self._message(user, "Not found", "That action is not on this site."))

    def _loopback(self, handler) -> bool:
        host = ""
        if getattr(handler, "client_address", None):
            host = handler.client_address[0]
        return host in ("127.0.0.1", "::1", "localhost")

    def _apply_posted_engine(self, handler, form, allow_remote=False):
        """Store a posted sqlite3 or mysql choice. A remote login cannot switch engines."""
        posted = self._first(form, "engine").strip().lower()
        if posted == "":
            return
        if posted in ("1", "sqlite3"):
            wanted = "sqlite3"
        elif posted in ("2", "mysql"):
            wanted = "mysql"
        else:
            raise SettingsError(
                "The database engine must be sqlite3 or mysql.",
                "choose sqlite3 or mysql",
                logger=self.logger,
            )
        if wanted == self.settings.engine():
            return
        if not allow_remote and not self._loopback(handler):
            raise SettingsError(
                "The database engine can be changed from this computer.",
                "open the site on 127.0.0.1, or run open-rbac db-engine",
                logger=self.logger,
            )
        self.settings.apply_choice(wanted)

    def _post_login(self, handler, form):
        self._apply_posted_engine(handler, form)
        if self.prepare is not None:
            self.prepare()
        user = self.access.login(
            self._first(form, "user_name"),
            self._first(form, "password"),
            ipaddr=handler.client_address[0] if handler.client_address else "",
            surface="web",
            user_agent=handler.headers.get("User-Agent", ""),
        )
        self._redirect(handler, "/", cookie=user["token"])

    def _fail(self, handler, exc):
        message = str(exc)
        nxt = getattr(exc, "nxt", "") or ""
        code = 403 if message.startswith("Missing permission") else 400
        try:
            user = self._user(handler)
        except Exception:
            user = None
        try:
            body = self._message(user, "Not completed", message, nxt)
        except Exception:
            text = message if nxt == "" else "{0}\n{1}".format(message, nxt)
            self._send_bytes(handler, code, (text + "\n").encode("utf-8"), "text/plain; charset=utf-8")
            return
        self._send(handler, code, body)

    def _user(self, handler):
        token = self._cookie(handler).get(self.COOKIE, "")
        if not token:
            return None
        return self.access.actor_from_token(token)

    def _cookie(self, handler):
        raw = handler.headers.get("Cookie", "")
        found = {}
        for part in raw.split(";"):
            if "=" not in part:
                continue
            key, value = part.split("=", 1)
            found[key.strip()] = value.strip()
        return found

    def _form(self, handler):
        length = int(handler.headers.get("Content-Length", "0") or "0")
        if length < 0 or length > 100000:
            raise ValueError("The form is too large.")
        raw = handler.rfile.read(length)
        ctype = handler.headers.get("Content-Type", "")
        if ctype.lower().startswith("multipart/form-data"):
            return self._multipart(raw, ctype)
        return parse_qs(raw.decode("utf-8", "replace"), keep_blank_values=True)

    def _multipart(self, raw, ctype):
        """General Purpose: One posted form that carries a csv file.

        requirement-html-user-management — import posts the file with the token.
        """
        marker = ""
        for piece in ctype.split(";"):
            piece = piece.strip()
            if piece.lower().startswith("boundary="):
                marker = piece.split("=", 1)[1].strip().strip('"')
        if not marker:
            raise ValueError("The upload has no boundary.")
        found = {}
        delimiter = ("--" + marker).encode("utf-8")
        for chunk in raw.split(delimiter):
            if chunk.startswith(b"\r\n"):
                chunk = chunk[2:]
            if chunk.endswith(b"\r\n"):
                chunk = chunk[:-2]
            if chunk in (b"", b"--"):
                continue
            if chunk.startswith(b"--"):
                continue
            head, sep, body = chunk.partition(b"\r\n\r\n")
            if not sep:
                continue
            disposition = ""
            for line in head.decode("utf-8", "replace").split("\r\n"):
                if line.lower().startswith("content-disposition:"):
                    disposition = line
                    break
            name = ""
            filename = ""
            for token in disposition.split(";"):
                token = token.strip()
                if token.lower().startswith("name="):
                    name = token.split("=", 1)[1].strip().strip('"')
                elif token.lower().startswith("filename="):
                    filename = token.split("=", 1)[1].strip().strip('"')
            if not name:
                continue
            if filename:
                found.setdefault(name, []).append(body.decode("utf-8-sig", "replace"))
                found.setdefault(name + "_filename", []).append(filename)
            else:
                found.setdefault(name, []).append(body.decode("utf-8", "replace"))
        return found

    def _first(self, form, name):
        values = form.get(name) or [""]
        return values[0]

    def _posted(self, form, name):
        """A missing key stays unchanged. A present key, including empty, is the new value."""
        if name not in form:
            return None
        return self._first(form, name)

    def _posted_ids(self, form, name):
        if name not in form:
            return None
        return self._number_list(form.get(name))

    def _number_list(self, values):
        found = []
        seen = set()
        for raw in values or []:
            text = str(raw).strip()
            if not text.isdigit():
                continue
            number = int(text)
            if number <= 0 or number in seen:
                continue
            seen.add(number)
            found.append(number)
        return found

    def _dept_number(self, value):
        try:
            number = int(value)
        except (TypeError, ValueError):
            return None
        if number <= 0:
            return None
        return number

    def _optional_int(self, form, name):
        raw = self._first(form, name)
        if raw == "":
            return None
        return int(raw)

    def _csrf_ok(self, user, form):
        return self._first(form, "csrf") != "" and self._first(form, "csrf") == user.get("csrf")

    def _send(self, handler, code, body, extra=None):
        data = body.encode("utf-8")
        handler.send_response(code)
        handler.send_header("Content-Type", "text/html; charset=utf-8")
        handler.send_header("Content-Length", str(len(data)))
        handler.send_header("X-Content-Type-Options", "nosniff")
        handler.send_header("Referrer-Policy", "no-referrer")
        handler.send_header(
            "Content-Security-Policy",
            "default-src 'none'; style-src 'self' 'unsafe-inline'; script-src 'self'; img-src 'self' data:; form-action 'self'",
        )
        if extra:
            for key, value in extra:
                handler.send_header(key, value)
        handler.end_headers()
        handler.wfile.write(data)

    def _send_bytes(self, handler, code, data, content_type, extra=None):
        """General Purpose: One non-HTML response, such as the stylesheet."""
        handler.send_response(code)
        handler.send_header("Content-Type", content_type)
        handler.send_header("Content-Length", str(len(data)))
        handler.send_header("X-Content-Type-Options", "nosniff")
        handler.send_header("Referrer-Policy", "no-referrer")
        if extra:
            for key, value in extra:
                handler.send_header(key, value)
        handler.end_headers()
        handler.wfile.write(data)

    def _posted_ints(self, form, name):
        """General Purpose: Posted ids. A blank value is skipped."""
        found = []
        for item in form.get(name, []) or []:
            if item is None or str(item).strip() == "":
                continue
            found.append(int(item))
        return found

    def _role_listed(self, user, role_id):
        """General Purpose: Whether role_list includes this id."""
        for row in self.access.role_list(user):
            if int(row["role_id"]) == int(role_id):
                return True
        return False

    def _export_users(self, handler, user):
        """General Purpose: The filtered account list as a csv download.

        requirement-html-user-management — the Export button.
        requirement-rbac-users — system:user:export.
        """
        query = getattr(self._request, "query", None) or {}
        picked = self._user_query(query)
        text = self.access.user_export(user, picked["access"])
        self._send_bytes(
            handler,
            200,
            text.encode("utf-8"),
            "text/csv; charset=utf-8",
            extra=(("Content-Disposition", 'attachment; filename="users.csv"'),),
        )

    def _export_roles(self, handler, user):
        """General Purpose: The filtered role list as a csv download.

        requirement-html-role-management — the Export button.
        requirement-rbac-roles — system:role:export.
        """
        query = getattr(self._request, "query", None) or {}
        picked = self._role_query(query)
        text = self.access.role_export(user, picked["access"])
        self._send_bytes(
            handler,
            200,
            text.encode("utf-8"),
            "text/csv; charset=utf-8",
            extra=(("Content-Disposition", 'attachment; filename="roles.csv"'),),
        )

    def _theme_css(self, path):
        """General Purpose: One theme sheet under /themes/, or an empty string.

        requirement-html-theme — the color sheet is a file on this host.
        """
        prefix = "/themes/"
        if not path.startswith(prefix) or not path.endswith(".css"):
            return ""
        name = path[len(prefix):]
        if "/" in name or "\\" in name or ".." in name:
            return ""
        stem = name[:-4]
        if stem not in Settings.THEMES:
            return ""
        return "themes/" + name

    def _icon_file(self, path):
        """General Purpose: One users icon under /icons/, or an empty string.

        requirement-html-user-management — the icon is a file on this host.
        requirement-web-interface — a separate file unless a requirement
        specifies an inline image.
        """
        prefix = "/icons/"
        if not path.startswith(prefix) or not path.endswith(".svg"):
            return ""
        name = path[len(prefix):]
        if len(name) < 5 or "/" in name or "\\" in name or ".." in name:
            return ""
        stem = name[:-4]
        for ch in stem:
            if not (ch.islower() or ch.isdigit() or ch == "-"):
                return ""
        return "icons/" + name

    def _send_static(self, handler, name, content_type):
        """General Purpose: A same-origin file from the Element Plus directory."""
        path = self.VENDOR / name
        if not path.is_file():
            self._send_bytes(handler, 404, b"Not found\n", "text/plain; charset=utf-8")
            return
        self._send_bytes(handler, 200, path.read_bytes(), content_type)

    def _redirect(self, handler, location, cookie=None, clear=False):
        handler.send_response(303)
        handler.send_header("Location", location)
        handler.send_header("Content-Length", "0")
        if cookie is not None:
            handler.send_header(
                "Set-Cookie",
                "{0}={1}; HttpOnly; SameSite=Lax; Path=/".format(self.COOKIE, cookie),
            )
        if clear:
            handler.send_header(
                "Set-Cookie",
                "{0}=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0".format(self.COOKIE),
            )
        handler.end_headers()

    def _nav(self, user):
        """General Purpose: Sidebar groups the account is allowed to open."""
        groups = (
            ("Home", (("/", "Home", None),)),
            ("Access", (
                ("/users", "Users", "system:user:list"),
                ("/roles", "Roles", "system:role:list"),
                ("/menus", "Menus", "system:menu:list"),
                ("/depts", "Departments", "system:dept:list"),
                ("/job-titles", "Job Titles", "system:jobtitle:list"),
            )),
            ("Catalog", (
                ("/configs", "Parameters", "system:config:list"),
                ("/dicts", "Dictionaries", "system:dict:list"),
                ("/notices", "Notices", "system:notice:list"),
            )),
            ("Audit", (
                ("/oper-log", "Operation log", "monitor:operlog:list"),
                ("/login-log", "Login log", "monitor:logininfor:list"),
                ("/online", "Online", "monitor:online:list"),
            )),
            ("Setup", (
                ("/database", "Database", "system:config:edit"),
            )),
        )
        visible_groups = []
        for label, items in groups:
            visible = []
            for href, text, perm in items:
                if perm is None or self.access.allows(user["user_id"], perm):
                    visible.append({"href": href, "label": text})
            if visible:
                visible_groups.append({"label": label, "items": visible})
        return visible_groups

    def _clean_path(self, path) -> str:
        """General Purpose: Request path without a trailing slash, except root.

        requirement-html-javascript — the menu highlight reads this path.
        requirement-web-interface — the shell sidebar uses it.
        """
        text = path or "/"
        if text != "/" and text.endswith("/"):
            text = text[:-1]
        return text or "/"

    def _current_path(self) -> str:
        """General Purpose: Path of the request on this thread."""
        text = getattr(self._request, "path", "") or ""
        return text or "/"

    def _frame(self, user, error, title) -> dict:
        """General Purpose: Names shared by every signed-in page."""
        return {
            "title": title,
            "error": error or "",
            "message": "",
            "detail": "",
            "signed_in": True,
            "user_name": user.get("user_name") or "",
            "csrf": user.get("csrf") or "",
            "nav_groups": self._nav(user),
            "path": self._current_path(),
            "theme": self.settings.theme(),
        }

    def _document(self, template, values) -> str:
        """General Purpose: The HTML document for one page template."""
        return self.templates.render_document(template, values)

    def _message(self, user, title, message, detail="") -> str:
        """General Purpose: An error or notice page, inside the shell when signed in."""
        if user is None:
            values = {
                "title": title,
                "error": "",
                "message": message,
                "detail": detail or "",
                "signed_in": False,
                "user_name": "",
                "csrf": "",
                "nav_groups": [],
                "path": self._current_path(),
                "theme": self.settings.theme(),
            }
        else:
            values = self._frame(user, "", title)
            values["message"] = message
            values["detail"] = detail or ""
        return self._document("message", values)

    def _engine_values(self) -> dict:
        """General Purpose: sqlite3, including the default file, and mysql."""
        path = self.settings.sqlite_path()
        mark = " (default file)" if self.settings.get("OPENRBAC_SQLITE_FILE") == "" else ""
        return {
            "engine": self.settings.engine(),
            "sqlite_label": "sqlite3 {0}{1}".format(path, mark),
            "mysql_label": "mysql {0}".format(self.settings.get("OPENRBAC_DB_NAME")),
            "sentence": self.settings.engine_sentence(),
        }

    def _list(self, user, error, title, template, rows, extra=None) -> str:
        """General Purpose: A list page value dictionary plus any dialog flags."""
        values = self._frame(user, error, title)
        values["rows"] = rows
        values["total"] = len(rows)
        if extra:
            values.update(extra)
        return self._document(template, values)

    def login_page(self, error) -> str:
        """General Purpose: The sign-in page, with sqlite3 and mysql and no captcha."""
        values = self._engine_values()
        values["title"] = "Sign in"
        values["error"] = error or ""
        values["signed_in"] = False
        values["theme"] = self.settings.theme()
        return self._document("login", values)

    def database_page(self, user, error) -> str:
        """General Purpose: The engine choice for an account that may edit parameters."""
        values = self._frame(user, error, "Database")
        values.update(self._engine_values())
        return self._document("database", values)

    def home_page(self, user, error) -> str:
        """General Purpose: The signed-in name from Access.describe."""
        values = self._frame(user, error, "Home")
        values["who"] = self.access.describe(user)
        return self._document("home", values)

    def users_page(self, user, error) -> str:
        """General Purpose: Organization tree, search, and the account table.

        requirement-html-user-management — the users list layout.
        requirement-rbac-users — list filters and the permission flags.
        """
        query = getattr(self._request, "query", None) or {}
        picked = self._user_query(query)
        can_add = self.access.allows(user["user_id"], "system:user:add")
        can_edit = self.access.allows(user["user_id"], "system:user:edit")
        can_reset = self.access.allows(user["user_id"], "system:user:resetPwd")
        can_remove = self.access.allows(user["user_id"], "system:user:remove")
        can_import = self.access.allows(user["user_id"], "system:user:import")
        can_export = self.access.allows(user["user_id"], "system:user:export")
        rows = [
            self._user_record(row, picked["keep"], can_edit)
            for row in self.access.user_list(user, picked["access"])
        ]
        department_rows = self.access.user_departments(user)
        form = picked["form"]
        target = None
        if form in ("edit", "reset", "remove") and picked["user_id"] is not None:
            for row in self.access.user_list(user):
                if int(row["user_id"]) == picked["user_id"]:
                    target = row
                    break
        if form in ("edit", "remove") and not error:
            if picked["user_id"] is None:
                error = "Choose an account."
            elif target is None:
                error = "That account is not in this list."
        editing = target if form == "edit" and can_edit else None
        values = {
            "limit": 200,
            "departments": self._user_tree(
                department_rows,
                picked["dept_id"],
                picked["keep"],
            ),
            "can_depts": self.access.allows(user["user_id"], "system:dept:list"),
            "query_user_name": picked["query_user_name"],
            "query_phone": picked["query_phone"],
            "query_state": picked["state"],
            "query_begin": picked["query_begin"],
            "query_end": picked["query_end"],
            "query_dept": picked["query_dept"],
            "state_all": picked["state"] == "",
            "state_on": picked["state"] == "0",
            "state_off": picked["state"] == "1",
            "state_all_href": self._users_href(picked["keep"], state=""),
            "state_on_href": self._users_href(picked["keep"], state="0"),
            "state_off_href": self._users_href(picked["keep"], state="1"),
            "note": picked["note"],
            "can_add": can_add,
            "can_edit": can_edit,
            "can_reset": can_reset,
            "can_remove": can_remove,
            "can_import": can_import,
            "can_export": can_export,
            "can_choose": can_edit or can_remove,
            "add_href": self._users_href(picked["keep"], form="add"),
            "import_href": self._users_href(picked["keep"], form="import"),
            "export_href": self._users_href(picked["keep"], path="/users/export"),
            "show_add": form == "add" and can_add,
            "show_edit": form == "edit" and can_edit and target is not None,
            "show_reset": form == "reset" and can_reset and target is not None,
            "show_remove": form == "remove" and can_remove and target is not None,
            "show_import": form == "import" and can_import,
            "edit_user_id": "" if target is None else str(target["user_id"]),
            "reset_user_id": "" if target is None else str(target["user_id"]),
            "remove_user_id": "" if target is None else str(target["user_id"]),
            "remove_name": "" if target is None else (target.get("user_name") or ""),
        }
        values.update(self._edit_context(user, editing, query, picked["keep"], department_rows))
        return self._list(user, error, "Users", "users", rows, values)

    def test_page(self, user, error) -> str:
        """General Purpose: The users table alone, for checking the AdminLTE skin."""
        can_edit = self.access.allows(user["user_id"], "system:user:edit")
        can_reset = self.access.allows(user["user_id"], "system:user:resetPwd")
        can_remove = self.access.allows(user["user_id"], "system:user:remove")
        rows = [
            self._user_record(row, {}, can_edit)
            for row in self.access.user_list(user)
        ]
        return self._list(user, error, "Users", "test", rows, {
            "can_choose": can_edit or can_remove,
            "can_edit": can_edit,
            "can_reset": can_reset,
            "can_remove": can_remove,
        })

    def _edit_context(self, user, target, query, keep, departments):
        """General Purpose: Edit dialog fields. A query key replaces the stored value.

        requirement-html-user-management — section 6. Login name is not the search field.
        """
        blank = {
            "edit_nick": "",
            "edit_phone": "",
            "edit_email": "",
            "edit_login": "",
            "edit_remark": "",
            "edit_dept_name": "",
            "edit_status": "0",
            "edit_close_href": self._users_href(keep),
            "dept_q": "",
            "picker_dept": False,
            "dept_cleared": False,
            "sex_male": False,
            "sex_female": False,
            "sex_unknown": True,
            "job_titles": [],
            "edit_roles": [],
            "edit_departments": [],
        }
        if target is None:
            return blank
        record = self.access.user_by_id(target["user_id"]) or target
        nick = self._override(query, "nick_name", record.get("nick_name") or "")
        phone = self._override(query, "phonenumber", record.get("phonenumber") or "")
        email = self._override(query, "email", record.get("email") or "")
        remark = self._override(query, "remark", record.get("remark") or "")
        status = str(record.get("status") or "0")
        if "status" in query:
            posted = self._first(query, "status").strip()
            if posted in ("0", "1"):
                status = posted
        sex = str(record.get("sex") or "2").strip() or "2"
        if "sex" in query:
            posted_sex = self._first(query, "sex").strip()
            if posted_sex:
                sex = posted_sex
        selected = self._dept_number(record.get("dept_id"))
        cleared = False
        if "dept_id" in query:
            selected = self._dept_number(self._first(query, "dept_id"))
            cleared = selected is None
        dept_name = ""
        if selected is not None:
            for row in departments or []:
                if self._dept_number(row.get("dept_id")) == selected:
                    dept_name = row.get("dept_name") or ""
                    break
            if dept_name == "":
                dept_name = record.get("dept_name") or target.get("dept_name") or ""
        title_ids = self._chosen_ids(query, "job_title_id", self.access.user_job_title_ids(target["user_id"]))
        role_ids = self._chosen_ids(query, "role_id", self.access.user_role_ids(target["user_id"]))
        account_id = int(target["user_id"])
        titles = []
        for row in self.access.edit_job_titles(user):
            number = int(row["job_title_id"])
            titles.append({
                "job_title_id": str(number),
                "job_title": row.get("job_title") or "",
                "checked": number in title_ids,
            })
        roles = []
        for row in self.access.edit_roles(user):
            number = int(row["role_id"])
            locked = account_id == 1 and number == 1
            roles.append({
                "role_id": str(number),
                "role_name": row.get("role_name") or "",
                "checked": locked or number in role_ids,
                "locked": locked,
            })
        return {
            "edit_nick": nick,
            "edit_phone": phone,
            "edit_email": email,
            "edit_login": record.get("user_name") or "",
            "edit_remark": remark,
            "edit_dept_name": dept_name,
            "edit_status": status,
            "edit_close_href": self._users_href(keep),
            "dept_q": self._first(query, "dept_q").strip(),
            "picker_dept": self._first(query, "picker").strip() == "dept",
            "dept_cleared": cleared,
            "sex_male": sex == "0",
            "sex_female": sex == "1",
            "sex_unknown": sex == "2",
            "job_titles": titles,
            "edit_roles": roles,
            "edit_departments": self._user_tree(
                departments,
                selected,
                keep,
                keyword=self._first(query, "dept_q").strip(),
            ),
        }

    def _override(self, query, key, stored):
        if key not in query:
            return "" if stored is None else str(stored)
        return self._first(query, key)

    def _chosen_ids(self, query, key, stored):
        if key not in query:
            return {int(item) for item in stored}
        return set(self._number_list(query.get(key)))

    def _user_query(self, query):
        """General Purpose: Search fields from the users page query string.

        requirement-html-user-management — login name, phone, status, dates, and dept.
        """
        user_name = self._first(query, "user_name").strip()
        phone = self._first(query, "phone").strip()
        state = self._first(query, "state").strip()
        if state not in ("", "0", "1"):
            state = ""
        begin = self._first(query, "begin").strip()
        end = self._first(query, "end").strip()
        dept = self._first(query, "dept").strip()
        dept_id = int(dept) if dept.isdigit() and int(dept) > 0 else None
        if dept_id is None:
            dept = ""
        form = self._first(query, "form").strip()
        if form not in ("add", "edit", "reset", "remove", "import"):
            form = ""
        note = self._first(query, "note").strip()
        raw_id = self._first(query, "user_id").strip()
        user_id = int(raw_id) if raw_id.isdigit() else None
        access = {}
        if user_name:
            access["user_name"] = user_name
        if phone:
            access["phonenumber"] = phone
        if state in ("0", "1"):
            access["status"] = state
        if dept_id is not None:
            access["dept_id"] = dept_id
        if begin:
            access["begin_time"] = begin
        if end:
            access["end_time"] = end
        return {
            "access": access,
            "keep": {
                "user_name": user_name,
                "phone": phone,
                "state": state,
                "begin": begin,
                "end": end,
                "dept": dept,
            },
            "form": form,
            "user_id": user_id,
            "dept_id": dept_id,
            "state": state,
            "query_user_name": user_name,
            "query_phone": phone,
            "query_begin": begin,
            "query_end": end,
            "query_dept": dept,
            "note": note,
        }

    def _users_href(self, keep, path="/users", **extra):
        """General Purpose: /users with the search fields and any override."""
        values = dict(keep or {})
        values.update(extra)
        params = []
        for key in ("user_name", "phone", "state", "begin", "end", "dept", "form", "user_id"):
            raw = values.get(key)
            if raw is None:
                continue
            text = str(raw).strip()
            if text == "":
                continue
            params.append((key, text))
        if not params:
            return path
        return path + "?" + urlencode(params)

    def _user_tree(self, departments, selected, keep, keyword=""):
        """General Purpose: Nested departments. A parent holds its children.

        A keyword keeps a match, its ancestors, and the chosen department.
        """
        rows = list(departments or [])
        chosen = self._dept_number(selected)
        needle = (keyword or "").strip().lower()
        if needle:
            by_id = {}
            for row in rows:
                number = self._dept_number(row.get("dept_id"))
                if number is not None:
                    by_id[number] = row
            keep_ids = set()
            for number, row in by_id.items():
                if needle in str(row.get("dept_name") or "").lower():
                    self._dept_family(number, by_id, keep_ids)
            if chosen is not None:
                self._dept_family(chosen, by_id, keep_ids)
            rows = [
                row for row in rows
                if self._dept_number(row.get("dept_id")) in keep_ids
            ]
        ids = set()
        for row in rows:
            try:
                ids.add(int(row["dept_id"]))
            except (TypeError, ValueError, KeyError):
                continue
        by_parent = {}
        for row in rows:
            try:
                dept_id = int(row["dept_id"])
            except (TypeError, ValueError, KeyError):
                continue
            try:
                parent_id = int(row.get("parent_id") or 0)
            except (TypeError, ValueError):
                parent_id = 0
            if parent_id not in ids:
                parent_id = 0
            by_parent.setdefault(parent_id, []).append((dept_id, row))
        seen = set()

        def walk(parent_id, depth):
            children = by_parent.get(parent_id, [])
            built = []
            last_index = len(children) - 1
            for index, (dept_id, row) in enumerate(children):
                if dept_id in seen:
                    continue
                seen.add(dept_id)
                kids = walk(dept_id, depth + 1)
                kind = "user-node-branch" if kids else "user-node-leaf"
                flags = []
                if index == 0:
                    flags.append("is-first")
                if index == last_index:
                    flags.append("is-last")
                if depth == 0 and index == 0 and index == last_index:
                    flags.append("is-root")
                mark = (" " + " ".join(flags)) if flags else ""
                built.append({
                    "dept_name": row.get("dept_name") or "",
                    "dept_id": str(dept_id),
                    "checked": chosen == dept_id,
                    "href": self._users_href(keep, dept=str(dept_id)),
                    "depth_class": "user-depth-{0} {1}{2}".format(min(depth, 6), kind, mark),
                    "link_class": "user-tree-link is-current" if chosen == dept_id else "user-tree-link",
                    "children": kids,
                })
            return built

        return walk(0, 0)

    def _dept_family(self, dept_id, by_id, found):
        """Keep this department, the ancestors column, and the parent chain."""
        if dept_id in found or dept_id not in by_id:
            return
        found.add(dept_id)
        row = by_id[dept_id]
        for piece in str(row.get("ancestors") or "").split(","):
            piece = piece.strip()
            if piece.isdigit() and int(piece) > 0:
                found.add(int(piece))
        parent = self._dept_number(row.get("parent_id"))
        if parent is not None:
            self._dept_family(parent, by_id, found)

    def _user_initials(self, nick, login):
        """General Purpose: Two letters for the account mark on the users table."""
        source = (nick or "").strip() or (login or "").strip()
        parts = [piece for piece in source.split() if piece]
        if len(parts) >= 2:
            raw = parts[0][0] + parts[1][0]
        else:
            raw = source[:2]
        letters = "".join(ch for ch in raw if ch.isalnum()).upper()
        return letters or "?"

    def _user_record(self, row, keep, can_edit):
        """General Purpose: One table row. Status is an on/off switch."""
        status = str(row.get("status") or "0")
        user_id = row.get("user_id")
        created = row.get("create_time")
        text = "" if created is None else str(created)
        return {
            "user_id": user_id,
            "user_name": row.get("user_name") or "",
            "nick_name": row.get("nick_name") or "",
            "initials": self._user_initials(row.get("nick_name"), row.get("user_name")),
            "dept_name": row.get("dept_name") or "",
            "phone": row.get("phonenumber") or "",
            "status": status,
            "status_label": "Disabled" if status == "1" else "Enabled",
            "status_next": "0" if status == "1" else "1",
            "status_form": "user-status-{0}".format(user_id),
            "status_post": bool(can_edit) and str(user_id) != "1",
            "created": text[:19],
            "edit_href": self._users_href(keep, form="edit", user_id=user_id),
            "remove_href": self._users_href(keep, form="remove", user_id=user_id),
            "reset_href": self._users_href(keep, form="reset", user_id=user_id),
        }

    def roles_page(self, user, error) -> str:
        """General Purpose: Search, toolbar, and the role table.

        requirement-html-role-management — the roles list layout.
        requirement-rbac-roles — list filters and the permission flags.
        """
        query = getattr(self._request, "query", None) or {}
        picked = self._role_query(query)
        can_add = self.access.allows(user["user_id"], "system:role:add")
        can_edit = self.access.allows(user["user_id"], "system:role:edit")
        can_remove = self.access.allows(user["user_id"], "system:role:remove")
        can_export = self.access.allows(user["user_id"], "system:role:export")
        rows = [
            self._role_record(row, picked["keep"], can_edit, can_remove)
            for row in self.access.role_list(user, picked["access"])
        ]
        form = picked["form"]
        target = None
        if form in ("edit", "remove", "scope") and picked["role_id"] is not None:
            for row in self.access.role_list(user):
                if int(row["role_id"]) == picked["role_id"]:
                    target = row
                    break
        protected = (
            target is not None
            and int(target["role_id"]) == self.access.PROTECTED_ROLE
        )
        if form in ("edit", "remove", "scope") and not error:
            if picked["role_id"] is None:
                error = "Choose a role."
            elif target is None:
                error = "That role is not in this list."
            elif protected:
                error = "The built-in administrator role is not edited here."
        open_target = target is not None and not protected
        show_add = form == "add" and can_add
        show_edit = form == "edit" and can_edit and open_target
        show_remove = form == "remove" and can_remove and open_target
        show_scope = form == "scope" and can_edit and open_target
        menus = []
        if show_add or show_edit:
            role_id = None if target is None else target["role_id"]
            menus = self._role_menu_choices(role_id)
        scope_menus = []
        scope_dept = ""
        scope_value = "1"
        if target is not None:
            scope_value = str(target.get("data_scope") or "1")
        if scope_value not in self.ROLE_SCOPES:
            scope_value = "1"
        if show_scope:
            scope_menus = self._role_scope_menus(target["role_id"])
            if scope_value == "2":
                scope_dept = self._role_scope_dept(target["role_id"])
        total = len(rows)
        if total == 0:
            count_line = "Showing 0 to 0 of 0 records"
        else:
            count_line = "Showing 1 to {0} of {0} records".format(total)
        status = "0" if target is None else str(target.get("status") or "0")
        blank = ""
        return self._list(user, error, "Roles", "roles", rows, {
            "count_line": count_line,
            "query_role_name": picked["query_role_name"],
            "query_role_key": picked["query_role_key"],
            "query_state": picked["state"],
            "query_begin": picked["query_begin"],
            "query_end": picked["query_end"],
            "state_all": picked["state"] == "",
            "state_on": picked["state"] == "0",
            "state_off": picked["state"] == "1",
            "can_add": can_add,
            "can_edit": can_edit,
            "can_remove": can_remove,
            "can_export": can_export,
            "can_choose": can_edit or can_remove,
            "add_href": self._roles_href(picked["keep"], form="add"),
            "export_href": self._roles_href(picked["keep"], path="/roles/export"),
            "show_add": show_add,
            "show_edit": show_edit,
            "show_remove": show_remove,
            "show_scope": show_scope,
            "menus": menus,
            "scope_menus": scope_menus,
            "scope_1": scope_value == "1",
            "scope_2": scope_value == "2",
            "scope_3": scope_value == "3",
            "scope_4": scope_value == "4",
            "edit_role_id": blank if not open_target else str(target["role_id"]),
            "edit_name": blank if target is None else (target.get("role_name") or ""),
            "edit_key": blank if target is None else (target.get("role_key") or ""),
            "edit_sort": blank if target is None else str(target.get("role_sort") if target.get("role_sort") is not None else ""),
            "edit_status": status,
            "edit_remark": blank if target is None else (target.get("remark") or ""),
            "remove_role_id": blank if not open_target else str(target["role_id"]),
            "remove_name": blank if target is None else (target.get("role_name") or ""),
            "scope_role_id": blank if not open_target else str(target["role_id"]),
            "scope_name": blank if target is None else (target.get("role_name") or ""),
            "scope_key": blank if target is None else (target.get("role_key") or ""),
            "scope_dept": scope_dept,
        })

    def _role_query(self, query):
        """General Purpose: Search fields from the roles page query string.

        requirement-html-role-management — role name, permission key, status, and dates.
        """
        role_name = self._first(query, "role_name").strip()
        role_key = self._first(query, "role_key").strip()
        state = self._first(query, "state").strip()
        if state not in ("", "0", "1"):
            state = ""
        begin = self._first(query, "begin").strip()
        end = self._first(query, "end").strip()
        form = self._first(query, "form").strip()
        if form not in ("add", "edit", "remove", "scope"):
            form = ""
        raw_id = self._first(query, "role_id").strip()
        role_id = int(raw_id) if raw_id.isdigit() else None
        access = {}
        if role_name:
            access["role_name"] = role_name
        if role_key:
            access["role_key"] = role_key
        if state in ("0", "1"):
            access["status"] = state
        if begin:
            access["begin_time"] = begin
        if end:
            access["end_time"] = end
        return {
            "access": access,
            "keep": {
                "role_name": role_name,
                "role_key": role_key,
                "state": state,
                "begin": begin,
                "end": end,
            },
            "form": form,
            "role_id": role_id,
            "state": state,
            "query_role_name": role_name,
            "query_role_key": role_key,
            "query_begin": begin,
            "query_end": end,
        }

    def _roles_href(self, keep, path="/roles", **extra):
        """General Purpose: /roles with the search fields and any override."""
        values = dict(keep or {})
        values.update(extra)
        params = []
        for key in ("role_name", "role_key", "state", "begin", "end", "form", "role_id"):
            raw = values.get(key)
            if raw is None:
                continue
            text = str(raw).strip()
            if text == "":
                continue
            params.append((key, text))
        if not params:
            return path
        return path + "?" + urlencode(params)

    def _role_record(self, row, keep, can_edit, can_remove):
        """General Purpose: One role row. Status is an on/off switch."""
        status = str(row.get("status") or "0")
        role_id = row.get("role_id")
        protected = int(role_id) == self.access.PROTECTED_ROLE
        scope = str(row.get("data_scope") or "")
        label, kind = self.ROLE_SCOPES.get(scope, (scope, ""))
        created = row.get("create_time")
        text = "" if created is None else str(created)
        editable = bool(can_edit) and not protected
        removable = bool(can_remove) and not protected
        return {
            "role_id": role_id,
            "role_name": row.get("role_name") or "",
            "role_key": row.get("role_key") or "",
            "role_sort": "" if row.get("role_sort") is None else row.get("role_sort"),
            "scope_label": label,
            "scope_type": kind,
            "status": status,
            "status_label": "Disabled" if status == "1" else "Enabled",
            "status_next": "0" if status == "1" else "1",
            "status_form": "role-status-{0}".format(role_id),
            "status_post": editable,
            "created": text[:19],
            "edit_action": editable,
            "remove_action": removable,
            "scope_action": editable,
            "edit_href": self._roles_href(keep, form="edit", role_id=role_id),
            "remove_href": self._roles_href(keep, form="remove", role_id=role_id),
            "scope_href": self._roles_href(keep, form="scope", role_id=role_id),
        }

    def _role_menu_choices(self, role_id):
        """General Purpose: Every menu. A menu the role already has starts checked."""
        linked = set()
        if role_id is not None:
            found = self.access.store.query_all(
                "SELECT menu_id FROM sys_role_menu WHERE role_id = %s",
                (role_id,),
            )
            for row in found:
                linked.add(int(row["menu_id"]))
        choices = []
        for row in self._menus_unscoped():
            menu_id = int(row["menu_id"])
            choices.append({
                "menu_id": menu_id,
                "menu_name": row.get("menu_name") or "",
                "perms": row.get("perms") or "",
                "checked": menu_id in linked,
            })
        return choices

    def _role_scope_menus(self, role_id):
        """General Purpose: Menu ids the grant form posts again so links stay."""
        return self.access.store.query_all(
            """
            SELECT m.menu_id
            FROM sys_role_menu rm
            JOIN sys_menu m ON m.menu_id = rm.menu_id
            WHERE rm.role_id = %s
            ORDER BY m.parent_id, m.order_num, m.menu_id
            """,
            (role_id,),
        )

    def _role_scope_dept(self, role_id):
        """General Purpose: The first custom department for one role."""
        row = self.access.store.query_one(
            """
            SELECT dept_id FROM sys_role_dept
            WHERE role_id = %s
            ORDER BY dept_id
            """,
            (role_id,),
        )
        if row is None or row.get("dept_id") is None:
            return ""
        return str(row["dept_id"])

    def _menus_unscoped(self):
        """Menu ids for the grant form when the actor may edit roles but not list menus.

        The grant still rejects unknown ids. The form needs the seeded ids.
        """
        return self.access.store.query_all(
            """
            SELECT menu_id, menu_name, perms FROM sys_menu
            WHERE status = '0' ORDER BY parent_id, order_num, menu_id
            """
        )

    def menus_page(self, user, error) -> str:
        """General Purpose: The menu tree, search, and the add, edit, and remove dialogs.

        requirement-rbac-menu — list, add, and the page actions edit, remove, and save sort.
        The tree opens contracted. Disabled rows stay off the list.
        """
        query = getattr(self._request, "query", None) or {}
        picked = self._menu_query(query)
        raw = self.access.menu_list(user)
        can_add = self.access.allows(user["user_id"], "system:menu:add")
        can_edit = self.access.allows(user["user_id"], "system:menu:edit")
        can_remove = self.access.allows(user["user_id"], "system:menu:remove")
        built = self._menu_table(raw, picked)
        known = set()
        for row in raw or []:
            try:
                known.add(str(int(row["menu_id"])))
            except (TypeError, ValueError, KeyError):
                continue
        parent_id = picked["parent_id"] if picked["parent_id"] in known else "0"
        target = None
        if picked["form"] in ("edit", "remove") and picked["menu_id"]:
            for row in raw or []:
                try:
                    if str(int(row["menu_id"])) == picked["menu_id"]:
                        target = row
                        break
                except (TypeError, ValueError, KeyError):
                    continue
        if picked["form"] in ("edit", "remove") and not error:
            if picked["menu_id"] == "":
                error = "Choose a menu."
            elif target is None:
                error = "That menu is not in this list."
        blank = target is None
        return self._list(user, error, "Menus", "menus", built["rows"], {
            "parents": list(raw or []),
            "can_add": can_add,
            "can_edit": can_edit,
            "can_remove": can_remove,
            "can_choose": can_edit,
            "can_act": can_add or can_edit or can_remove,
            "show_add": picked["form"] == "add" and can_add,
            "show_edit": picked["form"] == "edit" and can_edit and target is not None,
            "show_remove": picked["form"] == "remove" and can_remove and target is not None,
            "parent_id": parent_id,
            "query_menu_name": picked["menu_name"],
            "query_state": picked["state"],
            "query_closed": built["query_closed"],
            "has_closed": built["has_closed"],
            "state_all": picked["state"] == "",
            "state_show": picked["state"] == "0",
            "state_hide": picked["state"] == "1",
            "add_href": built["add_href"],
            "fold_href": built["fold_href"],
            "edit_menu_id": "" if blank else str(int(target["menu_id"])),
            "edit_name": "" if blank else (target.get("menu_name") or ""),
            "edit_parent": "0" if blank else str(int(target.get("parent_id") or 0)),
            "edit_type": "" if blank else str(target.get("menu_type") or ""),
            "edit_perms": "" if blank else (target.get("perms") or ""),
            "edit_path": "" if blank else (target.get("path") or ""),
            "edit_visible": "0" if blank else str(target.get("visible") or "0"),
            "remove_menu_id": "" if blank else str(int(target["menu_id"])),
            "remove_name": "" if blank else (target.get("menu_name") or ""),
        })

    def _menu_query(self, query):
        """General Purpose: Menu name, visibility, and which branches are closed."""
        menu_name = self._first(query, "menu_name").strip()
        state = self._first(query, "state").strip()
        if state not in ("", "0", "1"):
            state = ""
        closed = []
        seen = set()
        # A missing closed value is the contracted start. closed=open is every
        # branch open. A list of ids contracts those branches only.
        if "closed" not in query:
            closed_mode = "default"
        else:
            raw_closed = self._first(query, "closed").strip()
            for part in raw_closed.split(","):
                part = part.strip()
                if part.isdigit() and part not in seen:
                    seen.add(part)
                    closed.append(part)
            if raw_closed == "open" or not closed:
                closed_mode = "open"
            else:
                closed_mode = "list"
        form = self._first(query, "form").strip()
        if form not in ("add", "edit", "remove"):
            form = ""
        parent = self._first(query, "parent_id").strip()
        parent_id = parent if parent.isdigit() else "0"
        raw_id = self._first(query, "menu_id").strip()
        menu_id = str(int(raw_id)) if raw_id.isdigit() else ""
        return {
            "menu_name": menu_name,
            "state": state,
            "closed": closed,
            "closed_mode": closed_mode,
            "form": form,
            "parent_id": parent_id,
            "menu_id": menu_id,
        }

    def _menu_href(self, picked, **extra):
        """General Purpose: /menus with the search, the closed branches, and any override."""
        closed = picked.get("closed") or []
        if not isinstance(closed, str):
            closed = ",".join(closed)
        values = {
            "menu_name": picked.get("menu_name") or "",
            "state": picked.get("state") or "",
            "closed": closed,
        }
        values.update(extra)
        params = []
        for key in ("menu_name", "state", "closed", "form", "parent_id", "menu_id"):
            if key not in values:
                continue
            text = str(values.get(key) or "").strip()
            if text == "" or (key == "parent_id" and text == "0"):
                continue
            params.append((key, text))
        if not params:
            return "/menus"
        return "/menus?" + urlencode(params)

    def _menu_back(self, form):
        """General Purpose: /menus with the search the form carried back."""
        return self._menu_href({
            "menu_name": self._first(form, "keep_name"),
            "state": self._first(form, "keep_state"),
            "closed": self._first(form, "keep_closed"),
        })

    def _menu_table(self, raw, picked):
        """General Purpose: Flat tree rows. The page starts contracted.

        A missing closed value hides every child. closed=open shows every kept
        row. A list of ids hides those branches. A name or visibility filter
        with no closed value still shows the match and its ancestors.
        """
        nodes = {}
        order = []
        for row in raw or []:
            if not isinstance(row, dict):
                continue
            try:
                menu_id = int(row["menu_id"])
            except (TypeError, ValueError, KeyError):
                continue
            try:
                parent_id = int(row.get("parent_id") or 0)
            except (TypeError, ValueError):
                parent_id = 0
            try:
                sort_key = int(row.get("order_num") or 0)
            except (TypeError, ValueError):
                sort_key = 0
            nodes[menu_id] = {
                "menu_id": menu_id,
                "parent_id": parent_id,
                "menu_name": row.get("menu_name") or "",
                "menu_type": str(row.get("menu_type") or ""),
                "perms": row.get("perms") or "",
                "sort_key": sort_key,
                "path": row.get("path") or "",
                "visible": str(row.get("visible") or "0"),
                "kids": [],
            }
            order.append(menu_id)
        children_of = {0: []}
        for menu_id in order:
            item = nodes[menu_id]
            parent_id = item["parent_id"]
            if parent_id == menu_id or parent_id not in nodes:
                parent_id = 0
            children_of.setdefault(parent_id, []).append(item)
        for kids in children_of.values():
            kids.sort(key=lambda item: (item["sort_key"], item["menu_id"]))
        name_q = (picked.get("menu_name") or "").casefold()
        state = picked.get("state") or ""
        seen = set()

        def hit(item):
            name_ok = name_q == "" or name_q in item["menu_name"].casefold()
            visible_ok = state == "" or item["visible"] == state
            return name_ok and visible_ok

        def attach_all(item):
            kept_kids = []
            for child in children_of.get(item["menu_id"], []):
                if child["menu_id"] in seen:
                    continue
                seen.add(child["menu_id"])
                kept_kids.append(child)
                attach_all(child)
            item["kids"] = kept_kids

        def prepare(item):
            ident = item["menu_id"]
            if ident in seen:
                item["kids"] = []
                return False
            seen.add(ident)
            kids = children_of.get(ident, [])
            if name_q == "" and state == "":
                item["kids"] = list(kids)
                for child in item["kids"]:
                    prepare(child)
                return True
            if hit(item) and name_q != "" and state == "":
                attach_all(item)
                return True
            kept_kids = []
            for child in kids:
                if prepare(child):
                    kept_kids.append(child)
            item["kids"] = kept_kids
            return hit(item) or bool(kept_kids)

        roots = []
        for item in children_of.get(0, []):
            if prepare(item):
                roots.append(item)
        all_branch_ids = []

        def collect_branches(item):
            kids = item.get("kids") or []
            if not kids:
                return
            all_branch_ids.append(str(item["menu_id"]))
            for child in kids:
                collect_branches(child)

        for item in roots:
            collect_branches(item)
        mode = picked.get("closed_mode") or "default"
        filtering = name_q != "" or state != ""
        if mode == "open" or (mode == "default" and filtering):
            closed = set()
        elif mode == "default":
            closed = set(all_branch_ids)
        else:
            closed = set(str(item) for item in (picked.get("closed") or []))
        rows = []

        def emit(item, depth):
            kids = item.get("kids") or []
            is_branch = bool(kids)
            ident = str(item["menu_id"])
            shut = is_branch and ident in closed
            rows.append(self._menu_record(item, depth, is_branch, shut))
            if is_branch and not shut:
                for child in kids:
                    emit(child, depth + 1)

        for item in roots:
            emit(item, 0)
        active_closed = [item for item in all_branch_ids if item in closed]
        everything_shut = bool(all_branch_ids) and len(active_closed) == len(all_branch_ids)
        if mode == "open":
            state_token = "open"
        elif mode == "list":
            state_token = ",".join(active_closed) if active_closed else "open"
        else:
            state_token = ""
        if not all_branch_ids:
            fold_token = state_token
        elif everything_shut:
            fold_token = "open"
        else:
            fold_token = ",".join(all_branch_ids)
        kept = dict(picked)
        kept["closed"] = state_token

        def closed_token(id_list):
            if not id_list:
                return "open"
            return ",".join(id_list)

        for row in rows:
            ident = row["menu_id"]
            if row["is_branch"]:
                if ident in closed:
                    nxt = [item for item in all_branch_ids if item in closed and item != ident]
                    row["twist_class"] = "menu-twist is-shut"
                else:
                    nxt = [item for item in all_branch_ids if item in closed or item == ident]
                    row["twist_class"] = "menu-twist is-open"
                row["toggle_href"] = self._menu_href(kept, closed=closed_token(nxt))
            else:
                row["twist_class"] = "menu-twist is-leaf"
                row["toggle_href"] = self._menu_href(kept)
            row["add_href"] = self._menu_href(
                kept, form="add", parent_id=ident,
            )
            row["edit_href"] = self._menu_href(kept, form="edit", menu_id=ident)
            row["remove_href"] = self._menu_href(kept, form="remove", menu_id=ident)
        return {
            "rows": rows,
            "query_closed": state_token,
            "has_closed": bool(state_token),
            "add_href": self._menu_href(kept, form="add"),
            "fold_href": self._menu_href(kept, closed=fold_token),
        }

    def _menu_record(self, item, depth, is_branch, shut):
        """General Purpose: One menu row. Type and visibility are display words."""
        kinds = {
            "M": ("Directory", "menu-tag menu-tag-dir", "menu-icon menu-icon-dir"),
            "C": ("Menu", "menu-tag menu-tag-menu", "menu-icon menu-icon-menu"),
            "F": ("Button", "menu-tag menu-tag-button", "menu-icon menu-icon-button"),
        }
        menu_type = item.get("menu_type") or ""
        kind = kinds.get(menu_type)
        if kind is None:
            type_label = menu_type or "Menu"
            type_class = "menu-tag"
            icon_class = "menu-icon"
        else:
            type_label, type_class, icon_class = kind
        if str(item.get("visible") or "0") == "1":
            visible_class = "menu-tag menu-tag-hide"
            visible_label = "Hide"
        else:
            visible_class = "menu-tag menu-tag-show"
            visible_label = "Show"
        perms = str(item.get("perms") or "").strip()
        path = str(item.get("path") or "").strip()
        depth_n = depth if depth < 8 else 8
        return {
            "menu_id": str(item["menu_id"]),
            "menu_name": item.get("menu_name") or "",
            "order_num": str(item.get("sort_key") or 0),
            "request_path": path if path else "#",
            "type_label": type_label,
            "type_class": type_class,
            "visible_label": visible_label,
            "visible_class": visible_class,
            "perms_label": perms if perms else "-",
            "name_class": "menu-name menu-depth-{0}".format(depth_n),
            "icon_class": icon_class,
            "is_branch": is_branch,
            "is_shut": shut,
        }

    def depts_page(self, user, error) -> str:
        """General Purpose: The department table and the add dialog."""
        rows = self.access.dept_list(user)
        return self._list(user, error, "Departments", "depts", rows, {
            "parents": rows,
            "can_add": self.access.allows(user["user_id"], "system:dept:add"),
        })

    def job_titles_page(self, user, error) -> str:
        """General Purpose: The job title table and the add dialog."""
        rows = self.access.job_title_list(user)
        return self._list(user, error, "Job Titles", "job-titles", rows, {
            "can_add": self.access.allows(user["user_id"], "system:jobtitle:add"),
        })

    def configs_page(self, user, error) -> str:
        """General Purpose: Search, the parameter table, and the change dialog.

        requirement-html-parameter-management — the list layout.
        requirement-rbac-parameters — list, change, and the permission flags.
        """
        query = getattr(self._request, "query", None) or {}
        picked = self._config_query(query)
        can_edit = self.access.allows(user["user_id"], "system:config:edit")
        all_rows = self.catalog.config_list(user)
        shown = self._config_filter(all_rows, picked)
        rows = [self._config_record(row, picked["keep"]) for row in shown]
        notice = error or ""
        show_edit = False
        edit_name = ""
        edit_key = ""
        edit_value = ""
        if can_edit and picked["form"] == "edit":
            if picked["config_id"] == "":
                notice = "Choose a parameter."
            else:
                target = self._config_by_id(all_rows, picked["config_id"])
                if target is None:
                    notice = "Unknown parameter"
                else:
                    show_edit = True
                    edit_name = target.get("config_name") or ""
                    edit_key = target.get("config_key") or ""
                    edit_value = target.get("config_value")
                    if edit_value is None:
                        edit_value = ""
        total = len(rows)
        if total == 0:
            count_line = "Showing 0 to 0 of 0 records"
        else:
            count_line = "Showing 1 to {0} of {0} records".format(total)
        values = self._frame(user, notice, "Parameters")
        values.update({
            "rows": rows,
            "total": total,
            "count_line": count_line,
            "can_edit": can_edit,
            "show_edit": show_edit,
            "edit_name": edit_name,
            "edit_key": edit_key,
            "edit_value": edit_value,
            "close_href": self._configs_href(picked["keep"]),
            "query_config_name": picked["config_name"],
            "query_config_key": picked["config_key"],
            "query_config_type": picked["config_type"],
            "query_begin": picked["begin"],
            "query_end": picked["end"],
            "type_all": picked["type_all"],
            "type_yes": picked["type_yes"],
            "type_no": picked["type_no"],
        })
        return self._document("configs", values)

    def _config_query(self, query):
        """General Purpose: Search fields and the edit id from the parameters page.

        requirement-html-parameter-management — config_id chooses the row.
        config_key stays the contains filter, so the two do not share a name.
        """
        config_name = self._first(query, "config_name").strip()
        config_key = self._first(query, "config_key").strip()
        config_type = self._first(query, "config_type").strip()
        if config_type not in ("Y", "N"):
            config_type = ""
        begin = self._first(query, "begin").strip()
        end = self._first(query, "end").strip()
        form = self._first(query, "form").strip()
        if form != "edit":
            form = ""
        return {
            "config_name": config_name,
            "config_key": config_key,
            "config_type": config_type,
            "begin": begin,
            "end": end,
            "form": form,
            "config_id": self._first(query, "config_id").strip(),
            "keep": {
                "config_name": config_name,
                "config_key": config_key,
                "config_type": config_type,
                "begin": begin,
                "end": end,
            },
            "type_all": config_type == "",
            "type_yes": config_type == "Y",
            "type_no": config_type == "N",
        }

    def _config_day(self, text) -> bool:
        """General Purpose: A created-date query is YYYY-MM-DD."""
        if len(text) != 10 or text[4] != "-" or text[7] != "-":
            return False
        year, month, day = text[:4], text[5:7], text[8:]
        return year.isdigit() and month.isdigit() and day.isdigit()

    def _config_stamp(self, value) -> str:
        """General Purpose: create_time as YYYY-MM-DD HH:MM:SS, or empty."""
        if value is None:
            return ""
        text = str(value).strip().replace("T", " ")
        if len(text) >= 19 and text[4] == "-" and text[7] == "-" and text[10] == " ":
            return text[:19]
        if len(text) >= 10 and text[4] == "-" and text[7] == "-":
            return text[:10] + " 00:00:00"
        return ""

    def _config_filter(self, rows, picked):
        """General Purpose: The page subset. The verb list stays complete."""
        begin = picked["begin"]
        end = picked["end"]
        if (begin and not self._config_day(begin)) or (end and not self._config_day(end)):
            return []
        found = []
        for row in rows:
            name = str(row.get("config_name") or "")
            key = str(row.get("config_key") or "")
            if picked["config_name"] and picked["config_name"] not in name:
                continue
            if picked["config_key"] and picked["config_key"] not in key:
                continue
            kind = str(row.get("config_type") or "")
            if picked["config_type"] in ("Y", "N") and kind != picked["config_type"]:
                continue
            if begin or end:
                stamp = self._config_stamp(row.get("create_time"))
                if stamp == "":
                    continue
                if begin and stamp < begin + " 00:00:00":
                    continue
                if end and stamp > end + " 23:59:59":
                    continue
            found.append(row)
        return found

    def _config_by_id(self, rows, raw):
        """General Purpose: One parameter from the unfiltered list, or None."""
        if raw == "" or not str(raw).isdigit():
            return None
        wanted = int(raw)
        for row in rows:
            try:
                if int(row.get("config_id")) == wanted:
                    return row
            except (TypeError, ValueError):
                continue
        return None

    def _config_record(self, row, keep):
        """General Purpose: One parameter row for the table."""
        config_id = "" if row.get("config_id") is None else str(row.get("config_id"))
        if str(row.get("config_type") or "") == "Y":
            built_class = "el-tag el-tag--success"
            built_label = "Yes"
        else:
            built_class = "el-tag el-tag--info"
            built_label = "No"
        remark = row.get("remark")
        if remark is None:
            remark = ""
        created = row.get("create_time")
        if created is None:
            created = ""
        else:
            created = str(created)
        value = row.get("config_value")
        if value is None:
            value = ""
        return {
            "config_id": config_id,
            "config_name": row.get("config_name") or "",
            "config_key": row.get("config_key") or "",
            "config_value": value,
            "remark": remark,
            "created": created,
            "built_class": built_class,
            "built_label": built_label,
            "change_href": self._configs_href(keep, form="edit", config_id=config_id),
        }

    def _configs_href(self, keep, **extra) -> str:
        """General Purpose: /configs with the search fields and any override."""
        values = dict(keep or {})
        values.update(extra)
        params = []
        for key in ("config_name", "config_key", "config_type", "begin", "end", "form", "config_id"):
            raw = values.get(key)
            if raw is None:
                continue
            text = str(raw).strip()
            if text == "":
                continue
            params.append((key, text))
        if not params:
            return "/configs"
        return "/configs?" + urlencode(params)

    def dicts_page(self, user, error) -> str:
        """General Purpose: The dictionary type table, the search, and value add.

        requirement-html-dictionaries — search, six columns, the count line, and value add.
        requirement-rbac-dictionaries — dict_type_list. dict-list still returns values.
        """
        query = getattr(self._request, "query", None) or {}
        picked = self._dict_query(query)
        can_add = self.access.allows(user["user_id"], "system:dict:add")
        rows = []
        for row in self.catalog.dict_type_list(user):
            if self._dict_keeps(row, picked):
                rows.append(self._dict_record(row))
        total = len(rows)
        if total == 0:
            count_line = "Showing 0 to 0 of 0 records"
        else:
            count_line = "Showing 1 to {0} of {0} records".format(total)
        status = picked["status"]
        return self._list(user, error, "Dictionaries", "dicts", rows, {
            "can_add": can_add,
            "show_add": picked["form"] == "add" and can_add,
            "add_href": self._dicts_href(picked["keep"], form="add"),
            "count_line": count_line,
            "query_dict_name": picked["dict_name"],
            "query_dict_type": picked["dict_type"],
            "query_begin": picked["begin"],
            "query_end": picked["end"],
            "status_all": status not in ("0", "1"),
            "status_on": status == "0",
            "status_off": status == "1",
        })

    def _dict_query(self, query):
        """General Purpose: Search fields from the dictionaries page query string.

        requirement-html-dictionaries — name, type, status, and created dates.
        """
        dict_name = self._first(query, "dict_name").strip()
        dict_type = self._first(query, "dict_type").strip()
        status = self._first(query, "status").strip()
        if status not in ("0", "1"):
            status = ""
        begin = self._first(query, "begin").strip()
        end = self._first(query, "end").strip()
        form = self._first(query, "form").strip()
        if form != "add":
            form = ""
        return {
            "dict_name": dict_name,
            "dict_type": dict_type,
            "status": status,
            "begin": begin,
            "end": end,
            "form": form,
            "keep": {
                "dict_name": dict_name,
                "dict_type": dict_type,
                "status": status,
                "begin": begin,
                "end": end,
            },
        }

    def _dict_keeps(self, row, picked):
        """General Purpose: Whether one dictionary type matches the search."""
        name = str(row.get("dict_name") or "")
        kind = str(row.get("dict_type") or "")
        status = "" if row.get("status") is None else str(row.get("status"))
        if picked["dict_name"] and picked["dict_name"] not in name:
            return False
        if picked["dict_type"] and picked["dict_type"] not in kind:
            return False
        if picked["status"] in ("0", "1") and status != picked["status"]:
            return False
        stamp = self._dict_stamp(row.get("create_time"))
        begin = picked["begin"]
        end = picked["end"]
        if begin and (not self._DATE.match(begin) or stamp < "{0} 00:00:00".format(begin)):
            return False
        if end and (not self._DATE.match(end) or stamp > "{0} 23:59:59".format(end)):
            return False
        return True

    def _dict_stamp(self, value):
        """General Purpose: create_time as text, for the column and the date filter."""
        if value is None:
            return ""
        return str(value).strip()[:19]

    def _dict_record(self, row):
        """General Purpose: One type row. Status 0 is Normal. Any other status is Disabled."""
        status = "" if row.get("status") is None else str(row.get("status"))
        normal = status == "0"
        remark = row.get("remark")
        return {
            "dict_id": "" if row.get("dict_id") is None else str(row.get("dict_id")),
            "dict_name": row.get("dict_name") or "",
            "dict_type": row.get("dict_type") or "",
            "remark": "" if remark is None else str(remark),
            "created": self._dict_stamp(row.get("create_time")),
            "status_kind": "success" if normal else "info",
            "status_label": "Normal" if normal else "Disabled",
        }

    def _dicts_href(self, keep, **extra):
        """General Purpose: /dicts with the search fields and any override."""
        values = dict(keep or {})
        values.update(extra)
        params = []
        for key in ("dict_name", "dict_type", "status", "begin", "end", "form"):
            raw = values.get(key)
            if raw is None:
                continue
            text = str(raw).strip()
            if text == "":
                continue
            params.append((key, text))
        if not params:
            return "/dicts"
        return "/dicts?" + urlencode(params)

    def notices_page(self, user, error) -> str:
        """General Purpose: The notice table and the add dialog. The field name is title."""
        rows = self.catalog.notice_list(user)
        return self._list(user, error, "Notices", "notices", rows, {
            "can_add": self.access.allows(user["user_id"], "system:notice:add"),
        })

    def oper_log_page(self, user, error) -> str:
        """General Purpose: The operation log table."""
        rows = self.catalog.oper_log(user)
        return self._list(user, error, "Operation log", "oper-log", rows)

    def login_log_page(self, user, error) -> str:
        """General Purpose: The login log search row and the attempt table.

        requirement-html-login-log — nine columns, the status tag, and the count line.
        requirement-rbac — Catalog.login_log still owns who may list.
        """
        query = getattr(self._request, "query", None) or {}
        picked = self._login_query(query)
        rows = self._login_kept(self.catalog.login_log(user), picked)
        total = len(rows)
        if total == 0:
            count_line = "Showing 0 to 0 of 0 records"
        else:
            count_line = "Showing 1 to {0} of {0} records".format(total)
        return self._list(user, error, "Login log", "login-log", rows, {
            "query_ipaddr": picked["ipaddr"],
            "query_user_name": picked["user_name"],
            "query_begin": picked["begin"],
            "query_end": picked["end"],
            "status_all": picked["status"] == "",
            "status_ok": picked["status"] == "0",
            "status_bad": picked["status"] == "1",
            "count_line": count_line,
        })

    def _login_query(self, query):
        """General Purpose: Search fields from the login log query string.

        requirement-html-login-log — address, name, status, and the date pair.
        """
        status = self._first(query, "status").strip()
        if status not in ("0", "1"):
            status = ""
        return {
            "ipaddr": self._first(query, "ipaddr").strip(),
            "user_name": self._first(query, "user_name").strip(),
            "status": status,
            "begin": self._first(query, "begin").strip(),
            "end": self._first(query, "end").strip(),
        }

    def _login_date(self, text) -> bool:
        """General Purpose: True when text is YYYY-MM-DD."""
        if len(text) != 10 or text[4] != "-" or text[7] != "-":
            return False
        return text[:4].isdigit() and text[5:7].isdigit() and text[8:].isdigit()

    def _login_stamp(self, value) -> str:
        """General Purpose: One login time as YYYY-MM-DD HH:MM:SS, or empty."""
        if value is None or value == "":
            return ""
        if hasattr(value, "strftime"):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return str(value).strip().replace("T", " ", 1)

    def _login_kept(self, rows, picked):
        """General Purpose: The filtered login rows, newest info_id first.

        requirement-html-login-log — a bad date matches no row.
        """
        begin = picked["begin"]
        end = picked["end"]
        if (begin and not self._login_date(begin)) or (end and not self._login_date(end)):
            return []
        matched = []
        for row in rows:
            if self._login_match(row, picked, begin, end):
                matched.append(row)
        matched.sort(key=lambda row: int(row.get("info_id") or 0), reverse=True)
        return [self._login_record(row) for row in matched]

    def _login_match(self, row, picked, begin, end) -> bool:
        """General Purpose: Whether one stored attempt stays in the filtered list."""
        if picked["ipaddr"] and picked["ipaddr"] not in str(row.get("ipaddr") or ""):
            return False
        if picked["user_name"] and picked["user_name"] not in str(row.get("user_name") or ""):
            return False
        status = str(row.get("status") if row.get("status") is not None else "")
        if picked["status"] in ("0", "1") and status != picked["status"]:
            return False
        stamp = self._login_stamp(row.get("login_time"))
        if begin and (stamp == "" or stamp < "{0} 00:00:00".format(begin)):
            return False
        if end and (stamp == "" or stamp > "{0} 23:59:59".format(end)):
            return False
        return True

    def _login_record(self, row):
        """General Purpose: One table row. Status 0 is Success. Any other status is Failed."""
        status = str(row.get("status") if row.get("status") is not None else "")
        ok = status == "0"
        return {
            "info_id": "" if row.get("info_id") is None else row.get("info_id"),
            "user_name": row.get("user_name") or "",
            "ipaddr": row.get("ipaddr") or "",
            "login_location": row.get("login_location") or "",
            "browser": row.get("browser") or "",
            "os": row.get("os") or "",
            "msg": row.get("msg") or "",
            "login_time": self._login_stamp(row.get("login_time")),
            "status_label": "Success" if ok else "Failed",
            "tag_type": "success" if ok else "danger",
        }

    def online_page(self, user, error) -> str:
        """General Purpose: Online sessions. The button shows an 8-character token prefix.

        requirement-html-online — search, seven columns, the Online tag, and the count line.
        requirement-web-interface — the full token is only the hidden field.
        The verb online-list still returns every session. This page shows the filtered subset.
        """
        query = getattr(self._request, "query", None) or {}
        ipaddr = self._first(query, "ipaddr").strip()
        user_name = self._first(query, "user_name").strip()
        rows = []
        for row in self.catalog.online_list(user):
            host = self._online_text(row.get("ipaddr"))
            name = self._online_text(row.get("user_name"))
            if ipaddr and ipaddr not in host:
                continue
            if user_name and user_name not in name:
                continue
            token = self._online_text(row.get("token"))
            rows.append({
                "number": len(rows) + 1,
                "token": token,
                "token_prefix": token[:8],
                "user_name": name,
                "ipaddr": host,
                "login_time": self._online_text(row.get("login_time")),
                "last_access": self._online_text(row.get("last_access")),
            })
        total = len(rows)
        if total == 0:
            count_line = "Showing 0 to 0 of 0 records"
        else:
            count_line = "Showing 1 to {0} of {0} records".format(total)
        return self._list(user, error, "Online", "online", rows, {
            "can_logout": self.access.allows(user["user_id"], "monitor:online:forceLogout"),
            "query_ipaddr": ipaddr,
            "query_user_name": user_name,
            "count_line": count_line,
        })

    def _online_text(self, value) -> str:
        """General Purpose: A session cell. None is an empty cell."""
        if value is None:
            return ""
        return str(value)

    def store_menus_for_grant(self, user):
        """General Purpose: The same menu ids the grant form uses."""
        return self._menus_unscoped()
