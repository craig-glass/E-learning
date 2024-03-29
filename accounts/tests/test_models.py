import datetime
from django.test import TestCase
from courses.models import Course, Subject
from accounts.models import Profile, AccountSubmission

"""
Each class tests their relevant classes from models.py with the same class name
"""


class ProfileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.profile = Profile.objects.create(
            userid='t123',
            email='tiger@mail.com',
            first_name='tiger',
            last_name='k',
            phone_number='01-21-31',
            term_address='newcastle',
            date_joined=datetime.date.today()
        )

    def test_userid_label(self):
        self.assertEqual(self.profile.userid, 't123')

    def test_userid_max_length(self):
        max_length = Profile._meta.get_field('userid').max_length
        self.assertEqual(max_length, 50)

    def test_userid_help_text(self):
        help_text = Profile._meta.get_field('userid').help_text
        self.assertEqual(help_text, 'Unique identifier for the account')

    def test_email_label(self):
        self.assertEqual(self.profile.email, 'tiger@mail.com')

    def test_email_max_length(self):
        max_length = Profile._meta.get_field('email').max_length
        self.assertEqual(max_length, 254)

    def test_first_name_label(self):
        self.assertEqual(self.profile.first_name, 'tiger')

    def test_first_name_max_length(self):
        max_length = Profile._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 150)

    def test_last_name_label(self):
        self.assertEqual(self.profile.last_name, 'k')

    def test_last_name_max_length(self):
        max_length = Profile._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 150)

    def test_phone_number_label(self):
        self.assertEqual(self.profile.phone_number, '01-21-31')

    def test_phone_number_max_length(self):
        max_length = Profile._meta.get_field('phone_number').max_length
        self.assertEqual(max_length, 20)

    def test_term_address_label(self):
        self.assertEqual(self.profile.term_address, 'newcastle')

    def test_term_address_max_length(self):
        max_length = Profile._meta.get_field('term_address').max_length
        self.assertEqual(max_length, 150)


class AccountSubmissionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.submit = AccountSubmission.objects.create(
            email='tiger@mail.com',
            course=Course.objects.create(
                owner=Profile.objects.create(
                    userid='tiger',
                ),
                subject=Subject.objects.create(
                    title='subject'
                )
            ),
            valid=True,
            date_submitted=datetime.date.today()
        )

    def test_email_label(self):
        self.assertEqual(self.submit.email, 'tiger@mail.com')

    def test_email_max_length(self):
        submit = AccountSubmission.objects.get(id=1)
        max_length = submit._meta.get_field('email').max_length
        self.assertEqual(max_length, 254)

    def test_valid_label(self):
        self.assertTrue(self.submit.valid, True)

