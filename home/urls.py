from django.urls import path
from .views import HomePageView, CourseListView

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('home/courses/', CourseListView.as_view(),
         name='course_list'),
]