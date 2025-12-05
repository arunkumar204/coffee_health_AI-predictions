# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
import pandas as pd

# Authentication Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'date_joined')

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists."})
        
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

# Health Prediction Serializer (your existing code)
class HealthPredictionSerializer(serializers.Serializer):
    # Add your existing fields here based on your model features
    # Example fields (adjust according to your model):
    age = serializers.IntegerField(required=True)
    sleep_duration = serializers.FloatField(required=True)
    quality_of_sleep = serializers.FloatField(required=True)
    physical_activity_level = serializers.FloatField(required=True)
    stress_level = serializers.FloatField(required=True)
    heart_rate = serializers.IntegerField(required=True)
    daily_steps = serializers.IntegerField(required=True)
    systolic_bp = serializers.IntegerField(required=True)
    diastolic_bp = serializers.IntegerField(required=True)
    # Add more fields as per your model requirements
    
    def validate(self, data):
        # Add any custom validation here
        if data.get('systolic_bp') <= data.get('diastolic_bp'):
            raise serializers.ValidationError("Systolic BP must be greater than diastolic BP")
        
        if data.get('heart_rate') < 40 or data.get('heart_rate') > 200:
            raise serializers.ValidationError("Heart rate must be between 40 and 200")
        
        return data