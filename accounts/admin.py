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
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('userid', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Contact info', {'fields': ('email', 'phone_number', 'term_address')}),
        ('Permissions', {'fields': ('is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('userid', 'email', 'password'),
        }),
        ('Optional', {
            'fields': ('first_name', 'last_name',
                       'phone_number', 'term_address')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'groups', 'user_permissions'),
        }),
    )
    search_fields = ('userid', 'email')
    ordering = ('userid', 'email')
    filter_horizontal = ('user_permissions', 'groups')

    def is_staff(self, obj):
        return obj.is_staff

    is_staff.boolean = True

    def is_student(self, obj):
        return obj.is_student

    is_student.boolean = True


admin.site.register(Profile, UserAdmin)
