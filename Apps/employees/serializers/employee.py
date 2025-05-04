from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from ..models import Employee
import time

User = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    
    # Read-only fields for user information
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'username', 'email', 'password', 'confirm_password',
            'first_name', 'last_name', 'join_date', 'phone_number',
            'user_username', 'user_email', 'user_first_name', 'user_last_name'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # Generate a unique username by appending a timestamp
        base_username = attrs['username']
        timestamp = str(int(time.time()))[-4:]  # Use last 4 digits of timestamp
        attrs['username'] = f"{base_username}{timestamp}"
        
        return attrs

    def create(self, validated_data):
        # Create user first
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'is_employee': True,
        }
        validated_data.pop('confirm_password')  # Remove confirm_password as it's not needed
        
        # Create user with proper password hashing
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_employee=True
        )
        
        # Create employee linked to the user
        validated_data['user'] = user
        return super().create(validated_data) 