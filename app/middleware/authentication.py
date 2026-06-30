from fastapi import Request
from app.core.security import decode_token


def get_token(request: Request):

    auth = request.headers.get("Authorization")

    if not auth:
        return None

    try:
        scheme, token = auth.split()

        if scheme.lower() != "bearer":
            return None

        return token

    except Exception:
        return None


def authenticate_request(request: Request):

    token = get_token(request)

    if not token:
        return None

    return decode_token(token)