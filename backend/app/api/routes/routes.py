from fastapi import APIRouter
from app.schemas.common import ApiResponse
from app.schemas.route import RouteQuery, RouteResult
from app.services.mock_map_service import MockMapService
router = APIRouter(prefix="/routes", tags=["routes"]); service = MockMapService()
@router.post("/query", response_model=ApiResponse[RouteResult])
def query(request: RouteQuery): return ApiResponse(data=service.query(request))
