from datetime import date
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from typing import Annotated
from BoardGameLogAPI.repositories.db_manager import GameDataManager, UserDataManager
from BoardGameLogAPI.service.auth_logic import get_current_user
from .index_router import check_user
from ..custom_exceptions import NotFoundException

router = APIRouter(
    prefix="/user{user_id}/session",
    tags=["session"]
)

templates = Jinja2Templates(directory="templates")

game_manager = GameDataManager()
user_manager = UserDataManager()

user_dependency = Annotated[dict, Depends(get_current_user)]

class GameSession(BaseModel):
    boardgame_id: int
    date: str
    players: list[dict]

@router.get("/{session_id}")
def session_details(user_id: int, session_id: int, request: Request, current_user: user_dependency):
    check_user(user_id, current_user)

    user = user_manager.get_user_by_id(user_id)
    session = game_manager.get_session_by_id(session_id)
    games = game_manager.get_all_games(sort = True)

    context = {
        "request": request,
        "user": user,
        "session": session,
        "games": games
    }
    return templates.TemplateResponse("session_details.html", context=context)


@router.post("/")
def create_session(user_id: int, session: GameSession,current_user: user_dependency):
    check_user(user_id, current_user)

    try:
        date_splits = session.date.split("-")
        date_value = date(int(date_splits[0]), int(date_splits[1]), int(date_splits[2]))

        game_manager.create_session(
            game_id= int(session.boardgame_id),
            user_id = user_id,
            date_value = date_value,
            players=session.players,
        )

        return JSONResponse(
            status_code=HTTP_201_CREATED,
            content={
                "message": "Session successfully created",
            })
    except NotFoundException as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{session_id}")
def update_session(user_id: int, session_id: int, session: dict, current_user: user_dependency):
    check_user(user_id, current_user)

    game_id = int(session.get("game_id"))

    date_splits = session.get("date").split("-")
    date_value = date(int(date_splits[0]), int(date_splits[1]), int(date_splits[2]))

    players = session.get("existing_players")
    for player in session.get("new_players"):
        players.append(player)

    try:
        game_manager.update_session(session_id, game_id, date_value, players)
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={"message": "Session successfully updated"}
        )
    except NotFoundException as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{session_id}")
def delete_session(user_id: int, session_id: int, current_user: user_dependency):
    check_user(user_id, current_user)

    game_manager.delete_session(session_id)