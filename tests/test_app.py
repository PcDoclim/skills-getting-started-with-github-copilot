import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (nothing to set up for in-memory data)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_prevent_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response1.status_code == 200
    assert f"Signed up {email}" in response1.json()["message"]
    # Act (try duplicate)
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]

def test_unregister_participant():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

def test_signup_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "ghost@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
