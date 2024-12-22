from typing import Annotated

from api.v1.crud.posts import PostService
from core.db.db_helper import db_helper
from core.dependencies.get_user_from_jwt import get_current_user
from schemas.post import Post, PostCreate, PostUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from models.post import Post as PostModel

router = APIRouter(tags=["Posts"])

post_service = PostService()


@router.post("/", response_model=Post, status_code=201)
async def create_post(
    payload: PostCreate,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_dependency),
    ],
    current_user_id: Annotated[int, Depends(get_current_user)],
):
    """
    Создать новый пост.
    """

    payload.user_id = current_user_id
    return await post_service.create(session=session, data=payload)


@router.get("/", response_model=list[Post])
async def get_posts(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_dependency),
    ],
):
    """
    Получить список неархивированных постов.
    """

    filters = [PostModel.is_archived == False]
    return await post_service.get_list(session=session, filters=filters)


@router.get("/archived", response_model=list[Post])
async def get_posts_archived(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_dependency),
    ],
    current_user_id: Annotated[int, Depends(get_current_user)],
):
    """
    Получить список архивированных постов текущего пользователя.
    """

    filters = [PostModel.is_archived == True, PostModel.user_id == current_user_id]
    return await post_service.get_list(session=session, filters=filters)


@router.get("/{post_id}", response_model=Post)
async def get_post(
    post_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_dependency),
    ],
):
    """
    Получить неархивированный пост.
    """

    filters = [PostModel.is_archived == False]
    return await post_service.get(session=session, model_id=post_id, filters=filters)


@router.get("/archived/{post_id}", response_model=Post)
async def get_post_archived(
    post_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_dependency),
    ],
    current_user_id: Annotated[int, Depends(get_current_user)],
):
    """
    Получить архивированный пост.
    Доступ только для владельца поста.
    """

    filters = [PostModel.is_archived == True, PostModel.user_id == current_user_id]
    return await post_service.get(session=session, model_id=post_id, filters=filters)


@router.put("/{post_id}", response_model=Post)
async def update_post(
    post_id: int,
    payload: PostUpdate,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_dependency),
    ],
    current_user_id: Annotated[int, Depends(get_current_user)],
):
    """
    Обновить пост.
    Доступ только для владельца поста.
    """

    filters = [PostModel.user_id == current_user_id]
    return await post_service.update(
        session=session, id_or_instance=post_id, data=payload, filters=filters
    )


@router.patch("/{post_id}", response_model=Post)
async def update_partial_post(
    post_id: int,
    payload: PostUpdate,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_dependency),
    ],
    current_user_id: Annotated[int, Depends(get_current_user)],
):
    """
    Обновить данные поста.
    Доступ только для владельца поста.
    """

    filters = [PostModel.user_id == current_user_id]
    return await post_service.update_partial(
        session=session, id_or_instance=post_id, data=payload, filters=filters
    )


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_dependency),
    ],
    current_user_id: Annotated[int, Depends(get_current_user)],
):
    """
    Удалить пост.
    Доступ только для владельца поста.
    """

    filters = [PostModel.user_id == current_user_id]

    return await post_service.delete(
        session=session, id_or_instance=post_id, filters=filters
    )
