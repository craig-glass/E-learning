from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.models import Profile
from courses import views
from courses.views import ManageCourseListView

p = ManageCourseListView.permission_required


class ViewsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Profile.objects.create_user(
            userid='test1',
            email='abc1@gmail.com',
            password='password'
        )

    def test_courses_page_status_code(self):
        request = self.factory.get('/course/mine/')
        request.user = self.user
        response = ManageCourseListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'courses/manage/course/list.html')

    def test_response_with_anonymous_user(self):
        request = self.factory.get('/course/mine/', pk=1)
        request.user = AnonymousUser()
        response = ManageCourseListView.as_view()(request)
        self.assertEqual(response.status_code, 302)


class CourseCreateTest(TestCase):

    def test_page_status(self):
        response = self.client.get('/course/create/')
        self.assertEquals(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get('/course/create/')
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(response, 'courses/manage/course/form.html')