<<<<<<< HEAD
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    path('queryAjax', views.QueryAjax.as_view()),
=======
from django.urls import path
from .views import HomePageView, CourseListView

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('home/courses/', CourseListView.as_view(),
         name='course_list'),
>>>>>>> b3c63666f88322942e4caaaf25779a8d92280fe5
]