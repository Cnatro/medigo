from enum import Enum


class PaymentType(Enum):
    PAYMENT = "PAYMENT"
    REFUND = "REFUND"


class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class OrderStatus(Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

class PaymentProvider(Enum):
    MOMO = "MOMO"