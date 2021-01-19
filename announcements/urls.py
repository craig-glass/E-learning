from django.http import request

from . import views
from django.urls import path

app_name = 'announcements'

urlpatterns = [
    path('view/', views.AnnouncementList.as_view(), name='announcements'),
    path('add/', views.addAnnouncements, name='add_announcement'),
    path('getAnnouncementsAjax', views.GetAnnouncementsAjax.as_view()),
]