import pytest
from rest_framework.test import APIClient

from api.models.course import Course


@pytest.fixture
def api_client() -> APIClient:
    """
    Fixture to provide an instance of the APIClient for testing.

    Returns:
        APIClient: An instance of the APIClient for making requests in tests.
    """
    return APIClient()

@pytest.fixture
def sample_course() -> Course:
    """
    Fixture to create a sample course for testing purposes.

    Returns:
        Course: An instance of the Course model with sample data.
    """

    course = Course.objects.create(
        title="Sample course",
        summary="This is a sample course summary..."
    )

    return course