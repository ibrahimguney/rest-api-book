from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    name: str
    department: str

class StudentResponse(BaseModel):
    id: int
    name: str
    department: str

    model_config = {"from_attributes": True}

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = {"from_attributes": True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
