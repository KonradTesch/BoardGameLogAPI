from fastapi import APIRouter, HTTPException, status
from starlette.status import HTTP_422_UNPROCESSABLE_CONTENT
from app.custom_exceptions import NotFoundException, UnprocessableException
from .dependencies import check_user, user_dependency, player_repo_dependency
from app.schemas.player import PlayerResponse, PlayerCreate, UpdatePlayerRequest

router = APIRouter(
    prefix="/user/{user_id}/players",
    tags=["players"]
)

@router.get("/", response_model=list[PlayerResponse], response_model_by_alias=True)
def get_players(user_id: int, current_user: user_dependency, player_repo: player_repo_dependency):
    check_user(user_id, current_user)

    players = player_repo.get_user_players(user_id)

    return players



@router.post("/", response_model=PlayerResponse, response_model_by_alias=True, status_code=status.HTTP_201_CREATED)
def create_player(user_id: int,new_player: PlayerCreate, current_user: user_dependency, player_repo: player_repo_dependency):
    try:
        check_user(user_id, current_user)

        if new_player.name == "":
            raise UnprocessableException(f"Player name is empty.")

        player = player_repo.create_player(user_id, new_player.name)
        return player

    except UnprocessableException as e:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e)
        )


@router.patch("/", status_code=status.HTTP_204_NO_CONTENT)
def update_player(user_id: int, player_id: int, player_data: UpdatePlayerRequest, current_user: user_dependency, player_repo: player_repo_dependency):
    try:
        check_user(user_id, current_user)

        player_repo.update_player(user_id, player_id, player_data.new_title)

    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UnprocessableException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(user_id: int, player_id: int, current_user: user_dependency, player_repo: player_repo_dependency):
    try:
        check_user(user_id, current_user)

        player_repo.delete_player(player_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
