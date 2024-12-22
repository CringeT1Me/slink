import uuid

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, URL, CreatedAt, UserID
from .relations import post_images
from .post import Post


class Album(Base):
    user_id: Mapped[UserID]
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[CreatedAt]

    images: Mapped[list["Image"]] = relationship(back_populates="album")

    __table_args__ = (UniqueConstraint("user_id", "name", name="uix_user_id_name"),)

    @classmethod
    def create_post_album(cls, user_id: uuid.UUID, **kwargs) -> "Album":
        """Создает альбом с именем 'Посты'."""
        return cls(user_id=user_id, name="Посты", **kwargs)

    @classmethod
    def create_avatar_album(cls, user_id: uuid.UUID, **kwargs) -> "Album":
        """Создает альбом с именем 'Аватарки'."""
        return cls(user_id=user_id, name="Аватарки", **kwargs)


class Image(Base):
    user_id: Mapped[UserID]
    url: Mapped[URL]
    created_at: Mapped[CreatedAt]

    album_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("albums.id"), nullable=False)
    album: Mapped["Album"] = relationship(back_populates="images")
    posts: Mapped[list["Post"]] = relationship(
        "Post", secondary=post_images, back_populates="images"
    )
