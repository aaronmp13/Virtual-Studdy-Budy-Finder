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
from django.contrib.auth import logout

# Create your views here.

from django.http import HttpResponse
from .models import *

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
            #p.username = request.user.get_username()
            request.user.username = p.username
            p.save()
            users_inbox=UserInbox(profile=p) #Create an inbox for the new profile
            users_inbox.save() #save the new inbox
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

def logout_view(request):
    if not request.user.is_authenticated: #redirects to login if they haven't done that yet
        return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')
    logout(request)
    return HttpResponseRedirect('/virtualstudybuddy')

def editProfile(request):
    if not request.user.is_authenticated: #redirects to login if they haven't done that yet
        return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')
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
        initialDict = {f.name:getattr(p, f.name) for f in Profile._meta.get_fields() if f.name!="studygroup" and f.name!="usermessage"}
        form = ProfileForm(initial=initialDict)
        return render(request, 'virtualstuddybuddy/editProfile.html', context = {"form": form})

def get_profiles(request):
    if not request.user.is_authenticated: #redirects to login if they haven't done that yet
        return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')
    allProfiles = Profile.objects.all()
    query = ""
    if request.method=='POST':
        form = SearchBarForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            q = set(query.split())

            allProfiles = []
            for p in Profile.objects.all(): #I think this is pretty slow but luckily we are not gonna have 10000 profiles
                profileString = str(p)
                flag = True
                for s in q:
                    if s not in profileString:
                        flag = False
                if flag:
                    allProfiles.append(p)
        #return HttpResponseRedirect('/virtualstudybuddy/viewProfiles')
    form = SearchBarForm(initial = {'query':query})
    return render(request, 'virtualstuddybuddy/viewAllProfiles.html', context={'allProfiles': allProfiles, 'form': form})

def manual_match(request, pk): #FIX THIS
    if not request.user.is_authenticated: #redirects to login if they haven't done that yet
        return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')
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
    if not request.user.is_authenticated: #redirects to login if they haven't done that yet
        return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')
    current_user = Profile.objects.all().filter(username=request.user.get_username())[0]
    group_to_join= get_object_or_404(StudyGroup, pk=pk)
    group_to_join.profiles.add(current_user)
    return HttpResponseRedirect('/virtualstudybuddy/mygroups')

# class GroupView(generic.DetailView):
# 	model = StudyGroup
# 	template_name = 'virtualstuddybuddy/group.html'

def group_page(request, pk):
    if not request.user.is_authenticated: #redirects to login if they haven't done that yet
        return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')
    current_group=get_object_or_404(StudyGroup, pk=pk)
    current_user=Profile.objects.all().filter(username=request.user.get_username())[0]
    in_group=False
    current_inbox = current_group.groupinbox
    messages_to_group=current_inbox.groupmessage_set.all()
    form = GroupMessageForm()

    if request.method=="POST":
        form = GroupMessageForm(request.POST)
        mess = ""
        if form.is_valid():
            mess = form.cleaned_data['message']
            m = GroupMessage(message = mess, sender_username = current_user.username, recipient_group = current_group.group_name, groupinbox = current_inbox)
            m.save()
        return HttpResponseRedirect('/virtualstudybuddy/group/'+str(pk))
        
    if current_user in current_group.profiles.all():
        in_group=True

    return render(request, 'virtualstuddybuddy/group.html', context={'studygroup': current_group, 'inGroup': in_group, 'allMessages': messages_to_group, 'form':form})

def creategroup(request):
    if not request.user.is_authenticated: #redirects to login if they haven't done that yet
        return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')
    current_user = Profile.objects.all().filter(username=request.user.get_username())[0]
    if request.method == 'POST': #If a person filled out the form
        form = GroupForm(request.POST)
        g = None
        if form.is_valid():
            g = form.save()
            g.profiles.add(current_user)
            group_inbox=GroupInbox(group=g) #Create an inbox for the new group
            group_inbox.save() #save the new inbox
            print(str(group_inbox))
            g.save()
        else: #If the form is invalid, just make them fill it out again
            form = GroupForm(request.POST)
            return render(request, 'virtualstuddybuddy/creategroup.html', {'form':form})
        return HttpResponseRedirect('/virtualstudybuddy/mygroups')
    else:
        form = GroupForm()
        return render(request, 'virtualstuddybuddy/creategroup.html', context = {"form": form})

def editgroup(request, pk):
    if not request.user.is_authenticated: #redirects to login if they haven't done that yet
        return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')
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
    if not request.user.is_authenticated: #redirects to login if they haven't done that yet
        return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')
    current_user = Profile.objects.all().filter(username=request.user.get_username())[0]
    current_group = get_object_or_404(StudyGroup, pk=pk)
    current_group.profiles.remove(current_user)
    current_group.save()

    if current_group.profiles.count()==0:
        current_group.delete()

    return HttpResponseRedirect('/virtualstudybuddy/mygroups')

def meetgroup(request, pk):
    if not request.user.is_authenticated: #redirects to login if they haven't done that yet
        return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')
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

def chatindex(request):
    return render(request, 'virtualstuddybuddy/chatindex.html')

def room(request, room_name):
    return render(request, 'virtualstuddybuddy/room.html', {
        'room_name': room_name
    })

def my_inbox(request):
    if not request.user.is_authenticated: #redirects to login if they haven't done that yet
        return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')

    current_user = Profile.objects.all().filter(username=request.user.get_username())[0]
    current_inbox = current_user.userinbox
    messages_to_user=current_inbox.usermessage_set.all()
    messages_from_user=current_user.usermessage_set.all() # Reminder: I didn't define an outbox, just simply established a foreign key relationship
    return render(request, "virtualstuddybuddy/inbox.html", context={'allMessages': messages_to_user, 'outgoingMessages': messages_from_user})

def compose_message(request, target=None):
    if not request.user.is_authenticated: #redirects to login if they haven't done that yet
        return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')
    current_user = Profile.objects.all().filter(username=request.user.get_username())[0]

    if request.method == 'POST': #Message Sent
        form = MessageForm(request.POST)
        g = None
        if form.is_valid():
            g = form.save()
            g.sender_username=current_user.username
            recipient=Profile.objects.all().filter(username=g.recipient_username)[0]
            recipient_inbox=recipient.userinbox
            g.save()

            sender_username=current_user.username
            subject=g.subject
            recipient_username=g.recipient_username
            message=g.message

            x=UserMessage(sender_username=sender_username, subject=subject, recipient_username=recipient_username,
                          message=message, userinbox=None)
            x.save()

            recipient_inbox.usermessage_set.add(g)
            current_user.usermessage_set.add(x) #important distinction here, this is the outbox (no model for outbox like there is for inbox)
        else: #If the form is invalid, just make them fill it out again
            form = MessageForm(request.POST)
            return render(request, 'virtualstuddybuddy/composemessage.html', context={'form':form})

        return HttpResponseRedirect('/virtualstudybuddy/inbox')
    else:
        form = MessageForm()
        if target:
            form = MessageForm(initial = {'recipient_username':target})
        return render(request, 'virtualstuddybuddy/composemessage.html', context = {"form": form})

def delete_message(request, pk):
    if not request.user.is_authenticated: #redirects to login if they haven't done that yet
        return HttpResponseRedirect('/virtualstudybuddy/accounts/google/login/')
    message = get_object_or_404(UserMessage, pk=pk)
    message.delete()
    return HttpResponseRedirect('/virtualstudybuddy/inbox')