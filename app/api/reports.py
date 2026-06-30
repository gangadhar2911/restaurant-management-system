from datetime import datetime, date

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.menu_item import MenuItem
from app.models.bill import Bill

router = APIRouter(prefix="/reports", tags=["Reports"])


# -------------------------
# DAILY SALES REPORT
# -------------------------
@router.get("/daily-sales")
def daily_sales(report_date: date = date.today(), db: Session = Depends(get_db)):

    total_sales = db.query(
        func.sum(Bill.total_amount)
    ).filter(
        func.date(Bill.created_at) == report_date,
        Bill.is_paid == True
    ).scalar()

    return {
        "date": str(report_date),
        "total_sales": float(total_sales or 0)
    }


# -------------------------
# TOTAL REVENUE REPORT
# -------------------------
@router.get("/revenue")
def total_revenue(db: Session = Depends(get_db)):

    revenue = db.query(
        func.sum(Bill.total_amount)
    ).filter(
        Bill.is_paid == True
    ).scalar()

    return {
        "total_revenue": float(revenue or 0)
    }


# -------------------------
# TOP SELLING ITEMS
# -------------------------
@router.get("/top-items")
def top_selling_items(db: Session = Depends(get_db)):

    results = db.query(
        MenuItem.id,
        MenuItem.name,
        func.sum(OrderItem.quantity).label("total_sold")
    ).join(OrderItem, OrderItem.menu_item_id == MenuItem.id) \
     .group_by(MenuItem.id) \
     .order_by(func.sum(OrderItem.quantity).desc()) \
     .limit(10) \
     .all()

    return [
        {
            "menu_item_id": r.id,
            "name": r.name,
            "total_sold": int(r.total_sold)
        }
        for r in results
    ]


# -------------------------
# ORDER STATISTICS
# -------------------------
@router.get("/order-stats")
def order_statistics(db: Session = Depends(get_db)):

    total_orders = db.query(func.count(Order.id)).scalar()

    pending_orders = db.query(func.count(Order.id)).filter(
        Order.order_status == "Pending"
    ).scalar()

    completed_orders = db.query(func.count(Order.id)).filter(
        Order.order_status == "Completed"
    ).scalar()

    cancelled_orders = db.query(func.count(Order.id)).filter(
        Order.order_status == "Cancelled"
    ).scalar()

    return {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders
    }