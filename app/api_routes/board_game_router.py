from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from .index_router import check_user
from app.custom_exceptions import UnprocessableException, NotFoundException
from .user_router import user_dependency
from app.database import get_db
from app.repositories.board_game_repository import BoardGameRepository
from typing import Annotated
from app.schemas.board_games import BoardGameResponse, AddBoardGameRequest, EditBoardGameRequest

router = APIRouter(
    prefix="/user/{user_id}/board-games",
    tags=["board-games"]
)

def get_board_game_repo(db: Session = Depends(get_db)):  # get_db bekannt durch Import
    return BoardGameRepository(db)

board_game_repo_dependency = Annotated[BoardGameRepository, Depends(get_board_game_repo)]

@router.post("/", response_model=BoardGameResponse, status_code=status.HTTP_201_CREATED)
def create_board_game(user_id: int, current_user:user_dependency, board_game: AddBoardGameRequest, repo: board_game_repo_dependency):
    try:
        check_user(user_id, current_user)

        new_board_game = repo.create_board_game(board_game.title, user_id)

        return new_board_game

    except UnprocessableException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))


@router.get("/", response_model=list[BoardGameResponse], response_model_by_alias=True)
def get_board_games(user_id: int, current_user: user_dependency, repo: board_game_repo_dependency):
    check_user(user_id, current_user)
    board_games = repo.get_user_games(user_id)

    return board_games

@router.delete("/{board_game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board_game(user_id: int, board_game_id: int , current_user:user_dependency, repo: board_game_repo_dependency, ):
    try:
        check_user(user_id, current_user)

        repo.delete_board_game(board_game_id, user_id)

    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch("/{board_game_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_board_game(user_id: int, board_game_id: int, current_user:user_dependency, board_game_data: EditBoardGameRequest, repo: board_game_repo_dependency):
    try:
        check_user(user_id, current_user)

        repo.update_board_game_title(user_id, board_game_id, board_game_data.new_title)

    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


