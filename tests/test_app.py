import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_register(client):
    response = client.post('/register', json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 201

def test_login(client):
    response = client.post('/login', json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200