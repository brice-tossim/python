from django.db import models

class Course(models.Model):
    """
    Course model representing a course in the system.
    """
    id: models.AutoField = models.AutoField(primary_key=True)
    title: models.CharField = models.CharField(max_length=100)
    summary: models.TextField = models.TextField()
    created_at: models.DateField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateField = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "courses"