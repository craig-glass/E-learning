from django.urls import path, re_path
from .views import HomePageView, SearchView

urlpatterns = [
    path('', HomePageView.as_view()),
]