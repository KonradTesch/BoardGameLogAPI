from fastapi import APIRouter, HTTPException, status
from app.custom_exceptions import UnprocessableException, NotFoundException
from .dependencies import check_user, user_dependency, board_game_repo_dependency
from app.schemas.board_game import BoardGameResponse, AddBoardGameRequest, EditBoardGameRequest

router = APIRouter(
    prefix="/user/{user_id}/board-games",
    tags=["board-games"]
)

@router.post("/", response_model=BoardGameResponse, status_code=status.HTTP_201_CREATED)
def create_board_game(user_id: int, current_user:user_dependency, board_game: AddBoardGameRequest, repo: board_game_repo_dependency):
    try:
        check_user(user_id, current_user)

        new_board_game = repo.create_board_game(board_game.title, user_id)

        return new_board_game

    except UnprocessableException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))


@router.get("/", response_model=list[BoardGameResponse], response_model_by_alias=True)
def get_board_games(user_id: int, current_user: user_dependency, repo: board_game_repo_dependency):
    check_user(user_id, current_user)
    board_games = repo.get_user_games(user_id)

    return board_games

@router.delete("/{board_game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board_game(user_id: int, board_game_id: int , current_user:user_dependency, repo: board_game_repo_dependency, ):
    try:
        check_user(user_id, current_user)

        repo.delete_board_game(board_game_id, user_id)

    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch("/{board_game_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_board_game(user_id: int, board_game_id: int, current_user:user_dependency, board_game_data: EditBoardGameRequest, repo: board_game_repo_dependency):
    try:
        check_user(user_id, current_user)

        repo.update_board_game_title(user_id, board_game_id, board_game_data.new_title)

    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


