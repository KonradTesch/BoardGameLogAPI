from datetime import date, timedelta

import pytest
from sqlalchemy import select

from app.custom_exceptions import NotFoundException, UnprocessableException
from app.domain.session import GameSessionData, SessionPlayerData
from app.models import BoardGame, Player, SessionPlayer
from app.repositories.game_session_repository import GameSessionRepository


def test_create_session_stores_session_with_players(db_session, user, board_game, players):
    repo = GameSessionRepository(db_session)
    session_data = GameSessionData(
        date=date(2026, 1, 1),
        game_id=board_game.id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=11, winner=True),
            SessionPlayerData(player_id=players[1].id, score=10, winner=False),
        ]
    )

    created = repo.create_session(user.id, session_data)

    stored = repo.validate_session(user.id, created.id)
    assert stored.game_id == board_game.id
    assert stored.date == date(2026, 1, 1)
    results = {sp.player_id: (sp.score, sp.winner) for sp in stored.session_players}
    assert results == {
        players[0].id: (11, True),
        players[1].id: (10, False),
    }


def test_create_session_reject_other_user_game(db_session, user, second_user, players):
    repo = GameSessionRepository(db_session)

    board_game = BoardGame(title="Catan", user_id=second_user.id)

    db_session.add(board_game)
    db_session.flush()

    session_data = GameSessionData(
        date=date(2026, 1, 1),
        game_id=board_game.id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=11, winner=True),
            SessionPlayerData(player_id=players[1].id, score=9, winner=False)
        ]
    )

    with pytest.raises(NotFoundException, match="Board game"):
        repo.create_session(user.id, session_data)


def test_create_session_reject_other_user_player(db_session, user, second_user, board_game, players):
    repo = GameSessionRepository(db_session)

    other_player = Player(name="Henry", user_id=second_user.id)

    db_session.add(other_player)
    db_session.flush()

    session_data = GameSessionData(
        date=date(2026, 1, 1),
        game_id=board_game.id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=11, winner=True),
            SessionPlayerData(player_id=players[1].id, score=9, winner=False),
            SessionPlayerData(player_id=other_player.id, score=10, winner=False)
        ]
    )

    with pytest.raises(NotFoundException, match="Player"):
        repo.create_session(user.id, session_data)


def test_create_session_reject_duplicate_players(db_session, user, board_game, players):
    repo = GameSessionRepository(db_session)

    session_data = GameSessionData(
        date=date(2026, 1, 1),
        game_id=board_game.id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=11, winner=True),
            SessionPlayerData(player_id=players[0].id, score=9, winner=True),
        ]
    )

    with pytest.raises(UnprocessableException):
        repo.create_session(user.id, session_data)


def test_create_session_reject_future_date(db_session, user, board_game, players):
    repo = GameSessionRepository(db_session)

    session_data = GameSessionData(
        date=date.today() + timedelta(days=1),
        game_id=board_game.id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=11, winner=True),
            SessionPlayerData(player_id=players[1].id, score=9, winner=True),
        ]
    )

    with pytest.raises(UnprocessableException):
        repo.create_session(user.id, session_data)


def test_create_session_failed_creates_no_data(db_session, second_user, user, board_game):
    repo = GameSessionRepository(db_session)

    foreign_player = Player(user_id=second_user.id, name="Tom")

    db_session.add(foreign_player)
    db_session.commit()

    session_data = GameSessionData(
        date=date(2026, 1, 2),
        game_id=board_game.id,
        session_players=[
            SessionPlayerData(player_id=foreign_player.id, score=10, winner=True)
        ]
    )

    with pytest.raises(NotFoundException, match="Player"):
        repo.create_session(user.id, session_data)

    stored = repo.get_user_game_sessions_all(user.id)

    assert len(stored) == 0


def test_get_session_valid(db_session, game_session, user):
    repo = GameSessionRepository(db_session)

    assert repo.validate_session(user.id, game_session.id) == game_session


def test_get_session_reject_other_user(db_session, game_session, second_user):
    repo = GameSessionRepository(db_session)

    with pytest.raises(NotFoundException, match="Game Session"):
        repo.validate_session(second_user.id, game_session.id)


def test_get_session_reject_unknown_session(db_session, user):
    repo = GameSessionRepository(db_session)

    with pytest.raises(NotFoundException, match="Game Session"):
        repo.validate_session(user.id, -1)


def test_update_session_game(db_session, game_session, user, players):
    repo = GameSessionRepository(db_session)

    new_game = BoardGame(
        user_id=user.id,
        title="Risiko",
    )

    db_session.add(new_game)
    db_session.flush()

    new_session_data = GameSessionData(
        date=game_session.date,
        game_id=new_game.id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=11, winner=True),
            SessionPlayerData(player_id=players[1].id, score=10, winner=False)
        ]
    )

    repo.update_session(user.id, game_session.id, new_session_data)

    stored = repo.validate_session(user.id, game_session.id)

    assert stored.game_id == new_game.id


def test_update_session_date(db_session, game_session, user, players):
    repo = GameSessionRepository(db_session)

    new_date = date(2026, 1, 2)

    new_session_data = GameSessionData(
        date=new_date,
        game_id=game_session.game_id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=11, winner=True),
            SessionPlayerData(player_id=players[1].id, score=10, winner=False)
        ]
    )

    repo.update_session(user.id, game_session.id, new_session_data)

    stored = repo.validate_session(user.id, game_session.id)

    assert stored.date == new_date


def test_update_session_add_player(db_session, game_session, user, players):
    repo = GameSessionRepository(db_session)

    new_player = Player(
        user_id=user.id,
        name="Tom",
    )
    db_session.add(new_player)
    db_session.flush()

    new_session_data = GameSessionData(
        date=game_session.date,
        game_id=game_session.game_id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=11, winner=True),
            SessionPlayerData(player_id=players[1].id, score=10, winner=False),
            SessionPlayerData(player_id=new_player.id, score=9, winner=False)
        ]
    )

    repo.update_session(user.id, game_session.id, new_session_data)

    stored = repo.validate_session(user.id, game_session.id)

    results = {sp.player_id: (sp.score, sp.winner) for sp in stored.session_players}
    assert results == {
        players[0].id: (11, True),
        players[1].id: (10, False),
        new_player.id: (9, False)
    }


def test_update_session_remove_player(db_session, game_session, user, players):
    repo = GameSessionRepository(db_session)

    new_session_data = GameSessionData(
        date=game_session.date,
        game_id=game_session.game_id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=11, winner=True),
        ]
    )

    repo.update_session(user.id, game_session.id, new_session_data)

    stored = repo.validate_session(user.id, game_session.id)

    results = {sp.player_id: (sp.score, sp.winner) for sp in stored.session_players}
    assert results == {
        players[0].id: (11, True),
    }


def test_update_session_change_player(db_session, game_session, user, players):
    repo = GameSessionRepository(db_session)

    new_session_data = GameSessionData(
        date=game_session.date,
        game_id=game_session.game_id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=10, winner=False),
            SessionPlayerData(player_id=players[1].id, score=12, winner=True),
        ]
    )

    repo.update_session(user.id, game_session.id, new_session_data)

    stored = repo.validate_session(user.id, game_session.id)

    results = {sp.player_id: (sp.score, sp.winner) for sp in stored.session_players}
    assert results == {
        players[0].id: (10, False),
        players[1].id: (12, True)
    }


def test_update_session_reject_other_user(db_session, game_session, user, second_user, players):
    repo = GameSessionRepository(db_session)

    new_date = date(2026, 1, 2)

    new_session_data = GameSessionData(
        date=new_date,
        game_id=game_session.game_id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=11, winner=True),
            SessionPlayerData(player_id=players[1].id, score=9, winner=False)
        ]
    )

    with pytest.raises(NotFoundException, match="Game Session"):
        repo.update_session(second_user.id, game_session.id, new_session_data)


def test_update_session_reject_other_user_game(db_session, game_session, user, second_user, players):
    repo = GameSessionRepository(db_session)

    new_game = BoardGame(
        user_id=second_user.id,
        title="Risiko",
    )

    db_session.add(new_game)
    db_session.flush()

    new_session_data = GameSessionData(
        date=game_session.date,
        game_id=new_game.id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=11, winner=True),
            SessionPlayerData(player_id=players[1].id, score=9, winner=False)
        ]
    )

    with pytest.raises(NotFoundException, match="Board game"):
        repo.update_session(user.id, game_session.id, new_session_data)


def test_update_session_reject_future_date(db_session, game_session, user, players):
    repo = GameSessionRepository(db_session)

    new_date = date.today() + timedelta(days=1)

    new_session_data = GameSessionData(
        date=new_date,
        game_id=game_session.game_id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=11, winner=True),
            SessionPlayerData(player_id=players[1].id, score=9, winner=False)
        ]
    )

    with pytest.raises(UnprocessableException):
        repo.update_session(user.id, game_session.id, new_session_data)


def test_update_session_reject_other_user_player(db_session, game_session, user, second_user, players):
    repo = GameSessionRepository(db_session)

    new_player = Player(
        user_id=second_user.id,
        name="Tom",
    )
    db_session.add(new_player)
    db_session.flush()

    new_session_data = GameSessionData(
        date=game_session.date,
        game_id=game_session.game_id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=10, winner=False),
            SessionPlayerData(player_id=players[1].id, score=12, winner=True),
            SessionPlayerData(player_id=new_player.id, score=10, winner=False)
        ]
    )

    with pytest.raises(NotFoundException, match="Player"):
        repo.update_session(user.id, game_session.id, new_session_data)


def test_update_session_reject_duplicate_players(db_session, game_session, user, players):
    repo = GameSessionRepository(db_session)

    new_session_data = GameSessionData(
        date=game_session.date,
        game_id=game_session.game_id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=10, winner=False),
            SessionPlayerData(player_id=players[1].id, score=12, winner=True),
            SessionPlayerData(player_id=players[1].id, score=10, winner=False)
        ]
    )

    with pytest.raises(UnprocessableException):
        repo.update_session(user.id, game_session.id, new_session_data)


def test_update_session_failed_update_leaves_session_unchanged(db_session, game_session, user, second_user, board_game,
                                                               players):
    repo = GameSessionRepository(db_session)

    new_game = BoardGame(user_id=user.id, title="Risiko")
    foreign_player = Player(user_id=second_user.id, name="Tom")

    db_session.add_all([new_game, foreign_player])
    db_session.commit()

    session_data = GameSessionData(
        date=date(2026, 1, 2),
        game_id=new_game.id,
        session_players=[
            SessionPlayerData(player_id=players[0].id, score=99, winner=False),
            SessionPlayerData(player_id=foreign_player.id, score=10, winner=True),
        ],
    )

    with pytest.raises(NotFoundException):
        repo.update_session(user.id, game_session.id, session_data)

    stored = repo.validate_session(user.id, game_session.id)
    assert stored.game_id == board_game.id
    assert stored.date == date(2026, 1, 1)

    results = {sp.player_id: (sp.score, sp.winner) for sp in stored.session_players}
    assert results == {
        players[0].id: (11, True),
        players[1].id: (10, False),
    }


def test_delete_session(db_session, user, game_session, players):
    repo = GameSessionRepository(db_session)

    repo.delete_session(user.id, game_session.id)

    with pytest.raises(NotFoundException, match="Game Session"):
        repo.validate_session(user.id, game_session.id)

    remaining_session_players = db_session.scalars(
        select(SessionPlayer).where(SessionPlayer.session_id == game_session.id)
    ).all()
    assert len(remaining_session_players) == 0

    player_ids = {p.id for p in players}
    remaining_ids = set(db_session.scalars(
        select(Player.id).where(Player.id.in_(player_ids))
    ).all())
    assert remaining_ids == player_ids


def test_delete_session_reject_other_user(db_session, user, second_user, game_session):
    repo = GameSessionRepository(db_session)

    with pytest.raises(NotFoundException, match="Game Session"):
        repo.delete_session(second_user.id, game_session.id)

    assert repo.validate_session(user.id, game_session.id) == game_session


def test_get_all_sessions_returns_only_own_sessions(db_session, user, second_user, board_game, make_game_session):
    other_board_game = BoardGame(title="Azul", user_id=second_user.id)
    db_session.add(other_board_game)
    db_session.commit()

    own_session_1 = make_game_session(user, board_game)
    own_session_2 = make_game_session(user, board_game)
    make_game_session(second_user, other_board_game)
    repo = GameSessionRepository(db_session)

    result = repo.get_user_game_sessions_all(user.id)

    assert {s.id for s in result} == {own_session_1.id, own_session_2.id}


def test_get_all_sessions_user_without_sessions(db_session, second_user):
    repo = GameSessionRepository(db_session)

    result = repo.get_user_game_sessions_all(second_user.id)
    assert len(result) == 0


def test_get_user_game_sessions_by_game(db_session, user, second_user, board_game, make_game_session):
    other_board_game = BoardGame(title="Azul", user_id=user.id)
    db_session.add(other_board_game)
    db_session.commit()

    own_session_1 = make_game_session(user, board_game)
    own_session_2 = make_game_session(user, board_game)

    make_game_session(user, other_board_game)
    make_game_session(second_user, board_game)

    repo = GameSessionRepository(db_session)

    result = repo.get_user_game_session_by_game(user.id, board_game.id)

    assert {s.id for s in result} == {own_session_1.id, own_session_2.id}
