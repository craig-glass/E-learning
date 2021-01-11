from django.urls import path
from . import views


urlpatterns = [
    path('register/',
         views.StudentRegistrationView.as_view(),
         name='student_registration'),
    path('enroll-course/',
         views.StudentEnrollCourseView.as_view(),
         name='student_enroll_course'),
    path('courses/',
         views.StudentCourseListView.as_view(),
         name='student_course_list'),
    path('courses/<pk>',
         views.StudentHomePageView.as_view(),
         name='student_home_page'),
    path('course/<pk>/',
         views.StudentCourseDetailView.as_view(),
         name='student_course_detail'),
    path('course/<pk>/<module_id>/',
         views.StudentCourseDetailView.as_view(),
         name='student_course_detail_module'),
    path('assignments/<pk>/',
         views.AssignmentListStudentView.as_view(),
         name='assignments_list_student_view'),
    path('assignments/<pk>/<module_id>/',
         views.AssignmentListStudentView.as_view(),
         name='assignments_list_student_view_module'),
    path('assignments/<pk>/<module_id>/<assignment_id>/',
         views.AssignmentDetailStudentView.as_view(),
         name='student_assignment_detail'),
]