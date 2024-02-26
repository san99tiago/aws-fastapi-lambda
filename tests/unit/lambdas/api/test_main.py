from fastapi.testclient import TestClient
from src.lambdas.api.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello by Santi"}


def test_read_status_no_query():
    response = client.get("/items/123")
    assert response.status_code == 200
    assert response.json() == {"item_id": 123, "q": None}


def test_read_status_with_query():
    response = client.get("/items/456?q=Santi")
    assert response.status_code == 200
    assert response.json() == {"item_id": 456, "q": "Santi"}


def test_update_item_success():
    response = client.put(
        "/items/789",
        json={
            "name": "test name",
            "price": 99.9,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"item_name": "test name", "item_id": 789}


def test_update_item_wrong_payload():
    response = client.put(
        "/items/789",
        json={
            "name": "test name",
            "amount": 99.9,  # Intentionally wrong key (not in model)
        },
    )
    assert response.status_code == 422
