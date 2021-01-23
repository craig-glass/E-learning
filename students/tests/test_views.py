from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

from accounts.models import Profile
from courses.models import Course
from students.views import StudentRegistrationView


class StudentRegistrationTest(TestCase):

    def setUp(self):
        user = StudentRegistrationView.objects.create_user(username='user', password='password')
        user.save()

        # c = Client()
        # logged_in = c.login(userid='user', password='password')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, '/accounts/login/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='user', password='password')
        response = self.client.get(reverse('student_course_detail'))

        self.assertEqual(str(response.context['user']), 'password')
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'students/student/registration.html')

    def test_page_status_code(self):
        response = self.client.get('/students/register/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('student_registration'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('student_registration'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student/registration.html')


class StudentCourseListTest(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/students/courses/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('student_course_list'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('student_course_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/course/list.html')


class HomePageTest(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/students/courses/1/')  # Private key
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('student_home_page'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/home.html')


class CourseDetailTest(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/students/course/1/1/')
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('student_course_detail'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/course/detail.html')


class AssignmentListStudentTest(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/students/assignments/1/')  # Private key
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('assignments_list_student_view'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/assignments/list.html')


class AssignmentDetailStudentTest(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/students/assignments/1/1/')  # Private key
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('student_assignment_detail'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/assignments/detail.html')