import jwt
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from core.config import settings


def get_user_id_from_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        return payload.get("user_id")
    except jwt.PyJWTError:
        return None


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        token = request.headers.get("Authorization")
        if token:
            token = token.split(" ")[1] if token.startswith("Bearer ") else token
            user_id = get_user_id_from_token(token)
            if user_id:
                request.user.id = user_id
            else:
                raise HTTPException(status_code=401, detail="Неверный токен")
        else:
            raise HTTPException(status_code=401, detail="Пользователь не авторизован")
        response = await call_next(request)
        return response
