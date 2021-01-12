from django.test import TestCase
from django.urls import reverse
from students import views


class RegistrationView(TestCase):

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


class CourseListView(TestCase):

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


class HomePageView(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/students/courses/')  # Private key
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('student_home_page'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/home.html')


class CourseDetailView(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/students/courses/')  # Private key
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('student_course_detail'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/course/detail.html')