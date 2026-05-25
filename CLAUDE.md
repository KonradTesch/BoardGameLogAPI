# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BoardGameLogAPI is a board game session tracker with two frontends:
- **Legacy**: Jinja2 server-rendered HTML templates (still present, being phased out)
- **Active**: React/TypeScript SPA in `react/boardgame_api/`

The backend is a FastAPI app running on port 8000. The React dev server runs on port 5173 and proxies `/api/*` requests to the FastAPI backend (stripping the `/api` prefix).

## Commands

### Backend (FastAPI)

Run from the project root with the `.venv` activated:

```bash
source .venv/bin/activate
python app/main.py          # starts uvicorn on :8000 with reload
```

Database migrations:
```bash
alembic upgrade head        # apply all migrations
alembic revision --autogenerate -m "description"  # create new migration
```

Populate default boardgames:
```bash
python app/repositories/db_add_boardgames.py
```

### Frontend (React)

```bash
cd react/boardgame_api
npm install
npm run dev     # dev server on :5173
npm run build   # type-check + vite build
npm run lint    # eslint
```

### Environment

Requires a `.env` file in the project root:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
```

## Architecture

### Backend layers

```
app/
├── main.py              # FastAPI app setup, CORS, router registration
├── models.py            # SQLAlchemy ORM models (User, Player, Boardgame, Game_Session, Session_Player)
├── custom_exceptions.py # NotFoundException, UnauthorizedException, UnprocessableException
├── api_routes/          # FastAPI routers (thin: parse request, call manager, return response)
├── repositories/
│   └── db_manager.py    # Data managers: UserDataManager, PlayerDataManager, GameDataManager
│                        # Single shared SQLAlchemy session (module-level — not per-request)
└── service/
    ├── auth_logic.py    # JWT encode/decode; get_current_user()
    └── stats_calculator.py
```

**Auth flow**: JWT is stored as an `httponly` cookie (`access_token`). Each protected route injects the `user_dependency` (defined per-router via `Depends(get_user)`), which decodes the cookie and returns `{"name": str, "id": int}`.

**Exception handling**: Routers catch the three custom exceptions from `custom_exceptions.py` and re-raise them as `HTTPException` with appropriate status codes.

**Database session**: `db_manager.py` uses a single module-level `SessionLocal()` instance shared across all data managers. This is not thread-safe for production but works for the current single-threaded dev setup.

### React frontend (`react/boardgame_api/src/`)

```
context/AuthContext.tsx   # Global auth state: user (User | null) + isLoading
layout/AppAuth.tsx        # On mount: calls GET /api/auth/user, populates AuthContext
layout/AppContent.tsx     # Route definitions (react-router-dom v7)
pages/                    # Page-level components (LoginPage, DashboardPage, AccountSettingsPage)
components/               # Reusable UI components (all use Bootstrap 5)
types/                    # TypeScript types (User, BootstrapVariant, InfoText)
util/util.ts              # Shared utilities
```

**Auth pattern**: `AppAuth` runs once on app load to check the cookie-backed session via `GET /api/auth/user`. It sets `AuthContext.user` if authenticated. Pages read from `AuthContext` to determine the logged-in user rather than decoding the JWT themselves.

**API calls**: All frontend requests go to `/api/*`, which Vite proxies to `http://127.0.0.1:8000` with the `/api` prefix stripped. In production, this proxy must be replicated (e.g., nginx).

### Database schema

- `users` → `players` (one-to-many, user owns players)
- `users` → `sessions` (one-to-many, user owns sessions)
- `boardgames` → `sessions` (one-to-many)
- `sessions` ↔ `players` via `sessions_players` junction table (adds `score`, `winner`)
