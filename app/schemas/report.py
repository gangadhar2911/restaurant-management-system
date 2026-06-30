from datetime import date
from typing import List

from pydantic import BaseModel


# -------------------------
# DAILY SALES REPORT
# -------------------------
class DailySalesReport(BaseModel):
    report_date: date
    total_sales: float


# -------------------------
# REVENUE REPORT
# -------------------------
class RevenueReport(BaseModel):
    total_revenue: float


# -------------------------
# TOP SELLING ITEMS
# -------------------------
class TopItem(BaseModel):
    menu_item_id: int
    name: str
    total_sold: int


class TopItemsReport(BaseModel):
    items: List[TopItem]


# -------------------------
# ORDER STATS
# -------------------------
class OrderStatsReport(BaseModel):
    total_orders: int
    pending_orders: int
    completed_orders: int
    cancelled_orders: int


# -------------------------
# DASHBOARD REPORT
# -------------------------
class DashboardReport(BaseModel):
    daily_sales: DailySalesReport
    revenue: RevenueReport
    top_items: List[TopItem]
    order_stats: OrderStatsReport


# -------------------------
# REPORT RESPONSE
# -------------------------
class ReportResponse(BaseModel):
    daily_sales: DailySalesReport
    revenue: RevenueReport
    top_items: List[TopItem]
    order_stats: OrderStatsReport