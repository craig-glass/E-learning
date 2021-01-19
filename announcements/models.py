from django.db import models
from django.contrib.auth.models import User

from django.conf import settings


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title