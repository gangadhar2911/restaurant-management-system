from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.billing_repository import BillingRepository
from app.repositories.order_repository import OrderRepository
from app.utils.constants import DEFAULT_TAX_RATE

billing_repo = BillingRepository()
order_repo = OrderRepository()


class BillingService:
    @staticmethod
    def generate_bill(db: Session, order_id: int, tax_rate: float = DEFAULT_TAX_RATE, discount: float = 0.0):
        order = order_repo.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if billing_repo.get_bill_by_order(db, order_id):
            raise HTTPException(status_code=400, detail="Bill already generated")

        subtotal = float(order.total_amount)
        tax = round(subtotal * tax_rate, 2)
        total = subtotal + tax - discount

        return billing_repo.create_bill(db, {
            "order_id": order_id,
            "bill_number": f"BILL-{order_id}-{int(datetime.utcnow().timestamp())}",
            "subtotal": subtotal,
            "tax_amount": tax,
            "discount_amount": discount,
            "total_amount": total,
            "payment_status": "Pending",
            "is_paid": False,
        })

    @staticmethod
    def get_all(db: Session):
        return billing_repo.get_all_bills(db)

    @staticmethod
    def get_by_id(db: Session, bill_id: int):
        bill = billing_repo.get_bill_by_id(db, bill_id)
        if not bill:
            raise HTTPException(status_code=404, detail="Bill not found")
        return bill

    @staticmethod
    def apply_discount(db: Session, bill_id: int, discount_amount: float):
        bill = BillingService.get_by_id(db, bill_id)
        new_total = float(bill.subtotal) + float(bill.tax_amount) - discount_amount
        return billing_repo.update_bill(db, bill, {
            "discount_amount": discount_amount, "total_amount": new_total
        })

    @staticmethod
    def pay(db: Session, bill_id: int, payment_method: str, transaction_id: str = None):
        bill = BillingService.get_by_id(db, bill_id)
        if bill.is_paid:
            raise HTTPException(status_code=400, detail="Bill already paid")

        payment = billing_repo.create_payment(db, {
            "bill_id": bill_id,
            "payment_method": payment_method,
            "amount_paid": bill.total_amount,
            "transaction_id": transaction_id,
            "payment_status": "Success",
        })
        billing_repo.update_bill(db, bill, {"is_paid": True, "payment_status": "Paid"})
        return {"message": "Payment successful", "bill_id": bill.id, "payment_id": payment.id}

    @staticmethod
    def get_payments(db: Session):
        return billing_repo.get_all_payments(db)