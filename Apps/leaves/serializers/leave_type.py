from rest_framework import serializers
from ..models import LeaveType

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ['id', 'name', 'description', 'max_days'] 