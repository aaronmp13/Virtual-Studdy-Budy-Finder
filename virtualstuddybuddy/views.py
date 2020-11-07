from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.generic.list import ListView
from django.http import HttpRequest
from django.db import DataError
from .forms import *

# Create your views here.

from django.http import HttpResponse
from .models import Profile

class ProfileView(generic.DetailView):
	model = Profile
	template_name = 'virtualstuddybuddy/profile.html'


def index(request):
    return render(request, 'virtualstuddybuddy/index.html')

def signup(request): #How we handle signups and logins
	if not request.user.is_authenticated: #redirects to login if they haven't done that yet
		return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')
	
	if request.method == 'POST': #If a person filled out the sign up form
		form = ProfileForm(request.POST, request.FILES)
		p = None
		#p = form.save()
		if form.is_valid():
			p = form.save()
			p.username = request.user.get_username()
			p.save()
		else: #If the form is invalid, just make them fill it out again
			#print(form.errors)
			form = ProfileForm(request.POST, request.FILES)														
			return render(request, 'virtualstuddybuddy/signup.html', {'form':form})

		return HttpResponseRedirect('/virtualstudybuddy/profile/'+str(p.id)+'/')	
	else: 	#If a person just logged in		
		qs = Profile.objects.all()
		if qs.filter(username=request.user.get_username()).exists(): 				#If user is already signed up
			p = qs.filter(username=request.user.get_username())[0]
			return HttpResponseRedirect('/virtualstudybuddy/profile/'+str(p.id)+'/') #Direct them to their profile page
		else: 	
			form = ProfileForm()											#If the user hasn't filled out a profile yet
			return render(request, 'virtualstuddybuddy/signup.html', {'form':form}) 	#Direct them to the signup form

def editProfile(request):
	p = Profile.objects.all().filter(username=request.user.get_username())[0]
	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES, instance = p)
		if form.is_valid():
			form.save()
		else:
			# raise DataError(
			# 	form.errors
			# 	)
			form = ProfileForm(request.POST, request.FILES)														
			return render(request, 'virtualstuddybuddy/signup.html', {'form':form})
		return HttpResponseRedirect('/virtualstudybuddy/profile/'+str(p.id)+'/')
	else:
		initialDict = {f.name:getattr(p, f.name) for f in Profile._meta.get_fields()}
		form = ProfileForm(initial=initialDict)
		return render(request, 'virtualstuddybuddy/editProfile.html', context = {"form": form})

def get_profiles(request):
	return render(request, 'virtualstuddybuddy/viewAllProfiles.html', context={'allProfiles': Profile.objects.all()})

def manual_match(request, pk):
	#matcher=Profile.objects.all()[0]
	matcher = Profile.objects.all().filter(username=request.user.get_username())[0]
	matchee=get_object_or_404(Profile, pk=pk)
	matchee.matches.append(matcher)
	matcher_email=request.user.email
	matchee.matches_emails.append(matcher_email)

	return render(request, 'virtualstuddybuddy/match.html', context={'matcher': matcher, 'matchee': matchee})