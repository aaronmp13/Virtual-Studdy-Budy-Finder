from django.forms import *
from .models import *

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        #exclude = ["username"]
        fields = "__all__"

        labels = {
            'classOf': "Class of" 
        }

        widgets = {
            'description': Textarea(attrs={'rows':3}),
            'coursework': Textarea(attrs={'rows':3})
        }

class GroupForm(ModelForm):
    class Meta:
        model = StudyGroup
        exclude = ['profiles']

class MeetForm(Form):
    date = DateField(label = "Meeting Date (yyyy-mm-dd)")
    startTime = TimeField(label = "Start Time (hh:mm)")
    endTime = TimeField(label = "End Time (hh:mm)")