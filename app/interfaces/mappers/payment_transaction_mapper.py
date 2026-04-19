from app.core.entities.payment_transaction import PaymentTransaction
from app.infrastructure.models import PaymentTransactionModel


class PaymentTransactionMapper:

    @staticmethod
    def model_to_entity(model: PaymentTransactionModel):
        if not model:
            return None

        return PaymentTransaction(
            id=model.id,
            order_id=model.order_id,
            type=model.type,
            provider=model.provider,
            transaction_code=model.transaction_code,
            provider_transaction_id=model.provider_transaction_id,
            request_id=model.request_id,
            amount=float(model.amount) if model.amount is not None else None,
            status=model.status,
            parent_transaction_id=model.parent_transaction_id,
            raw_response=model.raw_response,
            logs=model.logs,
            paid_at=model.paid_at,
            created_at=model.created_at
        )

    @staticmethod
    def entity_to_model(entity: PaymentTransaction):
        if not entity:
            return None

        return PaymentTransactionModel(
            id=entity.id,
            order_id=entity.order_id,
            type=entity.type,
            provider=entity.provider,
            transaction_code=entity.transaction_code,
            provider_transaction_id=entity.provider_transaction_id,
            request_id=entity.request_id,
            amount=entity.amount,
            status=entity.status,
            parent_transaction_id=entity.parent_transaction_id,
            raw_response=entity.raw_response,
            logs= entity.logs,
            paid_at=entity.paid_at,
            created_at=entity.created_at
        )