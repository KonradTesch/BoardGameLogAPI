from datetime import date
from sqlalchemy import select, Sequence
from sqlalchemy.orm import Session
from app.domain.session import GameSessionData
from app.models import Player, GameSession, SessionPlayer
from app.custom_exceptions import NotFoundException



class GameSessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, session: GameSessionData) -> GameSession:
        new_session = GameSession(game_id=session.game_id, user_id=session.user_id, date=session.date)
        self.db.add(new_session)
        self.db.flush()

        for player in session.session_players:
            player_exists = self.db.scalars(select(Player).where(Player.id == player.player_id)).first()
            if player_exists is None:
                raise NotFoundException(f"Player not found")

            new_session_player = SessionPlayer(
                session_id = new_session.id,
                player_id = player.player_id,
                score = player.score,
                winner = player.winner
            )

            self.db.add(new_session_player)

        self.db.commit()

        return new_session

    def validate_session(self, session_id: int) -> GameSession:
        game_session = self.db.scalars(select(GameSession).where(GameSession.id == session_id)).first()

        if not game_session:
            raise NotFoundException("Game Session not found")

        return game_session

    def update_session(self, session_id: int, session_data: GameSessionData) -> GameSession:

        game_session = self.validate_session(session_id)

        game_session.game_id = session_data.game_id
        game_session.date = session_data.date

        session_players_before = list(self.db.scalars(
            select(SessionPlayer).where(SessionPlayer.session_id == session_id)
        ).all())

        for player in session_data.session_players:
            player_id = player.player_id

            #current players
            session_player = self.db.scalars(
                select(SessionPlayer)
                .where(SessionPlayer.session_id == game_session.id)
                .where(SessionPlayer.player_id == player_id)
            ).first()

            if not session_player:
                new_session_player = SessionPlayer(
                    session_id = game_session.id,
                    player_id = player_id,
                    score = player.score,
                    winner = player.winner
                )

                self.db.add(new_session_player)


            else:
                session_player.score = player.score
                session_player.winner = player.winner

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
        game_session = self.db.scalars(select(GameSession).where(GameSession.id == session_id)).first()
        return game_session

    def get_user_game_session_by_game(self, user_id, game_id) -> Sequence[GameSession]:
        game_sessions = self.db.scalars(
            select(GameSession)
            .where(GameSession.game_id == game_id)
            .where(GameSession.user_id == user_id)
        ).all()

        return game_sessions

    def get_user_game_sessions_all(self, user_id) -> Sequence[GameSession]:
        game_sessions = self.db.scalars(
            select(GameSession)
            .where(GameSession.user_id == user_id)
        ).all()

        return game_sessions
