from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#Test the health check route
def test_health_check():
    response = client.get('/health')
    assert response.json() == {'status': 'ok'}

#Test creating a student
def test_create_student():
    student_data = {'name': 'Test student', 'city': 'Austin', 'score': 85}
    response = client.post('/students', json=student_data)
    assert response.status_code == 201
    data = response.json()
    assert data['score'] == 85
    assert data['name'] == 'Test student'
    assert 'id' in data

# Test validation - bad data should be rejected
def test_create_student_invalid_score():
    bad_data = {'name': 'Bad student', 'city': 'Austin', 'score': 150}
    response = client.post('/students', json=bad_data)
    assert response.status_code == 422

#Test getting a student that does not exist
def test_get_nonexistent_student():
    response = client.get('/students/99999')
    assert response.status_code == 404

#Test the full create_then_retreive cycle
def test_create_and_retreive():
    data = {'name': 'Alice', 'city': 'NY', 'score': 20}
    first_response = client.post('/students', json=data)
    created = first_response.json()
    student_id = created['id']
    second_response = client.get(f'/students/{student_id}')
    assert second_response.status_code == 200
    assert second_response.json()['name'] == 'Alice'
    



