"""Tests for the Mergington High School API"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory activity state before each test."""
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        },
    })
    yield


def test_get_activities_returns_initial_data():
    # Arrange
    # (already arranged by fixture)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_adds_participant():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]
    assert email in activities[activity]["participants"]


def test_signup_duplicate_returns_400():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already" in response.json()["detail"].lower()


def test_delete_participant_then_404_on_second_delete():
    # Arrange
    activity = "Chess Club"
    email = "daniel@mergington.edu"

    # Act
    first = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert first.status_code == 200
    assert email not in activities[activity]["participants"]

    # Act second time
    second = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert second time
    assert second.status_code == 404
    assert "participant not found" in second.json()["detail"].lower()
