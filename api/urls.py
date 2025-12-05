from django.urls import path
from .views import (
    HomeView,
    HealthPredictionViewSet,
    LoginAPIView,
    SignupAPIView,
    LogoutAPIView,
    UserProfileAPIView,
    DashboardView,
    logout_view
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # SPA Landing Page
    path('', HomeView.as_view(), name='home'),

    # Health Prediction APIs
    path('api/predictions/', HealthPredictionViewSet.as_view(), name='health-prediction'),
    path('api/predictions/predict/', HealthPredictionViewSet.as_view(), name='health-predict'),

    # Authentication APIs
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/signup/', SignupAPIView.as_view(), name='api-signup'),
    path('api/logout/', LogoutAPIView.as_view(), name='api-logout'),

    # User Profile API
    path('api/profile/', UserProfileAPIView.as_view(), name='api-profile'),

    # SPA Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Django built-in logout for web
    path('logout/', logout_view, name='logout'),

    # Password reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='auth/password_reset.html',
             email_template_name='auth/password_reset_email.html',
             subject_template_name='auth/password_reset_subject.txt'
         ), name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='auth/password_reset_done.html'
         ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='auth/password_reset_confirm.html'
         ), name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='auth/password_reset_complete.html'
         ), name='password_reset_complete'),
]
