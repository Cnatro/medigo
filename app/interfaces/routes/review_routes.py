from flask import Blueprint
from flask_jwt_extended import verify_jwt_in_request

from app.dependencies import get_review_command_service, get_review_query_service
from app.interfaces.controllers.review_controller import ReviewController

review_bp = Blueprint("reviews", __name__)

@review_bp.before_request
def authenticated():
    verify_jwt_in_request()

controller = ReviewController(
    review_command_service= get_review_command_service(),
    review_query_service=get_review_query_service()
)


review_bp.route("",methods=["POST"])(controller.review_doctor)
review_bp.route("/doctors/<doctor_id>/reviews", methods=["GET"])(controller.get_doctor_reviews)
review_bp.route("/doctors/<doctor_id>/rating", methods=["GET"])(controller.get_doctor_rating)