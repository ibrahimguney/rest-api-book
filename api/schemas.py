from pydantic import BaseModel, EmailStr


# -------------------------
# STUDENT
# -------------------------

class StudentCreate(BaseModel):
    name: str
    department: str


# -------------------------
# USER
# -------------------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
