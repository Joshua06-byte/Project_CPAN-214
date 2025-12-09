from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    instructor = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('user', 'code')  # Each user can reuse codes

    def jsonFriendly(self):
        """Return a dictionary representation for JSON responses"""
        return {
            'id': self.id,
            'user_id': self.user.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'instructor': self.instructor
        }

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=255)
    due_date = models.DateField()
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    def jsonFriendly(self):
        return {
            'id': self.id,
            'course_id': self.course.id,
            'title': self.title,
            'due_date': self.due_date.isoformat(),
            'description': self.description,
            'is_completed': self.is_completed
        }

class StudyLog(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="study_logs")
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True, related_name="study_logs")
    date = models.DateField(auto_now_add=True)
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True)

    def jsonFriendly(self):
        return {
            'id': self.id,
            'course_id': self.course.id,
            'assignment_id': self.assignment.id if self.assignment else None,
            'date': self.date.isoformat(),
            'duration_minutes': self.duration_minutes,
            'notes': self.notes
        }
