from abc import abstractmethod

from app.core.entities.payment_transaction import PaymentTransaction
from app.shared.utils.payment_enum import PaymentStatus


class PaymentHistoryRepository:
    @abstractmethod
    def save(self, payment : PaymentTransaction): pass

    @abstractmethod
    def update_status_transaction(self, id, status : PaymentStatus): pass

    @abstractmethod
    def find_by_transaction_code(self, transaction_code ): pass

    @abstractmethod
    def update(self, payment: PaymentTransaction): pass

    @abstractmethod
    def find_refund_by_parent(self, parent_transaction_id): pass