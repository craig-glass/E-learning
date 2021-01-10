from django.contrib import admin
from event_calendar.models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_time', 'end_time', 'course')
    search_fields = ['title', 'content']


admin.site.register(Event, EventAdmin)