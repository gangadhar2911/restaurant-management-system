from datetime import date

from sqlalchemy.orm import Session
from app.repositories.report_repository import ReportRepository

repo = ReportRepository()


class ReportService:
    @staticmethod
    def daily_sales(db: Session, report_date: date = None):
        report_date = report_date or date.today()
        total = repo.daily_sales(db, report_date)
        return {"date": str(report_date), "total_sales": float(total or 0)}

    @staticmethod
    def revenue(db: Session):
        total = repo.total_revenue(db)
        return {"total_revenue": float(total or 0)}

    @staticmethod
    def top_selling_items(db: Session, limit: int = 10):
        results = repo.top_selling_items(db, limit)
        return [
            {"menu_item_id": r.id, "name": r.item_name, "total_sold": int(r.total_sold)}
            for r in results
        ]

    @staticmethod
    def order_statistics(db: Session):
        return repo.order_stats(db)