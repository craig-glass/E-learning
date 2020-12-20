from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.AccountDisplayView.as_view()),
    path('profile/<str:userid>', views.AccountDisplayView.as_view()),
    path('create', views.AccountCreateView.as_view())
]
