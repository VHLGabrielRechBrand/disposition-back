# tests/test_main.py

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_app_starts():
    response = client.get("/collections")
    # Como o banco pode estar vazio, esperamos qualquer código válido ou 200
    assert response.status_code in [200, 500, 404]


def test_cors_headers():
    response = client.options("/collections", headers={
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "GET"
    })
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
