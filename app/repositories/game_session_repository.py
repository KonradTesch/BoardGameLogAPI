from datetime import date
from sqlalchemy.orm import Session
from app.models import Player, GameSession, Session_Player
from app.custom_exceptions import NotFoundException


class GameSessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, game_id: int, user_id: int, date_value: date, players: list):
        new_session = GameSession(game_id=game_id, user_id=user_id, date=date_value)
        self.db.add(new_session)
        self.db.commit()
        self.db.refresh(new_session)

        for player in players:
            player_id = player["id"]
            if self.db.query(Player).filter(Player.id == player_id).count() == 0:
                raise NotFoundException("Player not found")

            new_session_player = Session_Player(
                session_id = new_session.id,
                player_id = player_id,
                score = player["score"],
                winner = player["winner"]
            )

            self.db.add(new_session_player)
            self.db.commit()

    def validate_session(self, session_id: int) -> GameSession:
        game_session = self.db.query(GameSession).filter(GameSession.id == session_id).first()

        if not game_session:
            raise NotFoundException("Game Session not found")

        return game_session

    def update_session(self, session_id: int, game_id: int, date_value: date, players: list):

        game_session = self.validate_session(session_id)

        game_session.game_id = game_id
        game_session.date = date_value

        session_players_before = self.db.query(Session_Player).filter(Session_Player.session_id == session_id).all()

        for player in players:
            player_id = player["player_id"]

            #current players
            session_player = self.db.query(Session_Player).filter(Session_Player.session_id == game_session.id).filter(Session_Player.player_id == player_id).first()

            if not session_player:
                new_session_player = Session_Player(
                    session_id = game_session.id,
                    player_id = player_id,
                    score = player["score"],
                    winner = player["winner"]
                )

                self.db.add(new_session_player)


            else:
                session_player.score = player["score"]
                session_player.winner = player["winner"]

                session_players_before.remove(session_player)

            if len(session_players_before) > 0:
                for session_player in session_players_before:
                    self.db.delete(session_player)
            self.db.commit()

    def delete_session(self, session_id: int):
        session_to_delete = self.validate_session(session_id)
        self.db.delete(session_to_delete)
        self.db.commit()

    def get_session_by_id(self, session_id: int) -> GameSession | None:
        game_session = self.db.query(GameSession).filter(GameSession.id == session_id).first()
        return game_session

    def get_user_game_session_by_game(self, user_id, game_id) -> list[GameSession]:
        game_sessions = (self.db.query(GameSession)
                      .filter(GameSession.game_id == game_id)
                      .filter(GameSession.user_id == user_id)
                      .all()
                         )

        return game_sessions

    def get_user_game_sessions_all(self, user_id) -> list[GameSession]:
        game_sessions = (self.db.query(GameSession)
                         .filter(GameSession.user_id == user_id)
                         .all()
                         )

        return game_sessions
