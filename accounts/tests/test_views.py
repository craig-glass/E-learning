from django.test import TestCase
from django.urls import reverse
from accounts import views


class RegistrationView(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    # Test for logged in account


class CreateAjaxView(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/accounts/createAccountAjax/')
        self.assertEquals(response.status_code, 200)