from django.forms.models import inlineformset_factory
from .models import Assignment
from courses.models import Module

AssignmentFormSet = inlineformset_factory(Module,
                                          Assignment,
                                          fields=[
                                              'title',
                                              'description'],
                                          extra=2,

                                          )
