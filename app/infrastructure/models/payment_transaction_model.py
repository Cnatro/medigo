import uuid
from datetime import datetime

from app.infrastructure.db import db


class PaymentTransactionModel(db.Model):
    __tablename__ = "payment_transactions"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String, db.ForeignKey("orders.id"), nullable=False)

    type = db.Column(db.String, nullable=False)  # PAYMENT | REFUND

    provider = db.Column(db.String)  # MOMO, PAYPAL...
    transaction_code = db.Column(db.String)
    provider_transaction_id = db.Column(db.String)
    request_id = db.Column(db.String)

    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String, nullable=False)  # PENDING, SUCCESS, FAILED

    parent_transaction_id = db.Column(
        db.String,
        db.ForeignKey("payment_transactions.id"),
        nullable=True
    )

    raw_response = db.Column(db.JSON)
    logs = db.Column(db.JSON, default=list) #fix tạm thêm logs -> thực tế nên tạo ra 1 bảng ghi log

    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)