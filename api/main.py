from fastapi import FastAPI
from api.routes import students
from api.database import Base, engine
from api import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="REST API Book")

app.include_router(students.router, prefix="/students", tags=["Students"])


@app.get("/")
def root():
    return {"message": "API with PostgreSQL is running 🚀"}
