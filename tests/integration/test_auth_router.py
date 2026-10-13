from datetime import datetime, timedelta, timezone

from jose import jwt
from sqlalchemy import select

from app.config import settings
from app.models import User
from app.repositories.user_repository import verify_password
from app.service.auth_logic import decode_access_token
from tests.constants import TEST_PASSWORD


def _make_token(user_id, issued_at, secret_key=settings.secret_key):
    encode = {
        "sub": str(user_id),
        "ver": 0,
        "iat": issued_at,
        "exp": issued_at + timedelta(days=settings.access_token_expire_days),
    }
    return jwt.encode(encode, secret_key, algorithm=settings.algorithm)


def test_login_sets_auth_cookie(client, user):
    response = client.post("/auth/login", data={"username": user.username, "password": TEST_PASSWORD})

    assert response.status_code == 200, response.text
    assert response.json()["id"] == user.id
    assert response.json()["username"] == user.username
    assert "access_token" in response.cookies


def test_login_rejected_wrong_password(client, user):
    response = client.post("/auth/login", data={"username": user.username, "password": "wrong_password"})

    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Incorrect username or password"
    assert "access_token" not in response.cookies


def test_login_rejected_unknown_user(client, user):
    response = client.post("/auth/login", data={"username": "unknown_user", "password": TEST_PASSWORD})

    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Incorrect username or password"
    assert "access_token" not in response.cookies


def test_register_creates_user(db_session, client):
    password = "new_password"
    response = client.post("/auth/register", json={"username": "Tom", "password": password})

    assert response.status_code == 201, response.text
    assert response.json()["message"] == "Registration successful"

    created_user = db_session.scalars(select(User).where(User.username == "Tom")).first()

    assert created_user is not None
    assert created_user.hashed_password != password
    assert verify_password(password, created_user.hashed_password)


def test_register_reject_existing_username(db_session, client, user):
    response = client.post("/auth/register", json={"username": user.username, "password": "new_password"})

    assert response.status_code == 409, response.text
    assert response.json()["detail"] == f"Username '{user.username}' already exists"

    users = db_session.scalars(select(User).where(User.username == user.username)).all()

    assert len(users) == 1
    assert verify_password(TEST_PASSWORD, users[0].hashed_password)


def test_get_auth_user_returns_current_user(logged_in_client, user):
    response = logged_in_client.get("/auth/user")

    assert response.status_code == 200, response.text
    assert response.json() == {"id": user.id, "username": user.username}
    assert "access_token" not in response.cookies


def test_get_auth_user_without_cookie(client):
    response = client.get("/auth/user")

    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Missing access token."


def test_get_auth_user_invalid_token(client):
    client.cookies.set("access_token", "garbage")

    response = client.get("/auth/user")

    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Invalid or expired access token."


def test_get_auth_user_token_signed_with_wrong_key(client, user):
    token = _make_token(user.id, datetime.now(timezone.utc), secret_key="wrong-secret-key")
    client.cookies.set("access_token", token)

    response = client.get("/auth/user")

    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Invalid or expired access token."


def test_get_auth_user_unknown_user(client, user):
    token = _make_token(user.id + 999, datetime.now(timezone.utc))
    client.cookies.set("access_token", token)

    response = client.get("/auth/user")

    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Invalid or expired access token."


def test_get_auth_user_rejects_expired_token(client, user):
    issued_at = datetime.now(timezone.utc) - timedelta(days=settings.access_token_expire_days + 1)
    client.cookies.set("access_token", _make_token(user.id, issued_at))

    response = client.get("/auth/user")

    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Invalid or expired access token."
    assert "access_token" not in response.cookies


def test_get_auth_user_renews_old_token(client, user):
    issued_at = datetime.now(timezone.utc) - timedelta(hours=settings.token_renew_after_hours + 1)
    old_token = _make_token(user.id, issued_at)
    client.cookies.set("access_token", old_token)

    response = client.get("/auth/user")

    assert response.status_code == 200, response.text
    assert response.json() == {"id": user.id, "username": user.username}

    new_token = response.cookies.get("access_token")

    assert new_token is not None
    assert new_token != old_token
    assert decode_access_token(new_token).user_id == user.id


def test_get_auth_user_does_not_renew_fresh_token(client, user):
    token = _make_token(user.id, datetime.now(timezone.utc) - timedelta(hours=1))
    client.cookies.set("access_token", token)

    response = client.get("/auth/user")

    assert response.status_code == 200, response.text
    assert "access_token" not in response.cookies


def test_logout_clears_auth_cookie(logged_in_client):
    response = logged_in_client.post("/auth/logout")

    assert response.status_code == 200, response.text

    response = logged_in_client.get("/auth/user")

    assert response.status_code == 401, response.text


def test_logout_without_cookie(client):
    response = client.post("/auth/logout")

    assert response.status_code == 200, response.text
