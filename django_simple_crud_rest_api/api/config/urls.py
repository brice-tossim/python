from django.urls import path

from api.views.course.course_detail import CourseDetailView
from api.views.course.course_list import CourseListView


urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail')
]