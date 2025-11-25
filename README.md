# BoardGameLogAPI

A web application for tracking board game sessions, managing players, and analyzing game statistics. Built with FastAPI, SQLAlchemy, and Bootstrap.

## Features

- **User Management**: Secure user registration and authentication with JWT tokens
- **Session Tracking**: Log board game sessions with dates, players, scores, and winners
- **Player Management**: Create and manage players associated with your account
- **Statistics**: View detailed statistics for both players and games
  - Player stats: Total sessions, win rates, average scores, and best scores per game
  - Game stats: Session counts, best scores, and top players per game
- **Responsive UI**: Modern dark-themed interface built with Bootstrap 5

## Technologies

- **Backend**: FastAPI, SQLAlchemy, Alembic
- **Authentication**: JWT tokens with passlib and python-jose
- **Database**: PostgreSQL (configurable via environment variables)
- **Frontend**: Jinja2 templates, Bootstrap 5, vanilla JavaScript
- **Styling**: Custom CSS with dark theme

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/BoardGameLogAPI.git
cd BoardGameLogAPI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
```

4. Initialize the database:
```bash
alembic upgrade head
```

5. (Optional) Add default board games:
```bash
python repositories/db_add_boardgames.py
```

## Usage

1. Start the application:
```bash
python main.py
```

2. Open your browser and navigate to `http://localhost:8000`

3. Register a new account or log in

4. Start tracking your board game sessions!

## Project Structure

```
BoardGameLogAPI/
├── alembic/              # Database migrations
├── api_routes/           # API route handlers
│   ├── auth_router.py    # Authentication endpoints
│   ├── user_router.py    # User management endpoints
│   ├── player_router.py  # Player management endpoints
│   └── session_router.py # Session management endpoints
├── repositories/         # Database access layer
│   └── db_manager.py     # Data managers for entities
├── service/              # Business logic
│   ├── auth_logic.py     # JWT token handling
│   └── stats_calculator.py # Statistics calculations
├── static/               # Static assets (CSS)
├── templates/            # Jinja2 HTML templates
├── models.py             # SQLAlchemy models
├── custom_exceptions.py  # Custom exception classes
└── main.py              # Application entry point
```

## Database Schema

- **Users**: User accounts with authentication
- **Players**: Players associated with user accounts
- **Boardgames**: Available board games
- **Game_Session**: Individual game sessions
- **Session_Player**: Junction table linking sessions, players, scores, and winners

## API Endpoints

### Authentication
- `POST /auth/` - Register new user
- `POST /auth/token` - Login and receive access token

### User Management
- `GET /user/{user_id}` - User home page
- `PATCH /user/{user_id}` - Update username
- `PATCH /user/{user_id}/password` - Change password
- `DELETE /user/{user_id}` - Delete account
- `POST /user/{user_id}/logout` - Logout

### Sessions
- `GET /user/{user_id}/session/{session_id}` - View session details
- `POST /user/{user_id}/session/` - Create new session
- `PATCH /user/{user_id}/session/{session_id}` - Update session
- `DELETE /user/{user_id}/session/{session_id}` - Delete session

### Players
- `POST /user/{user_id}/player/` - Create new player
- `PATCH /user/{user_id}/player/` - Update player
- `DELETE /user/{user_id}/player/` - Delete player
- `GET /user/{user_id}/player/{player_id}/stats` - View player statistics

### Statistics
- `GET /user/{user_id}/stats/games` - View game statistics

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Konrad Tesch

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI powered by [Bootstrap 5](https://getbootstrap.com/)
- Icons from [Bootstrap Icons](https://icons.getbootstrap.com/)
