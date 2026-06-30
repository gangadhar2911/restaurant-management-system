from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.bill import Bill
from app.models.order import Order
from app.models.payment import Payment

router = APIRouter(prefix="/billing", tags=["Billing"])


# -------------------------
# GENERATE BILL FROM ORDER
# -------------------------
@router.post("/generate/{order_id}")
def generate_bill(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    existing_bill = db.query(Bill).filter(Bill.order_id == order_id).first()

    if existing_bill:
        raise HTTPException(status_code=400, detail="Bill already generated")

    # Calculate basic total from order
    total = float(order.total_amount)

    tax = total * 0.05  # 5% tax
    discount = 0.0
    final_total = total + tax - discount

    bill = Bill(
        order_id=order_id,
        bill_number=f"BILL-{order_id}-{int(datetime.utcnow().timestamp())}",
        subtotal=total,
        tax_amount=tax,
        discount_amount=discount,
        total_amount=final_total,
        payment_status="Pending",
        is_paid=False
    )

    db.add(bill)
    db.commit()
    db.refresh(bill)

    return bill


# -------------------------
# GET ALL BILLS
# -------------------------
@router.get("/")
def get_all_bills(db: Session = Depends(get_db)):
    return db.query(Bill).all()


# -------------------------
# GET BILL BY ID
# -------------------------
@router.get("/{bill_id}")
def get_bill(bill_id: int, db: Session = Depends(get_db)):

    bill = db.query(Bill).filter(Bill.id == bill_id).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    return bill


# -------------------------
# MAKE PAYMENT
# -------------------------
@router.post("/pay/{bill_id}")
def pay_bill(bill_id: int, data: dict, db: Session = Depends(get_db)):

    bill = db.query(Bill).filter(Bill.id == bill_id).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    if bill.is_paid:
        raise HTTPException(status_code=400, detail="Bill already paid")

    payment = Payment(
        bill_id=bill_id,
        payment_method=data.get("payment_method"),
        amount_paid=bill.total_amount,
        transaction_id=data.get("transaction_id"),
        payment_status="Success"
    )

    bill.is_paid = True
    bill.payment_status = "Paid"

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "message": "Payment successful",
        "bill_id": bill.id,
        "amount_paid": bill.total_amount
    }


# -------------------------
# GET PAYMENT HISTORY
# -------------------------
@router.get("/payments/all")
def get_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()