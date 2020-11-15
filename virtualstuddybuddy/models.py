from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *

# Create your models here.

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
    ('Prefer not to say', 'Prefer not to answer')
]

MAJOR_CHOICES = [
    ('Aerospace Engineering', 'Aerospace Engineering'),
    ('African American and African Studies', 'African American and African Studies'),
    ('American Studies', 'American Studies'),
    ('Anthropology', 'Anthropology'),
    ('Archaeology', 'Archaeology'),
    ('Architectural History', 'Architectural History'),
    ('Architecture', 'Architecture'),
    ('Astronomy', 'Astronomy'),
    ('Bachelor of Interdisciplinary Studies', 'Bachelor of Interdisciplinary Studies'),
    ('Bachelor of Professional Studies in Health Sciences Management',
     'Bachelor of Professional Studies in Health Sciences Management'),
    ('Biology', 'Biology'),
    ('Biomedical Engineering', 'Biomedical Engineering'),
    ('Chemical Engineering', 'Chemical Engineering'),
    ('Chemistry', 'Chemistry'),
    ('Civil Engineering', 'Civil Engineering'),
    ('Classics', 'Classics'),
    ('Cognitive Science', 'Cognitive Science'),
    ('Commerce', 'Commerce'),
    ('Comparative Literature', 'Comparative Literature'),
    ('Computer Engineering', 'Computer Engineering'),
    ('Computer Science (B.A.)', 'Computer Science (B.A.)'),
    ('Computer Science (B.S.)', 'Computer Science (B.S.)'),
    ('Dance', 'Dance'),
    ('Drama', 'Drama'),
    ('East Asian Languages, Literatures and Culture', 'East Asian Languages, Literatures and Culture'),
    ('Economics', 'Economics'),
    ('Electrical Engineering', 'Electrical Engineering'),
    ('Engineering Science', 'Engineering Science'),
    ('English', 'English'),
    ('Environmental Sciences', 'Environmental Sciences'),
    ('Environmental Thought and Practice', 'Environmental Thought and Practice'),
    ('Five-Year Teacher Education Program', 'Five-Year Teacher Education Program'),
    ('French', 'French'),
    ('German', 'German'),
    ('German Studies', 'German Studies'),
    ('Global Studies', 'Global Studies'),
    ('Global Sustainability Minor', 'Global Sustainability Minor'),
    ('Historic Preservation Minor', 'Historic Preservation Minor'),
    ('History', 'History'),
    ('History of Art', 'History of Art'),
    ('Human Biology', 'Human Biology'),
    ('Interdisciplinary Major of Global Studies', 'Interdisciplinary Major of Global Studies'),
    ('Jewish Studies', 'Jewish Studies'),
    ('Kinesiology (BSEd)', 'Kinesiology (BSEd)'),
    ('Landscape Architecture Minor', 'Landscape Architecture Minor'),
    ('Latin American Studies', 'Latin American Studies'),
    ('Linguistics', 'Linguistics'),
    ('Materials Science and Engineering', 'Materials Science and Engineering'),
    ('Mathematics', 'Mathematics'),
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Media Studies', 'Media Studies'),
    ('Medieval Studies', 'Medieval Studies'),
    ('Middle Eastern and South Asian Languages and Cultures', 'Middle Eastern and South Asian Languages and Cultures'),
    ('Music', 'Music'),
    ('Neuroscience', 'Neuroscience'),
    ('Nursing', 'Nursing'),
    ('Philosophy', 'Philosophy'),
    ('Physics', 'Physics'),
    ('Political and Social Thought', 'Political and Social Thought'),
    ('Political Philosophy, Policy, and Law', 'Political Philosophy, Policy, and Law'),
    ('Politics', 'Politics'),
    ('Psychology', 'Psychology'),
    ('Religious Studies', 'Religious Studies'),
    ('Slavic Languages and Literatures', 'Slavic Languages and Literatures'),
    ('Sociology', 'Sociology'),
    ('Spanish', 'Spanish'),
    ('Speech Communication Disorders', 'Speech Communication Disorders'),
    ('Statistics', 'Statistics'),
    ('Studio Art', 'Studio Art'),
    ('Systems Engineering', 'Systems Engineering'),
    ('Urban and Environmental Planning', 'Urban and Environmental Planning'),
    ('Women, Gender & Sexuality', 'Women, Gender & Sexuality'),
    ('Youth & Social Innovation (BSEd)', 'Youth & Social Innovation (BSEd)'),
    ('Other', 'Other'),
]


class Profile(models.Model):
    username = models.CharField(max_length=20, default="", unique=True, validators=[MinLengthValidator(3)])
    name = models.CharField(max_length=50, default="", validators=[MinLengthValidator(1), MaxLengthValidator(50)])
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES, default="",
                              validators=[MinLengthValidator(1), MaxLengthValidator(200)])
    major = models.CharField(max_length=200, choices=MAJOR_CHOICES, default="",
                             validators=[MinLengthValidator(1), MaxLengthValidator(200)])
    age = models.IntegerField(default=20, validators=[MinValueValidator(1), MaxValueValidator(100)])
    description = models.CharField(max_length=2000, default="",
                                   validators=[MinLengthValidator(1), MaxLengthValidator(2000)])
    coursework = models.CharField(max_length=2000, default="",
                                  validators=[MinLengthValidator(1), MaxLengthValidator(2000)])
    classOf = models.IntegerField(default=2023, validators=[MinValueValidator(2020), MaxValueValidator(2024)])
    picture = models.ImageField(upload_to='uploads/', validators=[validate_image_file_extension], blank=True)
    matches = []
    matches_emails = []

    def __str__(self):
        return self.username + " " + self.name + " " + self.gender + " " + self.major + " " + str(
            self.age) + " " + self.description + " " + self.coursework + " " + str(self.classOf)


class StudyGroup(models.Model):
    group_name = models.CharField(max_length=50, default="", unique=True,
                                  validators=[MinLengthValidator(1), MaxLengthValidator(50)])
    group_description = models.CharField(max_length=300, default="",
                                         validators=[MinLengthValidator(1), MaxLengthValidator(2000)])
    profiles = models.ManyToManyField(Profile)

    def __str__(self):
        return self.group_name

class UserInbox(models.Model):
    profile= models.OneToOneField(Profile, on_delete=models.CASCADE) #each user has one inbox, each inbox belongs to one user

    def __str__(self):
        return "Inbox of: "+ self.profile.username

class UserMessage(models.Model):
    sender_username=models.CharField(max_length=20, default="", validators=[MinLengthValidator(3)])
    subject=models.CharField(max_length=50, default="", validators=[MinLengthValidator(1), MaxLengthValidator(50)])
    recipient_username=models.CharField(max_length=20, default="", validators=[MinLengthValidator(3)])
    message=models.CharField(max_length=1000, default="")
    userinbox=models.ForeignKey(UserInbox, null=True, on_delete= models.SET_NULL)

    def __str__(self):
        return self.sender_username + " to " + self.recipient_username + " Subject: " + self.subject