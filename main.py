from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from db_manager import DataManager

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
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


@app.get("/{user_id}")
async def user_home(user_id: int):
    pass


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


@app.post("user/{user_id}/player")
async def create_player(user_id: int):
    pass


@app.post("user/{user_id}/boardgame")
async def create_boardgame(user_id: int):
    pass


@app.post("user/{user_id}/session")
async def create_session(user_id: int):
    pass