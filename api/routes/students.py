from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from api.auth import get_current_user
from api.database import get_db
from api.models import Student, User
from api.schemas import StudentCreate, StudentResponse

router = APIRouter()


@router.get("/", response_model=list[StudentResponse])
def get_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.query(Student).offset(skip).limit(limit).all()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    new_student = Student(name=student.name, department=student.department)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    updated_student: StudentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = updated_student.name
    student.department = updated_student.department

    db.commit()
    db.refresh(student)
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    # 204 No Content
