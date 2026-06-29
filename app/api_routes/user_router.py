from fastapi import APIRouter, Request, Depends, status, HTTPException, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, Response
from typing import Annotated
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.game_session_repository import GameSessionRepository
from app.service.auth_logic import get_current_user
from app.service.stats_calculator import get_game_stats
from .index_router import check_user
from app.custom_exceptions import UnauthorizedException, NotFoundException
from app.schemas.user import PasswordChangeRequest, ChangeUsernameRequest

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

templates = Jinja2Templates(directory="templates")

def get_user(access_token: str = Cookie(None)):
    try:
        return get_current_user(access_token)

    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))

user_dependency = Annotated[dict, Depends(get_user)]

def get_user_repo(db: Session = Depends(get_db)):
    return UserRepository(db)

user_repo_dependency = Annotated[UserRepository, Depends(get_user_repo)]

def get_game_session_repo(db: Session = Depends(get_db)):
    return GameSessionRepository(db)

game_session_repo_dependency = Annotated[GameSessionRepository, Depends(get_game_session_repo)]

def formatted_date(date_string):
    if isinstance(date_string, str):
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
    else:
        date_obj = date_string
    return date_obj.strftime('%d.%m.%Y')


@router.patch("/{user_id}/username")
def change_username(user_id: int, body: ChangeUsernameRequest, current_user: user_dependency, user_repo: user_repo_dependency):
    check_user(user_id, current_user)
    new_username = body.get("new_username")
    user_repo.update_username(user_id, body["new_username"])
    return JSONResponse( status_code=status.HTTP_200_OK,
        content={
            "message": "Username successfully updated",
            "name": new_username,
            "id": user_id,
    })


@router.patch("/{user_id}/password")
def change_password(user_id: int, body: PasswordChangeRequest, current_user: user_dependency, user_repo: user_repo_dependency):
    try:
        check_user(user_id, current_user)

        user_repo.change_password(
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
def delete_account(user_id: int, current_user: user_dependency, user_repo: user_repo_dependency):
    try:
        check_user(user_id, current_user)

        user_repo.delete_user(user_id)

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


@router.get("/{user_id}/boardgames/stats")
def user_all_board_game_stats(user_id: int, request: Request, current_user: user_dependency, db: Session = Depends(get_db)):
    check_user(user_id, current_user)

    game_stats = get_game_stats(db, user_id)

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