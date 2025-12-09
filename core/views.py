from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Course, Assignment, StudyLog
from datetime import datetime

# ----------------------------
# Courses CRUD
# ----------------------------

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
def course_create(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST request required.")

    try:
        name = request.POST.get('name')
        code = request.POST.get('code')
        description = request.POST.get('description')
        instructor = request.POST.get('instructor')

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
def course_update(request, pk):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST request required.")

    course = get_object_or_404(Course, pk=pk, user=request.user)
    try:
        name = request.POST.get('name')
        code = request.POST.get('code')
        description = request.POST.get('description')
        instructor = request.POST.get('instructor')

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
def course_delete(request, pk):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST request required.")

    course = get_object_or_404(Course, pk=pk, user=request.user)
    course.delete()
    return JsonResponse({'success': True})

# ----------------------------
# Assignments CRUD
# ----------------------------

@login_required
def assignment_create(request, course_pk):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST request required.")

    course = get_object_or_404(Course, pk=course_pk, user=request.user)
    try:
        title = request.POST.get('title')
        due_date_raw = request.POST.get('due_date')
        description = request.POST.get('description')
        is_completed = bool(request.POST.get('is_completed'))

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
def assignment_update(request, pk):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST request required.")

    assignment = get_object_or_404(Assignment, pk=pk, course__user=request.user)
    try:
        title = request.POST.get('title')
        due_date_raw = request.POST.get('due_date')
        description = request.POST.get('description')
        is_completed = bool(request.POST.get('is_completed'))

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
def assignment_delete(request, pk):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST request required.")

    assignment = get_object_or_404(Assignment, pk=pk, course__user=request.user)
    assignment.delete()
    return JsonResponse({'success': True})

# ----------------------------
# StudyLogs CRUD
# ----------------------------

@login_required
def studylog_create(request, course_pk):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST request required.")

    course = get_object_or_404(Course, pk=course_pk, user=request.user)
    try:
        assignment_id = request.POST.get('assignment')
        duration_raw = request.POST.get('duration_minutes')
        notes = request.POST.get('notes')

        if not duration_raw or not duration_raw.isdigit() or int(duration_raw) <= 0:
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
def studylog_update(request, pk):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST request required.")

    studylog = get_object_or_404(StudyLog, pk=pk, course__user=request.user)
    try:
        assignment_id = request.POST.get('assignment')
        duration_raw = request.POST.get('duration_minutes')
        notes = request.POST.get('notes')

        if not duration_raw or not duration_raw.isdigit() or int(duration_raw) <= 0:
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
def studylog_delete(request, pk):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST request required.")

    studylog = get_object_or_404(StudyLog, pk=pk, course__user=request.user)
    studylog.delete()
    return JsonResponse({'success': True})
