from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import LeaveType, Leave, LeaveApproval
from .serializers import LeaveTypeSerializer, LeaveSerializer, LeaveApprovalSerializer, LeaveDetailSerializer

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

    def get_serializer_class(self):
        """
        Use different serializers for different actions
        """
        if self.action == 'retrieve':
            return LeaveDetailSerializer
        return LeaveSerializer

    def get_queryset(self):
        """
        Filter leaves based on user's role
        """
        user = self.request.user
        if not user.is_authenticated:
            return Leave.objects.none()
        
        # Managers and admins can see all leaves
        if user.is_manager or user.is_staff:
            return Leave.objects.all()
        
        # Regular employees can only see their own leaves
        return Leave.objects.filter(employee__user=user)

    def perform_create(self, serializer):
        """
        Always set the employee to the authenticated user's employee record
        """
        serializer.save(employee=self.request.user.employee)

    def get_permissions(self):
        """
        Set permissions based on the action
        """
        if self.action in ['create', 'list', 'retrieve']:
            # Any authenticated user can create and view their own leaves
            return [permissions.IsAuthenticated()]
        else:
            # Only managers/admins can update/delete leaves
            return [permissions.IsAuthenticated(), IsManagerOrAdmin()]

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
        if new_status not in ['approved', 'rejected', 'cancelled']:
            return Response(
                {'error': 'Invalid status. Must be either "approved", "rejected", or "cancelled"'},
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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter approvals based on user's role
        """
        user = self.request.user
        if not user.is_authenticated:
            return LeaveApproval.objects.none()
        
        # Managers and admins can see approvals they've made
        if user.is_manager or user.is_staff:
            return LeaveApproval.objects.filter(approver=user)
        
        # Regular employees can see approvals for their own leaves
        return LeaveApproval.objects.filter(leave__employee__user=user)

    def get_permissions(self):
        """
        Set permissions based on the action
        """
        if self.action in ['list', 'retrieve']:
            # Any authenticated user can view approvals
            return [permissions.IsAuthenticated()]
        else:
            # Only managers/admins can create/update/delete approvals
            return [permissions.IsAuthenticated(), IsManagerOrAdmin()]

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