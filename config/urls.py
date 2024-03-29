"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from home.views import *
from django.conf import settings
from django.conf.urls.static import static

handler400 = Error400View.as_view()
handler403 = Error403View.as_view()
handler404 = Error404View.as_view()
handler500 = error_500_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('announcements/', include('announcements.urls')),
    path('calendar/', include('event_calendar.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search/', SearchView.as_view(), name='search'),
    path('course/', include('courses.urls')),
    path('', include('home.urls')),
    path('students/', include('students.urls')),
    path('account/', include('accounts.urls')),
    path('', include('pwa.urls')),
    path('courseListAjax', CourseListAjax.as_view()),
    path('moduleListAjax', ModuleListAjax.as_view()),
    path('staffCourseListAjax', StaffCourseListAjax.as_view()),
    path('staffModuleListAjax', StaffModuleListAjax.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

