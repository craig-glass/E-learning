from . import views
from django.urls import path

app_name = 'event_calendar'
#These are the urls for the pages that call view functions which will render the display to the respective pages.
urlpatterns = [
    path('view/', views.CalendarView.as_view(), name='calendar'),
    path(r'^event/(?P<event_id>\d+)/$', views.event, name='event'),
    path('event_new/', views.event, name='event_new'),
]