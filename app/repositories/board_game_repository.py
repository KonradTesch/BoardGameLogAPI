from app.models import BoardGame
from sqlalchemy import select, Sequence
from sqlalchemy.orm import Session
from typing import Optional
from app.custom_exceptions import NotFoundException, UnprocessableException


class BoardGameRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_board_game(self, game_title: str, user_id:int ) -> BoardGame:
        existing_game = self.db.scalars(
            select(BoardGame)
            .where(BoardGame.title == game_title)
            .where(BoardGame.user_id == user_id)
        ).first()
        if existing_game is not None:
            raise UnprocessableException(f"Board game '{game_title}' already exists")

        new_game = BoardGame(title=game_title, user_id=user_id)
        self.db.add(new_game)
        self.db.commit()

        return new_game


    def validate_board_game(self, board_game_id:int, user_id:int) -> BoardGame:
        board_game: Optional[BoardGame] = self.db.scalars(
            select(BoardGame)
            .where(BoardGame.id == board_game_id)
            .where(BoardGame.user_id == user_id)
        ).first()

        if not board_game:
            raise NotFoundException(f"Board game '{board_game_id}' not found")

        return board_game


    def delete_board_game(self, board_game_id:int, user_id:int):
        board_game = self.validate_board_game(board_game_id, user_id)

        self.db.delete(board_game)
        self.db.commit()

    def get_user_games(self, user_id: int) -> Sequence[BoardGame]:
        user_games = self.db.scalars(
            select(BoardGame)
            .where(BoardGame.user_id == user_id)
        ).all()

        return user_games



