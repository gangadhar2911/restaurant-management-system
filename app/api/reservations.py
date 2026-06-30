from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.reservation import Reservation
from app.models.restaurant_table import RestaurantTable

router = APIRouter(prefix="/reservations", tags=["Reservations"])


# -------------------------
# CREATE RESERVATION
# -------------------------
@router.post("/")
def create_reservation(data: dict, db: Session = Depends(get_db)):

    table = db.query(RestaurantTable).filter(
        RestaurantTable.id == data.get("table_id")
    ).first()

    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    if table.status != "Available":
        raise HTTPException(status_code=400, detail="Table not available")

    reservation = Reservation(
        user_id=data.get("user_id"),
        table_id=data.get("table_id"),
        reservation_time=data.get("reservation_time"),
        guests_count=data.get("guests_count"),
        status="Confirmed"
    )

    # Mark table as reserved
    table.status = "Reserved"

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return {
        "message": "Reservation created successfully",
        "reservation_id": reservation.id
    }


# -------------------------
# GET ALL RESERVATIONS
# -------------------------
@router.get("/")
def get_all_reservations(db: Session = Depends(get_db)):

    return db.query(Reservation).order_by(Reservation.id.desc()).all()


# -------------------------
# GET RESERVATION BY ID
# -------------------------
@router.get("/{reservation_id}")
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):

    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    return reservation


# -------------------------
# CANCEL RESERVATION
# -------------------------
@router.delete("/{reservation_id}")
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):

    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Free the table again
    table = db.query(RestaurantTable).filter(
        RestaurantTable.id == reservation.table_id
    ).first()

    if table:
        table.status = "Available"

    db.delete(reservation)
    db.commit()

    return {"message": "Reservation cancelled successfully"}