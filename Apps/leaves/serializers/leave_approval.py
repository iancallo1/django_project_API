from rest_framework import serializers
from ..models import LeaveApproval, Leave
from .shared import LeaveBasicSerializer

class LeaveApprovalInfoSerializer(serializers.ModelSerializer):
    approver_name = serializers.SerializerMethodField()

    class Meta:
        model = LeaveApproval
        fields = ['approver_name', 'comments', 'approved_at']

    def get_approver_name(self, obj):
        return f"{obj.approver.first_name} {obj.approver.last_name}"

class LeaveApprovalSerializer(serializers.ModelSerializer):
    approver_name = serializers.SerializerMethodField()
    leave = LeaveBasicSerializer(read_only=True)
    leave_id = serializers.PrimaryKeyRelatedField(
        queryset=Leave.objects.filter(status='pending'),
        source='leave',
        write_only=True
    )

    class Meta:
        model = LeaveApproval
        fields = ['id', 'leave', 'leave_id', 'approver_name', 'comments', 'approved_at']
        read_only_fields = ['approved_at', 'approver_name']

    def get_approver_name(self, obj):
        return f"{obj.approver.first_name} {obj.approver.last_name}" 