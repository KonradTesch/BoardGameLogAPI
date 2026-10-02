from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.custom_exceptions import UnprocessableException, NotFoundException, UnauthorizedException
from app.service.auth_logic import create_access_token
from . import auth_cookie
from .dependencies import user_dependency, user_repo_dependency
from app.schemas.auth import RegisterRequest, AuthUserResponse
from ..domain.auth import RegisterData

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(register_request: RegisterRequest, repo: user_repo_dependency):
    try:
        register_data = RegisterData(username=register_request.username, password=register_request.password)

        repo.create_user(register_data)
        return {
            "message": "Registration successful",
        }

    except UnprocessableException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/user", response_model=AuthUserResponse, status_code=status.HTTP_200_OK)
async def get_auth_user(current_user: user_dependency):
    return current_user

@router.post("/login")
async def login_for_access_token(repo: user_repo_dependency, response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = repo.authenticate_user(form_data.username, form_data.password)

        token = create_access_token(user.id, 0)

        auth_cookie.set_auth_cookie(response, token)

        return {
            "message": "Login successful.",
            "id": user.id,
            "username": user.username
        }
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= e.detail)

@router.post("/logout")
async def logout(response: Response):
    auth_cookie.clear_auth_cookie(response)





