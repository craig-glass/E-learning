from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.db.models import Q

from courses.models import Course, Module

User = get_user_model()


class HomePageView(TemplateView):
    template_name = 'home/homepage.html'


class SearchView(View):
    template_name = 'home/search/search_page.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        query = request.GET.get('query')
        context = {
            "query": query,
            "models": MODELS.keys(),
        }
        return render(request, self.template_name, context)


class QueryAjax(View):
    """Ajax to find records of a given model with fields matching the given query string"""

    def post(self, request: HttpRequest) -> JsonResponse:
        query = request.POST.get('query')
        model = MODELS[request.POST.get('model')]

        # Generate queries for each field
        search_queries = [Q(**{x + "__icontains": query}) for x in model['fields']]

        # Combine queries into single OR delimited query
        q_object = Q()
        for q in search_queries:
            q_object |= q
        # Filter by the generated query
        results = model['model'].objects.filter(q_object)

        # Parse results into format users will see
        parsed_results = []
        for record in results:
            parsed_results.append({
                "title": model['title'].format(record=record),
                "link": model['link'].format(record=record)
            })

        context = {"results": parsed_results}
        return JsonResponse(context)


"""
Structure defining which models can be queried in QueryAjax, and how the response is formatted
model - reference to the model class being queried
title - format string to be shown as a link
link - url path the link should lead to
fields - fields the query string should be compared with
"""
MODELS = {
    "User": {
        "model": User,
        "title": "{record.userid}: {record.first_name}",
        "link": "/account/profile/{record.userid}",
        "fields": ["userid", "first_name", "last_name"]
    },
    "Course": {
        "model": Course,
        "title": "{record.title} - {record.owner.userid}: {record.owner.first_name}",
        "link": "/course/{record.slug}",
        "fields": ["title", "slug"]
    },
    "Module": {
        "model": Module,
        "title": "{record.course.title} - {record.title}",
        "link": "/course/module/{record.id}",
        "fields": ["title"]
    }
}
