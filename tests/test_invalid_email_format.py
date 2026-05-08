import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.app import create_app


def test_login_invalid_email_format():
    app = create_app()
    client = app.test_client()

    response = client.post(
        '/api/auth/login',
        json={
            "email": "abc",
            "password": "123"
        }
    )

    assert response.status_code in [400, 401, 422]