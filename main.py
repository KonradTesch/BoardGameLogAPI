from datetime import date
from http.client import HTTPException

import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from typing import Annotated
from db_manager import DataManager
import auth

app = FastAPI()
app.include_router(auth.router)

templates = Jinja2Templates(directory="templates")

data_manager = DataManager()

class User(BaseModel):
    username: str

class GameSession(BaseModel):
    boardgame_id: int
    date: str
    players: list[dict]

user_dependency = Annotated[dict, Depends(auth.get_current_user)]

def check_user(user_id: int, current_user):
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own data.",
        )



@app.get("/", response_class=RedirectResponse)
def index():
    return RedirectResponse("/login")


@app.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse("register.html", context={"request": request})


@app.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})


@app.get("/user/{user_id}")
def user_home(user_id: int, request: Request, current_user: user_dependency):
    check_user(user_id, current_user)

    user = data_manager.get_user_by_id(user_id)
    games = data_manager.get_all_games(sort = True)

    context = {
        "request": request,
        "user": user,
        "global_games": games,
        "player_names": [{"id" : player.id, "name": player.name} for player in user.players]
    }
    return templates.TemplateResponse("user_home.html", context=context)

#region User Endpoints

@app.patch("/user/{user_id}")
def update_user(user_id: int, user_data: User, current_user: user_dependency):
    check_user(user_id, current_user)

    data_manager.update_user(user_id, user_data.username)
    return JSONResponse( status_code=HTTP_200_OK,
        content={
        "message": "User successfully updated",
        "username": user_data.username
    })


@app.delete("/user/{user_id}")
def delete_user(user_id: int, current_user: user_dependency):
    check_user(user_id, current_user)

    data_manager.delete_user(user_id)

#endregion Endpoints

#region Player Endpoints

@app.post("/user/{user_id}/player")
def create_player(user_id: int,player_name: str, current_user: user_dependency):
    check_user(user_id, current_user)

    user = data_manager.get_user_by_id(user_id)
    players = user.players
    for player in players:
        if player.name == player_name:
            return JSONResponse(
                status_code=HTTP_400_BAD_REQUEST,
                content={"error": "Player exists already"}
            )

    data_manager.create_player(user, player_name)
    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content={
            "message": "Player successfully added",
        })


@app.patch("/user/{user_id}/player")
def update_player(user_id: int, player_data: dict, current_user: user_dependency):
    check_user(user_id, current_user)

    player_id = player_data.get("player_id")
    player_name = player_data.get("player_name")

    try:
        data_manager.update_player(user_id, player_id, player_name)
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={"message": "Player successfully updated"}
        )
    except ValueError as e:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"error": str(e)}
        )

@app.delete("/user/{user_id}/player")
def delete_player(user_id: int, player_id, current_user: user_dependency):
    check_user(user_id, current_user)

    data_manager.delete_player(player_id)

#endregion

#region Session Endpoints

@app.get("/user/{user_id}/session/{session_id}")
def session_details(user_id: int, session_id: int, request: Request, current_user: user_dependency):
    check_user(user_id, current_user)

    user = data_manager.get_user_by_id(user_id)
    session = data_manager.get_session_by_id(session_id)
    games = data_manager.get_all_games(sort = True)

    context = {
        "request": request,
        "user": user,
        "session": session,
        "games": games
    }
    return templates.TemplateResponse("session_details.html", context=context)


@app.post("/user/{user_id}/session")
def create_session(user_id: int, session: GameSession,current_user: user_dependency):
    check_user(user_id, current_user)

    print(f"game_id: {session.boardgame_id}, user_id: {user_id}, date: {session.date}, players: {session.players}")

    date_splits = session.date.split("-")
    date_value = date(int(date_splits[0]), int(date_splits[1]), int(date_splits[2]))

    data_manager.create_session(
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


@app.patch("/user/{user_id}/session/{session_id}")
def update_session(user_id: int, session_id: int, session: dict, current_user: user_dependency):
    check_user(user_id, current_user)

    game_id = int(session.get("game_id"))

    date_splits = session.get("date").split("-")
    date_value = date(int(date_splits[0]), int(date_splits[1]), int(date_splits[2]))

    players = session.get("existing_players")
    for player in session.get("new_players"):
        players.append(player)

    try:
        data_manager.update_session(session_id, game_id, date_value, players)
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={"message": "Session successfully updated"}
        )
    except ValueError as e:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"error": str(e)}
        )



@app.delete("/user/{user_id}/session/{session_id}")
def delete_session(user_id: int, session_id: int, current_user: user_dependency):
    check_user(user_id, current_user)

    data_manager.delete_session(session_id)

#endregion

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)