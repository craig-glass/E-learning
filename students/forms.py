from django import forms
from django.forms import inlineformset_factory, ModelForm, ModelMultipleChoiceField

from courses.models import Course, Question, Choice
from students.models import QuizAnswer


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)



