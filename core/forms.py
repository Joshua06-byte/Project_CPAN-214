from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Course, Assignment, StudyLog
from django.contrib.auth.models import User


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'instructor']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'due_date', 'description', 'is_completed']

class StudyLogForm(forms.ModelForm):
    class Meta:
        model = StudyLog
        fields = ['assignment', 'duration_minutes', 'notes']

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('course-list')  