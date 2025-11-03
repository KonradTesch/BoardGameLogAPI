import datetime

import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from db_manager import DataManager

app = FastAPI()

templates = Jinja2Templates(directory="templates")

data_manager = DataManager()

class User(BaseModel):
    username: str

class GameSession(BaseModel):
    boardgame_id: int
    date: str
    players: list[dict]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    users = data_manager.get_all_users()


    context = {
        "request": request,
        "users": users
    }
    return templates.TemplateResponse("index.html", context=context)


@app.get("/user/{user_id}")
async def user_home(user_id: int, request: Request):
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

@app.post("/user")
async def create_user(user_data: User):
    users = data_manager.get_all_users()

    for user in users:
        if user.name == user_data.username:
            return JSONResponse(
                status_code=HTTP_400_BAD_REQUEST,
                content={"error": "User exists already"}
            )

    data_manager.create_user(user_data.username)

    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content={
        "message": "User successfully created",
        "username": user_data.username
    })


@app.delete("/user/{user_id}")
async def delete_user(user_id: int, request: Request):
    data_manager.delete_user(user_id)

#endregion Endpoints


#region Player Endpoints

@app.post("/user/{user_id}/player")
async def create_player(user_id: int,player_name: str):
    user = data_manager.get_user_by_id(user_id)
    players = user.players
    for player in players:
        if player.name == player_name:
            return JSONResponse(
                status_code=HTTP_400_BAD_REQUEST,
                content={"error": "Player exists already"}
            )

    data_manager.create_user_player(user, player_name)
    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content={
            "message": "Player successfully added",
        })

@app.delete("/user/{user_id}/player")
async def delete_player(user_id: int, player_id):
    data_manager.delete_player(player_id)

#endregion

#region Session Endpoints

@app.post("/user/{user_id}/session")
async def create_session(user_id: int, session: GameSession):

    print(f"game_id: {session.boardgame_id}, user_id: {user_id}, date: {session.date}, players: {session.players}")

    data_manager.create_session(
        game_id= int(session.boardgame_id),
        date = session.date,
        players=session.players,
    )

    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content={
            "message": "Session successfully created",
        })

#endregion

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)