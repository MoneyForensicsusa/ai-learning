import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def test_student():
    data = {'name': 'Test student', 'city': 'Austin', 'score': 85}
    response = client.get('/students', json=data)
    created = response.json()

    yield created

    client.delete(f'/students/{created['id']}')