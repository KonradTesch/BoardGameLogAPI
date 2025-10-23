import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from db_manager import DataManager
from modules import User

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

data_manager = DataManager()

class User(BaseModel):
    username: str


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
    context = {
        "request": request,
        "user": user
    }
    return templates.TemplateResponse("user_home.html", context=context)


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


@app.post("user/{user_id}/boardgame")
async def create_boardgame(user_id: int):
    pass


@app.post("user/{user_id}/session")
async def create_session(user_id: int):
    pass

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)