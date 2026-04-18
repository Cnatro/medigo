import hashlib
import hmac


def sign_momo(data : str, secret_key : str):
    return hmac.new(
        secret_key.encode("utf-8"),
        data.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def verify_momo_signature(raw_data:str, signature:str, secret_key : str):
    expect = sign_momo(raw_data,secret_key)

    return expect == signature