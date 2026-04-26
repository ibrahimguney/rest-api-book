"""Students CRUD testleri (tum uclar auth ister)."""


def test_list_students_requires_auth(client):
    resp = client.get("/students/")
    assert resp.status_code == 401


def test_list_students_empty(client, auth_headers):
    resp = client.get("/students/", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_student_requires_auth(client):
    resp = client.post(
        "/students/",
        json={"name": "Ada Lovelace", "department": "Math"},
    )
    assert resp.status_code == 401


def test_create_student_with_auth(client, auth_headers):
    resp = client.post(
        "/students/",
        json={"name": "Ada Lovelace", "department": "Math"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["id"] >= 1
    assert body["name"] == "Ada Lovelace"
    assert body["department"] == "Math"


def test_create_student_validation(client, auth_headers):
    resp = client.post(
        "/students/",
        json={"name": "", "department": "Math"},
        headers=auth_headers,
    )
    assert resp.status_code == 422


def test_get_student_by_id(client, auth_headers):
    created = client.post(
        "/students/",
        json={"name": "Alan Turing", "department": "CS"},
        headers=auth_headers,
    ).json()
    resp = client.get(f"/students/{created['id']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Alan Turing"


def test_get_student_not_found(client, auth_headers):
    resp = client.get("/students/9999", headers=auth_headers)
    assert resp.status_code == 404


def test_get_student_requires_auth(client):
    resp = client.get("/students/1")
    assert resp.status_code == 401


def test_update_student(client, auth_headers):
    created = client.post(
        "/students/",
        json={"name": "Grace Hopper", "department": "CS"},
        headers=auth_headers,
    ).json()

    resp = client.put(
        f"/students/{created['id']}",
        json={"name": "Grace M. Hopper", "department": "Computer Science"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "Grace M. Hopper"
    assert body["department"] == "Computer Science"


def test_update_student_requires_auth(client, auth_headers):
    created = client.post(
        "/students/",
        json={"name": "Linus", "department": "OS"},
        headers=auth_headers,
    ).json()

    resp = client.put(
        f"/students/{created['id']}",
        json={"name": "Linus T.", "department": "OS"},
    )
    assert resp.status_code == 401


def test_delete_student(client, auth_headers):
    created = client.post(
        "/students/",
        json={"name": "Donald Knuth", "department": "CS"},
        headers=auth_headers,
    ).json()

    resp = client.delete(f"/students/{created['id']}", headers=auth_headers)
    assert resp.status_code == 204
    assert resp.content == b""

    # Ayni id artik 404 dondurmeli.
    assert client.get(
        f"/students/{created['id']}", headers=auth_headers
    ).status_code == 404


def test_delete_student_requires_auth(client):
    resp = client.delete("/students/1")
    assert resp.status_code == 401


def test_list_students_pagination(client, auth_headers):
    for i in range(5):
        client.post(
            "/students/",
            json={"name": f"Student {i}", "department": "Dept"},
            headers=auth_headers,
        )

    resp = client.get("/students/?skip=1&limit=2", headers=auth_headers)
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 2
    assert items[0]["name"] == "Student 1"
    assert items[1]["name"] == "Student 2"
