from sqlalchemy.orm import Session
from app.models import User, Player, BoardGame, GameSession, Session_Player
from app.custom_exceptions import NotFoundException, UnprocessableException
from typing import Optional, cast


class PlayerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_players(self, user_id: int) -> list[Player]:
        players = cast(list[Player], self.db.query(Player).filter(Player.user_id == user_id).all())

        return players

    def create_player(self, user_id, player_name:str) -> Player:
        if self.db.query(Player).filter(Player.name == player_name).first() is not None:
            raise UnprocessableException(f"Player {player_name} already exists.")

        new_player = Player(name=player_name, user_id=user_id)
        self.db.add(new_player)
        self.db.commit()

        return new_player

    def validate_player(self, player_id:int) -> Player:
        player: Optional[Player] = self.db.query(Player).filter(Player.id == player_id).first()

        if not player:
            raise NotFoundException("Player not found.")

        return player

    def update_player(self, user_id: int, player_id: int, new_name: str):
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise NotFoundException("User not found")

        for player in user.players:
            if player.id != player_id and player.name == new_name:
                raise UnprocessableException(f"Player name '{player.name}' already exists")

        player = self.validate_player(player_id)

        player.name = new_name
        self.db.commit()

    def delete_player(self, player_id: int) -> bool:
        player_to_delete = self.db.query(Player).filter(Player.id == player_id)
        if player_to_delete:
            player_to_delete.delete()
            self.db.commit()
            return True
        return False

    def get_player_scores_for_game(self, player_id: int, game_id: int) -> list[Session_Player]:
        player_scores = cast(list[Session_Player] ,(self.db.query(Session_Player)
                         .join(Session_Player.session)
                         .filter(Session_Player.player_id == player_id)
                         .filter(GameSession.game_id == game_id)
                         .all()
                         ))

        return player_scores

    def get_player_scores_all(self, player_id: int) -> list[Session_Player]:
        player_scores = cast(list[Session_Player] ,(self.db.query(Session_Player)
                         .filter(Session_Player.player_id == player_id)
                         .all()
                         ))

        return player_scores

    def get_player_games(self, player_id: int) -> list[BoardGame]:
        player_games = cast(list[BoardGame] ,(self.db.query(BoardGame)
                        .join(GameSession, BoardGame.sessions)
                        .join(Session_Player, GameSession.session_players)
                        .filter(Session_Player.player_id == player_id)
                        .distinct()
                        .all()
                        ))

        return player_games
