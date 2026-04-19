from abc import ABC, abstractmethod

from app.core.entities.order import Order


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order : Order): pass

    @abstractmethod
    def find_by_id(self, id ): pass

    @abstractmethod
    def update_order_status(self, order_id, status : str): pass