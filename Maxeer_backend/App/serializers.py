from rest_framework import serializers
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .models import AppUser, Education, Experience, Project
from .mail_utils import send_resend_email

class LoginSerializer(serializers.ModelSerializer):
    #serializer for logging in
    password = serializers.CharField(write_only=True)
    class Meta:
        model = AppUser
        fields = ['email', 'password']


class RegisterSerializer(serializers.ModelSerializer):
    #serializer for creating users
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AppUser
        fields = ['first_name', 'last_name', 'prof_title', 'prof_summary', 'email', 'password', 'phone', 'location']

    def create(self, validated_data):
        user = AppUser.objects.create_user(
            username=validated_data['first_name']+validated_data['last_name'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            prof_title=validated_data['prof_title'],
            prof_summary=validated_data['prof_summary'],
            password=validated_data['password'],
            location=validated_data['location'],
            phone=validated_data['phone'],
      # Inactive until verified
            is_active=False
        )
        self.send_verification_email(user)
        return user

    def send_verification_email(self, user):
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(self.context['request']).domain
        relative_link = reverse('email-verify')
        absurl = f'http://{current_site}{relative_link}?token={str(token)}'
        subject = 'Verify your email'
        message = f'Hi {user.first_name} Click the link to verify your account: {absurl}'
        html = f"""
<div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f9fafb; padding: 30px; border-radius: 10px; max-width: 600px; margin: auto; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
  <h2 style="color: #1e293b; text-align: center;">Welcome to <span style="color: #2563eb;">Maxeer</span>!</h2>
  
  <p style="font-size: 16px; color: #334155;">
    Hi <strong>{user.username}</strong>,
  </p>

  <p style="font-size: 16px; color: #334155;">
    We’re excited to have you on board. To get started, please verify your email by clicking the link below:
  </p>

  <p style="text-align: center; margin: 30px 0;">
    <a href="{absurl}" style="background-color: #2563eb; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 8px; font-weight: bold;">Verify Email</a>
  </p>

  <p style="font-size: 14px; color: #64748b;">
    If you didn’t request this, you can safely ignore this message.
  </p>

  <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 25px 0;">

  <p style="font-size: 13px; color: #94a3b8; text-align: center;">
    © Maxeer • Empowering ideas through technology
  </p>
</div>

    """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        send_resend_email(user.email, subject, message, html)

class EducationCreate(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['num','degree', 'field', 'institution', 'location', 'startDate',
                   'endDate', 'gpa', 'description', 'type']

class EducationList(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class EducationUpdate(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['num','degree', 'field', 'institution', 'location', 'startDate',
                   'endDate', 'gpa', 'description', 'type']


class ExperienceCreate(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'position', 'company', 'location', 'description',
                  'startDate', 'endDate', 'isCurrentRole']

class ExperienceList(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

class ExperienceUpdate(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [ 'position', 'company', 'location', 'description',
                  'startDate', 'endDate', 'isCurrentRole']

class ProjectCreate(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'company', 'description', 'technologies',
                  'startDate', 'endDate', 'status', 'url']

class ProjectList(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectUpdate(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'company', 'description', 'technologies',
                  'startDate', 'endDate', 'status', 'url']

class PortfolioSerializer(serializers.ModelSerializer):
    education = EducationList(many=True, read_only=True)
    experience = ExperienceList(many=True, read_only=True)  
    projects = ProjectList(many=True, read_only=True)   
    class Meta: 
        model = AppUser
        fields = ['first_name', 'last_name', 'prof_title', 'prof_summary', 'id',
                   'education', 'experience', 'projects', 'email', 'phone', 'location']
