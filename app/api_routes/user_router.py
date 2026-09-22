from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.service.stats_calculator import get_game_stats
from .dependencies import check_user, user_dependency, user_repo_dependency
from app.custom_exceptions import UnauthorizedException, NotFoundException
from app.schemas.user import PasswordChangeRequest, ChangeUsernameRequest

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.patch("/{user_id}/username")
def change_username(user_id: int, change_username_data: ChangeUsernameRequest, current_user: user_dependency, user_repo: user_repo_dependency):
    check_user(user_id, current_user)
    user_repo.update_username(user_id, change_username_data.new_username)
    return JSONResponse( status_code=status.HTTP_200_OK,
        content={
            "message": "Username successfully updated",
            "name": change_username_data.new_username,
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
def user_all_board_game_stats(user_id: int, current_user: user_dependency, db: Session = Depends(get_db)):
    check_user(user_id, current_user)

    return get_game_stats(db, user_id)


@router.post("/{user_id}/logout")
def logout(user_id: int, response: Response, current_user: user_dependency):
    check_user(user_id, current_user)

    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,
        samesite="lax"
    )