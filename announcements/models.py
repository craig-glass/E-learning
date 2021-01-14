from django.db import models
from django.contrib.auth.models import User

from django.conf import settings

from courses.models import Course


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='announcements')

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title