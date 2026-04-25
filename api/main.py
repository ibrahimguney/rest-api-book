from fastapi import FastAPI
from api.routes import students

app = FastAPI(title="REST API Book")

app.include_router(students.router, prefix="/students")

@app.get("/")
def root():
    return {"message": "API is running 🚀"}
