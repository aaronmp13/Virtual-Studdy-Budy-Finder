from django.forms import *
from .models import *
from django.utils.translation import gettext_lazy as _


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        # exclude = ["username"]
        fields = ["username", "name", "gender", "major", "age", "description", "coursework", "classOf", "picture"]

        labels = {
            'name': "Name",
            'classOf': "Class Of",
        }

        widgets = {
            'description': Textarea(attrs={'rows': 3,
                                           'placeholder': 'Write a little about yourself! Make sure to include what subjects you need help with as well as which ones you can help with.'}),
            'username': TextInput(attrs={'placeholder': 'Enter a Username'}),
            'name': TextInput(attrs={'placeholder': 'Firstname Lastname'}),
            'coursework': TextInput(attrs={'rows': 3, 'placeholder': 'CS3240, APMA3080, RELG1010, STAT2020, CS4774'}),
            'picture': FileInput(
                attrs={'style': 'display: none;', 'class': 'form-control', 'required': False})
        }


class GroupForm(ModelForm):
    class Meta:
        model = StudyGroup
        exclude = ['profiles']

        labels = {
            'group_name': "Group Name",
            'group_description': "Group Description",
        }

        widgets = {
            'group_name': TextInput(attrs={'placeholder': 'Awesome CS Group!'}),
            'group_description': TextInput(attrs={'placeholder': 'What is the focus of this study group?'}),

        }


class MeetForm(Form):
    date = DateField(label="Meeting Date", widget=TextInput(
        attrs={'type': 'date'}
    ))
    startTime = TimeField(label="Start Time", widget=TextInput(
        attrs={'type': 'time'}
    ))
    endTime = TimeField(label="End Time", widget=TextInput(
        attrs={'type': 'time'}))


class MessageForm(ModelForm):
    class Meta:
        model = UserMessage
        fields=['subject', 'recipient_username', 'message']

        labels = {
            'recipient_username': "Recipient Username",
            'subject': "Subject",
            'message': "Message",
        }

        widgets = {
            'recipient_username': TextInput(attrs={'placeholder': 'Type in a username, without the @'}),
            'subject': TextInput(attrs={'placeholder': 'Study Session on Tuesday'}),
            'message': Textarea(attrs={'rows': 3,'placeholder': 'Awesome CS Group is meeting on Tuesday at 5PM, wanna join?'}),
        }
