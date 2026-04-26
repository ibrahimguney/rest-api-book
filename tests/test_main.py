"""Health & root endpoint testleri."""


def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "message" in resp.json()


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_openapi_schema(client):
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    paths = resp.json()["paths"]
    assert "/students/" in paths
    assert "/users/register" in paths
    assert "/users/login" in paths
