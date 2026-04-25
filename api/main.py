from fastapi import FastAPI

from api.database import Base, engine
from api import models
from api.routes import students, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="REST API Book")

app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(users.router, prefix="/users", tags=["Users"])


@app.get("/")
def root():
    return {"message": "API with PostgreSQL and JWT is running 🚀"}
