class PaymentType:
    PAYMENT = "PAYMENT"
    REFUND = "REFUND"


class PaymentStatus:
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class OrderStatus:
    PENDING = "PENDING"
    WAITING_PAYMENT = "WAITING_PAYMENT"
    PAID = "PAID"
    CANCELLED = "CANCELLED"