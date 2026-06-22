from fastapi import APIRouter, Request, Depends, status, HTTPException, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Annotated
from datetime import datetime
from app.repositories.db_manager import UserDataManager, GameDataManager
from app.service.auth_logic import get_current_user
from app.service.stats_calculator import get_game_stats
from .index_router import check_user
from app.custom_exceptions import UnauthorizedException, NotFoundException
from app.schemas.user import PasswordChangeRequest, ChangeUsernameRequest
from app.schemas.board_games import BoardGameResponse

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

def formatted_date(date_string):
    if isinstance(date_string, str):
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
    else:
        date_obj = date_string
    return date_obj.strftime('%d.%m.%Y')

templates.env.filters['formatted_date'] = formatted_date

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


@router.patch("/{user_id}/username")
def change_username(user_id: int, body: ChangeUsernameRequest, current_user: user_dependency):
    check_user(user_id, current_user)
    new_username = body.get("new_username")
    user_manager.update_username(user_id, body["new_username"])
    return JSONResponse( status_code=status.HTTP_200_OK,
        content={
            "message": "Username successfully updated",
            "name": new_username,
            "id": user_id,
    })


@router.patch("/{user_id}/password")
def change_password(user_id: int, body: PasswordChangeRequest, current_user: user_dependency):
    try:
        check_user(user_id, current_user)

        user_manager.change_password(
            user_id,
            body.old_password,
            body.new_password
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
def delete_account(user_id: int, response: Response, current_user: user_dependency):
    try:
        check_user(user_id, current_user)

        user_manager.delete_user(user_id)

        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Account successfully deleted."
            }
        )
        response.delete_cookie(key="access_token", httponly=True, secure=False, samesite="lax")
        return response
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{user_id}/boardgames", response_model=list[BoardGameResponse], response_model_by_alias=True)
def user_all_board_games(user_id: int, current_user: user_dependency):
    check_user(user_id, currentUser)

    games = game_manager.get_all_games(sort = True)

    return games


@router.get("/{user_id}/boardgames/stats")
def user_all_board_game_stats(user_id: int, request: Request, current_user: user_dependency):
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