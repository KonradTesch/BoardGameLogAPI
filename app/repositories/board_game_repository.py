from app.models import BoardGame
from sqlalchemy.orm import Session
from typing import Optional, cast
from app.custom_exceptions import NotFoundException, UnprocessableException


class BoardGameRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_board_game(self, game_title: str,min_players: int, max_players:int, user_id:int ):
        if (self.db.query(BoardGame)
                .filter(BoardGame.title == game_title)
                .filter(BoardGame.user_id == user_id)
                .count() > 0):
            raise UnprocessableException(f"Board game '{game_title}' already exists")

        new_game = BoardGame(title=game_title, min_players=min_players, max_players=max_players, user_id=user_id)
        self.db.add(new_game)
        self.db.commit()


    def validate_board_game(self, board_game_id:int, user_id:int) -> BoardGame:
        board_game: Optional[BoardGame] = (self.db.query(BoardGame)
                      .filter(BoardGame.id == board_game_id)
                      .filter(BoardGame.user_id == user_id)
                      .first())

        if not board_game:
            raise NotFoundException(f"Board game '{board_game_id}' not found")

        return board_game


    def delete_board_game(self, board_game_id:int, user_id:int):
        board_game = self.validate_board_game(board_game_id, user_id)

        self.db.delete(board_game)
        self.db.commit()

    def get_user_games(self, user_id: int) -> list[BoardGame]:
        user_games = cast(list[BoardGame], (self.db.query(BoardGame)
                      .filter(BoardGame.user_id == user_id)
                      .all()))

        return user_games



