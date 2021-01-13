import datetime
from django.db import models
from config import settings
from courses.models import Assignment, Course


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

