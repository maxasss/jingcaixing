from typing import Literal
from pydantic import BaseModel, Field

Category = Literal["历史人文", "自然风光", "美食探店"]

class AttractionOut(BaseModel):
    attraction_id: int; name: str; category: str; description: str; duration: int
    opening_hours: str; latitude: float; longitude: float; image_path: str | None
    model_config = {"from_attributes": True}

class AttractionWrite(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: Category
    description: str = Field(min_length=1)
    duration: int = Field(gt=0, le=1440)
    opening_hours: str = Field(min_length=1, max_length=100)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    image_path: str | None = Field(default=None, max_length=255)
