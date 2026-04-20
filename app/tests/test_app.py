
from app.app import app


def test_home_returns_200():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200


def test_home_contains_title():
    client = app.test_client()
    response = client.get('/')
    assert b'DO IT' in response.data or b'Task Manager' in response.data
