from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK
from typing import Annotated
from pydantic import BaseModel
from BoardGameLogAPI.database.db_manager import UserDataManager, GameDataManager
from BoardGameLogAPI.logic.auth_logic import get_current_user
from .index_router import check_user

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

templates = Jinja2Templates(directory="templates")

user_manager = UserDataManager()
game_manager = GameDataManager()

user_dependency = Annotated[dict, Depends(get_current_user)]

class User(BaseModel):
    username: str


@router.get("/{user_id}")
def user_home(user_id: int, request: Request, current_user: user_dependency):
    check_user(user_id, current_user)

    user = user_manager.get_user_by_id(user_id)
    games = game_manager.get_all_games(sort = True)

    context = {
        "request": request,
        "user": user,
        "global_games": games,
        "player_names": [{"id" : player.id, "name": player.name} for player in user.players]
    }
    return templates.TemplateResponse("user_home.html", context=context)


@router.patch("/{user_id}")
def update_user(user_id: int, user_data: User, current_user: user_dependency):
    check_user(user_id, current_user)

    user_manager.update_user(user_id, user_data.username)
    return JSONResponse( status_code=HTTP_200_OK,
        content={
        "message": "User successfully updated",
        "username": user_data.username
    })


@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: user_dependency):
    check_user(user_id, current_user)

    user_manager.delete_user(user_id)