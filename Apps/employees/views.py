from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Department, Position, Employee
from .serializers import DepartmentSerializer, PositionSerializer, EmployeeSerializer

User = get_user_model()

class IsManagerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow managers or admins to access the view.
    """
    def has_permission(self, request, view):
        # First check if user is authenticated
        if not request.user.is_authenticated:
            return False
        # Then check if user is manager or admin
        return request.user.is_manager or request.user.is_staff

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows departments to be viewed or edited.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdmin]

class PositionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows positions to be viewed or edited.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdmin]

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employees to be viewed or edited.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an employee and their associated user account.
        """
        try:
            instance = self.get_object()
            # Get the associated user before deleting the employee
            user = instance.user
            
            # Delete the employee (this will cascade delete the user due to OneToOneField)
            self.perform_destroy(instance)
            
            # If it's a browsable API request, redirect to the list view
            if request.accepted_renderer.format == 'browsable':
                return HttpResponseRedirect(reverse('employee-list'))
            
            # For API requests, return JSON response
            return Response(
                {
                    "detail": "Employee and associated user account deleted successfully.",
                    "deleted_employee": {
                        "id": instance.id,
                        "username": user.username,
                        "name": f"{user.first_name} {user.last_name}"
                    }
                },
                status=status.HTTP_200_OK
            )
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Employee not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": f"Error deleting employee: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get', 'delete'])
    def delete_employee(self, request, pk=None):
        """
        Custom action to preview and delete an employee.
        GET: Preview employee data before deletion
        DELETE: Delete the employee and their user account
        """
        employee = self.get_object()
        
        if request.method == 'GET':
            # Return detailed information about the employee to be deleted
            return Response({
                "detail": "This action will delete the following employee and their user account:",
                "employee": {
                    "id": employee.id,
                    "username": employee.user.username,
                    "name": f"{employee.user.first_name} {employee.user.last_name}",
                    "email": employee.user.email,
                    "join_date": employee.join_date,
                    "phone_number": employee.phone_number
                },
                "warning": "This action cannot be undone. The employee's user account will also be deleted."
            })
        
        return self.destroy(request, pk=pk)

    def get_queryset(self):
        """
        Filter employees based on user's role
        """
        user = self.request.user
        if not user.is_authenticated:
            return Employee.objects.none()  # Return empty queryset for anonymous users
        if user.is_manager or user.is_staff:
            return Employee.objects.all()
        return Employee.objects.filter(user=user) 