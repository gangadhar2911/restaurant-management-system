from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
import app.models  # noqa: F401  (registers all models before mappers configure)

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.roles import router as roles_router
from app.api.restaurants import router as restaurant_router
from app.api.tables import router as table_router
from app.api.categories import router as categories_router
from app.api.menu import router as menu_router
from app.api.orders import router as order_router
from app.api.billing import router as billing_router
from app.api.kitchen import router as kitchen_router
from app.api.notifications import router as notification_router
from app.api.inventory import router as inventory_router
from app.api.reports import router as reports_router
from app.api.reservations import router as reservations_router
from app.api.audit_logs import router as audit_logs_router
from app.middleware.logging import LoggingMiddleware

app = FastAPI(title="Restaurant Management System")

# Create all tables on startup (use Alembic migrations for production)
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(restaurant_router)
app.include_router(table_router)
app.include_router(categories_router)
app.include_router(menu_router)
app.include_router(order_router)
app.include_router(billing_router)
app.include_router(kitchen_router)
app.include_router(notification_router)
app.include_router(inventory_router)
app.include_router(reports_router)
app.include_router(reservations_router)
app.include_router(audit_logs_router)


@app.get("/")
def root():
    return {"message": "Restaurant Management System is running"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
import app.models  # noqa: F401  (registers all models before mappers configure)

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.roles import router as roles_router
from app.api.restaurants import router as restaurant_router
from app.api.tables import router as table_router
from app.api.categories import router as categories_router
from app.api.menu import router as menu_router
from app.api.orders import router as order_router
from app.api.billing import router as billing_router
from app.api.kitchen import router as kitchen_router
from app.api.notifications import router as notification_router
from app.api.inventory import router as inventory_router
from app.api.reports import router as reports_router
from app.api.reservations import router as reservations_router
from app.api.audit_logs import router as audit_logs_router
from app.middleware.logging import LoggingMiddleware

app = FastAPI(title="Restaurant Management System")

# Create all tables on startup (use Alembic migrations for production)
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(restaurant_router)
app.include_router(table_router)
app.include_router(categories_router)
app.include_router(menu_router)
app.include_router(order_router)
app.include_router(billing_router)
app.include_router(kitchen_router)
app.include_router(notification_router)
app.include_router(inventory_router)
app.include_router(reports_router)
app.include_router(reservations_router)
app.include_router(audit_logs_router)


@app.get("/")
def root():
    return {"message": "Restaurant Management System is running"}