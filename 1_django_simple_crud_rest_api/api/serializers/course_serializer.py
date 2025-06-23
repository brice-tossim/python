from typing import Any
from rest_framework import serializers

from api.models.course import Course

class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model.
    """
    class Meta:
        model = Course
        fields = '__all__'