import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api_routes.user_router import router as user_router
from app.api_routes.session_router import router as session_router
from app.api_routes.player_router import router as player_router
from app.api_routes.board_game_router import router as board_game_router
from app.api_routes.auth_router import router as auth_router
app = FastAPI(
    docs_url="/docs" if settings.enable_docs else None,
    redoc_url="/redoc" if settings.enable_docs else None,
    openapi_url="/openapi.json" if settings.enable_docs else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(user_router)
app.include_router(session_router)
app.include_router(player_router)
app.include_router(board_game_router)
app.include_router(auth_router)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000, reload=True)
