# OpenRbac checklist — 2026-10-11

Use this list before a push to `cloudgen/OpenRbac`.

## Requirements

- [x] Exactly one Active domain file: `requirement-domain-openrbac`
- [x] RBAC, database, environment, local login, web, TUI, and CLI requirements exist
- [x] ChronicleLogger is required at `>=1.3.1` and constructed in `def main`
- [x] Index status matches the file headers for the new rows

## Behavior

- [x] Empty argv on a terminal uses the sqlite3 default file, restores a saved sign-in when it still matches, otherwise asks, then opens the menu, and does not run pip
- [x] Front rows are access, system-log, language, setup, audit, serve, self-management, Exit. There is no session row
- [x] Row 9 Exit asks. Enter or y logs out and removes the saved sign-in. n keeps it. Esc stays. End of input leaves without the question
- [x] Language stays on row 4, codes 41–53, leaf `~/.local/OpenRbac/language`
- [x] System-log stays on 3 and 31–33. Self-management stays on 8 and 82–87
- [x] Data scope 1–4. Unknown scope shows no users
- [x] Web bind defaults to loopback. CSRF and cookie are present
- [x] Passwords are not written to the ChronicleLogger file
- [x] A terminal sign-in stores the account and password as ciphertext, mode 0600, and logout removes that file
- [x] A failed restore removes the saved sign-in. A web sign-in does not write it

## Database

- [x] Default engine is sqlite3 file `openrbac.sqlite3`. mysql schema is `openrbac`. mysql tests use `openrbac_test`
- [x] The command, the text menu, and the web page each offer sqlite3 and mysql
- [x] `db-init` seeds only when `sys_user` is empty
- [x] A menu, `serve`, or domain verb initializes a missing database before it continues
- [x] Tests do not write `ruoyi_db` or `ry`

## Document

- [x] README screenshots are the current menu (1.0.4, no session row) and use absolute raw GitHub URLs
- [x] Seeded passwords are documented with a change-them warning
- [x] No vault path, private key, or live database password in versioned docs

## Publish

- [x] Public repository `cloudgen/OpenRbac` created with the GitHub REST API
- [x] Push uses the cloudgen SSH vault after `Hi cloudgen!`
- [x] The Wilgat/VideoJoin remote is not the push target
