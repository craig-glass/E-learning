from django.contrib import admin

from .models import Subject, Course, Module, Assignment, Quiz

"""
Registering models to be used in django admin.
"""
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class AssignmentInline(admin.StackedInline):
    model = Assignment


class QuizInline(admin.StackedInline):
    model = Quiz


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    search_fields = ['title', 'overview']
    inlines = [AssignmentInline, QuizInline]


class StaffInline(admin.TabularInline):
    model = Course.staff.through
    extra = 1
    verbose_name = "Course Staff"
    verbose_name_plural = "Course Staff"


class StudentInline(admin.TabularInline):
    model = Course.students.through
    extra = 1
    verbose_name = "Course Student"
    verbose_name_plural = "Course Students"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [
        StaffInline,
        StudentInline,
        ModuleInline
    ]

    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    fieldsets = (
        (None, {'fields': ('subject', 'owner')}),
        ('Context', {'fields': ('title', 'slug', 'overview')}),
    )
    add_fieldsets = (
        (None, {'fields': ('subject', 'owner')}),
        ('Context', {'fields': ('title', 'slug', 'overview')}),
    )
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}

