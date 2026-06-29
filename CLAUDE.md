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
├── database.py          # Engine, SessionLocal, get_db() per-request session dependency
├── models.py            # SQLAlchemy ORM models (User, Player, BoardGame, GameSession, Session_Player)
├── custom_exceptions.py # NotFoundException, UnauthorizedException, UnprocessableException
├── api_routes/          # FastAPI routers (thin: parse request, inject repos, return response)
│   ├── index_router.py        # /login, /register redirects + shared check_user() helper
│   ├── auth_router.py         # /auth (register, token/login, user, logout cookie handling)
│   ├── user_router.py         # /user/{user_id} (account, username, password, delete)
│   ├── session_router.py      # /user/{user_id}/sessions
│   ├── player_router.py       # /user/{user_id}/players
│   └── board_game_router.py   # /user/{user_id}/board-games
├── repositories/        # One repository class per aggregate, each takes a db Session
│   ├── user_repository.py         # UserRepository
│   ├── player_repository.py       # PlayerRepository
│   ├── board_game_repository.py   # BoardGameRepository
│   └── game_session_repository.py # GameSessionRepository
├── schemas/             # Pydantic request/response models (camelCase API contract)
│   ├── base.py          # RequestModel / ResponseModel base configs
│   ├── auth.py, user.py, board_games.py, sessions.py
└── service/
    ├── auth_logic.py    # JWT encode/decode; create_access_token(); get_current_user()
    └── stats_calculator.py  # Player/game stats, computed over repository queries
```

**Repository pattern**: Each repository is a class constructed with a per-request SQLAlchemy `Session` (`def __init__(self, db: Session)`). Repositories own all query/commit logic; routers stay thin. There is no longer a shared module-level session or `db_manager.py`.

**Dependency injection**: `database.get_db()` is a generator dependency that yields a fresh `SessionLocal()` per request and closes it afterward. Each router defines small factory functions (e.g. `get_user_repo(db = Depends(get_db))`) and exposes them as `Annotated[Repository, Depends(...)]` aliases (e.g. `user_repo_dependency`). Routes declare these aliases as parameters to receive a request-scoped repository. This replaces the previous single-threaded shared session and is request-safe.

**Auth flow**: JWT is stored as an `httponly` cookie (`access_token`). Each protected route injects `user_dependency` (defined per-router via `Depends(get_user)`), which decodes the cookie via `get_current_user()` and returns `{"name": str, "id": int}`. Routers call the shared `check_user(user_id, current_user)` helper (in `index_router.py`) to enforce that the path `user_id` matches the authenticated user, raising 403 otherwise.

**Schemas / API contract**: `schemas/base.py` defines `RequestModel` and `ResponseModel`, both using `alias_generator=to_camel` + `populate_by_name`. `ResponseModel` also sets `from_attributes=True` so ORM objects serialize directly. **The JSON API is therefore camelCase** (e.g. `boardGameId`, `userId`), while Python/ORM fields stay snake_case. Some response schemas (`schemas/sessions.py`) use `@model_validator(mode="before")` to flatten ORM relationships (e.g. derive `game_name` from `session.game.title`, build `players` from `session_players`).

**Exception handling**: Routers catch the three custom exceptions from `custom_exceptions.py` and re-raise them as `HTTPException` with appropriate status codes.

**Legacy endpoints**: Some routes still render Jinja2 templates (`TemplateResponse`) — e.g. `user_home`, `session_details`, and the stats pages — alongside the JSON endpoints the React SPA consumes. The `templates/` directory and these handlers remain while the legacy frontend is phased out.

### React frontend (`react/boardgame_api/src/`)

```
context/AuthContext.tsx     # Global auth state: user (User | null) + isLoading
context/UserDataContext.tsx # Per-user domain state: boardGames[] + players[] with add/remove helpers
layout/AppAuth.tsx          # On mount: calls GET /api/auth/user, populates AuthContext
layout/AppContent.tsx       # Route definitions (react-router-dom v7), driven by ROUTES
pages/                      # LoginPage, DashboardPage, AccountSettingsPage, EditSessionPage
components/                 # Reusable UI grouped by kind: Button/, Cards/, Dropdowns/,
                            #   Lists/, Modals/, Text/, plus top-level (all use Bootstrap 5)
types/                      # TS types (User, BoardGame, GameSession, Player, etc.) + routes.ts
util/util.ts                # Shared utilities
```

**Provider nesting** (`App.tsx`): `AuthProvider` → `UserDateProvider` → `BrowserRouter` → `AppAuth` + `AppContent`.

**Auth pattern**: `AppAuth` runs once on app load to check the cookie-backed session via `GET /api/auth/user`. It sets `AuthContext.user` if authenticated. Pages read from `AuthContext` to determine the logged-in user rather than decoding the JWT themselves.

**Routes**: `types/routes.ts` centralizes route definitions as a `ROUTES` object. Each entry has a `path` (the route pattern, e.g. `/user/:userId/dashboard`) and a `to` helper (a function or string for building links). Use these instead of hardcoding paths.

**API calls**: All frontend requests go to `/api/*`, which Vite proxies to `http://127.0.0.1:8000` with the `/api` prefix stripped. In production, this proxy must be replicated (e.g., nginx). Note the backend API is camelCase (see Schemas above).

### Database schema

- `users` → `players` (one-to-many, user owns players)
- `users` → `sessions` (one-to-many, user owns sessions)
- `users` → `boardgames` (one-to-many, user owns board games — `boardgames.user_id`)
- `boardgames` → `sessions` (one-to-many)
- `sessions` ↔ `players` via `sessions_players` junction table (adds `score`, `winner`; `GameSession.session_players` cascades delete-orphan)
