from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.attraction_repo import AttractionRepository
from app.schemas.attraction import AttractionOut, AttractionWrite
from app.schemas.common import ApiResponse
from app.services.attraction_admin_service import AttractionAdminService

router = APIRouter(prefix="/admin/attractions", tags=["admin-attractions"])
repo = AttractionRepository()
service = AttractionAdminService()

@router.get("", response_model=ApiResponse[list[AttractionOut]])
def list_all(db: Session = Depends(get_db)):
    return ApiResponse(data=repo.list(db))

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[AttractionOut])
def create(data: AttractionWrite, db: Session = Depends(get_db)):
    return ApiResponse(data=service.create(db, data))

@router.put("/{attraction_id}", response_model=ApiResponse[AttractionOut])
def update(attraction_id: int, data: AttractionWrite, db: Session = Depends(get_db)):
    return ApiResponse(data=service.update(db, attraction_id, data))

@router.delete("/{attraction_id}", response_model=ApiResponse[None])
def delete(attraction_id: int, db: Session = Depends(get_db)):
    service.delete(db, attraction_id)
    return ApiResponse(message="景点已删除")
