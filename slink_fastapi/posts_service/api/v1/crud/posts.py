from core.db.generics import GenericService
from models import Post


class PostService(GenericService):
    class Meta:
        model = Post
