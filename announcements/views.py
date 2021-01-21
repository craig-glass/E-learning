from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q

from announcements.forms import AnnouncementForm
from courses.models import Course
from .models import Announcement


class AnnouncementList(View):
    template_name = 'announcements.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {"courses": []}
        if request.user.is_authenticated:
            context["courses"] = Course.objects.filter(
                Q(students__in=[request.user]) | Q(owner=request.user)
            ).distinct()
        print(context)
        return render(request, self.template_name, context)


class GetAnnouncementsAjax(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        if not request.user.is_authenticated:
            response = JsonResponse({})
            response.status_code = 401
            return response
        course = request.POST.get('course')
        announcements = Announcement.objects.filter(course=course)
        context = {"announcements": []}
        for announcement in announcements:
            author = announcement.author.userid
            print(announcement.author.first_name, announcement.author.last_name, announcement.author.userid)
            if announcement.author.last_name:
                author += ":" + announcement.author.last_name[0]
                if announcement.author.first_name:
                    author += "." + announcement.author.first_name
            elif announcement.author.first_name:
                author += ":" + announcement.author.first_name
            context["announcements"].append({
                "title": announcement.title,
                "author": author,
                "content": announcement.content,
                "created": announcement.date_created
            })
        return JsonResponse(context)


def addAnnouncements(request):
    form = AnnouncementForm()
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)

        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'add_announcement.html', context)
