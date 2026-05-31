from .base import ResponseModel
from pydantic import model_validator
import datetime

class SessionPlayer(ResponseModel):
    name: str
    score: int
    winner: bool
    
    @model_validator(mode="before")
    @classmethod
    def extract_orm_player(cls, orm_player_relationship):
        if hasattr(orm_player_relationship, "player"):
            return {
                "name": orm_player_relationship.player.name,
                "score": orm_player_relationship.score,
                "winner": orm_player_relationship.winner
            }
        return orm_player_relationship

class GameSession(ResponseModel):
    date: datetime.date
    game_name: str
    players: list[SessionPlayer]

    @model_validator(mode="before")
    @classmethod
    def extract_orm_game_name(cls, orm_session):
        if hasattr(orm_session, "game"):
            return {
                "date": orm_session.date,
                "game_name": orm_session.game.title,
                "players": orm_session.session_players
            }
        return orm_session


