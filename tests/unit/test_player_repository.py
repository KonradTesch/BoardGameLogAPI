import pytest
from sqlalchemy import select

from app.custom_exceptions import NotFoundException, UnprocessableException
from app.models import BoardGame, Player, SessionPlayer, GameSession
from app.repositories.player_repository import PlayerRepository


def test_create_player_stores_player(db_session, user):
    repo = PlayerRepository(db_session)

    created = repo.create_player(user.id, "Clara")

    stored = repo.get_player(user.id, created.id)
    assert stored.name == "Clara"
    assert stored.user_id == user.id


def test_create_player_reject_duplicate_name(db_session, user, players):
    repo = PlayerRepository(db_session)

    with pytest.raises(UnprocessableException, match="already exists"):
        repo.create_player(user.id, players[0].name)

    assert len(repo.get_all_players(user.id)) == 2


def test_create_player_same_name_other_user(db_session, other_user, players):
    repo = PlayerRepository(db_session)

    created = repo.create_player(other_user.id, players[0].name)

    stored = repo.get_player(other_user.id, created.id)
    assert stored.name == players[0].name


def test_get_player_valid(db_session, user, players):
    repo = PlayerRepository(db_session)

    assert repo.get_player(user.id, players[0].id) == players[0]


def test_get_player_reject_other_user(db_session, other_user, players):
    repo = PlayerRepository(db_session)

    with pytest.raises(NotFoundException, match="Player"):
        repo.get_player(other_user.id, players[0].id)


def test_get_player_reject_unknown_player(db_session, user):
    repo = PlayerRepository(db_session)

    with pytest.raises(NotFoundException, match="Player"):
        repo.get_player(user.id, -1)


def test_update_player(db_session, user, players):
    repo = PlayerRepository(db_session)

    repo.update_player(user.id, players[0].id, "Clara")

    stored = repo.get_player(user.id, players[0].id)
    assert stored.name == "Clara"


def test_update_player_keep_own_name(db_session, user, players):
    repo = PlayerRepository(db_session)

    repo.update_player(user.id, players[0].id, players[0].name)

    stored = repo.get_player(user.id, players[0].id)
    assert stored.name == "Anna"


def test_update_player_reject_duplicate_name(db_session, user, players):
    repo = PlayerRepository(db_session)

    with pytest.raises(UnprocessableException, match="already exists"):
        repo.update_player(user.id, players[0].id, players[1].name)

    stored = repo.get_player(user.id, players[0].id)
    assert stored.name == "Anna"


def test_update_player_reject_other_user(db_session, user, other_user, players):
    repo = PlayerRepository(db_session)

    with pytest.raises(NotFoundException, match="Player"):
        repo.update_player(other_user.id, players[0].id, "Clara")

    stored = repo.get_player(user.id, players[0].id)
    assert stored.name == "Anna"


def test_delete_player(db_session, user, players, game_session):
    repo = PlayerRepository(db_session)

    repo.delete_player(user.id, players[0].id)

    with pytest.raises(NotFoundException, match="Player"):
        repo.get_player(user.id, players[0].id)

    remaining_session_players = db_session.scalars(
        select(SessionPlayer).where(SessionPlayer.session_id == game_session.id)
    ).all()
    assert {sp.player_id for sp in remaining_session_players} == {players[1].id}

    stored_session = db_session.get(GameSession, game_session.id)
    assert stored_session is not None
    assert stored_session.deleted_players is True


def test_delete_player_reject_other_user(db_session, user, other_user, players):
    repo = PlayerRepository(db_session)

    with pytest.raises(NotFoundException, match="Player"):
        repo.delete_player(other_user.id, players[0].id)

    assert repo.get_player(user.id, players[0].id) == players[0]


def test_get_all_players_returns_only_own_players(db_session, user, other_user, players):
    other_player = Player(name="Henry", user_id=other_user.id)
    db_session.add(other_player)
    db_session.commit()

    repo = PlayerRepository(db_session)

    result = repo.get_all_players(user.id)

    assert {p.id for p in result} == {p.id for p in players}


def test_get_all_players_user_without_players(db_session, other_user):
    repo = PlayerRepository(db_session)

    result = repo.get_all_players(other_user.id)
    assert len(result) == 0


def test_get_player_scores_for_game(db_session, user, players, board_game, game_session, make_game_session):
    other_game = BoardGame(title="Azul", user_id=user.id)
    db_session.add(other_game)
    db_session.commit()

    other_session = make_game_session(user, other_game)
    other_session.session_players.append(SessionPlayer(player_id=players[0].id, score=5, winner=False))
    db_session.commit()

    repo = PlayerRepository(db_session)

    result = repo.get_player_scores_for_game(user.id, players[0].id, board_game.id)

    assert [(sp.session_id, sp.score, sp.winner) for sp in result] == [(game_session.id, 11, True)]


def test_get_player_scores_for_game_reject_other_user(db_session, other_user, players, board_game):
    repo = PlayerRepository(db_session)

    with pytest.raises(NotFoundException, match="Player"):
        repo.get_player_scores_for_game(other_user.id, players[0].id, board_game.id)


def test_get_player_scores_all(db_session, user, players, game_session, make_game_session):
    other_game = BoardGame(title="Azul", user_id=user.id)
    db_session.add(other_game)
    db_session.commit()

    other_session = make_game_session(user, other_game)
    other_session.session_players.append(SessionPlayer(player_id=players[0].id, score=5, winner=False))
    db_session.commit()

    repo = PlayerRepository(db_session)

    result = repo.get_player_scores_all(user.id, players[0].id)

    results = {sp.session_id: (sp.score, sp.winner) for sp in result}
    assert results == {
        game_session.id: (11, True),
        other_session.id: (5, False),
    }


def test_get_player_scores_all_reject_other_user(db_session, other_user, players):
    repo = PlayerRepository(db_session)

    with pytest.raises(NotFoundException, match="Player"):
        repo.get_player_scores_all(other_user.id, players[0].id)


def test_get_player_games_returns_distinct_games(db_session, user, players, board_game, game_session,
                                                 make_game_session):
    second_session = make_game_session(user, board_game)
    second_session.session_players.append(SessionPlayer(player_id=players[0].id, score=7, winner=True))

    other_game = BoardGame(title="Azul", user_id=user.id)
    unplayed_game = BoardGame(title="Risiko", user_id=user.id)
    db_session.add_all([other_game, unplayed_game])
    db_session.commit()

    other_session = make_game_session(user, other_game)
    other_session.session_players.append(SessionPlayer(player_id=players[0].id, score=5, winner=False))
    db_session.commit()

    repo = PlayerRepository(db_session)

    result = repo.get_player_games(user.id, players[0].id)

    assert len(result) == 2
    assert {g.id for g in result} == {board_game.id, other_game.id}


def test_get_player_games_reject_other_user(db_session, other_user, players):
    repo = PlayerRepository(db_session)

    with pytest.raises(NotFoundException, match="Player"):
        repo.get_player_games(other_user.id, players[0].id)
