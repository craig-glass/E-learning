from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    path('queryAjax', views.QueryAjax.as_view()),
    path('home/', views.home),

]