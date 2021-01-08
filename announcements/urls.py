from django.http import request

from . import views
from django.urls import path

urlpatterns = [
    path('announcements/', views.AnnouncementList.as_view(), name='announcements'),
    path('add_announcement/', views.addAnnouncements, name='add_announcement'),
]