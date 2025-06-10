from typing import Optional
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from api.models.course import Course
from api.serializers.course_serializer import CourseSerializer

class CourseDetailView(APIView):
    """
    Handle single course operations
    """
    def get_course(self, pk: int) -> Optional[Course]:
        """
        Retrieve a course by its primary key (pk).
        
        Args:
            pk (int): The primary key of the course to retrieve.

        Returns:
            Optional[Course]: The course object if found, otherwise None.
        """
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    def get(self, request: Request, pk: int) -> Response:
        """
        Retrieve a course by its primary key (pk).

        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the course to retrieve.

        Returns:
            Response: A response containing the course data or a 404 error if not found.
        """
        course: Optional[Course] = self.get_course(pk)
        if course is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def patch(self, request: Request, pk: int) -> Response:
        """
        Update a course by its primary key (pk).

        Args:
            request (Request): The HTTP request object containing course data.
            pk (int): The primary key of the course to update.

        Returns:
            Response: A response containing the updated course data or error messages.
        """
        course: Optional[Course] = self.get_course(pk)
        if course is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        """
        Delete a course by its primary key (pk).

        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the course to delete.

        Returns:
            Response: A response indicating the result of the deletion operation.
        """
        course: Optional[Course] = self.get_course(pk)
        if course is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        