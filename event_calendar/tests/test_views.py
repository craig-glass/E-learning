from django.test import TestCase
from django.urls import reverse


class CalendarViewTest(TestCase):

    def test_calendar_status_code(self):
        response = self.client.get('/calendar/view/')
        self.assertEquals(response.status_code, 200)

    def test_calendar_uses_correct_template(self):
        response = self.client.get('/calendar/view/')
        self.assertTemplateUsed(response, 'calendar.html')

    def test_event_status_code(self):
        response = self.client.get('/calendar/event_new/')
        self.assertEquals(response.status_code, 200)

    def test_event_uses_correct_template(self):
        response = self.client.get('/calendar/event_new/')
        self.assertTemplateUsed(response, 'event_new.html')