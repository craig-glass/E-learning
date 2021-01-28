from django.db import models
from django.urls import reverse

from courses.models import Course

#This class creates Event model within database with the following attributes.
#As PostgreSQL is being used, primary key does not need to be defined.
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    #Foreign key from courses model.
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True)

    #Property that adds hyperlink to each event displayed on calendar so they can be
    #clicked to view details about them that are displayed using forms.py
    @property
    def get_html_url(self):
        url = reverse('event_calendar:event', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'