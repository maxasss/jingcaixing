from typing import Literal
from pydantic import BaseModel, Field
Interest = Literal["历史人文", "自然风光", "美食探店"]
Pace = Literal["轻松", "适中", "紧凑"]
class PlanRequest(BaseModel):
    days: int = Field(ge=1, le=7); interests: list[Interest] = Field(min_length=1); pace: Pace
class PlanItem(BaseModel): attraction_id: int; order: int
class DayPlan(BaseModel): day: int; attractions: list[PlanItem]
class Itinerary(BaseModel): days: int; interests: list[Interest]; pace: Pace; daily_plans: list[DayPlan]
class EditPlanRequest(BaseModel):
    itinerary: Itinerary; day: int = Field(ge=1, le=7); attraction_id: int = Field(gt=0)
