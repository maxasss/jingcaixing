from sqlalchemy.orm import Session
from app.core.exceptions import BusinessError
from app.repositories.attraction_repo import AttractionRepository
from app.schemas.plan import DayPlan, EditPlanRequest, Itinerary, PlanItem, PlanRequest
from app.services.mock_ai_service import MockAIService
class PlanService:
    def __init__(self): self.repo, self.mock_ai = AttractionRepository(), MockAIService()
    def generate(self, db: Session, request: PlanRequest) -> Itinerary: return self.mock_ai.generate(request, self.repo.list(db))
    def add(self, db: Session, request: EditPlanRequest) -> Itinerary:
        if not self.repo.get(db, request.attraction_id): raise BusinessError("ATTRACTION_NOT_FOUND", "景点不存在", 404)
        return self._edit(request, True)
    def delete(self, request: EditPlanRequest) -> Itinerary: return self._edit(request, False)
    def _edit(self, request: EditPlanRequest, add: bool) -> Itinerary:
        plan = request.itinerary.model_copy(deep=True)
        day = next((item for item in plan.daily_plans if item.day == request.day), None)
        if not day: day = DayPlan(day=request.day, attractions=[]); plan.daily_plans.append(day)
        ids = [item.attraction_id for item in day.attractions]
        if add and request.attraction_id not in ids: day.attractions.append(PlanItem(attraction_id=request.attraction_id, order=len(ids) + 1))
        if not add and request.attraction_id not in ids: raise BusinessError("PLAN_ITEM_NOT_FOUND", "该景点不在指定日期中", 404)
        if not add: day.attractions = [item for item in day.attractions if item.attraction_id != request.attraction_id]
        for index, item in enumerate(day.attractions, start=1): item.order = index
        return plan
