from .base import RequestModel

class RegisterRequest(RequestModel):
    name: str
    password: str