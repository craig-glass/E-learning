from django.shortcuts import render, redirect
from django.views.generic.base import View, TemplateResponseMixin
from django.http import HttpResponse, HttpRequest, JsonResponse
from typing import Dict
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
        if userid is None: # No userid specified in url
            if current_user.is_authenticated:
                # Redirect to current user's account page
                return redirect('/account/profile/' + current_user.userid)
            else:
                # Redirect to login page to authenticate
                return redirect('/accounts/login')
        user_details = get_user_details(Profile.objects.get(userid=userid), current_user)
        can_edit = False
        context = {
            "user_details": user_details,
            "can_edit": can_edit,
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
        elif not current_user.has_perm('accounts.create_user'):
            return redirect('/')
        return render(request, self.template_name)


class AccountCreateAjax(View):
    """
    Ajax submission for creating new accounts
    """
    def post(self, request):
        current_user = request.user
        if current_user.is_authenticated and current_user.has_perm('accounts.create_user'):
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



    # def post(self, request: HttpRequest) -> JsonResponse:
    #     current_user = request.user
    #     if not current_user.is_authenticated or not current_user.has_perm('accounts.create_new'):
    #         response = JsonResponse({})
    #         response.status_code = 401
    #         return response
    #     response_data = {}
    #     response = JsonResponse(response_data)
    #     userid = request.POST.get("userid")
    #     if userid != "" and (len(userid) > 50 or userid[0] == " "):
    #
    #     password = request.POST.get("password")
    #     firstname = request.POST.get("firstname")
    #     lastname = request.POST.get("lastname")
    #     email = request.POST.get("email")
    #     phone = request.POST.get("phone")
    #     address = request.POST.get("address")
    #     is_student = request.POST.get("is_student")
    #     is_staff = request.POST.get("is_staff")
    #     is_superuser = request.POST.get("is_superuser")
    #     return JsonResponse({})


def get_user_details(account: Profile, reader: User) -> Dict[str, any]:
    """
    Get details from account based on permissions held by reader
    account -- Profile instance of the account being read
    reader -- Profile instance of the user sending the request
    """
    user_details = {}
    if reader.is_authenticated and (account == reader or reader.has_perm('accounts.read_all')):
        user_details["userid"] = account.userid
        user_details["firstname"] = account.first_name
        user_details["lastname"] = account.last_name

        user_details["contacts"] = {"Email": account.email}
        user_details["contacts"]["Phone"] = account.phone_number
        user_details["contacts"]["Term Address"] = account.term_address

        user_details["student"] = account.is_student
        user_details["staff"] = account.is_staff
        user_details["superuser"] = account.is_superuser

        user_details["online"] = True
    return user_details
