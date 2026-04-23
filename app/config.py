import os
from datetime import timedelta


class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_SSLMODE = os.getenv("DB_SSLMODE", "require")

    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    MOMO_PARTNER_CODE = os.getenv("MOMO_PARTNER_CODE")
    MOMO_ACCESS_KEY = os.getenv("MOMO_ACCESS_KEY")
    MOMO_SECRET_KEY = os.getenv("MOMO_SECRET_KEY")

    MOMO_ENDPOINT = os.getenv("MOMO_ENDPOINT")
    MOMO_REFUND_ENDPOINT = os.getenv("MOMO_REFUND_ENDPOINT")
    MOMO_QUERY_ENDPOINT=os.getenv("MOMO_QUERY_ENDPOINT")

    MOMO_RETURN_URL = os.getenv("MOMO_RETURN_URL")
    MOMO_NOTIFY_URL = os.getenv("MOMO_NOTIFY_URL")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        f"?sslmode={DB_SSLMODE}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")