from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.plan import EditPlanRequest, Itinerary, PlanRequest
from app.services.plan_service import PlanService
router = APIRouter(prefix="/plans", tags=["plans"]); service = PlanService()
@router.post("/generate", response_model=ApiResponse[Itinerary])
def generate(request: PlanRequest, db: Session = Depends(get_db)): return ApiResponse(data=service.generate(db, request))
@router.post("/edit/add", response_model=ApiResponse[Itinerary])
def add(request: EditPlanRequest, db: Session = Depends(get_db)): return ApiResponse(data=service.add(db, request))
@router.post("/edit/delete", response_model=ApiResponse[Itinerary])
def delete(request: EditPlanRequest): return ApiResponse(data=service.delete(request))
