from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import make_password
import random

from .models import Profile, AccountSubmission


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def clean_userid(self):
        userid = str(self.cleaned_data['userid'])
        if userid is None or userid == '':
            for _ in range(100):
                userid = 'u' + ''.join([random.choice('0123456789') for __ in range(8)])
                if Profile.objects.filter(userid=userid).count() == 0:
                    return userid
            raise FailedGenerationError('Failed to generate unique userid')
        return userid

    def clean_password(self):
        password = self.cleaned_data['password']
        if password is None or password == '':
            return None
        return make_password(password)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') is None:
            cleaned_data['password'] = make_password(cleaned_data.get('userid'))

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Profile
        fields = ('userid', 'first_name', 'last_name', 'email', 'password')

    def clean_password(self):
        return self.initial["password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'term_address')

    def clean_password(self):
        return make_password(self.cleaned_data['password'])

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class CourseRegisterForm(forms.ModelForm):
    class Meta:
        model = AccountSubmission
        fields = ('email', 'course')

    def save(self, commit=True):
        submission = super().save(commit=False)
        if commit:
            submission.save()
        return submission


class FailedGenerationError(Exception):
    def __init(self, message="Failed attempt at generating default value"):
        self.message = message
        super().__init__(self.message)
