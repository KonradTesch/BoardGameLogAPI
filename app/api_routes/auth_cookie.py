from app.config import settings
from datetime import timedelta


def set_auth_cookie(response, token):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(timedelta(days=settings.access_token_expire_days).total_seconds()),
    )

def clear_auth_cookie(response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,
        samesite="lax",
    )