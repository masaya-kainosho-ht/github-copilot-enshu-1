"""Pytest configuration and fixtures for FastAPI tests."""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import app as app_module
from app import app


# Store the original activities state
ORIGINAL_ACTIVITIES = {
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
    "Basketball Team": {
        "description": "Competitive basketball training and tournaments",
        "schedule": "Mondays, Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis skills development and friendly matches",
        "schedule": "Tuesdays, Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["sarah@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and visual arts",
        "schedule": "Wednesdays, Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["jessica@mergington.edu", "alex@mergington.edu"]
    },
    "Music Band": {
        "description": "Learn instruments and perform in concerts",
        "schedule": "Mondays, Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["david@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["rachel@mergington.edu", "christopher@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore scientific experiments and research",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["kevin@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """Provide a TestClient instance for API testing."""
    return TestClient(app)


@pytest.fixture
def clean_activities():
    """
    Reset activities to a clean state before each test.
    This prevents test interdependencies due to the global activities dict.
    """
    # Clear the global activities dict and repopulate with original data
    app_module.activities.clear()
    app_module.activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    
    yield app_module.activities
    
    # Cleanup after test (reset to original state)
    app_module.activities.clear()
    app_module.activities.update(deepcopy(ORIGINAL_ACTIVITIES))


@pytest.fixture
def sample_email():
    """Provide a sample email for signup tests."""
    return "test.student@mergington.edu"
