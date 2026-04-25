from fastapi import FastAPI
from api.routes import students
from api.database import engine, Base
from api import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="REST API Book")

app.include_router(students.router, prefix="/students")

@app.get("/")
def root():
    return {"message": "API with PostgreSQL is running 🚀"}
