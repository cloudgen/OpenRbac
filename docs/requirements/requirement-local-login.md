**file**: docs/requirements/requirement-local-login.md
**Status**: Active (Version 1.0.0)
**Area**: domain
**Key**: `requirement-local-login`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

A successful terminal sign-in stores the account name and the password so the next start can try them again. The text menu skips the question when that sign-in still works. Row 9 Exit asks before it leaves, and a confirmed logout removes the saved sign-in.

### 1.1 Human-facing

**In one sentence:** After you sign in on the terminal, the next start can open the menu without asking, and Exit asks whether to log out.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person at the keyboard | Sign in once, start again, the menu opens |
| The other role | The saved sign-in | Two mode-0600 files in the home folder |
| Not this file | The web cookie | `requirement-web-interface` |

| Includes | Excludes |
|----------|----------|
| Terminal `login` and the text-menu sign-in | The web sign-in page |
| Exit asks, then logs out when confirmed | Leaving on end of input without a question |

## 2. Files

Both files live in the home folder from `requirement-environment` (`OPENRBAC_HOME`, otherwise `~/.local/OpenRbac`).

| File | Contents |
|------|----------|
| `local-login` | Ciphertext. Four text lines: `OPENRBACLOCAL1`, base64 nonce, base64 check, base64 ciphertext |
| `local-login-key` | 32 random bytes used only to read `local-login` |

The plaintext is two big-endian lengths and then the UTF-8 account name and password. Each length fits in 16 bits. The nonce is 16 random bytes. The stream and the check are both HMAC-SHA256, with different fixed labels, and the check is compared with `compare_digest`. The standard library is enough. No extra package is required.

## 3. Normative rules

1. **Store.** `Desk.login` **MUST** write the ciphertext after the terminal token. The text menu and the typed verb `login` both use that method. The account name and the password in the file **MUST** be ciphertext. The password **MUST NOT** appear in the login file as plain text.
2. **Modes.** Both files **MUST** be mode `0600`. Their folder **MUST** be mode `0700`. A file that is not mode `0600` **MUST** be treated as unusable. A key that is not mode `0600`, missing, or the wrong length **MUST** be replaced on the next save. A bad check **MUST** be treated as unusable.
3. **Restore.** On the text menu, after the database is prepared and before the sign-in question, the program **MUST** try the previous sign-in. A live terminal token **MUST** open the front board without a question. Otherwise the program **MUST** decode the saved account and password and try the login. A match **MUST** open the front board without a question. A failed try **MUST** remove the ciphertext and **MUST** ask. Esc on that question **MUST** still leave without the menu.
4. **Logout.** `Desk.logout` **MUST** remove the ciphertext. It **MUST** do that even when the terminal token is already gone. A missing token **MUST** still report not signed in. The typed verb `logout` uses that method.
5. **Exit.** Row 9 Exit **MUST** ask before it leaves. Enter or `y` **MUST** log out, remove the saved sign-in, and leave with status 0. `n` **MUST** leave and keep the saved sign-in. Esc **MUST** stay on the front board. End of input **MUST** leave without the question and **MUST NOT** log out. `self-uninstall` **MUST NOT** use this question.
6. **Web.** A web sign-in **MUST NOT** write `local-login` or `local-login-key`. It uses the cookie only.
7. **Log.** The status log **MUST NOT** contain the password, the ciphertext, or the key bytes. A saved, cleared, or rejected line **MUST** name the action only.
8. **Limit.** These files stop a person who can read only the login file from seeing the password. They do not stop a person who can already read both files. Versioned documents **MUST NOT** print a live password or the key bytes.

## 4. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | A saved sign-in round-trips, both files are mode 0600, and the password is not plain text in the login file |
| AC-2 | A bad mode or a bad check does not return the password |
| AC-3 | A second process with the same home restores the account after the token file is gone |
| AC-4 | Logout removes the ciphertext, including when the token is already gone |
| AC-5 | A failed restore removes the ciphertext |
| AC-6 | A web sign-in does not create the login file |
| AC-7 | Exit stays when the answer is Esc, logs out on Enter or `y`, and keeps the saved sign-in on `n` |
| AC-8 | End of input leaves without asking |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Saved sign-in | The ciphertext file plus its key file |
| Restore | Decode that sign-in and try it, or accept a live terminal token |
| Exit question | The row 9 prompt. Enter logs out. `n` keeps the saved sign-in. Esc stays |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-11 | Active 1.0.0 | Encrypted local sign-in. Exit asks, then logs out when confirmed |

---

**Last Updated**: 2026-10-11
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
