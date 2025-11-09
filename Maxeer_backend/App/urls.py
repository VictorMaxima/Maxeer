from django.urls import path
from .views import (
    LoginView, LogoutView, RegisterView, VerifyEmail, CustomTokenObtainPairView,
    CreateEducationView, EducationView, EducationDeleteView, EducationUpdateView,
    CreateExperienceView, ExperienceView, ExperienceDeleteView, ExperienceUpdateView,
    CreateProjectView, ProjectView, ProjectDeleteView, ProjectUpdateView, PortfolioView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken import views
urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/register', RegisterView.as_view(), name='register'),
    path('api/verify-email/', VerifyEmail.as_view(), name='email-verify'),
     path('api/token-auth/', views.obtain_auth_token, name='api_token_auth'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'
     ),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/edu/add', CreateEducationView.as_view(), name='add_education'),
    path('api/edu/all', EducationView.as_view(), name='list_education'),
    path('api/edu/<str:num>/change', EducationUpdateView.as_view(), name='education-update'),
    path('api/edu/<str:num>/delete', EducationDeleteView.as_view(), name='education-delete'),
    path('api/exp/add', CreateExperienceView.as_view(), name='add_experience'),
    path('api/exp/all', ExperienceView.as_view(), name='list_experience'),
    path('api/exp/<str:id>/change', ExperienceUpdateView.as_view(), name='experience-update'),
    path('api/exp/<str:id>/delete', ExperienceDeleteView.as_view(), name='experience-delete'),
    path('api/prj/add', CreateProjectView.as_view(), name='add_project'),
    path('api/prj/all', ProjectView.as_view(), name='list_project'),
    path('api/prj/<str:id>/change', ProjectUpdateView.as_view(), name='project-update'),
    path('api/prj/<str:id>/delete', ProjectDeleteView.as_view(), name='project-delete'),
    path('api/portfolio/<str:id>', PortfolioView.as_view(), name='portfolio-view'),
]