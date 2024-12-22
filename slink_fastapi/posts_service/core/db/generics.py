from core.db.mixins import (
    CreateMixin,
    RetrieveMixin,
    ListMixin,
    UpdateMixin,
    UpdatePartialMixin,
    DeleteMixin,
)


class GenericService(
    CreateMixin,
    RetrieveMixin,
    ListMixin,
    UpdateMixin,
    UpdatePartialMixin,
    DeleteMixin,
):
    pass
