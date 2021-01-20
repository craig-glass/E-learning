import datetime
from django.test import TestCase
from accounts.models import Profile


class ProfileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Profile.objects.create(userid='t123', email='tiger@mail.com', first_name='tiger', last_name='k', phone_number='01-21-31', term_address='newcastle')
        pass

    def test_userid_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('userid').verbose_name
        self.assertEqual(field_label, 'userid')

    def test_userid_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('userid').max_length
        self.assertEqual(max_length, 50)

    def test_help_text(self):
        profile = Profile.objects.get(id=1)
        help_text = profile._meta.get_field('userid').help_text
        self.assertEqual(help_text, 'Unique identifier for the account')

    def test_email_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_email_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('email').max_length
        self.assertEqual(max_length, 254)

    def test_first_name_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_first_name_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 150)

    def test_last_name_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_last_name_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 150)

    def test_phone_number_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('phone_number').verbose_name
        self.assertEqual(field_label, 'phone number')

    def test_phone_number_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('phone_number').max_length
        self.assertEqual(max_length, 20)

    def test_term_address_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('term_address').verbose_name
        self.assertEqual(field_label, 'term address')

    def test_term_address_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('term_address').max_length
        self.assertEqual(max_length, 150)

    def test_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        self.assertFalse(Profile.date_joined == date)

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        self.assertFalse(Profile.date_joined == date)

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        self.assertTrue(Profile.date_joined == date)