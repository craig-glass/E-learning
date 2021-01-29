import datetime

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.test import Client

from accounts.models import Profile
from courses.models import Course, Subject, Module
from students.views import StudentRegistrationView, StudentCourseListView, StudentHomePageView, StudentCourseDetailView, \
    AssignmentListStudentView, QuizListStudentView, AssignmentDetailStudentView


class RegistrationTest(TestCase):

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    def test_log_out(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, '/')


class StudentCourseListTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Profile.objects.create_user(
            userid='test1',
            email='abc1@gmail.com',
            password='password'
        )

    def test_logged_in_uses_correct_template(self):
        request = self.factory.get('/students/courses/')
        request.user = self.user
        response = StudentCourseListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.template_name[0], 'students/course/list.html')

    def test_redirect_to_login_anonymous_user(self):
        request = self.factory.get('/students/courses/')
        request.user = AnonymousUser()
        response = StudentCourseListView.as_view()(request)
        self.assertEquals(response.status_code, 302)

    def test_url_anonymous_user(self):
        response = self.client.get('/students/courses/')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/students/courses/')

    def test_page_status_code(self):
        response = self.client.get('/students/register/')
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/students/register/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student/registration.html')


class LoggedInPageTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Profile.objects.create_user(
            userid='test1',
            email='abc1@gmail.com',
            password='password',
        )

    def test_courses_page_status_code(self):
        url = self.factory.post(reverse('students:student_home_page', kwargs={'pk': 1}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/error_pages/error_page.html')

    def test_home_page_success_status_code(self):
        url = self.factory.post(reverse('students:student_course_detail', kwargs={'pk': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_course_detail_page_status_code(self):
        url = self.factory.post(reverse('students:student_course_detail_module', kwargs={'pk': 1, 'module_id': 1}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_module_home_page_status_code(self):
        url = self.factory.post(reverse('students:module_home_page', kwargs={'pk': 1, 'module_id': 1}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_assignments_list_student_view_status_code(self):
        url = self.factory.post(reverse('students:assignments_list_student_view', kwargs={'pk': 1}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_assignments_list_student_view_module_status_code(self):
        url = self.factory.post(reverse('students:assignments_list_student_view_module', kwargs={'pk': 1,
                                                                                                 'module_id': 1, }))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # def test_student_assignment_detail_page_status_code(self):
    #     url = self.factory.post(reverse('students:student_assignment_detail', kwargs={'pk': 1, 'module_id':1,
    #                                                                                   'assessment_id': 2}))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)

    # def test_assignment_submission_page_status_code(self):
    #     url = self.factory.post(reverse('students:assignment_submission', kwargs={'module_id': 1,
    #                                                                               'assessment_id': 2}))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)

    # def test_assignment_submission_redo_status_code(self):
    #     url = self.factory.post(reverse('students:assignment_submission_redo', kwargs={'pk': 1, 'module_id': 1,
    #                                                                                    'assessment_id': 2}))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)

    # def test_assignment_submitted_view_status_code(self):
    #     url = self.factory.post(reverse('students:assignment_submitted_view', kwargs={'pk': 1, 'module_id':1,
    #                                                                                   'assessment_id': 2}))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)

    def test_quiz_list_student_view_status_code(self):
        url = self.factory.post(reverse('students:quiz_list_student_view', kwargs={'pk': 1}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_quiz_detail_student_view_status_code(self):
        url = self.factory.post(reverse('students:quiz_detail_student_view', kwargs={'pk': 1, 'module_id': 1,
                                                                                     'quiz_id': 1}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_quiz_detail_student_view_redo_status_code(self):
        url = self.factory.post(reverse('students:quiz_detail_student_view_redo', kwargs={'pk': 1, 'module_id': 1,
                                                                                          'quiz_id': 2}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_quiz_submitted_view_status_code(self):
        url = self.factory.post(reverse('students:quiz_submitted_view', kwargs={'pk': 1, 'module_id': 1,
                                                                                              'quiz_id': 2}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_module_content_view_status_code(self):
        url = self.factory.post(reverse('students:module_content_view', kwargs={'pk': 1, 'module_id': 1}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
