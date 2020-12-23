from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View

from courses.models import Module


class AssignmentsContentView(TemplateResponseMixin, View):
    template_name = 'assignments/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        return self.render_to_response({'module': module})

