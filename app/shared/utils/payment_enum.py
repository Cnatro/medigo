from enum import Enum


class PaymentType(Enum):
    PAYMENT = "PAYMENT"
    REFUND = "REFUND"


class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUND_FAILED = "REFUND_FAILED"
    REFUND_SUCCESS = "REFUND_SUCCESS"

class OrderStatus(Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    REFUND_SUCCESS = "REFUND_SUCCESS"

class PaymentProvider(Enum):
    MOMO = "MOMO"