import pytest


class TestActivityManagement:
    """Test activity data retrieval endpoints"""
    
    def test_root_redirects_to_static_index(self, client):
        # Arrange - no setup needed
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        # Arrange - activities fixture handles setup
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert len(data) >= 2
    
    def test_activity_has_required_fields(self, client, reset_activities):
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_info in data.items():
            for field in required_fields:
                assert field in activity_info, f"Missing field '{field}' in {activity_name}"
    
    def test_participants_is_list(self, client, reset_activities):
        # Arrange
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_info in data.values():
            assert isinstance(activity_info["participants"], list)
