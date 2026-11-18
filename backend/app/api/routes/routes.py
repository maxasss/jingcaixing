from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import get_db
from app.core.exceptions import BusinessError
from app.repositories.attraction_repo import AttractionRepository
from app.schemas.common import ApiResponse
from app.schemas.route import RouteQuery, RouteResult
from app.services.mock_map_service import MockMapService
from app.services.amap_map_service import AMapMapService
router = APIRouter(prefix="/routes", tags=["routes"]); mock_service = MockMapService(); repo = AttractionRepository()
@router.post("/query", response_model=ApiResponse[RouteResult])
def query(request: RouteQuery, db: Session = Depends(get_db)):
    settings = get_settings()
    if settings.map_provider == "mock":
        return ApiResponse(data=mock_service.query(request))
    if settings.map_provider != "amap":
        raise BusinessError("MAP_PROVIDER_INVALID", "不支持的地图服务配置", 503)
    attractions = {item.attraction_id: item for item in repo.list(db)}
    return ApiResponse(data=AMapMapService(settings).query(request, attractions))
