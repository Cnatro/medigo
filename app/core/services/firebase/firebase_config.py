import os
import json
import base64

import firebase_admin
from firebase_admin import credentials

from app.config import Config


class FirebaseAdmin:

    _initialized = False

    @classmethod
    def initialize(cls):

        if cls._initialized:
            return

        firebase_base64 = Config.FIRE_BASE_SDK

        if not firebase_base64:
            raise Exception("FIREBASE_CREDENTIAL_BASE64 not found")

        try:
            firebase_json = base64.b64decode(
                firebase_base64
            ).decode("utf-8")

            firebase_dict = json.loads(firebase_json)

            cred = credentials.Certificate(firebase_dict)

            firebase_admin.initialize_app(cred)

            cls._initialized = True

            print(" Firebase initialized")

        except Exception as e:
            raise Exception(f"Firebase init failed: {str(e)}")