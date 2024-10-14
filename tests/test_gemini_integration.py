import pytest
from unittest.mock import Mock, patch
from src.useful_functions import call_gemini

# Mock GeminiClient class and get_main_prompt function
@pytest.fixture
def mock_gemini_client():
    with patch("src.useful_functions.GeminiClient") as mock_client:
        mock_client_instance = mock_client.return_value
        mock_client_instance.generate.return_value = "Mock response"
        yield mock_client_instance

def test_call_gemini_single_chunk(mock_gemini_client):
    chunks = ["This is a test chunk."]
    response = call_gemini(chunks, user_message="Test question")
    assert response == "Mock response", "Gemini API response did not match."

def test_call_gemini_multiple_chunks(mock_gemini_client):
    chunks = ["Chunk 1", "Chunk 2"]
    response = call_gemini(chunks, user_message="Test question")
    assert response == "Mock response", "Gemini API response did not match."
