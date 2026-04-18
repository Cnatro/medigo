import uuid
import requests

from app.config import Config
from app.core.entities.order import Order
from app.shared.utils.momo_utils import sign_momo


class MomoService:

    def created_payment(self, order: Order):
        request_id = str(uuid.uuid4())
        amount = int(order.total_amount)
        order_id = order.id
        order_info = "Thanh toán đặt lịch"

        raw_data = (
            f"accessKey={Config.MOMO_ACCESS_KEY}"
            f"&amount={amount}"
            f"&extraData="
            f"&ipnUrl={Config.MOMO_NOTIFY_URL}"
            f"&orderId={order_id}"
            f"&orderInfo={order_info}"
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
            "orderId": order_id,
            "orderInfo": order_info,
            "redirectUrl": Config.MOMO_RETURN_URL,
            "ipnUrl": Config.MOMO_NOTIFY_URL,
            "requestType": "captureWallet",
            "extraData": "",
            "signature": signature
        }

        res = requests.post(Config.MOMO_ENDPOINT, json=payload)
        return res.json()

    def handle_momo_callback(self): pass
