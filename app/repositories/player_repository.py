from collections.abc import Sequence
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.custom_exceptions import NotFoundException, UnprocessableException
from app.models import User, Player, BoardGame, GameSession, SessionPlayer


class PlayerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_players(self, user_id: int) -> Sequence[Player]:
        players = self.db.scalars(
            select(Player).where(Player.user_id == user_id)
        ).all()

        return players

    def create_player(self, user_id: int, player_name: str) -> Player:
        player_already_exists = self.db.scalars(select(Player)
                                                .where(Player.user_id == user_id)
                                                .where(Player.name == player_name)
                                                ).first()

        if player_already_exists:
            raise UnprocessableException(f"Player name '{player_name}' already exists")

        new_player = Player(name=player_name, user_id=user_id)
        self.db.add(new_player)
        self.db.commit()

        return new_player

    def get_player(self, user_id, player_id: int) -> Player:
        player = self.db.scalars(select(Player)
                                 .where(Player.id == player_id)
                                 .where(Player.user_id == user_id)
                                 ).first()

        if not player:
            raise NotFoundException("Player not found.")

        return player

    def update_player(self, user_id: int, player_id: int, new_name: str) -> None:
        player_already_exists = self.db.scalars(select(Player)
                                                .where(Player.user_id == user_id)
                                                .where(Player.id != player_id)
                                                .where(Player.name == new_name)
                                                ).first()

        if player_already_exists:
            raise UnprocessableException(f"Player name '{new_name}' already exists")

        player = self.get_player(user_id,player_id)

        player.name = new_name
        self.db.commit()

    def delete_player(self, user_id: int, player_id: int) -> None:
        player_to_delete = self.get_player(user_id, player_id)

        session_players = player_to_delete.session_players

        for session_player in session_players:
            session_player.session.deleted_players = True

        self.db.delete(player_to_delete)
        self.db.commit()

    def get_player_scores_for_game(self, user_id: int, player_id: int, game_id: int) -> Sequence[SessionPlayer]:
        self.get_player(user_id, player_id)

        player_scores = self.db.scalars(
            select(SessionPlayer)
            .join(SessionPlayer.session)
            .where(SessionPlayer.player_id == player_id)
            .where(GameSession.game_id == game_id)
        ).all()

        return player_scores

    def get_player_scores_all(self, user_id: int, player_id: int) -> Sequence[SessionPlayer]:

        self.get_player(user_id, player_id)

        player_scores = self.db.scalars(
            select(SessionPlayer)
            .where(SessionPlayer.player_id == player_id)
        ).all()

        return player_scores

    def get_player_games(self, user_id: int, player_id: int) -> Sequence[BoardGame]:
        self.get_player(user_id, player_id)

        player_games = self.db.scalars(
            select(BoardGame)
            .join(GameSession, BoardGame.sessions)
            .join(SessionPlayer, GameSession.session_players)
            .where(SessionPlayer.player_id == player_id)
            .distinct()
        ).all()

        return player_games
