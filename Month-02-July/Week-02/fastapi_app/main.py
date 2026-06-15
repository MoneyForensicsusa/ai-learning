from fastapi import FastAPI 
from pydantic import BaseModel, Field

app = FastAPI()

students = []

class Student(BaseModel):
    name: str 
    city: str
    score: int = Field(ge=0, le=100)

@app.get('/students')
def get_students():
    return students

@app.get('/students/stats')
def stats():
    if len(students) == 0:
        return {'error': 'No students yet'}
    scores = []
    for student in students:
        scores.append(student['score'])
    return {
        'count': len(scores),
        'average': sum(scores) / len(scores),
        'highest': max(scores),
        'lowest': min(scores)
    }

@app.post('/students', status_code=201)
def create_student(student: Student):
    students.append(student.dict())
    return {'message': 'Student Created', 'student': student}

@app.get('/students/{student_id}')
def get_student(student_id: int):
    if student_id >= len(students):
        return {'error': 'Student not found'}
    return students[student_id]


@app.delete('/students/{student_id}')
def delete_student(student_id: int):
    if student_id >= len(students):
        return {'error': 'student not found'}
    removed = students.pop(student_id)
    return {'message': 'Student deleted', 'student': removed}


