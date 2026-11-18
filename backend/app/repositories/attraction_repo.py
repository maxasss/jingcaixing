from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.attraction import Attraction
from app.schemas.attraction import AttractionWrite
class AttractionRepository:
    def list(self, db: Session, category: str | None = None, keyword: str | None = None) -> list[Attraction]:
        stmt = select(Attraction)
        if category: stmt = stmt.where(Attraction.category == category)
        if keyword: stmt = stmt.where(Attraction.name.contains(keyword))
        return list(db.scalars(stmt.order_by(Attraction.attraction_id)).all())
    def get(self, db: Session, attraction_id: int) -> Attraction | None: return db.get(Attraction, attraction_id)
    def create(self, db: Session, data: AttractionWrite) -> Attraction:
        attraction = Attraction(**data.model_dump())
        db.add(attraction); db.commit(); db.refresh(attraction)
        return attraction
    def update(self, db: Session, attraction: Attraction, data: AttractionWrite) -> Attraction:
        for field, value in data.model_dump().items(): setattr(attraction, field, value)
        db.commit(); db.refresh(attraction)
        return attraction
    def delete(self, db: Session, attraction: Attraction) -> None:
        db.delete(attraction); db.commit()
