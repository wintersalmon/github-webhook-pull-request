import pytest
from src.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_healthz(client):
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_ready(client):
    response = client.get('/ready')
    assert response.status_code == 200
    assert response.json['status'] == 'ready'

def test_handle_pull_request(client):
    payload = {
        "action": "opened",
        "number": 1,
        "pull_request": {
            "title": "Test PR"
        }
    }
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "pull_request",
        "X-Hub-Signature-256": "sha256=invalidsignature"  # Replace with a valid signature or mock the verification
    }
    response = client.post('/hooks/github/pull-request', json=payload, headers=headers)
    assert response.status_code == 403  # Since the signature is invalid