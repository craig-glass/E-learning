from django.db import models
from config import settings
from courses.models import Assignment, Course, Quiz


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
    quiz = models.ForeignKey(Quiz,
                             on_delete=models.CASCADE,
                             )
    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.quiz, 'submission'


class QuizAnswer(models.Model):
    quiz_submission = models.ForeignKey(QuizSubmission,
                                        on_delete=models.CASCADE,
                                        related_name='answers')
    answer = models.CharField(max_length=50)

    def __str__(self):
        return self.quiz_submission, 'answer'

