from django.forms import *
from .models import *
from django.utils.translation import gettext_lazy as _


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        #exclude = ["username"]
        fields = ["username", "name", "gender", "major", "age", "description", "coursework", "classOf", "picture"]

        labels = {
            'name': "Name",
            'classOf': "Class Of",
        }

        widgets = {
            'description': Textarea(attrs={'rows':3,'placeholder': 'Write a little about yourself! Make sure to include what subjects you need help with as well as which ones you can help with.'}),
            'username': TextInput(attrs={'placeholder': 'Enter a Username'}),
            'name': TextInput(attrs={'placeholder': 'Firstname Lastname'}),
            'coursework': TextInput(attrs={'rows':3, 'placeholder': 'CS3240, APMA3080, RELG1010, STAT2020, CS4774'}),
            'picture': FileInput(
                attrs={'style': 'display: none;', 'class': 'form-control', 'required': False})
        }

class GroupForm(ModelForm):
    class Meta:
        model = StudyGroup
        exclude = ['profiles']

class MeetForm(Form):
    date = DateField(label = "Meeting Date (yyyy-mm-dd)")
    startTime = TimeField(label = "Start Time (hh:mm, military time)")
    endTime = TimeField(label = "End Time (hh:mm, military time)")