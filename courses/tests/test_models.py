from django.test import TestCase
from courses.models import Subject, Text, Course


class SubjectCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Subject.objects.create(title='Computer Science', slug='slug')
        pass

    def test_title_label(self):
        subject = Subject.objects.get(id=1)
        field_label = subject._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        subject = Subject.objects.get(id=1)
        max_length = subject._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_slug_label(self):
        subject = Subject.objects.get(id=1)
        field_label = subject._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'slug')

    def test_slug_max_length(self):
        subject = Subject.objects.get(id=1)
        max_length = subject._meta.get_field('slug').max_length
        self.assertEqual(max_length, 200)


# class TestCourse(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         Course.objects.create(owner='owner_id', title='t')
#         pass
#
#     def test_title_label(self):
#         subject = Subject.objects.get(id=1)
#         field_label = subject._meta.get_field('title').verbose_name
#         self.assertEqual(field_label, 'title')


class TestTextField(TestCase):

    @classmethod
    def setUpTestData(cls):
        Text.objects.create(content='text', module='')
        pass

    def test_text_field(self):
        content = Text.objects.get(id=1)
        text_field = content._meta.get_field('content')
        self.assertEqual(text_field, 'content')
