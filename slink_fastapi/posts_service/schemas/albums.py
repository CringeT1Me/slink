import uuid
from datetime import datetime
from typing import List
from pydantic import Field
from .base import Base


class Album(Base):
    user: uuid.UUID
    name: str
    images: List["Image"] | list


class Image(Base):
    url: str
    created_at: datetime = datetime.now()
    album: "Album"
    posts: List[int] = Field(default=[], description="Список id постов.")
