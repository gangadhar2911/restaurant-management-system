from sqlalchemy.orm import Session
from app.models.bill import Bill
from app.models.payment import Payment


class BillingRepository:
    def create_bill(self, db: Session, data: dict) -> Bill:
        obj = Bill(**data)
        db.add(obj); db.commit(); db.refresh(obj)
        return obj

    def get_bill_by_order(self, db: Session, order_id: int):
        return db.query(Bill).filter(Bill.order_id == order_id).first()

    def get_all_bills(self, db: Session):
        return db.query(Bill).all()

    def get_bill_by_id(self, db: Session, bill_id: int):
        return db.query(Bill).filter(Bill.id == bill_id).first()

    def update_bill(self, db: Session, obj: Bill, data: dict) -> Bill:
        for k, v in data.items():
            setattr(obj, k, v)
        db.commit(); db.refresh(obj)
        return obj

    def create_payment(self, db: Session, data: dict) -> Payment:
        payment = Payment(**data)
        db.add(payment); db.commit(); db.refresh(payment)
        return payment

    def get_all_payments(self, db: Session):
        return db.query(Payment).all()