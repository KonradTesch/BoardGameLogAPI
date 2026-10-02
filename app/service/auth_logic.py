from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError

from app.config import settings
from app.custom_exceptions import UnauthorizedException


@dataclass(frozen=True)
class TokenPayload:
    user_id: int
    token_version: int
    issued_at: datetime

def create_access_token(user_id: int, token_version: int):
    now = datetime.now(timezone.utc)

    encode = {
        'sub': str(user_id),
        'ver': token_version,
        'iat': now,
        'exp': now + timedelta(days=settings.access_token_expire_days)

    }
    return jwt.encode(encode, settings.secret_key, algorithm=settings.algorithm)

def decode_access_token(token: str | None) -> TokenPayload:
    if not token:
        raise UnauthorizedException("Missing access token.")
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return TokenPayload(
            user_id=int(payload["sub"]),
            token_version=int(payload["ver"]),
            issued_at=datetime.fromtimestamp(payload["iat"], tz=timezone.utc),
        )
    except (JWTError, KeyError, ValueError):
        raise UnauthorizedException("Invalid or expired access token.")
