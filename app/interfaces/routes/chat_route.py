from flask import Blueprint

from app.dependencies import get_chat_command_service, get_chat_query_service
from app.interfaces.controllers.chat_controller import (
    ChatController
)

chat_bp = Blueprint("chat", __name__)

controller = ChatController(
    chat_command_service=get_chat_command_service(),
    chat_query_service=get_chat_query_service()
)

chat_bp.route("/ai/chat", methods=["POST"])(controller.send_message)

chat_bp.route("/ai/chat/history/<session_id>", methods=["GET"])(controller.get_history)

chat_bp.route("/ai/chat/sessions/<patient_id>", methods=["GET"])(controller.get_sessions)
