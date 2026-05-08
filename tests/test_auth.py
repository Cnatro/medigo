import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.app import create_app


def test_login_invalid_account():
    app = create_app()
    client = app.test_client()

    response = client.post(
        '/api/auth/login',
        json={
            "email": "abc@gmail.com",
            "password": "123456"
        }
    )

    assert response.status_code in [400, 401]

def test_login_success():
    app = create_app()
    client = app.test_client()

    response = client.post(
        '/api/auth/login',
        json={
            "email": "patient1@gmail.com",
            "password": "123"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data is not None

def test_get_doctors_with_token():
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

    # LẤY TOKEN ĐÚNG FORMAT
    token = login_data["data"]["access_token"]

    assert token is not None

    # GỌI API CẦN LOGIN
    response = client.get(
        '/api/doctors',
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200