from flask import request

from app.core.services.chat_command_service import ChatCommandService
from app.core.services.chat_query_service import ChatQueryService
from app.shared.utils.api_response import ApiResponse
from app.shared.utils.message_code import MessageCode


class ChatController:

    def __init__(   self, chat_command_service : ChatCommandService,  chat_query_service : ChatQueryService):
        self.chat_command_service = chat_command_service
        self.chat_query_service = chat_query_service

    def send_message(self):

        data = request.json

        patient_id = data.get("patient_id")
        message = data.get("message")
        session_id = data.get("session_id")

        if not patient_id or not message:
            return {
                "error": "patient_id and message are required"
            }, 400

        result = self.chat_command_service.send_message(
            patient_id=patient_id,
            message=message,
            session_id=session_id
        )

        return ApiResponse.success(
            MessageCode.SUCCESS,
            result
        )

    def get_history(self, session_id):

        result = self.chat_query_service.get_chat_history(
            session_id
        )

        return ApiResponse.success(
            MessageCode.SUCCESS,
            result
        )

    def get_sessions(self, patient_id):

        result = self.chat_query_service.get_sessions(
            patient_id
        )

        return ApiResponse.success(
            MessageCode.SUCCESS,
            result
        )