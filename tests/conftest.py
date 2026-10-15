from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.community.postgres import PostgresContainer

from app.database import get_db
from app.main import app
from app.models import Base
from app.models import BoardGame, Player, User, GameSession, SessionPlayer
from tests.constants import TEST_PASSWORD_HASH, TEST_PASSWORD


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        engine = create_engine(postgres.get_connection_url())
        yield engine
        engine.dispose()


@pytest.fixture
def db_session(engine):
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    # https so that secure cookies (COOKIE_SECURE=true) are sent back as well
    with TestClient(app, base_url="https://testserver") as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def logged_in_client(client, user):
    response = client.post("/auth/login", data={"username": user.username, "password": TEST_PASSWORD})

    assert response.status_code == 200, response.text

    return client


@pytest.fixture
def user(db_session):
    user = User(username="Max", hashed_password=TEST_PASSWORD_HASH)
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def other_user(db_session):
    user = User(username="Moritz", hashed_password=TEST_PASSWORD_HASH)
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def board_game(db_session, user):
    board_game = BoardGame(title="Catan", user_id=user.id)
    db_session.add(board_game)
    db_session.commit()
    return board_game


@pytest.fixture
def players(db_session, user):
    players = [
        Player(name="Anna", user_id=user.id),
        Player(name="Ben", user_id=user.id),
    ]
    db_session.add_all(players)
    db_session.commit()
    return players


@pytest.fixture
def game_session(db_session, user, board_game, players):
    game_session = GameSession(
        user_id=user.id,
        date=date(2026, 1, 1),
        game_id=board_game.id,
        session_players=[
            SessionPlayer(player=players[0], score=11, winner=True),
            SessionPlayer(player=players[1], score=10, winner=False)
        ]
    )

    db_session.add(game_session)
    db_session.commit()
    return game_session


@pytest.fixture
def make_game_session(db_session):
    def _make(owner, board_game, session_date=date(2026, 1, 1)):
        game_session = GameSession(user_id=owner.id, game_id=board_game.id, date=session_date)
        db_session.add(game_session)
        db_session.commit()
        return game_session

    return _make
