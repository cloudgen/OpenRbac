# PyRbac test plan — 2026-10-11

Run `tests/run.sh` from the repository root. The RBAC cases use a temporary sqlite3 file. They do not need MariaDB. `tests/test_rbac.py` also tries mysql database `pyrbac_test` when the mode-0600 database file has a password and the server accepts it. That case skips when mysql is down. Neither case writes `ruoyi_db` or `ry`.

| ID | File | Proves |
|----|------|--------|
| TP-TUI-09 | `tests/test_tui.py` | Path label stays `Path` when `LANG` is Traditional Chinese |
| TP-TUI-10 | `tests/test_tui.py` | Wide columns count as two. The front board fits the new rows |
| TP-LANG-01 | `tests/test_language.py` | Row 4, codes 41–53, mode 0600 leaf, `PYRBAC_LANG` does not write |
| TP-MENU-01 | `tests/test_hello.py` | Front numbers 2–9. No session row. Sign-in gate retries a wrong password. `login` does not open the menu. `hello` is absent |
| TP-DB-02 | `tests/test_rbac.py` | A domain verb and `serve` seed a database that has no tables, once |
| TP-ABOUT | `tests/test_about.py` | Identity block, host check, star box |
| TP-RBAC-01 | `tests/test_rbac.py` | Seed once, scopes 3, 4, and 5, protected user and role |
| TP-WEB-01 | `tests/test_rbac.py` | Login cookie, CSRF 400, operator 403, redirect |
| TP-ENV-01 | `tests/test_rbac.py` | Mode 0600 file, environment wins, remote bind refused |
| TP-DB-03 | `tests/test_rbac.py` | Default sqlite3 file, `db-engine` choices, web radios, file mode 0600, mysql seed when the server is up |
| TP-LOG-01 | `tests/test_rbac.py` | ChronicleLogger construct. Password absent from the log file |
| TP-DOC-01 | `tests/test_docs.py` | README headings, version badge, absolute screenshot URLs |
| TP-BUILD-01 | todo | `./build.sh` help lists every maintainer command. Not executed yet |
| TP-BUILD-02 | todo | `test` and `test-install` reject an extra token. Not executed yet |
| TP-BUILD-03 | todo | `./build.sh version` matches `src/PyRbac/__init__.py`. Not executed yet |
| TP-BUILD-04 | todo | `clean` removes `dist/` and leaves `src/PyRbac`. Not executed yet |

A failure in TP-RBAC-01 that names `ruoyi_db` or `ry` means the test pointed at the wrong schema. Stop and fix the environment before repeating the write.
