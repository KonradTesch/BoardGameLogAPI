# BoardGameLogAPI

A web application for tracking board game sessions, managing players and board games, and analyzing game statistics. It consists of a JSON-only **FastAPI** backend and a **React/TypeScript** single-page frontend.

## Features

- **User Management**: Registration, login/logout, change username and password, delete account
- **Secure Authentication**: JWT stored in an `httponly` cookie
- **Session Tracking**: Log board game sessions with dates, players, scores, and winners
- **Player Management**: Create, rename, and delete players associated with your account
- **Board Game Management**: Maintain your own collection of board games
- **Statistics**: Player and game statistics (sessions played, win rates, average and best scores)
- **Responsive UI**: React frontend styled with Bootstrap 5

## Technologies

- **Backend**: FastAPI, SQLAlchemy 2, Alembic, Pydantic v2 / pydantic-settings, psycopg 3
- **Authentication**: JWT via python-jose, password hashing with bcrypt
- **Database**: PostgreSQL 16 (provided via Docker Compose)
- **Frontend**: React 19, TypeScript, Vite, react-router-dom v7, Bootstrap 5, Bootstrap Icons
- **Testing**: pytest, httpx, testcontainers

## Installation

### Prerequisites

- Python 3.13+
- Node.js (LTS) and npm
- Docker (for the database and the test suite)

### 1. Clone the repository

```bash
git clone https://github.com/KonradTesch/BoardGameLogAPI.git
cd BoardGameLogAPI
```

### 2. Create a `.env` file in the project root

```env
# Database (used by the backend and Alembic)
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/dbname

# Postgres container (used by compose.yaml)
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=dbname

# Auth
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
# Optional (defaults shown)
ACCESS_TOKEN_EXPIRE_DAYS=7
TOKEN_RENEW_AFTER_HOURS=24
```

### 3. Start the database

```bash
docker compose up -d
```

### 4. Set up the backend

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # or requirements-dev.txt to include test tools
alembic upgrade head
```

### 5. Set up the frontend

```bash
cd react/boardgame_api
npm install
```

## Usage

1. Start the backend (port 8000, interactive API docs at `http://localhost:8000/docs`):
   ```bash
   python app/main.py
   ```

2. Start the frontend dev server:
   ```bash
   cd react/boardgame_api
   npm run dev
   ```

3. Open `http://localhost:5173`, register an account or log in, and start tracking your sessions.

The Vite dev server proxies all requests to `/api/*` to `http://127.0.0.1:8000`, stripping the `/api` prefix. In production this proxy must be replicated (e.g. with nginx).

### Other frontend commands

```bash
npm run build   # type-check + production build
npm run lint    # eslint
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

- `tests/unit/` – repository tests
- `tests/integration/` – router tests via the FastAPI test client

The tests spin up a temporary PostgreSQL database with testcontainers, so Docker must be running.

## Project Structure

```
BoardGameLogAPI/
├── app/
│   ├── main.py                 # FastAPI app, CORS, router registration
│   ├── config.py               # Settings loaded from .env
│   ├── database.py             # Engine, SessionLocal, get_db() dependency
│   ├── models.py               # SQLAlchemy ORM models
│   ├── custom_exceptions.py    # Custom exception classes
│   ├── api_routes/             # FastAPI routers + shared dependencies
│   ├── domain/                 # Plain dataclasses passed between layers
│   ├── repositories/           # One repository class per aggregate
│   ├── schemas/                # Pydantic request/response models (camelCase)
│   └── service/                # JWT handling, statistics
├── alembic/                    # Database migrations
├── tests/
│   ├── unit/
│   └── integration/
├── react/boardgame_api/        # React/TypeScript frontend
│   └── src/
│       ├── context/            # Auth and user data contexts
│       ├── layout/             # App auth check and route definitions
│       ├── pages/              # Login, Dashboard, Account Settings, Edit Session
│       ├── components/         # Reusable UI components
│       ├── types/              # TypeScript types and route definitions
│       └── util/               # Shared utilities
├── compose.yaml                # PostgreSQL service
├── requirements.txt
└── requirements-dev.txt
```

## Architecture

- **Thin routers, repository pattern**: Routers parse requests and delegate to repository classes. Each repository receives a request-scoped SQLAlchemy session via the `get_db()` dependency.
- **camelCase API**: Request/response schemas (`app/schemas/base.py`) use camelCase aliases (e.g. `boardGameId`), while Python code stays snake_case.
- **Auth**: The JWT is set as an `httponly` cookie (`access_token`). Protected routes verify that the `user_id` in the path matches the authenticated user and return `403` otherwise.

## Database Schema

- **users**: User accounts
- **players**: Players owned by a user
- **boardgames**: Board games owned by a user
- **sessions**: Game sessions owned by a user, each referencing a board game
- **sessions_players**: Junction table linking sessions and players, with `score` and `winner`

## API Endpoints

All endpoints exchange JSON in camelCase. Protected endpoints require the `access_token` cookie.

### Authentication (`/auth`)
- `POST /auth/register` – Register a new user
- `POST /auth/login` – Log in and set the auth cookie
- `GET /auth/user` – Get the currently authenticated user
- `POST /auth/logout` – Log out and clear the auth cookie

### User (`/user`)
- `PATCH /user/{user_id}/username` – Change username
- `PATCH /user/{user_id}/password` – Change password
- `DELETE /user/{user_id}` – Delete account
- `GET /user/{user_id}/boardgames/stats` – Board game statistics

### Sessions (`/user/{user_id}/sessions`)
- `GET /` – List sessions
- `POST /` – Create a session
- `PATCH /{session_id}` – Update a session
- `DELETE /{session_id}` – Delete a session

### Players (`/user/{user_id}/players`)
- `GET /` – List players
- `POST /` – Create a player
- `PATCH /{player_id}` – Update a player
- `DELETE /{player_id}` – Delete a player

### Board Games (`/user/{user_id}/board-games`)
- `GET /` – List board games
- `POST /` – Create a board game
- `PATCH /{board_game_id}` – Update a board game
- `DELETE /{board_game_id}` – Delete a board game

## License

This project is open source and available under the MIT License.

## Author

Konrad Tesch

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) and [React](https://react.dev/)
- Bundled with [Vite](https://vite.dev/)
- UI powered by [Bootstrap 5](https://getbootstrap.com/)
- Icons from [Bootstrap Icons](https://icons.getbootstrap.com/)
