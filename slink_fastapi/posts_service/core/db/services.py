from models import Base


class BaseService:
    class Meta:
        model = Base

    def __init__(self):
        if not hasattr(self, "Meta"):
            raise NotImplementedError("Класс должен содержать вложенный класс 'Meta'.")
        if not hasattr(self.Meta, "model"):
            raise NotImplementedError("'Meta' должен содержать атрибут 'model'.")
