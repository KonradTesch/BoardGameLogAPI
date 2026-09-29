from collections.abc import Sequence
from datetime import date, datetime
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.custom_exceptions import NotFoundException, UnprocessableException
from app.domain.session import GameSessionData
from app.models import Player, GameSession, SessionPlayer, BoardGame


def _validate_date(date_to_check: date) -> None:
    """
    Raises UnprocessableException if the date lies in the future
    """
    # Use the most advanced timezone (UTC+14) so no user's local "today" is rejected as future.
    latest_today = datetime.now(ZoneInfo("Pacific/Kiritimati")).date()
    if date_to_check > latest_today:
        raise UnprocessableException("Session date can't be in the future.")


class GameSessionRepository:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    def _own_game_sessions(self):
        return select(GameSession).where(GameSession.user_id == self.user_id)

    def create_session(self, session_data: GameSessionData) -> GameSession:
        """
        Creates a new game session
        """
        self._validate_session_data(session_data)

        new_session = GameSession(
            game_id=session_data.game_id,
            user_id=self.user_id,
            date=session_data.date,
            session_players=[
                SessionPlayer(player_id=sp.player_id, score=sp.score, winner=sp.winner)
                for sp in session_data.session_players
            ]
        )

        self.db.add(new_session)
        self.db.commit()

        return new_session

    def get_session(self, session_id: int) -> GameSession:
        """
        Gets the game session with the given id.
        """
        game_session = self.db.scalars(self._own_game_sessions()
                                       .where(GameSession.id == session_id)
                                       ).first()

        if not game_session:
            raise NotFoundException(f"Game Session {session_id} not found")

        return game_session

    def update_session(self, session_id: int, session_data: GameSessionData) -> GameSession:
        """
        Updates an existing game session
        """
        game_session = self.get_session(session_id)

        self._validate_session_data(session_data)

        game_session.game_id = session_data.game_id
        game_session.date = session_data.date

        players_before = {sp.player_id: sp for sp in game_session.session_players}

        for session_player in session_data.session_players:
            existing_player = players_before.pop(session_player.player_id, None)

            if existing_player is not None:
                existing_player.score = session_player.score
                existing_player.winner = session_player.winner
            else:
                new_player = SessionPlayer(
                    player_id=session_player.player_id,
                    score=session_player.score,
                    winner=session_player.winner
                )

                game_session.session_players.append(new_player)

        for removed_player in players_before.values():
            game_session.session_players.remove(removed_player)

        self.db.commit()

        return game_session

    def delete_session(self, session_id: int) -> None:
        """
        Deletes an existing game session with the given id.
        """
        session_to_delete = self.get_session(session_id)
        self.db.delete(session_to_delete)
        self.db.commit()

    def get_sessions_by_game(self, game_id: int) -> Sequence[GameSession]:
        """
        Gets all game_sessions with the given game from the given user.
        """
        game_sessions = self.db.scalars(
            self._own_game_sessions()
            .where(GameSession.game_id == game_id)
        ).all()

        return game_sessions

    def get_all_sessions(self) -> Sequence[GameSession]:
        """
        Gets all game sessions of the given user.
        """
        game_sessions = self.db.scalars(
            self._own_game_sessions()
        ).all()

        return game_sessions

    def _validate_session_data(self, session_data: GameSessionData) -> None:
        """
        Validates if the given session data is valid.
        """
        _validate_date(session_data.date)

        player_ids = [sp.player_id for sp in session_data.session_players]

        if len(set(player_ids)) != len(player_ids):
            raise UnprocessableException("Sessions can't have duplicate players.")

        self._validate_players(player_ids)

        self._validate_board_game(session_data.game_id)

    def _validate_players(self, player_ids: Sequence[int]) -> None:
        """
        Validates if the given players are existing and from the given user.
        """
        found_ids = self.db.scalars(select(Player.id)
                                    .where(Player.user_id == self.user_id)
                                    .where(Player.id.in_(player_ids))
                                    ).all()

        missing_ids = set(player_ids) - set(found_ids)

        if missing_ids:
            missing_string = ", ".join(str(i) for i in sorted(missing_ids))
            raise NotFoundException(f"Player not found: {missing_string}")

    def _validate_board_game(self, board_game_id: int) -> BoardGame:
        """
        Validates if the given board game id is existing and from the given user.
        """
        board_game = self.db.scalars(select(BoardGame)
                                     .where(BoardGame.id == board_game_id)
                                     .where(BoardGame.user_id == self.user_id)
                                     ).first()

        if not board_game:
            raise NotFoundException(f"Board game {board_game_id} not found")

        return board_game
