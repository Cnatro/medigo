from flask import jsonify

from app.shared.utils.message_code import MessageCode, STATUS_MAP


class ApiResponse:

    @staticmethod
    def success(messageCode, data=None, subData=None):
        return jsonify({
            "status": "success",
            "messageCode": str(messageCode.name),
            "data": _safe_json(data),
            **(subData or {})
        }), STATUS_MAP.get(messageCode, 200)

    @staticmethod
    def created(messageCode, data=None):
        return jsonify({
            "status": "success",
            "messageCode": str(messageCode.name),
            "data": _safe_json(data)
        }), STATUS_MAP.get(messageCode, 201)

    @staticmethod
    def error(messageCode, data=None):

        return jsonify({
            "status": "error",
            "messageCode": str(messageCode.name),
            "data": _safe_json(data)
        }), STATUS_MAP.get(messageCode, 400)

    @staticmethod
    def not_found(messageCode, data=None):
        return jsonify({
            "status": "error",
            "messageCode": str(messageCode.name),
            "data": _safe_json(data)
        }), STATUS_MAP.get(messageCode, 404)


def _safe_json(obj):
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, dict):
        return {k: _safe_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_safe_json(i) for i in obj]
    return str(obj)
