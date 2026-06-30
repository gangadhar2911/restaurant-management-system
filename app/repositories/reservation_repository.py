from sqlalchemy.orm import Session
from app.models.reservation import Reservation


class ReservationRepository:
    def create(self, db: Session, data: dict) -> Reservation:
        obj = Reservation(**data)
        db.add(obj); db.commit(); db.refresh(obj)
        return obj

    def get_all(self, db: Session):
        return db.query(Reservation).order_by(Reservation.id.desc()).all()

    def get_by_id(self, db: Session, reservation_id: int):
        return db.query(Reservation).filter(Reservation.id == reservation_id).first()

    def update(self, db: Session, obj: Reservation, data: dict) -> Reservation:
        for k, v in data.items():
            setattr(obj, k, v)
        db.commit(); db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: Reservation) -> None:
        db.delete(obj); db.commit()