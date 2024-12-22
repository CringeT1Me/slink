import asyncio

import pytest
from datetime import datetime, timedelta
import jwt
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from core.config import settings
from schemas.post import PostCreate
from main import app

import logging

logging.basicConfig(level=logging.DEBUG)


@pytest.yield_fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def token() -> str:
    """
    Фикстура для JWT токена.
    """
    payload = {
        "user_id": 123,
        "exp": datetime.now() + timedelta(hours=1),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


# Фикстура для создания клиента
@pytest_asyncio.fixture(name="client")
async def client(token: str) -> AsyncClient:
    """
    Фикстура для создания клиента
    """

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {token}"},
    ) as client:
        yield client


# Фикстура для создания поста
@pytest.fixture
def create_post_payload() -> PostCreate:
    """
    Фикстура для создания поста
    """

    return PostCreate(text="Test Post")
