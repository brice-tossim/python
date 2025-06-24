from typing import List
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from api.models.course import Course
from api.serializers.course_serializer import CourseSerializer

class CourseListView(APIView):
    """
    Handle listing and creating courses
    """
    def get(self, request: Request) -> Response:
        """
        List all courses

        Args:
            request (Request): The HTTP request object

        Returns:
            Response: A response containing the list of courses
        """
        courses: List[Course] = list(Course.objects.all())
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Create a new course

        Args:
            request (Request): The HTTP request object containing course data

        Returns:
            Response: A response containing the created course data or error messages
        """
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)