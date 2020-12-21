from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
import random

from .models import Profile


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'

    def clean_userid(self):
        userid = str(self.cleaned_data['userid'])
        if userid is None or userid == '':
            for _ in range(100):
                userid = "u" + "".join([random.choice("0123456789") for __ in range(19)])
                if Profile.objects.filter(userid=userid).count() == 0:
                    return userid
            raise FailedGenerationError("Failed to generate unique userid")
        return userid

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Profile
        fields = ('userid', 'email', 'password', 'is_student', 'is_staff', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]


class FailedGenerationError(Exception):
    def __init(self, message="Failed attempt at generating default value"):
        self.message = message
        super().__init__(self.message)
