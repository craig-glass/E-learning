from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from accounts import views


class RegistrationTest(TestCase):

    def setUp(self):
        self.user = views.User.objects.create_user(
            userid='tiger',
            password='password',
            email='tiger@mail.com'
        )
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_login_status_code(self):
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_logout_status_code(self):
        response = self.client.get('/accounts/logout/')
        self.assertEquals(response.status_code, 200)

    def test_logout_uses_correct_template(self):
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/logout.html')

    # Test for logged in account
    def test_page_status_code(self):
        response = self.client.get('/account/courseJoinAjax/')
        self.assertEquals(response.status_code, 200)

    def test_page_code(self):
        response = self.client.get('/account/register/')
        self.assertEquals(response.status_code, 200)


class CreateAjaxTest(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/account/courseJoinAjax/')
        self.assertEquals(response.status_code, 302)


class AccountsSettingsTest(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/account/register/')
        self.assertEquals(response.status_code, 200)