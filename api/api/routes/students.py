from fastapi import APIRouter

router = APIRouter()

students = []

@router.get("/")
def get_students():
    return students

@router.post("/")
def add_student(student: dict):
    students.append(student)
    return {"message": "Student added", "data": student}
