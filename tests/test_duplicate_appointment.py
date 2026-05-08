import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.app import create_app


def test_duplicate_appointment():
    app = create_app()
    client = app.test_client()

    # LOGIN
    login_response = client.post(
        '/api/auth/login',
        json={
            "email": "patient2@gmail.com",
            "password": "123"
        }
    )

    assert login_response.status_code == 200

    login_data = login_response.get_json()

    token = login_data["data"]["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    appointment_data = {
        "time_slot_id": 1
    }

    # TẠO LẦN 1
    first_response = client.post(
        '/api/appointments',
        json=appointment_data,
        headers=headers
    )

    # TẠO LẦN 2
    second_response = client.post(
        '/api/appointments',
        json=appointment_data,
        headers=headers
    )

    assert second_response.status_code in [400, 409]