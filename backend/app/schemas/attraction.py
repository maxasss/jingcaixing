from pydantic import BaseModel
class AttractionOut(BaseModel):
    attraction_id: int; name: str; category: str; description: str; duration: int
    opening_hours: str; latitude: float; longitude: float; image_path: str | None
    model_config = {"from_attributes": True}
