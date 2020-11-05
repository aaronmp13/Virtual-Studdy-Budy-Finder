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
