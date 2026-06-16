"""Pytest configuration and fixtures for FastAPI tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def reset_activities(client):
    """Reset activities to initial state between tests."""
    # Store original activities state
    from src import app as app_module
    
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Competitive soccer team practicing skills and playing matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 22,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Team practices for inter-school basketball competitions",
            "schedule": "Mondays, Wednesdays, 4:30 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["sophia@mergington.edu", "oliver@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore drawing, painting, and mixed media projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["ava@mergington.edu", "mia@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, stagecraft, and school theatrical productions",
            "schedule": "Fridays, 3:30 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
        },
        "Debate Team": {
            "description": "Practice public speaking and competitive debating",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["lucas@mergington.edu", "ethan@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments, research projects, and science fairs",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["isabella@mergington.edu", "harper@mergington.edu"]
        }
    }
    
    app_module.activities.clear()
    app_module.activities.update(original_activities)
    yield
    # Reset after test
    app_module.activities.clear()
    app_module.activities.update(original_activities)
