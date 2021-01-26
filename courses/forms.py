from django import forms
from django.forms.models import inlineformset_factory, ModelForm
from .models import Course, Module, Assignment, Quiz, Question, Choice

ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=[
                                          'title',
                                          'description'],
                                      extra=2,
                                      can_delete=True
                                      )

AssignmentFormSet = inlineformset_factory(Module,
                                          Assignment,
                                          fields=[
                                              'title',
                                              'description',
                                              'due_date'],
                                          extra=2,
                                          can_delete=True)

QuizFormSet = inlineformset_factory(Module,
                                    Quiz,
                                    fields=[
                                        'title',
                                        'description'],
                                    extra=2,
                                    can_delete=True)

ChoiceFormSet = inlineformset_factory(Question,
                                      Choice,
                                      fields=[
                                          'choice_text',
                                          'correct_answer'
                                      ],
                                      extra=1)


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['number', 'question_text']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False

