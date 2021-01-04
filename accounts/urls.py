from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.AccountDisplayView.as_view()),
    path('profile/<str:userid>/', views.AccountDisplayView.as_view()),
    path('edit/<str:userid>/', views.AccountSettingsView.as_view()),
    path('register/', views.CourseJoinView.as_view()),

    path('updateAccountAjax', views.AccountUpdateAjax.as_view()),
    path('courseJoinAjax', views.CourseJoinAjax.as_view()),
]
