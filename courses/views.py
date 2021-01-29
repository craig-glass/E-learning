from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic.base import TemplateResponseMixin, View
from students.forms import CourseEnrollForm
from .forms import ModuleFormSet, AssignmentFormSet, QuizFormSet, ChoiceFormSet, QuestionFormSet, QuestionForm
from .models import Course, ModuleContent, AssignmentContent, Quiz, Question, Choice
from django.apps import apps
from django.forms.models import modelform_factory, modelformset_factory
from .models import Module, Assignment, Content
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from .models import Subject
from django.views.generic.detail import DetailView


class OwnerMixin(object):
    """
    Filters objects that belong to the current user.
    To be used for views that interact with any model
    that contains an owner attribute
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    """
    Sets the current user in the owner attribute of the object being saved.
    To be used in form creation mixins to save the owner
    attribute as current user
    """

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CoursePageMixin:
    """
    Adds all existing objects to view
    """

    def get_context(self, request, course_slug=None, module_id=None,
                    assignment_id=None, quiz_id=None, subject_slug=None, **kwargs):
        context = {}
        context["subject_list"] = Subject.objects.all()
        if subject_slug is None:
            context["subject"] = None
            context["course_list"] = Course.objects.all().order_by('id')
        else:
            context["subject"] = get_object_or_404(Subject, slug=subject_slug)
            context["course_list"] = Course.objects.filter(subject=context["subject"])
        context["course"] = None if course_slug is None else get_object_or_404(Course, slug=course_slug)
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


class OwnedCoursePageMixin(CoursePageMixin):
    """
    Adds all existing objects that are owned by current user
    """

    def get_context(self, request, course_slug=None, module_id=None,
                    assignment_id=None, quiz_id=None, **kwargs):
        context = {}
        context["course_list"] = Course.objects.filter(owner=request.user).order_by('id')
        context["course"] = None if course_slug is None else get_object_or_404(Course, id=course_slug)
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


class OwnerCourseMixin(OwnerMixin,
                       LoginRequiredMixin,
                       PermissionRequiredMixin):
    """
    This adds the model used for querysets and ensures user
    is logged in and has correct permissions
    """

    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('courses:manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    This combines OwnerCourseMixin and OwnerEditMixin
    to define template that is used mutually by CreateView
    and UpdateView
    """

    template_name = 'courses/manage/course/form.html'


class CourseListView(CoursePageMixin, View):
    """
    Lists courses
    """

    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        context = self.get_context(request, subject_slug=subject)
        return render(request, self.template_name, context)


class CourseDetailView(CoursePageMixin, View):
    """
    Renders a detailed view of courses and modules it
    contains
    """

    template_name = 'courses/course/detail.html'

    def get(self, request, slug):
        context = self.get_context(request, course_slug=slug)
        return render(request, self.template_name, context)


class ManageCourseListView(LoginRequiredMixin, PermissionRequiredMixin,
                           OwnedCoursePageMixin, View):
    """
    Lists courses created by the user
    """

    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.create_course'

    def get(self, request):
        context = self.get_context(request)
        return render(request, self.template_name, context)


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """
    Checks the current user has correct permissions and
    allows the user to create page if authenticated
    """

    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """
    Checks current user's permissions to update course
    """

    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """
    Checks user's permissions to delete course
    """

    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, OwnerCourseEditMixin, View):
    """
    Dispatches course object based on url and allows
    user to update modules
    """

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
            return redirect('courses:manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """
    Dispatches module and allows user to create and update
    content for module
    """

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
            return redirect('courses:module_content_list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ContentDeleteView(View):
    """
    Checks that the user is the course owner and allows
    to delete module content if authenticated
    """

    def post(self, request, id):
        content = get_object_or_404(ModuleContent,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('courses:module_content_list', module.id)


class ModuleViewsMixin(TemplateResponseMixin, View):
    """
    Retrieves module related to course based on modules
    id given in url
    """

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        return self.render_to_response({'course': module.course, 'module': module})


class ModuleListView(ModuleViewsMixin):
    """
    Renders a list of modules
    """

    template_name = 'courses/manage/module/list.html'


class ModuleContentListView(ModuleViewsMixin):
    """
    Renders module content
    """

    template_name = 'courses/manage/module/content_list.html'


class AssignmentContentListView(ModuleViewsMixin):
    """
    Renders assignment content related to selected module
    """

    template_name = 'courses/manage/assignments/list.html'


class QuizListView(ModuleViewsMixin):
    """
    Renders list of quizzes related to selected module
    """

    template_name = 'courses/manage/quizzes/list.html'


class QuizAssignmentCreateView(TemplateResponseMixin, OwnerCourseEditMixin, View):
    """
    Gets selected module, checks permissions and renders
    a formset
    """

    module = None
    permission_required = 'courses.change_module'

    def dispatch(self, request, module_id):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        )
        return super().dispatch(request, module_id)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'module': self.module,
                                        'formset': formset})


class QuizCreateView(QuizAssignmentCreateView):
    """
    Renders a quiz form set for users to create
    quizzes for selected module
    """

    template_name = 'courses/manage/quizzes/formset.html'

    def get_formset(self, data=None):
        return QuizFormSet(instance=self.module,
                           data=data)

    def post(self, request, module_id, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses:quiz_list_view', module_id)
        return self.render_to_response({'module': self.module,
                                        'formset': formset})


class CourseAssignmentUpdateView(QuizAssignmentCreateView):
    """
    Renders a formset for users to create assignments for
    selected module
    """

    template_name = 'courses/manage/assignments/formset.html'

    def get_formset(self, data=None):
        return AssignmentFormSet(instance=self.module,
                                 data=data)

    def post(self, request, module_id, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses:assignment_content_list', module_id)
        return self.render_to_response({'module': self.module,
                                        'formset': formset})


class AssignmentUpdateView(TemplateResponseMixin, View):
    """
    Renders the contents of assignment that is selected and allows
    user to add content
    """

    template_name = 'courses/manage/assignments/content-list.html'

    def get(self, request, module_id, assignment_id):
        assignment = get_object_or_404(Assignment,
                                       id=assignment_id,
                                       )
        module = get_object_or_404(Module,
                                   id=module_id,
                                   )
        return self.render_to_response({'assignment': assignment,
                                        'module': module})


class QuizUpdateView(TemplateResponseMixin, View):
    """
    Renders the selected quiz with a list of current
    questions with the option to add more questions
    """

    template_name = 'courses/manage/quizzes/content-list.html'

    def get(self, request, module_id, quiz_id):
        quiz = get_object_or_404(Quiz,
                                 id=quiz_id)
        module = get_object_or_404(Module,
                                   id=module_id)
        return self.render_to_response({'quiz': quiz,
                                        'module': module})


class QuizCreateUpdateView(TemplateResponseMixin, View):
    """
    Allows users to create question and choices for
    selected quiz
    """

    model = None
    obj = None
    quiz = None
    module = None
    template_name = 'courses/manage/quizzes/form.html'

    def dispatch(self, request, module_id, quiz_id, id=None):
        self.quiz = get_object_or_404(Quiz,
                                      id=quiz_id)
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = apps.get_model(app_label='courses',
                                    model_name='Question')
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id)
        return super().dispatch(request, module_id, quiz_id, id)

    def get(self, request, module_id, quiz_id, id=None):
        question_formset = QuestionFormSet(instance=self.quiz, queryset=Question.objects.none())

        return self.render_to_response({'question_formset': question_formset,
                                        'quiz': self.quiz,
                                        'module': self.module,
                                        'object': self.obj})

    def post(self, request, module_id, quiz_id, id=None):
        question_formset = QuestionFormSet(request.POST, instance=self.quiz)

        if question_formset.is_valid():
            i = 0
            print(request.POST)
            question_formset.save()

            return redirect('courses:quiz_edit', self.module.id, self.quiz.id)
        return self.render_to_response({'question_formset': question_formset,
                                        'object': self.obj})


class AddChoiceView(TemplateResponseMixin, View):
    """
    Allows user to edit choices of the question selected
    """

    question = None
    module = None
    quiz = None
    template_name = 'courses/manage/quizzes/choices/formset.html'

    def get_formset(self, data=None):
        return ChoiceFormSet(instance=self.question,
                             data=data)

    def dispatch(self, request, module_id, quiz_id, question_id):
        self.question = get_object_or_404(Question,
                                          id=question_id,
                                          )
        self.module = get_object_or_404(Module,
                                        id=module_id)
        self.quiz = get_object_or_404(Quiz,
                                      id=quiz_id)
        return super().dispatch(request, module_id, quiz_id, question_id)

    def get(self, request, *args, **kwargs):
        form = QuestionForm(instance=self.question)
        formset = self.get_formset()
        return self.render_to_response({'module': self.module,
                                        'quiz': self.quiz,
                                        'form': form,
                                        'question': self.question,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        form = QuestionForm(instance=self.question, data=request.POST)
        formset = self.get_formset(data=request.POST)
        if form.is_valid():
            form.instance.quiz = self.quiz
            form.save()
        if formset.is_valid():
            formset.save()
            return redirect('courses:quiz_edit', self.module.id, self.quiz.id)
        return self.render_to_response({'module': self.module,
                                        'quiz': self.quiz,
                                        'form': form,
                                        'question': self.question,
                                        'formset': formset})


class QuestionDeleteView(View):
    """
    Checks that the user is the course owner and allows
    to delete module content if authenticated
    """

    def post(self, request, id):
        question = get_object_or_404(Question,
                                     id=id,
                                     quiz__module__course__owner=request.user)
        quiz = question.quiz
        module = quiz.module
        print(quiz)
        question.delete()
        return redirect('courses:quiz_edit', module.id, quiz.id)


class AssignmentCreateUpdateView(TemplateResponseMixin, View):
    """
    Renders a form for user to create content based on
    what content type user would like to create
    """

    model = None
    obj = None
    assignment = None
    module = None
    template_name = 'courses/manage/assignments/form.html'

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

    def dispatch(self, request, module_id, assignment_id, model_name, id=None):
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
        return super().dispatch(request, module_id, assignment_id, model_name, id)

    def get(self, request, module_id, assignment_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        print(module_id, assignment_id, model_name)
        print(Module.objects.filter(id=module_id))
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        assignment = get_object_or_404(Assignment,
                                       id=assignment_id)

        return self.render_to_response({'form': form,
                                        'module': module,
                                        'assignment': assignment,
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
            return redirect('courses:assignment_update', self.module.id, self.assignment.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """
    Used in conjuction with 'sortable' AJAX call to re-order
    modules by drag and drop
    """

    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(
                order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """
    Used in conjuction with 'sortable' AJAX call to re-order
    content by drag and drop
    """
    def post(self, request):
        for id, order in self.request_json.items():
            ModuleContent.objects.filter(id=id,
                                         module__course__owner=request.user).update(
                order=order)
        return self.render_json_response({'saved': 'OK'})
