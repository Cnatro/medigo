from flask import Blueprint

from app.dependencies import get_rag_service
from app.interfaces.controllers.rag_controller import RagController

rag_bp = Blueprint("rag", __name__)

controller = RagController(
    rag_service= get_rag_service()
)


rag_bp.route("/ai/consult",methods=["POST"])(controller.consult)