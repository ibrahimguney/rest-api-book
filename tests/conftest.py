"""
Test ayarlari: gercek PostgreSQL yerine gecici bir SQLite veritabani kullan.

Bu dosya pytest tarafindan otomatik yuklenir ve api.* modullerinden
herhangi biri import edilmeden ONCE calisir. Bu sayede api.database modulu,
DATABASE_URL ortam degiskeninden SQLite URL'sini alarak bir test engine'i kurar.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

# api.* modulleri import edilmeden ONCE env degiskenini ayarla.
TEST_DB_PATH = Path(__file__).parent / "_test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH.as_posix()}"
os.environ.setdefault("SECRET_KEY", "test-secret-key")

from fastapi.testclient import TestClient  # noqa: E402

from api.database import Base, engine  # noqa: E402
from api.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_database():
    """Her test oncesi tablolari sifirla."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def auth_headers(client: TestClient) -> dict[str, str]:
    """Bir kullanici olustur, login ol ve Authorization header'ini dondur."""
    email = "tester@example.com"
    password = "supersecret"

    client.post("/users/register", json={"email": email, "password": password})
    resp = client.post("/users/login", json={"email": email, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def pytest_sessionfinish(session, exitstatus):
    """Test bittiginde gecici DB dosyasini sil."""
    try:
        TEST_DB_PATH.unlink(missing_ok=True)
    except OSError:
        pass
