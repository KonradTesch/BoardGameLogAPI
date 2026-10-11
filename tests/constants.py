from app.repositories.user_repository import bcrypt_context

TEST_PASSWORD = "secret123"
TEST_PASSWORD_HASH = bcrypt_context.hash(TEST_PASSWORD)