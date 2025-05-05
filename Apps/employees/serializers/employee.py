from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from ..models import Employee

User = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'}
    )
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    
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
        # Only validate password if it's being set
        if 'password' in attrs and 'confirm_password' in attrs:
            if attrs['password'] != attrs['confirm_password']:
                raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Check username uniqueness only if it's being set
        if 'username' in attrs:
            if User.objects.filter(username=attrs['username']).exists():
                raise serializers.ValidationError({"username": "This username is already taken."})
        
        # Check email uniqueness only if it's being set
        if 'email' in attrs:
            if User.objects.filter(email=attrs['email']).exists():
                raise serializers.ValidationError({"email": "This email is already registered."})
        
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
        validated_data.pop('confirm_password', None)  # Remove confirm_password as it's not needed
        
        try:
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
        except IntegrityError:
            raise serializers.ValidationError({"username": "This username is already taken."})

    def update(self, instance, validated_data):
        # Update user fields if provided
        user = instance.user
        if 'username' in validated_data:
            user.username = validated_data.pop('username')
        if 'email' in validated_data:
            user.email = validated_data.pop('email')
        if 'password' in validated_data:
            user.set_password(validated_data.pop('password'))
        if 'first_name' in validated_data:
            user.first_name = validated_data.pop('first_name')
        if 'last_name' in validated_data:
            user.last_name = validated_data.pop('last_name')
        
        # Remove confirm_password if present
        validated_data.pop('confirm_password', None)
        
        # Save user changes
        user.save()
        
        # Update employee fields
        return super().update(instance, validated_data) 