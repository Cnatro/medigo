from typing_extensions import override

from app.core.repositories.chat_repository import ChatRepository
from app.infrastructure.db import db
from app.infrastructure.models import ChatSessionModel, ChatMessageModel


class ChatRepositoryImpl(ChatRepository):

    @override
    def create_session(self, patient_id):
        session = ChatSessionModel(
            patient_id=patient_id
        )

        db.session.add(session)
        db.session.commit()

        return session

    @override
    def find_session_by_id(self, session_id):
        model = ChatSessionModel.query.get(session_id)

        return model

    @override
    def save_message(self, session_id, sender, message):
        chat_message = ChatMessageModel(
            session_id=session_id,
            sender=sender,
            message=message
        )

        db.session.add(chat_message)
        db.session.commit()

        return chat_message

    @override
    def get_messages(self, session_id):
        models = ChatMessageModel.query.filter_by(
            session_id=session_id
        ).order_by(
            ChatMessageModel.created_at.asc()
        ).all()

        return models

    @override
    def get_sessions(self, patient_id):
        models = ChatSessionModel.query.filter_by(
            patient_id=patient_id
        ).order_by(
            ChatSessionModel.created_at.desc()
        ).all()

        return models
