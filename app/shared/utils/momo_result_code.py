from enum import Enum


class MomoResultCode(Enum):
    SUCCESS = 0
    MAINTENANCE = 10
    ACCESS_DENIED = 11
    UNSUPPORTED_API = 12
    AUTH_FAILED = 13

    INVALID_REQUEST_FORMAT = 20
    INVALID_AMOUNT_REQUEST = 21
    INVALID_AMOUNT = 22

    DUPLICATE_REQUEST_ID = 40
    DUPLICATE_ORDER_ID = 41
    ORDER_NOT_FOUND = 42
    CONFLICT_TRANSACTION = 43
    DUPLICATE_ITEM_ID = 45

    INVALID_DATA_LIST = 47

    QR_FAILED = 98
    UNKNOWN_ERROR = 99

    PENDING_USER_CONFIRM = 1000
    INSUFFICIENT_FUNDS = 1001
    PAYMENT_REJECTED = 1002
    TRANSACTION_CANCELLED = 1003
    LIMIT_EXCEEDED = 1004
    EXPIRED = 1005
    USER_REJECTED = 1006
    ACCOUNT_NOT_EXIST = 1007
    CANCELLED_BY_PARTNER = 1017
    PROMOTION_RESTRICTED = 1026

    REFUND_FAILED = 1080
    REFUND_REJECTED = 1081
    REFUND_NOT_SUPPORTED = 1088

    INVALID_ORDER_GROUP = 2019

    USER_RESTRICTED = 4001
    USER_NOT_VERIFIED = 4002
    LOGIN_FAILED = 4100

    PROCESSING = 7000
    PROCESSING_BY_PROVIDER = 7002

    CONFIRMED = 9000


RESULT_CODE_META = {
    MomoResultCode.SUCCESS: {
        "message": "Thành công",
        "final_status": True,
        "type": "SUCCESS"
    },
    MomoResultCode.MAINTENANCE: {
        "message": "Hệ thống đang bảo trì",
        "final_status": False,
        "type": "SYSTEM_ERROR"
    },
    MomoResultCode.ACCESS_DENIED: {
        "message": "Truy cập bị từ chối",
        "final_status": False,
        "type": "SYSTEM_ERROR"
    },
    MomoResultCode.AUTH_FAILED: {
        "message": "Xác thực thất bại",
        "final_status": False,
        "type": "MERCHANT_ERROR"
    },
    MomoResultCode.INSUFFICIENT_FUNDS: {
        "message": "Không đủ tiền",
        "final_status": True,
        "type": "MERCHANT_ERROR"
    },
    MomoResultCode.USER_REJECTED: {
        "message": "Người dùng từ chối thanh toán",
        "final_status": True,
        "type": "USER_ERROR"
    },
    MomoResultCode.PROCESSING: {
        "message": "Đang xử lý",
        "final_status": False,
        "type": "PENDING"
    },
    MomoResultCode.CONFIRMED: {
        "message": "Đã xác nhận",
        "final_status": False,
        "type": "PENDING"
    },
}