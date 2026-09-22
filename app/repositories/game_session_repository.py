from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.domain.session import GameSessionData
from app.models import Player, GameSession, SessionPlayer, BoardGame
from app.custom_exceptions import NotFoundException



class GameSessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, user_id: int, session_data: GameSessionData) -> GameSession:
        new_session = GameSession(game_id=session_data.game_id, user_id=user_id, date=session_data.date)

        self._validate_board_game(user_id, session_data.game_id)

        self.db.add(new_session)
        self.db.flush()

        for session_player in session_data.session_players:
            self._validate_player(user_id, session_player.player_id)

            new_session_player = SessionPlayer(
                session_id = new_session.id,
                player_id = session_player.player_id,
                score = session_player.score,
                winner = session_player.winner
            )

            self.db.add(new_session_player)

        self.db.commit()

        return new_session

    def validate_session(self, user_id: int, session_id: int) -> GameSession:
        game_session = self.db.scalars(select(GameSession)
                                       .where(GameSession.id == session_id)
                                       .where(GameSession.user_id == user_id)).first()

        if not game_session:
            raise NotFoundException(f"Game Session {session_id} not found")

        return game_session

    def _validate_player(self, user_id: int, player_id: int) -> Player:
        player = self.db.scalars(select(Player)
                                 .where(Player.id == player_id)
                                 .where(Player.user_id == user_id)
                                 ).first()

        if not player:
            raise NotFoundException(f"Player {player_id} not found")

        return player

    def _validate_board_game(self, user_id: int, board_game_id: int) -> BoardGame:
        board_game = self.db.scalars(select(BoardGame)
                                           .where(BoardGame.id == board_game_id)
                                           .where(BoardGame.user_id == user_id)
                                           ).first()

        if not board_game:
            raise NotFoundException(f"Board game {board_game_id} not found")

        return board_game


    def update_session(self, user_id: int, session_id: int, session_data: GameSessionData) -> GameSession:
        game_session = self.validate_session(user_id, session_id)

        self._validate_board_game(user_id, session_data.game_id)

        game_session.game_id = session_data.game_id
        game_session.date = session_data.date

        session_players_before = list(self.db.scalars(
            select(SessionPlayer).where(SessionPlayer.session_id == session_id)
        ).all())

        for player in session_data.session_players:
            self._validate_player(user_id, player.player_id)

            session_player = self.db.scalars(
                select(SessionPlayer)
                .where(SessionPlayer.session_id == game_session.id)
                .where(SessionPlayer.player_id == player.player_id)
            ).first()

            if not session_player:
                new_session_player = SessionPlayer(
                    session_id = game_session.id,
                    player_id = player.player_id,
                    score = player.score,
                    winner = player.winner
                )

                self.db.add(new_session_player)

            else:
                session_player.score = player.score
                session_player.winner = player.winner

                session_players_before.remove(session_player)

        for session_player in session_players_before:
            self.db.delete(session_player)


        self.db.commit()

        return game_session

    def delete_session(self, user_id: int, session_id: int):
        session_to_delete = self.validate_session(user_id, session_id)
        self.db.delete(session_to_delete)
        self.db.commit()

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
