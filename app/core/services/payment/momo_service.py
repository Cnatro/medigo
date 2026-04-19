import time
import uuid
import json
import base64
from datetime import datetime

import requests
import logging

from app.config import Config
from app.core.entities.order import Order
from app.core.entities.payment_transaction import PaymentTransaction
from app.infrastructure.repositories.order_repository_impl import OrderRepositoryImpl
from app.infrastructure.repositories.payment_history_repository_impl import PaymentHistoryRepositoryImpl
from app.shared.helper.momo_helper import get_result_meta
from app.shared.utils.message_code import MessageCode
from app.shared.utils.momo_utils import sign_momo, verify_momo_signature
from app.shared.utils.payment_enum import OrderStatus, PaymentType, PaymentProvider, PaymentStatus

log = logging.getLogger(__name__)


class MomoService:

    def __init__(self, payment_repo: PaymentHistoryRepositoryImpl):
        self.payment_repo = payment_repo

    def append_log(self, transaction, status, message, data):
        log_item = {
            "status": status,
            "message": message,
            "data": data,
            "created_at": datetime.utcnow().isoformat()
        }

        if not transaction.logs:
            transaction.logs = []

        transaction.logs.append(log_item)

    def created_payment(self, order: Order, payment_type: PaymentType):
        request_id = str(uuid.uuid4())
        amount = int(order.total_amount)
        transaction_code = f"PAY_{int(time.time())}_{uuid.uuid4()}"

        extra_data_dict = {
            "order_id": order.id
        }
        extra_data = base64.b64encode(json.dumps(extra_data_dict).encode()).decode()

        raw_data = (
            f"accessKey={Config.MOMO_ACCESS_KEY}"
            f"&amount={amount}"
            f"&extraData={extra_data}"
            f"&ipnUrl={Config.MOMO_NOTIFY_URL}"
            f"&orderId={transaction_code}"
            f"&orderInfo=Thanh toán đặt lịch"
            f"&partnerCode={Config.MOMO_PARTNER_CODE}"
            f"&redirectUrl={Config.MOMO_RETURN_URL}"
            f"&requestId={request_id}"
            f"&requestType=captureWallet"
        )

        signature = sign_momo(raw_data, Config.MOMO_SECRET_KEY)

        payload = {
            "partnerCode": Config.MOMO_PARTNER_CODE,
            "accessKey": Config.MOMO_ACCESS_KEY,
            "requestId": request_id,
            "amount": amount,
            "orderId": transaction_code,
            "orderInfo": "Thanh toán đặt lịch",
            "redirectUrl": Config.MOMO_RETURN_URL,
            "ipnUrl": Config.MOMO_NOTIFY_URL,
            "requestType": "captureWallet",
            "extraData": extra_data,
            "signature": signature
        }

        transaction = PaymentTransaction(
            id=None,
            order_id=str(order.id),
            type=payment_type.name,
            provider=PaymentProvider.MOMO.name,
            transaction_code=transaction_code,
            provider_transaction_id=None,
            request_id=request_id,
            amount=amount,
            status=PaymentStatus.PENDING.name,
            parent_transaction_id=None,
            raw_response=payload,
            paid_at=None,
            logs=[]
        )

        self.append_log(transaction, "PENDING", "Init payment", payload)

        self.payment_repo.save(transaction)

        res = requests.post(Config.MOMO_ENDPOINT, json=payload)

        log.info("[MOMO CREATE] orderId=%s and transaction_cde = %s", order.id , transaction_code)

        return res.json()



    def handle_momo_callback(self, order_repo: OrderRepositoryImpl, data):

        raw_data = (
            f"accessKey={Config.MOMO_ACCESS_KEY}"
            f"&amount={data['amount']}"
            f"&extraData={data['extraData']}"
            f"&message={data['message']}"
            f"&orderId={data['orderId']}"
            f"&orderInfo={data['orderInfo']}"
            f"&orderType={data['orderType']}"
            f"&partnerCode={data['partnerCode']}"
            f"&payType={data['payType']}"
            f"&requestId={data['requestId']}"
            f"&responseTime={data['responseTime']}"
            f"&resultCode={data['resultCode']}"
            f"&transId={data['transId']}"
        )

        is_verify = verify_momo_signature(
            raw_data=raw_data,
            signature=data["signature"],
            secret_key=Config.MOMO_SECRET_KEY
        )

        if not is_verify:
            log.warning("[MOMO] Invalid signature")
            return None, MessageCode.INVALID_SIGNATURE

        transaction = self.payment_repo.find_by_transaction_code(data["orderId"])

        if not transaction:
            log.error("[MOMO] Transaction not found: %s", data["orderId"])
            return None, MessageCode.TRANSACTION_NOT_FOUND


        if transaction.status == PaymentStatus.SUCCESS.name:
            log.info("[MOMO] Already processed")
            return None, MessageCode.ALREADY_PAID


        try:
            extra_data = json.loads(base64.b64decode(data["extraData"]))
        except Exception:
            extra_data = {}

        meta = get_result_meta(data["resultCode"])

        log.info(
            "[MOMO CALLBACK] orderId=%s | code=%s | msg=%s | type=%s",
            data["orderId"],
            data["resultCode"],
            meta["message"],
            meta["type"]
        )

        transaction.provider_transaction_id = str(data["transId"])
        transaction.request_id = str(data["requestId"])
        transaction.raw_response = data


        self.append_log(
            transaction,
            meta["type"],
            meta["message"],
            data
        )

        if meta["type"] == "SUCCESS":
            transaction.status = PaymentStatus.SUCCESS.name
            transaction.paid_at = datetime.fromtimestamp(data["responseTime"] / 1000)

            order = order_repo.update_order_status(
                order_id=extra_data.get("order_id"),
                status=OrderStatus.PAID
            )

            self.payment_repo.update(transaction)
            return order, MessageCode.PAYMENT_SUCCESS

        elif meta["type"] == "PENDING":
            transaction.status = PaymentStatus.PENDING.name
            transaction.paid_at = None

            self.payment_repo.update(transaction)
            return None, MessageCode.PAYMENT_PENDING

        else:
            transaction.status = PaymentStatus.FAILED.name
            transaction.paid_at = None

            self.payment_repo.update(transaction)
            return None, MessageCode.PAYMENT_FAILED