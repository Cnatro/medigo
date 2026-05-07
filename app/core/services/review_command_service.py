from sqlalchemy.sql.functions import localtime

from app.infrastructure.repositories.review_repository_impl import ReviewRepositoryImpl
from app.shared.utils.message_code import MessageCode

from app.core.entities.review import Review  # thêm import


class ReviewCommandService:
    def __init__(self, review_repo: ReviewRepositoryImpl):
        self.review_repo = review_repo

    def review_doctor(self, data: dict, user_id: int):
        # Validate cơ bản
        required = ['appointment_id', 'doctor_id', 'rating']
        for field in required:
            if field not in data:
                return f"Missing {field}", MessageCode.FAIL

        rating = data.get('rating')
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return "Rating must be 1-5", MessageCode.FAIL

        # Tạo entity Review (id, patient_id, created_at để None)
        review_entity = Review(
            id=None,
            appointment_id=data['appointment_id'],
            patient_id=None,
            doctor_id=data['doctor_id'],
            rating=rating,
            comment=data.get('comment', ''),
            created_at=None
        )

        review_doc = self.review_repo.review_doctor(review_entity, user_id)
        if not review_doc:
            return "Review failed", MessageCode.FAIL

        return review_doc, MessageCode.SUCCESS


