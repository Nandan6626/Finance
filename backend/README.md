# Finance Dashboard Backend

This project is a FastAPI backend for tracking financial records and building role-aware dashboard analytics.

The API supports:

- JWT-based login
- User lifecycle management
- Financial record CRUD
- Dashboard summaries and trends
## Design Approach
The codebase uses a layered module structure:
- routes -> controller -> service -> repository -> model
Why this split is used:
- routes: request/response contracts and dependencies
- controller: authorization and orchestration
- service: business rules
- repository: persistence/query logic
- model: SQLAlchemy entities

## Records Module

Location: `app/modules/records/`

Record schema fields:

- `amount`
- `type` (`income` or `expense`)
- `category`
- `date`
- `notes` (optional)

Supported operations:

- Create
- Read one
- Read list
- Update
- Delete

## Dashboard Module

Location: `app/modules/dashboard/`

Summary API returns:

- total income
- total expense
- net balance
- expense category breakdown
- monthly income/expense trends
- recent record activity

## Filters and Query Support

`GET /records/` supports:

- `type`
- `category`
- `date_from`
- `date_to`
- `search` (matches category/notes)
- `skip`
- `limit`

## Role-Based Access Rules

System roles:

- `viewer`
- `analyst`
- `admin`

Permissions:

- Viewer: records read-only, no dashboard access
- Analyst: records read-only, dashboard access allowed
- Admin: full records CRUD + dashboard + user administration

## API Reference

Auth:

- `POST /auth/login`
Users:
- `POST /users/` (public only for bootstrap, then admin-controlled)
- `GET /users/` (admin)
- `GET /users/me` (authenticated)
- `PATCH /users/{user_id}` (admin)

Records:
- `POST /records/` (admin)
- `GET /records/` (all authenticated roles)
- `GET /records/{record_id}` (all authenticated roles)
- `PATCH /records/{record_id}` (admin)
- `DELETE /records/{record_id}` (admin)
Dashboard:
- `GET /dashboard/` (analyst/admin)
- `GET /dashboard/external-data` (analyst/admin)

## Interactive Docs

FastAPI documentation endpoints:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Local Setup
1. Install packages:

```bash
pip install -r requirements.txt
```
2. Configure environment values (using the development template as a base):

- `SECRET_KEY`
- `DATABASE_URL`
- `CORS_ALLOW_ORIGINS`
- `APP_ENV`

3. Apply migrations:

```bash
alembic upgrade head
```

4. Run the server:

```bash
uvicorn app.main:app --reload
```
## Test Command

```bash
pytest -q
```

Covered test areas:

- login and user bootstrap flow
- records access control
- records filter behavior
- dashboard totals and role gating
- external API mocking path

## Project Assumptions

- Amounts are currently stored as `float`.
- Analysts can read organization-wide records for reporting.
- Viewers are restricted to their own records.
- Initial user bootstrap is intentionally open for first-run setup.


