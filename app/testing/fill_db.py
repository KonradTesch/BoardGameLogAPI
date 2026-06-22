"""
Seed script: adds players, boardgames, and sessions for user 'Konrad'.
Run from project root with .venv active:
    python app/repositories/db_seed_konrad.py
"""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Player, BoardGame, GameSession, Session_Player

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

user = db.query(User).filter(User.username == "Konrad").first()
if not user:
    print("User 'Konrad' not found. Please register first.")
    sys.exit(1)

print(f"Found user: {user.username} (id={user.id})")

# Players
player_names = ["Anna", "Ben", "Clara"]
players = []
for name in player_names:
    existing = db.query(Player).filter(Player.name == name, Player.user_id == user.id).first()
    if existing:
        print(f"Player '{name}' already exists, skipping.")
        players.append(existing)
    else:
        p = Player(name=name, user_id=user.id)
        db.add(p)
        db.commit()
        db.refresh(p)
        players.append(p)
        print(f"Created player: {name}")

# Boardgames
game_defs = [
    ("Catan", 3, 4),
    ("Ticket to Ride", 2, 5),
    ("Pandemic", 2, 4),
]
games = []
for title, min_p, max_p in game_defs:
    existing = db.query(BoardGame).filter(BoardGame.title == title, BoardGame.user_id == user.id).first()
    if existing:
        print(f"Boardgame '{title}' already exists, skipping.")
        games.append(existing)
    else:
        g = BoardGame(title=title, min_players=min_p, max_players=max_p, user_id=user.id)
        db.add(g)
        db.commit()
        db.refresh(g)
        games.append(g)
        print(f"Created boardgame: {title}")

anna, ben, clara = players
catan, ticket, pandemic = games

sessions_data = [
    {
        "game": catan,
        "date": date(2026, 5, 10),
        "players": [
            {"player": anna,  "score": 10, "winner": True},
            {"player": ben,   "score": 8,  "winner": False},
            {"player": clara, "score": 7,  "winner": False},
        ],
    },
    {
        "game": ticket,
        "date": date(2026, 5, 17),
        "players": [
            {"player": ben,   "score": 145, "winner": True},
            {"player": clara, "score": 130, "winner": False},
        ],
    },
    {
        "game": pandemic,
        "date": date(2026, 5, 24),
        "players": [
            {"player": anna,  "score": 0, "winner": True},
            {"player": clara, "score": 0, "winner": True},
        ],
    },
    {
        "game": catan,
        "date": date(2026, 6, 1),
        "players": [
            {"player": anna,  "score": 9,  "winner": False},
            {"player": ben,   "score": 12, "winner": True},
            {"player": clara, "score": 6,  "winner": False},
        ],
    },
    {
        "game": ticket,
        "date": date(2026, 6, 14),
        "players": [
            {"player": anna,  "score": 118, "winner": False},
            {"player": ben,   "score": 102, "winner": False},
            {"player": clara, "score": 155, "winner": True},
        ],
    },
]

for s_data in sessions_data:
    gs = GameSession(game_id=s_data["game"].id, user_id=user.id, date=s_data["date"])
    db.add(gs)
    db.commit()
    db.refresh(gs)

    for p_data in s_data["players"]:
        sp = Session_Player(
            session_id=gs.id,
            player_id=p_data["player"].id,
            score=p_data["score"],
            winner=p_data["winner"],
        )
        db.add(sp)
    db.commit()
    print(f"Created session: {s_data['game'].title} on {s_data['date']}")

print("\nSeed complete.")