import datetime
from statistics import mean
from typing import Dict, Sequence, Union

from django import forms
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from courses.models import Course, Module, Subject, Assignment, Grade
from .forms import UserUpdateForm, CourseRegisterForm

User = get_user_model()


class AccountDisplayView(View):
    """
    View for displaying details of account specified in url
    Will show different results based on users permission level
    """
    template_name = 'accounts/account_view/account_view.html'

    def get(self, request: HttpRequest, userid: str = None) -> HttpResponse:
        current_user = request.user
        if userid is None:  # No userid specified in url
            if current_user.is_authenticated:
                # Redirect to current user's account page
                return redirect('/account/profile/' + current_user.userid)
            else:
                # Redirect to login page to authenticate
                return redirect('/accounts/login')
        else:
            account = get_object_or_404(User, userid=userid)
            if not (current_user.is_authenticated or account.is_staff):
                # Unauthenticated users can only view staff accounts, otherwise redirect home
                return redirect('/')
        user_details = get_user_details(account, current_user)
        context = {
            "user_details": user_details,
            "is_user": current_user == account,
            "show_analytics": current_user == account or current_user.has_perm('accounts.view_profile'),
        }
        return render(request, self.template_name, context)


class AccountSettingsView(View):
    """
    View for displaying editable user details and other preferences
    """
    template_name = 'accounts/account_view/account_settings.html'

    def get(self, request: HttpRequest, userid: str) -> HttpResponse:
        current_user = request.user
        account = get_object_or_404(User, userid=userid)
        if not current_user.is_authenticated:
            return redirect('login')
        elif current_user == account:
            user_details = get_user_details(account, current_user)
            context = {
                "user_details": user_details,
                "is_user": True,
                "show_analytics": True,
            }
            return render(request, self.template_name, context)
        else:
            return redirect('/')


class AccountAnalyticsView(View):
    """
    View for displaying general account analytics of a given user
    """
    template_name = 'accounts/account_view/account_analytics.html'

    def get(self, request: HttpRequest, userid: str) -> HttpResponse:
        current_user = request.user
        account = get_object_or_404(User, userid=userid)
        if not current_user.is_authenticated:
            return redirect('login')
        elif current_user == account or current_user.has_perm('accounts.view_account'):
            user_details = get_user_details(account, current_user)
            context = {
                "user_details": user_details,
                "is_user": current_user == account,
                "show_analytics": True,

                "registered_courses": Course.objects.filter(students__in=[account]).order_by('title'),
                "owned_courses": Course.objects.filter(owner=account).order_by('title'),
            }
            return render(request, self.template_name, context)
        else:
            return redirect('/')


class CourseJoinView(View):
    """
    View for students to submit a request to join a course / create a new account
    """
    template_name = 'accounts/account_create/course_join.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        current_user = request.user
        context = {
            "subjects": Subject.objects.all(),
            "courses": Course.objects.all(),
        }
        return render(request, self.template_name, context)


class AccountUpdateAjax(View):
    """
    Ajax submission for updating existing accounts
    """

    def post(self, request: HttpRequest) -> JsonResponse:
        current_user = request.user
        account = get_object_or_404(User, userid=request.POST['userid'])
        if current_user.is_authenticated and current_user == account:
            form = UserUpdateForm(request.POST, instance=account)
            if form.is_valid():
                user = form.save()
                user.clean()
                return JsonResponse({})
            else:
                return invalid_form_response(form)
        else:
            response = JsonResponse({})
            response.status_code = 401
            return response


class CourseJoinAjax(View):
    """
    Ajax submission for course registration
    """

    def post(self, request: HttpRequest) -> JsonResponse:
        current_user = request.user
        if (current_user.is_authenticated and request.POST['email'] == current_user.email
                and not current_user.has_perm('accounts.can_add_account_submission')):
            response = JsonResponse({
                "responseMessage": "Permission Denied. You do not have authorisation to make changes to this account"
            })
            response.status_code = 401
            return response
        else:
            form = CourseRegisterForm({
                'email': request.POST['email'],
                'course': Course.objects.get(id=request.POST['course']),
            })
            if form.is_valid():
                submission = form.save()
                submission.clean()
                return JsonResponse({})
            else:
                return invalid_form_response(form)


class RegisteredCourseAnalyticsAjax(View):
    """Ajax request for analytics data relating to courses the given user is registered to"""

    def post(self, request: HttpRequest) -> JsonResponse:
        current_user = request.user
        account = User.objects.get(userid=request.POST['account'])
        response = validate_account_view_ajax(current_user, account)
        if response:
            return response
        course = Course.objects.get(id=request.POST.get('course'))

        context = {"graphs": []}
        if account.is_student:
            # Graph all grades for provided account and course
            assignment_marks = Grade.objects.filter(student=account, assignment__module__course=course) \
                .order_by('datetime_submitted')
            context["graphs"].append({
                "container_id": "registered-course-1",
                "title": "assignment marks",
                "type": "bar",
                "data": [mark.grade for mark in assignment_marks],
                "label": [mark.datetime_submitted for mark in assignment_marks],
                "color": {
                    "type": "gradient",
                    "value": ["#FF0000", "#FFFF00", "#00FF00"]
                }
            })

            # Graph number of assignments completed against total number of assignments for course
            total = Assignment.objects.filter(module__course__students__in=[account], module__course=course)
            completed = total.filter(grade__student=account)
            num_completed = completed.count()
            context["graphs"].append({
                "container_id": "registered-course-2",
                "title": "course progress",
                "type": "pie",
                "data": [num_completed, total.count() - num_completed],
                "label": ["completed", "uncompleted"],
                "color": {
                    "type": "list",
                    "value": ["#00AA22", "#22222288"]
                },
            })

            context['module_progress'] = []
            for module in Module.objects.filter(course=course):
                # Graph number of assignments completed for module in course
                total = Assignment.objects.filter(module__course__students__in=[account], module=module)
                completed = total.filter(grade__student=account)
                num_completed = completed.count()
                context["graphs"].append({
                    "container_id": "registered-course-3",
                    "title": "module: " + module.title,
                    "type": "pie",
                    "data": [num_completed, total.count() - num_completed],
                    "label": ["completed", "uncompleted"],
                    "color": {
                        "type": "list",
                        "value": ["#00AA22", "#22222288"]
                    },
                })

        return JsonResponse(context)


class OwnedCourseAnalyticsAjax(View):
    """Ajax request for analytics data relating to courses owned by a given user"""

    def post(self, request: HttpRequest) -> HttpResponse:
        current_user = request.user
        account = User.objects.get(userid=request.POST['account'])
        response = validate_account_view_ajax(current_user, account, True)
        if response:
            return response
        course = Course.objects.get(id=request.POST.get('course'))
        course_students = course.students.all()

        context = {
            "title": course.title,
            "graphs": [],
            "number_data": [
                {
                    "container_id": "owned-course-numbers-1",
                    "name": "student count",
                    "value": course_students.count(),
                }
            ]
        }

        # Graph average score for each assignment in course
        course_assignments = Assignment.objects.filter(module__course=course).order_by('order')
        assignment_titles = [assignment.title for assignment in course_assignments]
        context["graphs"].append({
            "container_id": "owned-course-1",
            "title": "average score",
            "type": "bar",
            "data": [mean(grade.grade for grade in Grade.objects.filter(assignment=assignment))
                     for assignment in course_assignments],
            "label": assignment_titles,
            "color": {
                "type": "gradient",
                "value": ["#FF0000", "#FFFF00", "#00FF00"]
            }
        })

        # Graph average time taken (minutes) to complete each assignment in course
        context["graphs"].append({
            "container_id": "owned-courses-2",
            "title": "average time taken",
            "type": "bar",
            "data": [mean(grade.time_taken.total_seconds()
                          for grade in Grade.objects.filter(assignment=assignment)) / 60
                     for assignment in course_assignments],
            "label": assignment_titles,
            "color": {
                "type": "gradient",
                "value": ["#FF0000", "#FFFF00", "#00FF00"]
            }
        })

        # Identify all modules and their assignments
        context["modules"] = {}
        for module in Module.objects.filter(course=course):
            context["modules"][module.id] = {
                "assignments": [{
                    "label": assignment.title,
                    "id": assignment.id
                } for assignment in module.assignments.all()],
                "name": module.title
            }
        return JsonResponse(context)


class CourseAssignmentAnalyticsAjax(View):
    """Ajax request for analytics data relating to assignments in a given course"""

    def post(self, request: HttpRequest) -> JsonResponse:
        current_user = request.user
        account = User.objects.get(userid=request.POST['account'])
        response = validate_account_view_ajax(current_user, account, True)
        if response:
            return response
        assignment = get_object_or_404(Assignment, id=request.POST.get('assignment'))

        context = {
            "graphs": [],
            "number_data": [
                {
                    "container_id": "course-assignment-numbers-1",
                    "name": "average score",
                    "value": mean(float(grade.grade) for grade in Grade.objects.filter(assignment=assignment)),
                },
                {
                    "container_id": "course-assignment-numbers-1",
                    "name": "average time",
                    "value": mean(grade.time_taken.total_seconds()
                                  for grade in Grade.objects.filter(assignment=assignment)) / 60
                },
            ]
        }

        # Graph of marks each student received for the given assignment
        students = assignment.module.course.students.all()
        context["graphs"].append({
            "container_id": "course-assignment-1",
            "title": "student marks",
            "type": "bar",
            "data": [Grade.objects.get(student=student, assignment=assignment).grade for student in students],
            "label": [student.id for student in students],
            "color": {
                "type": "gradient",
                "value": ["#FF0000", "#FFFF00", "#00FF00"]
            }
        })

        # Graph of time taken (minutes) for each student to complete the given assignment
        context["graphs"].append({
            "container_id": "course-assignment-2",
            "title": "time taken",
            "type": "bar",
            "data": [Grade.objects.get(student=student, assignment=assignment).time_taken.total_seconds() / 60
                     for student in students],
            "label": [student.id for student in students],
            "color": {
                "type": "gradient",
                "value": ["#FF0000", "#FFFF00", "#00FF00"]
            }
        })
        return JsonResponse(context)


def invalid_form_response(form: forms.ModelForm) -> JsonResponse:
    """
    Generate standard json response for invalid forms
    (uses error code 422 - Unprocessable Entity)
    form -- Form, which has been shown to be invalid
    return -- JsonResponse with error code and form parameters
    """
    response = JsonResponse({'form': form.errors})
    response.status_code = 422
    return response


def validate_account_view_ajax(current_user: User, account: User,
                               needs_view_perm: bool = False) -> Union[JsonResponse, None]:
    """
    Ensure the given user has permissions to view analytics data for the given account
    current_user -- User attempting to view the analytics
    account -- Account the current_user is trying to view
    needs_view_perm -- Whether the current_user should have permission to view all profiles to view this account
    return -- JsonResponse with error code if current_user is not authorized else None
    """
    if (not current_user.has_perm('accounts.view_profile') and (needs_view_perm or current_user != account)
            or not current_user.is_authenticated):
        response = JsonResponse({})
        response.status_code = 401
        return response
    return None


def get_user_details(account: User, reader: User) -> Dict[str, any]:
    """
    Get details from account based on permissions held by reader
    account -- Profile instance of the account being read
    reader -- Profile instance of the user sending the request
    """
    if reader.is_authenticated and (account == reader or reader.has_perm('accounts.view_profile')):
        # Reader has permissions to fully view this account, or is this account
        user_details = parse_details(account, FULL_VIEW)
    elif account.is_staff:
        user_details = parse_details(account, PARTIAL_STAFF_VIEW)
    else:
        user_details = parse_details(account, PARTIAL_VIEW)
    return user_details


def parse_details(account: User, allowed_details: Sequence[str]) -> Dict[str, any]:
    """
    Parse details on the given account into dictionary format
    account -- User to be parsed
    allowed_details -- Parameters to be parsed from the account
    """
    details = {}
    if 'userid' in allowed_details:
        details["userid"] = account.userid
    if 'firstname' in allowed_details:
        details["firstname"] = account.first_name
    if 'lastname' in allowed_details:
        details["lastname"] = account.last_name
    if 'contacts' in allowed_details or 'email' in allowed_details:
        details["contacts"] = []
        details["contacts"].append({"name": "email",
                                    "value": account.email,
                                    "show_as": "Email"})
        if "contacts" in allowed_details:
            details["contacts"].append({"name": "phone_number",
                                        "value": account.phone_number,
                                        "show_as": "Phone Number"})
            details["contacts"].append({"name": "term_address",
                                        "value": account.term_address,
                                        "show_as": "Term Address"})
    if 'student' in allowed_details:
        details["student"] = account.is_student
    if 'staff' in allowed_details:
        details["staff"] = account.is_staff
    if 'superuser' in allowed_details:
        details["superuser"] = account.is_superuser
    return details


PARTIAL_VIEW = ("userid", "firstname",
                "student", "staff")
PARTIAL_STAFF_VIEW = ("userid", "firstname", "email",
                      "student", "staff")
FULL_VIEW = ("userid", "firstname", "lastname", "contacts", "online",
             "student", "staff", "superuser")
