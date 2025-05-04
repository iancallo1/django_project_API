from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import LeaveType, Leave, LeaveApproval
from .serializers import LeaveTypeSerializer, LeaveSerializer, LeaveApprovalSerializer

class IsManagerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow managers or admins to access the view.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_manager or request.user.is_staff

class LeaveTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows leave types to be viewed or edited.
    """
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdmin]

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
        if not user.is_authenticated:
            return Leave.objects.none()
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

    def update(self, request, *args, **kwargs):
        """
        Handle leave approval/rejection
        """
        instance = self.get_object()
        
        # Only managers and admins can approve/reject leaves
        if not (request.user.is_manager or request.user.is_staff):
            return Response(
                {'error': 'Only managers and admins can approve/reject leaves'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if leave is already processed
        if instance.status != 'pending':
            return Response(
                {'error': 'This leave request has already been processed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the new status from request data
        new_status = request.data.get('status')
        if new_status not in ['approved', 'rejected']:
            return Response(
                {'error': 'Invalid status. Must be either "approved" or "rejected"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create leave approval record
        LeaveApproval.objects.create(
            leave=instance,
            approver=request.user,
            comments=request.data.get('comments', '')
        )

        # Update leave status
        instance.status = new_status
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class LeaveApprovalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows leave approvals to be viewed or edited.
    """
    queryset = LeaveApproval.objects.all()
    serializer_class = LeaveApprovalSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdmin]

    def get_queryset(self):
        """
        Show all pending leaves for managers/admins
        """
        user = self.request.user
        if not user.is_authenticated:
            return LeaveApproval.objects.none()
        if user.is_manager or user.is_staff:
            return LeaveApproval.objects.filter(approver=user)
        return LeaveApproval.objects.none()

    def create(self, request, *args, **kwargs):
        """
        Create a new leave approval
        """
        leave_id = request.data.get('leave_id')
        try:
            leave = Leave.objects.get(id=leave_id)
        except Leave.DoesNotExist:
            return Response(
                {'error': 'Leave request not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if leave.status != 'pending':
            return Response(
                {'error': 'This leave request has already been processed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the approval record
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Update the leave status to approved
        leave.status = 'approved'
        leave.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
        Set the approver when creating a new approval
        """
        serializer.save(approver=self.request.user) 