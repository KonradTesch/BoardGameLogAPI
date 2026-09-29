from app.models import BoardGame
from sqlalchemy import select
from collections.abc import Sequence
from sqlalchemy.orm import Session
from typing import Optional
from app.custom_exceptions import NotFoundException, UnprocessableException


class BoardGameRepository:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id: int = user_id

    def _own_games(self):
        return select(BoardGame).where(BoardGame.user_id == self.user_id)

    def create_board_game(self, game_title: str) -> BoardGame:
        if game_title == "":
            raise UnprocessableException(f"Board game title is empty.")

        existing_game = self.db.scalars(self._own_games()
            .where(BoardGame.title == game_title)
        ).first()
        if existing_game is not None:
            raise UnprocessableException(f"Board game '{game_title}' already exists")

        new_game = BoardGame(title=game_title, user_id=self.user_id)

        self.db.add(new_game)
        self.db.commit()

        return new_game


    def get_board_game(self, board_game_id:int,) -> BoardGame:
        board_game: Optional[BoardGame] = self.db.scalars(
            self._own_games()
            .where(BoardGame.id == board_game_id)
        ).first()

        if not board_game:
            raise NotFoundException(f"Board game '{board_game_id}' not found")

        return board_game


    def update_board_game_title(self, board_game_id:int, new_title:str) -> None:
        if new_title == "":
            raise UnprocessableException(f"Board game title is empty.")

        board_game = self.get_board_game(board_game_id)

        board_game.title = new_title

        self.db.commit()


    def delete_board_game(self, board_game_id:int) -> None:
        board_game = self.get_board_game(board_game_id)

        self.db.delete(board_game)
        self.db.commit()

    def get_all_games(self) -> Sequence[BoardGame]:
        user_games = self.db.scalars(
            self._own_games()
        ).all()

        return user_games



