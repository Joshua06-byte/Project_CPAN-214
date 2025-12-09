from django.urls import path
from . import views

urlpatterns = [
    # Courses
    path('courses/', views.course_list, name='course-list'),
    path('courses/<int:pk>/', views.course_detail, name='course-detail'),
    path('courses/create/', views.course_create, name='course-create'),
    path('courses/<int:pk>/update/', views.course_update, name='course-update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course-delete'),

    # Assignments
    path('assignments/create/<int:course_pk>/', views.assignment_create, name='assignment-create'),
    path('assignments/<int:pk>/update/', views.assignment_update, name='assignment-update'),
    path('assignments/<int:pk>/delete/', views.assignment_delete, name='assignment-delete'),

    # StudyLogs
    path('studylogs/create/<int:course_pk>/', views.studylog_create, name='studylog-create'),
    path('studylogs/<int:pk>/update/', views.studylog_update, name='studylog-update'),
    path('studylogs/<int:pk>/delete/', views.studylog_delete, name='studylog-delete'),
]
