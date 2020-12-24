from django.shortcuts import render, redirect
from django.views.generic.base import View, TemplateResponseMixin
from django.http import HttpResponse, HttpRequest, JsonResponse
from typing import Dict, Tuple, Sequence
from django.contrib.auth.models import User
from django.views.generic.edit import FormView, CreateView

from .models import Profile
from .forms import UserCreationForm


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
            account = Profile.objects.get(userid=userid)
            if not (current_user.is_authenticated or account.is_staff):
                # Unauthenticated users can only view staff accounts, otherwise redirect home
                return redirect('/')
        can_edit, user_details = get_user_details(account, current_user)
        context = {
            "user_details": user_details,
            "can_edit": can_edit,
        }
        return render(request, self.template_name, context)


class AccountSettingsView(View):
    template_name = "accounts/account_view/account_settings.html"

    def get(self, request: HttpRequest, userid: str) -> HttpResponse:
        account = Profile.objects.get(userid=userid)
        context = {
            "account": account,
        }
        return render(request, self.template_name, context)


class AccountCreateView(View):
    """
    View for staff to create new accounts
    """
    template_name = 'accounts/account_create/account_create.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        current_user = request.user
        if not current_user.is_authenticated:
            return redirect('/accounts/login')
        elif not current_user.has_perm('accounts.add_profile'):
            return redirect('/')
        return render(request, self.template_name)


class AccountCreateAjax(View):
    """
    Ajax submission for creating new accounts
    """
    def post(self, request):
        current_user = request.user
        if current_user.is_authenticated and current_user.has_perm('accounts.add_profile'):
            form = UserCreationForm(request.POST)
            print(request.POST)
            if form.is_valid():
                user = form.save()
                user.clean()
                return JsonResponse({})
            else:
                print("ERRORS " + str(form.errors))
                response = JsonResponse({})
                response.status_code = 422
                return response
        else:
            response = JsonResponse({})
            response.status_code = 401
            return response


def get_user_details(account: Profile, reader: User) -> Tuple[bool, Dict[str, any]]:
    """
    Get details from account based on permissions held by reader
    account -- Profile instance of the account being read
    reader -- Profile instance of the user sending the request
    """
    can_edit = False
    user_details = {}
    if reader.is_authenticated and (account == reader or reader.has_perm('accounts.view_profile')):
        # Reader has permissions to fully view this account, or is this account
        user_details = parse_details(account, FULL_VIEW)
        if account == reader or reader.has_perm('accounts.change_profile'):
            can_edit = True
    elif account.is_staff:
        user_details = parse_details(account, PARTIAL_STAFF_VIEW)
    else:
        user_details = parse_details(account, PARTIAL_VIEW)
    return can_edit, user_details


def parse_details(account: Profile, allowed_details: Sequence[str]) -> Dict[str, any]:
    details = {}
    if 'userid' in allowed_details:
        details["userid"] = account.userid
    if 'firstname' in allowed_details:
        details["firstname"] = account.first_name
    if 'lastname' in allowed_details:
        details["lastname"] = account.last_name
    if 'contacts' in allowed_details or 'email' in allowed_details:
        details["contacts"] = {}
        details["contacts"]["email"] = account.email
        if "contacts" in allowed_details:
            details["contacts"]["phone"] = account.phone_number
            details["contacts"]["term address"] = account.term_address
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
