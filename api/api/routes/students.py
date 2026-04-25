from fastapi import APIRouter

router = APIRouter()

students = []

@router.get("/")
def get_students():
    return students
