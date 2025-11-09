from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
import datetime
# Create your models here.

AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('username')._unique = False
class AppUser(AbstractUser):
    #user model
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name',]
    backend = 'App.views.UserBackend'
    prof_title = models.CharField(max_length=200, blank=True)
    prof_summary = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)

class Education(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=20)
    field = models.CharField(max_length=500)
    institution = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    startDate = models.CharField(max_length=250)
    endDate = models.CharField(max_length=230)
    gpa = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=23)
    num = models.CharField(max_length=230)

class Experience(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='experience')
    id = models.CharField(max_length=200, primary_key=True)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    startDate = models.CharField(max_length=200)
    endDate = models.CharField(max_length=200, blank=True)
    isCurrentRole = models.BooleanField(default=False)

class Project(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='projects')
    id = models.CharField(max_length=200, primary_key=True)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    technologies = models.TextField(max_length=500)
    startDate = models.CharField(max_length=200)
    endDate = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=200)