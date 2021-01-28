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
        self.assertEqual(response.template_name[0], 'students/course/list.html')

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
            password='password'
        )

    def test_courses_page_status_code(self):
        request = self.factory.get('/students/courses/')
        request.user = self.user
        response = StudentCourseListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'students/course/list.html')

    def test_home_page_status_code(self, pk):
        request = self.factory.get('/students/courses/1/')
        request.user = self.user
        response = StudentHomePageView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'students/home.html')

    def test_course_detail_page_status_code(self):
        url = 'students/course/1/'
        request = self.factory.get(url)
        request.user = self.user
        response = StudentCourseDetailView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'students/course/detail.html')

    def test_assignment_page_status_code(self):
        request = self.factory.get('/students/assignments/1/')
        request.user = self.user
        response = AssignmentListStudentView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'students/assignments/list.html')

    def test_assignment_detail_page_status_code(self):
        request = self.factory.get('/students/assignments/1/1/')
        request.user = self.user
        response = AssignmentDetailStudentView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'students/assignments/detail.html')

    def test_quiz_page_status_code(self):
        request = self.factory.get('/students/course/1/quizzes/')
        request.user = self.user
        response = QuizListStudentView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'students/quizzes/list.html')
