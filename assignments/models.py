from django.db import models

from courses.fields import OrderField


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


