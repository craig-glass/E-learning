import datetime

from django.test import TestCase
from accounts.models import Profile
from courses.models import Subject, Text, Course, Module, Assignment, Content, ModuleContent, ItemBase, Quiz, Question,\
    Choice, Grade


class SubjectTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.subject = Subject.objects.create(
            title='Computer Science',
            slug='slug'
        )

    def test_title_label(self):
        self.assertEqual(self.subject.title, 'Computer Science')

    def test_title_max_length(self):
        max_length = Subject._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_slug_label(self):
        self.assertEqual(self.subject.slug, 'slug')

    def test_slug_max_length(self):
        max_length = Subject._meta.get_field('slug').max_length
        self.assertEqual(max_length, 200)


class CourseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.course = Course.objects.create(
            owner=Profile.objects.create(
                userid='tiger'
            ),
            subject=Subject.objects.create(
                title='subject'
            ),
            title='course',
            slug='slug',
            overview='overview',
            created=datetime.date.today()
        )

    def test_owner_label(self):
        self.assertEqual(self.course.owner.userid, 'tiger')

    def test_subject_label(self):
        self.assertEqual(self.course.subject.title, 'subject')

    def test_course_title_label(self):
        self.assertEqual(self.course.title, 'course')

    def test_slug_label(self):
        self.assertEqual(self.course.slug, 'slug')

    def test_slug_max_length(self):
        max_length = Course._meta.get_field('slug').max_length
        self.assertEqual(max_length, 200)

    def test_overview_label(self):
        self.assertEqual(self.course.overview, 'overview')

    # def test_created(self):
    #     date = datetime.date.today()
    #     self.assertTrue(self.course.created == date)


class ModuleTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.module = Module.objects.create(
            course=Course.objects.create(
                owner=Profile.objects.create(
                    userid='tiger',
                ),
                subject=Subject.objects.create(
                    title='subject'
                ),
            ),
            title='title',
            description='description'
        )

    def test_title_label(self):
        self.assertEqual(self.module.title, 'title')

    def test_title_max_length(self):
        max_length = Module._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_description_label(self):
        self.assertEqual(self.module.description, 'description')


class AssignmentTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.assignment = Assignment.objects.create(
            module=Module.objects.create(
                course=Course.objects.create(
                    owner=Profile.objects.create(
                        userid='tiger',
                    ),
                    subject=Subject.objects.create(
                        title='subject'
                    ),
                ),
            ),

            title='title',
            description='description',
            due_date=datetime.date.today()
        )

    def test_title_label(self):
        self.assertEqual(self.assignment.title, 'title')

    def test_title_max_length(self):
        assign = Assignment.objects.get(id=1)
        max_length = assign._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_description_label(self):
        self.assertEqual(self.assignment.description, 'description')


# class ItemBaseTest(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         cls.item_base = ItemBase.objects.create(
#             owner=Profile.objects.create(
#                 userid='id',
#             ),
#             title='item',
#             created=datetime.date.today(),
#             updated=datetime.date.today()
#         )
#
#     def test_owner_label(self):
#         self.assertEqual(self.item_base.owner.userid, 'id')
#
#     def test_title_label(self):
#         self.assertEqual(self.item_base.title, 'item')
#
#     def test_title_max_length(self):
#         max_length = ItemBase._meta.get_field('title').max_length
#         print(max_length)
#         self.assertEqual(max_length, 250)
#
#     def test_created(self):
#         date = datetime.date.today()
#         self.assertTrue(self.item_base.created == date)
#
#     def test_updated(self):
#         date = datetime.date.today()
#         self.assertTrue(self.item_base.updated == date)
#

class TextFieldTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.text = Text.objects.create(
            content='text',
            owner=Profile.objects.create(
                userid='id',
            )
        )

    def test_text_field(self):
        self.assertEqual(self.text.content, 'text')


class QuizTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.quiz = Quiz.objects.create(
            title='quiz title',
            module=Module.objects.create(
                title='module title',
                course=Course.objects.create(
                    owner=Profile.objects.create(
                        userid='tiger',
                    ),
                    subject=Subject.objects.create(
                        title='subject title'
                    ),
                )
            ),
            description='description',
            date_created=datetime.date.today(),
        )

    def test_quiz_title(self):
        self.assertEqual(self.quiz.title, 'quiz title')

    def test_quiz_title_max_length(self):
        max_length = Quiz._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)

    def test_module_title(self):
        self.assertEqual(self.quiz.module.title, 'module title')

    def test_description(self):
        self.assertEqual(self.quiz.description, 'description')

    def test_created(self):
        date = datetime.date.today()
        self.assertTrue(self.quiz.date_created == date)


class QuestionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.question = Question.objects.create(
            quiz=Quiz.objects.create(
                title='question 1',
                module=Module.objects.create(
                    course=Course.objects.create(
                        owner=Profile.objects.create(
                            userid='1',
                        ),
                        subject=Subject.objects.create(
                            title='subject title'
                        ),
                    )
                )
            ),
            number=4,
            question_text='questions',
        )

    def test_quiz_title(self):
        self.assertEqual(self.question.quiz.title, 'question 1')

    def test_number_field(self):
        self.assertEqual(self.question.number, 4)

    def test_question_text(self):
        self.assertEqual(self.question.question_text, 'questions')


class ChoiceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.choice = Choice.objects.create(
            question=Question.objects.create(
                number='1',
                quiz=Quiz.objects.create(
                    module=Module.objects.create(
                        course=Course.objects.create(
                            owner=Profile.objects.create(
                                userid='1'
                            ),
                            subject=Subject.objects.create(
                                title='subject title'
                            ),
                        )
                    )
                )
            ),
            choice_text='choice',
            correct_answer=True,
        )

    def test_choice_number(self):
        self.assertEqual(self.choice.question.number, '1')

    def test_choice_text(self):
        self.assertEqual(self.choice.choice_text, 'choice')

    def test_choice_text_max_length(self):
        max_length = Choice._meta.get_field('choice_text').max_length
        self.assertEqual(max_length, 100)

    def test_correct_answer(self):
        self.assertTrue(self.choice.correct_answer)


class GradeTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.grade = Grade.objects.create(
            student=Profile.objects.create(
                userid='1',
                email='example@mail.com'
            ),
            teacher=Profile.objects.create(
                first_name='Tiger',
                email='teacher@mail.com'
            ),
            assignment=Assignment.objects.create(
                module=Module.objects.create(
                    title='assignment',
                    course=Course.objects.create(
                        owner=Profile.objects.create(
                            userid='2'
                        ),
                        subject=Subject.objects.create(
                            title='subject title'

                        )
                    )
                ),
                due_date=datetime.date.today()

            ),
            grade='2'
        )

    def test_student_userid(self):
        self.assertEqual(self.grade.student.userid, '1')

    def test_teacher_first_name(self):
        self.assertEqual(self.grade.teacher.first_name, 'Tiger')

    def test_assignment_title(self):
        self.assertEqual(self.grade.assignment.module.title, 'assignment')

    def test_grade(self):
        self.assertEqual(self.grade.grade, '2')

