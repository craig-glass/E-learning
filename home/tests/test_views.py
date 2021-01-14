from django.test import TestCase
from django.urls import reverse
from home import views


class HomePageViewTest(TestCase):

    def test_page_status_code(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('homepage'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('homepage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/homepage.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get('')
        self.assertContains(response, '<h1>Welcome!</h1>')


class SearchViewTest(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/search/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('search'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('search'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/search/search_page.html')
