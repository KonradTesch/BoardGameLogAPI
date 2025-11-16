from fastapi import APIRouter, Request, Depends, status, HTTPException, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, Response
from typing import Annotated
from pydantic import BaseModel
from BoardGameLogAPI.repositories.db_manager import UserDataManager, GameDataManager
from BoardGameLogAPI.service.auth_logic import get_current_user
from BoardGameLogAPI.service.stats_calculator import get_game_stats
from .index_router import check_user
from BoardGameLogAPI.custom_exceptions import UnauthorizedException, NotFoundException

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

templates = Jinja2Templates(directory="templates")

user_manager = UserDataManager()
game_manager = GameDataManager()

def get_user(access_token: str = Cookie(None)):
    try:
        return get_current_user(access_token)

    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))

user_dependency = Annotated[dict, Depends(get_user)]

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
def update_username(user_id: int, user_data: dict, current_user: user_dependency):
    check_user(user_id, current_user)

    user_manager.update_username(user_id, user_data["username"])
    return JSONResponse( status_code=status.HTTP_200_OK,
        content={
        "message": "Username successfully updated",
    })


@router.patch("/{user_id}/password")
def change_password(user_id: int, password_data: dict, current_user: user_dependency):
    try:
        check_user(user_id, current_user)

        user_manager.change_password(
            user_id,
            password_data["old_password"],
            password_data["new_password"]
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Password successfully changed"
            }
        )
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: user_dependency):
    check_user(user_id, current_user)

    user_manager.delete_user(user_id)


@router.get("/{user_id}/stats/games")
def user_game_stats(user_id: int, request: Request, current_user: user_dependency):
    check_user(user_id, current_user)

    game_stats = get_game_stats(user_id)

    context = {
        "request": request,
        "user": current_user,
        "game_stats": game_stats,
    }

    return templates.TemplateResponse("game_stats.html", context=context)


@router.post("/{user_id}/logout")
def logout(user_id: int, response: Response, current_user: user_dependency):
    check_user(user_id, current_user)

    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,
        samesite="lax"
    )