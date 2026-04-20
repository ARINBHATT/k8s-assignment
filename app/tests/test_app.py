from app import app
import sys
sys.path.insert(0, '/app')


def test_home_returns_200():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200


def test_home_contains_kubernetes():
    client = app.test_client()
    response = client.get('/')
    assert b'Kubernetes' in response.data
