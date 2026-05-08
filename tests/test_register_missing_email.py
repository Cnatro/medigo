import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.app import create_app


def test_register_without_email():
    app = create_app()
    client = app.test_client()

    response = client.post(
        '/api/auth/register',
        json={
            "full_name": "Test User",
            "password": "123456",
            "phone": "0123456789"
        }
    )

    assert response.status_code in [400, 422]