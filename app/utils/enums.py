class OrderStatus:
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PREPARING = "Preparing"
    READY = "Ready"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class TableStatus:
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    OCCUPIED = "Occupied"


class PaymentStatus:
    PENDING = "Pending"
    PAID = "Paid"
    FAILED = "Failed"
    REFUNDED = "Refunded"


class RoleName:
    ADMIN = "Admin"
    MANAGER = "Manager"
    WAITER = "Waiter"
    CHEF = "Chef"
    CUSTOMER = "Customer"


class NotificationType:
    ORDER_CONFIRMATION = "ORDER_CONFIRMATION"
    ORDER_READY = "ORDER_READY"
    RESERVATION_CONFIRMATION = "RESERVATION_CONFIRMATION"
    SYSTEM = "SYSTEM"