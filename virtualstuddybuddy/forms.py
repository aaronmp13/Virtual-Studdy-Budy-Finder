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
