from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_422_UNPROCESSABLE_CONTENT
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import get_db
from app.repositories.player_repository import PlayerRepository
from .index_router import check_user
from app.custom_exceptions import NotFoundException, UnprocessableException
from .user_router import user_dependency
from app.schemas.player import PlayerResponse

router = APIRouter(
    prefix="/user/{user_id}/players",
    tags=["players"]
)

templates = Jinja2Templates(directory="templates")

def get_player_repo(db: Session = Depends(get_db)):
    return PlayerRepository(db)

player_repo_dependency = Annotated[PlayerRepository, Depends(get_player_repo)]

@router.get("/", response_model=list[PlayerResponse], response_model_by_alias=True)
def get_players(user_id: int, current_user: user_dependency, player_repo: player_repo_dependency):
    check_user(user_id, current_user)

    players = player_repo.get_user_players(user_id)

    return players



@router.post("/")
def create_player(user_id: int,player_name: str, current_user: user_dependency, player_repo: player_repo_dependency):
    try:
        check_user(user_id, current_user)

        player_repo.create_player(user_id, player_name)
        return JSONResponse(
            status_code=HTTP_201_CREATED,
            content={
                "message": "Player successfully added",
            })
    except UnprocessableException as e:
        return HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e)
        )


@router.patch("/")
def update_player(user_id: int, player_data: dict, current_user: user_dependency, player_repo: player_repo_dependency):
    check_user(user_id, current_user)

    player_id = player_data.get("player_id")
    player_name = player_data.get("player_name")

    try:
        player_repo.update_player(user_id, player_id, player_name)
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={"message": "Player successfully updated"}
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UnprocessableException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))


@router.delete("/")
def delete_player(user_id: int, player_id, current_user: user_dependency, player_repo: player_repo_dependency):
    try:
        check_user(user_id, current_user)

        player_repo.delete_player(player_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
