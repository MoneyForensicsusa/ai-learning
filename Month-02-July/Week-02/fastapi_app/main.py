from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
class Student(BaseModel):
    name: str
    city: str
    score: int = Field(ge=0, le=100)

class ScoreUpdate(BaseModel):
    score: int = Field(ge=0, le=100)

@app.get('/students')
def get_all_students():
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, city, score FROM students ORDER BY score DESC')
            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append({'id': row[0], 'name': row[1], 'city': row[2], 'score': row[3]})
        return result
    except psycopg2.OperationalError as e:
        raise HTTPException(status_code=500, detail=str(e))

        
@app.post('/students', status_code=201)
def create_student(student: Student):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO students (name, city, score) VALUES (%s, %s, %s) RETURNING id',
            (student.name, student.city, student.score))
            new_id = cursor.fetchone()[0]
            conn.commit()
        return {'id': new_id, 'name': student.name, 'city': student.city, 'score': student.score}
    except psycopg2.OperationalError as e:
        return HTTPException(status_code=500, detail=str(e))

@app.delete('/students/{student_id}')
def delete_student(student_id: int):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM students WHERE id = %s', (student_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail='Student not found')
            conn.commit()
        return {'message': f'Student {student_id} deleted'}
    except psycopg2.OperationalError as e:
        return HTTPException(status_code=500, detail=str(e))

@app.get('/students/city/{city}')
def students_from_city(city: str):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, city FROM students WHERE city = %s', (city,))
            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append({
                    "name": row[0],
                    "city": row[1]
                })
        return result
    except psycopg2.OperationalError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/students/{student_id}')
def update_student_score(student_id: int, update: ScoreUpdate):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE students SET score = %s WHERE id = %s', (update.score, student_id))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail='Student not found')
            conn.commit()
            return {'message': f'Student {student_id} score updaed', 'new_score': update.score}
    except psycopg2.OperationalError as e:
        return HTTPException(status_code=500, detail=str(e))

