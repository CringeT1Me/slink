from typing import Annotated, List

from pydantic import BaseModel, Field, HttpUrl


class Base(BaseModel):
    id: int = Field(ge=1)


Images = Annotated[
    List[HttpUrl], Field(default=[], description="Список url изображений")
]
