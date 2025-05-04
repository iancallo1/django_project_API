from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Employee, LeaveType, Leave, LeaveApproval
from .serializers import (
    UserSerializer, EmployeeSerializer, LeaveTypeSerializer,
    LeaveSerializer, LeaveApprovalSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class LeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Leave.objects.all()
        return Leave.objects.filter(employee__user=user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Only admins can approve leaves'}, status=403)
        
        leave = self.get_object()
        if leave.status != 'PENDING':
            return Response({'error': 'Leave is not in pending status'}, status=400)
        
        leave.status = 'APPROVED'
        leave.save()
        
        LeaveApproval.objects.create(
            leave=leave,
            approved_by=request.user,
            comments=request.data.get('comments', '')
        )
        
        return Response({'status': 'Leave approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Only admins can reject leaves'}, status=403)
        
        leave = self.get_object()
        if leave.status != 'PENDING':
            return Response({'error': 'Leave is not in pending status'}, status=400)
        
        leave.status = 'REJECTED'
        leave.save()
        
        LeaveApproval.objects.create(
            leave=leave,
            approved_by=request.user,
            comments=request.data.get('comments', '')
        )
        
        return Response({'status': 'Leave rejected'})


class LeaveApprovalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LeaveApproval.objects.all()
    serializer_class = LeaveApprovalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LeaveApproval.objects.all()
        return LeaveApproval.objects.filter(leave__employee__user=user)