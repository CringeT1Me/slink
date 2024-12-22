from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from core.config import settings

security = HTTPBearer()


async def decode_token(token: str) -> int:
    """
    Декодирует JWT и извлекает user_id.
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Поле user_id отсутствует в токене"
            )
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен больше не действителен")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Неверный токен")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """
    Извлекает и проверяет токен из заголовка Authorization.
    """
    token = credentials.credentials
    return await decode_token(token)
