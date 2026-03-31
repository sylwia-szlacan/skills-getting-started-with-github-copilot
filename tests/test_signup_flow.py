import pytest


class TestSignupFlow:
    """Test student signup for activities"""
    
    def test_successful_signup_adds_participant(self, client, reset_activities):
        # Arrange
        activity = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity}"
        
        # Verify participant was added
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity]["participants"]
    
    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_duplicate_signup_returns_400(self, client, reset_activities):
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_full_activity_returns_400(self, client, reset_activities):
        # Arrange
        activity = "Chess Club"  # max_participants = 2
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Fill the activity (already has michael@mergington.edu)
        client.post(f"/activities/{activity}/signup", params={"email": email1})
        
        # Act - try to sign up when full
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email2}
        )
        
        # Assert
        assert response.status_code == 400
        assert "Too many students" in response.json()["detail"]
