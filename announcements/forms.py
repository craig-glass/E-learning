from django import forms
from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    title = forms.CharField()
    author = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Announcement
        fields = ('title', 'author','content',)

