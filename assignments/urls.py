from django.urls import path
from . import views


urlpatterns = [
    path('<int:assignment_id>/', views.AssignmentsListView.as_view(),
         name='assignments_list'),
    path('<pk>/assignment/', views.CourseAssignmentUpdateView.as_view(),
         name='course_assignment_update'),
]