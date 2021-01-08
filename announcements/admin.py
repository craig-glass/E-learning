from django.contrib import admin
from .models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'content', 'date_created')
    search_fields = ['title', 'content']


admin.site.register(Announcement, AnnouncementAdmin)