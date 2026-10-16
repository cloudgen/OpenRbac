**file**: docs/requirements/requirement-python-tui.md
**Status**: Active (Version 1.6.5)
**Area**: python
**Key**: `requirement-python-tui`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

The text menu is the front board plus nested boards. The first row is the working directory on the left and the local clock on the right. The bottom of the screen is a rounded input box. The status line under the box names the product, the version, and the board.

Empty arguments on a terminal use sqlite3 and the default file, then try a saved local sign-in (`requirement-local-login`). When that sign-in still matches, the menu opens without a question. Otherwise they ask for an account name and a password, then open this menu. They do not ask for the engine or the file path. They do not run pip. The same domain actions are typed verbs (`requirement-python-cli-interface`) and web pages (`requirement-web-interface`). The front board has no session row. `login`, `logout`, and `whoami` stay typed verbs. Row 9 Exit asks before it leaves.

### 1.1 Human-facing

**In one sentence:** On a terminal, `open-rbac` uses the sqlite3 default file, opens the menu when a saved sign-in still matches, and otherwise asks for an account and a password. The menu has no session row. Exit asks before it leaves.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person at the keyboard | `open-rbac`, then the account name and the password |
| The other role | The path label | `Path` until a language pick says otherwise |
| Not this file | Permission checks | `requirement-rbac` |

## 2. Front board

| Number | Kind | Role |
|--------|------|------|
| 1 | rbac | users, roles, menus, departments, job titles. Children 11–19 and 110–113. Back 0 returns to the front board |
| 2 | server | setup 21, audit 22, serve 23, theme 24. Back 0 returns to the front board |
| 3 | system-log | view-log 31, clear-log 32, log-folder 33, Back 0 |
| 6 | self-management | 62 version, 63 about, 64 version-check, 65 self-update, 66 self-uninstall, 67 self-install, Back 0 |
| 7 | language | codes 71–83 and Back 0 |
| 9 | Exit | ask, then log out or keep the saved sign-in |

Setup is server row 21. Its children are 211–218. Number 218 is `db-engine`. Back 0 returns to the server board. Audit is server row 22. Its children are 221–224. Back 0 returns to the server board. Serve is server row 23. It starts the web listener and shows the URL. It is not its own board. Theme is server row 24. It asks for the eleven skins in `requirement-html-theme`. Enter selects apex. It is not its own board. Numbers 4, 5, and 8 are not rows.

`help` is a word on the open menu. It is not a numbered row. `language` is not an argv verb.

## 3. Normative rules

1. **Path and clock.** The path line **MUST** be the path label, a colon, the absolute working directory, and `HH:MM:SS` when both fit. The label comes from the language requirement. `LANG` **MUST NOT** select it. The directory and the clock are not translated.
2. **Columns.** Wide and Fullwidth characters count as two columns. Ambiguous characters, including the box glyphs and the block caret, count as one. A wide character that does not fit is dropped whole.
3. **Frame.** The input box uses `╭`, `╮`, `╰`, `╯`, `─`, and `│`. The caret is `█`. The hint is `Up/Down  •  Enter`.
4. **Clock layers.** The one-second clock refresh applies on front, rbac, server, setup, audit, system-log, language, and self-management. It does not apply on a result page, the sign-in question, or another question.
5. **Password.** A password question **MUST** mask the input with asterisks. Esc on a board question **MUST** cancel that question and stay on the board. Esc on the sign-in question **MUST** leave without opening the menu.
6. **Result.** A string returned by a row **MUST** be a result page. Up and Down scroll it when it overflows. Another key returns to the front board.
7. **Pip.** Rows 64–67 and the matching verbs use `python -m pip`. Empty arguments **MUST NOT** run them. `self-uninstall` on the command line **MUST** require `--force`.
8. **Numbers.** Rbac is front row 1. Its children are 11–19 and 110–113. Server is front row 2 and holds setup 21, audit 22, serve 23, and theme 24. System-log stays 3 and 31–33. Self-management is front row 6 and 62–67. Language is front row 7 and 71–83. Exit stays 9. Numbers 4, 5, and 8 **MUST NOT** be rows. The front board **MUST NOT** include a session row. Back on setup and on audit **MUST** return to the server board. Back on rbac, server, system-log, language, and self-management **MUST** return to the front board. Esc on a nested board **MUST** return to the front board.
9. **Sign-in first.** Empty arguments on a terminal **MUST** use sqlite3 and the default file, then prepare the database (`requirement-database`), then try the saved local sign-in (`requirement-local-login`). When that sign-in still matches, the front board **MUST** open without a question. Otherwise they **MUST** ask for `user_name` and a masked password, one field at a time. They **MUST NOT** ask for the engine or the file path. The sign-in text **MUST** name that file. A wrong password **MUST** show the error and ask again. A match **MUST** open the front board. The menu **MUST NOT** appear before that match. Esc on the sign-in question **MUST** leave without the menu.
10. **Setup row.** Number 218 **MUST** be `db-engine` with the explain `sqlite3 file or mysql`. It **MUST** offer choice 1 sqlite3, including the default file, and choice 2 mysql. Enter **MUST** select sqlite3 and the default file. Esc **MUST** stay on the setup board.
11. **Exit.** Row 9 Exit **MUST** ask before it leaves, as `requirement-local-login` specifies. Enter or `y` **MUST** log out and leave. `n` **MUST** leave and keep the saved sign-in. Esc **MUST** stay on the front board. End of input **MUST** leave without the question.
12. **Theme row.** Number 24 **MUST** be `theme` with the explain `11 skins, default apex`. It **MUST** offer the eleven choices in `requirement-html-theme`. Enter **MUST** select apex. Esc **MUST** stay on the server board. A stored name that is not one of those eleven **MUST** still show the choices. Enter **MUST** store apex over that name. The question **MUST NOT** close the menu. The verb is `requirement-python-cli-interface`. This row **MUST NOT** open the database. The stored choice **MUST** be the skin `serve` renders, as `requirement-html-theme` requires. A page **MUST** still refuse an invalid theme until that choice is stored.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | Missing language file keeps the label `Path` while `LANG` is Traditional Chinese |
| AC-2 | Front numbers are 1, 2, 3, 6, 7, and 9. Row 1 is rbac. Row 7 is language. No row is session |
| AC-3 | Wide columns do not share a cell |
| AC-4 | Server row 24 is `theme` and offers apex and the other skins |
| AC-5 | A settings file that says `adminlte` still lists `1 apex` through `11 kero`. Enter stores apex. `theme()` still refuses `adminlte` until that store |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Front board | The menu opened after a successful sign-in |
| Path label | The word before the directory. Default `Path`. Traditional Chinese pick uses `路徑` |
| Leaf short | An English token such as `view-log` or `login` |
| Category short | A board name that follows the selected language when a translation exists |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.0.0 | Inherited frame, path, clock, and columns |
| 2026-10-11 | Active 1.1.0 | Session, access, setup, audit, and serve join the front board |
| 2026-10-11 | Active 1.2.0 | Sign-in before the menu. The session row is gone. Numbers 2–9 stay |
| 2026-10-11 | Active 1.3.0 | Engine choice before sign-in. Setup row 78 is db-engine |
| 2026-10-11 | Active 1.4.0 | Sign-in uses the sqlite3 default file. Row 78 still offers the choice |
| 2026-10-11 | Active 1.5.0 | A matching saved sign-in skips the question. Row 9 Exit asks |
| 2026-10-14 | Active 1.6.0 | Row 1 is rbac. Row 2 server holds setup, audit, and serve. Self-management is 6. Language is 7 |
| 2026-10-14 | Active 1.6.1 | Row 1 names job titles |
| 2026-10-14 | Active 1.6.2 | Server row 24 is `theme`. Choice 1 is vue3. Choice 2 is adminlte |
| 2026-10-14 | Active 1.6.3 | The stored choice is the skin `serve` renders |
| 2026-10-16 | Active 1.6.4 | Server row 24 offers apex and ten more skins |
| 2026-10-16 | Active 1.6.5 | An invalid stored name still lists the eleven skins. Enter stores apex |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
