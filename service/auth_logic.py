from fastapi import  HTTPException, Cookie, status
from jose import jwt, JWTError
from dotenv import load_dotenv
from os import getenv

from BoardGameLogAPI.custom_exceptions import UnauthorizedException

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")

def create_access_token(username: str, user_id: int):
    encode = {'sub': username, 'id': user_id}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise UnauthorizedException("Missing access token")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise UnauthorizedException("Could not validate user.")

        return {"username": username, "id": user_id}
    except JWTError:
        raise UnauthorizedException("Invalid or expired access token")
