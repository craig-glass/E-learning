from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Profile
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('userid', 'email', 'first_name', 'last_name',
                    'is_student', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser', 'is_staff', 'is_student')

    fieldsets = (
        (None, {'fields': ('userid', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Contact info', {'fields': ('email', 'phone_number', 'term_address')}),
        ('Permissions', {'fields': ('is_student', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')
        })
    )
    search_fields = ('userid', 'email')
    ordering = ('userid', 'email')
    filter_horizontal = ()


admin.site.register(Profile, UserAdmin)
