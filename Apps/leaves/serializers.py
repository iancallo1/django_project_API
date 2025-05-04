from rest_framework import serializers
from .models import LeaveType, Leave
from employees.serializers import EmployeeSerializer

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
    approved_by = EmployeeSerializer(read_only=True)
    approved_by_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        source='approved_by',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Leave
        fields = [
            'id', 'employee', 'employee_id', 'leave_type', 'leave_type_id',
            'start_date', 'end_date', 'reason', 'status', 'approved_by',
            'approved_by_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at'] 