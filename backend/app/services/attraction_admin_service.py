from sqlalchemy.orm import Session

from app.core.exceptions import BusinessError
from app.models.attraction import Attraction
from app.repositories.attraction_repo import AttractionRepository
from app.schemas.attraction import AttractionWrite


class AttractionAdminService:
    def __init__(self):
        self.repo = AttractionRepository()

    def create(self, db: Session, data: AttractionWrite) -> Attraction:
        return self.repo.create(db, data)

    def update(self, db: Session, attraction_id: int, data: AttractionWrite) -> Attraction:
        attraction = self._get_or_raise(db, attraction_id)
        return self.repo.update(db, attraction, data)

    def delete(self, db: Session, attraction_id: int) -> None:
        self.repo.delete(db, self._get_or_raise(db, attraction_id))

    def _get_or_raise(self, db: Session, attraction_id: int) -> Attraction:
        attraction = self.repo.get(db, attraction_id)
        if not attraction:
            raise BusinessError("ATTRACTION_NOT_FOUND", "景点不存在", 404)
        return attraction
