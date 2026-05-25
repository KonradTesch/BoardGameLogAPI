from app.schemas.base import RequestModel

class PasswordChangeRequest(RequestModel):
    old_password: str
    new_password: str


class ChangeUsernameRequest(RequestModel):
    new_username: str