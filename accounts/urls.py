from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.AccountDisplayView.as_view(), name='account_profile'),
    path('profile/<str:userid>/', views.AccountDisplayView.as_view(), name='account_view'),
    path('edit/<str:userid>/', views.AccountSettingsView.as_view(), name='account_edit'),
    path('analytics/<str:userid>/', views.AccountAnalyticsView.as_view(), name='account_analytics'),
    path('register/', views.CourseJoinView.as_view(), name='course_register'),

    path('updateAccountAjax', views.AccountUpdateAjax.as_view()),
    path('courseJoinAjax', views.CourseJoinAjax.as_view()),
    path('registeredCourseAnalyticsAjax', views.RegisteredCourseAnalyticsAjax.as_view()),
    path('ownedCourseAnalyticsAjax', views.OwnedCourseAnalyticsAjax.as_view()),
]
