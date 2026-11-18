from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.attraction import Attraction
class AttractionRepository:
    def list(self, db: Session, category: str | None = None, keyword: str | None = None) -> list[Attraction]:
        stmt = select(Attraction)
        if category: stmt = stmt.where(Attraction.category == category)
        if keyword: stmt = stmt.where(Attraction.name.contains(keyword))
        return list(db.scalars(stmt.order_by(Attraction.attraction_id)).all())
    def get(self, db: Session, attraction_id: int) -> Attraction | None: return db.get(Attraction, attraction_id)
