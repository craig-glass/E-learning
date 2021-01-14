from django.shortcuts import render
from django.views import generic
from django.views.generic import DetailView, ListView

from announcements.forms import AnnouncementForm
from courses.models import Course
from .models import Announcement


class AnnouncementList(DetailView):
    model = Course
    template_name = 'announcements.html'


def addAnnouncements(request):
        form = AnnouncementForm()
        if request.method == 'POST':
            form = AnnouncementForm(request.POST)

            if form.is_valid():
                form.save()

        context = {'form': form}
        return render(request, 'add_announcement.html', context)


