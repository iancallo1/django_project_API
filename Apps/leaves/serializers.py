from rest_framework import serializers
from .models import LeaveType, Leave, LeaveApproval
from employees.serializers import EmployeeSerializer
from employees.models import Employee
from authentication.serializers import UserSerializer

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ['id', 'name', 'description', 'max_days']

class LeaveSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        source='employee',
        write_only=True
    )
    leave_type = LeaveTypeSerializer(read_only=True)
    leave_type_id = serializers.PrimaryKeyRelatedField(
        queryset=LeaveType.objects.all(),
        source='leave_type',
        write_only=True
    )

    class Meta:
        model = Leave
        fields = [
            'id', 'employee', 'employee_id', 'leave_type', 'leave_type_id',
            'start_date', 'end_date', 'reason', 'status', 'created_at',
            'updated_at', 'duration'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at']

class LeaveApprovalSerializer(serializers.ModelSerializer):
    approver = UserSerializer(read_only=True)
    leave = LeaveSerializer(read_only=True)
    leave_id = serializers.PrimaryKeyRelatedField(
        queryset=Leave.objects.filter(status='pending'),
        source='leave',
        write_only=True
    )

    class Meta:
        model = LeaveApproval
        fields = ['id', 'leave', 'leave_id', 'approver', 'comments', 'approved_at']
        read_only_fields = ['approved_at', 'approver'] 