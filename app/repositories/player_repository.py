from sqlalchemy.orm import Session
from app.models import User, Player, BoardGame, GameSession, Session_Player
from app.custom_exceptions import NotFoundException, UnprocessableException


class PlayerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_player(self, user:User, player_name:str):
        new_player = Player(name=player_name, user_id=user.id)
        self.db.add(new_player)
        self.db.commit()

    def validate_player(self, player_id:int) -> Player:
        player = self.db.query(Player).filter(Player.id == player_id).first()

        if not player:
            raise NotFoundException("Player not found")

        return player

    def get_player_by_id(self, player_id: int) -> Player:
        player = self.validate_player(player_id)
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
        player_scores = (self.db.query(Session_Player)
                         .join(Session_Player.session)
                         .filter(Session_Player.player_id == player_id)
                         .filter(GameSession.game_id == game_id)
                         .all()
                         )

        return player_scores

    def get_player_scores_all(self, player_id: int) -> list[Session_Player]:
        player_scores = (self.db.query(Session_Player)
                         .filter(Session_Player.player_id == player_id)
                         .all()
                         )

        return player_scores

    def get_player_games(self, player_id: int) -> list[BoardGame]:
        player_games = (self.db.query(BoardGame)
                        .join(GameSession, BoardGame.sessions)
                        .join(Session_Player, GameSession.session_players)
                        .filter(Session_Player.player_id == player_id)
                        .distinct()
                        .all()
                        )

        return player_games
