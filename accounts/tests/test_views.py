from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.models import Profile
from accounts.views import AccountDisplayView


class RegistrationTest(TestCase):
    """
    URL tests as a normal user and its responses according to different pages
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Profile.objects.create_user(
            userid='test1',
            email='abc1@gmail.com',
            password='password'
        )

    def test_authenticated_profile_page(self):
        url = self.factory.post('/account/profile/', kwargs={'userid': 'test1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_response_with_anonymous_user(self):
        request = self.factory.get('/account/profile/')
        request.user = AnonymousUser()
        response = AccountDisplayView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_login_status_code(self):
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)

    def test_login_uses_correct_template(self):
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_register_status_code(self):
        response = self.client.get('/account/register/')
        self.assertEquals(response.status_code, 200)

    def test_account_view_status_code(self):
        url = self.factory.post(reverse('accounts:account_view', kwargs={'userid': 'test1'}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_edit_page_status_code(self):
        url = self.factory.post(reverse('accounts:account_edit', kwargs={'userid': 'test1'}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_analytics_page_status_code(self):
        url = self.factory.post(reverse('accounts:account_analytics', kwargs={'userid': 'test1'}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_course_register_autocourse_page_status_code(self):
        url = self.factory.post(reverse('accounts:course_register_autocourse', kwargs={'course_id': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
