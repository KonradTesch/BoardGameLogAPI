from sqlalchemy import select, Sequence
from sqlalchemy.orm import Session
from app.models import User, Player, BoardGame, GameSession, SessionPlayer
from app.custom_exceptions import NotFoundException, UnprocessableException
from typing import Optional


class PlayerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_players(self, user_id: int) -> Sequence[Player]:
        players = self.db.scalars(
            select(Player).where(Player.user_id == user_id)
        ).all()

        return players

    def create_player(self, user_id: int, player_name: str) -> Player:
        user = self.db.scalars(select(User).where(User.id == user_id)).first()

        if not user:
            raise NotFoundException("User not found")

        for player in user.players:
            if player.name == player_name:
                raise UnprocessableException(f"Player name '{player.name}' already exists")

        new_player = Player(name=player_name, user_id=user_id)
        self.db.add(new_player)
        self.db.commit()

        return new_player

    def validate_player(self, player_id: int) -> Player:
        player: Optional[Player] = self.db.scalars(select(Player).where(Player.id == player_id)).first()

        if not player:
            raise NotFoundException("Player not found.")

        return player

    def update_player(self, user_id: int, player_id: int, new_name: str):
        user = self.db.scalars(select(User).where(User.id == user_id)).first()

        if not user:
            raise NotFoundException("User not found")

        for player in user.players:
            if player.id != player_id and player.name == new_name:
                raise UnprocessableException(f"Player name '{player.name}' already exists")

        player = self.validate_player(player_id)

        player.name = new_name
        self.db.commit()

    def delete_player(self, player_id: int):
        player_to_delete = self.validate_player(player_id)

        session_players = player_to_delete.session_players

        for session_player in session_players:
            session_player.session.deleted_players = True

        self.db.delete(player_to_delete)
        self.db.commit()

    def get_player_scores_for_game(self, player_id: int, game_id: int) -> Sequence[SessionPlayer]:
        player_scores = self.db.scalars(
            select(SessionPlayer)
            .join(SessionPlayer.session)
            .where(SessionPlayer.player_id == player_id)
            .where(GameSession.game_id == game_id)
        ).all()

        return player_scores

    def get_player_scores_all(self, player_id: int) -> Sequence[SessionPlayer]:
        player_scores = self.db.scalars(
            select(SessionPlayer)
            .where(SessionPlayer.player_id == player_id)
        ).all()

        return player_scores

    def get_player_games(self, player_id: int) -> Sequence[BoardGame]:
        player_games = self.db.scalars(
            select(BoardGame)
            .join(GameSession, BoardGame.sessions)
            .join(SessionPlayer, GameSession.session_players)
            .where(SessionPlayer.player_id == player_id)
            .distinct()
        ).all()

        return player_games
