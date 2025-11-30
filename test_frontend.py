import pytest
from unittest.mock import Mock, patch, MagicMock
import requests
from streamlit.testing.v1 import AppTest


class TestStartupValidatorApp:
    """Test suite for the Startup Idea Validation Tool frontend"""
    
    @pytest.fixture
    def mock_successful_response(self):
        """Fixture for successful API response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "advice": "Great startup idea with strong market potential.",
            "advisor_recommendations": "Focus on MVP development and user validation.",
            "startup_idea": "AI-powered task management",
            "market_analysis": "Growing market with $5B TAM",
            "competition_analysis": "Moderate competition with differentiation opportunities",
            "risk_assessment": "Medium risk - technology and market risks identified"
        }
        return mock_response
    
    @pytest.fixture
    def mock_error_response(self):
        """Fixture for error API response"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        return mock_response

    def test_page_configuration(self):
        """Test that page is configured correctly"""
        at = AppTest.from_file("app.py")
        at.run()
        
        # Check page renders without errors
        assert not at.exception
        
    def test_page_title_and_description(self):
        """Test that title and description are displayed"""
        at = AppTest.from_file("app.py")
        at.run()
        
        # Check for title
        assert len(at.title) > 0
        assert "starup idea validation tool" in at.title[0].value.lower()
        
        # Check for description text
        assert len(at.markdown) > 0

    def test_text_area_exists(self):
        """Test that text area for startup idea exists"""
        at = AppTest.from_file("app.py")
        at.run()
        
        assert len(at.text_area) > 0
        assert "Enter your startup idea" in at.text_area[0].label

    def test_validate_button_exists(self):
        """Test that validate button exists"""
        at = AppTest.from_file("app.py")
        at.run()
        
        assert len(at.button) > 0
        assert at.button[0].label.lower() == "validate"

    @patch('requests.post')
    def test_successful_validation(self, mock_post, mock_successful_response):
        """Test successful validation flow"""
        mock_post.return_value = mock_successful_response
        
        at = AppTest.from_file("app.py")
        at.run()
        
        # Enter startup idea
        at.text_area[0].input("AI-powered task management app").run()
        
        # Click validate button
        at.button[0].click().run()
        
        # Check that API was called
        mock_post.assert_called_once()
        
        # Verify success message is displayed
        assert len(at.success) > 0
        assert "Validation successful" in at.success[0].value
        
        # Check that results are displayed in markdown
        markdown_content = " ".join([m.value for m in at.markdown])
        assert "Great startup idea" in markdown_content
        assert "market_analysis" in markdown_content

    @patch('requests.post')
    def test_api_error_handling(self, mock_post, mock_error_response):
        """Test handling of API errors"""
        mock_post.return_value = mock_error_response
        
        at = AppTest.from_file("app.py")
        at.run()
        
        # Enter startup idea
        at.text_area[0].input("Test idea").run()
        
        # Click validate button
        at.button[0].click().run()
        
        # Check that error message is displayed
        assert len(at.error) > 0
        assert "500" in at.error[0].value

    @patch('requests.post')
    def test_connection_error_handling(self, mock_post):
        """Test handling of connection errors"""
        mock_post.side_effect = requests.exceptions.ConnectionError()
        
        at = AppTest.from_file("app.py")
        at.run()
        
        # Enter startup idea
        at.text_area[0].input("Test idea").run()
        
        # Click validate button
        at.button[0].click().run()
        
        # Check that connection error message is displayed
        assert len(at.error) > 0
        assert "Unable to connect" in at.error[0].value

    def test_empty_input_validation(self):
        """Test validation with empty input"""
        at = AppTest.from_file("app.py")
        at.run()
        
        # Click validate without entering idea
        at.button[0].click().run()
        
        # Check that error message is displayed
        assert len(at.error) > 0
        assert "Please enter your startup idea" in at.error[0].value

    @patch('requests.post')
    def test_api_call_payload(self, mock_post, mock_successful_response):
        """Test that API is called with correct payload"""
        mock_post.return_value = mock_successful_response
        
        at = AppTest.from_file("app.py")
        at.run()
        
        test_idea = "Revolutionary blockchain solution"
        at.text_area[0].input(test_idea).run()
        at.button[0].click().run()
        
        # Verify the API was called with correct data
        call_args = mock_post.call_args
        assert call_args[1]['json']['startup_idea'] == test_idea

    @patch('requests.post')
    def test_all_response_fields_displayed(self, mock_post, mock_successful_response):
        """Test that all response fields are displayed"""
        mock_post.return_value = mock_successful_response
        
        at = AppTest.from_file("app.py")
        at.run()
        
        at.text_area[0].input("Test startup").run()
        at.button[0].click().run()
        
        # Collect all markdown content
        markdown_content = " ".join([m.value for m in at.markdown])
        
        # Check all expected fields are present
        expected_fields = [
            "advisor_recommendations",
            "startup_idea",
            "market_analysis",
            "competition_analysis",
            "risk_assessment"
        ]
        
        for field in expected_fields:
            assert field in markdown_content

    @patch('requests.post')
    def test_spinner_during_validation(self, mock_post, mock_successful_response):
        """Test that spinner is shown during validation"""
        mock_post.return_value = mock_successful_response
        
        at = AppTest.from_file("app.py")
        at.run()
        
        at.text_area[0].input("Test idea").run()
        at.button[0].click().run()
        
        # The spinner should have been displayed (checked via no exception)
        assert not at.exception

    @patch('config.BASE_URL', 'http://test-api.com')
    @patch('requests.post')
    def test_correct_api_endpoint(self, mock_post, mock_successful_response):
        """Test that correct API endpoint is used"""
        mock_post.return_value = mock_successful_response
        
        at = AppTest.from_file("app.py")
        at.run()
        
        at.text_area[0].input("Test").run()
        at.button[0].click().run()
        
        # Check the URL used in the API call
        call_args = mock_post.call_args
        assert '/validate' in call_args[0][0]


# Integration test example
class TestIntegration:
    """Integration tests requiring actual backend"""
    
    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires running backend server")
    def test_real_api_integration(self):
        """Test with real API (requires backend to be running)"""
        at = AppTest.from_file("app.py")
        at.run()
        
        at.text_area[0].input("AI-powered fitness tracker").run()
        at.button[0].click().run()
        
        # Should get actual response from backend
        assert len(at.success) > 0 or len(at.error) > 0