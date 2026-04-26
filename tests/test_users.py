"""Kullanıcı kaydı, login ve /users/me testleri."""


def test_register_user(client):
    resp = client.post(
        "/users/register",
        json={"email": "alice@example.com", "password": "alicepass"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "alice@example.com"
    assert "id" in body
    assert "password" not in body
    assert "hashed_password" not in body


def test_register_duplicate_email(client):
    payload = {"email": "bob@example.com", "password": "bobpass1"}
    assert client.post("/users/register", json=payload).status_code == 201

    resp = client.post("/users/register", json=payload)
    assert resp.status_code == 409
    assert resp.json()["detail"] == "Email already registered"


def test_register_invalid_email(client):
    resp = client.post(
        "/users/register",
        json={"email": "not-an-email", "password": "whatever"},
    )
    assert resp.status_code == 422


def test_login_success(client):
    client.post(
        "/users/register",
        json={"email": "carol@example.com", "password": "carolpass"},
    )
    resp = client.post(
        "/users/login",
        json={"email": "carol@example.com", "password": "carolpass"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str) and body["access_token"]


def test_login_wrong_password(client):
    client.post(
        "/users/register",
        json={"email": "dan@example.com", "password": "danpass1"},
    )
    resp = client.post(
        "/users/login",
        json={"email": "dan@example.com", "password": "wrong-pass"},
    )
    assert resp.status_code == 401


def test_login_unknown_email(client):
    resp = client.post(
        "/users/login",
        json={"email": "ghost@example.com", "password": "irrelevant"},
    )
    assert resp.status_code == 401


def test_me_requires_auth(client):
    resp = client.get("/users/me")
    assert resp.status_code == 401


def test_me_returns_current_user(client, auth_headers):
    resp = client.get("/users/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "tester@example.com"


def test_me_rejects_invalid_token(client):
    resp = client.get(
        "/users/me",
        headers={"Authorization": "Bearer not-a-real-token"},
    )
    assert resp.status_code == 401
