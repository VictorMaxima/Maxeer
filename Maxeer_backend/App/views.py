from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.shortcuts import render
from django.contrib.auth.backends import BaseBackend
from .serializers import (
    RegisterSerializer,  LoginSerializer, EducationCreate, EducationList,
    EducationUpdate, ExperienceCreate, ExperienceList, ExperienceUpdate,
    ProjectUpdate, ProjectCreate, ProjectList, PortfolioSerializer)
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import AppUser, Education, Experience, Project
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class UserBackend(BaseBackend):
    #user backend for authentication

    def authenticate(request, email=None, password=None):
        try:
            user = AppUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except AppUser.DoesNotExist:
            print(AppUser.objects) #for debugging
            return None
  

    def get_user(self, client_id):
        try:
            return AppUser.objects.get(pk=user_id)
        except AppUser.DoesNotExist:
            return None

class LoginView(APIView):
    #login view to be used as api end point
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = UserBackend.authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "Logged in successfully"})
        
        return Response({"error": "Invalid credentials"})

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})

class RegisterView(APIView):

    @swagger_auto_schema(
        request_body = RegisterSerializer,
        responses={
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created. Please verify your email.',
                            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
class VerifyEmail(APIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = AppUser.objects.get(email=user_id)
            if not user.is_active:
                user.is_active = True
                user.save()
            return render(request, "verify.html", {
        "message": "Email successfully verified! ",
        "redirect_url": "/"
    })
        except TokenError:
            return render(request, "alert_page.html", {
        "message": "expired Token",
        "redirect_url": "/home/"
    })
        
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        user = UserBackend.authenticate(request, email=request.data['email'], password=request.data['password'])
        if user is not None:
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token
            print(type(user))
            return Response(
                {
                    'access_token': str(access_token),
                    'refresh_token': str(refresh_token),
                    'user_id': user.id,
                }
            )
        return Response({'error': 'Invalid credentials'})

class CreateEducationView(CreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationCreate
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        self.instance = serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = self.instance.__dict__
        del data["_state"]
        return Response(data, status=status.HTTP_201_CREATED)

class EducationUpdateView(CreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationUpdate
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, num):
        return get_object_or_404(Education, num=num)
    
    def patch(self, request, num):
        edu = self.get_object(num)
        serializer =EducationUpdate(edu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EducationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        edus = request.user.education.all()
        serializer = EducationList(edus, many=True)
        return Response(serializer.data)

class EducationDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, num):
        edu = get_object_or_404(Education, num=num, user=request.user)
        edu.delete()
        return Response({
        'message': 'successfully deleted'
    })

class CreateExperienceView(CreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceCreate
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        self.instance = serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = self.instance.__dict__
        del data["_state"]
        return Response(data, status=status.HTTP_201_CREATED)

class ExperienceUpdateView(CreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceUpdate
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, id):
        return get_object_or_404(Experience, id=id)
    
    def patch(self, request, id):
        exp = self.get_object(id)
        serializer =ExperienceUpdate(exp, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExperienceView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        exps = request.user.experience.all()
        serializer = ExperienceList(exps, many=True)
        return Response(serializer.data)

class ExperienceDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        exp = get_object_or_404(Experience, id=id, user=request.user)
        exp.delete()
        return Response({
        'message': 'successfully deleted'
    })

class CreateProjectView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreate
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        self.instance = serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = self.instance.__dict__
        del data["_state"]
        return Response(data, status=status.HTTP_201_CREATED)

class ProjectUpdateView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectUpdate
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, id):
        return get_object_or_404(Project, id=id)
    
    def patch(self, request, id):
        prj = self.get_object(id)
        serializer =ProjectUpdate(prj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        prjs = request.user.projects.all()
        serializer = ProjectList(prjs, many=True)
        return Response(serializer.data)

class ProjectDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        prj = get_object_or_404(Project, id=id, user=request.user)
        prj.delete()
        return Response({
        'message': 'successfully deleted'
    })

class PortfolioView(APIView):
    def get(self, request, id):
        user = get_object_or_404(AppUser.objects.prefetch_related(
                'education', 
                'experience', 
                'projects'
            ),id=id)
        serializer = PortfolioSerializer(user)
        return Response(serializer.data)

def index(request):
    return render(request, "index.html")