from typing import Annotated, Any
from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.custom_exceptions import UnauthorizedException
from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.player_repository import PlayerRepository
from app.repositories.board_game_repository import BoardGameRepository
from app.repositories.game_session_repository import GameSessionRepository
from app.service.auth_logic import get_current_user


def check_user(user_id: int, current_user):
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own data.",
        )


def get_user(access_token: str = Cookie(None)) -> dict[str, Any]:
    try:
        return get_current_user(access_token)

    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

user_dependency = Annotated[dict, Depends(get_user)]


def get_user_repo(db: Session = Depends(get_db)):
    return UserRepository(db)

user_repo_dependency = Annotated[UserRepository, Depends(get_user_repo)]


def get_player_repo(db: Session = Depends(get_db)):
    return PlayerRepository(db)

player_repo_dependency = Annotated[PlayerRepository, Depends(get_player_repo)]


def get_board_game_repo(db: Session = Depends(get_db)):
    return BoardGameRepository(db)

board_game_repo_dependency = Annotated[BoardGameRepository, Depends(get_board_game_repo)]


def get_game_session_repo(db: Session = Depends(get_db)):
    return GameSessionRepository(db)

game_session_repo_dependency = Annotated[GameSessionRepository, Depends(get_game_session_repo)]
