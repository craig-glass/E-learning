from django.contrib import admin
from .models import Subject, Course, Module, Assignment, Quiz


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


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

