from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.generic.list import ListView
from django.http import HttpRequest

# Create your views here.

from django.http import HttpResponse
from .models import Profile

class ProfileView(generic.DetailView):
	model = Profile
	template_name = 'virtualstuddybuddy/profile.html'

def index(request):
    return render(request, 'virtualstuddybuddy/index.html')

def signup(request): #How we handle signups and logins
	try:
		if request.method == 'POST': 								#If a person filled out the sign up form
			profile1 = request.POST
			#print(comment1)
			p = Profile(username=request.user.get_username(), name=profile1['name'], gender=profile1['gender'], major=profile1['major'], age=profile1['age'], description=profile1['description'])
			
			if p.is_valid():
				p.save()
				qs = Profile.objects.all()
				return HttpResponseRedirect('/virtualstudybuddy/profile/'+str(p.id)+'/')
			else:
				return render(request, 'virtualstuddybuddy/signup.html')
		else: 														#If a person just logged in
			qs = Profile.objects.all()
			if qs.filter(username=request.user.get_username()).exists(): 				#If user is already signed up
				p = qs.filter(username=request.user.get_username())[0]
				return HttpResponseRedirect('/virtualstudybuddy/profile/'+str(p.id)+'/') #Direct them to their profile page
			else: 														#If the user hasn't filled out a profile yet
				return render(request, 'virtualstuddybuddy/signup.html') 	#Direct them to the signup form
	except:
		return render(request, 'virtualstuddybuddy/signup.html', {
			'error_message': "Invalid Input",
		})



