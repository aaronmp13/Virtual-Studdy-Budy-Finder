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
]