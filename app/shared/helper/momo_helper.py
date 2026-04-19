from app.shared.utils.momo_result_code import RESULT_CODE_META, MomoResultCode


def get_result_meta(code: int):
    try:
        enum_code = MomoResultCode(code)
        return RESULT_CODE_META.get(enum_code, {
            "message": "Unknown",
            "final_status": True,
            "type": "UNKNOWN"
        })
    except ValueError:
        return {
            "message": "Invalid code",
            "final_status": True,
            "type": "UNKNOWN"
        }