# Employee Management System (FastAPI + SQLAlchemy + SQLite)

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Docs at `http://127.0.0.1:8000/docs`. The SQLite file `employee_management.db`
is created automatically on first run.

## Structure

```
main.py                  # orchestration only: create app, create tables,
                          # register exception handlers, include routers
base.py                  # Base = declarative_base()
database.py              # engine, SessionLocal, get_db
models.py                # Pydantic request/response models
schemas.py                # Employees and Users table schema
exceptions.py             # custom domain exceptions (framework-agnostic)
exception_handlers.py     # maps each domain exception -> HTTP response
auth.py                   # password hashing, JWT, get_current_user
employee_service.py       # employee CRUD business logic
user_service.py           # signup/login business logic
endpoints/
    user_api.py            # router: /auth/signup, /auth/login
    employee_api.py        # router: /employees CRUD
```

**Request flow:** router -> service -> (raises a domain exception on
failure) -> global exception handler -> HTTP response. Routers never
catch exceptions themselves; they just call the service and return.

## Bootstrap problem (read this first)

Every `/employees` endpoint requires a logged-in user. Signing up requires
an already-eligible employee. So the very first employee has to be
inserted directly into the database — there's no way to do it through the
API before any user exists.


## Design notes

- **`is_eligible`** on `Employee` gates who's allowed to sign up.
- **`User.email`** is always set to `employee.email` at signup time —
  never supplied independently — so a user's login email can never drift
  from their employee record. This also makes `User.email` uniqueness
  automatic, since `Employee.email` is already unique and each employee
  maps to at most one user.
- **Self-deletion is blocked**: a logged-in user cannot delete the
  employee record linked to their own account, since `Employee.user` has
  `cascade="all, delete-orphan"` — deleting your own employee row would
  cascade-delete your own login mid-session.
- **Pagination**: `GET /employees` takes `page` (>=1) and `page_size`
  (1-100, default 10), returning `{items, total, page, page_size,
  total_pages}`.
- **Login form field**: `HTTPBearer` gives an access token which is responded back to you. use that access token to authorize. 
## Endpoints

| Method | Path            | Auth required | Purpose                          |
|--------|-----------------|---------------|-----------------------------------|
| POST   | /auth/signup    | no            | Create a user for an eligible employee |
| POST   | /auth/login     | no            | Get a JWT access token field
| POST   | /employees      | yes           | Create employee                   |
| GET    | /employees      | yes           | List employees (paginated)        |
| GET    | /employees/{id} | yes           | Retrieve one employee             |
| PUT    | /employees/{id} | yes           | Update employee (partial)         |
| DELETE | /employees/{id} | yes           | Delete employee (not your own)    |

## Before production


- Add rate limiting on `/auth/login`.
- Add Alembic for schema migrations — `Base.metadata.create_all()` only
  creates missing tables, it never alters existing ones.