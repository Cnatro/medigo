from app.core.services.ai.rag_service import RagService
from app.infrastructure.repositories.chat_repository_impl import ChatRepositoryImpl


class ChatCommandService:
    def __init__(self, chat_repo: ChatRepositoryImpl, rag_service: RagService):
        self.chat_repo = chat_repo
        self.rag_service = rag_service

    def send_message(self, patient_id, message, session_id):
        if session_id:

            session = self.chat_repo.find_session_by_id(
                session_id
            )

            if not session:
                return {
                    "error": "Session not found"
                }
        else:

            session = self.chat_repo.create_session(
                patient_id
            )

            # lưu user message
        self.chat_repo.save_message(
            session_id=session.id,
            sender="user",
            message=message
        )

        # AI xử lý
        ai_response = self.rag_service.handle_query(
            user_input=message
        )

        # lưu bot message
        self.chat_repo.save_message(
            session_id=session.id,
            sender="bot",
            message=ai_response
        )

        return {
            "session_id": session.id,
            "response": ai_response
        }
