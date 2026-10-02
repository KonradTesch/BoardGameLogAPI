from dataclasses import dataclass

@dataclass
class RegisterData:
    username: str
    password: str

@dataclass
class AuthUserData:
    id: int
    username: str