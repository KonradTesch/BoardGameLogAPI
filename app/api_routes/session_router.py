from datetime import date
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from app.repositories.db_manager import GameDataManager, UserDataManager
from .index_router import check_user
from app.custom_exceptions import NotFoundException
from .user_router import user_dependency, formatted_date
from app.schemas.sessions import GameSession

router = APIRouter(
    prefix="/user/{user_id}/sessions",
    tags=["sessions"]
)

templates = Jinja2Templates(directory="templates")
templates.env.filters['formatted_date'] = formatted_date

game_manager = GameDataManager()
user_manager = UserDataManager()


@router.get("/", response_model=list[GameSession], response_model_by_alias=True)
def get_all_sessions_of_user(user_id: int, current_user: user_dependency):
    check_user(user_id, current_user)

    sessions = game_manager.get_user_game_sessions_all(user_id)

    return sessions

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
    try:
        check_user(user_id, current_user)

        game_manager.delete_session(session_id)
    except NotFoundException as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))