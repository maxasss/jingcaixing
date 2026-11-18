from app.models.attraction import Attraction
from app.schemas.plan import DayPlan, Itinerary, PlanItem, PlanRequest
class MockAIService:
    def generate(self, request: PlanRequest, attractions: list[Attraction]) -> Itinerary:
        candidates = [item for item in attractions if item.category in request.interests] or attractions
        if not candidates: return Itinerary(days=request.days, interests=request.interests, pace=request.pace, daily_plans=[])
        count = {"轻松": 2, "适中": 3, "紧凑": 4}[request.pace]; used: set[int] = set(); cursor = 0; daily = []
        for day in range(1, request.days + 1):
            selected = []
            while len(selected) < min(count, len(candidates)) and cursor < len(candidates) * 2:
                candidate = candidates[cursor % len(candidates)]; cursor += 1
                if candidate.attraction_id not in used: used.add(candidate.attraction_id); selected.append(candidate)
            daily.append(DayPlan(day=day, attractions=[PlanItem(attraction_id=a.attraction_id, order=i + 1) for i, a in enumerate(selected)]))
        return Itinerary(days=request.days, interests=request.interests, pace=request.pace, daily_plans=daily)
