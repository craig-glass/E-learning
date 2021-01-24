import datetime

from django.apps import apps
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView

from courses.models import Course, Module, Assignment, AssignmentContent, Grade
from courses.models import Quiz, Question, Choice
from .forms import CourseEnrollForm
from .models import QuizAnswer, QuizSubmission, AssignmentSubmission


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('students:student_course_list')

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
        return reverse_lazy('students:student_course_detail',
                            args=[self.course.id])


class ModulePageMixin:
    def get_context(self, request, course_id=None, module_id=None, assignment_id=None, quiz_id=None, **kwargs):
        context = {}
        context["course_list"] = Course.objects.filter(students__in=[request.user]).order_by('id')
        context["course"] = None if course_id is None else get_object_or_404(Course, id=course_id)
        context["module_list"] = (None if context["course"] is None
                                  else Module.objects.filter(course=context["course"]).order_by('order'))
        context["module"] = None if module_id is None else get_object_or_404(Module, id=module_id)
        context["assignment_list"] = (None if context["module"] is None
                                      else Assignment.objects.filter(module=context["module"]))
        context["assignment"] = None if assignment_id is None else get_object_or_404(Assignment, id=assignment_id)
        context["quiz_list"] = (None if context["module"] is None
                                else Quiz.objects.filter(module=context["module"]))
        context["quiz"] = None if quiz_id is None else get_object_or_404(Quiz, id=quiz_id)
        return context


class StudentCourseListView(LoginRequiredMixin, ModulePageMixin, View):
    template_name = 'students/course/list.html'

    def get(self, request, pk=None):
        context = self.get_context(request, pk)
        return render(request, self.template_name, context)


class StudentCourseDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, module_id):
        return redirect('students:module_home_page', pk=pk, module_id=module_id)


class ModuleHomePageView(LoginRequiredMixin, ModulePageMixin, View):
    template_name = 'students/course/module_home.html'

    def get(self, request, pk, module_id):
        context = self.get_context(request, pk, module_id)
        return render(request, self.template_name, context)


class StudentHomePageView(LoginRequiredMixin, ModulePageMixin, View):
    template_name = 'students/home.html'

    def get(self, request, pk, module_id):
        context = self.get_context(request, pk, module_id)
        return render(request, self.template_name, context)


class AssignmentListStudentView(LoginRequiredMixin, ModulePageMixin, View):
    template_name = 'students/assignments/list.html'

    def get(self, request, pk, module_id):
        context = self.get_context(request, pk, module_id)
        return render(request, self.template_name, context)


class QuizListStudentView(LoginRequiredMixin, ModulePageMixin, View):
    template_name = 'students/quizzes/list.html'

    def get(self, request, pk, module_id):
        context = self.get_context(request, pk, module_id)
        return render(request, self.template_name, context)


class StudentDetailViewMixin(LoginRequiredMixin, DetailView):
    model = Course

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(
                id=self.kwargs['module_id']
            )

        return context


class AssignmentDetailStudentView(LoginRequiredMixin, ModulePageMixin, View):
    template_name = 'students/assignments/detail.html'

    def get(self, request, pk, module_id, assignment_id):
        context = self.get_context(request, pk, module_id, assignment_id=assignment_id)
        return render(request, self.template_name, context)


class AssignmentSubmissionView(TemplateResponseMixin, ModulePageMixin, View):
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

    def dispatch(self, request, pk, module_id, assignment_id, id=None, redo=None):
        self.assignment = get_object_or_404(Assignment,
                                            id=assignment_id)
        self.module = get_object_or_404(Module,
                                        id=module_id)
        self.course = get_object_or_404(Course,
                                        id=pk)
        self.model = self.get_model()
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, pk, module_id, assignment_id, id, redo=redo)

    def get(self, request, pk, module_id, assignment_id, id=None, redo=None):
        form = self.get_form(self.model, instance=self.obj)
        context = self.get_context(request, pk, module_id, assignment_id=assignment_id)
        context["form"] = form
        context["object"] = self.obj
        if not redo and AssignmentSubmission.objects.filter(assignment=context["assignment"],
                                                            student=request.user).count():
            return redirect("students:assignment_submitted_view", pk, module_id, assignment_id)
        elif context["assignment"].due_date is not None and context["assignment"].due_date < datetime.datetime.now():
            context["overdue"] = True
            return redirect("students:assignment_submitted_view", pk, module_id, assignment_id)
        return self.render_to_response(context)

    def post(self, request, course_id, module_id, assignment_id, id=None, redo=None):
        form = self.get_form(self.model,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.student = request.user
            obj.assignment = self.assignment
            obj.course = self.course
            obj.submitted_file = request.FILES['submitted_file']
            obj.save()
            return redirect('students:assignment_submitted_view', self.course.id, self.module.id, self.assignment.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


class QuizSubmissionView(TemplateResponseMixin, ModulePageMixin, View):
    model = None
    module = None
    course = None
    quiz = None
    obj = None
    template_name = 'students/quizzes/detail.html'

    def get_model(self):
        return apps.get_model(app_label='students',
                              model_name='QuizAnswer')

    def dispatch(self, request, pk, module_id, quiz_id, id=None, redo=None):
        self.quiz = get_object_or_404(Quiz,
                                      id=quiz_id)
        self.module = get_object_or_404(Module,
                                        id=module_id)
        self.course = get_object_or_404(Course,
                                        id=pk)
        self.model = self.get_model()
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, pk, module_id, quiz_id, id, redo=redo)

    def get(self, request, pk, module_id, quiz_id, id=None, redo=None):
        context = self.get_context(request, pk, module_id, quiz_id=quiz_id)
        context["object"] = self.obj
        if not redo and QuizSubmission.objects.filter(quiz=context["quiz"],
                                                      student=request.user).count():
            return redirect("students:quiz_submitted_view", pk, module_id, quiz_id)
        elif context["quiz"].due_date is not None and context["quiz"].due_date < datetime.datetime.now():
            context["overdue"] = True
            return redirect("students:quiz_submitted_view", pk, module_id, quiz_id)
        return self.render_to_response(context)

    def post(self, request, pk, module_id, quiz_id, id=None, redo=None):

        input_names = [name for name in request.POST.keys() if name.startswith('question')]

        if input_names:
            quiz_submission = QuizSubmission.objects.create(student=self.request.user, quiz=Quiz(quiz_id))
            for input_name in input_names:
                answer = request.POST[input_name]
                answer_split = input_name.split('-')
                question_id = answer_split[1]
                correct = False

                if Choice.objects.get(choice_text=answer, question=Question(question_id)).correct_answer:
                    correct = True

                QuizAnswer.objects.create(answer=answer, question=Question(question_id),
                                          quiz_submission=quiz_submission, is_correct=correct)
            score = QuizAnswer.objects.filter(quiz_submission=quiz_submission, is_correct=True).count()
            QuizSubmission.objects.filter(id=quiz_submission.id).update(score=score)
            return redirect('students:quiz_submitted_view', self.course.id, self.module.id, self.quiz.id)
        return redirect('students:quiz_detail_student_view', self.course.id, self.module.id, self.quiz.id)


class QuizSubmittedView(LoginRequiredMixin, ModulePageMixin, View):
    template_name = 'students/quizzes/submitted.html'

    def get(self, request, pk, module_id, quiz_id):
        context = self.get_context(request, pk, module_id, quiz_id=quiz_id)
        context["submission"] = context["quiz"].submissions.filter(
            student=self.request.user
        ).latest('id')
        return render(request, self.template_name, context)


class AssignmentSubmittedView(LoginRequiredMixin, ModulePageMixin, View):
    template_name = 'students/assignments/submitted.html'

    def get(self, request, pk, module_id, assignment_id, redo=False):
        context = self.get_context(request, pk, module_id, assignment_id=assignment_id)
        context["submission"] = context["assignment"].submissions.filter(
            student=self.request.user
        ).latest('id')
        context["grade"] = Grade.objects.filter(assignment=context["assignment"],
                                                student=request.user).latest('datetime_submitted')
        return render(request, self.template_name, context)


class ModuleContentView(LoginRequiredMixin, ModulePageMixin, View):
    template_name = 'students/contents/detail.html'

    def get(self, request, pk, module_id):
        context = self.get_context(request, pk, module_id)
        return render(request, self.template_name, context)
