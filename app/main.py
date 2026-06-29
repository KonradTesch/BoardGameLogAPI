import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api_routes.user_router import router as user_router
from app.api_routes.session_router import router as session_router
from app.api_routes.player_router import router as player_router
from app.api_routes.board_game_router import router as board_game_router
from app.api_routes.auth_router import router as auth_router
from app.api_routes.index_router import router as index_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(index_router)
app.include_router(user_router)
app.include_router(session_router)
app.include_router(player_router)
app.include_router(board_game_router)
app.include_router(auth_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)