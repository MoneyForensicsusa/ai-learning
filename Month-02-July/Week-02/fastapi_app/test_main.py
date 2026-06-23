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
    
# Test for deleting a student
def test_delete_student():
    data = {'name': 'Anny', 'city': 'Dallas', 'score': 97}
    first_response = client.post('/students', json=data)
    created = first_response.json()
    student_id = created['id']
    delete_response = client.delete(f'/students/{student_id}')
    assert delete_response.status_code == 200
    get_response = client.get(f'/students/{student_id}')
    assert get_response.status_code == 404

#Test for sending missing data
def test_sending_missing_data():
    data = {}
    response = client.post('/students', json=data)
    assert response.status_code == 422

# Test that verifies the stats endpoint returns correct values
def test_stats_verification():
    students = [
        {'name': 'jose', 'city': 'NY', 'score': 20},
        {'name': 'Aba', 'city': 'CA', 'score': 50},
        {'name': 'Uche', 'city': 'ATL', 'score': 20}
    ]
    created_ids = []
    for student in students:
        response = client.post('/students', json=student)
        created_ids.append(response.json()['id'])
    
    stats_response = client.get('/students/stats')
    assert stats_response.status_code == 200
    data = stats_response.json()
    assert data['count'] >= 3
    assert data['average'] >= 30.0
    assert data['maximum'] >=  50
    assert data['minimum'] <= 20

    for student_id in created_ids:
        client.delete(f'/students/{student_id}')

    
    
