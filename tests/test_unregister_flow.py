import pytest


class TestUnregisterFlow:
    """Test student unregistration from activities"""
    
    def test_successful_unregister_removes_participant(self, client, reset_activities):
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity}"
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        assert email not in activities_response.json()[activity]["participants"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client, reset_activities):
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_not_signed_up_returns_400(self, client, reset_activities):
        # Arrange
        activity = "Programming Class"
        email = "notsignup@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
