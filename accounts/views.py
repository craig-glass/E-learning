from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse, HttpRequest
from typing import Dict
from django.contrib.auth.models import User

from .models import Profile


class AccountDisplayView(View):
    """
    View for displaying details of account specified in url
    Will show different results based on users permission level
    """
    template_name = 'accounts/account_view/account_view.html'

    def get(self, request: HttpRequest, userid: str = None) -> HttpResponse:
        current_user = request.user
        if userid is None:
            if current_user.is_authenticated:
                return redirect('/account/profile/' + current_user.userid)
            else:
                return redirect('/accounts/login')
        user_details = get_user_details(Profile.objects.get(userid=userid), current_user)
        can_edit = False
        context = {
            "user_details": user_details,
            "can_edit": can_edit,
        }
        return render(request, self.template_name, context)


def get_user_details(account: Profile, reader: User) -> Dict[str, any]:
    """
    Get details from account based on permissions held by reader
    account -- Profile instance of the account being read
    reader -- Profile instance of the user sending the request
    """
    user_details = {}
    if reader.is_authenticated and (account == reader or reader.has_perm('accounts.readall')):
        user_details["userid"] = account.userid
        user_details["firstname"] = account.first_name
        user_details["lastname"] = account.last_name

        user_details["contacts"] = {"Email": account.email}
        user_details["contacts"]["Phone"] = account.phone_number
        user_details["contacts"]["Term Address"] = account.term_address

        user_details["student"] = account.is_student
        user_details["staff"] = account.is_staff
        user_details["superuser"] = account.is_superuser

        user_details["online"] = account.is_active
    return user_details
