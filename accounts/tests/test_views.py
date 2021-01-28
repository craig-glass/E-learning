from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.models import Profile
from accounts.views import AccountDisplayView


class RegistrationTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Profile.objects.create_user(
            userid='test1',
            email='abc1@gmail.com',
            password='password'
        )

    def test_logged_in_profile_page(self):
        request = self.factory.get('/account/profile/1/')
        request.user = self.user
        response = AccountDisplayView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'accounts/account_view/account_view.html')

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

    def test_register_page_code(self):
        response = self.client.get('/account/register/')
        self.assertEquals(response.status_code, 200)


