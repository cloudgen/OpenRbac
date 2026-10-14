**file**: docs/requirements/requirement-python-readme.md
**Status**: Active (Version 1.5.1)
**Area**: python
**Key**: `requirement-python-readme`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

The root `README.md` is the public user document. Its version badge matches `__version__`. Every screenshot is an absolute `https://raw.githubusercontent.com/cloudgen/OpenRbac/main/screenshots/<file>.png` link. The pictures are captures of the running text menu.

### 1.1 Human-facing

**In one sentence:** The README shows the real menu, the seeded accounts, and how to change those passwords.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | A reader on GitHub | The screenshot of the front board |
| The other role | The raw image URL | `https://raw.githubusercontent.com/cloudgen/OpenRbac/main/screenshots/main-menu-en.png` |
| Not this file | A host vault path | Never written here |

## 2. Required headings

Features, Advantages, Quick Installation, Usage, Screenshots, Examples, Platform Compatibility, Related Projects, Contributing, License, Last Update.

## 3. Normative rules

1. **Badge.** The version token is `1.0.5`.
2. **Images.** A picture **MUST** use the absolute raw URL above. A relative `screenshots/` link is not enough.
3. **Seed.** The document **MUST** list admin / admin123, operator / operator123, clerk / clerk123, and lead / lead123, and **MUST** tell the operator to change them.
4. **Differences.** The document **MUST** say passwords are PBKDF2 rather than bcrypt, sessions are `sys_session` rather than Redis, and data scope is 1–4.
5. **Bind.** The document **MUST** say the site listens on `127.0.0.1` unless `OPENRBAC_ALLOW_REMOTE=yes`.
6. **Process list.** The document **MUST** say `--password` is visible in the process list and the menu masks the field.
7. **No secrets.** The document **MUST NOT** include a vault path, a private key, or the live database password.
8. **Sign-in.** The document **MUST** say that a terminal with no arguments uses the sqlite3 default file and then asks for an account and a password before the menu when no saved sign-in matches, that a matching saved sign-in skips that question, that row 9 Exit asks and can log out, that the menu has no session row, and that a run creates missing tables before that question.
9. **Engine.** The document **MUST** say that sqlite3 is the default file `~/.local/OpenRbac/openrbac.sqlite3`, that Enter on `db-engine` selects that file, and that mysql is choice 2.

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Raw URL | The GitHub URL that serves one PNG from the `main` branch |
| Seed account | One of the four accounts created by the first `db-init` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.0.0 | Earlier picture catalog |
| 2026-10-11 | Active 1.1.0 | OpenRbac captures and seed disclosure |
| 2026-10-11 | Active 1.2.0 | Badge 1.0.1. Sign-in before the menu. No session row |
| 2026-10-11 | Active 1.3.0 | Badge 1.0.2. sqlite3 default file and mysql choice |
| 2026-10-11 | Active 1.4.0 | Badge 1.0.3. Sign-in uses the sqlite3 default file without an extra question |
| 2026-10-11 | Active 1.5.0 | Badge 1.0.4. Saved sign-in and the Exit question |
| 2026-10-14 | Active 1.5.1 | Badge 1.0.5. Pictures are the current front board |

---

**Last Updated**: 2026-10-14
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
