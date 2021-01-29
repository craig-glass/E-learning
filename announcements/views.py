from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django import forms
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from courses.models import Course
from .models import Announcement


class AnnouncementList(LoginRequiredMixin, View):
    template_name = 'announcements.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {"courses": []}
        if request.user.is_authenticated:
            context["courses"] = Course.objects.filter(
                Q(students__in=[request.user]) | Q(owner=request.user)
            ).distinct()
        return render(request, self.template_name, context)


class GetAnnouncementsAjax(LoginRequiredMixin, View):
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
    announcement_form = forms.modelform_factory(Announcement, fields=('title', 'course', 'author', 'content'))
    data = request.POST or None
    form = announcement_form(data=data)
    form.fields['course'].queryset = Course.objects.filter(owner=request.user)
    form.fields['author'].widget = forms.HiddenInput()
    form.fields['author'].initial = request.user
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('announcements:announcements')

    context = {'form': form}
    return render(request, 'add_announcement.html', context)
