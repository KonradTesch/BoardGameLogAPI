from datetime import date
from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import get_db
from app.repositories.game_session_repository import GameSessionRepository
from app.repositories.user_repository import UserRepository
from .index_router import check_user
from app.custom_exceptions import NotFoundException
from .user_router import user_dependency, formatted_date
from app.schemas.sessions import GameSessionResponse, GameSessionRequest

router = APIRouter(
    prefix="/user/{user_id}/sessions",
    tags=["sessions"]
)

templates = Jinja2Templates(directory="templates")
templates.env.filters['formatted_date'] = formatted_date

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

@router.get("/{session_id}")
def session_details(user_id: int, session_id: int, request: Request, current_user: user_dependency, game_repo: game_session_repo_dependency, user_repo: user_repo_dependency):
    check_user(user_id, current_user)

    user = user_repo.get_user_by_id(user_id)
    session = game_repo.get_session_by_id(session_id)
    games = game_repo.get_all_games(sort = True)

    context = {
        "request": request,
        "user": user,
        "session": session,
        "games": games
    }
    return templates.TemplateResponse("session_details.html", context=context)


@router.post("/", response_model=GameSessionResponse, response_model_by_alias=True, status_code=HTTP_201_CREATED)
def create_session(user_id: int, session: GameSessionRequest, current_user: user_dependency, game_session_repo: game_session_repo_dependency):
    check_user(user_id, current_user)
    try:
        new_session = game_session_repo.create_session(
            game_id= session.game_id,
            user_id = user_id,
            date_value = session.date,
            session_players = session.session_players
        )
        return new_session

    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{session_id}")
def update_session(user_id: int, session_id: int, session: dict, current_user: user_dependency, game_repo: game_session_repo_dependency):
    check_user(user_id, current_user)

    game_id = int(session.get("game_id"))

    date_splits = session.get("date").split("-")
    date_value = date(int(date_splits[0]), int(date_splits[1]), int(date_splits[2]))

    players = session.get("existing_players")
    for player in session.get("new_players"):
        players.append(player)

    try:
        game_repo.update_session(session_id, game_id, date_value, players)
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={"message": "Session successfully updated"}
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{session_id}")
def delete_session(user_id: int, session_id: int, current_user: user_dependency, game_repo: game_session_repo_dependency):
    try:
        check_user(user_id, current_user)

        game_repo.delete_session(session_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))