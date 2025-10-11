from fastapi import FastAPI
from modules import User ,Player, Boardgame

app = FastAPI()


@app.get("/")
async def index():
    pass

@app.get("/{user_id}")
async def user_home(user_id: int):
    pass

@app.post("user")
async def create_user():
    pass


@app.post("user/{user_id}/player")
async def create_player(user_id: int):
    pass


@app.post("user/{user_id}/boardgame")
async def create_boardgame(user_id: int):
    pass


@app.post("user/{user_id}/session")
async def create_session(user_id: int):
    pass