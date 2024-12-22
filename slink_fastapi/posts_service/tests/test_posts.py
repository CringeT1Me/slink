import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from schemas.post import PostCreate, PostUpdate
from main import app


@pytest.mark.asyncio
async def test_create_post(client: AsyncClient, create_post_payload: PostCreate):
    response = await client.post(
        "/api/v1/posts/", json=create_post_payload.model_dump(exclude_unset=True)
    )
    print(create_post_payload.model_dump())
    print(response)
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    assert response.json()["text"] == create_post_payload.text


@pytest.mark.asyncio
async def test_get_posts(client: AsyncClient):
    response = await client.get("/api/v1/posts/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_post(client: AsyncClient, create_post_payload: PostCreate):
    create_response = await client.post(
        "/api/v1/posts/", json=create_post_payload.model_dump(exclude_unset=True)
    )
    post_id = create_response.json()["id"]
    response = await client.get(f"/api/v1/posts/{post_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == post_id


@pytest.mark.asyncio
async def test_get_post_not_found(client: AsyncClient):
    response = await client.get("/api/v1/posts/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_post(client: AsyncClient, create_post_payload: PostCreate):
    create_response = await client.post(
        "/api/v1/posts/", json=create_post_payload.model_dump(exclude_unset=True)
    )
    post_id = create_response.json()["id"]
    update_payload = PostUpdate(text="Updated Title")
    response = await client.patch(
        f"/api/v1/posts/{post_id}", json=update_payload.model_dump(exclude_unset=True)
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == post_id
    assert data["text"] == update_payload.text


@pytest.mark.asyncio
async def test_update_post_not_found(client: AsyncClient):
    update_payload = PostUpdate(text="Updated Title")
    response = await client.patch(
        "/api/v1/posts/9999", json=update_payload.model_dump(exclude_unset=True)
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_post(client: AsyncClient, create_post_payload: PostCreate):
    create_response = await client.post(
        "/api/v1/posts/", json=create_post_payload.model_dump(exclude_unset=True)
    )
    post_id = create_response.json()["id"]
    response = await client.delete(f"/api/v1/posts/{post_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Запись успешно удалена"}


@pytest.mark.asyncio
async def test_delete_post_not_found(client: AsyncClient):
    response = await client.delete("/api/v1/posts/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_unauthorized_create_post(create_post_payload: PostCreate):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"Authorization": "Bearer invalid_token"},
    ) as client:
        response = await client.post(
            "/api/v1/posts/",
            json={"text": "Updated Title"},
        )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
