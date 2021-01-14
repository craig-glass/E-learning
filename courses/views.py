from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from students.forms import CourseEnrollForm
from .forms import ModuleFormSet, AssignmentFormSet
from .models import Course, ModuleContent, AssignmentContent
from django.apps import apps
from django.forms.models import modelform_factory
from .models import Module, Assignment, Content
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from .models import Subject
from django.views.generic.detail import DetailView


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin,
                       LoginRequiredMixin,
                       PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, OwnerCourseEditMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None
    permission_required = 'courses.change_module'

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,
                             data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)

        return self.render_to_response({'form': form,
                                        'module': module,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                ModuleContent.objects.create(module=self.module,
                                             item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(ModuleContent,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


class ModuleViewsMixin(TemplateResponseMixin, View):
    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        return self.render_to_response({'module': module})


class ModuleListView(ModuleViewsMixin):
    template_name = 'courses/manage/module/list.html'


class ModuleContentListView(ModuleViewsMixin):
    template_name = 'courses/manage/module/content_list.html'


class AssignmentContentListView(ModuleViewsMixin):
    template_name = 'courses/manage/module/assignments/list.html'


class QuizListView(ModuleViewsMixin):
    template_name = 'courses/manage/module/quizzes/list.html'


class CourseAssignmentUpdateView(TemplateResponseMixin, OwnerCourseEditMixin, View):
    template_name = 'courses/manage/module/assignments/formset.html'
    module = None
    permission_required = 'courses.change_module'

    def get_formset(self, data=None):
        return AssignmentFormSet(instance=self.module,
                                 data=data)

    def dispatch(self, request, module_id):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        )
        return super().dispatch(request, module_id)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'module': self.module,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'module': self.module,
                                        'formset': formset})


class AssignmentUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/assignments/content-list.html'

    def get(self, request, module_id, assignment_id):
        assignment = get_object_or_404(Assignment,
                                       id=assignment_id,
                                       )
        module = get_object_or_404(Module,
                                   id=module_id,
                                   )
        return self.render_to_response({'assignment': assignment,
                                        'module': module})


class AssignmentCreateUpdateView(TemplateResponseMixin, View):
    model = None
    obj = None
    assignment = None
    module = None
    template_name = 'courses/manage/module/assignments/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, assignment_id, module_id, model_name, id=None):
        self.assignment = get_object_or_404(Assignment,
                                            id=assignment_id,
                                            )
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, assignment_id, module_id, model_name, id)

    def get(self, request, module_id, assignment_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)

        return self.render_to_response({'form': form,
                                        'module': module,
                                        'object': self.obj})

    def post(self, request, module_id, assignment_id, model_name, id=None):
        form = self.get_form(self.model,
                             data=request.POST,
                             files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                AssignmentContent.objects.create(assignment=self.assignment,
                                                 item=obj)
            return redirect('assignment_update', self.module.id, self.assignment.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(
                order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            ModuleContent.objects.filter(id=id,
                                         module__course__owner=request.user).update(
                order=order)
        return self.render_json_response({'saved': 'OK'})


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(
            total_courses=Count('courses')
        )
        courses = Course.objects.annotate(
            total_modules=Count('modules')
        )
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})


class CourseDetailView(DeleteView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object}
        )
        return context
