from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    instructor = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('user', 'code') 

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=255)
    due_date = models.DateField()
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

class StudyLog(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="study_logs")
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True, related_name="study_logs")
    date = models.DateField(auto_now_add=True)
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
