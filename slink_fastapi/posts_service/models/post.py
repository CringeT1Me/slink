from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, CreatedAt, UserID
from .relations import post_images

if TYPE_CHECKING:
    from .album import Image


class Post(Base):
    user_id: Mapped[UserID]
    text: Mapped[str | None] = mapped_column(String(2000))
    created_at: Mapped[CreatedAt]
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    images: Mapped[list["Image"]] = relationship(
        "Image", secondary=post_images, back_populates="posts", lazy="selectin"
    )
