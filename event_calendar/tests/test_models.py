from django.test import TestCase

from accounts.models import Profile
from courses.models import Course, Subject
from event_calendar.models import Event
import datetime


class EventTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.event = Event.objects.create(
            title='event',
            description='description',
            start_time=datetime.date.today(),
            end_time=datetime.date.today(),
            course=Course.objects.create(
                title='course title',
                owner=Profile.objects.create(
                    userid='1'
                ),
                subject=Subject.objects.create(
                    title='subject title'
                )

            )
        )

    def test_title_label(self):
        self.assertEqual(self.event.title, 'event')

    def test_title_max_length(self):
        event = Event.objects.get(id=1)
        max_length = event._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_description_label(self):
        self.assertEqual(self.event.description, 'description')

    def test_start_time(self):
        s_date = datetime.date.today()
        self.assertTrue(self.event.start_time == s_date)

    def test_end_time(self):
        e_date = datetime.date.today()
        self.assertTrue(self.event.end_time == e_date)

    def test_course_title(self):
        self.assertEqual(self.event.course.title, 'course title')
