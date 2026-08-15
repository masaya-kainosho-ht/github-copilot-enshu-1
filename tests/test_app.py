"""Tests for the Mergington High School Activities API."""

import pytest


class TestRootEndpoint:
    """Tests for GET / endpoint."""

    def test_root_redirects_to_static_index(self, client):
        """Root endpoint should redirect to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivitiesEndpoint:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_200(self, client, clean_activities):
        """GET /activities should return status 200."""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client, clean_activities):
        """Response should contain all activities with their details."""
        response = client.get("/activities")
        activities = response.json()
        
        # Should have all 9 activities
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities

    def test_get_activities_includes_activity_details(self, client, clean_activities):
        """Each activity should have required fields."""
        response = client.get("/activities")
        activities = response.json()
        
        chess_club = activities["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club

    def test_get_activities_includes_participants(self, client, clean_activities):
        """Activities should include list of participants."""
        response = client.get("/activities")
        activities = response.json()
        
        # Chess Club should have initial participants
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) > 0
        assert "michael@mergington.edu" in chess_club["participants"]


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_participant_returns_200(self, client, clean_activities, sample_email):
        """Valid signup should return status 200."""
        activity_name = "Chess Club"
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 200

    def test_signup_new_participant_returns_success_message(self, client, clean_activities, sample_email):
        """Successful signup should return success message."""
        activity_name = "Chess Club"
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client, clean_activities, sample_email):
        """Signup should add participant to activity's participant list."""
        activity_name = "Chess Club"
        initial_count = len(clean_activities[activity_name]["participants"])
        
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        
        assert sample_email in clean_activities[activity_name]["participants"]
        assert len(clean_activities[activity_name]["participants"]) == initial_count + 1

    def test_signup_invalid_activity_returns_404(self, client, clean_activities, sample_email):
        """Signup to nonexistent activity should return 404."""
        response = client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_duplicate_participant_returns_400(self, client, clean_activities):
        """Signing up same participant twice should return 400."""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_duplicate_does_not_add_participant(self, client, clean_activities):
        """Failed duplicate signup should not add participant again."""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        initial_count = len(clean_activities[activity_name]["participants"])
        
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Count should remain the same
        assert len(clean_activities[activity_name]["participants"]) == initial_count


class TestUnregisterEndpoint:
    """Tests for DELETE /activities/{activity_name}/signup endpoint."""

    def test_unregister_existing_participant_returns_200(self, client, clean_activities):
        """Valid unregister should return status 200."""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200

    def test_unregister_existing_participant_returns_success_message(self, client, clean_activities):
        """Successful unregister should return success message."""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_removes_participant_from_activity(self, client, clean_activities):
        """Unregister should remove participant from activity's list."""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        initial_count = len(clean_activities[activity_name]["participants"])
        
        client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        assert email not in clean_activities[activity_name]["participants"]
        assert len(clean_activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_invalid_activity_returns_404(self, client, clean_activities):
        """Unregister from nonexistent activity should return 404."""
        response = client.delete(
            "/activities/Nonexistent Club/signup",
            params={"email": "someone@mergington.edu"}
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_unregister_not_signed_up_participant_returns_400(self, client, clean_activities):
        """Unregistering participant not signed up should return 400."""
        activity_name = "Chess Club"
        email = "noone@mergington.edu"  # Not signed up
        
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"].lower()

    def test_unregister_not_signed_up_does_not_change_list(self, client, clean_activities):
        """Failed unregister should not change participant list."""
        activity_name = "Chess Club"
        email = "noone@mergington.edu"
        initial_list = clean_activities[activity_name]["participants"].copy()
        
        client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # List should remain unchanged
        assert clean_activities[activity_name]["participants"] == initial_list


class TestSignupAndUnregisterFlow:
    """Tests for signup and unregister workflow together."""

    def test_signup_then_unregister_flow(self, client, clean_activities, sample_email):
        """Should be able to signup and then unregister."""
        activity_name = "Chess Club"
        initial_count = len(clean_activities[activity_name]["participants"])
        
        # Signup
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        assert signup_response.status_code == 200
        assert sample_email in clean_activities[activity_name]["participants"]
        
        # Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        assert unregister_response.status_code == 200
        assert sample_email not in clean_activities[activity_name]["participants"]
        assert len(clean_activities[activity_name]["participants"]) == initial_count

    def test_signup_after_unregister(self, client, clean_activities, sample_email):
        """Should be able to signup again after unregistering."""
        activity_name = "Chess Club"
        
        # First signup
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        
        # Unregister
        client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        
        # Sign up again - should work
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 200
        assert sample_email in clean_activities[activity_name]["participants"]
