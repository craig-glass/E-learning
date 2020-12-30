from django.shortcuts import render
from django.views.generic import TemplateView, ListView


# Create your views here.
from courses.models import Course


class HomePageView(TemplateView):
    template_name = 'home/homepage.html'


class CourseListView(ListView):
    model = Course
    template_name = 'home/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs
