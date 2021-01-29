from django import forms
from django.forms.models import inlineformset_factory, ModelForm, BaseInlineFormSet, modelform_factory
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


class BaseQuestionFormSet(BaseInlineFormSet):
    """
    BaseQuestionFormSet:
    This class allows choices to be nested inside
    a question form so that questions and choices can
    be created together dynamically on the same
    page. It is set as a parameter as the QuestionFormSet
    inline formset is created
    """

    def add_fields(self, form, index):
        super(BaseQuestionFormSet, self).add_fields(form, index)

        form.nested = ChoiceFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='choices-%s-%s' % (
                form.prefix,
                ChoiceFormSet.get_default_prefix()))

    def is_valid(self):
        result = super(BaseQuestionFormSet, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):
        result = super(BaseQuestionFormSet, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result


QuestionFormSet = inlineformset_factory(Quiz,
                                        Question,
                                        formset=BaseQuestionFormSet,
                                        fields=['number',
                                                'question_text'],
                                        extra=1)


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['number', 'question_text']
