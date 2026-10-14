# Tests — OpenRbac

Executable proof for product law. The public plan is `reviews/test-plan.md`.

## Run

```bash
./tests/run.sh
```

RBAC cases use a temporary sqlite3 file. A mysql case uses database `openrbac_test` when that server is reachable and skips otherwise. They do not write `ruoyi_db` or `ry`.

| File | What it proves |
|------|----------------|
| `test_tui.py` | Path label and wide columns |
| `test_language.py` | Row 7, codes 71–83, `OPENRBAC_LANG` |
| `test_hello.py` | Front board and the menu gate |
| `test_about.py` | About page and host check |
| `test_rbac.py` | Scope, web cookie, CSRF, environment, ChronicleLogger |
| `test_docs.py` | README headings and absolute screenshot URLs |
