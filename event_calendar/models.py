from django.db import models
from django.urls import reverse

from courses.models import Course


class Event(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True)

    @property
    def get_html_url(self):
        url = reverse('event_calendar:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'