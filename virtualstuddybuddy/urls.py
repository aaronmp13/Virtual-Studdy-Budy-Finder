from django.urls import path, include
from django.contrib import admin

from . import views

appname = "virtualstudybuddy"
urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls), #admin
    path('accounts/', include('allauth.urls')), #google login
    path('signup/', views.signup, name = "signup"),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'), #profile page
    path('editProfile/', views.editProfile, name = "editProfile"),
    path('viewProfiles/', views.get_profiles, name="viewProfiles"),
    path('viewProfiles/redirect/<int:pk>/', views.ProfileView.as_view(), name='profile'),  # probably don't need this anymore
    path('match/<int:pk>', views.manual_match, name="manualMatch")
]