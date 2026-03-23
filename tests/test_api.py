"""
Tests for FastAPI activities API endpoints using AAA pattern
(Arrange, Act, Assert)
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities_returns_data(client):
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Drama Club",
        "Art Studio",
        "Debate Team",
        "Science Club",
    ]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    for activity_name in expected_activities:
        assert activity_name in data
        assert "description" in data[activity_name]
        assert "schedule" in data[activity_name]
        assert "participants" in data[activity_name]


def test_post_signup_works(client):
    # Arrange
    activity_name = "Chess Club"
    email = "netstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Signed up" in response.json()["message"]


def test_post_signup_rejects_duplicates(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_delete_unregister_works(client):
    # Arrange
    activity_name = "Drama Club"
    email = "nobody@mergington.edu"

    # Ensure signup first
    response_signup = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert response_signup.status_code == 200

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]


def test_delete_unregister_rejects_nonexistent(client):
    # Arrange
    activity_name = "Drama Club"
    email = "doesnotexist@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"].lower()
