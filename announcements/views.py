from django.shortcuts import render
from django.views import generic
from announcements.forms import AnnouncementForm
from .models import Announcement


class AnnouncementList(generic.ListView):
    queryset = Announcement.objects.order_by('-date_created')[:15]
    template_name = 'announcements.html'



def addAnnouncements(request):
        form = AnnouncementForm()
        if request.method == 'POST':
            form = AnnouncementForm(request.POST)

            if form.is_valid():
                form.save()

        context = {'form': form}
        return render(request, 'add_announcement.html', context)


