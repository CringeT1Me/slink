from sqlalchemy import Table, Column, ForeignKey
from .base import Base

post_images = Table(
    "post_images",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("image_id", ForeignKey("images.id", ondelete="CASCADE"), primary_key=True),
)
