from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.models import Profile
from announcements.views import AnnouncementList


class AnnouncementListTest(TestCase):
    """
    URL tests as an anonymous user
    """
    def test_page_status_code(self):
        response = self.client.get('/announcements/view/')
        self.assertEquals(response.status_code, 302)


class LoggedInTest(TestCase):
    """
    URL tests as a superuser and its responses according to different pages
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Profile.objects.create_superuser(
            userid='test1',
            email='abc1@gmail.com',
            password='password'
        )

    def test_create_page_status_code(self):
        request = self.factory.get('/announcements/view/')
        request.user = self.user
        response = AnnouncementList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_module_list_page_status_code(self):
        url = self.factory.post(reverse('announcements:add_announcement'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

