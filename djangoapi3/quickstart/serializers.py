from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Employee, LeaveType, Leave, LeaveApproval


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Employee
        fields = ['id', 'user', 'department', 'position', 'join_date', 'remaining_leaves']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            employee = Employee.objects.create(user=user, **validated_data)
            return employee
        raise serializers.ValidationError(user_serializer.errors)


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ['id', 'name', 'description', 'max_days']


class LeaveSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    leave_type = LeaveTypeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        source='employee',
        write_only=True
    )
    leave_type_id = serializers.PrimaryKeyRelatedField(
        queryset=LeaveType.objects.all(),
        source='leave_type',
        write_only=True
    )

    class Meta:
        model = Leave
        fields = ['id', 'employee', 'employee_id', 'leave_type', 'leave_type_id', 
                 'start_date', 'end_date', 'reason', 'status', 'created_at', 'updated_at']


class LeaveApprovalSerializer(serializers.ModelSerializer):
    leave = LeaveSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)
    leave_id = serializers.PrimaryKeyRelatedField(
        queryset=Leave.objects.all(),
        source='leave',
        write_only=True
    )

    class Meta:
        model = LeaveApproval
        fields = ['id', 'leave', 'leave_id', 'approved_by', 'approved_at', 'comments']