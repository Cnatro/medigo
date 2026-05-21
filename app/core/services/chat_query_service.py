from app.infrastructure.repositories.chat_repository_impl import ChatRepositoryImpl


class ChatQueryService:
    def __init__(self, chat_repo: ChatRepositoryImpl):
        self.chat_repo = chat_repo

    def get_chat_history(self, session_id):
        messages = self.chat_repo.get_messages(
            session_id
        )

        return [
            {
                "id": m.id,
                "sender": m.sender,
                "message": m.message,
                "created_at": m.created_at.isoformat()
            }
            for m in messages
        ]

    def get_sessions(self, patient_id):
        sessions = self.chat_repo.get_sessions(
            patient_id
        )

        return [
            {
                "id": s.id,
                "created_at": s.created_at.isoformat()
            }
            for s in sessions
        ]
