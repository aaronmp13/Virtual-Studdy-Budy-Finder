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
from .googleMeet import createMeeting

# Create your views here.

from django.http import HttpResponse
from .models import Profile

class ProfileView(generic.DetailView):
	model = Profile
	template_name = 'virtualstuddybuddy/profile.html'


def index(request):
    return render(request, 'virtualstuddybuddy/index.html')

def chatindex(request):
    return render(request, 'virtualstuddybuddy/chatindex.html')

def signup(request): #How we handle signups and logins
	if not request.user.is_authenticated: #redirects to login if they haven't done that yet
		return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')
	
	if request.method == 'POST': #If a person filled out the sign up form
		form = ProfileForm(request.POST, request.FILES)
		p = None
		#p = form.save()
		if form.is_valid():
			p = form.save()
			#p.username = request.user.get_username()
			request.user.username = p.username
			p.save()
			request.user.save()
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
			request.user.username = p.username
			request.user.save()
		else:
			# raise DataError(
			# 	form.errors
			# 	)
			form = ProfileForm(request.POST, request.FILES)														
			return render(request, 'virtualstuddybuddy/signup.html', {'form':form})
		return HttpResponseRedirect('/virtualstudybuddy/profile/'+str(p.id)+'/')
	else:
		initialDict = {f.name:getattr(p, f.name) for f in Profile._meta.get_fields() if f.name!="studygroup"}
		form = ProfileForm(initial=initialDict)
		return render(request, 'virtualstuddybuddy/editProfile.html', context = {"form": form})

def get_profiles(request):
	return render(request, 'virtualstuddybuddy/viewAllProfiles.html', context={'allProfiles': Profile.objects.all()})

def manual_match(request, pk): #FIX THIS
	matcher = Profile.objects.all().filter(username=request.user.get_username())[0]

	matchee=get_object_or_404(Profile, pk=pk)
	matchee.matches.append(matcher)
	matcher_email=request.user.email
	matchee.matches_emails.append(matcher_email)

	return render(request, 'virtualstuddybuddy/match.html', context={'matcher': matcher, 'matchee': matchee})

def my_groups(request):
	if not request.user.is_authenticated: #redirects to login if they haven't done that yet
		return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')

	current_user = Profile.objects.all().filter(username=request.user.get_username())[0]
	current_users_groups = current_user.studygroup_set.all()
	return render(request,'virtualstuddybuddy/myGroups.html', context={'currentUser': current_user, 'groups': current_users_groups})

def all_groups(request): #Shows all the groups that the current user is NOT in
	if not request.user.is_authenticated: #redirects to login if they haven't done that yet
		return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')

	all_groups=StudyGroup.objects.all()
	current_user = Profile.objects.all().filter(username=request.user.get_username())[0]
	groups_not_in=[]
	for i in range(0, len(all_groups)):
		if all_groups[i] not in current_user.studygroup_set.all():
			groups_not_in.append(all_groups[i])

	return render(request,'virtualstuddybuddy/allGroups.html', context={'currentUser': current_user, 'groups': groups_not_in})

def join_group(request, pk):
	current_user = Profile.objects.all().filter(username=request.user.get_username())[0]
	group_to_join= get_object_or_404(StudyGroup, pk=pk)
	group_to_join.profiles.add(current_user)
	return HttpResponseRedirect('/virtualstudybuddy/mygroups')

# class GroupView(generic.DetailView):
# 	model = StudyGroup
# 	template_name = 'virtualstuddybuddy/group.html'

def group_page(request, pk):
	current_group=get_object_or_404(StudyGroup, pk=pk)
	current_user=Profile.objects.all().filter(username=request.user.get_username())[0]
	in_group=False
	if current_user in current_group.profiles.all():
		in_group=True
	return render(request, 'virtualstuddybuddy/group.html', context={'studygroup': current_group, 'inGroup': in_group})

def creategroup(request):
	current_user = Profile.objects.all().filter(username=request.user.get_username())[0]
	if request.method == 'POST': #If a person filled out the form
		form = GroupForm(request.POST)
		g = None
		if form.is_valid():
			g = form.save()
			g.profiles.add(current_user)
			g.save()
		else: #If the form is invalid, just make them fill it out again
			form = GroupForm(request.POST)														
			return render(request, 'virtualstuddybuddy/creategroup.html', {'form':form})
		return HttpResponseRedirect('/virtualstudybuddy/mygroups')
	else:
		form = GroupForm()
		return render(request, 'virtualstuddybuddy/creategroup.html', context = {"form": form})

def editgroup(request, pk):
	current_user = Profile.objects.all().filter(username=request.user.get_username())[0]
	current_group = get_object_or_404(StudyGroup, pk=pk)
	if request.method == 'POST': #If a person filled out the form
		form = GroupForm(request.POST, instance = current_group)
		g = None
		if form.is_valid():
			g = form.save()
			g.profiles.add(current_user)
			g.save()
		else: #If the form is invalid, just make them fill it out again
			form = GroupForm(request.POST)														
			return render(request, 'virtualstuddybuddy/creategroup.html', {'form':form})
		return HttpResponseRedirect('/virtualstudybuddy/group/'+str(pk))
	else:
		form = GroupForm()
		return render(request, 'virtualstuddybuddy/creategroup.html', context = {"form": form})

def leavegroup(request, pk):
	current_user = Profile.objects.all().filter(username=request.user.get_username())[0]
	current_group = get_object_or_404(StudyGroup, pk=pk)
	current_group.profiles.remove(current_user)
	current_group.save()
	return HttpResponseRedirect('/virtualstudybuddy/mygroups')

def meetgroup(request, pk):
	current_group = get_object_or_404(StudyGroup, pk=pk)
	if request.method == 'POST': #If a person filled out the form
		form = MeetForm(request.POST)
		if form.is_valid():
			date = form.cleaned_data['date']
			startTime = form.cleaned_data['startTime']
			endTime = form.cleaned_data['endTime']
			emails = []
			for p in current_group.profiles.all():
				username = p.username
				email = User.objects.all().filter(username = username)[0].email
				emails.append(email)
			print(date, startTime, endTime, emails)
			try:
				createMeeting(current_group.group_name,emails, date, startTime, endTime) #uncomment this to enable google meet
			except:
				form.add_error(None, "Not a valid meeting")											
				return render(request, 'virtualstuddybuddy/meetgroup.html', {'form':form})

		else: #If the form is invalid, just make them fill it out again
			form = MeetForm(request.POST)														
			return render(request, 'virtualstuddybuddy/meetgroup.html', {'form':form})
		return HttpResponseRedirect('/virtualstudybuddy/group/'+str(pk))
	else:
		form = MeetForm()
		return render(request, 'virtualstuddybuddy/meetgroup.html', context = {"form": form})
