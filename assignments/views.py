from django.forms.models import modelform_factory
from django.apps import apps
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View

from assignments.forms import AssignmentFormSet
from assignments.models import Assignment
from courses.forms import ModuleFormSet
from courses.models import Module, Content, AssignmentContent, Course
from courses.views import OwnerCourseEditMixin


class AssignmentsListView(TemplateResponseMixin, View):
    template_name = 'assignments/list.html'

    def get(self, request, assignment_id):
        assignment = get_object_or_404(Assignment,
                                       id=assignment_id,
                                       )
        return self.render_to_response({'assignment': assignment})


class CourseAssignmentUpdateView(TemplateResponseMixin, OwnerCourseEditMixin, View):
    template_name = 'assignments/manage/assignment/formset.html'
    module = None
    permission_required = 'courses.change_module'

    def get_formset(self, data=None):
        return AssignmentFormSet(instance=self.module,
                                 data=data)

    def dispatch(self, request, pk):
        self.module = get_object_or_404(Module,
                                        id=pk,
                                        )
        return super().dispatch(request, pk)

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


class AssignmentContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(AssignmentContent,
                                    id=id,
                                    module__course__owner=request.user)
        assignment = content.assignment
        content.item.delete()
        content.delete()
        return redirect('assignments_list', assignment.id)