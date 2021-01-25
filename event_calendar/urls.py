from . import views
from django.urls import path

app_name = 'event_calendar'

urlpatterns = [
    path('view/', views.CalendarView.as_view(), name='calendar'),
    # path(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path('event_new/', views.event_new, name='event_new'),
]