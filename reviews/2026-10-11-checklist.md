# PyRbac checklist — 2026-10-11

Use this list before a push to `cloudgen/PyRbac`.

## Requirements

- [x] Exactly one Active domain file: `requirement-domain-pyrbac`
- [x] RBAC, database, environment, web, TUI, and CLI requirements exist
- [x] ChronicleLogger is required at `>=1.3.1` and constructed in `def main`
- [x] Index status matches the file headers for the new rows

## Behavior

- [x] Empty argv on a terminal asks for a sign-in, then opens the menu, and does not run pip
- [x] Front rows are access, system-log, language, setup, audit, serve, self-management, Exit. There is no session row
- [x] Language stays on row 4, codes 41–53, leaf `~/.local/PyRbac/language`
- [x] System-log stays on 3 and 31–33. Self-management stays on 8 and 82–87
- [x] Data scope 1–4. Unknown scope shows no users
- [x] Web bind defaults to loopback. CSRF and cookie are present
- [x] Passwords are not written to the ChronicleLogger file

## Database

- [x] Product schema is `pyrbac`. Tests use `pyrbac_test`
- [x] `db-init` seeds only when `sys_user` is empty
- [x] A menu, `serve`, or domain verb initializes a missing database before it continues
- [x] Tests do not write `ruoyi_db` or `ry`

## Document

- [x] README screenshots use absolute raw GitHub URLs
- [x] Seeded passwords are documented with a change-them warning
- [x] No vault path, private key, or live database password in versioned docs

## Publish

- [x] Public repository `cloudgen/PyRbac` created with the GitHub REST API
- [x] Push uses the cloudgen SSH vault after `Hi cloudgen!`
- [x] The Wilgat/VideoJoin remote is not the push target
