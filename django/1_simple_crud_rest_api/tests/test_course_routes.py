from typing import Dict
from django.urls import reverse
import pytest

from rest_framework import status
from rest_framework.test import APIClient

from api.models.course import Course


@pytest.mark.django_db
class TestCourseViews:
    """Test suite for course-related views in the API."""

    def test_list_courses(self, api_client: APIClient) -> None:
        # Arrange
        url: str = reverse('course-list')
        Course.objects.create(
            title="Test title",
            summary="This is a test summary"
        )

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        result: Dict[str, str] = response.data[0]
        assert result['title'] + ' - ' + result['summary'] == 'Test title - This is a test summary'

    def test_create_course(self, api_client: APIClient) -> None:
        # Arrange
        url: str = reverse('course-list')
        payload: Dict[str, str] = {
            'title': 'New course',
            'summary': 'This is another course'
        }

        # Act
        response = api_client.post(url, payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Course.objects.count() == 1
        
        new_course = Course.objects.get()
        assert new_course.title + ' - ' + new_course.summary == 'New course - This is another course'

    def test_get_course(self, api_client: APIClient, sample_course: Course):
        # Arrange
        url: str = reverse('course-detail', args=[sample_course.id])

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        result: Dict[str, str] = response.data
        assert result['title'] + ' - ' + result['summary'] == 'Sample course - This is a sample course summary...'


    def test_update_course(self, api_client: APIClient, sample_course: Course) -> None:
        # Arrange
        url: str = reverse('course-detail', args=[sample_course.id])
        payload: Dict[str, str] = {
            'summary': 'Updated summary of the sample course'
        }

        # Act
        response = api_client.patch(url, payload)

        # Assert
        assert response.status_code == status.HTTP_200_OK

        result: Dict[str, str] = response.data
        assert result['title'] + ' - ' + result['summary'] == 'Sample course - Updated summary of the sample course'

    def test_delete_course(self, api_client: APIClient, sample_course: Course) -> None:
        # Arrange
        url: str = reverse('course-detail', args=[sample_course.id])

        # Act
        response = api_client.delete(url)

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Course.objects.count() == 0

    def test_create_course_invalid_data(self, api_client: APIClient) -> None:
        """Test creating a course with invalid data returns 400."""
        # Arrange
        url: str = reverse('course-list')
        payload: Dict[str, str] = {
            'title': '',  # Empty title should fail validation
            'summary': 'This is another course'
        }

        # Act
        response = api_client.post(url, payload)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'title' in response.data  # Check error message exists for title

    def test_get_nonexistent_course(self, api_client: APIClient) -> None:
        """Test getting a course that doesn't exist returns 404."""
        # Arrange
        url: str = reverse('course-detail', args=[999])  # Non-existent ID

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_nonexistent_course(self, api_client: APIClient) -> None:
        """Test updating a non-existent course returns 404."""
        # Arrange
        url: str = reverse('course-detail', args=[999])
        payload: Dict[str, str] = {
            'summary': 'Updated summary'
        }

        # Act
        response = api_client.patch(url, payload)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_course(self, api_client: APIClient) -> None:
        """Test deleting a non-existent course returns 404."""
        # Arrange
        url: str = reverse('course-detail', args=[999])

        # Act
        response = api_client.delete(url)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_course_invalid_data(self, api_client: APIClient, sample_course: Course) -> None:
        """Test updating a course with invalid data returns 400."""
        # Arrange
        url: str = reverse('course-detail', args=[sample_course.id])
        payload: Dict[str, str] = {
            'title': ''  # Empty title should fail validation
        }

        # Act
        response = api_client.patch(url, payload)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'title' in response.data  # Check error message exists for title
        