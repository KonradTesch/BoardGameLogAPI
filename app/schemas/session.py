from .base import ResponseModel, RequestModel
from pydantic import model_validator
import datetime

class SessionPlayerResponse(ResponseModel):
    player_id: int
    player_name: str
    score: float
    winner: bool
    
    @model_validator(mode="before")
    @classmethod
    def extract_orm_player(cls, orm_player_relationship):
        if hasattr(orm_player_relationship, "player"):
            return {
                "player_id": orm_player_relationship.player_id,
                "player_name": orm_player_relationship.player.name,
                "score": orm_player_relationship.score,
                "winner": orm_player_relationship.winner
            }
        return orm_player_relationship

class GameSessionResponse(ResponseModel):
    id: int
    date: datetime.date
    game_id: int
    game_name: str
    session_players: list[SessionPlayerResponse]

    @model_validator(mode="before")
    @classmethod
    def extract_orm_game_name(cls, orm_session):
        if hasattr(orm_session, "game"):
            return {
                "id": orm_session.id,
                "date": orm_session.date,
                "game_id": orm_session.game_id,
                "game_name": orm_session.game.title,
                "session_players": orm_session.session_players
            }
        return orm_session

class SessionPlayerRequest(RequestModel):
    player_id: int
    score: float
    winner: bool

class GameSessionRequest(RequestModel):
    date: datetime.date
    game_id: int
    session_players: list[SessionPlayerRequest]





