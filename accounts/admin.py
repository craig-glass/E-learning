from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserCreationForm, UserChangeForm
from .models import Profile, AccountSubmission


def accept_submissions(modeladmin, request, queryset):
    for submission in queryset:
        existing_user = Profile.objects.filter(email=submission.email)
        if existing_user.exists():
            print("exists")
        else:
            print("not exist")


def reject_submissions(modeladmin, request, queryset):
    queryset.delete()


accept_submissions.short_description = 'Accept selected submissions'
reject_submissions.short_description = 'Reject selected submissions'


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


class AccountSubmissionAdmin(admin.ModelAdmin):
    list_display = ('email', 'course', 'date_submitted')
    list_filter = ('course', 'date_submitted')
    search_fields = ('email', 'course', 'date_submitted')
    ordering = ('date_submitted', 'course', 'email')

    actions = (accept_submissions, reject_submissions)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(AccountSubmission, AccountSubmissionAdmin)
admin.site.register(Profile, UserAdmin)
