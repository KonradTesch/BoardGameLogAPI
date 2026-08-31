from dataclasses import dataclass
from datetime import datetime


@dataclass
class SessionPlayerData:
    player_id: int
    score: float
    winner: bool

@dataclass
class GameSessionData:
    id: int
    date: datetime.date
    game_id: int
    session_players: list [SessionPlayerData]