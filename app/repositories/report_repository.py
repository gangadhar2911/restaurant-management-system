from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.bill import Bill
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.menu import MenuItem


class ReportRepository:
    def daily_sales(self, db: Session, report_date: date):
        return db.query(func.sum(Bill.total_amount)).filter(
            func.date(Bill.created_at) == report_date, Bill.is_paid == True  # noqa: E712
        ).scalar()

    def total_revenue(self, db: Session):
        return db.query(func.sum(Bill.total_amount)).filter(Bill.is_paid == True).scalar()  # noqa: E712

    def top_selling_items(self, db: Session, limit: int = 10):
        return db.query(
            MenuItem.id, MenuItem.item_name, func.sum(OrderItem.quantity).label("total_sold")
        ).join(OrderItem, OrderItem.menu_item_id == MenuItem.id) \
         .group_by(MenuItem.id).order_by(func.sum(OrderItem.quantity).desc()).limit(limit).all()

    def order_stats(self, db: Session):
        total = db.query(func.count(Order.id)).scalar()
        pending = db.query(func.count(Order.id)).filter(Order.order_status == "Pending").scalar()
        completed = db.query(func.count(Order.id)).filter(Order.order_status == "Completed").scalar()
        cancelled = db.query(func.count(Order.id)).filter(Order.order_status == "Cancelled").scalar()
        return {
            "total_orders": total, "pending_orders": pending,
            "completed_orders": completed, "cancelled_orders": cancelled,
        }