from pydantic import BaseModel, ConfigDict, EmailStr, Field


# -------------------------
# STUDENT
# -------------------------

class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    department: str = Field(..., min_length=1, max_length=120)


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# USER
# -------------------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# TOKEN
# -------------------------

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
