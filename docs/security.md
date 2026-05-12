# Security Design & STRIDE Threat Model

## Authentication & Authorization

- **Mechanism:** JWT (HS256) issued via OAuth2 Password flow (`POST /api/auth/token`).
- **Token lifetime:** 60 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`).
- **Roles:** `viewer`, `analyst`, `admin`. Only `admin` can trigger ETL refresh.
- **Password storage:** bcrypt (cost factor 12) via passlib. Passwords are never logged.
- **Secret key:** Loaded from `SECRET_KEY` env var. Default value in config is a placeholder that must be replaced in production.

## STRIDE Threat Model

### S — Spoofing
| Threat | Mitigation |
|--------|-----------|
| Attacker forges a JWT | HS256 signature verified on every request; token expiry enforced by `python-jose`. |
| Credential stuffing on `/api/auth/token` | slowapi rate limiting: 60 req/min per IP on all endpoints. |

### T — Tampering
| Threat | Mitigation |
|--------|-----------|
| SQL injection via query params | All user-supplied values go through DuckDB `?` parameterized queries. Column names and filter keywords are fixed string literals in code. |
| Tampered JWT payload | HMAC-SHA256 signature invalidates any modified payload. |
| Tampered database file | Out of scope for this portfolio project; in production, mount as read-only after ETL and use filesystem-level integrity checks. |

### R — Repudiation
| Threat | Mitigation |
|--------|-----------|
| Disputed API actions | structlog emits structured JSON logs with `request_id`, timestamp, and route on every request. Admin ETL triggers are logged with the authenticated `user_id`. |

### I — Information Disclosure
| Threat | Mitigation |
|--------|-----------|
| Secrets in source code | `.env` is gitignored; `.env.example` contains only placeholder values. `SECRET_KEY` is never hardcoded. |
| Error messages leaking stack traces | FastAPI's default exception handlers return generic messages; Python tracebacks are not forwarded to clients. |
| Sensitive data in logs | GPA and student records are never logged at `INFO` level; only aggregate counts appear in ETL output. |

### D — Denial of Service
| Threat | Mitigation |
|--------|-----------|
| Request flooding | slowapi enforces 60 req/min per remote IP. Fly.io enforces `hard_limit = 200` concurrent requests. |
| Expensive query via classification list | `classification IN (?)` is bounded by the four valid values; unlimited lists are not accepted. |

### E — Elevation of Privilege
| Threat | Mitigation |
|--------|-----------|
| Viewer calling admin ETL endpoint | `require_admin` dependency checks `role == "admin"` in the JWT payload; returns HTTP 403 otherwise. |
| JWT role tampering | Role claim is inside the signed payload; any modification invalidates the HMAC. |

## CORS Policy

CORS is configured with `allow_origins=["*"]` for the portfolio demo. In a production environment, `allow_origins` should be restricted to the Vercel frontend domain.

## Dependency Supply Chain

All dependencies are pinned to semver ranges in `pyproject.toml` and `package.json`. CI runs on every push; Dependabot should be enabled on the repository to receive automated security updates.
