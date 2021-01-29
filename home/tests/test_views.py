from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.models import Profile
from home.views import HomePageView


class HomePageViewTest(TestCase):
    """
    URL tests while signed out - all users have permission to enter these pages
    """
    def test_home_page_status_code(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)

    def test_page_url_by_name(self):
        response = self.client.get(reverse('homepage'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('homepage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/homepage.html')


class SearchViewTest(TestCase):

    def test_search_page_status_code(self):
        response = self.client.get('/search/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('search'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('search'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/search/search_page.html')


class LoggedInTest(TestCase):
    """
    URL tests as a superuser
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Profile.objects.create_superuser(
            userid='tiger',
            email='tiger@mail.com',
            password='password'
        )

    def test_home_page_status_code(self):
        request = self.factory.get('')
        request.user = self.user
        response = HomePageView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'home/homepage.html')

