**file**: docs/requirements/requirement-database.md
**Status**: Active (Version 1.0.0)
**Area**: domain
**Key**: `requirement-database`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

PyRbac stores its RBAC tables in MariaDB or MySQL. The product database is `pyrbac`. Tests use `pyrbac_test`. Existing databases, including `ruoyi_db` and `ry`, are not this product's schema and **MUST NOT** be written.

The table shapes follow the FastAPI edition of RuoYi: `user_name` is the login, and there is no password salt column. The password column is wider than the upstream bcrypt column because this product stores PBKDF2. Online sessions are `sys_session` because this product does not use Redis.

### 1.1 Human-facing

**In one sentence:** `py-rbac db-init` creates the tables in this product's database and fills them only when no user exists yet.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The operator with a database password | `py-rbac db-init` |
| The other role | The database account `pyrbac`@localhost | It can use only `pyrbac` and `pyrbac_test` |
| Not this file | Which departments a user may see | `requirement-rbac` |

| Includes | Excludes |
|----------|----------|
| Parameterized SQL through PyMySQL | String-built SQL from a typed name |
| Create-if-missing, then seed-if-empty | A second seed that duplicates admin |
| `sys_session` for online users | Redis |

## 2. Normative rules

1. **Schemas.** The product **MUST** use the database named by `PYRBAC_DB_NAME`. The default is `pyrbac`. Tests **MUST** set `pyrbac_test`. The product **MUST NOT** open `ruoyi_db` or `ry` as its working database.
2. **Privilege.** The database account **MUST** be limited to `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `DROP`, `INDEX`, and `ALTER` on `pyrbac` and `pyrbac_test`.
3. **Statements.** Every value **MUST** be a parameter. An error returned to the operator **MUST NOT** include the SQL text or the password.
4. **Tables.** `db-init` **MUST** create `sys_dept`, `sys_user`, `sys_post`, `sys_role`, `sys_menu`, `sys_user_role`, `sys_role_menu`, `sys_role_dept`, `sys_user_post`, `sys_oper_log`, `sys_dict_type`, `sys_dict_data`, `sys_config`, `sys_logininfor`, `sys_notice`, and `sys_session` when they are missing.
5. **Seed once.** When `sys_user` has any row, `db-init` **MUST** return `present` and **MUST NOT** insert another admin. The first empty run **MUST** return `seeded`.
6. **Other verbs.** A verb that needs a table **MUST** fail with a next step that names `py-rbac db-init` when the table is missing. It **MUST NOT** create the seed by itself except `db-init`.

## 3. Acceptance checks

| ID | Check |
|----|-------|
| AC-1 | The first `db-init` on an empty `pyrbac_test` reports seeded |
| AC-2 | The second `db-init` reports present |
| AC-3 | A failed statement does not echo the password |

## Terminologies

| Term | Meaning in this file |
|------|----------------------|
| Product database | The schema named `pyrbac` unless `PYRBAC_DB_NAME` says otherwise |
| Test database | `pyrbac_test` |
| Seed | The first English rows inserted only into an empty `sys_user` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-11 | Active 1.0.0 | Dedicated MariaDB schemas and FastAPI-shaped tables |

---

**Last Updated**: 2026-10-11
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
