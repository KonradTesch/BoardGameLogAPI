import pytest

from app.custom_exceptions import NotFoundException, UnprocessableException
from app.models import BoardGame
from app.repositories.board_game_repository import BoardGameRepository


def test_create_board_game_stores_game(db_session, user):
    repo = BoardGameRepository(db_session, user.id)

    created = repo.create_board_game("Catan")

    stored = repo.get_board_game(created.id)
    assert stored.title == "Catan"
    assert stored.user_id == user.id


def test_create_board_game_reject_empty_title(db_session, user):
    repo = BoardGameRepository(db_session, user.id)

    with pytest.raises(UnprocessableException, match="empty"):
        repo.create_board_game("")

    assert len(repo.get_all_games()) == 0


def test_create_board_game_reject_duplicate_title(db_session, user, board_game):
    repo = BoardGameRepository(db_session, user.id)

    with pytest.raises(UnprocessableException, match="already exists"):
        repo.create_board_game(board_game.title)

    assert len(repo.get_all_games()) == 1


def test_create_board_game_same_title_other_user(db_session, other_user, board_game):
    repo = BoardGameRepository(db_session, other_user.id)

    created = repo.create_board_game(board_game.title)

    stored = repo.get_board_game(created.id)
    assert stored.title == board_game.title


def test_get_board_game_valid(db_session, user, board_game):
    repo = BoardGameRepository(db_session, user.id)

    assert repo.get_board_game(board_game.id) == board_game


def test_get_board_game_reject_other_user(db_session, other_user, board_game):
    repo = BoardGameRepository(db_session, other_user.id)

    with pytest.raises(NotFoundException, match="Board game"):
        repo.get_board_game(board_game.id)


def test_get_board_game_reject_unknown_game(db_session, user):
    repo = BoardGameRepository(db_session, user.id)

    with pytest.raises(NotFoundException, match="Board game"):
        repo.get_board_game(-1)


def test_update_board_game_title(db_session, user, board_game):
    repo = BoardGameRepository(db_session, user.id)

    repo.update_board_game_title(board_game.id, "Risiko")

    stored = repo.get_board_game(board_game.id)
    assert stored.title == "Risiko"


def test_update_board_game_title_reject_empty_title(db_session, user, board_game):
    repo = BoardGameRepository(db_session, user.id)

    with pytest.raises(UnprocessableException, match="empty"):
        repo.update_board_game_title(board_game.id, "")

    stored = repo.get_board_game(board_game.id)
    assert stored.title == "Catan"


def test_update_board_game_title_reject_other_user(db_session, user, other_user, board_game):
    other_repo = BoardGameRepository(db_session, other_user.id)

    with pytest.raises(NotFoundException, match="Board game"):
        other_repo.update_board_game_title(board_game.id, "Risiko")

    owner_repo = BoardGameRepository(db_session, user.id)

    stored = owner_repo.get_board_game(board_game.id)
    assert stored.title == "Catan"


def test_delete_board_game(db_session, user, board_game):
    repo = BoardGameRepository(db_session, user.id)

    repo.delete_board_game(board_game.id)

    with pytest.raises(NotFoundException, match="Board game"):
        repo.get_board_game(board_game.id)


def test_delete_board_game_reject_other_user(db_session, user, other_user, board_game):
    other_repo = BoardGameRepository(db_session, other_user.id)

    with pytest.raises(NotFoundException, match="Board game"):
        other_repo.delete_board_game(board_game.id)

    owner_repo = BoardGameRepository(db_session, user.id)

    assert owner_repo.get_board_game(board_game.id) == board_game


def test_get_all_games_returns_only_own_games(db_session, user, other_user, board_game):
    own_game = BoardGame(title="Azul", user_id=user.id)
    other_game = BoardGame(title="Risiko", user_id=other_user.id)
    db_session.add_all([own_game, other_game])
    db_session.commit()

    repo = BoardGameRepository(db_session, user.id)

    result = repo.get_all_games()

    assert {g.id for g in result} == {board_game.id, own_game.id}


def test_get_all_games_user_without_games(db_session, other_user):
    repo = BoardGameRepository(db_session, other_user.id)

    result = repo.get_all_games()
    assert len(result) == 0
