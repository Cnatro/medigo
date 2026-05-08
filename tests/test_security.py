import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.app import create_app


def test_create_appointment_without_token():
    app = create_app()
    client = app.test_client()

    response = client.post(
        '/api/appointments',
        json={
            "time_slot_id": "123"
        }
    )

    assert response.status_code == 401