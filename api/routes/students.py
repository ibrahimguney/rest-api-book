from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
from api.models import Student
from api.schemas import StudentCreate, StudentResponse
from api.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Student).all()

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/", response_model=StudentResponse, status_code=201)
def add_student(student: StudentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_student = Student(name=student.name, department=student.department)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, updated: StudentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    student.name = updated.name
    student.department = updated.department
    db.commit()
    db.refresh(student)
    return student

@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
