from django.forms import *
from .models import *
from django.utils.translation import gettext_lazy as _
import datetime

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
    
    def clean_date(self):
        date = self.cleaned_data['date']
        curr_date = datetime.datetime.now().date()
        if date < curr_date:
            raise ValidationError("This date is in the past!")
        else:
            return date


class MessageForm(ModelForm):
    class Meta:
        model = UserMessage
        fields = ['subject', 'recipient_username', 'message']

        labels = {
            'recipient_username': "Recipient Username",
            'subject': "Subject",
            'message': "Message",
        }

        widgets = {
            'recipient_username': TextInput(attrs={'placeholder': 'Type in a username, without the @'}),
            'subject': TextInput(attrs={'placeholder': 'Study Session on Tuesday'}),
            'message': Textarea(
                attrs={'rows': 3, 'placeholder': 'Awesome CS Group is meeting on Tuesday at 5PM, wanna join?'}),
        }

    def clean_recipient_username(self):
        data = self.cleaned_data['recipient_username']
        if not Profile.objects.all().filter(username=data).exists():
            raise ValidationError("Username does not exist")
        return data

class GroupMessageForm(Form): #honestly not sure if its good to make a Django form in this case but whatever
    message =  CharField(max_length = 100, label = "Message", widget=Textarea(attrs={'rows': 1,'placeholder': "When do you guys want to meet up for that project due in 30 minutes?"}))

class SearchBarForm(Form): 
 
    query =  CharField(max_length = 100, label = "", required = False,
        widget=TextInput(attrs={'placeholder': 'Biology Female 2023', 'id':'profile-search'}))
