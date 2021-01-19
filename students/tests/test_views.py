from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client


class RegistrationTest(TestCase):
    #
    #     def setUp(self):
    #         user = User.objects.create(username='tiger')
    #         user.set_password('password')
    #         user.save()
    #
    #         c = Client()
    #         login = c.login(username='tiger', password='password')
    #
    # def tearDown(self):
    #     self.user.delete()

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


class CourseListTest(TestCase):

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
        response = self.client.get('/students/courses/')  # Private key
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('student_home_page'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/home.html')


class CourseDetailTest(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/students/courses/')  # Private key
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('student_course_detail'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/course/detail.html')


class AssignmentListStudentTest(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/students/assignments/')  # Private key
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('assignments_list_student_view'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/assignments/list.html')


class AssignmentDetailStudentTest(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/students/assignments/1/2/3')  # Private key
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('student_assignment_detail'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/assignments/detail.html')