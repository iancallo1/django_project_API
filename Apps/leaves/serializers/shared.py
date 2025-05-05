from rest_framework import serializers
from ..models import Leave

class LeaveBasicSerializer(serializers.ModelSerializer):
    """Basic serializer for leave information used in other serializers"""
    employee_name = serializers.SerializerMethodField()
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)

    class Meta:
        model = Leave
        fields = ['id', 'employee_name', 'leave_type_name', 'start_date', 'end_date', 'status']

    def get_employee_name(self, obj):
        return f"{obj.employee.user.first_name} {obj.employee.user.last_name}" 