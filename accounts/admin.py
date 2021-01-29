from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserCreationForm, UserChangeForm
from .models import Profile, AccountSubmission
from courses.models import Course


def accept_submissions(modeladmin, request, queryset):
    failures = []
    for submission in queryset:
        user = Profile.objects.filter(email=submission.email)
        if user.exists():
            user = user.first()
        else:
            form = UserCreationForm({"email": submission.email})
            if form.is_valid():
                user = form.save()
                user.clean()
            else:
                failures.append((submission, form))
                continue
        if not user.is_student:
            Group.objects.get(name='student').user_set.add(user)
        submission.course.students.add(user)
        submission.delete()
    if failures:
        for s, f in failures:
            s.valid = False
            s.save()
        messages.warning(request, "Some submissions have failed validation.")


def reject_submissions(modeladmin, request, queryset):
    queryset.delete()


accept_submissions.short_description = 'Accept selected submissions'
reject_submissions.short_description = 'Reject selected submissions'


class CourseStudentsInline(admin.TabularInline):
    model = Course.students.through
    extra = 1
    verbose_name = "Student of Course"
    verbose_name_plural = "Student of Courses"


class CourseStaffInline(admin.TabularInline):
    model = Course.staff.through
    extra = 1
    verbose_name = "Staff of Course"
    verbose_name_plural = "Staff of Courses"


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    inlines = [
        CourseStudentsInline,
        CourseStaffInline
    ]

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
    list_display = ('email', 'course', 'date_submitted', 'valid')
    list_filter = ('course', 'date_submitted', 'valid')
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
