import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import Integer, String, DateTime, UUID
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


CreatedAt = Annotated[
    datetime, mapped_column(DateTime, default=datetime.now, nullable=False)
]

URL = Annotated[str, mapped_column(String(200), nullable=False)]

UserID = Annotated[int, mapped_column(Integer, nullable=False)]
