# app/core/services/review_query_service.py
from app.infrastructure.repositories.review_repository_impl import ReviewRepositoryImpl

class ReviewQueryService:
    def __init__(self, review_repo: ReviewRepositoryImpl):
        self.review_repo = review_repo

    def get_reviews_by_doctor(self, doctor_id: str, page: int, per_page: int):
        reviews, total = self.review_repo.get_reviews_by_doctor(doctor_id, page, per_page)
        reviews_data = []
        for r in reviews:
            reviews_data.append({
                'id': r.id,
                'appointment_id': r.appointment_id,
                'patient_id': r.patient_id,
                'doctor_id': r.doctor_id,
                'rating': r.rating,
                'comment': r.comment,
                'created_at': r.created_at.isoformat() if r.created_at else None
            })
        return reviews_data, total

    def get_doctor_rating_stats(self, doctor_id: str):
        avg, total = self.review_repo.get_doctor_rating_stats(doctor_id)
        if avg is None:
            return None, None
        return avg, total