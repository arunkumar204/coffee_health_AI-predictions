# views.py
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .serializers import (
    HealthPredictionSerializer,
    SignupSerializer,
    LoginSerializer,
    UserSerializer
)
import pandas as pd
import joblib
import os
import json

# ======== LAZY LOADING FOR ML MODELS ========
# Don't load at module level - load only when needed
_model = None
_scaler = None
_features = None

def get_model():
    """Lazy load model only when needed"""
    global _model
    if _model is None:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        MODEL_PATH = os.path.join(BASE_DIR, '../ml_model/saved_model/model.pkl')
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Missing model file: {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
        print(f"✅ Model loaded (scikit-learn v{joblib.__version__})")
    return _model

def get_scaler():
    """Lazy load scaler only when needed"""
    global _scaler
    if _scaler is None:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        SCALER_PATH = os.path.join(BASE_DIR, '../ml_model/saved_model/scaler.pkl')
        if not os.path.exists(SCALER_PATH):
            raise FileNotFoundError(f"Missing scaler file: {SCALER_PATH}")
        _scaler = joblib.load(SCALER_PATH)
    return _scaler

def get_features():
    """Lazy load features only when needed"""
    global _features
    if _features is None:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FEATURES_PATH = os.path.join(BASE_DIR, '../ml_model/saved_model/features.pkl')
        if not os.path.exists(FEATURES_PATH):
            # If features file doesn't exist, use default features
            _features = ['daily_cups', 'caffeine_per_cup', 'age', 'body_weight', 
                        'sleep_hours', 'exercise_minutes', 'water_intake', 'stress_level']
        else:
            _features = joblib.load(FEATURES_PATH)
    return _features

# ======== Helper Function: JWT Token Generation ========
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

# ======== SPA Landing Page ========
class HomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'index.html')

# ======== Health Prediction API ========
class HealthPredictionViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = HealthPredictionSerializer(data=request.data)
            if serializer.is_valid():
                # LAZY LOAD: Load model, scaler, features only now
                model = get_model()
                scaler = get_scaler()
                features = get_features()
                
                input_df = pd.DataFrame([serializer.validated_data])
                
                # Ensure all required features are present
                for feature in features:
                    if feature not in input_df.columns:
                        input_df[feature] = 0  # Default value for missing features
                
                input_df = input_df[features]  # Ensure correct columns
                input_scaled = scaler.transform(input_df)
                prediction = model.predict(input_scaled)[0]
                
                return Response({
                    'success': True,
                    'stress_level': float(prediction),
                    'message': 'Prediction successful'
                }, status=status.HTTP_200_OK)
            
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except FileNotFoundError as e:
            return Response({
                'success': False,
                'message': f'Model files not found: {str(e)}. Please train the model first.'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Prediction error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ======== Authentication APIs ========
class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body) if request.body else request.data
            serializer = SignupSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                login(request, user)  # Auto-login
                tokens = get_tokens_for_user(user)
                return Response({
                    'success': True,
                    'message': 'Registration successful',
                    'user': UserSerializer(user).data,
                    'token': tokens['access']
                }, status=status.HTTP_201_CREATED)
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body) if request.body else request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                user = authenticate(
                    username=serializer.validated_data['username'],
                    password=serializer.validated_data['password']
                )
                if user:
                    login(request, user)
                    tokens = get_tokens_for_user(user)
                    return Response({
                        'success': True,
                        'message': 'Login successful',
                        'user': UserSerializer(user).data,
                        'token': tokens['access']
                    }, status=status.HTTP_200_OK)
                return Response({
                    'success': False,
                    'message': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': False, 'errors': serializer.errors}, status=400)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'success': True, 'message': 'Logged out successfully'}, status=200)

# ======== User Profile API ========
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'success': True, 'user': UserSerializer(request.user).data}, status=200)

# ======== SPA Views ========
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'index.html')  # SPA handles routing

# ======== Health Check Endpoint (for Render) ========
class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Simple health check for Render's monitoring"""
        return Response({
            'status': 'healthy',
            'service': 'CoffeeHealth AI API',
            'timestamp': pd.Timestamp.now().isoformat()
        }, status=status.HTTP_200_OK)

# Legacy Django logout for web
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

