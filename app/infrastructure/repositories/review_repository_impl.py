from sqlalchemy import func

from app.core.entities.review import Review
from app.core.repositories.review_repository import ReviewRepository
from app.infrastructure.db import db
from app.infrastructure.models import ReviewModel, PatientModel, AppointmentModel, DoctorModel
from app.interfaces.mappers.review_mapper import ReviewMapper

from sqlalchemy.exc import IntegrityError


class ReviewRepositoryImpl(ReviewRepository):
    def review_doctor(self, review: Review, user_id):
        patient = PatientModel.query.filter_by(user_id=user_id).first()
        if not patient:
            return None

        appointment = AppointmentModel.query.filter_by(
            id=review.appointment_id,
            patient_id=patient.id
        ).first()
        if not appointment:
            return None

        review.patient_id = patient.id
        model = ReviewMapper.entity_to_model(review)

        try:
            db.session.add(model)
            db.session.commit()
            return ReviewMapper.model_to_entity(model)
        except IntegrityError:
            db.session.rollback()
            return None

    def get_reviews_by_doctor(self, doctor_id: str, page: int, per_page: int):
        query = ReviewModel.query.filter_by(doctor_id=doctor_id).order_by(ReviewModel.created_at.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        reviews = [ReviewMapper.model_to_entity(m) for m in paginated.items]
        return reviews, paginated.total

    def get_doctor_rating_stats(self, doctor_id: str):

        avg, total = db.session.query(
            func.avg(ReviewModel.rating),
            func.count(ReviewModel.id)
        ).filter(
            ReviewModel.doctor_id == doctor_id
        ).first()

        return round(float(avg), 1) if avg else 0, total
