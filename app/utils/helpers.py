import random
import string
from datetime import datetime


def generate_code(prefix: str = "", length: int = 6) -> str:
    """Generate a short unique-ish code, e.g. for bill numbers, order codes."""
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
    timestamp = int(datetime.utcnow().timestamp())
    return f"{prefix}-{timestamp}-{suffix}" if prefix else f"{timestamp}-{suffix}"


def to_dict(model_instance) -> dict:
    """Convert a SQLAlchemy model instance into a plain dict."""
    return {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}


def calculate_tax(amount: float, rate: float = 0.05) -> float:
    return round(amount * rate, 2)


def calculate_discount(amount: float, percent: float = 0.0) -> float:
    return round(amount * (percent / 100), 2)