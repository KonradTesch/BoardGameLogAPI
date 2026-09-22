from fastapi import APIRouter, HTTPException, status, Depends
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import get_db
from app.repositories.game_session_repository import GameSessionRepository
from app.repositories.user_repository import UserRepository
from .index_router import check_user
from app.custom_exceptions import NotFoundException
from .user_router import user_dependency
from app.schemas.session import GameSessionResponse, GameSessionRequest
from app.domain.session import GameSessionData, SessionPlayerData

router = APIRouter(
    prefix="/user/{user_id}/sessions",
    tags=["sessions"]
)

def get_game_session_repo(db: Session = Depends(get_db)):
    return GameSessionRepository(db)

game_session_repo_dependency = Annotated[GameSessionRepository, Depends(get_game_session_repo)]

def get_user_repo(db: Session = Depends(get_db)):
    return UserRepository(db)

user_repo_dependency = Annotated[UserRepository, Depends(get_user_repo)]

@router.get("/", response_model=list[GameSessionResponse], response_model_by_alias=True)
def get_all_sessions_of_user(user_id: int, current_user: user_dependency, game_repo: game_session_repo_dependency):
    check_user(user_id, current_user)

    sessions = game_repo.get_user_game_sessions_all(user_id)

    return sessions


@router.post("/", response_model=GameSessionResponse, response_model_by_alias=True, status_code=HTTP_201_CREATED)
def create_session(user_id: int, session: GameSessionRequest, current_user: user_dependency, game_session_repo: game_session_repo_dependency):
    check_user(user_id, current_user)
    try:

        new_session_data = GameSessionData(
            game_id = session.game_id,
            date = session.date,
            session_players= [SessionPlayerData(
                player_id=player.player_id,
                score=player.score,
                winner=player.winner
            ) for player in session.session_players]
        )

        new_session = game_session_repo.create_session(user_id, new_session_data)
        return new_session

    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{session_id}", response_model=GameSessionResponse, response_model_by_alias=True)
def update_session(user_id: int, session_id: int, session: GameSessionRequest, current_user: user_dependency, game_repo: game_session_repo_dependency):
    check_user(user_id, current_user)

    players = [SessionPlayerData(
        player_id=player.player_id,
        score = player.score,
        winner=player.winner
    ) for player in session.session_players]

    session_data = GameSessionData(
        game_id = session.game_id,
        date = session.date,
        session_players = players
    )

    try:
        updated_session = game_repo.update_session(user_id, session_id, session_data)
        return updated_session

    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{session_id}", status_code=HTTP_204_NO_CONTENT)
def delete_session(user_id: int, session_id: int, current_user: user_dependency, game_repo: game_session_repo_dependency):
    try:
        check_user(user_id, current_user)

        game_repo.delete_session(user_id, session_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))