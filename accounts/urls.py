from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.AccountDisplayView.as_view()),
    path('profile/<str:username>', views.AccountDisplayView.as_view()),
]
