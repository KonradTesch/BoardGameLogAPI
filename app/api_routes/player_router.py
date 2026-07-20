from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_CONTENT
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import get_db
from app.repositories.player_repository import PlayerRepository
from .index_router import check_user
from app.custom_exceptions import NotFoundException, UnprocessableException
from .user_router import user_dependency
from app.schemas.player import PlayerResponse, PlayerCreate, UpdatePlayerRequest

router = APIRouter(
    prefix="/user/{user_id}/players",
    tags=["players"]
)

def get_player_repo(db: Session = Depends(get_db)):
    return PlayerRepository(db)

player_repo_dependency = Annotated[PlayerRepository, Depends(get_player_repo)]

@router.get("/", response_model=list[PlayerResponse], response_model_by_alias=True)
def get_players(user_id: int, current_user: user_dependency, player_repo: player_repo_dependency):
    check_user(user_id, current_user)

    players = player_repo.get_user_players(user_id)

    return players



@router.post("/", response_model=PlayerResponse, response_model_by_alias=True, status_code=status.HTTP_201_CREATED)
def create_player(user_id: int,new_player: PlayerCreate, current_user: user_dependency, player_repo: player_repo_dependency):
    try:
        check_user(user_id, current_user)

        if new_player.name == "":
            raise UnprocessableException(f"Player name is empty.")

        player = player_repo.create_player(user_id, new_player.name)
        return player

    except UnprocessableException as e:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e)
        )


@router.patch("/", status_code=status.HTTP_204_NO_CONTENT)
def update_player(user_id: int, player_id: int, player_data: UpdatePlayerRequest, current_user: user_dependency, player_repo: player_repo_dependency):
    try:
        check_user(user_id, current_user)

        player_repo.update_player(user_id, player_id, player_data.new_title)

    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UnprocessableException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(user_id: int, player_id: int, current_user: user_dependency, player_repo: player_repo_dependency):
    try:
        check_user(user_id, current_user)

        player_repo.delete_player(player_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
