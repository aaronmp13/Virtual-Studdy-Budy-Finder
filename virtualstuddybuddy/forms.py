from django.forms import *
from .models import *

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ["username"]

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
    
    def clean_group_name(self):
        data = self.cleaned_data['group_name']
        if StudyGroup.objects.all().filter(group_name=data):
            raise ValidationError("This group name is taken!")
        else:
            return data
