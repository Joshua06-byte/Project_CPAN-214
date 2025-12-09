from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Course, Assignment, StudyLog
from datetime import datetime



# COURSES CRUD


@login_required
def course_list(request):
    courses = Course.objects.filter(user=request.user)
    return render(request, 'courses/course_list.html', {'courses': courses})


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk, user=request.user)
    return render(request, 'courses/course_detail.html', {'course': course})


@login_required
def course_create(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            code = request.POST.get('code')
            description = request.POST.get('description')
            instructor = request.POST.get('instructor')

            # --- VALIDATION ---
            if not name:
                raise ValueError("Course name is required.")

            if any(c.isdigit() for c in name):
                raise ValueError("Course name cannot contain numbers.")

            if not code:
                raise ValueError("Course code is required.")

            if Course.objects.filter(user=request.user, code=code).exists():
                raise ValueError("You already created a course with this code.")

            # --- CREATE ---
            Course.objects.create(
                user=request.user,
                name=name,
                code=code,
                description=description,
                instructor=instructor
            )

            return redirect('course-list')

        except Exception as e:
            return render(request, 'courses/course_form.html', {"error": str(e)})

    return render(request, 'courses/course_form.html')


@login_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk, user=request.user)

    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            code = request.POST.get('code')
            description = request.POST.get('description')
            instructor = request.POST.get('instructor')

            if not name:
                raise ValueError("Course name is required.")
            if any(c.isdigit() for c in name):
                raise ValueError("Course name cannot contain numbers.")

            if not code:
                raise ValueError("Course code is required.")

            # Check the updated code does not collide with another
            if Course.objects.filter(user=request.user, code=code).exclude(id=course.id).exists():
                raise ValueError("Another course with this code already exists.")

            course.name = name
            course.code = code
            course.description = description
            course.instructor = instructor
            course.save()

            return redirect('course-list')

        except Exception as e:
            return render(request, 'courses/course_form.html', {
                'course': course,
                'error': str(e)
            })

    return render(request, 'courses/course_form.html', {'course': course})


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, user=request.user)

    if request.method == 'POST':
        course.delete()
        return redirect('course-list')

    return render(request, 'courses/course_confirm_delete.html', {'course': course})




# ASSIGNMENTS CRUD


@login_required
def assignment_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk, user=request.user)

    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            due_date_raw = request.POST.get('due_date')
            description = request.POST.get('description')
            is_completed = bool(request.POST.get('is_completed'))

            if not title:
                raise ValueError("Assignment title is required.")

            if not due_date_raw:
                raise ValueError("Due date is required.")

            # Validate date
            try:
                due_date = datetime.strptime(due_date_raw, "%Y-%m-%d").date()
            except:
                raise ValueError("Due date must be in YYYY-MM-DD format.")

            Assignment.objects.create(
                course=course,
                title=title,
                due_date=due_date,
                description=description,
                is_completed=is_completed
            )

            return redirect('course-detail', pk=course.pk)

        except Exception as e:
            return render(request, 'assignments/assignment_form.html', {
                'course': course,
                'error': str(e)
            })

    return render(request, 'assignments/assignment_form.html', {'course': course})


@login_required
def assignment_update(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, course__user=request.user)
    course = assignment.course

    if request.method == 'POST':
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

            return redirect('course-detail', pk=course.pk)

        except Exception as e:
            return render(request, 'assignments/assignment_form.html', {
                'assignment': assignment,
                'course': course,
                'error': str(e)
            })

    return render(request, 'assignments/assignment_form.html', {'assignment': assignment, 'course': course})


@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, course__user=request.user)
    course = assignment.course

    if request.method == 'POST':
        assignment.delete()
        return redirect('course-detail', pk=course.pk)

    return render(request, 'assignments/assignment_confirm_delete.html', {'assignment': assignment, 'course': course})




# STUDY LOG CRUD


@login_required
def studylog_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk, user=request.user)

    if request.method == 'POST':
        try:
            assignment_id = request.POST.get('assignment')
            duration_raw = request.POST.get('duration_minutes')
            notes = request.POST.get('notes')

            if not duration_raw:
                raise ValueError("Duration is required.")

            if not duration_raw.isdigit():
                raise ValueError("Duration must be a positive number.")

            duration = int(duration_raw)
            if duration <= 0:
                raise ValueError("Duration must be greater than 0.")

            assignment = None
            if assignment_id:
                assignment = Assignment.objects.filter(
                    pk=assignment_id,
                    course=course
                ).first()
                if not assignment:
                    raise ValueError("Invalid assignment selected.")

            StudyLog.objects.create(
                course=course,
                assignment=assignment,
                duration_minutes=duration,
                notes=notes
            )

            return redirect('course-detail', pk=course.pk)

        except Exception as e:
            return render(request, 'study_logs/studylog_form.html', {
                'course': course,
                'error': str(e)
            })

    return render(request, 'study_logs/studylog_form.html', {'course': course})


@login_required
def studylog_update(request, pk):
    studylog = get_object_or_404(StudyLog, pk=pk, course__user=request.user)
    course = studylog.course

    if request.method == 'POST':
        try:
            assignment_id = request.POST.get('assignment')
            duration_raw = request.POST.get('duration_minutes')
            notes = request.POST.get('notes')

            if not duration_raw:
                raise ValueError("Duration is required.")

            if not duration_raw.isdigit():
                raise ValueError("Duration must be a positive number.")

            duration = int(duration_raw)
            if duration <= 0:
                raise ValueError("Duration must be greater than 0.")

            assignment = None
            if assignment_id:
                assignment = Assignment.objects.filter(
                    pk=assignment_id,
                    course=course
                ).first()
                if not assignment:
                    raise ValueError("Invalid assignment selected.")

            studylog.assignment = assignment
            studylog.duration_minutes = duration
            studylog.notes = notes
            studylog.save()

            return redirect('course-detail', pk=course.pk)

        except Exception as e:
            return render(request, 'study_logs/studylog_form.html', {
                'studylog': studylog,
                'course': course,
                'error': str(e)
            })

    return render(request, 'study_logs/studylog_form.html', {'studylog': studylog, 'course': course})


@login_required
def studylog_delete(request, pk):
    studylog = get_object_or_404(StudyLog, pk=pk, course__user=request.user)
    course = studylog.course

    if request.method == 'POST':
        studylog.delete()
        return redirect('course-detail', pk=course.pk)

    return render(request, 'study_logs/studylog_confirm_delete.html', {'studylog': studylog, 'course': course})
