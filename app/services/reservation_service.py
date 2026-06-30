from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.reservation_repository import ReservationRepository
from app.repositories.table_repository import TableRepository

repo = ReservationRepository()
table_repo = TableRepository()


class ReservationService:
    @staticmethod
    def create(db: Session, data: dict):
        table = table_repo.get_by_id(db, data.get("table_id"))
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")
        if table.status != "Available":
            raise HTTPException(status_code=400, detail="Table not available")

        reservation = repo.create(db, {**data, "status": "Confirmed"})
        table_repo.update(db, table, {"status": "Reserved"})
        return reservation

    @staticmethod
    def get_all(db: Session):
        return repo.get_all(db)

    @staticmethod
    def get_by_id(db: Session, reservation_id: int):
        obj = repo.get_by_id(db, reservation_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Reservation not found")
        return obj

    @staticmethod
    def cancel(db: Session, reservation_id: int):
        reservation = ReservationService.get_by_id(db, reservation_id)
        table = table_repo.get_by_id(db, reservation.table_id)
        if table:
            table_repo.update(db, table, {"status": "Available"})
        repo.delete(db, reservation)
        return {"message": "Reservation cancelled successfully"}