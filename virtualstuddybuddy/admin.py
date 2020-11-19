from django.contrib import admin

# Register your models here.
from .models import Profile
from .models import StudyGroup
from .models import *

admin.site.register(Profile)
admin.site.register(StudyGroup)
admin.site.register(UserInbox)
admin.site.register(UserMessage)
admin.site.register(GroupInbox)
admin.site.register(GroupMessage)
