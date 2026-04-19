from typing import override

from sqlalchemy.exc import SQLAlchemyError

from app.core.entities.payment_transaction import PaymentTransaction
from app.core.repositories.payment_history_repository import PaymentHistoryRepository
from app.infrastructure.db import db
from app.infrastructure.models import PaymentTransactionModel
from app.interfaces.mappers.payment_transaction_mapper import PaymentTransactionMapper
from app.shared.utils.payment_enum import PaymentStatus, PaymentType


class PaymentHistoryRepositoryImpl(PaymentHistoryRepository):

    @override
    def save(self, payment : PaymentTransaction):
        model = PaymentTransactionMapper.entity_to_model(payment)

        db.session.add(model)
        db.session.commit()
        db.session.refresh(model)

        return PaymentTransactionMapper.model_to_entity(model)

    @override
    def update_status_transaction(self, id, status : PaymentStatus):
        model = PaymentTransactionModel.query.filter_by(id=id).first()

        if not model :
            raise ValueError("Not found payment history")

        if model.status == status.name :
            return PaymentTransactionMapper.model_to_entity(model)

        try :
            model.status = status.name
            db.session.commit()

            return PaymentTransactionMapper.model_to_entity(model)
        except SQLAlchemyError :
            db.session.rollback()


    @override
    def find_by_transaction_code(self, transaction_code ):
        model = PaymentTransactionModel.query.filter_by(transaction_code=transaction_code).first()

        if not model :
            return None

        return PaymentTransactionMapper.model_to_entity(model)

    @override
    def update(self, payment: PaymentTransaction):
        model = PaymentTransactionModel.query.filter_by(id=payment.id).first()

        if not model:
            raise ValueError("Payment not found")

        try:
            model.order_id = payment.order_id
            model.type = payment.type
            model.provider = payment.provider
            model.transaction_code = payment.transaction_code
            model.provider_transaction_id = payment.provider_transaction_id
            model.request_id = payment.request_id
            model.amount = payment.amount
            model.status = payment.status
            model.parent_transaction_id = payment.parent_transaction_id
            model.raw_response = payment.raw_response
            model.paid_at = payment.paid_at
            model.logs = payment.logs

            db.session.commit()
            db.session.refresh(model)

            return PaymentTransactionMapper.model_to_entity(model)

        except SQLAlchemyError:
            db.session.rollback()
            raise

    @override
    def find_refund_by_parent(self, parent_transaction_id):
        model = (
            PaymentTransactionModel.query
            .filter(
                PaymentTransactionModel.parent_transaction_id == parent_transaction_id,
                PaymentTransactionModel.type == PaymentType.REFUND.name
            )
            .order_by(PaymentTransactionModel.created_at.desc())
            .first()
        )

        if not model:
            return None

        return PaymentTransactionMapper.model_to_entity(model)