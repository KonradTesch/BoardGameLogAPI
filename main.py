from datetime import date
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
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
def index(request: Request):
    users = data_manager.get_all_users()


    context = {
        "request": request,
        "users": users
    }
    return templates.TemplateResponse("index.html", context=context)


@app.get("/user/{user_id}")
def user_home(user_id: int, request: Request):
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
def create_user(user_data: User):
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

@app.patch("/user/{user_id}")
def update_user(user_id: int, user_data: User):
    data_manager.update_user(user_id, user_data.username)
    return JSONResponse( status_code=HTTP_200_OK,
        content={
        "message": "User successfully updated",
        "username": user_data.username
    })


@app.delete("/user/{user_id}")
def delete_user(user_id: int, request: Request):
    data_manager.delete_user(user_id)

#endregion Endpoints

#region Player Endpoints

@app.post("/user/{user_id}/player")
def create_player(user_id: int,player_name: str):
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
def update_player(user_id: int, player_data: dict):
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
def delete_player(user_id: int, player_id):
    data_manager.delete_player(player_id)

#endregion

#region Session Endpoints

@app.get("/user/{user_id}/session/{session_id}")
def session_details(user_id: int, session_id: int, request: Request):
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
def create_session(user_id: int, session: GameSession):
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
def update_session(user_id: int, session_id: int, session: dict):
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
def delete_session(user_id: int, session_id: int):
    data_manager.delete_session(session_id)

#endregion

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)