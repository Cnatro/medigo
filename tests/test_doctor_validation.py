import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.app import create_app


def test_get_doctor_not_found():
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

    # GỌI DOCTOR KHÔNG TỒN TẠI
    response = client.get(
        '/api/doctors/999999',
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in [400, 404]