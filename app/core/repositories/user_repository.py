from abc import ABC, abstractmethod

from app.core.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email): pass

    @abstractmethod
    def save(self,user : User): pass

    @abstractmethod
    def find_by_id(self, id): pass

    @abstractmethod
    def update_current_user(self,  user_id, data): pass