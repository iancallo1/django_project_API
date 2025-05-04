from rest_framework import viewsets, permissions
from .models import LeaveType, Leave
from .serializers import LeaveTypeSerializer, LeaveSerializer

class LeaveTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows leave types to be viewed or edited.
    """
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

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
        if user.is_manager:
            return Leave.objects.all()
        return Leave.objects.filter(employee__user=user) 