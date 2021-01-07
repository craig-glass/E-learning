from . import views
from django.urls import path

urlpatterns = [
    path('announcements/', views.PostList.as_view(), name='announcements'),
]