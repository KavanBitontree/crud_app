import os
import sys

from fastapi.testclient import TestClient


def build_client(tmp_path):
    os.environ["DATABASE_URL"] = f"sqlite:///{tmp_path / 'test.db'}"
    os.environ["JWT_SECRET_KEY"] = "test-secret"

    for module_name in ["routes.auth", "main", "database", "security", "config"]:
        sys.modules.pop(module_name, None)

    import database
    import main
    from models.base import Base

    Base.metadata.drop_all(bind=database.engine)
    Base.metadata.create_all(bind=database.engine)
    return TestClient(main.app)


def test_signup_creates_user_without_returning_password(tmp_path):
    client = build_client(tmp_path)

    response = client.post(
        "/signup",
        json={"username": "alice", "password": "correct horse battery staple"},
    )

    assert response.status_code == 201
    assert response.json() == {"id": 1, "username": "alice"}


def test_signup_rejects_duplicate_username(tmp_path):
    client = build_client(tmp_path)
    payload = {"username": "alice", "password": "correct horse battery staple"}

    first = client.post("/signup", json=payload)
    duplicate = client.post("/signup", json=payload)

    assert first.status_code == 201
    assert duplicate.status_code == 409
    assert duplicate.json()["detail"] == "Username already registered"


def test_login_returns_bearer_token_for_valid_credentials(tmp_path):
    client = build_client(tmp_path)
    client.post(
        "/signup",
        json={"username": "alice", "password": "correct horse battery staple"},
    )

    response = client.post(
        "/login",
        json={"username": "alice", "password": "correct horse battery staple"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"].count(".") == 2


def test_login_rejects_bad_credentials(tmp_path):
    client = build_client(tmp_path)
    client.post(
        "/signup",
        json={"username": "alice", "password": "correct horse battery staple"},
    )

    response = client.post(
        "/login",
        json={"username": "alice", "password": "wrong password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_auth_routes_are_in_openapi_schema(tmp_path):
    client = build_client(tmp_path)

    schema = client.get("/openapi.json").json()

    assert "/signup" in schema["paths"]
    assert "/login" in schema["paths"]
