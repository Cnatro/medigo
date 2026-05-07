from abc import ABC, abstractmethod

from app.core.entities.review import Review


class ReviewRepository(ABC):
    @abstractmethod
    def review_doctor(self, review: Review, user_id): pass

    @abstractmethod
    def get_reviews_by_doctor(self, doctor_id: str, page: int, per_page: int):
        pass

    @abstractmethod
    def get_doctor_rating_stats(self, doctor_id: str):
        pass