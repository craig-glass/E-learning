import calendar
from datetime import datetime, timedelta, date

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.views import generic
from .forms import EventForm, EventNewForm
from .models import *
from .utils import Calendar

#This class is used to display the calendar with the next and previous month buttons,
#and the current date so the calendar knows what page to start on.
class CalendarView(generic.ListView):
    model = Event
    #The template to render view to.
    template_name = 'calendar.html'

    #Function to get all data that is needed such as the current datetime, the calendar and next/previous buttons
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


#This function gets the current datetime
def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

#This function calculates the previous month that will be displayed when the button is pressed.
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

#This function calculates the next month that will be displayed when the button is pressed.
def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

#This function gets the id of an event when it is clicked and populates a form with the data
#about that form that the user can then see.
def event(request, event_id=None):
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
        #if a user is a staff member display the form that is not read only so they can edit calendar entries
        #and change the template so that they can save their changes
    if request.user.is_staff:
        form = EventNewForm(request.POST or None, instance=instance)
        template = "edit_event.html"
    #else display events as read only
    else:
        form = EventForm(request.POST or None, instance=instance)
        template = "event.html"
    form.fields['course'].queryset = Course.objects.filter(Q(owner=request.user) | Q(students__in=[request.user]))
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('event_calendar:calendar'))
    return render(request, template, {'form': form, 'event_id': event_id})


