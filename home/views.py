from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View

import itertools


User = get_user_model()


class HomePageView(TemplateView):
    template_name = 'home/homepage.html'


class SearchView(View):
    template_name = 'home/search/search_page.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        print(request.GET['query'])
        context = {}
        return render(request, self.template_name, context)
