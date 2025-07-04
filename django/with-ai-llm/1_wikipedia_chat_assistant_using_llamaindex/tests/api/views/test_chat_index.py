"""
Tests for the ChatView API endpoint.

This module contains test cases for the ChatView, which handles chat requests
and returns responses using the WikipediaRagService.
"""
from typing import Dict
from unittest.mock import patch, MagicMock

from django.test import TestCase
from rest_framework import status


class TestChatView(TestCase):
    """Test cases for the ChatView API endpoint."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.url = "/api/chat/"
        self.valid_payload: Dict[str, str] = {"query": "What is Python?"}
        self.invalid_payload: Dict[str, str] = {}

    def test_post_missing_query(self) -> None:
        """Test that a request with a missing query returns a 400 status code."""
        # Act
        response = self._post_payload({})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertEqual(data["error"], "Validation error")
        self.assertIn("details", data)
        self.assertTrue(any("Field 'query' is required" in msg for msg in data["details"]))

    def test_post_empty_query(self) -> None:
        """Test that a request with an empty query returns a 400 status code."""
        # Act
        response = self._post_payload({"query": ""})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertEqual(data["error"], "Validation error")
        self.assertIn("details", data)
        # The actual error message from Pydantic might be different, so we'll just check for the field name
        self.assertTrue(any("query" in msg.lower() for msg in data["details"]))

    @patch('api.views.chat.index.WikipediaRagService')
    def test_post_success(self, mock_rag_service: MagicMock) -> None:
        """Test that a valid request returns a successful response."""
        # Arrange
        mock_response = "Python is a high-level programming language..."
        mock_service = mock_rag_service.return_value
        mock_service.query.return_value = mock_response

        # Create a valid payload that matches the expected format
        query = "What is Python?"
        valid_payload = {"query": query}

        # Act
        response = self._post_payload(valid_payload)

        # Debug output
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content}")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f"Expected status 200 but got {response.status_code}. Response: {response.content}")
        data = response.json()
        self.assertEqual(data["response"], mock_response)
        mock_service.query.assert_called_once_with(query)

    @patch('api.views.chat.index.WikipediaRagService')
    def test_service_error_handling(self, mock_rag_service: MagicMock) -> None:
        """Test that service errors are properly handled."""
        # Arrange
        mock_service = mock_rag_service.return_value
        # We need to mock the service to raise the exception after validation passes
        mock_service.query.side_effect = Exception("Service error")

        # Create a valid payload that will pass validation
        valid_payload = {"query": "test query"}

        # Act
        response = self._post_payload(valid_payload)

        # Debug output
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content}")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR,
                         f"Expected status 500 but got {response.status_code}. Response: {response.content}")
        data = response.json()
        self.assertEqual(data["error"], "Unexpected error")

    def _post_payload(self, valid_payload):
        return self.client.post(
            self.url,
            data=valid_payload,
            content_type='application/json',
            format='json'
        )
