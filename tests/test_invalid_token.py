import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.app import create_app


def test_invalid_jwt_token():
    app = create_app()
    client = app.test_client()

    response = client.get(
        '/api/doctors',
        headers={
            "Authorization": "Bearer fake_token_123"
        }
    )

    assert response.status_code in [401, 422]