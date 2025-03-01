from fastapi.testclient import TestClient
from app.main import app
import httpx
from app.database import Base, engine

# Create the database schema before running the tests
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "name": "Raju Cena",
        "age": 30,
        "gender": "male",
        "email": "raju.cena@example.com",
        "city": "New York",
        "interests": ["reading", "traveling"]
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Raju Cena"

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_user():
    response = client.put("/users/1", json={"name": "Raju Cena"})
    assert response.status_code == 200
    assert response.json()["name"] == "Raju Cena"


def test_find_matches():
    response = client.get("/users/1/matches")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_validate_email():
    response = client.post("/validate_email/", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1