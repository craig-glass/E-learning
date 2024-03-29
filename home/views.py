from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import Resolver404
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.db.models import Q
from courses.models import Course, Module

import json

User = get_user_model()

#
# def home(request):
#     template = 'home/homepage.html'
#     return render(request, template)


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


class Error400View(View):
    template_name = 'home/error_pages/error_page.html'

    def get(self, request: HttpRequest, exception) -> HttpResponse:
        context = {
            "error_code": 400,
            "error_message": str(exception),
        }
        return render(request, self.template_name, context)


class Error403View(View):
    template_name = 'home/error_pages/error_page.html'

    def get(self, request: HttpRequest, exception) -> HttpResponse:
        context = {
            "error_code": 403,
            "error_message": str(exception),
        }
        return render(request, self.template_name, context)


class Error404View(View):
    template_name = 'home/error_pages/error_page.html'

    def get(self, request: HttpRequest, exception) -> HttpResponse:
        context = {
            "error_code": 404,
            "error_message": str(exception),
        }
        return render(request, self.template_name, context)


def error_500_view(request):
    context = {
        "error_code": 500,
        "error_message": "Server Error",
    }
    return render(request, 'home/error_pages/error_page.html', context)


class CourseListAjax(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        context = {"nav_links": []}
        if request.user.is_authenticated and request.user.is_student:
            for course in Course.objects.filter(students__in=[request.user]).order_by('id'):
                context["nav_links"].append({
                    "text": course.title,
                    "context": json.dumps({"course_id": course.id}),
                    "function": "_loadModuleNavigator",
                    "ajax": "/moduleListAjax",
                    "icon": "fas fa-book-open",
                    "type": "list",
                })
        else:
            response = JsonResponse({})
            response.status_code = 401
            return response
        return JsonResponse(context)


class ModuleListAjax(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        context = {"nav_links": []}
        if request.user.is_authenticated and request.user.is_student:
            for module in Module.objects.filter(course=get_object_or_404(Course, id=request.POST.get('course_id'))).order_by('order'):
                context["nav_links"].append({
                    "text": module.title,
                    "context": json.dumps({
                        "course_id": request.POST.get('course_id'),
                        "module_id": module.id,
                    }),
                    "function": "_loadModuleContentsNavigator",
                    "type": "list",
                })
        else:
            response = JsonResponse({})
            response.status_code = 401
            return response
        return JsonResponse(context)


class StaffCourseListAjax(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        context = {"nav_links": []}
        if request.user.is_authenticated and request.user.is_staff:
            for course in Course.objects.filter(owner=request.user).order_by('id'):
                context["nav_links"].append({
                    "text": course.title,
                    "context": json.dumps({"course_id": course.id}),
                    "function": "_loadStaffModuleNavigator",
                    "ajax": "/staffModuleListAjax",
                    "icon": "fas fa-book-open",
                    "type": "list",
                })
        else:
            response = JsonResponse({})
            response.status_code = 401
            return response
        return JsonResponse(context)


class StaffModuleListAjax(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        context = {"nav_links": []}
        if request.user.is_authenticated and request.user.is_staff:
            for module in Module.objects.filter(
                    course=get_object_or_404(Course, id=request.POST.get('course_id'))).order_by('order'):
                context["nav_links"].append({
                    "text": module.title,
                    "context": json.dumps({
                        "course_id": request.POST.get('course_id'),
                        "module_id": module.id,
                    }),
                    "function": "_loadStaffModuleContentsNavigator",
                    "type": "list",
                })
        else:
            response = JsonResponse({})
            response.status_code = 401
            return response
        return JsonResponse(context)


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
