import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock


# Mock the graph module before importing main
@patch('graphs.workflow.build_graph')
def get_client(mock_build_graph):
    """Create test client with mocked graph"""
    mock_graph = AsyncMock()
    mock_build_graph.return_value = mock_graph
    
    from main import app
    return TestClient(app), mock_graph


class TestRootEndpoint:
    """Test the root endpoint"""
    
    def test_root_returns_welcome_message(self):
        """Test GET / returns welcome message"""
        client, _ = get_client()
        response = client.get("/")
        
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the ai-startup-validator API"}


class TestValidateEndpoint:
    """Test the /validate endpoint"""
    
    def test_validate_without_startup_idea(self):
        """Test POST /validate without startup_idea field"""
        client, _ = get_client()
        
        response = client.post("/validate", json={})
        
        assert response.status_code == 422
    
    def test_validate_with_invalid_json(self):
        """Test POST /validate with invalid JSON"""
        client, _ = get_client()
        
        response = client.post(
            "/validate",
            data="not a json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_validate_with_wrong_field_type(self):
        """Test POST /validate with number instead of string"""
        client, _ = get_client()
        
        response = client.post("/validate", json={"startup_idea": 123})
        
        assert response.status_code == 422


class TestHTTPMethods:
    """Test HTTP methods"""
    
    def test_validate_only_accepts_post(self):
        """Test that /validate only accepts POST requests"""
        client, _ = get_client()
        
        # GET should fail
        response = client.get("/validate")
        assert response.status_code == 405
        
        # PUT should fail
        response = client.put("/validate")
        assert response.status_code == 405
        
        # DELETE should fail
        response = client.delete("/validate")
        assert response.status_code == 405
    
    def test_root_only_accepts_get(self):
        """Test that / only accepts GET requests"""
        client, _ = get_client()
        
        response = client.post("/")
        assert response.status_code == 405