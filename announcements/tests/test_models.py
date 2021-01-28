import datetime

from django.test import TestCase

from accounts.models import Profile
from announcements.models import Announcement
from courses.models import Course, Subject


class AnnouncementTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.announcement = Announcement.objects.create(
            title='announcement',
            author=Profile.objects.create(
                    userid='author',
                    email='email@email.com'
                ),
            content='content',
            date_created=datetime.date.today(),
            course=Course.objects.create(
                owner=Profile.objects.create(
                    userid='tiger',
                ),
                subject=Subject.objects.create(
                    title='subject'
                ),
            )
        )

    def test_title_label(self):
        self.assertEqual(self.announcement.title, 'announcement')

    def test_title_max_length(self):
        announcements = Announcement.objects.get(id=1)
        max_length = announcements._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_author_userid(self):
        self.assertEqual(self.announcement.author.userid, 'author')

    def test_content_label(self):
        self.assertEqual(self.announcement.content, 'content')

    def test_date_created(self):
        date = datetime.date.today()
        print(date)
        print(self.announcement.date_created)
        self.assertTrue(self.announcement.date_created == date)

    def test_course_subject(self):
        self.assertEqual(self.announcement.course.subject.title, 'subject')

