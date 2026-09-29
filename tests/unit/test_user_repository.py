import pytest

from app.custom_exceptions import NotFoundException, UnauthorizedException, UnprocessableException
from app.repositories.user_repository import UserRepository


def test_create_user_stores_user_with_hashed_password(db_session):
    repo = UserRepository(db_session)

    created = repo.create_user("Lisa", "secret")

    stored = repo.get_user_by_id(created.id)
    assert stored.username == "Lisa"
    assert stored.hashed_password != "secret"
    assert repo.authenticate_user("Lisa", "secret") == stored


def test_create_user_reject_duplicate_username(db_session, user):
    repo = UserRepository(db_session)

    with pytest.raises(UnprocessableException, match="already exists"):
        repo.create_user(user.username, "secret")

    assert len(repo.get_all_users()) == 1


def test_authenticate_user_valid(db_session):
    repo = UserRepository(db_session)
    created = repo.create_user("Lisa", "secret")

    assert repo.authenticate_user("Lisa", "secret") == created


def test_authenticate_user_reject_unknown_username(db_session):
    repo = UserRepository(db_session)

    with pytest.raises(NotFoundException, match="Username"):
        repo.authenticate_user("Unknown", "secret")


def test_authenticate_user_reject_wrong_password(db_session):
    repo = UserRepository(db_session)
    repo.create_user("Lisa", "secret")

    with pytest.raises(UnauthorizedException, match="password"):
        repo.authenticate_user("Lisa", "wrong")


def test_update_username(db_session, user):
    repo = UserRepository(db_session)

    repo.update_username(user.id, "Lisa")

    stored = repo.get_user_by_id(user.id)
    assert stored.username == "Lisa"


def test_update_username_reject_duplicate_username(db_session, user, other_user):
    repo = UserRepository(db_session)

    with pytest.raises(UnprocessableException, match="already exists"):
        repo.update_username(user.id, other_user.username)

    stored = repo.get_user_by_id(user.id)
    assert stored.username == "Max"


def test_update_username_reject_unknown_user(db_session):
    repo = UserRepository(db_session)

    with pytest.raises(NotFoundException, match="User"):
        repo.update_username(-1, "Lisa")


def test_change_password(db_session):
    repo = UserRepository(db_session)
    created = repo.create_user("Lisa", "secret")

    repo.change_password(created.id, "secret", "new_secret")

    assert repo.authenticate_user("Lisa", "new_secret") == created
    with pytest.raises(UnauthorizedException):
        repo.authenticate_user("Lisa", "secret")


def test_change_password_reject_wrong_old_password(db_session):
    repo = UserRepository(db_session)
    created = repo.create_user("Lisa", "secret")

    with pytest.raises(UnauthorizedException, match="Old password"):
        repo.change_password(created.id, "wrong", "new_secret")

    assert repo.authenticate_user("Lisa", "secret") == created


def test_change_password_reject_unknown_user(db_session):
    repo = UserRepository(db_session)

    with pytest.raises(NotFoundException, match="User"):
        repo.change_password(-1, "secret", "new_secret")


def test_delete_user(db_session, user):
    repo = UserRepository(db_session)

    repo.delete_user(user.id)

    with pytest.raises(NotFoundException, match="User"):
        repo.get_user_by_id(user.id)


def test_delete_user_reject_unknown_user(db_session, user):
    repo = UserRepository(db_session)

    with pytest.raises(NotFoundException, match="User"):
        repo.delete_user(-1)

    assert repo.get_user_by_id(user.id) == user


def test_validate_user_valid(db_session, user):
    repo = UserRepository(db_session)

    assert repo.validate_user(user.id) == user


def test_validate_user_reject_unknown_user(db_session):
    repo = UserRepository(db_session)

    with pytest.raises(NotFoundException, match="User"):
        repo.validate_user(-1)


def test_get_user_by_id_valid(db_session, user):
    repo = UserRepository(db_session)

    assert repo.get_user_by_id(user.id) == user


def test_get_user_by_id_reject_unknown_user(db_session):
    repo = UserRepository(db_session)

    with pytest.raises(NotFoundException, match="User"):
        repo.get_user_by_id(-1)


def test_get_all_users(db_session, user, other_user):
    repo = UserRepository(db_session)

    result = repo.get_all_users()

    assert {u.id for u in result} == {user.id, other_user.id}


def test_get_all_users_without_users(db_session):
    repo = UserRepository(db_session)

    assert len(repo.get_all_users()) == 0
