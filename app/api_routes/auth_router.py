from typing import Any, Annotated
from fastapi import APIRouter, Depends, Response, HTTPException, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette import status
from app.custom_exceptions import UnprocessableException, NotFoundException, UnauthorizedException
from app.repositories.db_manager import UserDataManager
from app.service.auth_logic import get_current_user
from dotenv import load_dotenv
from os import getenv
from app.service.auth_logic import create_access_token
from app.schemas.auth import RegisterRequest, AuthUserResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")

def get_user(access_token: str = Cookie(None)) -> dict[str, Any] :
    try:
        return get_current_user(access_token)

    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))

user_dependency = Annotated[dict, Depends(get_user)]

user_manager = UserDataManager()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest):
    try:
        user_manager.create_user(body.name, body.password)
        return {
            "message": "Registration successful",
        }

    except UnprocessableException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/user", response_model=AuthUserResponse, status_code=status.HTTP_200_OK)
async def get_auth_user(current_user: user_dependency):
        return current_user

@router.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = user_manager.authenticate_user(form_data.username, form_data.password)

        token = create_access_token(user.username, user.id)

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax"
        )

        return {
            "message": "Login successful.",
            "id": user.id,
            "name": user.username
        }
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= e.detail)
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= e.detail)





