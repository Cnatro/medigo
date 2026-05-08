import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.app import create_app


def test_get_doctors_without_login():
    app = create_app()
    client = app.test_client()

    response = client.get('/api/doctors')

    assert response.status_code == 401