import datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from accounts.models import Profile
from .fields import OrderField
from django.template.loader import render_to_string
from django.conf import settings


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      related_name='courses_joined',
                                      blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}.{self.title}'


class Assignment(models.Model):
    module = models.ForeignKey('courses.Module',
                               related_name='assignments',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}.{self.title}'


class Content(models.Model):
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'file',
                                         'image',
                                         'video'
                                     )})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['order']
        abstract = True


class ModuleContent(Content):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    order = OrderField(blank=True, for_fields=['module'])


class AssignmentContent(Content):
    assignment = models.ForeignKey(Assignment,
                                   related_name='contents',
                                   on_delete=models.CASCADE)
    order = OrderField(blank=True, for_fields=['assignment'])


class ItemBase(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self}
        )


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()


class Quiz(models.Model):
    title = models.CharField(max_length=50)
    module = models.ForeignKey(Module,
                               on_delete=models.CASCADE,
                               related_name='quizzes')
    description = models.TextField()
    date_created = models.DateTimeField('date created', null=True)

    class Meta:
        verbose_name_plural = 'quizzes'

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz,
                             on_delete=models.CASCADE,
                             related_name='questions')
    number = models.PositiveIntegerField()
    question_text = models.TextField()

    def __str__(self):
        return str(self.number)


class Choice(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='choices')
    choice_text = models.CharField(max_length=100)
    correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Grade(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.PROTECT,
                                related_name='grades')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.PROTECT,
                                )
    assignment = models.ForeignKey(Assignment,
                                   on_delete=models.PROTECT,
                                   null=True,
                                   blank=True)
    # quiz = models.ForeignKey(Quiz,
    #                          on_delete=models.PROTECT,
    #                          null=True,
    #                          blank=True)
    grade = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.grade
