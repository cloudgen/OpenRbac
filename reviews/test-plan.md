# PyRbac test plan — 2026-10-11

Run `tests/run.sh` from the repository root. The RBAC cases need MariaDB, the `pyrbac_test` schema, and `PYRBAC_DB_PASSWORD` in the mode-0600 database file or in the environment. They set `PYRBAC_DB_NAME=pyrbac_test` themselves.

| ID | File | Proves |
|----|------|--------|
| TP-TUI-09 | `tests/test_tui.py` | Path label stays `Path` when `LANG` is Traditional Chinese |
| TP-TUI-10 | `tests/test_tui.py` | Wide columns count as two. The front board fits the new rows |
| TP-LANG-01 | `tests/test_language.py` | Row 4, codes 41–53, mode 0600 leaf, `PYRBAC_LANG` does not write |
| TP-MENU-01 | `tests/test_hello.py` | Front numbers 1–9. `login` does not open the menu. `hello` is absent |
| TP-ABOUT | `tests/test_about.py` | Identity block, host check, star box |
| TP-RBAC-01 | `tests/test_rbac.py` | Seed once, scopes 3, 4, and 5, protected user and role |
| TP-WEB-01 | `tests/test_rbac.py` | Login cookie, CSRF 400, operator 403, redirect |
| TP-ENV-01 | `tests/test_rbac.py` | Mode 0600 file, environment wins, remote bind refused |
| TP-LOG-01 | `tests/test_rbac.py` | ChronicleLogger construct. Password absent from the log file |
| TP-DOC-01 | `tests/test_docs.py` | README headings, version badge, absolute screenshot URLs |

A failure in TP-RBAC-01 that names `ruoyi_db` or `ry` means the test pointed at the wrong schema. Stop and fix the environment before repeating the write.
