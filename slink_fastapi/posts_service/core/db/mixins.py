from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_
from pydantic import BaseModel
from core.db.services import BaseService
from fastapi import HTTPException


class CreateMixin(BaseService):
    """
    Миксин для создания записи.
    """

    async def create(self, session: AsyncSession, data: BaseModel):
        instance = self.Meta.model(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance


class ListMixin(BaseService):
    """
    Миксин для получения списка записей с фильтрами.
    """

    async def get_list(self, session: AsyncSession, filters: list = None):
        query = select(self.Meta.model).order_by(self.Meta.model.id)
        if filters:
            query = query.where(and_(*filters))
        result = await session.execute(query)
        return result.scalars().all()


class RetrieveMixin(BaseService):
    """
    Миксин для получения одной записи по ID или другим условиям.
    """

    async def get(
        self, session: AsyncSession, model_id: int = None, filters: list = None
    ):
        query = select(self.Meta.model).order_by(self.Meta.model.id)
        if model_id is not None:
            query = query.where(self.Meta.model.id == model_id)
        if filters:
            query = query.where(and_(*filters))
        result = await session.execute(query)
        instance = result.scalars().first()
        if not instance:
            raise HTTPException(
                status_code=404,
                detail=f"{self.Meta.model.__name__} не найден.",
            )
        return instance


class UpdateMixin(BaseService):
    """
    Миксин для полного обновления записи с фильтрами.
    """

    async def update(
        self,
        session: AsyncSession,
        id_or_instance,
        data: BaseModel,
        filters: list = None,
    ):
        if isinstance(id_or_instance, int):
            query = select(self.Meta.model).where(self.Meta.model.id == id_or_instance)
            if filters:
                query = query.where(and_(*filters))
            result = await session.execute(query)
            instance = result.scalars().first()
            if not instance:
                raise HTTPException(
                    status_code=404,
                    detail=f"{self.Meta.model.__name__} с id {id_or_instance} не найден.",
                )
        else:
            instance = id_or_instance

        for field, value in data.model_dump().items():
            setattr(instance, field, value)
        session.add(instance)
        await session.commit()
        return instance


class UpdatePartialMixin(BaseService):
    """
    Миксин для частичного обновления записи с фильтрами.
    """

    async def update_partial(
        self,
        session: AsyncSession,
        id_or_instance,
        data: BaseModel,
        filters: list = None,
    ):
        if isinstance(id_or_instance, int):
            query = select(self.Meta.model).where(self.Meta.model.id == id_or_instance)
            if filters:
                query = query.where(and_(*filters))
            result = await session.execute(query)
            instance = result.scalars().first()
            if not instance:
                raise HTTPException(
                    status_code=404,
                    detail=f"{self.Meta.model.__name__} с id {id_or_instance} не найден.",
                )
        else:
            instance = id_or_instance

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, field, value)
        session.add(instance)
        await session.commit()
        return instance


class DeleteMixin(BaseService):
    """
    Миксин для удаления записи с фильтрами.
    """

    async def delete(self, session: AsyncSession, id_or_instance, filters: list = None):
        if isinstance(id_or_instance, int):
            query = select(self.Meta.model).where(self.Meta.model.id == id_or_instance)
            if filters:
                query = query.where(and_(*filters))
            result = await session.execute(query)
            instance = result.scalars().first()
            if not instance:
                raise HTTPException(
                    status_code=404,
                    detail=f"{self.Meta.model.__name__} с id {id_or_instance} не найден.",
                )
        else:
            instance = id_or_instance

        await session.delete(instance)
        await session.commit()
        return {"message": "Запись успешно удалена"}
