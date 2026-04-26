from fastapi import FastAPI

from api.database import Base, engine
from api import models  # noqa: F401  (modelleri Base'e kaydetmek icin import)
from api.routes import students, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="REST API Book",
    description="REST API, Docker, PostgreSQL ve JWT ile uygulamali kitap projesi.",
    version="1.0.0",
)

app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(users.router, prefix="/users", tags=["Users"])


@app.get("/", tags=["Health"])
def root():
    return {"message": "API with PostgreSQL and JWT is running"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
