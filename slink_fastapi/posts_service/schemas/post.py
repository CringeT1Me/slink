from datetime import datetime

from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema

from .base import Base, Images


class Post(Base):
    user_id: int = Field(ge=1)
    text: str | None = None
    created_at: datetime = datetime.now()
    is_archived: bool = False
    images: Images


class PostCreate(BaseModel):
    user_id: SkipJsonSchema[int] | None = None
    text: str | None = None
    is_archived: SkipJsonSchema[bool] | None = False
    images: Images


class PostUpdate(BaseModel):
    text: str | None = None
    is_archived: bool | None = False
    images: Images
