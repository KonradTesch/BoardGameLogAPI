from .base import RequestModel, ResponseModel

class RegisterRequest(RequestModel):
    name: str
    password: str

class AuthUserResponse(ResponseModel):
    id: int
    name: str