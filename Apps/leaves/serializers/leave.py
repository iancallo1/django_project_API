from rest_framework import serializers
from ..models import Leave, LeaveType
from employees.serializers import EmployeeSerializer
from .leave_type import LeaveTypeSerializer
from .leave_approval import LeaveApprovalInfoSerializer

class LeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    leave_type_id = serializers.PrimaryKeyRelatedField(
        queryset=LeaveType.objects.all(),
        source='leave_type',
        write_only=True
    )
    approval = LeaveApprovalInfoSerializer(read_only=True)

    class Meta:
        model = Leave
        fields = [
            'id', 'employee_name', 'leave_type_name', 'leave_type_id',
            'start_date', 'end_date', 'reason', 'status', 'created_at',
            'updated_at', 'duration', 'approval'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at', 'employee_name', 'approval']

    def get_employee_name(self, obj):
        return f"{obj.employee.user.first_name} {obj.employee.user.last_name}"

class LeaveDetailSerializer(LeaveSerializer):
    """Detailed serializer for single leave view"""
    employee = EmployeeSerializer(read_only=True)
    leave_type = LeaveTypeSerializer(read_only=True)

    class Meta(LeaveSerializer.Meta):
        fields = LeaveSerializer.Meta.fields + ['employee', 'leave_type'] 