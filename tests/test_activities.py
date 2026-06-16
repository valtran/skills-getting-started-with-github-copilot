"""Tests for the Activities API endpoints using AAA (Arrange-Act-Assert) pattern."""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities."""
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        for activity_name in expected_activities:
            assert activity_name in data

    def test_get_activities_includes_participants(self, client):
        """Test that activities include participant lists."""
        # Arrange
        expected_participant = "michael@mergington.edu"

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert "participants" in data["Chess Club"]
        assert isinstance(data["Chess Club"]["participants"], list)
        assert expected_participant in data["Chess Club"]["participants"]

    def test_get_activities_has_required_fields(self, client):
        """Test that each activity has all required fields."""
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, f"Missing {field} in {activity_name}"
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful(self, client, reset_activities):
        """Test successful signup for an activity."""
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert new_email in data["message"]

        # Verify participant was added by fetching activities
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert new_email in activities[activity_name]["participants"]

    def test_signup_activity_not_found(self, client):
        """Test signup returns 404 for non-existent activity."""
        # Arrange
        non_existent_activity = "Non-Existent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{non_existent_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_prevents_duplicate(self, client, reset_activities):
        """Test that duplicate signup returns error."""
        # Arrange
        activity_name = "Chess Club"
        duplicate_email = "duplicate@mergington.edu"

        # Act - First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": duplicate_email}
        )
        assert response1.status_code == 200

        # Act - Attempt duplicate signup
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": duplicate_email}
        )

        # Assert
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"]

    def test_signup_response_format(self, client, reset_activities):
        """Test that signup response has correct format."""
        # Arrange
        activity_name = "Programming Class"
        email = "test@mergington.edu"
        expected_message_format = f"Signed up {email} for {activity_name}"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == expected_message_format


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup endpoint."""

    def test_unregister_successful(self, client, reset_activities):
        """Test successful unregistration from activity."""
        # Arrange
        activity_name = "Programming Class"
        email = "newstudent@mergington.edu"
        
        # First sign up the student
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act - Unregister
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_activity_not_found(self, client):
        """Test unregister returns 404 for non-existent activity."""
        # Arrange
        non_existent_activity = "Non-Existent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{non_existent_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_participant_not_signed_up(self, client):
        """Test unregister returns 404 when participant not registered."""
        # Arrange
        activity_name = "Chess Club"
        not_registered_email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": not_registered_email}
        )

        # Assert
        assert response.status_code == 404
        assert "not signed up" in response.json()["detail"]

    def test_unregister_response_format(self, client, reset_activities):
        """Test that unregister response has correct format."""
        # Arrange
        activity_name = "Gym Class"
        email = "tempstudent@mergington.edu"
        expected_message_format = f"Unregistered {email} from {activity_name}"

        # First sign up
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == expected_message_format


class TestActivityIntegration:
    """Integration tests for multi-step workflows."""

    def test_signup_and_unregister_workflow(self, client, reset_activities):
        """Test complete signup and unregister workflow."""
        # Arrange
        activity_name = "Art Club"
        email = "artist@mergington.edu"

        # Act - Sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert signup
        assert signup_response.status_code == 200
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]

        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert unregister
        assert unregister_response.status_code == 200
        activities = client.get("/activities").json()
        assert email not in activities[activity_name]["participants"]

    def test_multiple_participants_signup(self, client, reset_activities):
        """Test multiple participants signing up for same activity."""
        # Arrange
        activity_name = "Science Club"
        participants = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]

        # Act - Sign up all participants
        for email in participants:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Assert - All participants are registered
        activities = client.get("/activities").json()
        for email in participants:
            assert email in activities[activity_name]["participants"]
