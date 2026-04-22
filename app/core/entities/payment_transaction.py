from app.core.entities.base_entity import BaseEntity


class PaymentTransaction(BaseEntity):

    def __init__(self, id, order_id, type, provider,
                 transaction_code, provider_transaction_id,
                 request_id, amount, status,
                 parent_transaction_id=None,
                 raw_response=None,
                 logs=None,
                 paid_at=None,
                 created_at=None):
        super().__init__(id)
        self.order_id = order_id
        self.type = type
        self.provider = provider
        self.transaction_code = transaction_code
        self.provider_transaction_id = provider_transaction_id
        self.request_id = request_id
        self.amount = amount
        self.status = status
        self.parent_transaction_id = parent_transaction_id
        self.raw_response = raw_response
        self.logs = logs
        self.paid_at = paid_at
        self.created_at = created_at