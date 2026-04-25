from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database import SessionLocal
from api.models import Student
from api.schemas import StudentCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.post("/")
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        name=student.name,
        department=student.department
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student   # ⚠️ sadece bunu döndür!
