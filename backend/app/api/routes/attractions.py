from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.exceptions import BusinessError
from app.repositories.attraction_repo import AttractionRepository
from app.schemas.common import ApiResponse
from app.schemas.attraction import AttractionOut
router = APIRouter(prefix="/attractions", tags=["attractions"])
repo = AttractionRepository()
@router.get("", response_model=ApiResponse[list[AttractionOut]])
def list_attractions(category: str | None = None, keyword: str | None = Query(default=None), db: Session = Depends(get_db)):
    return ApiResponse(data=repo.list(db, category, keyword))
@router.get("/{attraction_id}", response_model=ApiResponse[AttractionOut])
def get_attraction(attraction_id: int, db: Session = Depends(get_db)):
    attraction = repo.get(db, attraction_id)
    if not attraction: raise BusinessError("ATTRACTION_NOT_FOUND", "景点不存在", 404)
    return ApiResponse(data=attraction)
