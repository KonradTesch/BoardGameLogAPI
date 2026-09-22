from dataclasses import dataclass
from datetime import date

@dataclass
class SessionPlayerData:
    player_id: int
    score: float
    winner: bool

@dataclass
class GameSessionData:
    date: date
    game_id: int
    session_players: list [SessionPlayerData]