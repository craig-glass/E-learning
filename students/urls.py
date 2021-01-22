from django.urls import path
from . import views

app_name = 'students'

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
    path('course/<pk>/module/<module_id>/',
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
    path('assignments/<pk>/<module_id>/<assignment_id>/submission/',
         views.AssignmentSubmissionView.as_view(),
         name='assignment_submission'),
    path('course/<pk>/quizzes/',
         views.QuizListStudentView.as_view(),
         name='quiz_list_student_view'),
    path('course/<pk>/module/<module_id>/quizzes/',
         views.QuizListStudentView.as_view(),
         name='quiz_list_student_view_module'),
    path('course/<pk>/module/<module_id>/quiz/<quiz_id>/',
         views.QuizSubmissionView.as_view(),
         name='quiz_detail_student_view'),
    path('course/<pk>/module/<module_id>/quiz/<quiz_id>/submitted/',
         views.QuizSubmittedView.as_view(),
         name='quiz_submitted_view'),
]