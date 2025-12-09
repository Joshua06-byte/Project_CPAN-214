import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Course, Assignment, StudyLog


# REGISTER

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if not username or not password or not password2:
            messages.error(request, "All fields are required.")
            return render(request, "registration/register.html")

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "registration/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "registration/register.html")

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("course-list")

    return render(request, "registration/register.html")


# COURSES

@login_required
def course_list(request):
    courses = Course.objects.filter(user=request.user)
    data = [c.jsonFriendly() for c in courses]
    return JsonResponse({'courses': data})

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk, user=request.user)
    return JsonResponse(course.jsonFriendly())

@login_required
@require_http_methods(["POST"])
def course_create(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        code = data.get('code')
        description = data.get('description')
        instructor = data.get('instructor')

        if not name or any(c.isdigit() for c in name):
            raise ValueError("Course name is required and cannot contain numbers.")
        if not code:
            raise ValueError("Course code is required.")
        if Course.objects.filter(user=request.user, code=code).exists():
            raise ValueError("You already created a course with this code.")

        course = Course.objects.create(
            user=request.user,
            name=name,
            code=code,
            description=description,
            instructor=instructor
        )
        return JsonResponse(course.jsonFriendly())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(["PUT"])
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk, user=request.user)
    try:
        data = json.loads(request.body)
        name = data.get('name')
        code = data.get('code')
        description = data.get('description')
        instructor = data.get('instructor')

        if not name or any(c.isdigit() for c in name):
            raise ValueError("Course name is required and cannot contain numbers.")
        if not code:
            raise ValueError("Course code is required.")
        if Course.objects.filter(user=request.user, code=code).exclude(id=course.id).exists():
            raise ValueError("Another course with this code already exists.")

        course.name = name
        course.code = code
        course.description = description
        course.instructor = instructor
        course.save()

        return JsonResponse(course.jsonFriendly())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(["DELETE"])
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, user=request.user)
    course.delete()
    return JsonResponse({'success': True})


# ASSIGNMENTS

@login_required
@require_http_methods(["POST"])
def assignment_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk, user=request.user)
    try:
        data = json.loads(request.body)
        title = data.get('title')
        due_date_raw = data.get('due_date')
        description = data.get('description')
        is_completed = data.get('is_completed', False)

        if not title:
            raise ValueError("Assignment title is required.")
        if not due_date_raw:
            raise ValueError("Due date is required.")
        try:
            due_date = datetime.strptime(due_date_raw, "%Y-%m-%d").date()
        except:
            raise ValueError("Due date must be in YYYY-MM-DD format.")

        assignment = Assignment.objects.create(
            course=course,
            title=title,
            due_date=due_date,
            description=description,
            is_completed=is_completed
        )
        return JsonResponse(assignment.jsonFriendly())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(["PUT"])
def assignment_update(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, course__user=request.user)
    try:
        data = json.loads(request.body)
        title = data.get('title')
        due_date_raw = data.get('due_date')
        description = data.get('description')
        is_completed = data.get('is_completed', False)

        if not title:
            raise ValueError("Assignment title is required.")
        if not due_date_raw:
            raise ValueError("Due date is required.")
        try:
            due_date = datetime.strptime(due_date_raw, "%Y-%m-%d").date()
        except:
            raise ValueError("Due date must be in YYYY-MM-DD format.")

        assignment.title = title
        assignment.due_date = due_date
        assignment.description = description
        assignment.is_completed = is_completed
        assignment.save()

        return JsonResponse(assignment.jsonFriendly())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(["DELETE"])
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, course__user=request.user)
    assignment.delete()
    return JsonResponse({'success': True})


# STUDYLOGS

@login_required
@require_http_methods(["POST"])
def studylog_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk, user=request.user)
    try:
        data = json.loads(request.body)
        assignment_id = data.get('assignment')
        duration_raw = data.get('duration_minutes')
        notes = data.get('notes')

        if not duration_raw or not str(duration_raw).isdigit() or int(duration_raw) <= 0:
            raise ValueError("Duration must be a positive number.")

        assignment = Assignment.objects.filter(pk=assignment_id, course=course).first() if assignment_id else None
        if assignment_id and not assignment:
            raise ValueError("Invalid assignment selected.")

        studylog = StudyLog.objects.create(
            course=course,
            assignment=assignment,
            duration_minutes=int(duration_raw),
            notes=notes
        )
        return JsonResponse(studylog.jsonFriendly())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(["PUT"])
def studylog_update(request, pk):
    studylog = get_object_or_404(StudyLog, pk=pk, course__user=request.user)
    try:
        data = json.loads(request.body)
        assignment_id = data.get('assignment')
        duration_raw = data.get('duration_minutes')
        notes = data.get('notes')

        if not duration_raw or not str(duration_raw).isdigit() or int(duration_raw) <= 0:
            raise ValueError("Duration must be a positive number.")

        assignment = Assignment.objects.filter(pk=assignment_id, course=studylog.course).first() if assignment_id else None
        if assignment_id and not assignment:
            raise ValueError("Invalid assignment selected.")

        studylog.assignment = assignment
        studylog.duration_minutes = int(duration_raw)
        studylog.notes = notes
        studylog.save()

        return JsonResponse(studylog.jsonFriendly())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(["DELETE"])
def studylog_delete(request, pk):
    studylog = get_object_or_404(StudyLog, pk=pk, course__user=request.user)
    studylog.delete()
    return JsonResponse({'success': True})
