from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from .index_router import check_user
from app.custom_exceptions import UnprocessableException, NotFoundException
from .user_router import user_dependency
from app.database import get_db
from app.repositories.board_game_repository import BoardGameRepository
from typing import Annotated
from app.schemas.board_games import BoardGameResponse

router = APIRouter(
    prefix="/user/{user_id}/board-games",
    tags=["board-games"]
)

def get_board_game_repo(db: Session = Depends(get_db)):  # get_db bekannt durch Import
    return BoardGameRepository(db)

board_game_repo_dependency = Annotated[BoardGameRepository, Depends(get_board_game_repo)]

@router.post("/")
def create_board_game(user_id: int, current_user:user_dependency, game_title:str, min_players:int, max_players: int, repo: board_game_repo_dependency):
    try:
        check_user(user_id, current_user)

        repo.create_board_game(game_title, min_players, max_players, user_id)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Boardgame successfully created",
            })

    except UnprocessableException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))


@router.get("/", response_model=list[BoardGameResponse], response_model_by_alias=True)
def get_board_games(user_id: int, current_user: user_dependency, repo: board_game_repo_dependency):
    check_user(user_id, current_user)
    board_games = repo.get_user_games(user_id)

    return board_games

@router.delete("/{board_game_id}")
def delete_board_game(user_id: int, current_user:user_dependency, repo: board_game_repo_dependency, board_game_id: int):
    try:
        check_user(user_id, current_user)

        repo.delete_board_game(board_game_id, user_id)

    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


