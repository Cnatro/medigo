from flask import request

from app.shared.utils.api_response import ApiResponse
from app.shared.utils.message_code import MessageCode


class RagController:

    def __init__(self, rag_service):
        self.rag_service = rag_service

    def consult(self):
        data = request.json

        user_input = data.get("message")

        if not user_input:
            return {
                "error": "message is required"
            }, 400

        result = self.rag_service.handle_query(user_input)

        return ApiResponse.success(MessageCode.SUCCESS, result)