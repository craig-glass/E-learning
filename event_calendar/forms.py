from django.forms import ModelForm, DateInput
from event_calendar.models import Event

#The EventForm class created a form using the Django library ModelForm. The library is used to
# a form using the data fields of the event model. This class is specifically used to create a
#form that will be populated with data about an event which has been clicked on.
class EventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields.
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    #This function adds widgets to each field to set them to read only, so the user cannot
    #edit them when viewing the populated data.
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['readonly'] = True
        self.fields['description'].widget.attrs['readonly'] = True
        #Select fields cannot be set to readonly so disabled widget has to be used.
        self.fields['course'].widget.attrs['disabled'] = True
        self.fields['description'].widget.attrs['textarea'] = True
        self.fields['start_time'].widget.attrs['readonly'] = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].widget.attrs['readonly'] = ('%Y-%m-%dT%H:%M',)


#This class is used by staff to either edit existing events or to add new events.
class EventNewForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields.
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventNewForm, self).__init__(*args, **kwargs)
        # input_formats parses HTML5 datetime-local input to datetime field.
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
