from rest_framework import viewsets, permissions
from .models import LeaveType, Leave
from .serializers import LeaveTypeSerializer, LeaveSerializer

class IsManagerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow managers or admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_manager or request.user.is_staff)

class LeaveTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows leave types to be viewed or edited.
    """
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [IsManagerOrAdmin]

class LeaveViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows leaves to be viewed or edited.
    """
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter leaves based on user's role
        """
        user = self.request.user
        if user.is_manager or user.is_staff:
            return Leave.objects.all()
        return Leave.objects.filter(employee__user=user)

    def perform_create(self, serializer):
        """
        Set the employee when creating a new leave request
        """
        if not self.request.user.is_manager and not self.request.user.is_staff:
            serializer.save(employee=self.request.user.employee)
        else:
            serializer.save() 