import datetime

from django.test import TestCase

from accounts.models import Profile
from courses.models import Course, Assignment, Module, Subject, Quiz, Question
from students.models import AssignmentSubmission, QuizSubmission, QuizAnswer

"""
Each class tests their relevant classes from models.py with the same class name
"""


class AssignmentSubmissionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.submission = AssignmentSubmission.objects.create(
            assignment=Assignment.objects.create(
                module=Module.objects.create(
                    title='module_title',
                    course=Course.objects.create(
                        title='course_title',
                        slug='slug',
                        subject=Subject.objects.create(
                            title='subject',
                            slug='subject'
                        ),
                        owner=Profile.objects.create(
                            userid='tiger',
                            email='tiger@mail.com'
                        )
                    )
                )
            ),
            student=Profile.objects.create(
                userid='student',
                first_name='name'

            ),
            course=Course.objects.create(
                title='computing',
                slug='computing',
                subject=Subject.objects.create(
                    title='subject2'
                ),
                owner=Profile.objects.create(
                    userid='tiger2',
                    email='example@email.com'
                )

            ),
            date_submitted=datetime
        )

    def test_assignment_module(self):
        self.assertEqual(self.submission.assignment.module.title, 'module_title')

    def test_course_title(self):
        self.assertEqual(self.submission.course.title, 'computing')

    def test_submission_owner(self):
        self.assertEqual(self.submission.student.userid, 'student')

    def test_assignment_subject(self):
        self.assertEqual(self.submission.assignment.module.course.subject.title, 'subject')

    def test_student_first_name(self):
        self.assertEqual(self.submission.student.first_name, 'name')

    def test_course_owner(self):
        self.assertEqual(self.submission.course.owner.userid, 'tiger2')


class QuizSubmissionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.quiz = QuizSubmission.objects.create(
            student=Profile.objects.create(
                userid='student',
                first_name='name'
            ),
            date_submitted=datetime.date.today(),
            quiz=Quiz.objects.create(
                title='quiz title',
                module=Module.objects.create(
                    course=Course.objects.create(
                        owner=Profile.objects.create(
                            userid='owner',
                            email='owner@email.com'
                        ),
                        subject=Subject.objects.create(
                            title='subject',
                        )
                    )
                )
            ),
            score=10
        )

    def test_student_userid(self):
        self.assertEqual(self.quiz.student.userid, 'student')

    def test_quiz_title(self):
        self.assertEqual(self.quiz.quiz.title, 'quiz title')

    def test_score(self):
        self.assertEqual(self.quiz.score, 10)


class QuizAnswerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.answer = QuizAnswer.objects.create(
            quiz_submission=QuizSubmission.objects.create(
                student=Profile.objects.create(
                    userid='user',
                    first_name='first'
                ),
                quiz=Quiz.objects.create(
                    module=Module.objects.create(
                        course=Course.objects.create(
                            slug='course slug',
                            owner=Profile.objects.create(
                                userid='user2',
                                email='user2@email.com'
                            ),
                            subject=Subject.objects.create(
                                title='subject',
                                slug='subject'
                            )
                        )
                    )
                )
            ),
            answer='answer',
            question=Question.objects.create(
                number=1,
                quiz=Quiz.objects.create(
                    title='quiz',
                    module=Module.objects.create(
                        course=Course.objects.create(
                            owner=Profile.objects.create(
                                userid='user3',
                                email='user3@email.com'
                            ),
                            subject=Subject.objects.create(
                                title='subject2',
                                slug='slug'
                            )
                        )
                    )
                )
            ),
            is_correct=True
        )

    def test_submitted_student_first_name(self):
        self.assertEqual(self.answer.quiz_submission.student.first_name, 'first')

    def test_answer(self):
        self.assertEqual(self.answer.answer, 'answer')

    def test_answer_max_length(self):
        max_length = QuizAnswer._meta.get_field('answer').max_length
        self.assertEqual(max_length, 50)

    def test_question_title(self):
        self.assertEqual(self.answer.question.quiz.title, 'quiz')

    def test_is_correct(self):
        self.assertTrue(self.answer.is_correct, True)
