from django.db import models
from config import settings
from courses.models import Assignment, Course, Quiz, Question


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.PROTECT)

    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='assignment_submission',
                                on_delete=models.CASCADE,
                                null=True)
    course = models.ForeignKey(Course,
                               on_delete=models.PROTECT)
    date_of_submission = models.DateTimeField(auto_now_add=True)
    submitted_file = models.FileField(upload_to='submitted_assignments')


class QuizSubmission(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.PROTECT,
                                default=None)
    date_submitted = models.DateTimeField(auto_now=True)
    quiz = models.ForeignKey(Quiz,
                             on_delete=models.CASCADE,
                             related_name='submissions',
                             default=None)
    score = models.PositiveIntegerField(null=True,
                                        default=0)

    def __str__(self):
        return self.date_submitted


class QuizAnswer(models.Model):
    quiz_submission = models.ForeignKey(QuizSubmission,
                                        on_delete=models.CASCADE,
                                        related_name='answers',
                                        default=None)
    answer = models.CharField(max_length=50)
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 default=None)
    is_correct = models.BooleanField(default=None)

    def __str__(self):
        return self.answer

