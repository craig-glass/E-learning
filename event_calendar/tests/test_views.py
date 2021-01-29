from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.models import Profile
from event_calendar.views import CalendarView


class CalendarViewTest(TestCase):
    """
    URL tests while signed out - can be viewed by all users but cannot create an event
    """
    def test_calendar_status_code(self):
        response = self.client.get('/calendar/view/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name[0], 'calendar.html')


class LoggedInTest(TestCase):
    """
    URL tests as a superuser
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Profile.objects.create_superuser(
            userid='tester',
            email='test@mail.com',
            password='password'
        )

    def test_calendar_view_page_status_code(self):
        request = self.factory.get('/calendar/view/')
        request.user = self.user
        response = CalendarView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_event_new_page_status_code(self):
        url = self.factory.post(reverse('event_calendar:event_new'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

