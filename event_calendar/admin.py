from django.contrib import admin
from event_calendar.models import Event

#This class sets what attributes should be displayed on /admin page
#and what fields can be used to search.
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_time', 'end_time')
    search_fields = ['title', 'content']

#Adds Event model to the admin page.
admin.site.register(Event, EventAdmin)