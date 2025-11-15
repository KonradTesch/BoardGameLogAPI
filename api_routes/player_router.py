from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from BoardGameLogAPI.repositories.db_manager import PlayerDataManager, UserDataManager
from .index_router import check_user
from BoardGameLogAPI.custom_exceptions import NotFoundException, UnprocessableException
from .user_router import user_dependency

router = APIRouter(
    prefix="/user/{user_id}/player",
    tags=["player"]
)

templates = Jinja2Templates(directory="templates")

player_manager = PlayerDataManager()
user_manager = UserDataManager()


@router.post("/")
def create_player(user_id: int,player_name: str, current_user: user_dependency):
    check_user(user_id, current_user)

    user = user_manager.get_user_by_id(user_id)
    players = user.players
    for player in players:
        if player.name == player_name:
            return JSONResponse(
                status_code=HTTP_400_BAD_REQUEST,
                content={"error": "Player exists already"}
            )

    player_manager.create_player(user, player_name)
    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content={
            "message": "Player successfully added",
        })


@router.patch("/")
def update_player(user_id: int, player_data: dict, current_user: user_dependency):
    check_user(user_id, current_user)

    player_id = player_data.get("player_id")
    player_name = player_data.get("player_name")

    try:
        player_manager.update_player(user_id, player_id, player_name)
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={"message": "Player successfully updated"}
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UnprocessableException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))


@router.delete("/")
def delete_player(user_id: int, player_id, current_user: user_dependency):
    try:
        check_user(user_id, current_user)

        player_manager.delete_player(player_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
