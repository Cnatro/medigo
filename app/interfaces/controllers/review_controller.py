from flask import request
from flask_jwt_extended import get_jwt_identity

from app.core.services.review_command_service import ReviewCommandService
from app.core.services.review_query_service import ReviewQueryService
from app.shared.utils.api_response import ApiResponse
from app.shared.utils.message_code import MessageCode


class ReviewController:

    def __init__(self, review_command_service: ReviewCommandService, review_query_service: ReviewQueryService):
        self.review_command_service = review_command_service
        self.review_query_service = review_query_service

    def review_doctor(self):
        data = request.json

        user_id = get_jwt_identity()

        result, code = self.review_command_service.review_doctor(data, user_id)

        return ApiResponse.success(code, result)

    def get_doctor_reviews(self, doctor_id):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        reviews, total = self.review_query_service.get_reviews_by_doctor(doctor_id, page, per_page)
        return ApiResponse.success(MessageCode.SUCCESS, {
            'reviews': reviews,
            'total': total,
            'page': page,
            'per_page': per_page
        })

    def get_doctor_rating(self, doctor_id):
        avg, total = self.review_query_service.get_doctor_rating_stats(doctor_id)
        if avg is None:
            return ApiResponse.error(MessageCode.FAIL, "Doctor not found")
        return ApiResponse.success(MessageCode.SUCCESS, {
            'rating_avg': avg,
            'total_reviews': total
        })