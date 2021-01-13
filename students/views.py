from django.apps import apps
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from config import settings
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from courses.models import Course, Module, Assignment
from django.views.generic.detail import DetailView
from courses.views import ModuleViewsMixin

from .models import AssignmentSubmission


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentHomePageView(DetailView):
    model = Course
    template_name = 'students/home.html'


class StudentDetailViewMixin(DetailView):
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(
                id=self.kwargs['module_id']
            )
        else:
            context['module'] = course.modules.all()[0]

        return context


class StudentCourseDetailView(StudentDetailViewMixin):
    template_name = 'students/course/detail.html'


class AssignmentListStudentView(StudentDetailViewMixin):
    template_name = 'students/assignments/list.html'


class AssignmentDetailStudentView(DetailView):
    model = Course
    template_name = 'students/assignments/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['module'] = course.modules.get(
            id=self.kwargs['module_id']
        )
        context['assignment'] = context['module'].assignments.get(
            id=self.kwargs['assignment_id']
        )

        return context


class AssignmentSubmissionView(TemplateResponseMixin, View):
    model = None
    module = None
    course = None
    assignment = None
    obj = None
    template_name = 'students/assignments/submission.html'

    def get_model(self):
        return apps.get_model(app_label='students',
                              model_name='AssignmentSubmission')

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['assignment',
                                                 'course',
                                                 'date_of_submission',
                                                 'student'
                                                 ])
        return Form(*args, **kwargs)

    def dispatch(self, request, pk, module_id, assignment_id, id=None):
        self.assignment = get_object_or_404(Assignment,
                                            id=assignment_id,
                                            )
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        )
        self.model = self.get_model()
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, pk, module_id, assignment_id, id)

    def get(self, request, pk, module_id, assignment_id, id=None):
        form = self.get_form(self.model, instance=self.obj)
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        assignment = get_object_or_404(Assignment,
                                       id=assignment_id,
                                       )
        course = get_object_or_404(Course,
                                   id=pk,
                                   )
        return self.render_to_response({'form': form,
                                        'module': module,
                                        'course': course,
                                        'assignment': assignment,
                                        'object': self.obj})

    def post(self, request, course_id, module_id, assignment_id, id=None):
        form = self.get_form(self.model,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.student = request.user
            obj.assignment = self.assignment
            obj.course = self.course
            obj.submitted_file = request.FILES['submitted_file']
            obj.save()
            return redirect('student_assignment_detail', self.course.id, self.module.id, self.assignment.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

