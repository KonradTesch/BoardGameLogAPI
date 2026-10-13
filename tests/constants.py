from app.repositories.user_repository import hash_password

TEST_PASSWORD = "secret123"
TEST_PASSWORD_HASH = hash_password(TEST_PASSWORD)