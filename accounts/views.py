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

        context = {}
        if account.is_student:
            # Graph all grades for provided account and course
            assignment_marks = Grade.objects.filter(student=account, assignment__module__course=course)\
                .order_by('date_submitted')
            context['assignment_marks'] = {
                "data": [mark.grade for mark in assignment_marks],
                "label": [mark.date_submitted for mark in assignment_marks],
                "color": {
                    "type": "gradient",
                    "gradient": ["#FF0000", "#FFFF00", "#00FF00"]
                }
            }
            # Graph number of assignments completed against total number of assignments for course
            total = Assignment.objects.filter(module__course__students__in=[account], module__course=course)
            completed = total.filter(grade__student=account)
            num_completed = completed.count()
            context['course_progress'] = {
                "data": [num_completed, total.count() - num_completed],
                "label": ["completed", "uncompleted"],
                "color": {
                    "type": "list",
                    "value": ["#00AA22", "#22222288"]
                },
            }

            context['module_progress'] = []
            for module in Module.objects.filter(course=course):
                total = Assignment.objects.filter(module__course__students__in=[account], module=module)
                completed = total.filter(grade__student=account)
                num_completed = completed.count()
                context['module_progress'].append(
                    {
                        "data": {
                            "data": [num_completed, total.count() - num_completed],
                            "label": ["completed", "uncompleted"],
                            "color": {
                                "type": "list",
                                "value": ["#00AA22", "#22222288"]
                            },
                        },
                        "name": "module: " + module.title,
                    }
                )

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
        import random
        random.seed(course.id)
        context = {}
        context['title'] = course.title
        # TODO use real data
        context['number_data'] = {
            "student_count": random.randint(100, 500)
        }
        as_data = [0.0004 * pow(random.randint(0, 100) - 50, 3) + 50 for i in range(random.randint(5, 15))]
        as_label = ['ws' + str(i) for i in range(len(as_data))]
        # TODO use real data
        context['average_score'] = {
            "data": as_data,
            "label": as_label,
            "color": {
                "type": "gradient",
                "gradient": ["#FF0000", "#FFFF00", "#00FF00"]
            }
        }
        at_data = [0.0011 * pow(random.randint(0, 60) - 30, 3) + 30 for i in range(len(as_label))]
        # TODO use real data
        context['average_time'] = {
            "data": at_data,
            "label": as_label,
            "color": {
                "type": "gradient",
                "gradient": ["#FF0000", "#FFFF00", "#00FF00"]
            }
        }

        context['modules'] = {}
        for module in Module.objects.filter(course=course):
            context['modules'][module.id] = {
                "assignments": [],
                "name": module.title
            }
        for assignment in Assignment.objects.filter(module__course=course):
            context['modules'][assignment.module.id]['assignments'].append({
                "label": assignment.title,
                "id": assignment.id
            })
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
        import random
        context = {}
        context['number_data'] = {
            # TODO use real data
            "average_score": random.randint(0, 100),
            # TODO use real data
            "average_time": random.randint(20, 60)
        }
        labels = [student.userid for student in assignment.module.course.students.all()]
        # TODO use real data
        context['assignment_marks'] = {
            "data": [random.randint(0, 100) for _ in range(len(labels))],
            "label": labels,
            "color": {
                "type": "gradient",
                "gradient": ["#FF0000", "#FFFF00", "#00FF00"]
            }
        }
        # TODO use real data
        context['assignment_time'] = {
            "data": [random.randint(20, 60) for _ in range(len(labels))],
            "label": labels,
            "color": {
                "type": "gradient",
                "gradient": ["#FF0000", "#FFFF00", "#00FF00"]
            }
        }
        return JsonResponse(context)


def invalid_form_response(form: forms.ModelForm) -> JsonResponse:
    """
    Generate standard json response for invalid forms
    (uses error code 422 - Unprocessable Entity)
    form -- Form, which has been shown to be invalid
    """
    response = JsonResponse({'form': form.errors})
    response.status_code = 422
    return response


def validate_account_view_ajax(current_user: User, account: User,
                               needs_view_perm: bool = False) -> Union[JsonResponse, None]:
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
    account --

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
