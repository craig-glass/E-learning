from django.test import TestCase
from django.urls import reverse
from courses import views


class ViewsTest(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/course/mine/')
        self.assertEquals(response.status_code, 302)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('manage_course_list'))
        self.assertEquals(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('manage_course_list'))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(response, 'courses/manage/course/list.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get('/course/mine/')
        self.assertContains(response, '<h1>Courses</h1>')


class OwnerCourseTest(TestCase):

    def test_page_status(self):
        response = self.client.get('/course/create/')
        self.assertEquals(response.status_code, 302)


class ContentCreateTest(TestCase):

    def test_page_status(self):
        response = self.client.get('/course/create/')
        self.assertEquals(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('module_content_create'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/manage/course/form.html')